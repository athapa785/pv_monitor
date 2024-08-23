from PyQt5 import QtGui
from epics import PV
from pydm import Display
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import *
import sys

STYLE_WHITE = "background-color: rgb(255, 255, 255);"

class monitorDisplay(Display):
	
	def __init__(self, parent=None, args=None):
		super(monitorDisplay, self).__init__(parent=parent, args=args)
		self.ui.flag.setStyleSheet(STYLE_WHITE) #white
		
		self.ui.comp_input.returnPressed.connect(self.start_timer)
		
		#Timer
		self.timer = QTimer(self)
		self.timer.timeout.connect(self.update_epics_value)
		self.pv_name = None
		self.comparison_value = None
		
	def ui_filename(self):
		return 'monitor.ui'
	
	def start_timer(self):
		self.pv_name = self.ui.pv_input.text()
		self.comparison_value = self.ui.comp_input.text() 
		self.flag.channel = self.pv_name
		self.timer.start(1000)  # Update every second
		self.update_epics_value()

	def update_epics_value(self):
		if self.pv_name is None or self.comparison_value is None:
			return
			
		pv = PV(self.pv_name)
		value = pv.get()

		self.pv_name_disp.setText(self.pv_input.text())
	
		if float(value) > float(self.comparison_value):
			self.ui.flag.setStyleSheet("background-color: red;")
		else:
			self.ui.flag.setStyleSheet("background-color: lime;")


if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = monitorDisplay()
	window.show()
	sys.exit(app.exec_())

