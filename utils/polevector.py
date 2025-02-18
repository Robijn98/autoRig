import maya.cmds as cmds
import math
import numpy as np


class poleVector:

    def __init__(self, shoulderJnt, elbowJnt, wristJnt):
        print("Initializing polevector")
        self.shoulderJnt = shoulderJnt
        self.elbowJnt = elbowJnt
        self.wristJnt = wristJnt

    def calculate_vector(self, A, B):
        if len(A) != len(B):
            raise ValueError("Points must have the same dimensionality")

        vector = [B[i] - A[i] for i in range(len(A))]
        return vector

    def project_vector_onto_direction(self, A, B, C):
        A = np.array(A)
        B = np.array(B)
        C = np.array(C)

        AC = C - A
        AB = B - A

        dot_product = np.dot(AB, AC)
        magnitude_squared = np.dot(AC, AC)

        scalar_projection = dot_product / magnitude_squared
        vector_projection = scalar_projection * AC

        projected_point = A + vector_projection

        return projected_point

    def find_polevector(self, scalar=3):
        print("Finding polevector")        
        A = cmds.xform(self.shoulderJnt, q=True, t=True, ws=True)
        B = cmds.xform(self.elbowJnt, q=True, t=True, ws=True)
        C = cmds.xform(self.wristJnt, q=True, t=True, ws=True)

        D = self.project_vector_onto_direction(A,B,C)
        vector_DB = self.calculate_vector(D, B)
        new_vec = []

        for point in range(3):
            new_point = vector_DB[point] * scalar
            new_vec.append(new_point)

        E = []

        for point in range(3):
            new_point = D[point] + new_vec[point]
            E.append(new_point)

        return E



