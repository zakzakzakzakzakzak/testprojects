import requests
import os
import time
from bs4 import BeautifulSoup
from email.message import EmailMessage
import ssl
import smtplib
import time

URL_TO_MONITOR = "https://glastonbury.seetickets.com/content/extras" #change this to the URL you want to monitor

# write me a function to send emails through python



DELAY_TIME = 1 # seconds

# the following is a processing function to alter the format of the GET request into something more readable for humans and to remove annoying tags which change with every page query

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

# set up of email details and email content




 # instantiating email objects for each recipient using the imported email module and then tagging the relevant attributes. The SSL class adds extra ecurity onto the email contents

email_sender = 'zakreynolds96@gmail.com'
email_password = 'fakepassword' # fake password inputted here for sharing with world on GitHub
email_receiver1 = 'zak@cellcraft.com'
email_receiver2 = 'ariannasmithbdc@gmail.com'
email_receiver3 = 'kane_reynolds@hotmail.com'
email_receiver4 = 'kairobinson00@icloud.com'

subject = 'Website has changed!'
body = """Get your ass over to the glasto site right now https://glastonbury.seetickets.com/content/extras
Arianwen Smith 1123314535 EN49FE
Zak Reynolds 3288228557 EN76RS
Kane Reynolds 1711364100 EN76RS
Kai Robinson 1469727581 EN106FE"""

 # instantiating email object using the imported email module and then tagging the relevant attributes. The SSL class adds extra ecurity onto the email contents
em1 = EmailMessage()
em1['From'] = email_sender
em1['To'] = email_receiver1
em1['Subject'] = subject
em1.set_content(body)
context = ssl.create_default_context()

em2 = EmailMessage()
em2['From'] = email_sender
em2['To'] = email_receiver2
em2['Subject'] = subject
em2.set_content(body)
context = ssl.create_default_context()

em3 = EmailMessage()
em3['From'] = email_sender
em3['To'] = email_receiver3
em3['Subject'] = subject
em3.set_content(body)
context = ssl.create_default_context()

em4 = EmailMessage()
em4['From'] = email_sender
em4['To'] = email_receiver4
em4['Subject'] = subject
em4.set_content(body)
context = ssl.create_default_context()

def webpage_was_changed(): 
    # Returns true if the webpage was changed, otherwise false
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Pragma': 'no-cache', 'Cache-Control': 'no-cache'}
    response = requests.get(URL_TO_MONITOR, headers=headers)


    # create the previous_content.txt if it doesn't exist
    if not os.path.exists("previous_content.txt"): #does this file exist from a previous loop, if not then create it
        open("previous_content.txt", 'w+').close()
        

    # open the previous context file and assign it to file handle which is passed to previous_response_html and then closed
    filehandle = open("previous_content.txt", 'r')
    previous_response_html = filehandle.read() 
    filehandle.close()

    # processes the get request into a format which removes meta,script, and nonce tags and outputs filw as variable for comparison with previous response
    processed_response_html = process_html(response.text)

 
    # check if new iteration is same as previous iterarion, if True then website hasn't changed, if False then website has changed and function should return True to the While loop
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
    # while loop to run continuously with a delay sleep time of 5 seconds per cycle. __name__ == "__main__" means the main function will only be called when the script is the main script running and not just a module imported into another script
def main():  
    while True:
            try:
        
                if webpage_was_changed():
                    print('Yay')
                    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
                        smtp.login(email_sender,email_password)
                        smtp.sendmail(email_sender,email_receiver1,em1.as_string())
                        smtp.sendmail(email_sender,email_receiver2,em2.as_string())
                        smtp.sendmail(email_sender,email_receiver3,em3.as_string())
                        smtp.sendmail(email_sender,email_receiver4,em4.as_string())
                      
                   
                            
                    print("Successfully sent email")           
                else:
                    print('Nothing yet')
            except:
                print('Error in sending email')
        
            time.sleep(DELAY_TIME)
if __name__ == "__main__":
    main()