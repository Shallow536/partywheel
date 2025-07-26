from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty, StringProperty, ListProperty
from utils.wheel import WheelLogic
import random

from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rotate, PushMatrix, PopMatrix
from kivy.core.text import Label as CoreLabel
from kivy.clock import Clock
import math

from kivy.animation import Animation
from kivy.properties import ListProperty

from kivy.graphics import Rectangle, Triangle

from kivy.factory import Factory



class WheelScreen(Screen):
    suggestions = ListProperty([])
    result = StringProperty("")
    wheel_angle = NumericProperty(0)

    def on_pre_enter(self):
        # 从 WheelLogic 读取用户输入提议
        self.suggestions = WheelLogic.get_suggestions()
        self.result = ""

    def spin(self):
        if not self.suggestions:
            self.result = "add first"
            return

        picked_text, picked_index = WheelLogic.pick()
        num = len(self.suggestions)
        angle_per = 360 / num
        current_angle = self.wheel_angle % 360
        N = 5
        # 让picked_index的中心对齐12点钟方向（0°）
        target_angle = self.wheel_angle + 360 * N + (0 - (picked_index + 0.5) * angle_per - current_angle)
        self.target_index = picked_index
        self.result = ""
        anim = Animation(wheel_angle=target_angle, duration=4, t='out_cubic')
        anim.bind(on_complete=lambda *a: self._show_result(picked_text))
        anim.start(self)

    def _show_result(self, picked_text):
        self.result = picked_text



class SpinningWheel(Widget):
    angle = NumericProperty(0)
    suggestions = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.on_size, pos=self.on_pos, angle=self.on_angle)

    def on_suggestions(self, instance, value):
        self.canvas.clear()
        if not value:
            return
        self.draw_wheel()

    def on_angle(self, instance, value):
        self.canvas.clear()
        if not self.suggestions:
            return
        self.draw_wheel()

    def on_size(self, *args):
        self.canvas.clear()
        if not self.suggestions:
            return
        self.draw_wheel()

    def on_pos(self, *args):
        self.canvas.clear()
        if not self.suggestions:
            return
        self.draw_wheel()

    def draw_wheel(self):
        with self.canvas:
            PushMatrix()
            # 转盘正常旋转，不加偏移
            Rotate(angle=self.angle, origin=self.center)
            num = len(self.suggestions)
            if num == 0:
                PopMatrix()
                return
            angle_per = 360 / num
            radius = min(self.width, self.height) / 2
            center = self.center
            def hsv_to_rgb(h, s, v):
                import colorsys
                return colorsys.hsv_to_rgb(h, s, v)
            colors = [hsv_to_rgb(i/num, 0.6, 0.95) + (0.95,) for i in range(num)]

            for i, text in enumerate(self.suggestions):
                Color(*colors[i])
                # 扇形角度分配：第0号扇形从0°开始，顺时针排列
                start_angle = i * angle_per
                end_angle = (i + 1) * angle_per
                Ellipse(pos=(center[0] - radius, center[1] - radius),
                        size=(radius * 2, radius * 2),
                        angle_start=start_angle,
                        angle_end=end_angle)

                # 内容绘制：加90°偏移让内容在扇形中央
                base_angle = (i + 0.5) * angle_per + 90
                show_angle = math.radians(base_angle)
                label = CoreLabel(text=text, font_size=26, bold=True)
                label.refresh()
                texture = label.texture
                x = center[0] + radius * 0.65 * math.cos(show_angle - math.pi/2) - texture.size[0] / 2
                y = center[1] + radius * 0.65 * math.sin(show_angle - math.pi/2) - texture.size[1] / 2
                padding_w = texture.size[0] * 0.7
                padding_h = texture.size[1] * 0.9
                ellipse_x = x - padding_w / 2
                ellipse_y = y - padding_h / 2
                ellipse_w = texture.size[0] + padding_w
                ellipse_h = texture.size[1] + padding_h
                Color(1, 1, 1, 0.98)
                Ellipse(pos=(ellipse_x, ellipse_y), size=(ellipse_w, ellipse_h))
                Color(0, 0, 0, 1)
                Rectangle(texture=texture, pos=(x, y), size=texture.size)

            PopMatrix()
            # 指针绘制在12点钟方向
            pointer_height = radius * 0.13
            pointer_width = radius * 0.22
            px = center[0]
            py = center[1] + radius + pointer_height / 2
            Color(0.2, 0.2, 0.2, 0.4)
            Triangle(points=[
                px, py-3,
                px - pointer_width / 2, py - pointer_height-3,
                px + pointer_width / 2, py - pointer_height-3
            ])
            Color(1, 0.84, 0, 1)
            Triangle(points=[
                px, py,
                px - pointer_width / 2, py - pointer_height,
                px + pointer_width / 2, py - pointer_height
            ])

Factory.register('SpinningWheel', cls=SpinningWheel)