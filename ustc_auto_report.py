import requests
import json
from bs4 import BeautifulSoup
import pytesseract
from PIL import Image
import numpy as np
import cv2
import time


class USTCAutoHealthReport(object):
    def __init__(self):
        self.sess = requests.session()
        self.url = 'https://passport.ustc.edu.cn/login?service=https%3A%2F%2Fweixine.ustc.edu.cn%2F2020%2Fcaslogin'
        self.login_url = 'https://passport.ustc.edu.cn/login'
        self.validate_url = 'https://passport.ustc.edu.cn/validatecode.jsp?type=login'
        self.report_url = 'https://weixine.ustc.edu.cn/2020/daliy_report'
        self.number_file = ''
        self.number = ''

    def get_CAS_LT(self):
        """
        获取登录时需要提供的验证字段
        """
        response = self.sess.get(self.url)
        CAS_LT = BeautifulSoup(response.text, 'lxml').find(attrs={'id': 'CAS_LT'}).get('value')
        return CAS_LT

    def get_token(self, response):
        """
        获取打卡时需要提供的验证字段
        """
        s = BeautifulSoup(response.text, 'lxml')
        token = s.find(attrs={'name': '_token'}).get('value')
        return token

    def save_validate_number(self):
        """
        将验证码图片保存到一个文件
        """
        validate_number = self.sess.get(self.validate_url)
        self.number_file = str(time.time()) + '.jpg'
        with open('/tmp/' + self.number_file, 'wb') as f:
            f.write(validate_number.content)

    def recognize_validate_number(self):
        """
        识别验证码
        """
        image = cv2.imread('/tmp/' + self.number_file)
        kernel = np.ones((2, 2), np.uint8)
        image = cv2.dilate(image, kernel, iterations=1)
        image = Image.fromarray(image).convert('L')
        config = '--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789'
        self.number = pytesseract.image_to_string(image, config=config).strip()

    def login(self, username, password):
        """
        登录,需要提供用户名、密码
        """
        CAS_LT = self.get_CAS_LT()
        self.save_validate_number()
        self.recognize_validate_number()
        login_data = {
            'username': username,
            'password': password,
            'warn': '',
            'CAS_LT': CAS_LT,
            'showCode': '1',
            'button': '',
            'model': 'uplogin.jsp',
            'service': 'https://weixine.ustc.edu.cn/2020/caslogin',
            'LT': self.number
        }
        response = self.sess.post(self.login_url, login_data)
        token = self.get_token(response)
        return token

    def daily_report(self, post_data_file, token):
        """
        登录成功后，提交表单
        """
        with open(post_data_file, 'r') as f:
            post_data = json.loads(f.read())
        post_data['_token'] = token
        response = self.sess.post(self.report_url, data=post_data)
        return response

    def check_success(self, response):
        """
        简单check一下有没有成功打上卡
        """
        return '上报成功' in response.text

    def main(self, username, password, post_data_file):
        """
        主函数，需要提供用户名、密码以及包含表单内容的json文件
        """
        try:
            self.sess.cookies.clear()
            self.number_file = ''
            self.number = ''
            token = self.login(username, password)
            response = self.daily_report(post_data_file, token)
            return self.check_success(response)
        except:
            return False

# 调用示例
if __name__ == '__main__':
    bot = USTCAutoHealthReport()
    bot.main('SAxxxxxxxx', 'password', 'post.json')
