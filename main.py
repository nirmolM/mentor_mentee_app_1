# todo -> try to implement outlook email functionality, include parent email in database

import sys
from PyQt6.QtWidgets import QApplication
import windows.login_window
app = QApplication(sys.argv)
main_window = windows.login_window.MainWindow()
main_window.show()
sys.exit(app.exec())
