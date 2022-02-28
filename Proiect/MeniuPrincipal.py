from ClientiDialog import *
from TranzactiiDialog import *
from ArmeDialog import *
from TipuriArmeDialog import *
from ConditiiArmeDialog import *
from MunitieDialog import *
from PoligonDialog import *


def show_dialog(dialog, savepoint):
    if CustomDialog.WINDOW_OPEN == 0:
        dialog.changes = 0
        dialog.setFixedWidth(800)
        dialog.setFixedHeight(600)
        dialog.show()
        dialog.load_data()
        cursor = con.cursor()
        cursor.execute('savepoint '+savepoint)
        cursor.close()
        CustomDialog.WINDOW_OPEN = 1


class MeniuPrincipal(QMainWindow):
    def __init__(self):
        super(MeniuPrincipal, self).__init__()
        loadUi("interface/meniu.ui", self)

        self.clienti_dialog = ClientiDialog()
        self.tranzactii_dialog = TranzactiiDialog()
        self.arme_dialog = ArmeDialog()
        self.tipuri_arme_dialog = TipuriArmeDialog()
        self.conditii_arme_dialog = ConditiiArmeDialog()
        self.munitie_dialog = MunitieDialog()
        self.poligon_dialog = PoligonDialog()

        self.button_clienti.clicked.connect(lambda: show_dialog(self.clienti_dialog, "clienti"))
        self.button_tranzactii.clicked.connect(lambda: show_dialog(self.tranzactii_dialog, "tranzactii"))
        self.button_arme.clicked.connect(lambda: show_dialog(self.arme_dialog, "arme"))
        self.button_tipuri.clicked.connect(lambda: show_dialog(self.tipuri_arme_dialog, "tipuri"))
        self.button_conditii.clicked.connect(lambda: show_dialog(self.conditii_arme_dialog, "conditii"))
        self.button_munitie.clicked.connect(lambda: show_dialog(self.munitie_dialog, "munitie"))
        self.button_poligon.clicked.connect(lambda: show_dialog(self.poligon_dialog, "poligon"))
