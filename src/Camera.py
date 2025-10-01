# This file contains the Camera class, which is used to move the camera around the 3D world.

import math
import pygame
from pygame.locals import *


class Camera:
    def __init__(self):
        self.projection_matrix = None
        self.x, self.y, self.z = 0, 0, -5
        self.yaw, self.pitch, self.roll = 0, 0, 0
        self.speed = 0.1
        self.sensitivity = 0.002

    def move(self, keys, grab):
        direction_x = math.sin(self.yaw)
        direction_z = math.cos(self.yaw)

        if not grab:
            return

        if keys[K_w]:
            self.x += direction_x * self.speed
            self.z += direction_z * self.speed
        if keys[K_s]:
            self.x -= direction_x * self.speed
            self.z -= direction_z * self.speed
        if keys[K_a]:
            self.x -= direction_z * self.speed
            self.z += direction_x * self.speed
        if keys[K_d]:
            self.x += direction_z * self.speed
            self.z -= direction_x * self.speed
        if keys[K_SPACE]:
            self.y += self.speed
        if keys[K_LSHIFT]:
            self.y -= self.speed
        if keys[K_q]:
            self.roll += self.speed
        if keys[K_e]:
            self.roll -= self.speed

    def look(self, rel_x, rel_y):
        self.yaw += rel_x * self.sensitivity
        self.pitch -= rel_y * self.sensitivity
        self.pitch = max(-math.pi / 2, min(math.pi / 2, self.pitch))

    def update_projection_matrix(self, width, height):
        self.projection_matrix = pygame.transform.scale(
            pygame.Surface((width, height)), (width, height)
        )
