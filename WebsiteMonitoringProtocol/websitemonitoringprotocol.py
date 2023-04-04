import requests
import os
import time
from bs4 import BeautifulSoup
from twilio.rest import Client
TWILIO_ACCOUNT_SID = "AC05bfedd2bb9c2d6e1dd5769554342df8" # my Account SID
TWILIO_AUTH_TOKEN = "87b99416ce5a609c4975ad0c34b5549d" # my Auth Token
TWILIO_PHONE_SENDER = "+447700165801" # replace with the phone number you registered in twilio
TWILIO_PHONE_RECIPIENT = "+447513766675" # replace with your phone number


def send_text_alert(alert_str):
    """Sends an SMS text alert."""
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(to=TWILIO_PHONE_RECIPIENT, from_=TWILIO_PHONE_SENDER, body=alert_str)

URL_TO_MONITOR = "https://glastonbury.seetickets.com/content/extras" #change this to the URL you want to monitor


DELAY_TIME = 5 # seconds

def process_html(string):
    soup = BeautifulSoup(string, features="lxml")

    # make the html look good
    soup.prettify()

    # remove script tags
    for s in soup.select('script'):
        s.extract()
    
    for s in soup.select('nonce'):
        s.extract()

    # remove meta tags 
    for s in soup.select('meta'):
        s.extract()
    
    # convert to a string, remove '\r', and return
    return str(soup).replace('\r', '')

def webpage_was_changed(): 
    # Returns true if the webpage was changed, otherwise false
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Pragma': 'no-cache', 'Cache-Control': 'no-cache'}
    response = requests.get(URL_TO_MONITOR, headers=headers)
    print(dir(response))

    # create the previous_content.txt if it doesn't exist
    if not os.path.exists("previous_content.txt"): #does this file exist from a previous loop, if not then create it
        open("previous_content.txt", 'w+').close()

    # open the previous context file and assign it to file handle which is passed to previous_response_html and then closed
    filehandle = open("previous_content.txt", 'r')
    previous_response_html = filehandle.read() 
    filehandle.close()

    # processes the get request into a format which removes meta,script, and nonce tags and outputs filw as variable for comparison with previous response
    processed_response_html = process_html(response.text)

    if previous_response_html == processed_response_html:
        return False   
    else:
        filehandle = open("previous_content.txt", 'w')
        filehandle.write(processed_response_html)
        open("newsite.txt", 'w+').close()
        New_URL = open("newsite.txt",'w')
        New_URL.write(processed_response_html)
        filehandle.close()
        New_URL.close()
        print('Changing everytime')
        return True
    
def main():  
    while True:
        try:
            if webpage_was_changed():
                print('Yay')
            else:
                print('Nothing yet')
        except:
            print('Error')
        
        time.sleep(DELAY_TIME)
if __name__ == "__main__":
    main()