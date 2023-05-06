# Importing libraries
import imaplib
import getpass
from datetime import datetime

# Credentials
user = input("Username: ")
password = getpass.getpass("Password: ")
imap_url = 'imap.gmail.com'
 
# this is done to make SSL connection with GMAIL
con = imaplib.IMAP4_SSL(imap_url)
 
# logging the user in
con.login(user, password)
print('Login Successful!')

# calling function to check for email under this label
con.select('"[Gmail]/Sent Mail"')

# #Dates
# date_format = "%d-%b-%Y"
# startingDate = None
# with open('last.txt', 'r') as f:
#   startStr = f.read()
#   startingDate = datetime.strptime(startStr, date_format) if startStr != 'None' else None
# endingDate = datetime.strptime('8-May-2023', date_format)

# # fetching emails from this user
# hours = []
# emailDates = {}
# result, data = con.search(None, f'(SUBJECT "Time Card" TO "{os.environ["to_email"]}"'+(f' SENTSINCE {startingDate.strftime(date_format)}' if startingDate else '') + (f' BEFORE {endingDate.strftime(date_format)}' if endingDate else '') + ')')
# for id in data[0].split():
#   typ, subject = con.fetch(id, '(BODY.PEEK[HEADER])')
#   subject=[i for i in str(subject[0]).split('\\r\\n') if 'Subject' in i][0].replace('Subject: ', '').strip('Re: ')
#   resp, mailData = con.fetch(id, "(UID BODY[TEXT])")
    
#   #get the body of the email
#   body = str(mailData[0][1]).split('--')[1].replace('Content-Type: text/plain;', '').split(':')
#   hoursInWeek = []
#   for t in body:
#     if 'Saptak Das' in t: #Does not double count in replies.
#       break
#     if 'hours' in t:
#       hoursInWeek.append(float(t.split('hours')[0].strip(' ')))
#   if subject not in emailDates:
#     emailDates[subject] = hoursInWeek
#   else:
#     emailDates[subject] += hoursInWeekpass