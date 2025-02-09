#Description: Retrieves customer and appointment information from the Setmore API, inserts it into an email 
#template and sends it using the Google Gmail API.
#Author: souXess (clcrx7@hotmail.com)
#Created: 09Feb2025
#Last Modified: 09Feb2025

'''
Notes:

>Google API:
-Must create a Google Cloud project first and then create new OAuth client credentials (Google Cloud Console > 
APIs & Services > Credentials > + CREATE CREDENTIALS).
https://developers.google.com/workspace/guides/configure-oauth-consent
-Sending emails with Google Gmail API: https://developers.google.com/gmail/api/guides/sending
-Make sure the email of the user consenting is also listed as a test user (Google Cloud Dashboard > 
APIs & Services > OAuth consent screen > Test users).

>Setmore API:
-Setmore API documentation: https://setmore.docs.apiary.io
-Additional fields can be added from your Setmore calendar (Settings > Booking Page > Contact fields). The fields
should be set to 'Required.' 'Women', 'Men', 'Girls (under 12)' and 'Boys (under 12)' were the addtional fields added
for this project.
-The default value 'No label' of the label field is updated to 'Confirmation email sent' once the confirmation
email has been sent.
-Be sure to turn off Setmore's built-in confirmation email function (Settings > Notifications > Customer Notifications >
Confirmations).
'''

import requests, json, datetime as dt, time, os, logging, traceback, base64
from email.message import EmailMessage

#These packages need to be installed
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

#Supporting files
#The setmore_credentials.py file needs to contain the variable names SETMORE_REFRESH_TOKEN, BUSINESS_EMAIL and
#ADMINISTRATOR_EMAIL and their values
import setmore_credentials as sc

GMAIL_API_SCOPE = ['https://www.googleapis.com/auth/gmail.send']
google_credentials = None

SETMORE_API_ENDPOINT = 'https://developer.setmore.com/api/v1'
setmore_request_headers = None

def check_setmore_access_token():
    global setmore_request_headers
    
    def request_access_token():
        access_token_request = requests.get(SETMORE_API_ENDPOINT + '/o/oauth2/token?refreshToken=' 
                                            + sc.SETMORE_REFRESH_TOKEN)
        response = json.loads(access_token_request.text)
        #Calculate and add the actual expiration date to the response
        response['token_expires'] = str(dt.datetime.now() + dt.timedelta(seconds = response['data']['token']['expires_in']))
        with open('setmore_access_token.json', 'w') as file:
            json.dump(response, file)
            file.close()

        setmore_request_headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' 
                                   + response['data']['token']['access_token']}

    if os.path.exists('setmore_access_token.json'):
        with open('setmore_access_token.json') as file:
            dictionary = json.load(file)
            file.close()
            #If the access token expires in less than 10 minutes
            if (dt.datetime.strptime(dictionary['token_expires'], '%Y-%m-%d %H:%M:%S.%f') 
                   - dt.datetime.now()).total_seconds() < 600:
                request_access_token()
            #At least 10 mins of access token validity left
            else:
                setmore_request_headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' 
                                   + dictionary['data']['token']['access_token']}
    else:
         request_access_token()
            
def check_google_access_token():
    global google_credentials
    #The file google_access_token.json stores the access and refresh tokens, and is created automatically 
    #when the authorization flow completes for the first time.
    if os.path.exists('google_access_token.json'):
        google_credentials = Credentials.from_authorized_user_file('google_access_token.json', GMAIL_API_SCOPE)
    #If there are no (valid) credentials available, log in.
    if not google_credentials or not google_credentials.valid:
        if google_credentials and google_credentials.expired and google_credentials.refresh_token:
            google_credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('oauth_client_credentials.json', GMAIL_API_SCOPE)
            google_credentials = flow.run_local_server(port = 0)
    #Save the credentials for the next run
    with open('google_access_token.json', 'w') as file:
        file.write(google_credentials.to_json())
        file.close()

def create_email(appointment_datetime, email, customer_name, total_women, total_girls, total_men,
              total_boys, company_key, booking_id, mystery_key, comment):
    
    '''
    write_a_review_url = f'https://reviews.setmore.com/v1/accounts/{company_key}/reviews/write-review'
    
    reschedule_url = f'https://booking.setmore.com/scheduleappointment/{company_key}/manage/{mystery_key}\
    ?utm_source=email&utm_medium=bookingpagerescheduleappointment'
    
    cancel_appointment_url = f'https://booking.setmore.com/scheduleappointment/{company_key}/manage/{mystery_key}\
    ?utm_source=email&utm_medium=bookingpagecancelappointment'
    '''
    #provider constant for this project; Get 'staff_key' from appointments and match with 'key' from '/bookingapi/staffs'
    provider = '<insert provider>'  
    #service constant for this project; Get 'service_key' from appointments and match with 'key' from '/bookingapi/services'
    service = '<insert service>'
    
    #Convert appointment_datetime string to datetime object
    to_datetime_object = dt.datetime.strptime(appointment_datetime[0:10] + ' ' + appointment_datetime[11:16], '%Y-%m-%d %H:%M')
    #Format the datetime object
    formatted_appointment_datetime = dt.datetime.strftime(to_datetime_object, '%a %d %b, %Y %H:%M')
    
    ln1 = f'Hi {customer_name},\n\n'
    ln2 = f'Thank you for booking an appointment with {provider}.\n\n'
    ln3 = f'When: {formatted_appointment_datetime} (JST)\n'
    ln4 = f'Service: {service}\n'
    ln5 = f'Provider: {provider}\n'
    ln6 = 'Participants:\n'
    ln7 = f'   Total Women: {total_women}\n'
    ln8 = f'   Total Girls: {total_girls}\n'
    ln9 = f'   Total Men: {total_men}\n'
    ln10 = f'   Total Boys: {total_boys}\n'
    ln11 = f'Appointment Notes: {comment}\n\n'
    ln12 = ('Special Instructions: You can add any special instructions you want here.\n\n' +
            'Please reply to this email if you have any questions or need to cancel/reschedule your appointment.\n\n' +
            'Thanks,\nCool Dude')
    
    email_subject = f'Appointment scheduled for {formatted_appointment_datetime} (JST) with {provider}'
    email_body = f'{ln1}{ln2}{ln3}{ln4}{ln5}{ln6}{ln7}{ln8}{ln9}{ln10}{ln11}{ln12}'
    
    send_email(email_subject, email_body, email)

