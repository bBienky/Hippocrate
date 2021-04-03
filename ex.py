from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow
from addcase import Addcase
from menuprincipal import Menupricipal
from smp import Add_symptom
from PyQt5.QtCore import pyqtSlot
from hpothes import Hypothese
from Protocole import Protocole

class Menuprincipal_child(QMainWindow, Menupricipal):
    def __init__(self):
        super().__init__()
        self.addcase = Addcase_child()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.click_addcase)
    
    def click_addcase(self):
        if self.addcase.isVisible():
            self.addcase.hide()
        else :
            self.hide()
            self.addcase.show()

class Addcase_child(QMainWindow, Addcase):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.child = None
        self.pushButton.clicked.connect(self._back_menu)
        self.pushButton_2.clicked.connect(self._go_symptom)
        
    @pyqtSlot()
    def _back_menu(self) :
        self.displayUi = Menuprincipal_child()
        self.hide()
        self.displayUi.show()
        
    @pyqtSlot()
    def _go_symptom(self):
        if(self.child is None) :
            self.child =Addsymptom_child(self)
            self.displayUi = self.child
           
        else :
            self.displayUi = self.child
        self.hide()
        self.displayUi.show()

class Addsymptom_child(QMainWindow, Add_symptom):
    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)
        self.parent = parent
        self.child = None
        self.pushButton_3.clicked.connect(self._addRow)
        self.pushButton_4.clicked.connect(self._removeRow)
        self.pushButton.clicked.connect(self._back_case)
        self.pushButton_2.clicked.connect(self._go_hypothese)
       
    @pyqtSlot()
    def _back_case(self):
        self.displayUi = self.parent
        self.hide()
        self.displayUi.show()
    @pyqtSlot()
    def _go_hypothese(self):
        if(self.child is None) :
            self.child = Hypothese_child(self)
            self.displayUi = self.child
           
        else :
            self.displayUi = self.child
        self.hide()
        self.displayUi.show()


class Hypothese_child(QMainWindow, Hypothese) :
    def __init__(self,sparent) :
        super().__init__()
        self.setupUi(self)
        self.sparent = sparent
        self.pushButton.clicked.connect(self._back_symptom)
    @pyqtSlot()
    def _back_symptom(self):
        self.displayUi = self.sparent
        self.hide()
        self.displayUi.show()
    
    @pyqtSlot()
    def _go_protocole(self) :
        row = self.tableWidget.rowCount()
        col = 3
        for i in range(row):
            item = 

class Protocole_child(QMainWindow, Protocole) :
    def __init__(self, hparent):
        super().__init__()
        self.setupUi(self)
        self.hparent = hparent
    



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form =QMainWindow()
    app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    #ui1 = Addcase_child()
    #ui2 = Addsymptom_child(ui1)
    #ui3 = Hypothese_child(ui2)
    ui = Protocole()
    Form.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())