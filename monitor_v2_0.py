# Author: Aditya
# 04/17/2024

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QHBoxLayout, QLineEdit, QPushButton, QSizePolicy
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont
from pydm.widgets.label import PyDMLabel
from pydm.utilities.units import find_unittype as unit_type
from epics import PV

class EPICSWatcher(QWidget):
    def __init__(self, parent=None):
        super(EPICSWatcher, self).__init__(parent)
        
        #self.pv_label = QLabel("EPICS PV Name:")
        self.pv_input = QLineEdit()
        self.pv_input.setPlaceholderText("Enter PV")
        self.pv_input.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pv_input.returnPressed.connect(self.start_timer)
        
        self.comp_label = QLabel("Comparison Value(s):")
        self.comp_input_high = QLineEdit()
        self.comp_input_high.setPlaceholderText("Enter upper limit")
        self.comp_input_high.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.comp_input_high.returnPressed.connect(self.start_timer)
        
        self.comp_input_low = QLineEdit()
        self.comp_input_low.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.comp_input_low.setPlaceholderText("Enter lower limit")
        self.comp_input_low.returnPressed.connect(self.start_timer)
        
        
        #font size
        self.size1 = 20
        self.weight1 = 65
        self.font = QFont()
        self.font.setPointSize(self.size1)
        self.font.setWeight(self.weight1)
        
        self.size2 = 40
        self.weight2 = 65
        self.font2 = QFont()
        self.font2.setPointSize(self.size2)
        self.font2.setWeight(self.weight2)

        self.epics_label = PyDMLabel()
        self.epics_label.setText("PV Readback")
        self.epics_label.setAlignment(Qt.AlignCenter)
        self.epics_label.setFont(self.font2)
        self.epics_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.epics_label.setEnabled(True)
        self.epics_label.setScaledContents(True)
        self.epics_label.setProperty("showUnits", True)
        self.epics_label.setProperty("alarmSensitiveBorder", False)
        self.epics_label.setStyleSheet("background-color: white;")
        
        self.pv_name_disp = QLabel()
        self.pv_name_disp.setText("PV Name")
        self.pv_name_disp.setAlignment(Qt.AlignCenter)
        self.pv_name_disp.setFont(self.font)
        
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_timer)
        self.start_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_timer)
        
        
        self.bigify = QPushButton("Make Bigger")
        self.bigify.clicked.connect(self.enbiggen)
        
        self.smallify = QPushButton("Make Smaller")
        self.smallify.clicked.connect(self.smallification)
        
        self.resetfont = QPushButton("Reset Font")
        self.resetfont.clicked.connect(self.reset_font)
        
        self.layout = QGridLayout()
        self.layout.addWidget(self.pv_input, 0, 0, 1, 2)
        self.layout.addWidget(self.comp_label, 1, 0, 1, 2)
        self.layout.addWidget(self.comp_input_high, 2, 0)
        self.layout.addWidget(self.comp_input_low, 2, 1)
        self.layout.addWidget(self.start_button, 3, 0)
        self.layout.addWidget(self.stop_button, 3, 1)
        self.layout.addWidget(self.pv_name_disp, 4, 0, 1, 2)
        self.layout.addWidget(self.epics_label, 5, 0, 1, 2)
        self.layout.addWidget(self.bigify, 6, 0)
        self.layout.addWidget(self.smallify, 6, 1)
        self.layout.addWidget(self.resetfont, 7, 0, 1, 2)
        
        self.setLayout(self.layout)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_epics_value)
        self.pv_name = None
        self.comparison_value_high = float('nan')
        self.comparison_value_low = 0

    def start_timer(self):
        self.pv_name = self.pv_input.text()
        try:
        		self.comparison_value_high = float(self.comp_input_high.text())
        		self.comparison_value_low = float(self.comp_input_low.text())
        except Exception:
        		pass
        self.epics_label.channel = self.pv_name
        
        self.timer.start(1000)  # Update every second
        self.update_epics_value()
        
    def stop_timer(self):
    		self.timer.stop()
    		self.epics_label.channel = None
    		self.epics_label.setStyleSheet("background-color: white;")
    		self.comparison_value_high = float('nan')
    		self.comparison_value_low = float('nan')
    		
    def enbiggen(self):
        self.size1 += 5				
        self.size2 += 10
        
        self.font.setPointSize(self.size1)
        self.font2.setPointSize(self.size2)
        
        self.pv_name_disp.setFont(self.font)
        self.epics_label.setFont(self.font2)
				
    def smallification(self):
        self.size1 -= 5
        self.size2 -= 10
        
        self.font.setPointSize(self.size1)
        self.font2.setPointSize(self.size2)
        
        self.pv_name_disp.setFont(self.font)
        self.epics_label.setFont(self.font2)
        
    def reset_font(self):
        #font size
        self.size1 = 20
        self.weight1 = 65
        self.font = QFont()
        self.font.setPointSize(self.size1)
        self.font.setWeight(self.weight1)
        
        self.size2 = 40
        self.weight2 = 65
        self.font2 = QFont()
        self.font2.setPointSize(self.size2)
        self.font2.setWeight(self.weight2)
        
        self.pv_name_disp.setFont(self.font)
        self.epics_label.setFont(self.font2)
				

    def update_epics_value(self):
        if self.pv_name is None or (self.comparison_value_high==float('nan') and self.comparison_value_low==float('nan')):
            return

        pv = PV(self.pv_name)
        value = pv.get()
        self.pv_name_disp.setText(self.pv_input.text())

        if value > self.comparison_value_high or value < self.comparison_value_low:
            self.epics_label.setStyleSheet("background-color: red;")
        elif (self.comparison_value_high==float('nan') and self.comparison_value_low==float('nan')):
            self.epics_label.setStyleSheet("background-color: white;")
        else:
            self.epics_label.setStyleSheet("background-color: lime;")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    watcher = EPICSWatcher()
    watcher.show()
    sys.exit(app.exec_())
