import json
from bs4 import BeautifulSoup
import datetime

from ustc_passport_login import USTCPassportLogin


class USTCAutoHealthReport(object):
    def __init__(self):
        # 用于登录
        self.login_bot = USTCPassportLogin()
        self.sess = self.login_bot.sess
        # CAS身份认证url
        self.cas_url = 'https://passport.ustc.edu.cn/login?service=https%3A%2F%2Fweixine.ustc.edu.cn%2F2020%2Fcaslogin'
        # 打卡url
        self.clock_in_url = 'https://weixine.ustc.edu.cn/2020/daliy_report'
        # 每周报备url
        self.report_url = 'https://weixine.ustc.edu.cn/2020/apply/daliy/ipost'
        # 身份认证token
        self.token = ''

    def _get_token(self):
        """
        获取打卡时需要提供的验证字段
        """
        response = self.sess.get(self.cas_url)
        s = BeautifulSoup(response.text, 'html.parser')
        token = s.find(attrs={'name': '_token'}).get('value')
        return token

    def _check_success(self, response):
        """
        简单check一下有没有成功打卡、报备
        """
        s = BeautifulSoup(response.text, 'html.parser')
        msg = s.select('.alert')[0].text
        return '成功' in msg

    def login(self, username, password):
        """
        登录,需要提供用户名、密码
        """
        self.token = ''
        is_success = self.login_bot.login(username, password)
        if is_success:
            self.token = self._get_token()
        return is_success

    def daily_clock_in(self, post_data_file):
        """
        打卡函数，需要提供包含表单内容的json文件（示例见post.json）
        打卡成功返回True，打卡失败返回False
        """
        try:
            with open(post_data_file, 'r') as f:
                post_data = json.loads(f.read())
            post_data['_token'] = self.token
            response = self.sess.post(self.clock_in_url, data=post_data)
            return self._check_success(response)
        except Exception as e:
            print(e)
            return False

    def report(self, data_file):
        """
        出入校报备，需要提供包含表单内容的json文件（示例见report.json）
        申请成功返回True,申请失败返回False
        :param data_file表单数据文件
        """
        try:
            with open(data_file, 'r') as f:
                post_data = json.loads(f.read())
            now = datetime.datetime.now()
            post_data['_token'] = self.token
            post_data['start_date'] = now.strftime("%Y-%m-%d %H:%M:%S")
            post_data['end_date'] = now.strftime("%Y-%m-%d 23:59:59")
            response = self.sess.post(self.report_url, data=post_data)
            return self._check_success(response)
        except Exception as e:
            print(e)
            return False
