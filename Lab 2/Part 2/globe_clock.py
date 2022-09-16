from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import smbus, time

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

def screenshot_image(driver, i, tag):
    screenshot = driver.save_screenshot(f'globe_{tag}_{i}.png')
    print(f"Done with screenshot {tag} {i}")

def collect_images(driver):
    print("Loading page")
    driver.get('https://www.nightearth.com/?@37.09024,-95.712891,2z&data=$bWVsc2Qx') # Satellite view
    time.sleep(60)

    print("Collecting images")
    actions = ActionChains(driver)
    for i in range(8):
        screenshot_image(driver, i, "cn")
        actions.send_keys(Keys.ARROW_RIGHT).perform()
        time.sleep(5)
    actions.send_keys(Keys.ARROW_UP).perform()
    for i in range(8):
        screenshot_image(driver, i, "up")
        actions.send_keys(Keys.ARROW_RIGHT).perform()
        time.sleep(5)
    actions.send_keys(Keys.ARROW_DOWN).perform()
    actions.send_keys(Keys.ARROW_DOWN).perform()
    for i in range(8):
        screenshot_image(driver, i, "dn")
        actions.send_keys(Keys.ARROW_RIGHT).perform()
        time.sleep(5)

def collect_image_flat_earth(driver):
    driver.get('https://static.die.net/earth/mercator/2048.jpg')
    print("Updating image and saving screenshot.")
    time.sleep(20)

    screenshot = driver.save_screenshot('earth.png')

def crop_image_flat_earth(scale, l, t, r, b):
    print(f"Cropping image at scale {scale} with l={l}, t={t}, r={r}, b={b}.")
    im = Image.open('earth.png')
    width, height = im.size
    left = l + r - (2-scale)*r#scale*l
    top = t + b - (2-scale)*b#scale*t
    right = (2 - scale)*r
    bottom = (2- scale)*b
    print(f"Effective limits after scale l={left}, t={top}, r={right}, b={bottom}.")

    im1 = im.crop((left, top, right, bottom))
    im1 = im1.convert('RGB')
    im1 = im1.save("earth_cropped.jpg")

def crop_image():
    print(f"Cropping images.")
    for tag in ["cn", "up", "dn"]:
        for i in range(8):              
            im = Image.open(f'globe_{tag}_{i}.png')
            width, height = im.size
            left = 210
            top = 170
            right = 570
            bottom = 525

            im1 = im.crop((left, top, right, bottom))
            im1 = im1.convert('RGB')
            im1 = im1.save(f"globe_{tag}_{i}_cropped.jpg")

# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# pylint: disable=line-too-long
# Create the display:
# disp = st7789.ST7789(spi, rotation=90,                            # 2.0" ST7789
# disp = st7789.ST7789(spi, height=240, y_offset=80, rotation=180,  # 1.3", 1.54" ST7789
# disp = st7789.ST7789(spi, rotation=90, width=135, height=240, x_offset=53, y_offset=40, # 1.14" ST7789
# disp = hx8357.HX8357(spi, rotation=180,                           # 3.5" HX8357
# disp = st7735.ST7735R(spi, rotation=90,                           # 1.8" ST7735R
# disp = st7735.ST7735R(spi, rotation=270, height=128, x_offset=2, y_offset=3,   # 1.44" ST7735R
# disp = st7735.ST7735R(spi, rotation=90, bgr=True,                 # 0.96" MiniTFT ST7735R
# disp = ssd1351.SSD1351(spi, rotation=180,                         # 1.5" SSD1351
# disp = ssd1351.SSD1351(spi, height=96, y_offset=32, rotation=180, # 1.27" SSD1351
# disp = ssd1331.SSD1331(spi, rotation=180,                         # 0.96" SSD1331
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)
# pylint: enable=line-too-long

backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

# for joystick
bus = smbus.SMBus(1)
addr = 0x20
global bus_data, X, Y

