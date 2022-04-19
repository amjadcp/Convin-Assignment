from googleapiclient import discovery
from oauth2client import tools
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
import httplib2

i=1
#---------------------------------------------------------------------------
# google_calendar_connection
#---------------------------------------------------------------------------
def google_calendar_connection():
    """
    This method used for connect with google calendar api.
    """
    
    flags = tools.argparser.parse_args([])
    FLOW = OAuth2WebServerFlow(
        client_id='538222486044-uhbs8097ctdopi5uo8ok417emt8ic2ea.apps.googleusercontent.com',
        client_secret='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',
        scope='https://www.googleapis.com/auth/calendar',
        user_agent='test'
        )
    storage = Storage('calendar.dat')
    # credentials = storage.get()
    # if credentials is None or credentials.invalid == True:
    #     credentials = tools.run_flow(FLOW, storage, flags)

    credentials = tools.run_flow(FLOW, storage)
    
    # Create an httplib2.Http object to handle our HTTP requests and authorize it
    # with our good Credentials.
    http = httplib2.Http()
    http = credentials.authorize(http)
    service = discovery.build('calendar', 'v3', http=http)
    return service

service = google_calendar_connection()

# service = build("calendar", "v3", credentials=credentials)
result = service.calendarList().list().execute()
calendar_id = result['items'][0]['id']
result = service.events().list(calendarId=calendar_id, timeZone="Asia/Kolkata").execute()
print(result['items'][0])