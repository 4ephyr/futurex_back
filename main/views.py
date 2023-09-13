from django.shortcuts import render
from django.http import JsonResponse
from django_ratelimit.decorators import ratelimit
from .models import Courses, ApplicationDetails, partnerLogos, FrequentlyAskedQuestions
from .forms import ApplicationDetailsForm
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.http import JsonResponse
import os
import smtplib

def indexPage(request):
    partners = partnerLogos.objects.all()
    replicated_partners = list(partners) * 8
    country_codes = [
        ("973", "BH"),
        ("91", "IN"),
        ("1", "US"),
    ]
    form = ApplicationDetailsForm()
    faq = FrequentlyAskedQuestions.objects.all()[:5]

    return render(request, 'main/index.html', {'form': form, 'country_codes': country_codes, 'partners': replicated_partners, 'faqs': faq})

def admissionPage(request):
    course = Courses.objects.all()[:3]
    return render(request, 'main/admissions.html',{
        'courses': course,
    })

def eventsPage(request):
    return render(request, 'main/events.html')

def eventPage(request):
    return render(request, 'main/event.html')

def launchpadPage(request):
    return render(request, 'main/launchpad.html')



def sendStatusMail(receiver_email, name, course, phone, status='Pending'):
    try:
        os.environ['GMAIL_USERNAME'] = 'technicalsahal25@gmail.com'
        os.environ['GMAIL_PASSWORD'] = 'ihyseubzeiaegoxw'
        msg = MIMEMultipart()
        msg['From'] = os.environ.get('GMAIL_USERNAME')
        msg['To'] = receiver_email
        msg['Subject'] = 'Application Confirmation Of Your Selected Course'

        if status in ["Pending", "Selected", "Rejected"]:
            message = ""
            subject = ""

        if status == 'Pending':
            subject = 'Congratulations! You have been shortlisted for the course'
            message = f"""Dear {name},

Congratulations! You have been shortlisted for the {course} course at FutureX. We look forward to having you in our program.
We will contact you through {phone}

Best regards,
4ephyr
Developer
FutureX
"""
        elif status == 'Selected':
            subject = 'Congratulations! You have been selected for the course'
            message = f"""Dear {name},

Congratulations! You have been selected for the {course} course at FutureX. We look forward to having you in our program.
We will contact you through {phone}

Best regards,
4ephyr
Developer
FutureX
"""
        elif status == 'Rejected':
            subject = 'Application Status: Rejected'
            message = f"""Dear {name},

We regret to inform you that your application for the {course} course at FutureX has been rejected.
We will contact you through {phone}

Best regards,
4ephyr
Developer
FutureX
"""

        msg.attach(MIMEText(message, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)

        server.starttls()

        sender_email = os.environ.get('GMAIL_USERNAME')
        sender_password = os.environ.get('GMAIL_PASSWORD')
        server.login(sender_email, sender_password)

        server.sendmail(sender_email, receiver_email, msg.as_string())

        server.quit()

        return JsonResponse({'message': 'mail sent successfully.'}, status=200)
    except Exception:
        return JsonResponse({'message': 'An error occured while sending the mail'}, status=500)

@ratelimit(key='ip', rate='1/m', method='POST', block=True)
def reg_submit(request):
   
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            course = request.POST.get('course')
            country_code = request.POST.get('country_code')
            phone = country_code + " " + request.POST.get('phone')
            
            data = ApplicationDetails(
                name=name,
                email=email,
                course=course,
                country_code=country_code,
                phone=phone
            )
            data.save()

            sendStatusMail(email, name, course, phone)

            return JsonResponse({'message': 'Application received successfully.'}, status=200)
        except Exception as e:
            return JsonResponse({'message': 'An error occurred while processing your application.'}, status=500)

    return JsonResponse({'message': 'Invalid request method.'}, status=405)
