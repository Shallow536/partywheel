from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from utils.wheel import WheelLogic
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class HomeScreen(Screen):
    input_text = ObjectProperty(None)
    suggestion_list = ObjectProperty(None)

    def on_pre_enter(self):
        self.update_list()

    def open_input_popup(self):
        box = BoxLayout(orientation='vertical', padding=20, spacing=10)
        input_field = TextInput(hint_text='your advise', multiline=False, font_size=18, size_hint_y=None, height=44)
        btns = BoxLayout(size_hint_y=None, height=44, spacing=10)
        btn_ok = Button(text='ok', background_color=(0.2,0.4,0.8,1), color=(1,1,1,1), font_size=16)
        btn_cancel = Button(text='no', background_color=(0.7,0.7,0.7,1), color=(1,1,1,1), font_size=16)
        btns.add_widget(btn_ok)
        btns.add_widget(btn_cancel)
        box.add_widget(input_field)
        box.add_widget(btns)
        popup = Popup(title='your advise', content=box, size_hint=(.8, None), height=200, auto_dismiss=False)
        def on_ok(instance):
            text = input_field.text.strip()
            if text:
                WheelLogic.add_suggestion(text)
                self.update_list()
            popup.dismiss()
        def on_cancel(instance):
            popup.dismiss()
        btn_ok.bind(on_release=on_ok)
        btn_cancel.bind(on_release=on_cancel)
        popup.open()

    def update_list(self):
        suggestions = WheelLogic.get_suggestions()
        self.suggestion_list.text = "\n".join(f"• {s}" for s in suggestions)

    def go_to_wheel(self):
        self.manager.current = 'wheel'




