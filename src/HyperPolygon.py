import math
import random
import pygame
from src.Utils import Utils


class HyperPolygon:
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges
        self.angleX = 0
        self.angleY = 0
        self.angleZW = 0
        self.is_4d = False
        self.w_factor = 0.0
        self.color = [random.randint(0, 255) for _ in range(3)]
        self.color_direction = [1, 1, 1]

    def set_selected_shape(self, selected_shape):
        self.vertices = selected_shape["vertices"]
        self.edges = selected_shape["edges"]

    def rotateX(self, point, angle):
        x, y, z, w = point
        cosA, sinA = math.cos(angle), math.sin(angle)
        return x, y * cosA - z * sinA, y * sinA + z * cosA, w

    def rotateY(self, point, angle):
        x, y, z, w = point
        cosA, sinA = math.cos(angle), math.sin(angle)
        return x * cosA + z * sinA, y, -x * sinA + z * cosA, w

    def rotateZW(self, point, angle):
        x, y, z, w = point
        cosA, sinA = math.cos(angle), math.sin(angle)
        return x, y, z * cosA - w * sinA, z * sinA + w * cosA

    def rotateW(self, point, w_factor):
        x, y, z, w = point
        scale = 1 / (2 - w * w_factor) if self.is_4d else 1
        return x * scale, y * scale, z * scale

    def project(self, point, camera):
        scale = 300
        x, y, z = point

        x -= camera.x
        y -= camera.y
        z -= camera.z

        temp_x = x * math.cos(camera.yaw) - z * math.sin(camera.yaw)
        temp_z = x * math.sin(camera.yaw) + z * math.cos(camera.yaw)
        temp_y = y * math.cos(camera.pitch) - temp_z * math.sin(camera.pitch)
        temp_z = y * math.sin(camera.pitch) + temp_z * math.cos(camera.pitch)

        if temp_z <= 0.1:
            temp_z = 0.1

        return int(Utils.WIDTH / 2 + temp_x * scale / temp_z), int(Utils.HEIGHT / 2 - temp_y * scale / temp_z)

    def project_to_sphere(self, point):
        if len(point) == 4:
            x, y, z, w = point
            r = math.sqrt(x ** 2 + y ** 2 + z ** 2 + w ** 2)
        elif len(point) == 3:
            x, y, z = point
            r = math.sqrt(x ** 2 + y ** 2 + z ** 2)
        else:
            return 0, 0, 0

        if r != 0:
            return x / r, y / r, z / r
        return 0, 0, 0

    def update(self):
        self.angleX += 0.02
        self.angleY += 0.03
        if self.is_4d:
            self.angleZW += 0.03
            self.w_factor = min(self.w_factor + 0.02, 1)
        else:
            self.angleZW = 0
            self.w_factor = max(self.w_factor - 0.02, 0)

        for i in range(3):
            self.color[i] += self.color_direction[i] * 2
            if self.color[i] >= 255 or self.color[i] <= 0:
                self.color_direction[i] *= -1
                self.color[i] = max(0, min(255, self.color[i]))

    def draw(self, screen, camera, special):
        transformed_vertices = [
            self.rotateW(
                self.rotateZW(
                    self.rotateX(
                        self.rotateY(v, self.angleY), self.angleX
                    ), self.angleZW
                ), self.w_factor
            )
            for v in self.vertices
        ]

        color = tuple(self.color)
        for edge in self.edges:
            if special:
                # Aqui não aplicamos as rotações porque o ponto já foi projetado para 3D
                p1 = self.project_to_sphere(transformed_vertices[edge[0]])
                p2 = self.project_to_sphere(transformed_vertices[edge[1]])
                # Projeção para a tela 2D usando a função project
                pygame.draw.line(screen, color, self.project(p1, camera), self.project(p2, camera), 2)
            else:
                p1 = self.project(transformed_vertices[edge[0]], camera)
                p2 = self.project(transformed_vertices[edge[1]], camera)
                pygame.draw.line(screen, color, p1, p2, 2)

