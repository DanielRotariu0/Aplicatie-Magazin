import datetime

import cx_Oracle
from CustomDialog import *


class TranzactiiDialog(CustomDialog):
    def __init__(self):
        super().__init__("tranzactii")

    def load_data(self):
        self.comboBox_id_client.clear()
        self.comboBox_id_arma.clear()
        self.comboBox_id_munitie.clear()
        tranzactii = []
        cursor = con.cursor()
        cursor.execute('select * from tranzactii order by id')
        for result in cursor:
            tranzactie = {'id': str(result[0]), 'id_client': str(result[1]), 'id_arma': str(result[2]),
                          'bucati_arma': str(result[3]), 'id_munitie': str(result[4]),
                          'bucati_munitie': str(result[5]), 'data': str(result[6])}
            tranzactii.append(tranzactie)
        cursor.close()
        row = 0
        self.table.setRowCount(len(tranzactii))
        for tranzactie in tranzactii:
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(tranzactie["id"]))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(tranzactie["id_client"]))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(tranzactie["id_arma"]))
            self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(tranzactie["bucati_arma"]))
            self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(tranzactie["id_munitie"]))
            self.table.setItem(row, 5, QtWidgets.QTableWidgetItem(tranzactie["bucati_munitie"]))
            data = datetime.datetime.strptime(tranzactie["data"].split(" ")[0], "%Y-%m-%d").strftime("%d-%m-%Y")
            self.table.setItem(row, 6, QtWidgets.QTableWidgetItem(data))
            row = row + 1
        self.table.resizeColumnsToContents()
        clienti = []
        cursor = con.cursor()
        cursor.execute('select * from detalii_clienti')
        for result in cursor:
            client = {'id': str(result[0]), 'nume': str(result[1]), 'prenume': str(result[2]), 'cnp': str(result[3]),
                      'adresa': str(result[4]),
                      'email': str(result[5]), 'data_inregistrare': str(result[6])}
            clienti.append(client)
        cursor.close()
        for client in clienti:
            data = datetime.datetime.strptime(client["data_inregistrare"]
                                              .split(" ")[0], "%Y-%m-%d").strftime("%d-%m-%Y")
            option = client["id"] + ": " + client["nume"] + " " + client["prenume"] + " " + client["cnp"] + " " + \
                     client["adresa"] + " " + client["email"] + " " + data
            self.comboBox_id_client.addItem(option)
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
        self.text_bucati_arma.setPlainText("")
        self.text_bucati_munitie.setPlainText("")
        self.text_data.setPlainText("")
        self.text_bucati_arma.setEnabled(False)
        self.text_bucati_munitie.setEnabled(False)
        self.text_data.setEnabled(False)
        self.comboBox_id_client.setEnabled(False)
        self.comboBox_id_arma.setEnabled(False)
        self.comboBox_id_munitie.setEnabled(False)

    def enable_text(self):
        self.text_bucati_arma.setEnabled(True)
        self.text_bucati_munitie.setEnabled(True)
        self.text_data.setEnabled(True)
        self.comboBox_id_client.setEnabled(True)
        self.comboBox_id_arma.setEnabled(True)
        self.comboBox_id_munitie.setEnabled(True)

    def editeaza(self):
        super().editeaza()
        selected_row = self.table.currentRow()
        self.id = self.table.item(selected_row, 0).text()
        id_client = self.table.item(selected_row, 1).text()
        clienti = [self.comboBox_id_client.itemText(i) for i in range(self.comboBox_id_client.count())]
        for client in clienti:
            if client.split(" ")[0][0] == id_client:
                self.comboBox_id_client.setCurrentText(client)

        id_arma = self.table.item(selected_row, 2).text()
        arme = [self.comboBox_id_arma.itemText(i) for i in range(self.comboBox_id_arma.count())]
        for arma in arme:
            if arma.split(" ")[0][0] == id_arma:
                self.comboBox_id_arma.setCurrentText(arma)

        id_munitie = self.table.item(selected_row, 4).text()
        munitie = [self.comboBox_id_munitie.itemText(i) for i in range(self.comboBox_id_munitie.count())]
        for m in munitie:
            if m.split(" ")[0][0] == id_munitie:
                self.comboBox_id_munitie.setCurrentText(m)

        self.text_bucati_arma.setPlainText(self.table.item(selected_row, 3).text())
        self.text_bucati_munitie.setPlainText(self.table.item(selected_row, 5).text())
        self.text_data.setPlainText(self.table.item(selected_row, 6).text())

    def salveaza(self):
        id_client = self.comboBox_id_client.currentText().split(" ")[0][0]
        id_arma = self.comboBox_id_arma.currentText().split(" ")[0][0]
        id_munitie = self.comboBox_id_munitie.currentText().split(" ")[0][0]
        bucati_arma = self.text_bucati_arma.toPlainText()
        bucati_munitie = self.text_bucati_munitie.toPlainText()
        data = self.text_data.toPlainText()
        valid = 0
        r_b = re.compile(r'[0-9]*')
        r_d = re.compile(r'[0-9]{2}-[0-9]{2}-[0-9]{4}')
        if re.fullmatch(r_b, bucati_arma) and re.fullmatch(r_b, bucati_munitie):
            if re.fullmatch(r_d, data):
                ds = data.split("-")
                if int(ds[2]) in range(1900, 2101) and int(ds[1]) in range(1, 13) and int(ds[0]) in range(1, 32):
                    if not(int(bucati_munitie) == 0 and int(bucati_munitie) == 0) or\
                            not((int(id_arma) == 0 and int(bucati_arma) != 0) or (int(id_munitie) == 0 and int(bucati_munitie) != 0)):
                        valid = 1
        if valid == 1:
            found = 0
            try:
                data_new = datetime.datetime.strptime(data, "%d-%m-%Y")
                cursor = con.cursor()
                cursor.execute("select data_inregistrare from detalii_clienti where id = {}".format(id_client))
                for result in cursor:
                    data_t = datetime.datetime.strptime(str(result[0]).split(" ")[0], "%Y-%m-%d")
                    if data_t > data_new:
                        found = 1
                cursor.close()

            except cx_Oracle.DatabaseError as exc:
                error, = exc.args
                print("Oracle-Error-Code:", error.code)
                print("Oracle-Error-Message:", error.message)
            if found == 1:
                msg = QMessageBox()
                msg.setWindowTitle("Eroare")
                msg.setText("Data unei tranzactii nu poate fi mai mica decat data inregistrarii.")
                msg.exec_()
            else:
                if self.context == 1:
                    try:
                        cursor = con.cursor()
                        cursor.execute("select max(id) from tranzactii")
                        max_id = 0
                        for result in cursor:
                            max_id = result[0]
                        cursor.close()
                        cursor = con.cursor()
                        cursor.execute(
                            "insert into tranzactii values (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', "
                            "TO_DATE(\'{}\', \'DD-MM-YYYY\'))".format(max_id + 1, id_client, id_arma, bucati_arma,
                                                                      id_munitie, bucati_munitie, data))
                        cursor.close()
                    except cx_Oracle.DatabaseError as exc:
                        error, = exc.args
                        print("Oracle-Error-Code:", error.code)
                        print("Oracle-Error-Message:", error.message)
                    self.load_data()
                    self.disable_text()
                    self.button_salveaza.setEnabled(False)
                    self.button_adauga.setEnabled(True)
                    self.button_editeaza.setEnabled(True)
                    self.button_sterge.setEnabled(True)
                    super().salveaza()
                elif self.context == 2:
                    try:
                        cursor = con.cursor()
                        cursor.execute(
                            "update tranzactii set detalii_clienti_id = \'{}\', arme_id = \'{}\', bucati_arma = \'{}\',"
                            " munitie_id = \'{}\',bucati_munitie = \'{}\', data = TO_DATE(\'{}\', \'DD-MM-YYYY\') "
                            "where id = {}".format(id_client, id_arma, bucati_arma, id_munitie, bucati_munitie, data,
                                                   self.id))
                        cursor.close()
                    except cx_Oracle.DatabaseError as exc:
                        error, = exc.args
                        print("Oracle-Error-Code:", error.code)
                        print("Oracle-Error-Message:", error.message)
                    self.load_data()
                    self.disable_text()
                    self.button_salveaza.setEnabled(False)
                    self.button_adauga.setEnabled(True)
                    self.button_editeaza.setEnabled(True)
                    self.button_sterge.setEnabled(True)
                    super().salveaza()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Eroare")
            msg.setText(
                "Nu ati introdus un camp sau ati introdus un camp gresit!\n\nConstrangerile sunt:\n\tNr. Bucati Arma: "
                "numar\n\tNr. Bucati Munitie: numar\n\tData: format DD-MM-YYYY\n"
                "\n\tNr. Bucati Arma si Nr. Bucati Munitie nu pot fi ambele 0"
                "\n\tDaca Arma este 0, Nr. Bucati Arma trebuie sa fie 0"
                "\n\tDaca Munitie este 0, Nr. Bucati Munitie trebuie sa fie 0")
            msg.exec_()

    def sterge(self):
        super().sterge()
        selected_row = self.table.currentRow()
        self.id = self.table.item(selected_row, 0).text()
        try:
            cursor = con.cursor()
            cursor.execute("delete from tranzactii where id = {}".format(self.id))
            cursor.close()
        except cx_Oracle.DatabaseError as exc:
            error, = exc.args
            print("Oracle-Error-Code:", error.code)
            print("Oracle-Error-Message:", error.message)
        self.load_data()
