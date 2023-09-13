from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class partnerLogos(models.Model):
    partner1 = models.ImageField(upload_to='partners',null=True,blank=True)
    partner2 = models.ImageField(upload_to='partners',null=True,blank=True)
    partner3 = models.ImageField(upload_to='partners',null=True,blank=True)

    class Meta:
        verbose_name = verbose_name_plural = "Partner Logos"
    
    def __str__(self):
        return 'Partner'

class OurCommunityEvents(models.Model):

    field1 = models.ImageField(upload_to='events',null=True,blank=True)
    field2 = models.ImageField(upload_to='events',null=True,blank=True)
    field3 = models.ImageField(upload_to='events',null=True,blank=True)
    field4 = models.ImageField(upload_to='events',null=True,blank=True)
    field5 = models.ImageField(upload_to='events',null=True,blank=True)

    class Meta:
        verbose_name = verbose_name_plural = "Event Images"

    def __str__(self):
        return 'Images'

class Courses(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=1)
    features = models.JSONField(blank=True,null=True)
    position = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self):
        return self.name
    

class ApplicationDetails(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Selected', 'Selected'),
        ('Rejected', 'Rejected'),
    )
    name = models.CharField(max_length=255)
    email = models.EmailField()
    country_code = models.CharField(max_length=5, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True)
    course = models.CharField(max_length=50)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        verbose_name = verbose_name_plural = "Application Details"

    def save(self, *args, **kwargs):
        name = self.name
        email = self.email
        course = self.course
        phone = self.country_code + " " + self.phone
        status = self.status

        self.statusChange(name, email, course, phone, status)

        super().save(*args, **kwargs)

    def statusChange(self, name, email, course, phone, status):
        from .views import sendStatusMail

        sendStatusMail(email, name, course, phone, status)

    def __str__(self):
        return self.name

class UpcomingEvent(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()

    class Meta:
        verbose_name = verbose_name_plural = "Upcoming Event"

    def __str__(self):
        return self.name

class News(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    content = models.TextField()
    date = models.DateTimeField()

    class Meta:
        verbose_name = verbose_name_plural = "News"

    def __str__(self):
        return self.title
    
class RecentEvents(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()

    class Meta:
        verbose_name = verbose_name_plural = "Recent Events"

    def __str__(self):
        return self.name
    
@receiver(post_save, sender=UpcomingEvent)
def add_to_recent_events_and_delete_previous(sender, instance, **kwargs):
    most_recent_upcoming_event = UpcomingEvent.objects.exclude(pk=instance.pk).order_by('-date').first()

    if most_recent_upcoming_event:
        RecentEvents.objects.create(
            name=most_recent_upcoming_event.name,
            description=most_recent_upcoming_event.description,
            date=most_recent_upcoming_event.date
        )

    if most_recent_upcoming_event:
        most_recent_upcoming_event.delete()

class FrequentlyAskedQuestions(models.Model):
    question = models.TextField()
    answer = models.TextField()

    class Meta:
        verbose_name = verbose_name_plural = "FAQs"

    def __str__(self):
        id = str(self.id)
        return "Faq" + " " + id
