# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'hpothes.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Protocole(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1277, 730)
        Form.setStyleSheet("")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(10, 680, 151, 38))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(1080, 680, 151, 38))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setGeometry(QtCore.QRect(0, 0, 1281, 91))
        self.label_8.setStyleSheet("background-color :rgb(180, 223, 255)")
        self.label_8.setObjectName("label_8")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(1100, 190, 161, 41))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(1100, 260, 161, 41))
        self.pushButton_4.setObjectName("pushButton_4")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(30, 110, 531, 41))
        self.label.setObjectName("label")
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(60, 190, 1011, 400))
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
        self.tableWidget.setColumnWidth(3, 150)
        self.tableWidget.setColumnWidth(2, 400)
        self.tableWidget.setColumnWidth(1, 150)
        self.tableWidget.setColumnWidth(0, 250)
        self.pushButton_3.clicked.connect(self._addRow)
        self.pushButton_4.clicked.connect(self._removeRow)
        self.ba = []
        self.uplets = {}
        self.save_protocol = {}
        self.prot_updateflag = True
        self.prot_update = {}
        self.numId = 0
        f = open ("button.css","r")
        cssb = f.read()
        f.close()
        self.pushButton.setStyleSheet(cssb)
        self.pushButton_2.setStyleSheet(cssb)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form) 

    def _addRow(self) :
        rowCount = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowCount )
        button = QtWidgets.QPushButton()
        combo2 = QtWidgets.QComboBox()
        combo2.addItem('Haut niveau')
        combo2.addItem('Bas niveau')
        self.tableWidget.setCellWidget(rowCount, 1, combo2)
        button.setText("Editer Actions")
        self.tableWidget.setCellWidget(rowCount, 3, button)
        self.ba.append(button)
        
    def _removeRow(self):
        current = self.tableWidget.currentRow()
        if (current==-1) :
            r = self.tableWidget.rowCount()
            if r > 0:
                button = self.ba[r-1]
                self.tableWidget.removeRow(r-1)
                if (button in self.save_protocol.keys()):
                    del self.save_protocol[button]
                if (button in self.uplets.keys()):
                    del self.uplets[button]
                self.ba.pop(r-1)
                if not self.prot_updateflag :
                    if r<=self.numId :
                        if button in self.prot_update.keys():
                            self.prot_update[button][1] = "DELETE"
        else :
            self.tableWidget.removeRow(current) 
            button = self.ba[current]
            if( button in self.save_protocol) :
                del self.save_protocol[button]
            if (button in self.uplets.keys()):
                del self.uplets[button]
            self.ba.pop(current)
            if not self.prot_updateflag :
                if button in self.prot_update.keys():
                    if current <self.numId :
                        self.prot_update[button][1] = "DELETE"

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "Retour"))
        self.pushButton_2.setText(_translate("Form", "Enregistrer"))
        self.label_8.setText(_translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:20pt; font-weight:600; color:#ffffff;\">EDITEUR DE CAS MEDICAUX HIPPOCRATE</span></p></body></html>"))
        self.pushButton_3.setText(_translate("Form", "Ajouter un protocole"))
        self.pushButton_4.setText(_translate("Form", "Supprimer un protocole"))
        self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:11pt;\">Veuillez formuler les protocoles résultant de votre hypothèse </span></p></body></html>"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Protocole"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Type"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Description"))