def display_image_on_screen(i, tag):
    print("Displaying Image.")
    # Create blank image for drawing.
    # Make sure to create image with mode 'RGB' for full color.
    if disp.rotation % 180 == 90:
        height = disp.width  # we swap height/width to rotate it to landscape!
        width = disp.height
    else:
        width = disp.width  # we swap height/width to rotate it to landscape!
        height = disp.height
    image = Image.new("RGB", (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
    disp.image(image)

    image = Image.open(f"globe_{tag}_{i}_cropped.jpg")

    # Scale the image to the smaller screen dimension
    image_ratio = image.width / image.height
    screen_ratio = width / height
    if screen_ratio < image_ratio:
        scaled_width = image.width * height // image.height
        scaled_height = height
    else:
        scaled_width = width
        scaled_height = image.height * width // image.width
    image = image.resize((scaled_width, scaled_height), Image.Resampling.BICUBIC)

    # Crop and center the image
    x = scaled_width // 2 - width // 2
    y = scaled_height // 2 - height // 2
    image = image.crop((x, y, x + width, y + height))

    # Display image.
    disp.image(image)

def display_flat_earth_image_on_screen(): # slightly different things in some places
    print("Displaying Flat Earth Image.")
    # Create blank image for drawing.
    # Make sure to create image with mode 'RGB' for full color.
    if disp.rotation % 180 == 90:
        height = disp.width  # we swap height/width to rotate it to landscape!
        width = disp.height
    else:
        width = disp.width  # we swap height/width to rotate it to landscape!
        height = disp.height
    image = Image.new("RGB", (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
    disp.image(image)

    image = Image.open("earth_cropped.jpg")
    image = image.rotate(90, expand=True)

    # Scale the image to the smaller screen dimension
    image_ratio = image.width / image.height
    screen_ratio = width / height
    if screen_ratio < image_ratio:
        scaled_width = image.width * height // image.height
        scaled_height = height
    else:
        scaled_width = width
        scaled_height = image.height * width // image.width

    image = image.resize((scaled_width, scaled_height), Image.Resampling.BICUBIC)

    # Crop and center the image
    x = scaled_width // 2 - width // 2
    y = scaled_height // 2 - height // 2
    image = image.crop((x, y, x + width, y + height))

    # Display image.
    disp.image(image)

def qwiicjoystick():
    global bus_data, X, Y
    
    try:
        bus_data = bus.read_i2c_block_data(addr, 0x03, 5)
        #X_MSB = bus.read_byte_data(addr, 0x03) # Reads MSB for horizontal joystick position
        #X_LSB = bus.read_byte_data(addr, 0x04) # Reads LSB for horizontal joystick position
    
        #Y_MSB = bus.read_byte_data(addr, 0x05) # Reads MSB for vertical joystick position
        #Y_LSB = bus.read_byte_data(addr, 0x06) # Reads LSB for vertical joystick position

        #Select_Button = bus.read_byte_data(addr, 0x07) # Reads button position
    except Exception as e:
        print(e)

    X = (bus_data[0]<<8 | bus_data[1])>>6
    Y = (bus_data[2]<<8 | bus_data[3])>>6
    
    
    #print(X_MSB, Y_MSB)

    time.sleep(.5) # dont need readings very often
    if bus_data[4] not in [0, 1]: # bad data reading for this one?, ignore and continue
        return
    #print(X, Y, " Button = ", bus_data[4])
    direction = None
    #time.sleep(1)
    if X < 450:
        direction = "RIGHT"
    elif 575 < X:
        direction = "LEFT"

    
    if Y< 450:
        direction = "DOWN"
    elif 575 < Y:
        direction = "UP"

    #print(direction)

    #if Select_Button == 1:
    if bus_data[4] == 0:
        direction = "SELECT" # to switch to the flat view
    return direction


# Start the main program here
image_num = 0
tag = "cn"
scale = 1.00
l, t, r, b = 140, 170, 140 + 240, 170 + 135 
update = False
#collect_images(driver) # TODO spawn a separate thread to collect the images every 30 minutes
#collect_image_flat_earth(driver)
crop_image()
crop_image_flat_earth(scale, l, t, r, b)
display_image_on_screen(image_num, tag)
globe_mode = True
while True:
    joy_direction = qwiicjoystick()
    if joy_direction == "SELECT":
        globe_mode = not globe_mode
        update = True
    # Joystick controls rotation of globe images and pan of flat image
    elif joy_direction == "RIGHT":
        if globe_mode:
            image_num += 1
            image_num %= 8
        else:
            old_r = r
            r = min(800, old_r + (old_r - l))
            l = r - (old_r - l)
        update = True
    elif joy_direction == "LEFT":
        if globe_mode:
            image_num -= 1
            image_num %= 8
        else:
            old_l = l
            l = max(0, l - (r - old_l))
            r = l + (r - old_l)
        update = True
    elif joy_direction == "DOWN":
        if globe_mode:
            if tag == "up":
                tag = "cn"
                update = True
            elif tag == "cn":
                tag = "dn"
                update = True
        else:
            old_b = b
            b = min(520, b + (old_b - t))
            t = b - (old_b - t)
            update = True
    elif joy_direction == "UP":
        if globe_mode:
            if tag == "dn":
                tag = "cn"
                update = True
            elif tag == "cn":
                tag = "up"
                update = True
        else:
            old_t = t
            t = max(80, t - (b - old_t))
            b = t + (b - old_t)
            update = True
    # Flat earth mode
    # Whenever buttonA is pressed, zoomOut; buttonB is zoomIn
    if buttonB.value and not buttonA.value and not globe_mode:  # just button A pressed ... zoom into the regular canvas
        scale += 0.05
        scale = min(scale, 1.20)
        update = True

    if buttonA.value and not buttonB.value and not globe_mode:  # just button B pressed
        scale -= 0.05
        scale = max(scale, 1.00)
        update = True


    if update:
        if globe_mode:
            display_image_on_screen(image_num, tag)
        else:
            crop_image_flat_earth(scale, l, t, r, b)
            display_flat_earth_image_on_screen()
        update = False

    #if (not buttonA.value and not buttonB.value):  # none pressed
    #    pass

driver.quit()
