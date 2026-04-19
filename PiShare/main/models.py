from django.db import models
import uuid
from django.utils import timezone
from datetime import timedelta

# Create your models here.




class Session(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='files/', null=True, blank=True)
    sender_role = models.CharField(max_length=20, default='Laptop or Desktop') #laptop or desktop, phone
    status_choices =[
        ('waiting', 'waiting'),
        ('file_sent', 'file_sent'),
        ('expired', 'expired'),
        ('file_receive', 'file_receive')
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='waiting') #waiting, file_sent, expired

    def is_expired(self):
        return timezone.now()> self.created_at + timedelta(minutes=30)

    def cleanup(self):
        if self.is_expired():
            if self.file:
                self.file.delete(save=False)
            self.delete()



class TransferFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='files')
    file = models.FileField('upload_to=file/')
    original_name = models.CharField(max_length=255)
    file_size = models.BigIntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def cleanup(self):
        if self.is_expired():
            if self.file:
                self.file.delete(save=False)
            self.delete()

    def get_file_size_readable(self):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if self.file_size < 1024.0:
                return f"{self.file_size:.1f} {unit}"
            self.file_size /= 1024.0
            return f"{self.file_size:1f} TB"
