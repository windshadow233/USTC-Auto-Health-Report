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
        self.report_url = 'https://weixine.ustc.edu.cn/2020/apply/daliy/post'
        # 每日进出校申请url
        self.stayinout_apply_url = 'https://weixine.ustc.edu.cn/2020/stayinout_apply'
        # 身份认证token
        self.token = ''

    def _get_token(self):
        """
        获取打卡时需要提供的验证字段
        """
        response = self.sess.get(self.cas_url)
        s = BeautifulSoup(response.text, 'lxml')
        token = s.find(attrs={'name': '_token'}).get('value')
        return token

    def _check_success(self, response):
        """
        简单check一下有没有成功打卡、报备
        """
        return '成功' in response.text

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
        打卡函数，需要提供包含表单内容的json文件
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

    def weekly_report(self):
        """
        报备函数
        报备成功返回1，七天内重复报备返回-1，因其他原因报备失败返回0
        """
        try:
            start_date = datetime.datetime.now()
            end_date = start_date + datetime.timedelta(days=6)
            data = {
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
                "_token": self.token
            }
            response = self.sess.post(self.report_url, data=data)
            if not self._check_success(response):
                if '你当前处于“在校已出校报备”状态' in response.text:
                    return -1
                return 0
            return 1
        except Exception as e:
            print(e)
            return 0

    def daily_stayinout_apply(self, apply_data_file, days=5):
        """
        2022年3月18日起每日进出校申请
        需要提供包含表单内容的json文件
        发现目前可以任意修改申请的天数: days
        申请成功返回True,申请失败返回False
        """
        try:
            with open(apply_data_file, 'r') as f:
                post_data = json.loads(f.read())
            post_data['_token'] = self.token
            now = datetime.datetime.now()
            post_data['start_date'] = now.strftime("%Y-%m-%d %H:%M:%S")
            post_data['end_date'] = (datetime.datetime(year=now.year, month=now.month, day=now.day,
                                                       hour=23, minute=59, second=59) + datetime.timedelta(
                days=days)).strftime('%Y-%m-%d %H:%M:%S')
            response = self.sess.post(self.stayinout_apply_url, data=post_data)
            return self._check_success(response)
        except Exception as e:
            print(e)
            return False
