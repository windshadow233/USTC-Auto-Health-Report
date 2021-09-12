# USTC-Auto-Health-Report
中科大健康打卡脚本

本项目仅供学习使用

# 环境

python==3.6

见requirements.txt

需要安装tesseract,参考版本为4.0.0-beta.1

# 使用方法

手动打卡并抓包，将除_token外的其他内容以JSON格式放置于post.json文件中，即可结合各类定时程序，调用脚本进行打卡。

健康打卡每天调用一次；出校报备一周仅需调用一次，时效为7天
