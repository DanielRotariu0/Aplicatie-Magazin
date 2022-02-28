from MeniuPrincipal import *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    meniu = MeniuPrincipal()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(meniu)
    widget.setWindowTitle("Meniu Principal")
    widget.setFixedWidth(800)
    widget.setFixedHeight(600)
    widget.show()
    try:
        sys.exit(app.exec_())
    except:
        pass
