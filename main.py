from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.properties import StringProperty, ObjectProperty, OptionProperty
from kivy.uix.textinput import TextInput
from random import randint
import os

os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'  # opengl error fix for win10


class Trainer(BoxLayout):
	text = StringProperty()
	display = ObjectProperty(None)

	def __init__(self, **kwargs):
		super(Trainer, self).__init__(**kwargs)  # init BoxLayout
		self.numbers = []
		self.operator = []
		with open('exercise.txt') as f:
			data = f.readlines()
		for i in range(len(data)):
			line = data[i].replace(" ", "")
			cursor = 0
			temp = []
			temp2 = []
			while cursor != -1:
				cursor = line.find('[')
				cursor2 = line.find(']')
				if cursor2 != -1:
					temp.append(line[cursor + 1:cursor2].split(','))
					temp2.append(line[cursor2 + 1:line.find('[', cursor2)])
				line = line[cursor2 + 1:]
			self.numbers.append(temp)
			del temp2[-1]
			self.operator.append(temp2)
		self.new_exercise()  # first exercise

	def check(self):
		try:
			textinput = int(self.display.text)
			try:
				solution = eval(self.text)
			except Exception:
				self.text = "Error"
			if solution == textinput:
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

	def smart_check(self):
		try:
			textinput = int(self.display.text)
			try:
				solution = eval(self.text)
			except Exception:
				self.text = "Error"
			if solution == textinput:
				self.new_exercise()
				self.display.text = ""
		except ValueError:  # when textinput is NaN
			pass


class ValueErrorPopup(Popup):
	pass


class TAPopup(Popup):
	pass


class SolutionInput(TextInput):
	input_type = OptionProperty('number', options=('number', 'text')) #number keyboard on android


class MathApp(App):
	def build(self):
		self.load_kv("main.kv")
		return Trainer()


if __name__ == "__main__":
	MathApp().run()
