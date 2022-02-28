import cx_Oracle
from CustomDialog import *


class ConditiiArmeDialog(CustomDialog):
    def __init__(self):
        super().__init__("conditii")

    def load_data(self):
        self.comboBox_id_arma.clear()
        conditii = []
        cursor = con.cursor()
        cursor.execute('select * from conditii_arme order by id_arma')
        for result in cursor:
            conditie = {'id_arma': str(result[0]), 'varsta_necesara': str(result[1]), 'permis_necesar': str(result[2])}
            conditii.append(conditie)
        cursor.close()
        row = 0
        self.table.setRowCount(len(conditii))
        for conditie in conditii:
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(conditie["id_arma"]))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(conditie["varsta_necesara"]))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(conditie["permis_necesar"]))
            row = row + 1
        self.table.resizeColumnsToContents()
        arme = []
        cursor = con.cursor()
        cursor.execute('select * from arme')
        for result in cursor:
            arma = {'id': str(result[0]), 'tipuri_arme_id': str(result[1]), 'pret': str(result[2]),
                    'denumire': str(result[3]),
                    'munitie_id': str(result[4]),
                    'gloante/incarcator': str(result[5]), 'calibru': str(result[6])}
            arme.append(arma)
        cursor.close()
        for arma in arme:
            option = arma["id"] + ": " + arma["tipuri_arme_id"] + " " + arma["pret"] + " " + arma["denumire"] + " " + \
                     arma["munitie_id"] + " " + arma["gloante/incarcator"] + " " + arma["calibru"]
            self.comboBox_id_arma.addItem(option)

    def disable_text(self):
        self.text_varsta.setPlainText("")
        self.text_permis.setPlainText("")
        self.text_varsta.setEnabled(False)
        self.text_permis.setEnabled(False)
        self.comboBox_id_arma.setEnabled(False)

    def enable_text(self):
        self.text_varsta.setEnabled(True)
        self.text_permis.setEnabled(True)
        self.comboBox_id_arma.setEnabled(True)

    def editeaza(self):
        selected_row = self.table.currentRow()
        id_arma = self.table.item(selected_row, 0).text()
        if int(id_arma) == 0:
            msg = QMessageBox()
            msg.setWindowTitle("Eroare")
            msg.setText("Aceasta inregistrare nu poate fi modificata")
            msg.exec_()
        else:
            arme = [self.comboBox_id_arma.itemText(i) for i in range(self.comboBox_id_arma.count())]
            for arma in arme:
                if arma.split(" ")[0][0] == id_arma:
                    self.comboBox_id_arma.setCurrentText(arma)
            self.text_varsta.setPlainText(self.table.item(selected_row, 1).text())
            self.text_permis.setPlainText(self.table.item(selected_row, 2).text())
            super().editeaza()

    def salveaza(self):
        id_arma = self.comboBox_id_arma.currentText().split(" ")[0][0]
        varsta = self.text_varsta.toPlainText()
        permis = self.text_permis.toPlainText()
        valid = 0
        r_v = re.compile(r'[0-9]+')
        r_p = re.compile(r'.+')
        if re.fullmatch(r_v, varsta) and re.fullmatch(r_p, permis) and int(varsta) >= 16:
            valid = 1
        if valid == 1:
            if self.context == 1:
                try:
                    cursor = con.cursor()
                    cursor.execute("insert into conditii_arme values (\'{}\', \'{}\', \'{}\')"
                                   .format(id_arma, varsta, permis))
                    cursor.close()
                except cx_Oracle.DatabaseError as exc:
                    error, = exc.args
                    print("Oracle-Error-Code:", error.code)
                    print("Oracle-Error-Message:", error.message)
                self.load_data()
                super().salveaza()
                self.disable_text()
                self.button_salveaza.setEnabled(False)
                self.button_adauga.setEnabled(True)
                self.button_editeaza.setEnabled(True)
                self.button_sterge.setEnabled(True)
            elif self.context == 2:
                selected_row = self.table.currentRow()
                id_arma_old = self.table.item(selected_row, 0).text()
                varsta_old = self.table.item(selected_row, 1).text()
                permis_old = self.table.item(selected_row, 2).text()
                try:
                    cursor = con.cursor()
                    cursor.execute(
                        "update conditii_arme set id_arma = \'{}\', varsta_necesara = \'{}\', permis_necesar = \'{}\'"
                        " where id_arma = \'{}\' and varsta_necesara = \'{}\' and  permis_necesar = \'{}\'"
                            .format(id_arma, varsta, permis, id_arma_old, varsta_old, permis_old))
                    cursor.close()
                except cx_Oracle.DatabaseError as exc:
                    error, = exc.args
                    print("Oracle-Error-Code:", error.code)
                    print("Oracle-Error-Message:", error.message)
                self.load_data()
                super().salveaza()
                self.disable_text()
                self.button_salveaza.setEnabled(False)
                self.button_adauga.setEnabled(True)
                self.button_editeaza.setEnabled(True)
                self.button_sterge.setEnabled(True)
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Eroare")
            msg.setText(
                "Nu ati introdus un camp sau ati introdus un camp gresit!\n\nConstrangerile sunt:\n\tVarsta necesara: "
                "numar mai mare sau egal cu 16\n\tPermis necesar: un singur caracter")
            msg.exec_()

    def sterge(self):
        selected_row = self.table.currentRow()
        id_arma_old = self.table.item(selected_row, 0).text()
        varsta_old = self.table.item(selected_row, 1).text()
        permis_old = self.table.item(selected_row, 2).text()
        try:
            cursor = con.cursor()
            cursor.execute("delete from conditii_arme where id_arma = \'{}\' and varsta_necesara = \'{}\' and  "
                           "permis_necesar = \'{}\' ".format(id_arma_old, varsta_old, permis_old))
            cursor.close()
        except cx_Oracle.DatabaseError as exc:
            error, = exc.args
            print("Oracle-Error-Code:", error.code)
            print("Oracle-Error-Message:", error.message)
        self.load_data()
        super().sterge()
