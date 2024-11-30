import sys
import qt_controller 

from PyQt5.QtWidgets import QApplication


if __name__ == "__main__":

    app = QApplication(sys.argv)
    controller = qt_controller.QT_Controler()
    
    try:
        sys.exit(app.exec_())
    except:
        print('Exiting')