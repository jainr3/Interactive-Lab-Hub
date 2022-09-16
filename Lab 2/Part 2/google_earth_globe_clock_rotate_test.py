from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

import digitalio
import board
from PIL import Image, ImageDraw
import adafruit_rgb_display.ili9341 as ili9341
import adafruit_rgb_display.st7789 as st7789  # pylint: disable=unused-import
import adafruit_rgb_display.hx8357 as hx8357  # pylint: disable=unused-import
import adafruit_rgb_display.st7735 as st7735  # pylint: disable=unused-import
import adafruit_rgb_display.ssd1351 as ssd1351  # pylint: disable=unused-import
import adafruit_rgb_display.ssd1331 as ssd1331  # pylint: disable=unused-import


driver_path = '/usr/lib/chromium-browser/chromedriver'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
# browser is Chromium instead of Chrome
#chrome_options.BinaryLocation = "/usr/bin/chromium-browser"
# we use custom chromedriver for raspberry
#driver_path = "/usr/bin/chromedriver"
driver = webdriver.Chrome(driver_path, options=chrome_options)
#driver = webdriver.Chrome(options=chrome_options, service=Service(driver_path))
#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

print("Instantiated Chromium Drivers.")

driver.get('https://www.google.com/maps/@16.3451777,-125.0301768,23006762m/data=!3m1!1e3')
time.sleep(60)
screenshot = driver.save_screenshot('google_globe_0.png')
# getting the button by class name 
# TODO or SKIP: zoom in out doesnt work
#zoom_in_button = driver.find_element(By.CLASS_NAME, "ol-zoom-in")
#zoom_out_button = driver.find_element(By.CLASS_NAME, "ol-zoom-out")
#zoom_in_button.click()
#time.sleep(300)
#print("Saving screenshot.")

#screenshot = driver.save_screenshot('globe.png')

# Start the click and hold (or "rotate") test
#print("Rotating globe...")
#draggable = driver.find_element(By.CLASS_NAME, "ol-unselectable")
#start = draggable.location
#finish = draggable.location
#finish['x'] -= 50
#finish['y'] -= 50
#ActionChains(driver)\
#    .drag_and_drop_by_offset(draggable, finish['x'] - start['x'], finish['y'] - start['y'])\
#    .perform()

#time.sleep(60)
#screenshot = driver.save_screenshot('google_globe_1.png')

driver.quit()
