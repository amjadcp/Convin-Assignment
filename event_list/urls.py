from django.urls import path
from event_list.views import GoogleCalendarInitView, GoogleCalendarRedirectView

app_name = 'event_list'

urlpatterns = [
    path('init/', GoogleCalendarInitView, name='init'),
    path('redirect/', GoogleCalendarRedirectView, name='redirect'),
]