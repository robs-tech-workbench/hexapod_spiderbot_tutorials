# Servo Calibration with a Servo Tester

This tutorial guides you through the process of calibrating a servo using a servo tester. 

## Requirements

1. A servo motor
2. A servo tester
3. A power supply or batteries appropriate for your servo tester
4. A 3D model for precise calibration (optional)


## Resources

This repository includes a [Jupyter Notebook](servo_calibration.ipynb) that contains the code and visualizations. 

### 3D Model for Precise Calibration

To make the calibration process easier and more precise, I have prepared a 3D model specifically designed for popular servo sizes. This model includes template angles at -90, -45, 0, 45, and 90 degrees, as well as a gauge that you can place on the moving outer shaft of the servo.

By lining up the gauge with the template angles, you can get exact pulse width readings for those specific angles. This not only simplifies the process but also ensures that you achieve an accurate and consistent calibration across different servos. You can download and 3D print this model [here](LINK_TO_3D_MODEL).

## Steps

1. **Connect Servo to Servo Tester:** Plug the servo connector into the servo tester. The order usually is Signal-Positive-Negative (orange-red-black or yellow-red-brown).

2. **Power up the Servo Tester:** Connect your power supply or battery to the servo tester. Ensure you use the right voltage and current rating for your servo.

3. **Calibration and Testing:**
   - **Neutral Position:** Set the pulse width to 1500 μs (or any value suggested by the manufacturer) using the tester. This should move the servo to the 0 degree position.
   - **Negative and Positive 90 Degrees:** Slowly decrease the pulse width from 1500 μs until the servo moves to what you want to consider as -90 degrees. Note down the pulse width at this point. Then, increase the pulse width from 1500 μs until the servo reaches +90 degrees and note down the pulse width.
   - **Full Range:** By alternating the pulse width from minimum (for -90 degrees) to maximum (for +90 degrees), you can see the full range of motion of the servo. 

## Important: Relationship between pulse width and servo angle

For visualizing the relationship between pulse width and servo angle, a Python script can be found [in this Jupyter notebook](servo_calibration.ipynb).

The notebook will plot the measured pulse widths (x-axis) and corresponding angles (y-axis). The plot will have two lines:

- The blue line represents the actual measured positions.
- The gray dashed line represents an approximation.

A "linear approximation" is a simplified representation of data that assumes the relationship between two variables can be represented by a straight line. The concept comes from the field of mathematics, where it's often useful to approximate complex functions with simpler ones.

In the context of a servo motor, we often assume the relationship between pulse width (input) and the angle of the servo arm (output) is linear. This means we expect the servo arm to move at a constant rate as we increase the pulse width. For example, if increasing the pulse width by 100 µs causes the servo arm to move by 10 degrees, we expect that increasing the pulse width by 200 µs will move the servo arm by 20 degrees, and so on.

However, this relationship isn't always perfectly linear in real servos. Mechanical imperfections, non-linear electronics, or other factors may cause the servo to deviate from the expected linear behavior. That's why it's helpful to measure the actual response of the servo and compare it to the linear "perfect" approximation.

Here's what's being plotted in the previous code:
![Alt text](media/image.png)

The pulse_widths and angles lists represent the actual measured response of the servo. The plt.plot(pulse_widths, angles, marker='o') line plots these values as blue dots on the graph.

The pulse_width_range and angle_range lists represent the expected linear response of the servo, based on the assumption that the servo moves 90 degrees when the pulse width changes by 400 µs. The plt.plot(pulse_width_range, angle_range, '--', color='gray') line plots this expected response as a dashed gray line on the graph.

By comparing the actual response to the expected linear response, you can see how much your servo deviates from the expected behavior. If the blue dots fall on the gray line, your servo behaves exactly as expected. If the blue dots deviate from the gray line, it means your servo doesn't move at a constant rate, and you might need to take this into account in your project.
