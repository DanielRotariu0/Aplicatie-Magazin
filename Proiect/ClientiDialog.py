import datetime

import cx_Oracle
from CustomDialog import *


class ClientiDialog(CustomDialog):
    def __init__(self):
        super().__init__("clienti")

    def load_data(self):
        clienti = []
        cursor = con.cursor()
        cursor.execute('select * from detalii_clienti order by id')
        for result in cursor:
            client = {'id': str(result[0]), 'nume': str(result[1]), 'prenume': str(result[2]), 'cnp': str(result[3]), 'adresa': str(result[4]),
                      'email': str(result[5]), 'data_inregistrare': str(result[6])}
            clienti.append(client)
        cursor.close()
        row = 0
        self.table.setRowCount(len(clienti))
        for client in clienti:
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(client["id"]))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(client["nume"]))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(client["prenume"]))
            self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(client["cnp"]))
            self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(client["adresa"]))
            self.table.setItem(row, 5, QtWidgets.QTableWidgetItem(client["email"]))
            data = datetime.datetime.strptime(client["data_inregistrare"]
                                              .split(" ")[0], "%Y-%m-%d").strftime("%d-%m-%Y")
            self.table.setItem(row, 6, QtWidgets.QTableWidgetItem(data))
            row = row + 1
        self.table.resizeColumnsToContents()

    def disable_text(self):
        self.text_nume.setPlainText("")
        self.text_prenume.setPlainText("")
        self.text_cnp.setPlainText("")
        self.text_adresa.setPlainText("")
        self.text_email.setPlainText("")
        self.text_data.setPlainText("")
        self.text_nume.setEnabled(False)
        self.text_prenume.setEnabled(False)
        self.text_cnp.setEnabled(False)
        self.text_adresa.setEnabled(False)
        self.text_email.setEnabled(False)
        self.text_data.setEnabled(False)

    def enable_text(self):
        self.text_nume.setEnabled(True)
        self.text_prenume.setEnabled(True)
        self.text_cnp.setEnabled(True)
        self.text_adresa.setEnabled(True)
        self.text_email.setEnabled(True)
        self.text_data.setEnabled(True)

    def editeaza(self):
        super().editeaza()
        selected_row = self.table.currentRow()
        self.id = self.table.item(selected_row, 0).text()
        self.text_nume.setPlainText(self.table.item(selected_row, 1).text())
        self.text_prenume.setPlainText(self.table.item(selected_row, 2).text())
        self.text_cnp.setPlainText(self.table.item(selected_row, 3).text())
        self.text_adresa.setPlainText(self.table.item(selected_row, 4).text())
        self.text_email.setPlainText(self.table.item(selected_row, 5).text())
        self.text_data.setPlainText(self.table.item(selected_row, 6).text())

    def salveaza(self):
        nume = self.text_nume.toPlainText()
        prenume = self.text_prenume.toPlainText()
        cnp = self.text_cnp.toPlainText()
        adresa = self.text_adresa.toPlainText()
        email = self.text_email.toPlainText()
        data = self.text_data.toPlainText()
        valid = 0
        r_n_p = re.compile(r'[a-zA-Z-*]{3,}')
        r_c = re.compile(r'[0-9]{13}')
        r_e = re.compile(r'[A-Za-z0-9._%-]+@[a-z0-9._%-]+\.[a-z]{2,4}')
        r_d = re.compile(r'[0-9]{2}-[0-9]{2}-[0-9]{4}')
        if re.fullmatch(r_n_p, nume) and re.fullmatch(r_n_p, prenume) and re.fullmatch(r_c, cnp):
            if re.fullmatch(r_e, email) and re.fullmatch(r_d, data):
                ds = data.split("-")
                if int(ds[2]) in range(1900, 2101) and int(ds[1]) in range(1, 13) and int(ds[0]) in range(1, 32):
                    valid = 1

        if valid == 1:
            if self.context == 1:
                found_ce = 0
                try:
                    cnp_new = str(cnp)
                    email_new = str(email)
                    cursor = con.cursor()
                    cursor.execute("select cnp from detalii_clienti")
                    for result in cursor:
                        cnp_o = str(result[0])
                        if cnp_new == cnp_o:
                            found_ce = 1
                    cursor.close()
                    cursor = con.cursor()
                    cursor.execute("select email from detalii_clienti")
                    for result in cursor:
                        email_o = str(result[0])
                        if email_o == email_new:
                            found_ce = 1
                    cursor.close()
                except cx_Oracle.DatabaseError as exc:
                    error, = exc.args
                    print("Oracle-Error-Code:", error.code)
                    print("Oracle-Error-Message:", error.message)

                if found_ce == 1:
                    msg = QMessageBox()
                    msg.setWindowTitle("Eroare")
                    msg.setText("CNP-ul si Email-ul trebuie sa fie unice.")
                    msg.exec_()
                else:
                    try:
                        cursor = con.cursor()
                        cursor.execute("select max(id) from detalii_clienti")
                        max_id = 0
                        for result in cursor:
                            max_id = result[0]
                        cursor.close()
                        cursor = con.cursor()
                        cursor.execute(
                            "insert into detalii_clienti values (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', "
                            "TO_DATE(\'{}\', \'DD-MM-YYYY\'))".format(max_id + 1, nume, prenume, cnp, adresa, email,
                                                                      data))
                        cursor.close()
                    except cx_Oracle.DatabaseError as exc:
                        error, = exc.args
                        print("Oracle-Error-Code:", error.code)
                        print("Oracle-Error-Message:", error.message)
                    self.button_salveaza.setEnabled(False)
                    self.button_adauga.setEnabled(True)
                    self.button_editeaza.setEnabled(True)
                    self.button_sterge.setEnabled(True)
                    self.disable_text()
                    self.load_data()
                    super().salveaza()
            elif self.context == 2:
                found_ce = 0
                try:
                    cnp_new = str(cnp)
                    email_new = str(email)
                    cursor = con.cursor()
                    cursor.execute("select cnp from detalii_clienti where id != {}".format(self.id))
                    for result in cursor:
                        cnp_o = str(result[0])
                        if cnp_new == cnp_o:
                            found_ce = 1
                    cursor.close()
                    cursor = con.cursor()
                    cursor.execute("select email from detalii_clienti where id != {}".format(self.id))
                    for result in cursor:
                        email_o = str(result[0])
                        if email_o == email_new:
                            found_ce = 1
                    cursor.close()
                except cx_Oracle.DatabaseError as exc:
                    error, = exc.args
                    print("Oracle-Error-Code:", error.code)
                    print("Oracle-Error-Message:", error.message)

                if found_ce == 1:
                    msg = QMessageBox()
                    msg.setWindowTitle("Eroare")
                    msg.setText("CNP-ul si Email-ul trebuie sa fie unice.")
                    msg.exec_()
                else:
                    found = 0
                    try:
                        data_new = datetime.datetime.strptime(data, "%d-%m-%Y")
                        cursor = con.cursor()
                        cursor.execute("select data from tranzactii where detalii_clienti_id = {}".format(self.id))
                        for result in cursor:
                            data_t = datetime.datetime.strptime(str(result[0]).split(" ")[0], "%Y-%m-%d")
                            if data_t < data_new:
                                found = 1
                        cursor.close()
                        cursor = con.cursor()
                        cursor.execute("select data_utilizare from log_poligon where detalii_clienti_id = {}".format(self.id))
                        for result in cursor:
                            data_t = datetime.datetime.strptime(str(result[0]).split(" ")[0], "%Y-%m-%d")
                            if data_t < data_new:
                                found = 1
                        cursor.close()
                    except cx_Oracle.DatabaseError as exc:
                        error, = exc.args
                        print("Oracle-Error-Code:", error.code)
                        print("Oracle-Error-Message:", error.message)
                    if found == 1:
                        msg = QMessageBox()
                        msg.setWindowTitle("Eroare")
                        msg.setText("Data inregistrarii nu poate fi mai mare decat data unei tranzactii.")
                        msg.exec_()
                    else:
                        try:
                            cursor = con.cursor()
                            cursor.execute("update detalii_clienti set nume = \'{}\', prenume = \'{}\', cnp = \'{}\', "
                                           "adresa = \'{}\', email = \'{}\', data_inregistrare = TO_DATE(\'{}\', "
                                           "\'DD-MM-YYYY\') where id = {}".format(nume, prenume, cnp, adresa, email,
                                                                                  data, self.id))
                            cursor.close()
                        except cx_Oracle.DatabaseError as exc:
                            error, = exc.args
                            print("Oracle-Error-Code:", error.code)
                            print("Oracle-Error-Message:", error.message)
                        self.button_salveaza.setEnabled(False)
                        self.button_adauga.setEnabled(True)
                        self.button_editeaza.setEnabled(True)
                        self.button_sterge.setEnabled(True)
                        self.disable_text()
                        self.load_data()
                        super().salveaza()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Eroare")
            msg.setText(
                "Nu ati introdus un camp sau ati introdus un camp gresit!\n\nConstrangerile sunt:\n\tNume: sir de "
                "caractere unic de lungime minima 3\n\tPrenume: sir de caractere de lungime minima 3\n\tCNP: sir de "
                "cifre unic de lungime 13\n\tEmail: de forma nume@exemplu.com\n\tData: format DD-MM-YYYY")
            msg.exec_()

    def sterge(self):
        selected_row = self.table.currentRow()
        self.id = self.table.item(selected_row, 0).text()
        found = 0
        try:
            cursor = con.cursor()
            cursor.execute("select detalii_clienti_id from tranzactii")
            for result in cursor:
                if self.id == str(result[0]):
                    found = 1
            cursor.close()

            cursor = con.cursor()
            cursor.execute("select detalii_clienti_id from log_poligon")
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
            msg.setText("Clientul nu poate fi sters deoarece apare intr-o tranzactie\n\tsau intr-o sedinta in cadrul "
                        "poligonului.")
            msg.exec_()
        else:
            try:
                cursor = con.cursor()
                cursor.execute("delete from detalii_clienti where id = {}".format(self.id))
                cursor.close()
            except cx_Oracle.DatabaseError as exc:
                error, = exc.args
                print("Oracle-Error-Code:", error.code)
                print("Oracle-Error-Message:", error.message)
            self.load_data()
            super().sterge()
