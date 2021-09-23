# USTC-Auto-Health-Report
中科大健康打卡脚本

支持通过统一身份认证登录（包括验证码识别） 进行打卡 & 出校报备

本项目仅供学习使用

# 环境

python==3.6

见requirements.txt

# 使用方法

手动打卡并抓包，将除_token外的其他内容以JSON格式放置于post.json文件中，即可结合各类定时程序，调用脚本进行打卡。

健康打卡每天调用一次；出校报备每周仅需调用一次，时效为7天。

调用示例:
```python
from ustc_auto_report import USTCAutoHealthReport

bot = USTCAutoHealthReport()
# 登录
login_success = bot.login('SAxxxxxxxx', 'password')
# 打卡
report_success = bot.daily_clock_in('post.json')
# 报备
post_success = bot.weekly_report()
```
