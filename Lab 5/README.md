# Observant Systems

**NAMES OF COLLABORATORS HERE** Rahul Jain

For lab this week, we focus on creating interactive systems that can detect and respond to events or stimuli in the environment of the Pi, like the Boat Detector we mentioned in lecture. 
Your **observant device** could, for example, count items, find objects, recognize an event or continuously monitor a room.

This lab will help you think through the design of observant systems, particularly corner cases that the algorithms need to be aware of.

## Prep

1. Spend about 10 Minutes doing the Listening exercise as described in [ListeningExercise.md](https://github.com/FAR-Lab/Interactive-Lab-Hub/blob/Fall2022/Lab%205/ListeningExercise.md)
2.  Install VNC on your laptop if you have not yet done so. This lab will actually require you to run script on your Pi through VNC so that you can see the video stream. Please refer to the [prep for Lab 2](https://github.com/FAR-Lab/Interactive-Lab-Hub/blob/Fall2022/Lab%202/prep.md), we offered the instruction at the bottom.
3.  Read about [OpenCV](https://opencv.org/about/), [MediaPipe](https://mediapipe.dev/), and [TeachableMachines](https://teachablemachine.withgoogle.com/).
4.  Read Belloti, et al.'s [Making Sense of Sensing Systems: Five Questions for Designers and Researchers](https://www.cc.gatech.edu/~keith/pubs/chi2002-sensing.pdf).

### For the lab, you will need:
1. Pull the new Github Repo.(Please wait until thursday morning. There are still some incompatabilities to make the assignment work.)
1. Raspberry Pi
1. Webcam 

### Deliverables for this lab are:
1. Show pictures, videos of the "sense-making" algorithms you tried.
1. Show the filledout answers for the Contextual Interaction Design Tool.
1. Show a video of how you embed one of these algorithms into your observant system.
1. Test, characterize your interactive device. Show faults in the detection and how the system handled it.

## Overview
Building upon the paper-airplane metaphor (we're understanding the material of machine learning for design), here are the four sections of the lab activity:

A) [Play](#part-a)

B) [Fold](#part-b)

C) [Flight test](#part-c)

D) [Reflect](#part-d)

---
### Lab Prep

I did the listening exercise and the results are [here](./ListeningExercise.md).

### Part A
### Play with different sense-making algorithms.

#### OpenCV

**\*\*\*Try each of the following four examples in the `openCV-examples`, include screenshots of your use and write about one design for each example that might work based on the individual benefits to each algorithm.\*\*\***

### Contour Detection

I was able to run the contour detection script on the Queensboro Bridge and it seemed to pick up many of the contours. It wasn't perfect but did a decent job. In general, contour detection is useful for identifying the boundaries of different shapes. One design that contour detection could be used for is separating coins from dollar bills. The coins would have a circular shape while dollar bills would be rectangles (or squares if folded).

<img src="img/contours_test.png" alt="Contours" width="400"/>

### Face Detection

I was able to run the face detection script on myself and it seemed to pick up my face and also thought I had multiple eyes (green boxes). In general face detection can be applied to many use cases where one wants to check whether a person is present or not. One design that face detection could be used for is a smart security system where it would notify the homeowner when a face was detected so they could make a decision whether or not to let them in.

<img src="img/face_detection_test.png" alt="Face Detection" width="400"/>

### Optical Flow 

I was able to run the optical flow test where it traced different points as I moved around the screen. In general this is good for figuring out how objects are moving in a space and tracking them. One design that this could be used for is a movie/video stabilization device which tries to reorient the camera position based on how something in the shot is moving / shaking. So for example if the person holding the camera is running, the image might be shaky so this could help stabilize the image. Another example could be detecting traffic flow.

<img src="img/optical_flow_test.png" alt="Optical Flow" width="400"/>

### Object Detection

I was able to run the object detection test where it drew a bounding box around my computer mouse. In general this is good for figuring out what and how many of different objects appear in the image. One design that this could be used for is identifying how busy a particular parking lot is. For example, if there are a lot of cars parked then we know that it is fairly busy.

<img src="img/detected_test.png" alt="Object Detection" width="400"/>

#### Filtering, FFTs, and Time Series data. 

**1. Set up threshold detection** Can you identify when a signal goes above certain fixed values?

Yes. I was able to set a threshold on the volume to print a line whenever it was above 85 (which I found from being silent in the room). Thus whenever I spoke, the volume would increase and the threshold would be hit.

```
# Threshold Detection
if volume > 85:
    print("The volume is greater than 85:", volume)
```

**2. Set up a running averaging** Can you set up a running average over one of the variables that are being calculated.[moving average](https://en.wikipedia.org/wiki/Moving_average)

Yes. I was able to print out the running average of the volume. This is simply the sum of the volumes / number of volume points.

```
# Running Average
if len(VolumeHistory) != 0:
    print("The volume running average is", np.sum(VolumeHistory) / len(VolumeHistory))
```

**3. Set up peak detection** Can you identify when your signal reaches a peak and then goes down?

Yes. I was able to print out a line whenever a peak occured in the volume. I simply looked at three points and if the center measurement was higher than both the left and right by some threshold, I considered it to be a peak. There are probably more advanced ways to do this, but this simple approximation seems to work fine.

```
# Peak Detection
if len(VolumeHistory) > 2:
    peak_threshold = 5
    if (VolumeHistory[-3] - VolumeHistory[-2] < -peak_threshold) and (VolumeHistory[-2] - VolumeHistory[-1] > peak_threshold):
        print("Peak detected!")
```

**\*\*\*Include links to your code here, and put the code for these in your repo--they will come in handy later.\*\*\***

The code for these tests is located [here](./ExampleAudioFFT.py) and a short video is below.

[![Part 1 (A) Filtering, FFTs, and Time Series Data Test](https://img.youtube.com/vi/r0I9Pp5WC_s/0.jpg)](https://www.youtube.com/watch?v=r0I9Pp5WC_s)

### (Optional Reading) Introducing Additional Concepts

I ended up bricking my Pi's SD card... so I decided to install the old RPi image which I found [here](https://github.com/FAR-Lab/Interactive-Lab-Hub/blob/Spring2021/Lab%202/prep.md).

<img src="img/bricked_pi.jpg" alt="Bricked Pi" width="400"/>

#### MediaPipe

I was able to run the [MediaPipe](https://mediapipe.dev/) test (screenshot and video below).

<img src="img/mediapipe_test.png" alt="MediaPipe Test" width="400"/>

[![Part 1 (A) MediaPipe Test](https://img.youtube.com/vi/vpBuVtDPl2I/0.jpg)](https://www.youtube.com/watch?v=vpBuVtDPl2I)

**\*\*\*Consider how you might use this position based approach to create an interaction, and write how you might use it on either face, hand or body pose tracking.\*\*\***

One idea is to make a rock paper scissors game using hand tracking. Using 2 camera inputs, I could possibly run the mediapipe script to detect which hand shape the players are making and output a decision.

#### Teachable Machines

I was able to run the [TeachableMachines](https://teachablemachine.withgoogle.com) test (video below)

[![Part 1 (A) Teachable Machines Test](https://img.youtube.com/vi/gvn3inwG-9E/0.jpg)](https://www.youtube.com/watch?v=gvn3inwG-9E)

**\*\*\*Whether you make your own model or not, include screenshots of your use of Teachable Machines, and write how you might use this to create your own classifier. Include what different affordances this method brings, compared to the OpenCV or MediaPipe options.\*\*\***

The teachable machines modeling allows for image recognition of arbitrary items based on previous items. OpenCV tries to use things like contour detection, face detection, flow detection, and object detection to identify whether things appear in the camera image but it cannot easily tell you what those things are. Similarly, MediaPipe enables face, face mesh, hand pose, and body pose detection but again can't really identify the difference between two faces for example because it is looking at the structure.

### Part B
### Construct a simple interaction.

* Pick one of the models you have tried, and experiment with prototyping an interaction.
* This can be as simple as the boat detector showen in a previous lecture from Nikolas Matelaro.
* Try out different interaction outputs and inputs.
* Fill out the ``Contextual Interaction Design Tool`` sheet.[Found here.](ThinkingThroughContextandInteraction.png)

**\*\*\*Describe and detail the interaction, as well as your experimentation here.\*\*\***

Before I decided on my interaction, I did some experimentation on recognizing different poker chips to see if the TeachableMachines classification would work (which it did). The keras file for the TeachableMachines classifier is [here](./models/blue_versus_red_keras.zip).

<img src="img/blue_vs_red.png" alt="Blue Versus Red"/>

### Wizard of Odds

The model that I picked was the TeachableMachines classification. The interaction that I chose was a group of people playing the card game blackjack. The goal for the interaction is to have a device (called the Wizard of Odds) calculate recommended actions based on what cards the player has and what card the dealer is showing. The TeachableMachines classifier will automatically recognize the number that each card represents and will learn to recognize them regardless of suite. Also, the device should signal the player with a recommended action through an LED strip or voice output. The Contextual Interaction Design Tool sheet is filled out below.

<img src="img/part_b_tool.png" alt="Contextual Interaction Design Tool"/>

<img src="img/part_b_storyboard.png" alt="Storyboard"/>

<img src="img/part_b_verplank.png" alt="Verplank Diagram"/>

### Part C
### Test the interaction prototype

Now flight test your interactive prototype and **note down your observations**:
For example:
1. When does it do what it is supposed to do?
1. When does it fail?
1. When it fails, why does it fail?
1. Based on the behavior you have seen, what other scenarios could cause problems?

**\*\*\*Think about someone using the system. Describe how you think this will work.\*\*\***
1. Are they aware of the uncertainties in the system?
1. How bad would they be impacted by a miss classification?
1. How could change your interactive system to address this?
1. Are there optimizations you can try to do on your sense-making algorithm.

For the first test, I tried to do a two versus ten classifier. When I was capturing image samples, I rotated the cards so that it would be able to understand different orientations and capture that in the model. I also used all 4 variations of 2's and 4 variations of 10's. I didn't however include a background class which would be helpful for the future. A short video is below. The keras file for the TeachableMachines classifier is [here](./models/two_versus_ten_keras.zip) and tensorflowlite version is [here](./models/two_versus_ten_tflite.zip). I exported the tensorflowlite version as well because I saw [here](https://www.tensorflow.org/lite/guide/python) that it might be possible to run it that way on the Raspberry Pi as well.

<img src="img/two_versus_ten.png" alt="Two versus ten"/>

[![Part 1 (C) Two versus Ten Classifier](https://img.youtube.com/vi/HZEc9LwuTio/0.jpg)](https://www.youtube.com/watch?v=HZEc9LwuTio)

This test was incredibly successful and whenever I held up a card it would be able to classify it correctly. It would fail sometimes if I held up both the two and ten in the same image or if I didn't have any card in the image. These failures are due to the fact that there is no class for both of the cards and also no class for no cards. Other scenarios that can occur are identifying whose card is being classified at that point in time. To handle the uncertainty around identification of whose card is being classified, I will have the player assume that they should input the dealer's card into the system first and then their cards. Also, I will have the player press a button to manually capture the card that they want to process into the system. If there was a misclassification, it is not a big deal because they can just hit the reset button and scan the cards into the system again. There is no need to change the system further because I have handled these cases. Some additional optimizations could be to play around with the rotation of the card to see how the number of training examples impacts the model accuracy and also the overall model size. For example, since the card is likely symmetric, I don't necessarily need to have both the 0 degrees and 180 degrees training images. Also, I realized later that in Blackjack the 10, Jack, Queen, and King all have the same numerical value of 10, so I could potentially try to condense them down into one class.

Overall, the use of the Wizard of Odds device will work as follows. The dealer will hand out two cards to the player and show one of the dealer's cards to the player. The player will scan the dealer's card first and then scan their cards. Note that to scan a card, the player points the camera part of the device at the card (one at a time) and then presses a button. Once the three cards are scanned, the Wizard of Odds device will do a calculation and then recommend an action by lighting up a light on the LED panel. If further cards are dealt to the player in the same hand, the player can scan those additional cards in and the recommendation will update. Once the interaction is complete, the player can reset the count by pressing the other button and repeat the process.

### Part D
### Characterize your own Observant system

Now that you have experimented with one or more of these sense-making systems **characterize their behavior**.
During the lecture, we mentioned questions to help characterize a material:
* What can you use X for?
* What is a good environment for X?
* What is a bad environment for X?
* When will X break?
* When it breaks how will X break?
* What are other properties/behaviors of X?
* How does X feel?

**\*\*\*Include a short video demonstrating the answers to these questions.\*\*\***

For this part, I tried to make a more complicated classifier with all the classes (13 + 1 background class). This can be used for detecting the number of each card (note that the suite does not matter and makes the classification simpler). A good environment for this classification is anywhere with normal light levels as low light levels would make it hard for the camera to pick up on the features of the image and classify it properly. The classification might break if the player mistakenly scans two or more cards. If that happens, it might show an incorrect sum since the wrong number would be input to the system. In the complex classifier, I will include an empty background class to account for the no cards case. Another thing to consider is the distance with which to hold the device from the card surface. If it is two close, the classifier may not be able to pick up and scan the entire card in. Finally, the entire device should not feel too clunky and should be easy to hold in one's hands. I also drew a more detailed diagram (first draft sketch) about how the Wizard of Odds device will look and feel like (below). A short video that shows how the classifier works is shown below as well. The classifier seemed to work pretty well for most of the numbers. It had some trouble with the ace and five and a few of the face cards were mistaken for other face cards (totally ok!). For the final classifier, I can also try to increase the number of epochs. The keras file for the TeachableMachines classifier is [here](./models/card_numbers_keras.zip). I also ran one for 150 epochs, and that classifier is [here](./models//card_numbers_150_keras.zip). The raw samples are [here](./samples/).

<img src="img/part_d_design.png" alt="Device Design"/>

<img src="img/training_complex.png" alt="Training Complex"/>

[![Part 1 (D) Card Numbers Classifier](https://img.youtube.com/vi/BdQmkDdYr3k/0.jpg)](https://www.youtube.com/watch?v=BdQmkDdYr3k)

I was also able to run the classifier on the Raspberry Pi!

<img src="img/card_numbers.png" alt="Card Numbers"/>


### Part 2.

Following exploration and reflection from Part 1, finish building your interactive system, and demonstrate it in use with a video.

**\*\*\*Include a short video demonstrating the finished result.\*\*\***
