import smtplib
import email
# 负责构造文本
from email.mime.text import MIMEText
# 负责构造图片
from email.mime.image import MIMEImage
# 负责将多个对象集合起来
from email.mime.multipart import MIMEMultipart
from email.header import Header

# SMTP服务器的设置
smtp_server = "smtp.qq.com"
# 发件人邮箱
mail_sender = "xxx@qq.com"
# 邮箱授权码
mail_license = "sfvlbzdgtdghfbeegs"
# 邮箱收件人
mail_receivers = "xxxx@qq.com"

# 构造MIMEMultipart对象
mail_content = MIMEMultipart('related')
# 邮件主题
subject_content = """Python Test Mail"""
# 设置发送者
mail_content["From"] = "sender_name<xxx@qq.com>"
# 设置接收者
mail_content["To"] = "receiver_name<xxx@qq.com>"
# 设置邮件主题
mail_content["Subject"] = Header(subject_content,'utf-8')

# 构造正文内容
body_content = "This is a Test Mail"
# 构造文本
message_text = MIMEText(body_content,"plain","utf-8")
# 向MIMEMultipart对象增加文本对象
mail_content.attach(message_text)

# 构造图片内容
image_data = open('a.jpg','rb')
# 设置获取的二进制数据
message_image = MIMEImage(image_data.read())
# 关闭打开的文件
image_data.close()
#message_image.add_header('Content-ID','')
message_image["Content-Disposition"] = 'attachment; filename="a.jpg"'
# 向MIMEMultipart对象增加图片对象
mail_content.attach(message_image)

# 添加附件
atta = MIMEText(open('aaa.docx','rb').read(),'base64','utf-8')
# 设置附件的信息
atta["Content-Disposition"] = 'attachment; filename="aaa.docx"'
# 向MIMEMultipart对象增加附件对象
mail_content.attach(atta)

# 发送邮件
smtp_sender = smtplib.SMTP()
#设置发件人的信息
smtp_sender.connect(smtp_server,25)
# 打印与SMTP交互的信息
smtp_sender.set_debuglevel(1)
# 登陆邮箱
smtp_sender.login(mail_sender,mail_license)
# 发送邮件
smtp_sender.sendmail(mail_sender,mail_receivers,mail_content.as_string())
print("邮件发送成")
smtp_sender.quit()