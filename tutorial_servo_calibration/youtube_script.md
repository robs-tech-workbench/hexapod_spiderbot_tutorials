[INTRO]

[ON SCREEN: Preview of the spider robot in action]

Ever seen a spider robot in action?
Well, in this series, we're rolling up our sleeves and crafting our very own!
Using materials that are easy to find, we're crafting a DIY spider robot, and I'm inviting you to join me on this adventure.
Now, a small confession: I'm learning as I go. Some challenges still puzzle me, and the beauty of this series is that we'll tackle them together, step by step. I believe It's the essence of DIY—learning, iterating, and improving.
If you're just tuning in, I suggest starting from the beginning to get the full experience. [ON SCREEN: Link to the playlist]
Throughout this series, I'll break down each part of the project, ensuring you can follow along with ease and maybe even kickstart your own robotic creation.
I aim to keep these sessions short and to the point. However, if anything feels a bit rushed or unclear, don't hesitate to pause or rewind. Additionally, I've provided supplementary documentation and Jupyter notebooks to help reinforce and expand on what I cover. Remember, it's about the journey and understanding, not the pace.
For those curious about the tools, you'll find all the details in the description below. Join me, and let's embark on this exciting DIY voyage together!


[REQUIREMENTS]

Hey everyone! Today, let's talk about why calibrating servos is a must-do:

Consistency: Servos, even of the same model, can behave differently due to manufacturing variations. Calibration ensures they all work uniformly.

Accuracy: For projects needing exact movements, like our spider robot, even a wee error can be a big issue. Calibration ensures each move is spot-on.

Safety and Reliability: Uncalibrated servos can cause unexpected motions, which might damage your project or even pose risks. Calibrating them makes sure they act predictably.

Max Performance: Calibration helps you get the most out of your servo, from its full range of motion to efficient power use.

In short, if you want your servos to work reliably, safely, and at their best, calibration is the key. Stay tuned for our step-by-step guide on how to do it right!

We're taking an important step in this process: adjusting the servos using a servo tester.

[ON SCREEN: List of Requirements]

You need a few things: A servo motor, a servo tester, and a power supply or batteries that work with your servo tester.



[STEPS]



[ON SCREEN: Close-up of the servo, servo tester, and power supply]

Ok, let's start the adjusting process.
The first step is to connect the servo to the servo tester.
The servo has a cable with three wires.
Usually, these wires are red, black, and white or yellow.

The red wire is for power (also known as the VCC).
The black wire is for ground.
The white or yellow wire is for the signal (often marked with an 'S' on the servo tester).
Connect these wires to the matching ports on the servo tester.
The servo tester usually has three sets of pins: 'S' for signal, '+' for power, and '-' for ground.



[ON SCREEN: Close-up of the power supply connection]

After the servo is connected, it's time to turn on the tester.
On your servo tester, you'll usually find separate ports for the power supply, often marked as 'VCC' and 'GND' or '+', '-'.

For the model I'm using, the HJ Digital Servo Tester, the first pins are for connecting the battery or power supply.
Connect the positive wire of your power supply to the '+' pin and the negative wire to the '-' pin.

With everything connected and turned on, we're ready to start the adjusting and testing.
Let's calibrate our servo. 
Set it to the middle, or 0 degrees. 
Then, move it to -90 degrees and note the pulse width. 
Do the same for +90 degrees. Keep in mind, these angles, -90 and +90, are just examples; 
you can choose others based on your needs. 
Remember these pulse widths; they help control the servo accurately in future projects.
The last step is to check the full movement of the servo.



[3D MODEL]



[ON SCREEN: 3D Model]

To make this process easier and more accurate, I've made a 3D model designed for popular servo sizes.
This model includes template angles and a gauge that you can put on the moving outer part of the servo.
You can download and 3D print this model; I've put the link in the description below.



[CONFIGURATION FILE]



[ON SCREEN: Displaying the JSON configuration file]

In our spider robot project, we use a JSON configuration file to store all the important details about the robot's sizes, leg details, controller, and servo settings.
Today, I'm focusing on the servos key.



[ON SCREEN: Zoom in on servos key]

The servos key is a list containing detailed settings for each servo motor used in the robot.
Each servo is identified by its pin number, which matches the physical pin on the controller that it's connected to.



[ON SCREEN: Highlight pin, angle_range, reverse, calibration_data, offset in the JSON]

Let's explain the keys in the servo setting:

angle_range: This is a list that holds the smallest and biggest angles the servo can rotate.
reverse: This true or false value tells if the direction of the servo needs to be reversed.
calibration_data: The calibration_data key usually contains a list of two pairs of matching values.
The first pair is the pulse width values (in microseconds) for the arbitrary, chosen by you positions of the servo.
The second pair is the matching angles (in degrees) that these pulse width values represent.
For example, a servo might have a calibration_data list like this: 

[1000, 2000, -90, 90].
This means that a pulse width of 1000 microseconds matches an angle of -90 degrees, and a pulse width of 2000 microseconds matches an angle of +90 degrees.
offset: This is the difference from the zero position, which can be adjusted to fix for mechanical misalignments.


[ON SCREEN: Highlight the calibration_data in the JSON]

Among these, calibration_data is the most important for our current video.
These values are very important for mapping PWM signals to specific angles, which we'll use later to control the servos accurately.
With these settings, we can control the robot's movements accurately, making sure that each part works together to achieve the wanted behavior.



[RELATIONSHIP]



[ON SCREEN: Displaying the plot of pulse width vs servo angle]

Now, let's understand the relationship between pulse width and servo angle.
I'll use Python to show this relationship.
In a perfect world, this relationship would be a straight line - a constant increase in pulse width would result in a constant rotation of the servo arm.
But in reality, because of mechanical imperfections and other factors, real servos can be different from this perfect behavior.
By plotting the actual response of the servo, we can see how much the servo is different from the expected behavior.



[CONCLUSION]



[ON SCREEN: Channel's Outro Animation or Logo]

That's all for this video on servo adjusting!
I hope you've found it helpful.
Remember, understanding your servo's behavior is key to making your spider robot move smoothly and accurately.
[END]

I hope you found this video helpful! If you did, please give it a thumbs up and consider subscribing if you want to see more like this. Don't hesitate to drop any questions or suggestions in the comments below. I love hearing from you all.

We have many more exciting topics to cover in the upcoming videos, so stay tuned! Until then, keep exploring, and happy robot building!

[ON SCREEN: Outro Animation]
