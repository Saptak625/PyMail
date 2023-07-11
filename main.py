# Importing libraries
import imaplib
import getpass
from time import sleep
from plyer import notification
import pystray
from PIL import Image
import sys
 
image = Image.open("logo.png")

tray_exit = False # The preferred way to exit the program is to click the tray icon for PyMail and select "Exit".

def after_click(icon, query):
    if str(query) == "Exit":
        icon.stop()
        global tray_exit
        tray_exit = True
 
 
icon = pystray.Icon("PyMail", image, "PyMail", menu=pystray.Menu(pystray.MenuItem("Exit", after_click)))

# Credentials
print('='*40+'Welcome to PyMail!'+'='*40)
print('The preferred way to exit the program is to click the tray icon for PyMail and select "Exit".')
print('-'*100)
if len(sys.argv) == 3:
    user = sys.argv[1]
    password = sys.argv[2]
    print(f'Using username: {user} and password: '+'*'*len(password))
else:
    print('Enter your credentials:')
    user = input("Username: ")
    password = getpass.getpass("Password: ")

imap_url = 'imap.gmail.com'

delay = 10 # seconds
notification_time = 5 # seconds

# If either of these criteria are met, a push notification will be sent. If both are empty, all emails will be notified.
# Priority 1: Emails from specific senders.
priority_1 = []
            
# Priority 2: Emails with specific keywords.
priority_2 = []
 
# this is done to make SSL connection with GMAIL
with imaplib.IMAP4_SSL(imap_url) as con:
    # logging the user in
    login_failed = False
    try:
        con.login(user, password)
        print('Login Successful!\n')
        icon.run_detached()
    except imaplib.IMAP4.error:
        print('Login Failed!\n')
        login_failed = True

    if not login_failed:
        email_ids = []
        while not tray_exit:
            try:
                # Get all unread emails
                con.select('INBOX')

                # Check for new emails based on delay.
                result, data = con.search(None, 'UNSEEN')
                ids = data[0]
                id_list = ids.split()
                print('='*40+f'Found {len(id_list)} unread emails.'+'='*40)

                for ind, i in enumerate(id_list):
                    if i in email_ids:
                        continue

                    # If id_list has more than 50 emails, read all emails, except last 50.
                    email_limit = False
                    if len(id_list) > 50 and ind+1 < len(id_list)-50:
                        email_limit = True
                        _, _ = con.fetch(i, '(RFC822)')

                    # Peek at the email to get the sender and subject. Do not mark as read.
                    result, data = con.fetch(i, '(BODY.PEEK[HEADER])')
                    email_msg = data[0][1].decode('utf-8')
                    sender = email_msg[email_msg.find('From: ')+6:]
                    sender = sender[:sender.find('\n')]
                    subject = email_msg[email_msg.find('Subject: ')+9:]
                    subject = subject[:subject.find('\n')]
                    print('-'*100)
                    print(f'From: {sender}')
                    print(f'Subject: {subject}')

                    show_email = False
                    if not priority_1 and not priority_2:
                        show_email = True # Show all emails if no criteria are specified.
                    else:
                        # Check if email meets one of the criteria in priority 1 or 2.
                        # Priority 1: Emails from specific senders.
                        sender_email = sender[sender.find('<')+1:sender.find('>')]
                        if priority_1 and sender_email in priority_1:
                            show_email = True
                        # Priority 2: Emails with specific keywords.
                        elif priority_2 and any(keyword in subject for keyword in priority_2):
                            show_email = True

                    # Show push notification if email meets criteria.
                    if show_email and not email_limit:
                        print('Sending notification...')
                        notification.notify(
                            title=subject if len(subject) < 25 else subject[:25]+'...',
                            message=f'From: {sender}\nTo: {user}',
                            timeout=notification_time  # The notification will automatically close after 10 seconds
                        )
                    else:
                        print('Email does not meet criteria. Skipping...')

                    print('-'*100)

                    email_ids.append(i)
            except imaplib.abort as e:
                print('Connection aborted. Reconnecting...')
                con = imaplib.IMAP4_SSL(imap_url)
            # Wait for delay before checking for new emails again.
            sleep(delay)  
        print('Exiting...')
        icon.stop()