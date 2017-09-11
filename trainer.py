from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.properties import StringProperty, ObjectProperty, OptionProperty
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from random import randint
import json


class Trainer(Widget):
	text = StringProperty("")
	time = StringProperty("Training")
	display = ObjectProperty(None)

	def __init__(self, exercises, timer=False, **kwargs):
		super(Trainer, self).__init__(**kwargs)
		self.numbers = []
		self.operator = []
		self.score = 0
		self.exercises = exercises
		with open('data.json', 'r') as f:
			array = json.load(f)
		for a in range(len(array)):
			i = array[a]
			if a in exercises or not exercises:
				temp = []
				for a in range(i['len']):
					temp.append(i[str(a)])
				self.numbers.append(temp)
				self.operator.append(i["op"])
		self.new_exercise()  # first exercise
		if timer:
			self.time = "30"
			self.event = Clock.schedule_interval(self.timer, 1)

	def timer(self, *args):
		time = int(self.time) - 1
		self.time = str(time)
		if time == 0:
			self.event.cancel()
			popup = ScorePopup(auto_dismiss=False)
			popup.score = str(self.score)
			popup.open()

	def check(self):  # check on enter
		try:
			textinput = int(self.display.text)
			try:
				solution = eval(self.text)
			except Exception:
				self.text = "Error"
			if solution == textinput:
				self.score += 1
				self.new_exercise()
			else:
				popup = TAPopup(auto_dismiss=False)
				popup.open()
			self.display.text = ""
		except ValueError:  # when textinput is NaN
			popup = ValueErrorPopup(auto_dismiss=False)
			popup.open()

	def new_exercise(self):
		rand = []
		line_index = randint(0, len(self.numbers) - 1)
		for i in self.numbers[line_index]:
			rand.append(randint(int(i[0]), int(i[1])))
		self.text = str(rand[0])
		for i in range(1, len(rand)):
			self.text += self.operator[line_index][i - 1]
			self.text += str(rand[i])

	def smart_check(self):  # check on input
		try:
			textinput = int(self.display.text)
			try:
				solution = eval(self.text)
			except Exception:
				self.text = "Error"
			if solution == textinput:
				self.new_exercise()
				self.score += 1
				self.display.text = ""
		except ValueError:  # when textinput is NaN
			pass


class ValueErrorPopup(Popup):
	pass


class TAPopup(Popup):
	pass


class ScorePopup(Popup):
	score = StringProperty("")


class SolutionInput(TextInput):
	input_type = OptionProperty('number', options=('number', 'text'))  # number keyboard on android
