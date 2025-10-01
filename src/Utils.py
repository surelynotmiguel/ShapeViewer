# This file contains the Utils class, which contains some constants that are used throughout the application.

import ctypes

user32 = ctypes.windll.user32


class Utils:

    VERSION = "1.0.0"
    WIDTH = user32.GetSystemMetrics(0) - (user32.GetSystemMetrics(0) - 1200)
    HEIGHT = user32.GetSystemMetrics(1) - (user32.GetSystemMetrics(1) - 800)
    APP_NAME = "HyperPolygon"
    APP_ICON_PATH = "E:/Imagens/raizenbergue.jpg"

    @staticmethod
    def get_usable_screen_size() -> tuple[int, int]:
        screen_height = user32.GetSystemMetrics(1)
        work_height = user32.GetSystemMetrics(3)

        usable_height = screen_height - work_height

        return user32.GetSystemMetrics(0), usable_height

