# -*- coding: UTF-8 -*-
import pytesseract

# เรียกใช้โมดูล Image จาก Pillow
from PIL import Image
# เปิดรูปภาพตามที่อยู่ที่ได้ใส่ไว้ แล้วเก็บไว้ในตัวแปร img
img = Image.open('lic6 shot.jpg')

txt = pytesseract.image_to_string(img, lang='tha')
