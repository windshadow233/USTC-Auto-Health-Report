import json
from bs4 import BeautifulSoup
import datetime
import time
from PIL import ImageFont, Image, ImageDraw
import os
import random
import re
import io

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
        # 图片上传get url
        self.upload_url = 'https://weixine.ustc.edu.cn/2020/upload/xcm'
        # 图片上传post url
        self.upload_image_url = 'https://weixine.ustc.edu.cn/2020img/api/upload_for_student'
        # 每日进出校申请url
        self.stayinout_apply_url = 'https://weixine.ustc.edu.cn/2020/apply/daliy/ipost'
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
        s = BeautifulSoup(response.text, 'lxml')
        msg = s.select('.alert')[0].text
        return '成功' in msg

    def _generate_xing_cheng_ma(self, phone_number):
        dir_path = os.path.dirname(os.path.abspath(__file__))
        img_pil = Image.open(os.path.join(dir_path, "xcm/blank_xcm.jpg")).convert('RGBA')
        time_font = ImageFont.truetype(os.path.join(dir_path, "xcm/fonts/arial.ttf"), 33)
        draw = ImageDraw.Draw(img_pil)
        draw.text((242, 342), time.strftime("%Y.%m.%d %H:%M:%S", time.localtime()), (0x94, 0x94, 0x9e), time_font)
        if phone_number:
            mobile_number_font = ImageFont.truetype(os.path.join(dir_path, "xcm/fonts/arialbd.ttf"), 27)
            draw.text((178, 283), f'{phone_number[:3]}****{phone_number[-4:]}', (0x46, 0x46, 0x4c), mobile_number_font)
        arrow = Image.open(os.path.join(dir_path, "xcm/gif_green", random.choice(os.listdir(os.path.join(dir_path, "xcm/gif_green")))))
        r, g, b, a = arrow.split()
        img_pil.paste(arrow, (180, 400), mask=a)
        return img_pil

    def _get_gid_sign(self):
        r = self.sess.get(self.upload_url)
        gid = re.search("'gid': '(.*)'", r.text).groups()[0]
        sign = re.search("'sign': '(.*)'", r.text).groups()[0]
        return gid, sign

    def _upload_xing_cheng_ma(self, image):
        gid, sign = self._get_gid_sign()
        output = io.BytesIO()
        image.save(output, format='PNG')
        image = output.getvalue()
        data = {"_token": "", "gid": gid, "sign": sign, "t": 1, "id": "WU_FILE_0",
                "name": "Screenshot_Wechat.png", "type": "image/png",
                "file": "", 'size': len(image)}
        files = {'file': ("Screenshot_Wechat.png", image, "image/png", {})}
        r = self.sess.post(self.upload_image_url, data=data, files=files)
        return r.json()['status']

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

    def stayinout_apply(self, apply_data_file, phone_number=None):
        """
        2022年3月18日起每日进出校申请
        申请成功返回True,申请失败返回False
        :param apply_data_file表单数据文件
        :param phone_number手机号(用以生成行程码,若不提供则不自动上传行程码)
        """
        try:
            if phone_number is not None:
                xcm = self._generate_xing_cheng_ma(phone_number)
                status = self._upload_xing_cheng_ma(xcm)
                if not status:
                    return False
                time.sleep(random.randint(10, 20))
            with open(apply_data_file, 'r') as f:
                post_data = json.loads(f.read())
            now = datetime.datetime.now()
            post_data['_token'] = self.token
            post_data['start_date'] = now.strftime("%Y-%m-%d %H:%M:%S")
            post_data['end_date'] = now.strftime("%Y-%m-%d 23:59:59")
            response = self.sess.post(self.stayinout_apply_url, data=post_data)
            return self._check_success(response)
        except Exception as e:
            print(e)
            return False
