# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'boucles.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Boucle(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1221, 738)
        Form.setStyleSheet("")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(10, 680, 151, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(1010, 670, 151, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setGeometry(QtCore.QRect(0, 0, 1281, 91))
        self.label_8.setStyleSheet("background-color :rgb(180, 223, 255)")
        self.label_8.setObjectName("label_8")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(30, 110, 321, 41))
        self.label.setObjectName("label")
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(130, 150, 851, 411))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Poppins SemiBold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Poppins SemiBold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Poppins SemiBold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Poppins SemiBold")
        font.setPointSize(10)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(1010, 290, 151, 41))
        self.pushButton_3.setObjectName("pushButton_3")
        self.tableWidget.horizontalHeader().setDefaultSectionSize(200)
        self.tableWidget.setColumnWidth(3, 170)
        self.tableWidget.setColumnWidth(2, 210)
        self.tableWidget.setColumnWidth(1, 210)
        self.tableWidget.setColumnWidth(0, 200)
        self.boucle = []
        self.list_boucle = []
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def _removeRow(self):
        current = self.tableWidget.currentRow()
        row = self.tableWidget.rowCount()
        if (current==-1) :
            if  row > 0:
                self.boucle.pop(row-1)
                self.tableWidget.removeRow(row-1)
        else :
            self.boucle.pop(current)
            self.tableWidget.removeRow(current) 

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "Retour"))
        self.pushButton_2.setText(_translate("Form", "Enregistrer"))
        self.label_8.setText(_translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:20pt; font-weight:600; color:#ffffff;\">EDITEUR DE CAS MEDICAUX HIPPOCRATE</span></p></body></html>"))
        self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:11pt;\">Veuillez éditer la boucle d\'actions</span></p></body></html>"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Boucles"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Action initiale"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Action finale"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "Nbre d\'itérations"))
        self.pushButton_3.setText(_translate("Form", "Supprimer"))
