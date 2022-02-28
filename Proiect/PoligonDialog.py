import datetime
import cx_Oracle
from CustomDialog import *


class PoligonDialog(CustomDialog):
    def __init__(self):
        super().__init__("poligon")

    def load_data(self):
        self.comboBox_id_client.clear()
        sedinte = []
        cursor = con.cursor()
        cursor.execute('select * from log_poligon order by id')
        for result in cursor:
            sedinta = {'id': str(result[0]), 'id_client': str(result[1]), 'data': str(result[2])}
            sedinte.append(sedinta)
        cursor.close()
        row = 0
        self.table.setRowCount(len(sedinte))
        for sedinta in sedinte:
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(sedinta["id"]))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(sedinta["id_client"]))
            data = datetime.datetime.strptime(sedinta["data"].split(" ")[0], "%Y-%m-%d").strftime("%d-%m-%Y")
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(data))
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

    def disable_text(self):
        self.text_data.setPlainText("")
        self.text_data.setEnabled(False)
        self.comboBox_id_client.setEnabled(False)

    def enable_text(self):
        self.text_data.setEnabled(True)
        self.comboBox_id_client.setEnabled(True)

    def editeaza(self):
        super().editeaza()
        selected_row = self.table.currentRow()
        self.id = self.table.item(selected_row, 0).text()
        id_client = self.table.item(selected_row, 1).text()
        clienti = [self.comboBox_id_client.itemText(i) for i in range(self.comboBox_id_client.count())]
        for client in clienti:
            if client.split(" ")[0][0] == id_client:
                self.comboBox_id_client.setCurrentText(client)
        self.text_data.setPlainText(self.table.item(selected_row, 2).text())

    def salveaza(self):
        id_client = self.comboBox_id_client.currentText().split(" ")[0][0]
        data = self.text_data.toPlainText()
        valid = 0
        r_d = re.compile(r'[0-9]{2}-[0-9]{2}-[0-9]{4}')
        if re.fullmatch(r_d, data):
            ds = data.split("-")
            if int(ds[2]) in range(1900, 2101) and int(ds[1]) in range(1, 13) and int(ds[0]) in range(1, 32):
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
                msg.setText("Data unei sedinte nu poate fi mai mica decat data inregistrarii.")
                msg.exec_()
            else:
                if self.context == 1:
                    try:
                        cursor = con.cursor()
                        cursor.execute("select max(id) from log_poligon")
                        max_id = 0
                        for result in cursor:
                            max_id = result[0]
                        cursor.close()
                        cursor = con.cursor()
                        cursor.execute("insert into log_poligon values (\'{}\', \'{}\', TO_DATE(\'{}\', "
                                       "\'DD-MM-YYYY\'))"
                                       .format(max_id + 1, id_client, data))
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
                            "update log_poligon set detalii_clienti_id = \'{}\', data_utilizare = TO_DATE(\'{}\', "
                            "\'DD-MM-YYYY\') where id = {}".format(id_client, data, self.id))
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
                "Nu ati introdus un camp sau ati introdus un camp gresit!\n\nConstrangerile sunt:"
                "\n\tData: format DD-MM-YYYY")
            msg.exec_()

    def sterge(self):
        selected_row = self.table.currentRow()
        self.id = self.table.item(selected_row, 0).text()
        try:
            cursor = con.cursor()
            cursor.execute("delete from log_poligon where id = {}".format(self.id))
            cursor.close()
        except cx_Oracle.DatabaseError as exc:
            error, = exc.args
            print("Oracle-Error-Code:", error.code)
            print("Oracle-Error-Message:", error.message)
        self.load_data()
        super().sterge()
