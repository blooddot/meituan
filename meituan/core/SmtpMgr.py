from email.header import Header
from email.mime.text import MIMEText
from enum import Enum
from smtplib import SMTP

PRESET_ADDRESS_LIST = ['blooddot@hotmail.com']


class ESmtpType(Enum):
    """邮件格式"""

    plain = "plain"  # 文本
    html = "html"  # html 格式


class __SmtpMgr:
    """邮件管理器"""
    _address: str = 'bextalyst@hotmail.com'
    _user: str = 'bextalyst@hotmail.com'
    _password: str = 'Bextanalyst666'
    _host: str = 'smtp.office365.com'
    _port: int = 587

    def sendMail(self, subject: str, content: str, to_addrs: list[str] = PRESET_ADDRESS_LIST, subtype: ESmtpType = ESmtpType.plain):
        smtp = SMTP(self._host, self._port)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(user=self._user, password=self._password)

        # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
        msg = MIMEText(content, subtype.value, 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')   # 标题

        smtp.sendmail(self._address, to_addrs, msg.as_string())


SmtpMgr = __SmtpMgr()
