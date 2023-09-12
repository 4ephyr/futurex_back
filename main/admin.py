from django.contrib import admin
from .models import OurCommunityEvents, Courses, ApplicationDetails, partnerLogos, UpcomingEvent, RecentEvents, News


admin.site.register(OurCommunityEvents)
admin.site.register(Courses)
admin.site.register(ApplicationDetails)
admin.site.register(partnerLogos)
admin.site.register(UpcomingEvent)
admin.site.register(RecentEvents)
admin.site.register(News)