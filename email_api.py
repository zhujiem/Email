# coding: utf-8

'''
   @Author: Yong Gao,
            Jamie Zhu
   @Date: 2018-11-17
'''


import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.header import Header
from email.utils import formataddr

class EmailAPI():
    # 目前仅实现了 163 和 qq 邮箱两种; 其他邮箱服务器需另行查找设置；
    # QQ邮箱需要设置授权码, 参考https://service.mail.qq.com/cgi-bin/help?subtype=1&id=28&no=1001256
    def __init__(self, username, password):
        self.mail_user = username
        self.mail_pass = password
        email_type_dict = {
            '163.com': 'no_ssl',
            'qq.com':  'no_ssl',
            'logpai.com': 'no_ssl'
        }
        mail_host_dict = {
            'qq.com': "smtp.qq.com",
            '163.com': "smtp.163.com",
            'logpai.com': "smtp.qiye.aliyun.com"
        }
        email_type = username.split('@')[1]
        self.mail_host = mail_host_dict[ email_type ]
        if email_type in email_type_dict:
            self.mail_type = email_type_dict[ email_type ]
        else:
            print( '暂时不支持的邮箱类型' )
            self.mail_type = 'ssl'
        self.login()

    def set_reciv_list(self, receivers_list):
        # 发件人收件人信息格式化 ，可防空
        # 固定用法不必纠结，我使用lambda表达式进行简单封装方便调用
        lam_format_addr = lambda name, addr: formataddr((Header(name, 'utf-8').encode(), addr))

        self.msg = MIMEMultipart()
        self.msg['From'] = lam_format_addr("LogPAI Team", self.mail_user) # 腾讯邮箱可略 
        self.msg['To'] = ";".join(receivers_list) #lam_format_addr('',  receivers_list[0]) # 腾讯邮箱可略

    def set_email_msg(self, to_list, msg_title, msg_content, content_type='str' ):
        '''
        content_type = str/html/html_file
        '''
        self.to_list = to_list
        self.set_reciv_list(to_list)
        self.msg['Subject'] = Header( msg_title, 'utf-8').encode() # 腾讯邮箱略过会导致邮件被屏蔽 
        if content_type == 'str':
            content_main = MIMEText(msg_content, 'plain', 'utf-8')
        elif content_type == 'html':
            content_main = MIMEText(msg_content, 'html', 'utf-8')
        elif content_type == 'html_file':
            with open(msg_content,'r') as f:
                content = f.read()
            #设置html格式参数
            content_main = MIMEText(content, 'html', 'utf-8')
        self.msg.attach(content_main)

    def add_attach_pic(self, pic_path_name):
        file_path, file_name = os.path.split(pic_path_name)
        #添加照片附件
        with open(pic_path_name, 'rb')as fp:
            picture = MIMEImage(fp.read())
            #与txt文件设置相似
            picture['Content-Type'] = 'application/octet-stream'
            picture['Content-Disposition'] = 'attachment;filename="{}"'.format(file_name)
        #将内容附加到邮件主体中
        self.msg.attach(picture)

    def add_attach_file(self, file_path_name):
        file_path, file_name = os.path.split(file_path_name)
        #添加一个txt文本附件
        with open(file_path_name,'r')as h:
            attach_file = h.read()
        #设置txt参数
        attach_file = MIMEText(attach_file, 'plain', 'utf-8')
        #附件设置内容类型，方便起见，设置为二进制流
        attach_file['Content-Type'] = 'application/octet-stream'
        #设置附件头，添加文件名
        attach_file['Content-Disposition'] = 'attachment;filename="{}"'.format(file_name)
        self.msg.attach(attach_file)

    def send_email(self):
        #登录并发送

        try:
            self.smtpObj.sendmail( self.mail_user, self.to_list, self.msg.as_string() )
            print('Send success: ' + str(self.to_list))
        except Exception as e:
            print('Error: ', e)


    def login(self):
        smtpObj = None
        try:
            if self.mail_type =='no_ssl':
                smtpObj = smtplib.SMTP()
                smtpObj.connect(self.mail_host, 25)
            elif self.mail_type == 'ssl':
                smtpObj = smtplib.SMTP_SSL(self.mail_host, 465)

            smtpObj.login(self.mail_user, self.mail_pass)
            self.smtpObj = smtpObj
            print('Login success.')
        except:
            print('Login failed.')
            raise
    
    def close(self):
        self.smtpObj.quit()


if __name__=='__main__':
    # Example
    email = EmailAPI(username='info@logpai.com', password='*****')
    to_list = [ 'xxx@logpai.com' ] # Set mailto list
    msg_subject = "Notice: This is a test." # Set email subject
    msg_content = "This is a test.\n\nLogPAI Team" # Set email content
    email.set_email_msg(to_list, msg_subject, msg_content)
    email.send_email()    
    email.close()


    
