from django.db import models

# Create your models here.
from editions.models import Edition, Session
from tickets.models import Attendant

class Streaming(models.Model):
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    url = models.URLField()


'''
For each session, 3 qrs will be created. This QR must be read by the students
if the want to demostrate that they attended the session. Mininum of QRs: 2
'''
  

class AttendanceSlot(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)


class Attendance(models.Model):
    attendant = models.ForeignKey(Attendant, on_delete=models.CASCADE, blank=True)
    slot = models.ForeignKey(AttendanceSlot, on_delete=models.CASCADE, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["attendant", "slot"]