# Ph-UI!!!

**NAMES OF COLLABORATORS HERE** Rahul Jain


For lab this week, we focus both on sensing, to bring in new modes of input into your devices, as well as prototyping the physical look and feel of the device. You will think about the physical form the device needs to perform the sensing as well as present the display or feedback about what was sensed. 

## Part 1 Lab Preparation

### Get the latest content:

I have pulled the latest content.

### Start brainstorming ideas by reading: 
* [What do prototypes prototype?](https://www.semanticscholar.org/paper/What-do-Prototypes-Prototype-Houde-Hill/30bc6125fab9d9b2d5854223aeea7900a218f149)
* [Paper prototyping](https://www.uxpin.com/studio/blog/paper-prototyping-the-practical-beginners-guide/) is used by UX designers to quickly develop interface ideas and run them by people before any programming occurs. 
* [Cardboard prototypes](https://www.youtube.com/watch?v=k_9Q-KDSb9o) help interactive product designers to work through additional issues, like how big something should be, how it could be carried, where it would sit. 
* [Tips to Cut, Fold, Mold and Papier-Mache Cardboard](https://makezine.com/2016/04/21/working-with-cardboard-tips-cut-fold-mold-papier-mache/) from Make Magazine.
* [Surprisingly complicated forms](https://www.pinterest.com/pin/50032245843343100/) can be built with paper, cardstock or cardboard.  The most advanced and challenging prototypes to prototype with paper are [cardboard mechanisms](https://www.pinterest.com/helgangchin/paper-mechanisms/) which move and change. 
* [Dyson Vacuum Cardboard Prototypes](http://media.dyson.com/downloads/JDF/JDF_Prim_poster05.pdf)
<p align="center"><img src="https://dysonthedesigner.weebly.com/uploads/2/6/3/9/26392736/427342_orig.jpg"  width="200" > </p>

### Gathering materials for this lab:

* Cardboard (start collecting those shipping boxes!)
* Found objects and materials--like bananas and twigs.
* Cutting board
* Cutting tools
* Markers

(We do offer shared cutting board, cutting tools, and markers on the class cart during the lab, so do not worry if you don't have them!)

## Deliverables \& Submission for Lab 4

The deliverables for this lab are, writings, sketches, photos, and videos that show what your prototype:
* "Looks like": shows how the device should look, feel, sit, weigh, etc.
* "Works like": shows what the device can do.
* "Acts like": shows how a person would interact with the device.

For submission, the readme.md page for this lab should be edited to include the work you have done:
* Upload any materials that explain what you did, into your lab 4 repository, and link them in your lab 4 readme.md.
* Link your Lab 4 readme.md in your main Interactive-Lab-Hub readme.md. 
* Group members can turn in one repository, but make sure your Hub readme.md links to the shared repository.
* Labs are due on Mondays, make sure to submit your Lab 4 readme.md to Canvas.


## Lab Overview

A) [Capacitive Sensing](#part-a)

B) [OLED screen](#part-b) 

C) [Paper Display](#part-c)

D) [Materiality](#part-d)

E) [Servo Control](#part-e)

F) [Record the interaction](#part-f)

## The Report (Part 1: A-D, Part 2: E-F)

### Part A
### Capacitive Sensing, a.k.a. Human-Twizzler Interaction 

<p float="left">
<img src="https://cdn-learn.adafruit.com/guides/cropped_images/000/003/226/medium640/MPR121_top_angle.jpg?1609282424" height="150" />
</p>

I was able to successfully test the capacitance sensor. A short video is below.

[![Part 1 (A) Capacitance Sensor Test](https://img.youtube.com/vi/IirIRkTAhOM/0.jpg)](https://www.youtube.com/watch?v=IirIRkTAhOM)

### Part B
### More sensors

#### Light/Proximity/Gesture sensor (APDS-9960)

<img src="https://cdn-shop.adafruit.com/970x728/3595-03.jpg" width=200>

#### Rotary Encoder

<p float="left">
<img src="https://cdn-shop.adafruit.com/970x728/4991-01.jpg" height="200" />
<img src="https://cdn-shop.adafruit.com/970x728/377-02.jpg" height="200" />
<img src="https://cdn-shop.adafruit.com/970x728/4991-09.jpg" height="200">
</p>

#### Joystick

<p float="left">
<img src="https://cdn.sparkfun.com//assets/parts/1/3/5/5/8/15168-SparkFun_Qwiic_Joystick-01.jpg" height="200" />
</p>

#### Distance Sensor

<p float="left">
<img src="https://cdn.sparkfun.com//assets/parts/1/6/0/3/4/17072-Qwiic_Multi_Distance_Sensor_-_VL53L3CX-01.jpg" height="200" />
</p>

#### Results for the Light/Proximity/Gesture sensor, Rotary Encoder, Joystick, and Distance sensor

I was able to successfully test all of these sensors. For the Rotary Encoder, I was able to light up the LED on the board. A short video of these sensor tests is below.

[![Part 1 (B) More Sensors Test](https://img.youtube.com/vi/mF1nCXS7cWI/0.jpg)](https://www.youtube.com/watch?v=mF1nCXS7cWI)

### Part C
### Physical considerations for sensing

**Chosen Sensor: Adafruit Circuit Playground Express**

<img src="img/circuit_playground_express-labeled.jpg" alt="Circuit Playground Express" width="500"/>

**\*\*\*Draw 5 sketches of different ways you might use your sensor, and how the larger device needs to be shaped in order to make the sensor useful.\*\*\***

### Sketch / Verplank Diagram 1: Capacitive Lock

The first idea is a capacitive lock which is intended to work like an (cost-effective) version of an electronic padlock with "buttons". Instead, I will use the capacitance sensors and copper tape to detect "button" presses. The neopixel lights on the lock will light up when a user is making an attempt to unlock it. Certain lights will light up green on each button press and when the enter button is pressed they will light up all green if the correct combination is entered else all red if it was wrong. Additionally, if the combination is incorrect a small buzzing sound will play.

<img src="img/part_c_sketch_1.png" alt="Sketch 1"/>

<img src="img/part_c_verplank_1.png" alt="Verplank 1"/>

### Sketch / Verplank Diagram 2: Light-level aware lamp

The next idea is to create a light-level aware lamp. This might be useful for people who are sitting at their desk and studying over the course of the day / night. Often times, the sun sets but people don't notice this and they end up trying to squint at their laptop screen or textbook without adequate lighting. Instead of this, the light-level aware lamp will automatically detect the light level and turn the lamp on to the correct brightness based on what level of light it detects in the room. This idea would again make use of the capacitance sensors and the neopixel LEDs on the board.

<img src="img/part_c_sketch_2.png" alt="Sketch 2"/>

<img src="img/part_c_verplank_2.png" alt="Verplank 2"/>

### Sketch / Verplank Diagram 3: Capacitive music controller

The next idea is to simply use the capacitance sensors to control songs that are being played. Based on the pad that is pressed, the song will change to a corresponding preselected song. In addition, a knob will be used to increase / decrease the volume and the slide switch can be used to pause / play the song.

<img src="img/part_c_sketch_3.png" alt="Sketch 3"/>

<img src="img/part_c_verplank_3.png" alt="Verplank 3"/>

### Sketch / Verplank Diagram 4: Arcade games

For the fourth idea, I will use the capacitance sensors to make a small arcade game device with 3 different games. The first game is the spinning light game where the light is spinning around at various speeds where the player has to press the capacitance sensor at the right time to score the points (at which point the lights will also flash green/red depending on if the selection was correct). The second game is the reaction time game, where the user will observe random lights being lit up and has to press the capacitance sensor at the right time (not early and not late) to score the points. Finally, the third game is a memory game where the lights get lit up in a sequence and the user has to try to remember the pattern. After the sequence has been lit up, they simply have to hit the correct capacitance sensor pads in the right order to score the points and advance to the next level.

<img src="img/part_c_sketch_4.png" alt="Sketch 4"/>

<img src="img/part_c_verplank_4.png" alt="Verplank 4"/>

### Sketch / Verplank Diagram 5: Dice alternative

The final idea is an alternative to a classic item, a die. This idea will make use of the built in accelerometer to detect a dice "roll" and then it will light up a certain (random) number of lights based on the detected motion. Additionally, the user can double tap the device to "roll" the device if they don't wish to shake it.

<img src="img/part_c_sketch_5.png" alt="Sketch 5">

<img src="img/part_c_verplank_5.png" alt="Verplank 5"/>

**\*\*\*What are some things these sketches raise as questions? What do you need to physically prototype to understand how to answer those questions?\*\*\***

The sketches raise a number of questions about the place of interaction, the positioning of the physical prototype, the physical shape and size of the device, and the people involved in the interaction. Additionally, I thought about where the additional wiring / miscellaneous pieces of the project would need to go as well as the reliability of the sensors (detection thresholds). 

For the first idea, the place of interaction would be outside a locked apartment door, the prototype would be positioned on the middle, front part of the door, would be in a circular shape (as small as possible) and the apartment residents would be the people involved. The size of this prototype is the main unknown since I have to figure out how to fit the sensor (with copper conductive tape on the contacts) and a battery case into a small device that is not too heavy so that it can attach to the front of the door. Also it cannot be too large since I don't want the device to physically extrude too far out in front of the door. I would need to physically prototype the enclosure so I can get an idea of the dimensions and how it looks on the door.

The second idea would involve a person studying at a desk in an office or bedroom, where the device is positioned on the desk or lamp base (near a window so it can detect light levels?). The size and shape should be as small as possible and match lamp base shape. For this idea, the positioning will be critical since the light sensor will be highly dependent on exactly where the device is placed. For example, if the device is placed in the center of the room, the light levels might be a bit lower than expected since it is away from the window. Thus, for this idea I would want to prototype the shape and orientation of the device so that I can understand how sensitive the sensor is and define appropriate detection thresholds.

Next, the third idea could be used in a variety of places such as a bedroom, kitchen, car, etc by anyone. In these locations, the device would be positioned in a stable place such as a table, desk, or countertop and would ideally be as small as possible and shaped like a traditional bluetooth speaker device. The main challenge with this idea is understanding if it is intuitive for the user to use the various capacitance sensors (with copper conductive tape) as "buttons", use the actual buttons to increase/decrease volume, and slide switch to pause / play the song. I would need to physically prototype the exterior casing for the device so that each of these areas of the board are easily accessible.

Similarly, the fourth idea can be used in a variety of areas by anyone. In those places, the device is ideally positioned on a table, desk, or countertop and the size would be a bit larger than the minimum space needed. This is because I want a bit more space for the copper conductive tape which is what the user will be interacting with frequently. If I didn't use a good amount of copper conductive tape the area for the interaction would be somewhat narrow, meaning that the user would have to be very precise with the button presses which is not very practical. To summarize, I would need to experiment with the size to figure out what is the optimal size for users to possibly either place the device on a surface or hold in their hand and then interact with the device.

Finally, the last idea involves multiple people playing a board game that requires the use of a die (or dice) on a coffee table. The device would be resting on the table or picked up by the person "rolling" the die. As for shape and size, the die would be shaped like a cube and as small as possible so someone could hold it in their hand. Because there are two separate ways that a user can "roll" the die (shake or double tap), the main thing to prototype is the casing and how that affects the two separate sensor inputs. The main risk for this idea is that a user goes to pick the device up to shake it, but the double tap registers instead causing the device to light up (which indicates the device roll number) earlier than expected.

**\*\*\*Pick one of these designs to prototype.\*\*\***

I chose the first idea, a capacitive lock, to prototype.

### Part D
### Physical considerations for displaying information and housing parts

I was able to run oled_test.py and put the OLED screen inside a small cardboard prototype box that I made for testing purposes. Some pictures of the box that I made **(not for the final design / chosen idea)** are located below.

<img src="img/part_d_oled_box.jpg" alt="OLED Box" width="400"/>
<img src="img/part_d_oled_box2.jpg" alt="OLED Box" width="400"/>


**\*\*\*Sketch 5 designs for how you would physically position your display and any buttons or knobs needed to interact with it.\*\*\***

### Idea 1 Design 1

<img src="img/part_d_design_1.png" alt="Design 1"/>

### Idea 1 Design 2

<img src="img/part_d_design_2.png" alt="Design 2"/>

### Idea 1 Design 3

<img src="img/part_d_design_3.png" alt="Design 3"/>

### Idea 1 Design 4

<img src="img/part_d_design_4.png" alt="Design 4"/>

### Idea 1 Design 5

<img src="img/part_d_design_5.png" alt="Design 5"/>

**\*\*\*What are some things these sketches raise as questions? What do you need to physically prototype to understand how to answer those questions?\*\*\***

From earlier, the biggest open question was size (dimensions) and from doing the sketches I realized that this was indeed a problem but the positioning of the device was equally important. Once again, I considered the place of interaction, the positioning of the physical prototype, the physical shape and size of the device, and the people involved in the interaction. The place and people in the interaction is simply the apartment residents trying to open their apartment door. The size of the device is as small as possible to fit all the electronics (exact dimensions to be determined still) and the variations on shape that I considered were squares / rectangles / circular. Additionally, the positioning and layout of the "buttons" or capacitive pads could vary from a grid-like shape, two columns, or even equidistant around the sensor. Finally, the placement of the device in relation to the door handle was quite important and I considered designs which for example placed it on the top / left / bottom of the handle, as well as other creative designs where the two parts are split above / below the handle or even attached separately to the door. Out of all these questions, the sketches highlighted again that the dimensions would be critical and that the positioning of the device might influence them.

In addition to the existing questions, some new ones were raised. One question was that the weight of the overall device might also influence the layout since the surface area of the device against the door would determine how much weight could be supported. Another question was whether the door handle turning might interfere with the device (especially true if the device was located below). Also, the actual sensor that I am using only has 7 capacitive contacts that I can use to take in the input. This meant that it would not be practical to lay them out like numbers on a traditional electronic keypad (requires 10 contacts for numbers 0-9). The layout also had to be aware of the fact that the "wires" should not overlap, meaning that the capacitive tape lines that connect to the sensor should have a clear path since overlapping wires will cause the sensing to not work.

To answer these questions, I would need to physically prototype the casing. This would help me to answer the question about the dimensions of the device and allow me to place the shell up against a door to see if it looks natural. I could also place all the components into the shell which would help me gauge the weight and decide the best way to attach it to the door. Placing the device up against a door would also help me understand how a user would interact with it and then the door handle since they need to be able to open the door. Finally, for the issue with the "wiring", I can first draw lines with sharpies from the sensor going outward and then place some of the capacitive tape ontop to actually test it out.

**\*\*\*Pick one of these display designs to integrate into your prototype.\*\*\***

I will prototype design 2B.

**\*\*\*Explain the rationale for the design.\*\*\*** (e.g. Does it need to be a certain size or form or need to be able to be seen from a certain distance?)

Design 2B seemed to be the most practical one since there were less uncertainties related to the open questions and it was the easiest to manufacture (circles are hard). Additionally, the design is similar to some of the commercial electronic locks that are on the market (with the exception of the button spacing). The layout of the device is also better than most of the other designs since there is an easier mapping from touch pads to the neopixel LEDs. Finally, the sizing of the device would be reasonable since it could fit everything in the back and also not appear too large on an actual door.

Build a cardboard prototype of your design.

**\*\*\*Document your rough prototype.\*\*\***

### Physical portion of the rough prototype

Pictures of the prototype with and without the capacitive tape is shown below. One minor addition that I had to make was a small notch for the power cable so that the device could be powered. As for dimensions, I used the size of the sensor as a baseline size and added ~1 inch on each side so there was enough room for the capacitive tape. Also for the weight, a few pieces of duct tape were enough to hold the device up against the wall.

<img src="img/part_1_prototype_1_inside.jpg" alt="Prototype 1 Inside" width="800"/>

<img src="img/part_1_prototype_1_unfinished.jpg" alt="Prototype 1 Unfinished" width="400"/>
<img src="img/part_1_prototype_1.jpg" alt="Prototype 1" width="400"/>

<img src="img/part_1_prototype_1_door.jpg" alt="Prototype 1 On Door" width="600"/>


### Code portion of the rough prototype

The Adafruit Circuit Playground Express did not interface with the Raspberry Pi using the Stemma QT connectors, so I had to program the board directly using the Mu Code editor (screenshot below). Additionally, I first tried to program the board with Arduino [(blink example code,](./part1_arduino_testing_scripts/blink/blink.ino) [switches example code)](./part1_arduino_testing_scripts/switches/switches.ino) and then I later realized that I could use [CircuitPython](https://learn.adafruit.com/adafruit-circuit-playground-express/circuitpython-quickstart).

<img src="img/mu_code_editor.png" alt="Mu Code Editor" width="700"/>

To develop the software for the rough prototype, I followed many of the Adafruit [tutorials](https://cdn-learn.adafruit.com/downloads/pdf/adafruit-circuit-playground-express.pdf) (testing code: [1](./AudioFiles/CircuitPython%208.x/code.py), [2](./AudioSine/CircuitPython%208.x/code.py), [3](./CapTouch/CircuitPython%208.x/code.py), [4](./NeoPixel/CircuitPython%208.x/code.py)). The capacitive touch tutorial helped me configure the capacitance sensors and also helped me play around with the sensitivity. The NeoPixel tutorial showed me how to light up the LEDs and make different types of patterns with the lights. The AudioFiles and AudioSine tutorials showed me how to play sound out of the buzzer. I considered using a .wav file to output as sound but during the testing, I found out that the on-board speaker was not as good as I thought so I opted for the buzzer noise (generated by a sine wave). The original sources for these code snippets are here: [1](https://learn.adafruit.com/adafruit-circuit-playground-express/circuitpython-audio-out), [2](https://learn.adafruit.com/adafruit-circuit-playground-express/adafruit2-circuitpython-cap-touch), [3](https://learn.adafruit.com/adafruit-circuit-playground-express/circuitpython-neopixel).

In the process of working with some of the code, I had to manually install many different libraries onto the board, including those from the tutorials, as well as the [official library bundle](https://learn.adafruit.com/adafruit-circuit-playground-express/circuitpython-libraries). I also wanted to do some concurrent tasks but I ran into a bunch of issues with threads and the asyncio library which is [not supported on the Adafruit Circuit Playground Express due to lack of firmware and RAM space](https://learn.adafruit.com/cooperative-multitasking-in-circuitpython-with-asyncio/overview). Being able to use this library would have made a lot of my code much cleaner and more precise since I would have been able to do multiple tasks simultaneously [(asyncio example 1](https://learn.adafruit.com/cooperative-multitasking-in-circuitpython-with-asyncio/concurrent-tasks), [example 2)](https://github.com/adafruit/Adafruit_CircuitPython_asyncio/blob/main/examples/asyncio_displayio_button.py). For example, I could have sensed capacitive input at the same time as lighting up a Neopixel or maybe lit up a Neopixel at the same time as making sound from the buzzer. Instead, I had to use approximations for these operations which was acceptable for the lab. To summarize, the final version of the code for part 1 has capacitive touch sensors, neopixels (light modality), and a buzzer (sound modality). The version 1 code (simple version) is [here](./part1/code_v1.py) and the version 2 code (full version) is [here](./part1/code_v2.py).

### Behind-the-scenes video with the rough prototype

[![Part 1 (D) Behind-the-scenes Rough Prototype](https://img.youtube.com/vi/8IFukSmVqqc/0.jpg)](https://www.youtube.com/watch?v=8IFukSmVqqc)

### Interacting with the rough prototype

A minor note for the video is that the buzzing sound for an unsuccessful unlock attempt is not loud enough for the video to pick it up but the user was able to hear it when testing.

[![Part 1 (D) Interacting with the Rough Prototype](https://img.youtube.com/vi/eQd_Jj52FrU/0.jpg)](https://www.youtube.com/watch?v=eQd_Jj52FrU)


LAB PART 2

### Part 2

Following exploration and reflection from Part 1, complete the "looks like," "works like" and "acts like" prototypes for your design, reiterated below.

### Part E (Optional)
### Servo Control with Joystick

In the class kit, you should be able to find the [Qwiic Servo Controller](https://www.sparkfun.com/products/16773) and [Micro Servo Motor SG51](https://www.adafruit.com/product/2201). The Qwiic Servo Controller will need external power supply to drive, which are included in your kit. Connect the servo controller to the miniPiTFT through qwiic connector and connect the external battery to the 2-Pin JST port (ower port) on the servo controller. Connect your servo to channel 2 on the controller, make sure the brown is connected to GND and orange is connected to PWM.

<img src="Servo_Setup.jpg" width="400"/>

In this exercise, we will be using the nice [ServoKit library](https://learn.adafruit.com/16-channel-pwm-servo-driver/python-circuitpython) developed by Adafruit! We will continue to use the `circuitpython` virtual environment we created. Activate the virtual environment and make sure to install the latest required libraries by running:

```
(circuitpython) pi@ixe00:~/Interactive-Lab-Hub/Lab 4 $ pip3 install -r requirements.txt
```

A servo motor is a rotary actuator or linear actuator that allows for precise control of angular or linear position. The position of a servo motor is set by the width of an electrical pulse, that is, we can use PWM (pulse-width modulation) to set and control the servo motor position. You can read [this](https://learn.adafruit.com/adafruit-arduino-lesson-14-servo-motors/servo-motors) to learn a bit more about how exactly a servo motor works.

Now that you have a basic idea of what a servo motor is, look into the script `qwiic_servo_example.py` we provide. In line 14, you should see that we have set up the min_pulse and max_pulse corresponding to the servo turning 0 - 180 degree. Try running the servo example code now and see what happens:

```
(circuitpython) pi@ixe00:~/Interactive-Lab-Hub/Lab 4 $ python servo_test.py
```

It is also possible to control the servo using the sensors mentioned in as in part A and part B, and/or from some of the buttons or parts included in your kit, the simplest way might be to chain Qwiic buttons to the other end of the Qwiic OLED. Like this:

<p align="center"> <img src="chaining.png"  width="200" ></p>

You can then call whichever control you like rather than setting a fixed value for the servo. For more information on controlling Qwiic devices, Sparkfun has several python examples, such as [this](https://learn.sparkfun.com/tutorials/qwiic-joystick-hookup-guide/all#python-examples).

We encourage you to try using these controls, **while** paying particular attention to how the interaction changes depending on the position of the controls. For example, if you have your servo rotating a screen (or a piece of cardboard) from one position to another, what changes about the interaction if the control is on the same side of the screen, or the opposite side of the screen? Trying and retrying different configurations generally helps reveal what a design choice changes about the interaction -- _make sure to document what you tried_!

### Part F
### Record

Document all the prototypes and iterations you have designed and worked on! Again, deliverables for this lab are writings, sketches, photos, and videos that show what your prototype:
* "Looks like": shows how the device should look, feel, sit, weigh, etc.
* "Works like": shows what the device can do
* "Acts like": shows how a person would interact with the device

