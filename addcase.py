# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addcase.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
from PyQt5 import QtCore, QtGui, QtWidgets
class Addcase(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        f = open ("button.css","r")
        cssb = f.read()
        f.close()
        Form.resize(973, 590)
        Form.setStyleSheet("")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(100, 110, 291, 31))
        self.label.setObjectName("label")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(130, 310, 291, 31))
        self.label_4.setObjectName("label_4")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(40, 530, 151, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setStyleSheet(cssb)
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(760, 530, 151, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setStyleSheet(cssb)
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setGeometry(QtCore.QRect(0, 0, 971, 91))
        self.label_8.setStyleSheet("background-color :rgb(180, 223, 255)")
        self.label_8.setObjectName("label_8")
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(190, 160, 581, 141))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setStyleSheet("font: 8pt \"Poppins\";")
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.radioButton = QtWidgets.QRadioButton(self.layoutWidget)
        self.radioButton.setObjectName("radioButton")
        self.gridLayout.addWidget(self.radioButton, 0, 1, 1, 1)
        self.radioButton_2 = QtWidgets.QRadioButton(self.layoutWidget)
        self.radioButton_2.setObjectName("radioButton_2")
        self.gridLayout.addWidget(self.radioButton_2, 0, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setStyleSheet("font: 8pt \"Poppins\";")
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.textEdit = QtWidgets.QTextEdit(self.layoutWidget)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 1, 1, 1, 2)
        self.layoutWidget1 = QtWidgets.QWidget(Form)
        self.layoutWidget1.setGeometry(QtCore.QRect(190, 360, 581, 151))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_5 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_5.setStyleSheet("font: 8pt \"Poppins\";")
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 0, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.layoutWidget1)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_2.addWidget(self.lineEdit, 0, 1, 1, 2)
        self.label_6 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_6.setStyleSheet("font: 8pt \"Poppins\";")
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 1, 0, 1, 1)
        self.radioButton_3 = QtWidgets.QRadioButton(self.layoutWidget1)
        self.radioButton_3.setObjectName("radioButton_3")
        self.gridLayout_2.addWidget(self.radioButton_3, 1, 1, 1, 1)
        self.radioButton_4 = QtWidgets.QRadioButton(self.layoutWidget1)
        self.radioButton_4.setObjectName("radioButton_4")
        self.gridLayout_2.addWidget(self.radioButton_4, 1, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_7.setStyleSheet("font: 8pt \"Poppins\";")
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 2, 0, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.layoutWidget1)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout_2.addWidget(self.comboBox, 2, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">Information sur le cas médical</span></p></body></html>"))
        self.label_4.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">Informations sur le patient</span></p></body></html>"))
        self.pushButton.setText(_translate("Form", "Annuler"))
        self.pushButton_2.setText(_translate("Form", "Suivant-Symptomes"))
        self.label_8.setText(_translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:20pt; font-weight:600; color:#ffffff;\">EDITEUR DE CAS MEDICAUX HIPPOCRATE</span></p></body></html>"))
        self.label_2.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:9pt;\">Type du cas</span></p></body></html>"))
        self.radioButton.setText(_translate("Form", "urgence"))
        self.radioButton_2.setText(_translate("Form", "normal"))
        self.label_3.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:9pt;\">Description du cas</span></p></body></html>"))
        self.label_5.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:9pt;\">Nom du patient</span></p></body></html>"))
        self.label_6.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:9pt;\">Genre du patient</span></p></body></html>"))
        self.radioButton_3.setText(_translate("Form", "Homme"))
        self.radioButton_4.setText(_translate("Form", "Femme"))
        self.label_7.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:9pt;\">Age du patient</span></p></body></html>"))

