import cx_Oracle
from CustomDialog import *


class ArmeDialog(CustomDialog):
    def __init__(self):
        super().__init__("arme")

    def load_data(self):
        self.comboBox_id_tip_arma.clear()
        self.comboBox_id_munitie.clear()
        arme = []
        cursor = con.cursor()
        cursor.execute('select * from arme order by id')
        for result in cursor:
            arma = {'id': str(result[0]), 'tipuri_arme_id': str(result[1]), 'pret': str(result[2]),
                    'denumire': str(result[3]),
                    'munitie_id': str(result[4]),
                    'gloante/incarcator': str(result[5]), 'calibru': str(result[6])}

            arme.append(arma)
        cursor.close()
        row = 0
        self.table.setRowCount(len(arme))
        for arma in arme:
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(arma["id"]))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(arma["tipuri_arme_id"]))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(arma["pret"]))
            self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(arma["denumire"]))
            self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(arma["munitie_id"]))
            self.table.setItem(row, 5, QtWidgets.QTableWidgetItem(arma["gloante/incarcator"]))
            self.table.setItem(row, 6, QtWidgets.QTableWidgetItem(arma["calibru"]))
            row = row + 1
        self.table.resizeColumnsToContents()
        tipuri_arme = []
        cursor = con.cursor()
        cursor.execute('select * from tipuri_arme')
        for result in cursor:
            tip = {'id': str(result[0]), 'denumire': str(result[1])}
            tipuri_arme.append(tip)
        cursor.close()
        for tip in tipuri_arme:
            option = tip["id"] + ": " + tip["denumire"]
            self.comboBox_id_tip_arma.addItem(option)

        munitie = []
        cursor = con.cursor()
        cursor.execute('select * from munitie')
        for result in cursor:
            m = {'id': str(result[0]), 'denumire': str(result[1]), 'tip': str(result[2])}
            munitie.append(m)
        cursor.close()
        for m in munitie:
            option = m["id"] + ": " + m["denumire"] + " " + m["tip"]
            self.comboBox_id_munitie.addItem(option)

    def disable_text(self):
        self.text_pret.setPlainText("")
        self.text_denumire.setPlainText("")
        self.text_gloante.setPlainText("")
        self.text_calibru.setPlainText("")
        self.text_pret.setEnabled(False)
        self.text_denumire.setEnabled(False)
        self.text_gloante.setEnabled(False)
        self.text_calibru.setEnabled(False)
        self.comboBox_id_tip_arma.setEnabled(False)
        self.comboBox_id_munitie.setEnabled(False)

    def enable_text(self):
        self.text_pret.setEnabled(True)
        self.text_denumire.setEnabled(True)
        self.text_gloante.setEnabled(True)
        self.text_calibru.setEnabled(True)
        self.comboBox_id_tip_arma.setEnabled(True)
        self.comboBox_id_munitie.setEnabled(True)

    def editeaza(self):
        selected_row = self.table.currentRow()
        self.id = self.table.item(selected_row, 0).text()
        if int(self.id) == 0:
            msg = QMessageBox()
            msg.setWindowTitle("Eroare")
            msg.setText("Aceasta inregistrare nu poate fi modificata")
            msg.exec_()
        else:
            super().editeaza()
            id_tip_arma = self.table.item(selected_row, 1).text()
            tipuri_arme = [self.comboBox_id_tip_arma.itemText(i) for i in range(self.comboBox_id_tip_arma.count())]
            for tip in tipuri_arme:
                if tip.split(" ")[0][0] == id_tip_arma:
                    self.comboBox_id_tip_arma.setCurrentText(tip)

            id_munitie = self.table.item(selected_row, 4).text()
            munitie = [self.comboBox_id_munitie.itemText(i) for i in range(self.comboBox_id_munitie.count())]
            for m in munitie:
                if m.split(" ")[0][0] == id_munitie:
                    self.comboBox_id_munitie.setCurrentText(m)

            self.text_pret.setPlainText(self.table.item(selected_row, 2).text())
            self.text_denumire.setPlainText(self.table.item(selected_row, 3).text())
            self.text_gloante.setPlainText(self.table.item(selected_row, 5).text())
            self.text_calibru.setPlainText(self.table.item(selected_row, 6).text())

    def salveaza(self):
        id_tip_arma = self.comboBox_id_tip_arma.currentText().split(" ")[0][0]
        id_munitie = self.comboBox_id_munitie.currentText().split(" ")[0][0]
        pret = self.text_pret.toPlainText()
        denumire = self.text_denumire.toPlainText()
        gloante = self.text_gloante.toPlainText()
        calibru = self.text_calibru.toPlainText()
        valid = 0
        r_p_g = re.compile(r'[0-9]+')
        r_c_d = re.compile(r'.+')
        if re.fullmatch(r_p_g, pret) and re.fullmatch(r_p_g, gloante):
            if re.fullmatch(r_c_d, denumire) and re.fullmatch(r_c_d, calibru):
                if not (int(id_munitie) == 0 and (int(gloante) != 0 or int(calibru) != 0)):
                    valid = 1
        if valid == 1:
            self.disable_text()
            self.button_salveaza.setEnabled(False)
            self.button_adauga.setEnabled(True)
            self.button_editeaza.setEnabled(True)
            self.button_sterge.setEnabled(True)
            if self.context == 1:
                try:
                    cursor = con.cursor()
                    cursor.execute("select max(id) from arme")
                    max_id = 0
                    for result in cursor:
                        max_id = result[0]
                    cursor.close()
                    cursor = con.cursor()
                    cursor.execute(
                        "insert into arme values (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', "
                        "\'{}\')".format(max_id + 1, id_tip_arma, pret, denumire, id_munitie, gloante, calibru))
                    cursor.close()
                except cx_Oracle.DatabaseError as exc:
                    error, = exc.args
                    print("Oracle-Error-Code:", error.code)
                    print("Oracle-Error-Message:", error.message)
                self.load_data()
                super().salveaza()
            elif self.context == 2:
                try:
                    cursor = con.cursor()
                    cursor.execute(
                        "update arme set tipuri_arme_id = \'{}\', pret = \'{}\', denumire = \'{}\', munitie_id = "
                        "\'{}\', gloante_pe_incarcator = \'{}\', calibru = \'{}\' where id = {}"
                            .format(id_tip_arma, pret, denumire, id_munitie, gloante, calibru, self.id))
                    cursor.close()
                except cx_Oracle.DatabaseError as exc:
                    error, = exc.args
                    print("Oracle-Error-Code:", error.code)
                    print("Oracle-Error-Message:", error.message)
                self.load_data()
                super().salveaza()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Eroare")
            msg.setText(
                "Nu ati introdus un camp sau ati introdus un camp gresit!\n\nConstrangerile sunt:\n\tPret: "
                "numar\n\tDenumire: sir de caractere\n\tGloante/Incarcator: numar\n\tCalibru: sir de caractere\n"
                "\n\tDaca Munitie este 0, atunci Gloante/Incarcator si Calibru trebuie sa fie 0")
            msg.exec_()

    def sterge(self):
        selected_row = self.table.currentRow()
        self.id = self.table.item(selected_row, 0).text()
        found = 0
        try:
            cursor = con.cursor()
            cursor.execute("select arme_id from tranzactii")
            for result in cursor:
                if self.id == str(result[0]):
                    found = 1
            cursor.close()
            cursor = con.cursor()
            cursor.execute("select arme_id from conditii_arme")
            for result in cursor:
                if self.id == str(result[0]):
                    found = 1
            cursor.close()
        except cx_Oracle.DatabaseError as exc:
            error, = exc.args
            print("Oracle-Error-Code:", error.code)
            print("Oracle-Error-Message:", error.message)
        if found == 1:
            msg = QMessageBox()
            msg.setWindowTitle("Eroare")
            msg.setText("Arma nu poate fi stearsa deoarece apare intr-o tranzactie sau in conditii.")
            msg.exec_()
        else:
            try:
                cursor = con.cursor()
                cursor.execute("delete from arme where id = {}".format(self.id))
                cursor.close()
            except cx_Oracle.DatabaseError as exc:
                error, = exc.args
                print("Oracle-Error-Code:", error.code)
                print("Oracle-Error-Message:", error.message)
            self.load_data()
            super().sterge()
