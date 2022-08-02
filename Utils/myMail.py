# @Time : 2022/7/19 21:02 
# @Author : cyq
# @File : myMail.py 
# @Software: PyCharm
# @Desc: mail
from typing import Any
from flask_mail import Mail, Message
from App import create_app
from Models import Report


class SendMail:
    app = create_app()
    mail = Mail(app)

    def sendReport(self, report: Report):
        """
        发送报告
        """
        msg = Message(subject=report.title, sender=self.app.config["MAIL_USERNAME"],
                      recipients=[self.app.config['REPORT_MAIL']])
        msg.body = f"""
        hi all \n
        test version {report.version} success \n
        desc {report.desc} \n
        online date {report.online} \n
        demands {report.demands} \n
        bugs {report.bugs}
         """
        self.sender(msg)

    def sender(self, msg: Any):
        with self.app.app_context():
            self.mail.send(msg)
