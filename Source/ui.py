# Python Wheels Import
import pygame
from win32gui import GetForegroundWindow, GetActiveWindow, SetForegroundWindow, SetWindowPos
from win32con import HWND_TOPMOST, SWP_NOMOVE, SWP_NOSIZE
from time import sleep, time


# My Files Import


# End Import

class UiConfig:
    def __init__(self):
        self.title = ""
        self.size = (500, 300)
        self.bg_color = (230, 230, 230, 255)

        self.exit_max = 15
        self.exit_init_sec = 1

        self.ender_print_time = 3


class Ui:
    def __init__(self, _config_obj: UiConfig):
        self.running = True
        self.exit = 0
        self.mouse_pos = (-1, -1)

        self.__config = _config_obj

        self.low_time = time()

        pygame.init()

        pygame.display.set_caption(self.__config.title, self.__config.title)  # 设置窗口标题
        pygame.display.set_icon(pygame.image.load("./Resource/Ui/Images/alpha.png"))  # 设置图标为透明图片
        self.screen = pygame.display.set_mode(self.__config.size, pygame.NOFRAME)  # 创建无边框屏幕surface
        self.hwnd = pygame.display.get_wm_info()["window"]
        self.screen.fill(self.__config.bg_color)

        self.main_image = pygame.image.load("./Resource/Ui/Images/main.png")
        self.main_image = pygame.transform.scale(self.main_image, _config_obj.size)

        self.ender_false_image = pygame.image.load("./Resource/Ui/Images/ender-false.png")
        self.ender_false_image = pygame.transform.scale(self.ender_false_image, _config_obj.size)

        self.ender_true_image = pygame.image.load("./Resource/Ui/Images/ender-true.png")
        self.ender_true_image = pygame.transform.scale(self.ender_true_image, _config_obj.size)

        # self.active_window(self.hwnd)
        self.pinned_window(self.hwnd)

    @staticmethod
    def active_window(hwnd: int):
        try:
            SetForegroundWindow(hwnd)
            return True, "Success"
        except Exception as e:
            return False, e

    @staticmethod
    def check_active(hwnd: int):
        try:
            if GetForegroundWindow() == hwnd or GetActiveWindow() == hwnd:
                return True, "Yes"
            else:
                return False, "Unknown"
        except Exception as e:
            return False, e

    @staticmethod
    def pinned_window(hwnd):
        try:
            SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)
            return True, "Success"
        except Exception as e:
            return False, e

    def header(self):
        self.screen.fill(self.__config.bg_color)
        self.screen.blit(self.main_image, (0, 0))
        for e in pygame.event.get():
            if e.type == pygame.KEYUP:
                self.exit += 1
                self.low_time = time()
            if e.type == pygame.MOUSEBUTTONDOWN or e.type == pygame.MOUSEBUTTONUP:
                self.exit = self.__config.exit_max + 1
                self.low_time = time()

            if self.mouse_pos != (-1, -1) and pygame.mouse.get_pos() != self.mouse_pos:
                self.exit += 1
                self.low_time = time()
            else:
                self.mouse_pos = pygame.mouse.get_pos()

        if time() - self.low_time > self.__config.exit_init_sec:
            self.exit = 0
            self.low_time = time()

        if not self.check_active(self.hwnd)[0]:
            self.exit = self.__config.exit_max + 1
        # self.active_window(self.hwnd)
        self.pinned_window(self.hwnd)

        pygame.display.update()

    def ender(self, timeout: float, _type: bool):
        # self.active_window(self.hwnd)
        self.pinned_window(self.hwnd)
        i = 0
        while i <= timeout * 100:
            self.screen.fill(self.__config.bg_color)
            if _type:
                self.screen.blit(self.ender_true_image, (0, 0))
            else:
                self.screen.blit(self.ender_false_image, (0, 0))
            sleep(0.01)
            i += 1
            pygame.event.get()
            pygame.display.update()

    def mainloop(self, timeout: float):
        low_time = time()
        while True:
            self.header()
            if self.exit > self.__config.exit_max:
                self.ender(self.__config.ender_print_time, False)
                pygame.display.quit()
                pygame.quit()
                return 1
            sleep(0.01)
            if time() - low_time > timeout:
                break
        self.ender(self.__config.ender_print_time, True)
        pygame.display.quit()
        pygame.quit()
        return 0
