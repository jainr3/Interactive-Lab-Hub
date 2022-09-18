# Interactive Prototyping: The Clock of Pi
**NAMES OF COLLABORATORS HERE**: Rahul Jain

Does it feel like time is moving strangely during this semester?

For our first Pi project, we will pay homage to the [timekeeping devices of old](https://en.wikipedia.org/wiki/History_of_timekeeping_devices) by making simple clocks.

It is worth spending a little time thinking about how you mark time, and what would be useful in a clock of your own design.

**Please indicate anyone you collaborated with on this Lab here.**

* I worked on this lab by myself, and I was inspired from a few different sources:
  * [The Billion Dollar Code Netflix Series](https://en.wikipedia.org/wiki/The_Billion_Dollar_Code)
  * [Nasa Mars Clock](https://www.giss.nasa.gov/tools/mars24/)
  * Main source for Earth images is the [die.net World Sunlight Map](https://www.die.net/earth/)
  * Main source for Globe images is [nightearth.com](https://www.nightearth.com/)
  * Many different sun clocks like these: [1](https://www.mathsisfun.com/sun-clock.html), [2](https://zoom.earth/), [3](https://www.timeanddate.com/worldclock/sunearth.html?iso=20151222T1648&earth=1), [Google Earth](https://www.google.com/maps/@13.3406399,-114.6590665,22983304m/data=!3m1!1e3) ([Google Earth](./img/google_maps.png) requires sign-in else [this happens](./Part%202/google_globe_0.png))

## Overview
For this assignment, you are going to 

A) [Connect to your Pi](#part-a)  

B) [Try out cli_clock.py](#part-b) 

C) [Set up your RGB display](#part-c)

D) [Try out clock_display_demo](#part-d) 

E) [Modify the code to make the display your own](#part-e)

F) [Make a short video of your modified barebones PiClock](#part-f)

G) [Sketch and brainstorm further interactions and features you would like for your clock for Part 2.](#part-g)

## Part A. 
### Connect to your Pi
I was able to connect to my Pi over SSH and setup a personal access token to push code from the Pi.

<img src="img/part_a.png" alt="Part A">

## Part B. 
### Try out the Command Line Clock
I was able to clone the lab-hub repo on the Pi and install the packages and then run the script which just printed out the current date / time.

## Part C. 
### Set up your RGB Display
I was able to successfully setup the RGB Display.

### Hardware (you have done this in the prep)
I was able to successfully connect the RGB Display to the Pi.

### Testing your Screen
The short video for the screen test is below:

[![Screen Test](https://img.youtube.com/vi/Rs2h-IAYhHg/0.jpg)](https://www.youtube.com/watch?v=Rs2h-IAYhHg)

#### Displaying Info with Texts
This test to display text on the screen with `stats.py` was successful.

<img src="img/part_c_stats.png" alt="Part C Stats" width=400>

#### Displaying an image
I was able to use `image.py` to display the basic image and also use the code from the screen test to push a button and swap to another image.

<img src="img/part_c_image.png" alt="Part C Image" width=400>

Video:

[![Image Swap](https://img.youtube.com/vi/39Yqq0AsUIo/0.jpg)](https://www.youtube.com/watch?v=39Yqq0AsUIo)

## Part D. 
### Set up the Display Clock Demo
I successfully edited `screen_clock.py` to show the time by filling in the while loop. I used the code in `cli_clock.py` and `stats.py` to generate a clock time and draw it in blue text on the screen.

<img src="img/part_d_demo.png" alt="Part D Demo">

### How to Edit Scripts on Pi
I am familiar with using the nano editor to edit scripts on the Pi. However, I opted to use the [Visual Studio Code SSH Plugin](https://code.visualstudio.com/docs/remote/ssh) which lets me code in VS Code from my laptop while all the files are stored on the Pi. I can also open an integrated terminal in VS Code and run the scripts remotely.

## Part E.
### Modify the barebones clock to make it your own

Introducing the EarthClock. My clock measures time based on the sunlight over the earth. For example, the following pair of images shows the sunlight patterns at 10:30 AM and 11:30PM. The user can infer what time it is at their geographic location by looking at these images similar to the way a sundial operates (e.g. sun's rays = time).

**Sunlight Pattern at 10:30 AM**

<img src="img/part_e_10_30_am.jpg" alt="Part E 10:30 AM" width=400>

**Sunlight Pattern at 11:30 PM**

<img src="img/part_e_11_30_pm.jpg" alt="Part E 11:30 PM" width=400>

I created a Verplank diagram for my idea:

<img src="img/verplank.png" alt="Verplank Diagram">

As noted in the diagram, the buttons can be used to zoom in and out on the earth image. The reason for doing this is that the screen size is too small to show any specific locations with an adequate amount of detail. This opens up my idea to further modifications which are described in Part G below. Overall, the zoom in / out feature allows users to see as much or as little detail for an approaching sunrise / sunset as well as how "far away" these times are.

\*\*\***A copy of your code should be in your Lab 2 Github repo.**\*\*\*

I had to do a few creative things to get the right earth images since it was especially challenging to find a live map API or service. I found a few websites that overlaid the sunlight shading onto the Earth but none of them offered an API that I could easily get the data or an image. Instead, I opted to use Chrome's chromedriver for python which basically allows me to open a webpage on the Raspberry Pi's webbrowser and take a screenshot. This was especially tricky since some pages take a variable amount of time to load the 3D model or image, but since I don't want to really update my image very often it was acceptable. Interestingly enough, I couldn't use wget or curl to retreive the image directly for the [die.net World Sunlight Map](https://www.die.net/earth/) since the website returned a 503 Service Unavailable code.

I first considered using [nightearth.com](https://www.nightearth.com/) which has a nice globe looking display, but I quickly realized that because of the 3D modeling, the Raspberry Pi could not handle loading the graphics consistently between zooming in / out the globe. Additionally, this website doesn't seem to "turn off" the lights from towns and cities during the day which makes the image a bit misleading. Instead, I opted to use the [die.net World Sunlight Map](https://www.die.net/earth/) which also has live data (every half hour) for the sunlight and also cloud coverage (updated daily) overlaid onto a Mercator projection of the Earth. Using this, I cropped the image and displayed it onto the LCD screen. Whenever the zoom in / zoom out button is pressed, I simply scale the cropped image (within some limits) and display that. I only fetch the image every 30 minutes since that is how often the website updates theirs. The full code is located in the `earth_clock.py` and the testing scripts that I used are `globe_clock_testing.py` and `earth_clock_testing.py`.

The globe image from [nightearth.com](https://www.nightearth.com/) that I didn't end up using (and how it looked on the screen):

<img src="img/globe_clock_testing.jpg" alt="Globe Clock Testing" width=400>
<img src="img/globe_clock_display_test.png" alt="Globe Clock Display Test" width=400>

The Mercator projection from [die.net World Sunlight Map](https://www.die.net/earth/) (and the cropped version that gets displayed):

<img src="img/mercator_clock.jpg" alt="Mercator Clock">

<img src="img/mercator_clock_cropped.jpg" alt="Mercator Clock Cropped">

The documentation that I referenced to create these scripts are listed below:

* https://stackoverflow.com/a/52572919
* https://sites.google.com/a/chromium.org/chromedriver/getting-started
* https://ivanderevianko.com/2020/01/selenium-chromedriver-for-raspberrypi
* https://www.pythonanywhere.com/forums/topic/28261/
* https://stackoverflow.com/questions/64717302/deprecationwarning-executable-path-has-been-deprecated-selenium-python
* https://stackoverflow.com/questions/70886717/chromedriver-for-linux32-does-not-exist-python-selenium-chromedriver
* https://pillow.readthedocs.io/en/stable/deprecations.html
* https://selenium-python.readthedocs.io/locating-elements.html
* https://stackoverflow.com/questions/72773206/selenium-python-attributeerror-webdriver-object-has-no-attribute-find-el

## Part F. 
## Make a short video of your modified barebones PiClock

\*\*\***Take a video of your PiClock.**\*\*\*

Video of the Zoom Out feature

[![Zoom Out](https://img.youtube.com/vi/YK0vy8ecRP0/0.jpg)](https://www.youtube.com/watch?v=YK0vy8ecRP0)

Video of the Zoom In feature

[![Zoom In](https://img.youtube.com/vi/YfOPFjc1BsQ/0.jpg)](https://www.youtube.com/watch?v=YfOPFjc1BsQ)

## Part G. 
## Sketch and brainstorm further interactions and features you would like for your clock for Part 2.
Another function that might be desired by the user is the ability to pan around the image to see different parts of the Earth. This could be very useful if they don't know whether their friend on the other side of the world is awake or not. To control this, the user could use a joystick to move the image around the screen.

Also, depending on the exact technical implementation, I could overlay some text to show the digital time or possibly the timezone for the location currently shown. This could be useful so the user doesn't have to "eyeball" the time (although the main purpose of this clock is to indicate day / night at a high level and whether it is close to sunrise / sunset). To implement this, I would have to figure out the coordinates on the static map and then convert that to the time / timezone, which might be very difficult!

Another idea could be to somehow incorporate the globe view if a different button is pressed. Although the zoom in / out for that view seems out of reach for the lab, it would be interesting to test whether I could rotate the globe and show that to the user.

# Prep for Part 2

## Peer Review Comments:

* Joseph Iovine : Try adding a reset button for the zoom

* Yusef Iskandar: Maybe add a scale, plus / minus visual button (piece of paper on the button)

* Kenneth Alvarez: Consider adding a list of images for the globe to solve the latency problem

From this feedback, I decided to try using the globe view in combination with the earth's Mercator view. Because it was not technically possible to show a "video" of the earth rotating on the screen, I used the list of images idea instead so the user could pan around. I also added a plus / minus to the button so it was more obvious which was which.

## Updated Verplank Diagram

<img src="img/updated_verplank.png" alt="Updated Verplank Diagram">

The big changes are the addition of the Globe view and the joystick which allows the user to pan around the globe or the flat map. To swap between views, the joystick button is used.

# Lab 2 Part 2

## Feature Improvements

There were different pieces to implementing the project and a couple different technical tools that I used to make everything work (listed below):

* **Obtaining the Live Mercator Projection (Flat) Image**: I took the image from the [die.net World Sunlight Map](https://www.die.net/earth/) by webscraping it using Selenium in Python. This image is updated every 30 minutes as described above.
\
<img src="img/mercator_clock.jpg" alt="Mercator Clock" width="400">

* **Obtaining the Live Globe Image**: This was the most complicated / difficult step. I took the 24 different images of the globe from [nightearth.com](https://www.nightearth.com/) in the Satellite view by webscraping it using Selenium in Python. Previously in part 1 of the lab, I only looked at the Night view which I thought was a bit misleading (since in areas where it was daytime would still show city lights), but the Satellite view shows the sun shading properly. See below for some examples. I had to capture 8 different images to get all the perspectives around the globe and then also 8 more for the top part of the globe and 8 more for the bottom part. These images are updated every 30 minutes and because Selenium is a bit slow, this process takes about 5 minutes which is acceptable for this use case. The testing script for this is [here](./Part%202/night_earth_globe_clock_rotate_test.py).


<img src="Part 2/globe_cn_0_cropped.jpg" alt="Satellite View" width="200"/><img src="Part 2/globe_cn_1_cropped.jpg" alt="Satellite View" width="200"/><img src="Part 2/globe_cn_2_cropped.jpg" alt="Satellite View" width="200"/><img src="Part 2/globe_cn_5_cropped.jpg" alt="Satellite View" width="200"/>
* **Cropping & displaying the Mercator Projection (Flat) Image**: I cropped the image to match the size of the screen. The cropping also had to take into account the scaling of the image and had to resize / rescale the image depending on if the user wants a zoomed in view. Additionally, I had to crop different sections of the image based on where the user was panning to. I tried a few different self-designed algorithms, so there might be some edge cases that are buggy. Some of the scratch work for that is [here](./Part%202/scaling_scratchwork.pdf) and the test code for cropping is [here](./Part%202/earth_clock_testing.py).
* **Cropping & displaying the Globe View Images**: I cropped the image according to some preset coordinates (square) and then resized it so that it fit on the screen. Since this view only has the pan feature, I cropped all 24 images once and then just displayed them when the user panned to that area.
* **Zoom In / Out on the Mercator (Flat) Image**: The two buttons located on the display allow for zooming in and out within some limits. This is good for users who want to zoom in on a particular area.
* **User Panning**: For both the globe and flat views, the user can pan around to see different areas of the earth. For the globe image, the panning is allowed for 3 layers around the entire globe and the user can pan all the way around in any direction. The flat view allows the user to pan around in the image but limits the panning to the edges of the image. The user input for the panning comes from the Qwiic Joystick which I use like "arrow keys" to control the direction.
* **Qwiic Joystick**: The qwiic joystick was added so the user can pan the image on the screen to see whether it is day or night at a particular location. Additionally, pressing the button on the joystick lets the user switch between the globe and flat views. A short script to test that is located [here](./Part%202/qwiic_joystick.py).

## Final script and other testing

**The final code script is located [here](./Part%202/globe_clock.py).** I also experimented with using the two buttons on the screen to let the user rotate the globe image side to side (script is [here](./Part%202/globe_clock_simple.py)) but this was only good if the user didn't want to pan up and down as well. I also tried to use the google earth globe which has much better graphics (see below) but I wasn't able to have the Pi automatically grab the live image using Selenium.

<img src="img/google_maps.png" alt="Google Earth" width="200">

## Video documenting globe view feature

Rotating the joystick will let the user pan around the globe to see different views.

[![Globe View Feature](https://img.youtube.com/vi/Lz7R5ytabOo/0.jpg)](https://www.youtube.com/watch?v=Lz7R5ytabOo)

## Video documenting Mercator (flat) view feature

Rotating the joystick will let the user pan around the flat image to see different views and pressing the buttons will allow for zoom in / out.

[![Flat View Feature](https://img.youtube.com/vi/e0Bt10zUVuw/0.jpg)](https://www.youtube.com/watch?v=e0Bt10zUVuw)

## Final Video of Interaction

[![Final Video of Interaction](https://img.youtube.com/vi/tXeU4mNqZ1E/0.jpg)](https://www.youtube.com/watch?v=tXeU4mNqZ1E)


## References

The documentation that I referenced to create these scripts are listed below:

* https://stackoverflow.com/questions/70410883/using-arrow-keys-on-chrome-selenium-popup-python
* https://www.geeksforgeeks.org/special-keys-in-selenium-python/
* https://www.browserstack.com/guide/python-selenium-to-run-web-automation-test
* https://stackoverflow.com/questions/26566799/wait-until-page-is-loaded-with-selenium-webdriver-for-python
* https://selenium-python.readthedocs.io/locating-elements.html
* https://github.com/sparkfun/Qwiic_Joystick_Py
* https://github.com/sparkfun/Qwiic_Joystick/blob/master/Firmware/Python%20Examples/Example%201%20-%20Basic%20Readings/Qwiic_Joystick.py
* https://docs.particle.io/hardware/expansion/about-i2c/#i2c-scanner
* https://learn.sparkfun.com/tutorials/qwiic-joystick-hookup-guide/hardware-overview
