# USTC-Auto-Health-Report

![GitHub](https://img.shields.io/github/license/windshadow233/USTC-Auto-Health-Report?style=plastic)
![Python](https://img.shields.io/badge/Language-Python-blueviolet?style=plastic)

## 中科大健康打卡脚本

- [x] 统一身份认证登录
    - [x] 验证码绕过
    - [ ] 验证码识别（能绕过为什么要识别？）
    
- [x] 健康打卡
- [x] 出校报备
- [x] 进出校报备
- [x] 进出校申请

本项目仅供学习使用，请勿过分依赖。开发者对使用本脚本造成的问题不负任何责任，不对脚本执行效果做出任何担保，原则上不提供任何形式的技术支持。

# 环境

python==3.6

见requirements.txt

# 使用方法

## 每日打卡
手动打卡并抓包，将除_token外的其他内容以JSON格式放置于post.json文件中，即可结合各类定时程序，调用脚本进行打卡。

示例见post.json。

每天调用一次。

## 进出校报备

每天调用一次，不需要经过老师审核。（目前该功能暂时不可用，替换为下面的进出校申请）

## 进出校申请

每天调用一次，需要经过老师审核。

## 调用示例:

```python
from ustc_auto_report import USTCAutoHealthReport

bot = USTCAutoHealthReport()
# 登录
bot.login('SAxxxxxxxx', 'password')
# 打卡
bot.daily_clock_in('post.json')
# 调整位置与字体大小，预览生成的行程码
bot.generate_xcm('18888888888', time_pos=(242, 342), phone_number_pos=(178, 283), display=True)
# 进出校报备
bot.report('report.json', True, '18888888888')  # 填写手机号，自动生成行程码并上传
bot.report('report.json', True)  # 不填手机号，只在行程码的时间位置生成时间字符串
bot.report('report.json', False)  # 不生成、也不上传行程码
# 进出校申请
bot.stayinout_apply('apply.json')
```
