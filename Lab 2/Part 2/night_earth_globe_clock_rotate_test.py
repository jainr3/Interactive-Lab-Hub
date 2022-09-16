from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
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

"""chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--enable-automation")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-browser-side-navigation")
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--dns-prefetch-disable")
chrome_options.add_experimental_option('extensionLoadTimeout', 60000)
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)"""

# browser is Chromium instead of Chrome
#chrome_options.BinaryLocation = "/usr/bin/chromium-browser"
# we use custom chromedriver for raspberry
#driver_path = "/usr/bin/chromedriver"
driver = webdriver.Chrome(driver_path, options=chrome_options)
#driver = webdriver.Chrome(options=chrome_options, service=Service(driver_path))
#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

print("Instantiated Chromium Drivers.")

#driver.get('https://www.nightearth.com/?@37.09024,-95.712891,2z&data=$bWVsMmMxZDE=')
driver.get('https://www.nightearth.com/?@37.09024,-95.712891,2z&data=$bWVsc2Qx') # Satellite view
#satellite_button = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'mapbutton_satellite')))
#satellite_button = driver.find_element(By.ID, "mapbutton_satellite")
#satellite_button = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//div[@id='mapbutton_satellite']/button")))
#satellite_button = driver.find_element(By.XPATH, "//div[@id='mapbutton_satellite']/button")
#satellite_button.click()
print("Got the satellite view...")
time.sleep(60)
screenshot = driver.save_screenshot('globe_0.png')
# getting the button by class name 
# TODO or SKIP: zoom in out doesnt work
#zoom_in_button = driver.find_element(By.CLASS_NAME, "ol-zoom-in")
#zoom_out_button = driver.find_element(By.CLASS_NAME, "ol-zoom-out")
#zoom_in_button.click()
#time.sleep(300)
#print("Saving screenshot.")

#screenshot = driver.save_screenshot('globe.png')

# Start the click and hold (or "rotate") test

# Test 1 click and hold - fails
print("Rotating globe...")
#draggable = driver.find_element(By.ID, "map_canvas")
#start = draggable.location
#finish = draggable.location
#finish['x'] -= 50
#finish['y'] -= 50
#ActionChains(driver)\
#    .drag_and_drop_by_offset(draggable, finish['x'] - start['x'], finish['y'] - start['y'])\
#    .perform()

# Test 2 arrow keys - This works! (kind of slow...)
#canvas = driver.find_element(By.ID, "map_canvas")

#canvas.send_keys(Keys.ARROW_RIGHT)

#canvas.send_keys(Keys.ARROW_RIGHT)
#canvas.send_keys(Keys.ARROW_DOWN)

# Rotate alternate way with arrow keys

actions = ActionChains(driver)
for i in range(1, 9):
  actions.send_keys(Keys.ARROW_RIGHT).perform()
  screenshot = driver.save_screenshot(f'globe_{i}.png')
  time.sleep(5)
  print(f"Did globe {i}")

print("Finished center")
actions.send_keys(Keys.ARROW_UP).perform()
for i in range(1, 9):
  actions.send_keys(Keys.ARROW_RIGHT).perform()
  screenshot = driver.save_screenshot(f'globe_up_{i}.png')
  time.sleep(5)
  print(f"Did globe up {i}")

print("Finished up")
actions.send_keys(Keys.ARROW_DOWN).perform()
actions.send_keys(Keys.ARROW_DOWN).perform()
for i in range(1, 9):
  actions.send_keys(Keys.ARROW_RIGHT).perform()
  screenshot = driver.save_screenshot(f'globe_dn_{i}.png')
  time.sleep(5)
  print(f"Did globe down {i}")

print("Finished down")
print("Done Rotating")
driver.quit()
