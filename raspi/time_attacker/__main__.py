import RPi.GPIO as GPIO

import time
import math

from PIL import Image, ImageDraw, ImageFont
from device.ssd1306 import SSD1306

class TimeAttacker:
  def __init__(self):
    # 測定中のランプ
    self.processed_lamp = 13
    # 開始ボタン
    self.start_btn = 19
    # 終了ボタン
    self.finish_btn = 26

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.processed_lamp, GPIO.OUT)
    GPIO.setup(self.start_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(self.finish_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)

  def execute(self):
    GPIO.add_event_detect(self.start_btn, GPIO.FALLING, callback=self.start, bouncetime=350)
    GPIO.add_event_detect(self.finish_btn, GPIO.FALLING, callback=self.finish, bouncetime=350)
    GPIO.output(self.processed_lamp, GPIO.LOW)

    # self.display = SSD1306(0x3c, 128, 32)
    self.display = SSD1306(0x3c, 128, 64)
    self.write("Ready")

    try:
      while True:
        time.sleep(100000000)
    except Exception as e:
      print(e)
    finally:
      GPIO.cleanup(self.processed_lamp)
      GPIO.remove_event_detect(self.start_btn)
      GPIO.cleanup(self.start_btn)
      GPIO.remove_event_detect(self.finish_btn)
      GPIO.cleanup(self.finish_btn)
      self.display.reset()

  def start(self, gpio):
    print("start")
    self.display.reset()
    self.write("start")
    self.start = time.perf_counter()
    self.turn_on_led()

  def finish(self, gpio):
    if GPIO.input(self.processed_lamp) == 1:
      print("finish")
      self.display.reset()
      self.end = time.perf_counter()
      attack_time = self.calculate(self.start, self.end)
      print(attack_time)
      formatted_attack_time = format(attack_time, '.1f') + '  Sec'
      self.write(formatted_attack_time)
      self.turn_off_led()
      self.reset()

  def write(self, text):
    #font = ImageFont.load_default()
    font = ImageFont.truetype(font='/usr/share/fonts/truetype/piboto/PibotoLt-Regular.ttf', size=30)
    # https://pillow.readthedocs.io/en/stable/reference/Image.html#constructing-images
    image = Image.new('1', (self.display.width, self.display.hight), 0)
    draw = ImageDraw.Draw(image)
    font_width, font_height = font.getsize(text)
    draw.text(
        (self.display.width // 2 - font_width // 2, self.display.hight // 2 - font_height // 2),
        text,
        font=font,
        fill=255,
    )
    self.display.write(image)

  def reset(self):
    self.start = 0
    self.end = 0

  def turn_on_led(self):
    GPIO.output(self.processed_lamp, GPIO.HIGH)

  def turn_off_led(self):
    GPIO.output(self.processed_lamp, GPIO.LOW)

  def calculate(self, start_time, end_time):
    return end_time - start_time

TimeAttacker().execute()
