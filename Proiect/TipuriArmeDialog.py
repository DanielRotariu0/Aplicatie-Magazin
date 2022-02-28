import cx_Oracle
from CustomDialog import *


class TipuriArmeDialog(CustomDialog):
    def __init__(self):
        super().__init__("tipuri")

    def load_data(self):
        tipuri = []
        cursor = con.cursor()
        cursor.execute('select * from tipuri_arme order by id')
        for result in cursor:
            tip = {'id': str(result[0]), 'denumire': str(result[1])}
            tipuri.append(tip)
        cursor.close()
        row = 0
        self.table.setRowCount(len(tipuri))
        for tip in tipuri:
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(tip["id"]))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(tip["denumire"]))
            row = row + 1
        self.table.resizeColumnsToContents()

    def disable_text(self):
        self.text_denumire.setPlainText("")
        self.text_denumire.setEnabled(False)

    def enable_text(self):
        self.text_denumire.setEnabled(True)

    def editeaza(self):
        selected_row = self.table.currentRow()
        self.id = self.table.item(selected_row, 0).text()
        if int(self.id) == 0:
            msg = QMessageBox()
            msg.setWindowTitle("Eroare")
            msg.setText("Aceasta inregistrare nu poate fi modificata")
            msg.exec_()
        else:
            self.text_denumire.setPlainText(self.table.item(selected_row, 1).text())
            super().editeaza()

    def salveaza(self):
        denumire = self.text_denumire.toPlainText()
        valid = 0
        r_d = re.compile(r'.+')
        if re.fullmatch(r_d, denumire):
            valid = 1
        if valid == 1:
            if self.context == 1:
                try:
                    cursor = con.cursor()
                    cursor.execute("select max(id) from tipuri_arme")
                    max_id = 0
                    for result in cursor:
                        max_id = result[0]
                    cursor.close()
                    cursor = con.cursor()
                    cursor.execute(
                        "insert into tipuri_arme values (\'{}\', \'{}\')"
                            .format(max_id + 1, denumire))
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
                        "update tipuri_arme set denumire = \'{}\' where id = {}".format(denumire, self.id))
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
                "sir de caractere")
            msg.exec_()

    def sterge(self):
        selected_row = self.table.currentRow()
        self.id = self.table.item(selected_row, 0).text()
        found = 0
        try:
            cursor = con.cursor()
            cursor.execute("select tipuri_arme_id from arme")
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
            msg.setText("Tipul nu poate fi sters deoarece apare in arme.")
            msg.exec_()
        else:
            try:
                cursor = con.cursor()
                cursor.execute("delete from tipuri_arme where id = {}".format(self.id))
                cursor.close()
            except cx_Oracle.DatabaseError as exc:
                error, = exc.args
                print("Oracle-Error-Code:", error.code)
                print("Oracle-Error-Message:", error.message)
            self.load_data()
            super().sterge()
