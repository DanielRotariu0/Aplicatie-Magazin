import sys
import re
import cx_Oracle
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *

con = cx_Oracle.connect("bd059", "bd059", "bd-dc.cs.tuiasi.ro:1539/orcl")


class CommitDialog(QDialog):
    def __init__(self, savepoint):
        super(QDialog, self).__init__()
        self.savepoint = savepoint
        loadUi("interface/commit.ui", self)
        self.setWindowTitle("Commit")
        self.button_da.clicked.connect(self.commit)
        self.button_nu.clicked.connect(self.rollback)

    def commit(self):
        cursor = con.cursor()
        cursor.execute('commit')
        cursor.close()
        self.hide()

    def rollback(self):
        cursor = con.cursor()
        cursor.execute('rollback to ' + self.savepoint)
        cursor.close()
        self.hide()
