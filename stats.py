from __future__ import print_function
import os.path
import smtplib
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1btjUrMpjFoN6VNThFfFGVacxf2H5hWXpHnS7emWLv2Y'
SAMPLE_RANGE_NAME = 'Master Sheet Spring 2022!A2:T263'

def send_email(data):
	SUBJECT = "BearDown Stats HTML"
	FROMADDR = "variousemaillists@gmail.com"
	FROMPASSWORD = "***" 
	TOADDR = ['JasonG7234@gmail.com']
	
	MESSAGE = MIMEMultipart('alternative')
	MESSAGE['subject'] = SUBJECT
	MESSAGE['From'] = FROMADDR

	HTML_BODY = MIMEText(data, 'html') #Record MIME type text/html
	MESSAGE.attach(HTML_BODY)
	
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.login(FROMADDR, FROMPASSWORD)
	
	for email in TOADDR:
		MESSAGE['To'] = email
		server.sendmail(FROMADDR, [email], MESSAGE.as_string())
		
	server.quit()

def table_start_html():
    return '''
        <table class="stats" id="infoTable" cellspacing="0" cellpadding="0">
            <tbody>
    '''

def table_end_html():
    return '''
        </tbody>
        </table>
    '''

def main():
    """Shows basic usage of the Sheets API.
    Prints values fcxf2H5hWXpHnS7emWLv2Yrom a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request()).with_traceback(True)
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', 
                SCOPES)
            flow.authorization_url(prompt='consent')
            creds = flow.run_local_server(port=58371)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    
    html = '''
        <div id="wrapper">
    '''
    if not values:
        print('No data found.')
    else:
        for row in values:
            if (len(row) <= 1 and row[0] != "Substitues"):
                html += table_end_html()
                html += "<h2>" + row[0] + "</h2>"
                html += table_start_html()
                print("Current team is: " + row[0])
            else:
                html += "<tr>"
                for item in row:
                    html += "<td>" + item + "</td>"
                html += "</tr>"
    html += table_end_html() 
    html += '''
        </div>
    '''

    send_email(html)

if __name__ == '__main__':
    main()
