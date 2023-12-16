import argparse, requests, smtplib

# Arguments
argParser =  argparse.ArgumentParser()
argParser.add_argument("-u", "--urls", help="URLs to test, comma-separated values")
argParser.add_argument("-s", "--sender", help="error email sender")
argParser.add_argument("-r", "--receivers", help="error email receivers, comma-separated values")
argParser.add_argument("-H", "--host", help="SMTP host")
args = argParser.parse_args()

urls = args.urls.split(',')
urlsNotResponding = []

# Concat each URL not responding 200 code to the array urlsNotResponding
for url in urls:
    response = requests.get(url)
    if response.status_code != 200:
        urlsNotResponding.append(url)

# We send an email if one or more URLs are not responding
if len(urlsNotResponding) > 0:
    message = 'URLs not responding: ' + ', '.join(urlsNotResponding)

    smtpObj = smtplib.SMTP(args.host)
    smtpObj.sendmail(args.sender, args.receivers.split(','), message)
