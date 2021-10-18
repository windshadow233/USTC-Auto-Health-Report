# USTC-Auto-Health-Report

![GitHub](https://img.shields.io/github/license/windshadow233/USTC-Auto-Health-Report?style=plastic)
![Python](https://img.shields.io/badge/Language-Python-blueviolet?style=plastic)

## 中科大健康打卡脚本

- [x] 统一身份认证登录
    - [x] 验证码绕过
    - [ ] 验证码识别（能绕过为什么要识别？）
    
- [x] 健康打卡
- [x] 出校报备

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
bot.login('SAxxxxxxxx', 'password')
# 打卡
bot.daily_clock_in('post.json')
# 报备
bot.weekly_report()
```
