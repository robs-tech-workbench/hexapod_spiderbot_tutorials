> **Disclaimer:** This tutorial is part of a comprehensive series that I've created to guide you through the process of building a spider robot. Each tutorial in the series is designed to cover a specific aspect of the project, providing detailed instructions and insights to help you understand and replicate the steps.
> 
> You can find the entire series [here](../README.md). I encourage you to explore all the tutorials in the series to gain a complete understanding of the project. Whether you're a beginner or an expert, I hope you find these resources helpful and informative. Happy building!

## Resources

This repository includes a [Jupyter Notebook](forward_kinematics.ipynb) that contains the code and visualizations. 

# Understanding the Forward Kinematics Method in a Spider Robot

Welcome, coding enthusiasts and aspiring roboticists! My goal is to document my journey of building a spider robot in the form of short but detailed tutorials. These tutorials will be easy for everyone to follow, packed with code examples and thorough explanations. Whether you're a seasoned coder or a beginner just starting out, I believe these guides will be a valuable resource in your learning journey. 

Today, in this installment of our exciting series on building a spider robot, we're going to delve into a vital aspect of robot motion planning - the forward kinematics method. Specifically, we'll be exploring the `forwardKinematicsNaive` method in our `SpiderLeg` class.

# Forward Kinematics in Robotics

Forward kinematics is a term in robotics that refers to the calculation of the end effector's position (for instance, a robot arm's or a leg's tip position) given the joint angles. It's essentially about predicting the pose of a robot given its joint parameters.

For a spider-like robot, which could be a quadruped (4-legged) or hexapod (6-legged) robot, forward kinematics would involve determining the position of each of its feet given the angles of its joints. Each leg of the robot is typically a kinematic chain, with joints that allow movements in specific directions.

In practical terms, forward kinematics allows the robot to plan its movements. If the robot's brain decides to move a specific leg to a certain position, it can use inverse kinematics to calculate the necessary joint angles, then move the joints to those angles, and use forward kinematics to check that the leg ended up in the right place.

## Brief Introduction to Trigonometry

Before we dive into the code, let's briefly touch upon some basic trigonometry concepts that are used in this method:

- **Sine (sin)**: In a right-angled triangle, the sine of an angle is the length of the side opposite to that angle divided by the length of the hypotenuse (the longest side, opposite the right angle). This is expressed as: \(\sin(\theta) = \frac{{\text{{opposite}}}}{{\text{{hypotenuse}}}}\).

- **Cosine (cos)**: Similarly, the cosine of an angle in a right-angled triangle is the length of the side adjacent to the angle divided by the length of the hypotenuse. This is expressed as: \(\cos(\theta) = \frac{{\text{{adjacent}}}}{{\text{{hypotenuse}}}}\).

- **Tangent (tan)**: The tangent of an angle is defined as the ratio of the sine to the cosine of that angle, or equivalently, the ratio of the side opposite the angle to the side adjacent to the angle in a right-angled triangle. This is expressed as: \(\tan(\theta) = \frac{{\sin(\theta)}}{{\cos(\theta)}}\).

- **Pythagorean theorem**: In any right-angled triangle, the square of the length of the hypotenuse (the side opposite the right angle) is equal to the sum of the squares of the lengths of the other two sides. This can be written as \(a^2 + b^2 = c^2\), where \(c\) is the length of the hypotenuse, and \(a\) and \(b\) are the lengths of the other two sides.

These concepts allow us to calculate the lengths of sides in a right triangle when an angle is known, or to find an angle when the lengths of the sides are known. They form the basis for many geometric calculations and transformations, including those used in our forward kinematics.

Let's get started!

## The `forwardKinematicsNaive` Method: A Deep Dive

The `forwardKinematicsNaive` method calculates the position of each joint in the robot's leg based on the current angles of the joints. Here's how it works, step by step:

1. `if angles is None:` This line checks whether any joint angles were provided as input to the method. If not, it will use the current angles of the leg.

2. `angles=[(self.theta1),(self.theta2),(self.theta3)]`: Here, the current angles of the leg are fetched from the `SpiderLeg` object and stored in the variable `angles`.

3. `theta1,theta2,theta3=radians(angles[0]),radians(angles[1]),radians(angles[2])`: The angles are then converted from degrees to radians to be used in subsequent calculations. This is because trigonometric functions in Python expect the input in radians.

4. `Xa = self.COXA*cos((theta1))` and `Ya = self.COXA*sin((theta1))`: These lines calculate the x and y coordinates of the joint between the coxa (hip) and femur (thigh) segments of the leg. 

   The `Xa` coordinate is calculated by multiplying the length of the coxa (`self.COXA`) by the cosine of the first joint angle (`theta1`). This gives the horizontal distance from the origin (base of the leg) to the hip joint.
   
   The `Ya` coordinate is calculated by multiplying the length of the coxa (`self.COXA`) by the sine of the first joint angle (`theta1`). This gives the vertical distance from the origin to the hip joint.

5. `G2=sin(theta2)*self.FEMUR`: This line calculates the vertical component of the length of the femur segment. It's obtained by multiplying the length of the femur (`self.FEMUR`) by the sine of the second joint angle (`theta2`).

6. `P1=cos(theta2)*self.FEMUR`: Here, `P1` is the horizontal component of the length of the femur segment. It's calculated by multiplying the length of the femur (`self.FEMUR`) by the cosine of the second joint angle (`theta2`).

7. `Xc=cos(theta1)*P1` and `Yc=sin(theta1)*P1`: These lines calculate the x and y coordinates of the femur-tibia joint (or "knee" of the spider leg). The x and y coordinates are calculated by multiplying `P1` (the horizontal component of the femur length) by the cosine and sine of the first joint angle (`theta1`), respectively.

The next set of lines calculate the x, y, and z coordinates for the tibia-tip joint. The calculations involve more trigonometry and geometry, similar to the previous steps.

The final output of the method is a list of joint locations, with each location represented by a list of x, y, and z coordinates.

In the next tutorial, we will delve into how we can use this forward kinematics method for motion planning and control in our spider robot. Stay tuned!

Remember, the beauty of robotics lies not just in the final product, but in the intricate processes that bring the robot to life. Happy coding!