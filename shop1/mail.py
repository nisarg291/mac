import smtplib


def send_mail_student(sender,reciever,mail_body,mail_subject):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo() #The client sends this command to the SMTP server to identify itself and initiate the SMTP conversation.
    server.starttls() #encrypts are connection
    server.ehlo()

    server.login('nisargadalja24680@gmail.com','NisargHitesh@2620029164#')

    subject = mail_subject
    body = mail_body

    msg = f"Subject: {subject}\n\n{body}" #new f-string way to format in python like we use ``  and ${} in js
    
    server.sendmail(
        sender, #from
        reciever, #to
        msg
    )
    print('mail sent!')
    server.quit()

def send_mail(line):
    print(line)
    sender = line[2]
    reciever = line[3]
    mail_body = line[1]
    mail_subject = line[0]
    send_mail_student(sender,reciever,mail_body,mail_subject)