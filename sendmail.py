# -*- coding: utf-8 -*-
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr
import smtplib
import os
#用来格式化邮件地址
def _format_addr(s):
    name, addr = parseaddr(s)#这个函数会解析出姓名和邮箱地址
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, bytes) else addr))

def send_mail(mail_text,
              from_addr = '17610469836@163.com',
              password = 'yingu123',
              to_addr = '2312256442@qq.com',
              smtp_server='smtp.163.com'):

    # 输入Email地址和口令:
    from_addr = from_addr
    # 这里的密码一定是授权码，163邮箱原始密码不行。
    password = password
    # 输入SMTP服务器地址:这里我们用smtp.163.com
    smtp_server = smtp_server
    # 输入收件人地址:
    to_addr = to_addr


    #print(mail_text)
    msg = MIMEText(mail_text, 'plain', 'utf-8')
    # 设置发件人，收件人姓名和邮件主题
    msg['From'] = _format_addr(u'服务器<%s>' % from_addr)
    msg['To'] = _format_addr(u'负责人 <%s>' % to_addr)
    msg['Subject'] = Header(u'服务器程序告警邮件', 'utf-8').encode()

    server = smtplib.SMTP(smtp_server, 25)  # SMTP协议默认端口是25
    server.set_debuglevel(1)  # 打印出和SMTP服务器交互的所有信息
    server.login(from_addr, password)  # 登录服务器
    # 发送邮件，这里第二个参数是个列表，可以有多个收件人
    # 邮件正文是一个str，as_string()把MIMEText对象变成str
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()
if __name__ == '__main__':
    send_mail('Error! please have a look!')
    #print(type(sys.argv[0]))