def send_email(email_subject, email_body, email_address):
    #Create the gmail api client
    #Set cache_discovery to false to stop the 'file_cache is only supported with oauth2client<4.0.0' warning
    service = build('gmail', 'v1', credentials = google_credentials, cache_discovery = False)

    message = EmailMessage()
    message.set_content(email_body)
    message['To'] = sc.ADMINISTRATOR_EMAIL if email_address == sc.ADMINISTRATOR_EMAIL else email_address
    message['From'] = sc.ADMINISTRATOR_EMAIL if email_address == sc.ADMINISTRATOR_EMAIL else sc.BUSINESS_EMAIL
    message['Subject'] = email_subject

    #Encoded message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {'raw': encoded_message}

    send_message = (service.users()
                    .messages()
                    .send(userId = 'me', body = create_message)
                    .execute())   

def update_appointment_labels(appointment_key_list):
    for appointment_key in appointment_key_list:
        appointment_label_update_url = f'/bookingapi/appointments/{appointment_key}/label?label=Confirmation%20email%20sent'
        update_appointment_label = requests.put(SETMORE_API_ENDPOINT + appointment_label_update_url, 
                                                headers = setmore_request_headers)
    
    logging.info(f'Confirmation emails sent: {str(appointment_key_list)}')

def get_appointment_details():
    start_date = dt.datetime.now().strftime('%d-%m-%Y')
    end_date = (dt.datetime.now() + dt.timedelta(days = 90)).strftime('%d-%m-%Y')
    appointment_details_url = f'/bookingapi/appointments?startDate={start_date}&endDate={end_date}&customerDetails=true'
    appointment_details_request = requests.get(SETMORE_API_ENDPOINT + appointment_details_url, 
                                               headers = setmore_request_headers)
    appointment_details = json.loads(appointment_details_request.text)['data']['appointments']

    if len(appointment_details) == 0:
        logging.info('No new reservations')
    else:
        x = 0
        appointment_key_list = []        

        while x < len(appointment_details):        
            if appointment_details[x]['label'] == 'No label':
                appointment_datetime = appointment_details[x]['start_time']
                email = appointment_details[x]['customer']['email_id']
                customer_name = appointment_details[x]['customer']['first_name']
                total_women = appointment_details[x]['customer']['additional_fields']['Women']
                total_girls = appointment_details[x]['customer']['additional_fields']['Girls (under 12)']
                total_men = appointment_details[x]['customer']['additional_fields']['Men']
                total_boys = appointment_details[x]['customer']['additional_fields']['Boys (under 12)']
                appointment_key = appointment_details[x]['key']
                company_key = appointment_details[x]['customer']['company_key']
                #Waiting on response from Setmore regarding booking ID accessibilty in the API
                booking_id = None
                #Waiting on response from Setmore regarding 2nd key used in reschedule and cancel appointment links
                mystery_key = None
                #Comment field is not required; Set a default value if customer doesn't enter comments to avoid a key error
                comment = appointment_details[x].setdefault('comment', 'none')

                create_email(appointment_datetime, email, customer_name, total_women, total_girls, total_men,
                          total_boys, company_key, booking_id, mystery_key, comment)
                
                appointment_key_list.append(appointment_key)
           
            x += 1
        
        if len(appointment_key_list) == 0:
            logging.info('No new reservations')
        else:
            update_appointment_labels(appointment_key_list)
            
if __name__ == '__main__':
    if os.path.exists('setmore_script.log'):
        file_created = time.ctime(os.path.getctime('setmore_script.log'))
        #Delete the setmore_script.log file if it's over a week old 
        if (dt.datetime.now() - dt.datetime.strptime(file_created, '%a %b %d %H:%M:%S %Y')).total_seconds() > 604800:
            os.remove('setmore_script.log')
                
    #Configure logging
    logging.basicConfig(filename = 'setmore_script.log',
                        encoding = 'utf-8',
                        filemode = 'a',
                        format = '{asctime} - {levelname} - {name} - {message}', 
                        style = '{', 
                        datefmt = '%Y-%m-%d %H:%M:%S',
                        level = 'INFO')
    
    try:
        check_setmore_access_token()
        check_google_access_token()
        get_appointment_details()     
    except:
        logging.exception('')
        
        try:
            check_google_access_token()
            send_email('Setmore Script has Encountered an Error', traceback.format_exc(), sc.ADMINISTRATOR_EMAIL)
        except:
            logging.exception('Email could not be sent to administrator')
