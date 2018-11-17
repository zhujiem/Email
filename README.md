# Email
An API to send emails programmatically:

``` python
email = EmailAPI(username='info@logpai.com', password='*****')
to_list = [ 'xxx@logpai.com' ] # Set mailto list
msg_subject = "Notice: This is a test." # Set email subject
msg_content = "This is a test.\n\nLogPAI Team" # Set email content
email.set_email_msg(to_list, msg_subject, msg_content)
email.send_email()    
email.close()
```
