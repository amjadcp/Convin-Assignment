from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.shortcuts import redirect
import os.path
# import google_auth_oauthlib.flow
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# save client_secret.json in secret_folder
CLIENT_SECRETS_FILE = os.path.join(os.path.dirname(__file__), '../secret_folder/client_secret.json')
SCOPES = ['https://www.googleapis.com/auth/calendar']
ROOTURL = 'http://localhost:8000/'

@api_view(['GET'])
def GoogleCalendarInitView(request):
    # creating the flow
    flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)
    # redirecting url after the user completes authorization
    flow.redirect_uri = f'{ROOTURL}rest/v1/calendar/redirect/'

    #  Generate URL for request to Google's OAuth 2.0 server.
    authorization_url, state = flow.authorization_url(
    access_type='offline',
    include_granted_scopes='true')

    # creating session for state
    request.session['state'] = state

    return redirect(authorization_url)

@api_view(['GET'])
def GoogleCalendarRedirectView(request):

    # access state from session
    state = request.session['state']
    
    # creating the flow
    flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)

    # redirecting url after the user completes authorization
    flow.redirect_uri = f'{ROOTURL}rest/v1/calendar/redirect/'

    # access the authorization response
    authorization_response = request.get_full_path()

    # fetch the token
    flow.fetch_token(authorization_response=authorization_response)

    # access credentials
    credentials = flow.credentials

    try:
        # access the calender
        service = build('calendar', 'v3', credentials=credentials)

        # get the calender list
        calendarlist = service.calendarList().list().execute()

        # get the calender id
        calendar_id = calendarlist['items'][0]['id']

        # get the list of whole event in calender
        events = service.events().list(calendarId=calendar_id).execute().get('items', [])


        if not events:
            return JsonResponse({'message': 'events not found'})
        else:
            return JsonResponse({ "events_list" : events })

    # except block, works if any error occurs
    except HttpError as error:
        return JsonResponse({'Message': f'An error occurred: {error}'})