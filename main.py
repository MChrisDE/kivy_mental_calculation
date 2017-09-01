from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from trainer import *

exercises = []


class MainScreen(Screen):
	pass


class PlayMenuScreen(Screen):
	def startgame(self, name):
		global exercises
		exercises = list(range(name))
		print(exercises)


class TrainingMenuScreen(Screen):
	def checkbox(self, active, name):
		global exercises
		if active:
			exercises.append(name)
		else:
			exercises.remove(name)


class TrainingScreen(Screen):
	def __init__(self, **kwargs):
		super(TrainingScreen, self).__init__(**kwargs)

	def on_pre_enter(self, *args):
		global exercises
		self.exercises = exercises
		self.trainer = Trainer(self.exercises)
		self.add_widget(self.trainer)

	def on_leave(self, *args):
		self.remove_widget(self.trainer)


class PlayScreen(Screen):
	def __init__(self, **kwargs):
		super(PlayScreen, self).__init__(**kwargs)

	def on_pre_enter(self, *args):
		global exercises
		self.exercises = exercises
		self.trainer = Trainer(self.exercises, timer=True)
		self.add_widget(self.trainer)

	def on_leave(self, *args):
		self.trainer.event.cancel()
		self.remove_widget(self.trainer)


class ScreenManagement(ScreenManager):
	pass


class MathApp(App):
	def build(self):
		self.load_kv("main.kv")
		sm = ScreenManagement()
		return sm


if __name__ == "__main__":
	MathApp().run()
