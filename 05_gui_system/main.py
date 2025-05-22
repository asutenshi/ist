import sys
from PyQt5.QtWidgets import QApplication
from gui_logic import ShopApp

def main():
    app = QApplication(sys.argv)
    
    window = ShopApp()
    
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()