# USTC-Auto-Health-Report
中科大健康打卡脚本

# 环境依赖

python==3.6

requests==2.18.4

bs4==4.9.3

pytesseract(需要安装tesseract环境,后者版本为4.0.0-beta.1)

pillow==8.3.1

numpy==1.19.5

opencv-python==4.5.3

lxml==4.6.3

# 使用方法

手动打卡并抓包，将除去_token的其他内容放置于post.json文件中，即可结合各类定时程序，调用脚本进行打卡。
