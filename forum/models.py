from django.db import models
from datetime import datetime    

class Week(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Thread(models.Model):
    title = models.TextField()
    deadline = models.DateTimeField(default=datetime.now(), blank=True)
    description = models.TextField(blank=True)
    mechanism_expectation = models.TextField(blank=True)
    summary_content = models.TextField(blank=True)
    week = models.ForeignKey(Week, related_name="threads", on_delete=models.CASCADE)

    class InquiryState(models.TextChoices):
        PHASE1 = 1
        PHASE2 = 2
        PHASE3 = 3
        PHASE4 = 4
        PHASE5 = 5

    state = models.CharField(
        max_length=255,
        choices=InquiryState.choices,
        default=InquiryState.PHASE1
    )
    
    def __str__(self):
        return self.title
    
    @property
    def week_name(self):
        return self.week.name

class ReferenceFile(models.Model):
    title = models.TextField()
    url = models.TextField()
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="reference_file")
