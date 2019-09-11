import yagmail #https://github.com/kootenpv/yagmail
    
def send_email(recipient_email, subject, html_email, text_email=None):
    sender_email = 'wdgrantham@gmail.com'
    try:
        #with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        #    server.login("wdgrantham@gmail.com", password)
        #    server.sendmail(sender_email, receiver_email, message.as_string())
        yag = yagmail.SMTP(sender_email)
        yag.send(to=recipient_email, subject = subject, contents = html_email)
        print(f'Successfully sent email to { recipient_email } with subject: { subject }')
            
    except:
        print(f'Failed to send email to { recipient_email } with subject: { subject }')
        
#send_email('wdgrantham@yahoo.com', 'Test from python script', '<p>Here is some sample html for the html version.</p><img src="https://via.placeholder.com/100x100.png">', 'Here is some sample text for the text email version')