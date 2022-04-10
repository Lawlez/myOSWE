#!/usr/bin/env python3
# -*- coding: utf8 -*-
import os
import sys
import json
import requests
import psutil
import time
import logging
sys.path.insert(1,"./lib")
from PIL import Image, ImageFont, ImageDraw
from lib import epd2in13_V2
from gpiozero import CPUTemperature

cpu = CPUTemperature()

# Set current directory

os.chdir(os.path.dirname(os.path.abspath(__file__)))
logging.basicConfig(level=logging.DEBUG)
    
def system_uptime():
  return time.time() - psutil.boot_time()

# check online status
try:
  r = requests.get('https://www.ncsc.admin.ch/ncsc/de/home.html')
  print(r.status_code)
  online = 'true' if r.status_code == 200 else 'false'
  print(online)
  logging.info("PiHole is online " + str(online))
except: 
  online = 'false'
  exit()

# get api data

try:
 
  r = requests.get('http://localhost/admin/api.php')
  json_string = r.json()
  adsblocked = json_string['ads_blocked_today']
  ratioblocked = json_string['ads_percentage_today']
  queries = json_string['dns_queries_today']
  queries_cached = json_string['queries_cached']
  logging.info(json_string)

  font2 = ImageFont.truetype('FiraCode-Regular', 12)
  font = ImageFont.truetype('FiraCode-SemiBold', 18)
  font3 = ImageFont.truetype("FiraCode-SemiBold", 28)
  
  epd = epd2in13_V2.EPD()
  epd.init(epd.FULL_UPDATE)
                  
  image = Image.new('1', (epd.height, epd.width), 255)  # 0: clear the frame
  draw = ImageDraw.Draw(image)
  draw.rectangle([(0,0),(249,120)],outline = 0)
  draw.rectangle([(2,2),(247,118)],outline = 0)
  
  if online == 'true':
  # pihole stats
 
    draw.text((5,2), str("Pi-Hole DNSSEC Filter"), font = font, fill = 0)
    draw.text((5,20), str("Ads blocked:   ") + str(adsblocked), font = font, fill = 0)
    draw.text((5,40), str("block ratio:   ") + str(round(ratioblocked, 2)) + "%", font = font, fill = 0)
    draw.text((5,60), str("DNS queries:   ") + str(queries), font = font, fill = 0)
    draw.text((5,80), str("Cached queries:") + str(queries_cached), font = font, fill = 0)
  
  # Time and OS info
    draw.text((4, 100), str("NET:" + online), font = font2, fill = 0)
    draw.text((65, 100), str(round(cpu.temperature)) + str("°C"), font = font2, fill = 0)
    draw.text((100, 100), str(round(system_uptime()/3600, 1)) + "h", font = font2, fill = 0)
    draw.text((188, 100), time.strftime('%H:%M:%S'), font = font2, fill = 0)
  
  elif online == 'false': 
    draw.text((5,40), "(ノò益ó)ノ彡┻━┻", font = font3, fill = 0)
    draw.text((5,80), str("NO INTERNET!!"), font = font, fill = 0)
    draw.text((65, 100), str(round(cpu.temperature)) + str("°C"), font = font2, fill = 0)
    draw.text((188, 100), time.strftime('%H:%M:%S'), font = font2, fill = 0)
    
  # draw shit
  image = image.transpose(Image.ROTATE_180)
  epd.display(epd.getbuffer(image))
  

except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13_V2.epdconfig.module_exit()
    exit()

except:
  exit()
