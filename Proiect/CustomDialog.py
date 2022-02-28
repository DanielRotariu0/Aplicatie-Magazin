from CommitDialog import *

WINDOW_OPEN = 0


class CustomDialog(QDialog):
    def __init__(self, name):
        super(QDialog, self).__init__()
        loadUi("interface/" + name + ".ui", self)
        self.setWindowTitle(name.capitalize())
        self.commit_dialog = CommitDialog(name)
        self.commit_dialog.setFixedWidth(400)
        self.commit_dialog.setFixedHeight(400)
        self.table.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.disable_text()
        self.button_salveaza.setEnabled(False)
        self.context = 0
        self.id = 0
        self.changes = 0
        CustomDialog.WINDOW_OPEN = 0
        self.button_adauga.clicked.connect(self.adauga)
        self.button_editeaza.clicked.connect(self.editeaza)
        self.button_salveaza.clicked.connect(self.salveaza)
        self.button_sterge.clicked.connect(self.sterge)
        self.button_iesire.clicked.connect(self.iesire)

    def closeEvent(self, event):
        self.iesire()

    def load_data(self):
        pass

    def disable_text(self):
        pass

    def enable_text(self):
        pass

    def adauga(self):
        self.enable_text()
        self.button_adauga.setEnabled(False)
        self.button_editeaza.setEnabled(False)
        self.button_sterge.setEnabled(False)
        self.button_salveaza.setEnabled(True)
        self.context = 1

    def editeaza(self):
        self.enable_text()
        self.button_adauga.setEnabled(False)
        self.button_editeaza.setEnabled(False)
        self.button_sterge.setEnabled(False)
        self.button_salveaza.setEnabled(True)
        self.context = 2

    def salveaza(self):
        self.changes = 1

    def sterge(self):
        self.changes = 1

    def iesire(self):
        self.disable_text()
        self.button_salveaza.setEnabled(False)
        self.button_adauga.setEnabled(True)
        self.button_editeaza.setEnabled(True)
        self.button_sterge.setEnabled(True)
        self.hide()
        CustomDialog.WINDOW_OPEN = 0
        if self.changes == 1:
            self.commit_dialog.show()
