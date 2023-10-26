# todo -> Implement Outlook email functionality
import sys
from PyQt6.QtWidgets import QApplication
import windows.login_window
app = QApplication(sys.argv)
main_window = windows.login_window.MainWindow()
main_window.show()
sys.exit(app.exec())
