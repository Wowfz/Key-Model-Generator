from mainWindow import *

def main():
    app = QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
