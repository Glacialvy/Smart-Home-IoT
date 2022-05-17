import smtplib
import time
from thingspeak import getData

running = True

def sendEmail():
    while running:
        #time.sleep(10)
        time.sleep(86400)

        field1 = 0
        field2 = 0
        field3 = 0
        field4 = 0

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        thingspeakData = getData();
        feedNum = len(thingspeakData)

        for data in thingspeakData:
            field1 += float(data['field1']);
            field2 += float(data['field2']);
            field3 += int(data['field3']);
            field4 += int(data['field4']);

        field1Avg = field1 / feedNum
        field2Avg = field2 / feedNum

        EMAIL_ADDRESS = "s4yur1.chan.006@gmail.com"
        PASSWORD = "root_pass_006"
        #EMAIL_ADDRESS = ""
        #PASSWORD = ""

        resCode = server.login(EMAIL_ADDRESS, PASSWORD)

        subject = "Daily Report.."
        body = "Body content..\n \n Temperature: {} \n Brightness: {} \n Doors opened: {} \n Relay opened: {}".format(field1Avg, field2Avg, field3, field4)
        fullEmail = "Subject: {}\n\n{}".format(subject, body)

        resCode = server.sendmail(from_addr=EMAIL_ADDRESS, to_addrs="s4yur1.chan.006@gmail.com", msg=fullEmail)

        server.quit()