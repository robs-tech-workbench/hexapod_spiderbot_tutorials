Read the companion tutorial on [Catch IT](https://catchit.pl/): [Controlling One Hexapod Leg](https://catchit.pl/blog/controlling-one-hexapod-leg/).

> **Disclaimer:** This tutorial is part of a comprehensive series that I've created to guide you through the process of building a spider robot. Each tutorial in the series is designed to cover a specific aspect of the project, providing detailed instructions and insights to help you understand and replicate the steps.
> 
> You can find the entire series [here](../README.md). I encourage you to explore all the tutorials in the series to gain a complete understanding of the project. Whether you're a beginner or an expert, I hope you find these resources helpful and informative. Happy building!

# Controlling One Hexapod Leg

This tutorial covers the basics of programming the hexapod: the `SpiderLeg` class with forward and inverse kinematics, simulation and visualization of a single leg, and mapping joint angles to servo pulse widths on the real hardware.

## Resources

- [`spider_leg.py`](spider_leg.py) — the `SpiderLeg` class implementing forward and inverse kinematics for a three-joint leg (coxa, femur, tibia).
- [`one_leg_controll.ipynb`](one_leg_controll.ipynb) — Jupyter notebook that simulates the leg, moves the tip through a set of positions, and projects paths onto the plane defined by those positions.
- [`image_processing.ipynb`](image_processing.ipynb) — image processing helper notebook (OpenCV): it turns a drawing ([`rip.jpg`](rip.jpg)) into paths that can be projected onto the leg's working plane.
- [`hardware_controller.py`](hardware_controller.py) — the `Servo`, `HardwareController`, and `ChicaController` classes for converting joint angles to servo pulse widths and communicating with the servo controller over serial.

The servo configuration file used by `HardwareController` is described in the [Servo Calibration](../tutorial_servo_calibration/README.md) tutorial.
