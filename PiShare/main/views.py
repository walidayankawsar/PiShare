from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import Session
from .forms import FileForm
import qrcode
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from io import BytesIO
import base64

# Create your views here.


def cleanup():
    for s in Session.objects.all():
        s.cleanup()  # model er cleanup method ke call korche


def home(request):
    cleanup()

    if 'session_id' in request.session:
        session = Session.objects.filter(id=request.session['session_id']).first()
        if not session or session.is_expired():
            session = Session.objects.create(sender_role='Laptop or Desktop')
            request.session['session_id'] = str(session.id)
    else:
        session = Session.objects.create(sender_role='Laptop or Desktop')
        request.session['session_id'] = str(session.id)


    # url make * aita connect page er url so connect views and url make korte hobe.
    qr_url = request.build_absolute_uri(f'/connect/{session.id}/')
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(qr_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    # QR image ke HTML page e show korar jonno text format e convert kora.Because browser directly Python image object bujhe na.

    buffer = BytesIO()  # BytesIO() holo ekta temporary memory file.
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


def send_file(request, session_id):
    cleanup()
    session = get_object_or_404(Session, id=session_id)
    if session.is_expired():
        return HttpResponse("This session has expired.", status=410)
    return render(request, 'sent_file.html', {
        'session_id': session_id
    })


def receive_file(request, session_id):
    cleanup()
    session = get_object_or_404(Session, id=session_id)
    if session.is_expired():
        return HttpResponse("This session has expired.", status=410)

    files = session.files.all().orderby('-uploaded_at')

    return render(request, 'receive.html', {
        'session_id': session_id,
        'files': files
    })



@csrf_exempt
@require_http_methods(["POST"])
def upload_file(request, session_id):
    cleanup()
    session = get_object_or_404(Session, id=session_id)

    if session.is_expired():
        return JsonResponse({'error': 'Session expired'}, status=410)

    if 'file' not in request.FILES:
        return JsonResponse({'error': 'No file provided'}, status=400)

    uploaded_file = request.FILES['file']


    transfer_file = TransferFile.objects.create(
        session = session,
        file = uploaded_file,
        orignal_name = uploaded_file.name,
        file_size = uploaded_file.size
    )


    if session.status == 'waiting':
        session.status = 'file_sent'
        session.save()

    return response