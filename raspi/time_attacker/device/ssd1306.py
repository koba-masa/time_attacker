import board
import busio
import adafruit_ssd1306

import time

# https://www.amazon.co.jp/dp/B085C67PF1
# https://micropython-docs-ja.readthedocs.io/ja/latest/esp8266/tutorial/ssd1306.html
# https://learn.adafruit.com/monochrome-oled-breakouts/python-setup
class SSD1306:
  def __init__(self, slave_address, width, hight):
    self.slave_address = slave_address
    self.width = width
    self.hight = hight
    self.setup()

  def setup(self):
    self.i2c = busio.I2C(board.SCL, board.SDA)
    self.oled = adafruit_ssd1306.SSD1306_I2C(self.width, self.hight, self.i2c, addr=self.slave_address)
    self.clear()

  def clear(self):
    self.oled.fill(0)
    self.oled.show()

  def write(self, image):
    self.oled.image(image)
    self.oled.show()

  def reset(self):
    self.clear()
