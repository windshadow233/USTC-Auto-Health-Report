# USTC-Auto-Health-Report

![GitHub](https://img.shields.io/github/license/windshadow233/USTC-Auto-Health-Report?style=plastic)
![Python](https://img.shields.io/badge/Language-Python-blueviolet?style=plastic)

## 中科大健康打卡脚本

- [x] 统一身份认证登录
    - [x] 验证码绕过
    - [ ] 验证码识别（能绕过为什么要识别？）
    
- [x] 健康打卡
- [x] 出校报备
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

## 出校报备

每周仅需调用一次，时效为7天。（目前该功能暂时不可用，替换为下面的进出校申请）

## 进出校申请

手动进行申请并抓包，将除_token、时间参数以外的内容以JSON格式放置于apply.json文件中，即可结合各类定时程序，调用脚本进行进出校申请。

若有多个相同参数，请以list数据类型存放。

函数的参数t表示申请前往的区域:

- 前往合肥市包河、庐阳、蜀山、瑶海区范围内校外：t=2
- 前往东西南北中校区：t=3
- 前往高新校区、先研院、国金院：t=4

每天调用一次。

## 调用示例:
```python
from ustc_auto_report import USTCAutoHealthReport

bot = USTCAutoHealthReport()
# 登录
bot.login('SAxxxxxxxx', 'password')
# 打卡
bot.daily_clock_in('post.json')
# 报备
bot.weekly_report()
# 进出校申请
bot.stayinout_apply('apply.json', t="3")
```
