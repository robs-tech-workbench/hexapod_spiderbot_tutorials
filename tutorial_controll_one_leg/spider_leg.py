from math import degrees, radians, cos, sin, sqrt, acos, atan,asin
import numpy as np

class SpiderLeg:
    def __init__(self, name, COXA, FEMUR, TIBIA):
        self.name = name
        self.COXA = COXA
        self.FEMUR = FEMUR
        self.TIBIA = TIBIA
        self.theta1 = 0.
        self.theta2 = 0.
        self.theta3 = 0.

        # Forward kinematics calculates the target position (x, y, z) based on the joint angles
        self.joints = self.forwardKinematics()

    def setAngles(self, angles):
        """
        Set the joint angles for the leg.
        
        Args:
            angles (list): A list of three angles in degrees, corresponding to theta1, theta2, and theta3.
            
        Returns:
            list: The updated joint angles.
        """
        angles = self.normalizeAngles(angles)
        self.theta1, self.theta2, self.theta3 = angles
        return self.getAngles()

    def getAngles(self):
        """
        Get the current joint angles.
        
        Returns:
            list: A list containing the current joint angles (theta1, theta2, theta3) in degrees.
        """
        return [self.theta1, self.theta2, self.theta3]

    def normalizeAngles(self, angles):
        """
        Normalize joint angles to be in the range [-180, 180] degrees.
        
        Args:
            angles (list): A list of joint angles in degrees.
            
        Returns:
            list: A list of normalized joint angles in degrees.
        """
        for idx, ang in enumerate(angles):
            sign = 1
            if ang < 0:
                sign = -1
            angles[idx] = sign * (abs(ang) % 360)
            if abs(ang) > 180:
                angles[idx] = ang - (360 * sign)
        return angles

    def getTarget(self):
        """
        Get the target position of the leg tip.
        
        Returns:
            list: A list containing the x, y, and z coordinates of the leg tip.
        """
        return self.joints[3]

        # Calculate the joint angles required to reach a target position using inverse kinematics
    def inverseKinematics(self, target=None):
        if target is None:
            target = self.joints[3]
        x, y, z = target[0], target[1], target[2]

        # Calculate theta1 using arctangent (tan^-1) based on x and y coordinates
        # arctan(y/x) gives the angle of a right-angled triangle with legs x and y
        theta1 = atan(y / x)

        # Calculate intermediate values for theta2 and theta3
        # Here, we apply trigonometric rules to find the lengths of the sides of the triangles
        # We use the cosine and sine functions to find the lengths Xa and Ya
        Xa = self.COXA * cos((theta1))
        Ya = self.COXA * sin((theta1))

        Xb = x - Xa
        Yb = y - Ya

        # Divide Xb by cos(theta1) to find P (projection of Xb on the x-axis)
        P = Xb / cos(theta1)

        # Calculate the absolute value of z, which will be used in the calculation of H
        G = abs(z)

        # Use Pythagorean theorem to find the length H (the hypotenuse of a right-angled triangle with legs P and G)
        H = sqrt(P ** 2 + G ** 2)

        # Calculate the angle phi3 using arcsine (sin^-1) based on G and H
        # arcsin(G/H) gives the angle of a right-angled triangle with legs G and H
        phi3 = asin(G / H)

        # Apply the cosine rule to find the angle phi2
        # Cosine rule: (c^2 = a^2 + b^2 - 2ab * cos(C))
        # We rearrange the formula to find the cosine of angle C:
        # cos(C) = (a^2 + b^2 - c^2) / (2ab)
        # In our case, a = self.TIBIA, b = H, c = self.FEMUR
        phi2Acos = ((self.TIBIA ** 2) + (H ** 2) - (self.FEMUR ** 2)) / (2 * self.TIBIA * H)
        phi2 = acos(phi2Acos)

        # Apply the cosine rule again to find the angle phi1
        # In this case, a = self.FEMUR, b = H, c = self.TIBIA
        phi1 = acos((self.FEMUR ** 2 + H ** 2 - self.TIBIA ** 2) / (2 * self.FEMUR * H))

        # Calculate theta2 and theta3 based on phi values and the sign of z
        # If z is positive, theta2 = phi1 + phi3; otherwise, theta2 = phi1 - phi3
        if z > 0:
            theta2 = phi1 + phi3
        else:
            theta2 = phi1 - phi3

        # Calculate theta3 as the sum of phi1 and phi2
        theta3 = phi1 + phi2

        # Update joint angles and forward kinematics with the new angles
        ang = [degrees(theta1), degrees(theta2), degrees(theta3)]
        self.setAngles(ang)
        self.forwardKinematics()
        return ang


    # Calculate the joint positions (x, y, z) based on the given joint angles using forward kinematics
    def forwardKinematics(self, angles=None):
        if angles is None:
            angles = [radians(self.theta1), radians(self.theta2), radians(self.theta3)]
        theta1, theta2, theta3 = angles

        # Calculate the positions of each joint based on the given angles
        Xa = self.COXA * cos((theta1))
        Ya = self.COXA * sin((theta1))
        G2 = sin(theta2) * self.FEMUR
        P1 = cos(theta2) * self.FEMUR
        Xc = cos(theta1) * P1
        Yc = sin(theta1) * P1

        # Calculate the position of the tip of the leg (end effector)
        H = sqrt(self.TIBIA ** 2 + self.FEMUR ** 2 - (2 * self.TIBIA * self.FEMUR * cos(radians(180) - theta3)))
        phi1 = acos((self.FEMUR ** 2 + H ** 2 - self.TIBIA ** 2) / (2 * self.FEMUR * H))
        phi2 = radians(180) - (radians(180) - theta3) - phi1
        phi3 = (phi1 - theta2)
        Pp = cos(phi3) * H
        P2 = Pp - P1
        Yb = sin(theta1) * Pp
        Xb = cos(theta1) * Pp
        G1 = sin(phi3) * H
        G1 = -G1

        # Store the joint positions in a list
        jointLocation = [
            [0, 0, 0],  # start joint
            [Xa, Ya, 0],  # coxa-femur joint
            [Xa + Xc, Ya + Yc, G2],  # femur-tibia joint
            [Xa + Xb, Ya + Yb, G1]  # tip of the leg
        ]

        self.joints = jointLocation
        return jointLocation
