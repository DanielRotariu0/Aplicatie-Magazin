import cx_Oracle
from CustomDialog import *


class MunitieDialog(CustomDialog):
    def __init__(self):
        super().__init__("munitie")

    def load_data(self):
        munitie = []
        cursor = con.cursor()
        cursor.execute('select * from munitie order by id')
        for result in cursor:
            m = {'id': str(result[0]), 'denumire': str(result[1]), 'tip': str(result[2])}
            munitie.append(m)
        cursor.close()
        row = 0
        self.table.setRowCount(len(munitie))
        for m in munitie:
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(m["id"]))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(m["denumire"]))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(m["tip"]))
            row = row + 1
        self.table.resizeColumnsToContents()

    def disable_text(self):
        self.text_denumire.setPlainText("")
        self.text_tip.setPlainText("")
        self.text_denumire.setEnabled(False)
        self.text_tip.setEnabled(False)

    def enable_text(self):
        self.text_denumire.setEnabled(True)
        self.text_tip.setEnabled(True)

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
            self.text_denumire.setPlainText(self.table.item(selected_row, 1).text())
            self.text_tip.setPlainText(self.table.item(selected_row, 2).text())

    def salveaza(self):
        denumire = self.text_denumire.toPlainText()
        tip = self.text_tip.toPlainText()
        valid = 0
        r_d = re.compile(r'.+')
        if re.fullmatch(r_d, denumire) and re.fullmatch(r_d, tip):
            valid = 1

        if valid == 1:
            if self.context == 1:
                try:
                    cursor = con.cursor()
                    cursor.execute("select max(id) from munitie")

                    max_id = 0
                    for result in cursor:
                        max_id = result[0]

                    cursor.close()

                    cursor = con.cursor()
                    cursor.execute(
                        "insert into munitie values (\'{}\', \'{}\', \'{}\')"
                            .format(max_id + 1, denumire, tip))
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
                try:
                    cursor = con.cursor()
                    cursor.execute(
                        "update munitie set denumire = \'{}\', tip = \'{}\'  where id = {}".format(denumire, tip,
                                                                                                   self.id))
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
                "Nu ati introdus un camp sau ati introdus un camp gresit!\n\nConstrangerile sunt:\n\tDenumire: "
                "sir de caractere\n\tTip: sir de caractere")
            msg.exec_()

    def sterge(self):
        selected_row = self.table.currentRow()
        self.id = self.table.item(selected_row, 0).text()
        found = 0
        try:
            cursor = con.cursor()
            cursor.execute("select munitie_id from tranzactii")
            for result in cursor:
                if self.id == str(result[0]):
                    found = 1
            cursor.close()
            cursor = con.cursor()
            cursor.execute("select munitie_id from arme")
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
            msg.setText("Munitia nu poate fi stearsa deoarece apare in tranzactii sau in arme.")
            msg.exec_()
        else:
            try:
                cursor = con.cursor()
                cursor.execute("delete from munitie where id = {}".format(self.id))
                cursor.close()
            except cx_Oracle.DatabaseError as exc:
                error, = exc.args
                print("Oracle-Error-Code:", error.code)
                print("Oracle-Error-Message:", error.message)
            self.load_data()
            super().sterge()
