from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screens.home_screen import HomeScreen
from screens.wheel_screen import WheelScreen

class PartyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(WheelScreen(name='wheel'))
        return sm

if __name__ == '__main__':
    PartyApp().run()
