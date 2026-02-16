from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import Session
from .forms import FileForm
import qrcode
from django.conf import settings

from io import BytesIO
import base64

# Create your views here.




def cleanup():
    for s in Session.objects.all():
        s.cleanup()   #model er cleanup method ke call korche

def home(request):
    cleanup()
    session = Session.objects.create(sender_role='Laptop or Desktop')
    qr_url = request.build_absolute_uri(f'/connect/{session.id}/') #url make * aita connect page er url so connect views and url make korte hobe.
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(qr_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
                                                                    # QR image ke HTML page e show korar jonno text format e convert kora.Because browser directly Python image object bujhe na.

    buffer = BytesIO() # BytesIO() holo ekta temporary memory file.
    img.save(buffer, format='PNG')
    qr_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return render(request, 'index.html', {
        'qr_code': qr_base64,
        'session_id': str(session.id)
    })



def connect(request, session_id):
    cleanup()
    session = get_object_or_404(Session, id=session_id)
    if session.is_expired():
        return HttpResponse("This session has expired.", status=410)
    return render(request, 'phone.html', {
        'session_id': session_id
    })



def send_from_phone(request, session_id):
    cleanup()
    session = get_object_or_404(Session, id=session_id)

    if session.is_expired():
        return HttpResponse("Session expired", status=410)
    
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            session.file = request.FILES['file']
            session.status = 'file_sent'
            session.save()
            return render(request, 'sent_file.html', {'form': form, 'session_id': session_id})
    else:
        form = FileForm()
    return render(request, 'sent_file.html', {'session_id': session_id})