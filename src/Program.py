import ctypes
import json
import platform

import psutil
import pygame
from src.Utils import Utils
from src.HyperPolygon import HyperPolygon
from src.Camera import Camera
from src.HyperDodecahedronGenerator import HyperDodecahedronGenerator
from typing import Any
from pygame.locals import *

try:
    from pynvml import (nvmlInit, nvmlDeviceGetHandleByIndex, nvmlDeviceGetUtilizationRates, nvmlDeviceGetTemperature,
                        NVML_TEMPERATURE_GPU, nvmlSystemGetDriverVersion, nvmlDeviceGetName)
    nvmlInit()
    gpu_available = True
    gpu_handle = nvmlDeviceGetHandleByIndex(0)
except ImportError:
    gpu_available = False
except Exception as e:
    gpu_available = False
    print(f"An error occurred while trying to get the GPU information: {e}")

pygame.init()


class Program:

    shapes = {
        0: "hyper_cube",
        1: "hyper_tetrahedron",
        2: "hyper_octahedron",
        3: "hyper_dodecahedron"
    }

    shape_names = {
        "hyper_cube": "Hyper Cube",
        "hyper_tetrahedron": "Hyper Tetrahedron",
        "hyper_octahedron": "Hyper Octahedron",
        "hyper_dodecahedron": "Hyper Dodecahedron"
    }

    @staticmethod
    def maximize_window() -> None:
        hwnd = pygame.display.get_wm_info()["window"]
        ctypes.windll.user32.ShowWindow(hwnd, 3)

    @staticmethod
    def run() -> None:
        screen = pygame.display.set_mode((Utils.WIDTH, Utils.HEIGHT), pygame.RESIZABLE, vsync=True)
        pygame.display.set_caption(Utils.APP_NAME)
        pygame.display.set_icon(pygame.image.load(Utils.APP_ICON_PATH))
        clock = pygame.time.Clock()
        font = pygame.font.SysFont("Minecraft Regular", 24)

        HyperDodecahedronGenerator.generate_120cell()

        with open("hyper_shapes.json", "r") as file:
            hyper_shapes = json.load(file)

        selected_shape = hyper_shapes[Program.shapes[0]]
        hyper_polygon = HyperPolygon(selected_shape["vertices"], selected_shape["edges"])

        camera = Camera()
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)

        running = True
        index = 0
        show_info = False
        fullscreen = False
        special = False
        while running:
            screen.fill((0, 0, 0))
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN and event.key == K_r and pygame.event.get_grab():
                    index = (index + 1) % len(Program.shapes)
                    selected_shape = hyper_shapes[Program.shapes[index]]
                    hyper_polygon.set_selected_shape(selected_shape)
                elif event.type == KEYDOWN and event.key == K_x and pygame.event.get_grab():
                    running = False
                elif event.type == KEYDOWN and event.key == K_i and pygame.event.get_grab():
                    show_info = not show_info
                elif event.type == MOUSEBUTTONDOWN and event.button == 3 and not special and pygame.event.get_grab():
                    hyper_polygon.is_4d = not hyper_polygon.is_4d
                elif event.type == MOUSEBUTTONDOWN and event.button == 1 and not pygame.event.get_grab():
                    pygame.event.set_grab(True)
                    pygame.mouse.set_visible(False)
                elif event.type == KEYDOWN and event.key == K_ESCAPE and pygame.event.get_grab():
                    pygame.event.set_grab(False)
                    pygame.mouse.set_visible(True)
                elif event.type == MOUSEMOTION and pygame.event.get_grab():
                    rel_x, rel_y = event.rel
                    camera.look(rel_x, rel_y)
                elif event.type == VIDEORESIZE:
                    if not fullscreen:
                        Utils.WIDTH, Utils.HEIGHT = event.w, event.h
                        screen = pygame.display.set_mode((Utils.WIDTH, Utils.HEIGHT), pygame.RESIZABLE, vsync=True)
                        camera.update_projection_matrix(Utils.WIDTH, Utils.HEIGHT)
                elif event.type == KEYDOWN and event.key == K_f:
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((0, 0),
                                                         pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF,
                                                         vsync=True)

                        Utils.WIDTH, Utils.HEIGHT = 1920, 1080
                    else:
                        screen = pygame.display.set_mode((Utils.WIDTH, Utils.HEIGHT), pygame.RESIZABLE, vsync=True)
                        Program.maximize_window()

                    camera.update_projection_matrix(Utils.WIDTH, Utils.HEIGHT)
                elif event.type == KEYDOWN and event.key == K_g and not hyper_polygon.is_4d and pygame.event.get_grab():
                    special = not special

            camera.move(keys)
            hyper_polygon.update()
            hyper_polygon.draw(screen, camera, special)

            info_texts = [
                f"{int(clock.get_fps())} fps",
                f"Version: {Utils.VERSION}",
                f"Shape: {Program.shape_names[Program.shapes[index]] if hyper_polygon.is_4d else Program.shape_names[Program.shapes[index]].replace("Hyper", "")}",
                f"Dimension: {4 if hyper_polygon.is_4d else 3}",
                f"Special: {'Active' if special else 'Inactive'}"
            ]

            if show_info:
                cpu_name, cpu_usage, cpu_temp, gpu_name, gpu_usage, gpu_temp, gpu_driver = Program.get_system_info()
                info_texts.extend([
                    f"CPU Name: {cpu_name}",
                    f"    Usage: {cpu_usage:.0f}% | Temp: {cpu_temp}ºC" if cpu_temp != "N/A" else f"    Usage: {cpu_usage:.0f}%",
                    f"GPU Name: {gpu_name}" if gpu_available else "GPU: N/A",
                    f"    Usage: {gpu_usage}% | Temp: {gpu_temp}ºC",
                    f"Driver: {gpu_driver}" if gpu_available else "GPU: N/A"
                ])
            elif not show_info and len(info_texts) > 1:
                info_texts = info_texts[:5]

            y_offset = 10
            for text in info_texts:
                text_surface = font.render(text, True, (255, 255, 255))
                screen.blit(text_surface, (Utils.WIDTH - (Utils.WIDTH - 10), y_offset))
                y_offset += 25

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

    @staticmethod
    def get_system_info() -> tuple[str | Any, float, str | Any, str | Any, str | Any, str | Any, str | Any]:
        cpu_usage = psutil.cpu_percent()

        cpu_name = platform.processor()
        cpu_temp = "N/A"
        if hasattr(psutil, "sensors_temperatures"):
            temps = psutil.sensors_temperatures()
            if 'coretemp' in temps and len(temps['coretemp']) > 0:
                cpu_temp = temps['coretemp'][0].current
            else:
                cpu_temp = "N/A"

        if gpu_available:
            gpu_name = nvmlDeviceGetName(gpu_handle).encode()
            gpu_usage = nvmlDeviceGetUtilizationRates(gpu_handle).gpu
            gpu_temp = nvmlDeviceGetTemperature(gpu_handle, NVML_TEMPERATURE_GPU)
            gpu_driver = nvmlSystemGetDriverVersion().encode()
        else:
            gpu_name, gpu_usage, gpu_temp, gpu_driver = "N/A", "N/A", "N/A", "N/A"

        return cpu_name, cpu_usage, cpu_temp, gpu_name, gpu_usage, gpu_temp, gpu_driver

