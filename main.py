from random import *
import json

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty


with open("data2.json", mode='r', buffering=-1, encoding='utf8') as read_file:  # подключение файла с текстом
    data = json.load(read_file)


class Menu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        boxlayout = BoxLayout(orientation="vertical", spacing=5, padding=[10])

        button_play = Button(
            text="Play",
            background_color=[0, 1.5, 3, 1],
            size_hint=[1, 0.1],
            on_press=self._on_press_button_play,
        )

        boxlayout.add_widget(button_play)
        self.add_widget(boxlayout)

    def _on_press_button_play(self, *args):
        self.manager.transition.direction = 'left'
        self.manager.current = 'gamescreen'


class MyLabel(Label):
    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(5, 5, 5, 1)
            Rectangle(pos=self.pos, size=self.size)


class Game_Screen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        menu = BoxLayout(orientation="horizontal", size_hint=[1, 0.1])
        boxlayout = BoxLayout(orientation="vertical", spacing=5, padding=[10])

        monitor = BoxLayout()
        self.tx = MyLabel(text=data["stats"]["text"],color=[0,0,1,1])
        monitor.add_widget(self.tx)

        self.bt1 = Button(text=self.t[0], background_color=[0, 1.5, 3, 1], size_hint=[1, 0.1],
                     on_press=lambda *args: self.do(1, *args))
        self.bt2 = Button(text=self.t[1], background_color=[0, 1.5, 3, 1], size_hint=[1, 0.1],
                     on_press=lambda *args: self.do(2, *args))
        self.bt3 = Button(text=self.t[2], background_color=[0, 1.5, 3, 1], size_hint=[1, 0.1],
                     on_press=lambda *args: self.do(3, *args))
        self.bt4 = Button(text=self.t[3], background_color=[0, 1.5, 3, 1], size_hint=[1, 0.1],
                     on_press=lambda *args: self.do(4, *args))

        self.exit = Button(text="exit", background_color=[0, 1.5, 3, 1], size_hint=[0.5, 1],
                          on_press=self._on_press_exit_game)
        self.reset = Button(text="restart", background_color=[0, 1.5, 3, 1], size_hint=[0.5, 1],
                           on_press=lambda *args: self.do(1, *args))

        menu.add_widget(self.exit)
        menu.add_widget(self.reset)
        boxlayout.add_widget(menu)
        boxlayout.add_widget(monitor)
        boxlayout.add_widget(self.bt1)
        boxlayout.add_widget(self.bt2)
        boxlayout.add_widget(self.bt3)
        boxlayout.add_widget(self.bt4)
        self.add_widget(boxlayout)

    def _on_press_exit_game(self, *args):
        self.manager.transition.direction = 'right'
        self.manager.current = 'main_menu'

    # ----------------


class Game(Game_Screen):
    l = 1
    special = {'s': 5, 'p': 5, 'e': 5, 'c': 5, 'i': 5, 'a': 5, 'l': 5}
    path = "stats"
    a = 0
    hp = 20
    state = "start"
    inventory = ["0"]
    t=data["stats"]["variants"]


    def do(self,a,*args):
        self.v(a)
        self.bt1.text = self.t[0]  # заполнение текста
        self.bt2.text = self.t[1]
        self.bt3.text = self.t[2]
        self.bt4.text = self.t[3]

    def v(self, n):  # обработка выбора и генерация пути
        if data[self.path]["key"][n - 1] not in self.inventory:
            self.tx.text = 'У выс нет предмета для совершения данного действия'  # очистить текст
            self.t = ["Напасть--", "Бежать.", "Говорить.", "Приручить."]
            return
        if len(data[self.path]["test"][n - 1])>0:
            self.tx.text = '- выс нет предмета для совершения данного error'  # очистить текст
            self.t = ["Напасть--", "Бежать.", "Говорить.", "Приручить."]
            return
        self.path=data[self.path]["path"][n]
        if self.path[0] == 'b':
            self.battle(n-1)
        else:
            self.choise(n)
    # ----------------

    def battle(self, a):
        chance = random()
        if self.state != "batle":
            self.tx.text = data[self.path]["text"]  # очистить текст
            self.t = data[self.path]["variants"]
            self.state = "batle"
            return
        if chance <= data[self.path]["chance"][a]:
            self.hp -= (data[self.path]["damage"][a])
            self.tx.text = "enemy hp is " + str(self.hp)  # очистить текст
        else:
            self.tx.text = "miss"  # очистить текст
        if self.hp <= 0:
            self.hp = 20
            self.path = 'b1'
            self.tx.text = data[self.path]["text"] # очистить текст
        # вставить текст вариантов

    # ----------------
    def choise(self, a):
        if self.state=="start":
            self.special = data["stats"]["special"][a]
            self.state="travel"
        if self.path == '0':
            self.path = ["v1", "v2", "v3", "v4"][randint(0,3)]
        self.tx.text = data[self.path]["text"]  # очистить текст
        self.t = data[self.path]["variants"]  # вставить текст вариантов


class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Menu(name='main_menu'))
        sm.add_widget(Game(name='gamescreen'))

        return sm


if __name__ == "__main__":
    MainApp().run()

