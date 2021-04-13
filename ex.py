from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow
from addcase import Addcase
from menuprincipal import Menupricipal
from smp import Add_symptom
from PyQt5.QtCore import pyqtSlot
from hpothes import Hypothese
from Protocole import Protocole
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem
from actions import Actions
from boucles import Boucle
from PyQt5.QtWidgets import QMessageBox
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from mapping_class import *
from help_func import *
engine = create_engine('sqlite:///hippocrate.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


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
        self.save_case = None
        self.pushButton.clicked.connect(self._back_menu)
        self.pushButton_2.clicked.connect(self._go_symptom)
        
    @pyqtSlot()
    def _back_menu(self) :
        self.displayUi = Menuprincipal_child()
        self.hide()
        self.displayUi.show()
        
    @pyqtSlot()
    def _go_symptom(self):
        name_patient = self.lineEdit.text()
        descr = self.textEdit.toPlainText()
        b1 =self.radioButton
        b2 = self.radioButton_2
        b3=self.radioButton_3
        b4 =self.radioButton_4
        age = self.comboBox.currentText()
        if ((name_patient != "") & (descr != "") & (b1.isChecked()|b2.isChecked()) & (b3.isChecked()|b4.isChecked())) :
            b11, b22 = '', ''
            if (b1.isChecked()) :
                b11 = b1.text()
            if (b2.isChecked()) :
                b11 = b1.text()
            if (b3.isChecked()) :
                b22 = b1.text()
            if (b4.isChecked()) :
                b22 = b1.text()
            self.save_case = Case(name_patient = name_patient, age_patient =age, gender_patient = b22, type_case =b11, desc_case= descr )
            if(self.child is None) :
                self.child =Addsymptom_child(self)
                self.displayUi = self.child
            else :
                self.displayUi = self.child
            self.hide()
            self.displayUi.show()
        else :
            error_dialog = QMessageBox()
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.setText("Remplissez tous les champs d Mettez N/A si non existant pour la description")
            error_dialog.exec_()
class Addsymptom_child(QMainWindow, Add_symptom):
    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)
        self.parent = parent
        self.child = None
        self.error_dialog = QMessageBox()
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
        row = self.tableWidget.rowCount()
        if row == 0:
            self.error_dialog.setIcon(QMessageBox.Critical)
            self.error_dialog.setText("Veuillez éditer tous les symptômes du patient avant de passer aux hypothèses")
            self.error_dialog.exec_()

        else :
            smp = []
            col1, col2, col3, col4 = self.tableWidget.item(row-1, 0), self.tableWidget.item(row-1, 1), self.tableWidget.item(row-1, 2), self.tableWidget.item(row-1, 3)
            if ( (col1 is None)|(col2 is None)|(col3 is None)|(col4 is None)) :
                self.error_dialog.setIcon(QMessageBox.Critical)
                self.error_dialog.setText("Remplissez tous les champs de la ligne " + str(row)+"\n Mettez N/A si non existant")
                self.error_dialog.exec_()
            else :
                for i in range(row):
                        smp.append(Symptom(name_symptom = self.tableWidget.item(i,0).text(), desc_symptom= self.tableWidget.item(i,1).text(),
                        type_symptom = self.tableWidget.item(i, 2).text(), val_symptom =self.tableWidget.item(i,3).text()))
                self.parent.save_case.symptoms = smp
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
        self.error_dialog =QMessageBox()
        self.pchild_list = {}
        self.counter = 0
        self.pushButton.clicked.connect(self._back_symptom)
        self.pushButton_2.clicked.connect(self._save_case_final)
    
    @pyqtSlot()
    def _save_case_final(self) :
        row =  self.tableWidget.rowCount()
        if (row ==0) :
            self.error_dialog.setIcon(QMessageBox.Critical)
            self.error_dialog.setText("Veuillez formuler au moins une hypothèse avant de sauvegarder le cas")
            self.error_dialog.exec_()
        else :
            if (len(self.save_hp2)<row):
                self.error_dialog.setIcon(QMessageBox.Critical)
                self.error_dialog.setText("Veuillez terminer d'éditer toutes les hypothèses avant de sauvegarder le cas")
                self.error_dialog.exec_()
            else :
                hp_list =[]
                for h in self.save_hp2.keys() :
                    hp_list.append(self.save_hp2[h])
                case = self.sparent.parent.save_case
                case.hypothesis_list = hp_list
                session.add(case)
                session.commit()

    @pyqtSlot()
    def _back_symptom(self):
        self.displayUi = self.sparent
        self.hide()
        self.displayUi.show()
    
    @pyqtSlot()
    def _go_protocole(self) :
        button = self.sender()
        index = self.tableWidget.indexAt(button.pos())
        n = index.row()
        hcol1, hcol2, hcol3 = self.tableWidget.item(n, 0), self.tableWidget.cellWidget(n, 1), self.tableWidget.item(n, 2)
        
        if((hcol1 is None)|(hcol2 is None)|(hcol3 is None)):
            self.error_dialog.setIcon(QMessageBox.Critical)
            self.error_dialog.setText("Veuillez saisir tous les champs avant l'édition des protocoles")
            self.error_dialog.exec_()
        else :
            if index.isValid():  
                self.save_hp[button] = Hypothesis(name_hypothesis = hcol1.text(), desc_hypothesis =hcol3.text(), true_false_hypothesis=true_false(hcol2.currentText()) )
                self.displayUi = self.pchild_list[button]
                self.hide()
                self.displayUi.show()
    @pyqtSlot()
    def _addRow(self) :
        row = self.tableWidget.rowCount()
        if (row<=0) :
            super()._addRow()
            self.pchild_list[self.bl[row]] = Protocole_child(self, self.bl[row])
            self.bl[0].clicked.connect(self._go_protocole)
        else : 
            
            if(len(self.save_hp)==row) :
                super()._addRow()
                self.pchild_list[self.bl[row]] = Protocole_child(self, self.bl[row])
                self.bl[row].clicked.connect(self._go_protocole)
            else :
                self.error_dialog.setIcon(QMessageBox.Critical)
                self.error_dialog.setText("Veuillez terminer l'édition de la ligne " + str(row))
                self.error_dialog.exec_()


class Protocole_child(QMainWindow, Protocole) :
    def __init__(self, hparent, button):
        super().__init__()
        self.setupUi(self)
        self.hparent = hparent
        self.action_list = {}
        self.hbcreate = button
        self.pushButton.clicked.connect(self._back_hp)
        self.error_dialog = QMessageBox()
        self.pushButton_2.clicked.connect(self._save_protocols)

    @pyqtSlot()
    def _back_hp(self) :
        self.displayUi = self.hparent
        self.hparent = self.hparent
        self.hide()
        self.displayUi.show()

    @pyqtSlot()
    def _save_protocols(self):
        if(len(self.uplets)==0):
            self.error_dialog.setIcon(QMessageBox.Critical)
            self.error_dialog.setText("Ajouter et éditer au moins un protocole avant de sauvegarder")
            self.error_dialog.exec_()
        else :
            if len(self.uplets) < self.tableWidget.rowCount() :
                self.error_dialog.setIcon(QMessageBox.Critical)
                self.error_dialog.setText("Veuillez terminer l'édition des actions de tous les protocoles ")
                self.error_dialog.exec_()
            else :
                for elem in self.uplets.keys() :
                    self.hparent.save_hp[self.hbcreate].protocol_list.append(self.uplets[elem])
                self.hparent.save_hp2[self.hbcreate] = self.hparent.save_hp[self.hbcreate]
                self.displayUi = self.hparent
                self.hide()
                self.displayUi.show()
    
    @pyqtSlot()
    def _go_action(self) :
        button = self.sender()
        index = self.tableWidget.indexAt(button.pos())
        p  = index.row()
        pcol1, pcol2, pcol3 = self.tableWidget.item(p, 0), self.tableWidget.cellWidget(p, 1),self.tableWidget.item(p, 2)
        if((pcol1 is None)|(pcol2 is None)|(pcol3 is None)):
            self.error_dialog.setIcon(QMessageBox.Critical)
            self.error_dialog.setText("Veuillez saisir tous les champs avant l'édition des actions")
            self.error_dialog.exec_()
        else :
            if index.isValid():       
                self.save_protocol[button] = Protocol(name_protocol = pcol1.text(), desc_protocol = pcol3.text(), type_protocol = pcol2.currentText())
                self.displayUi = self.action_list[button]
                self.hide()
                self.displayUi.show()
            
            
    @pyqtSlot()
    def _addRow(self) :
        row = self.tableWidget.rowCount()   
        if (row<=0) :
            super()._addRow()
            self.action_list[self.ba[row]] = Action_child(self, self.ba[row])
            self.ba[0].clicked.connect(self._go_action)
        else : 
            if(len(self.save_protocol)==row) :
                super()._addRow()
                self.action_list[self.ba[row]] = Action_child(self, self.ba[row])
                self.ba[row].clicked.connect(self._go_action)     
            else :
                self.error_dialog.setIcon(QMessageBox.Critical)
                self.error_dialog.setText("Veuillez terminer l'édition de la ligne " + str(row))
                self.error_dialog.exec_()                   



class Action_child(Actions, QMainWindow) :
    def __init__(self, pparent, button):
        super().__init__()
        self.setupUi(self)
        self.pparent = pparent
        self.bchild = None
        self.i = 0
        self.bcreate = button
        self.pushButton.clicked.connect(self._back_protocole)
        self.pushButton_4.clicked.connect(self._add_boucle)
        self.pushButton_2.clicked.connect(self._save_actions)
        self.error_dialog =QMessageBox()

    @pyqtSlot()
    def _add_action_row(self) :
        rowCount = self.tableWidget.rowCount()
        if (rowCount == 0):
            super()._add_action_row()
        else :
            item = self.tableWidget.item(rowCount-1, 0)
            if(item is None) :
                self.error_dialog.setIcon(QMessageBox.Critical)
                self.error_dialog.setText("Veuillez terminer l'édition de l'action précédente \n avant d'ajouter une nouvelle")
                self.error_dialog.exec_()
            else :
                super()._add_action_row()

        
    @pyqtSlot()
    def _back_protocole(self):
        print(self.bcreate)
        self.displayUi = self.pparent
        self.hide()
        self.displayUi.show()

    @pyqtSlot()
    def _add_boucle(self) :
        if(self.bchild is None) :
            self.bchild = Boucle_child(self)
            rowCount = self.tableWidget.rowCount()
            rowCount2 = self.bchild.tableWidget.rowCount()
            select_rows = self.tableWidget.selectedIndexes()
            n  = len(select_rows)
            if(n==0):
                self.error_dialog.setIcon(QMessageBox.Critical)
                self.error_dialog.setText("Veuillez sélectionner des actions")
                self.error_dialog.exec_()
            else :
                self.bchild.tableWidget.insertRow(rowCount)
                item1 = self.tableWidget.item(select_rows[0].row(), 0)
                item2 = self.tableWidget.item(select_rows[n-1].row(), 0)
                self.bchild.tableWidget.insertRow(rowCount2)
                self.displayUi = self.bchild
                if ((item1 is None)|(item2 is None)) :
                    self.error_dialog.setIcon(QMessageBox.Critical)
                    self.error_dialog.setText("Veuillez renseigner les champs des différents actions")
                    self.error_dialog.exec_()
                else :
                    self.i +=1
                    item = QTableWidgetItem("boucle d'action - "+str(self.i))
                    self.bchild.tableWidget.setItem(rowCount2,1,item1.clone())
                    self.bchild.tableWidget.setItem(rowCount2, 2, item2.clone())
                    self.bchild.tableWidget.setItem(rowCount2, 0, item)

                    self.hide()
                    self.displayUi.show()           
        else :
            self.displayUi = self.bchild
            select_rows = self.tableWidget.selectedIndexes()
            rowCount2 = self.bchild.tableWidget.rowCount()
            n = len(select_rows)
            if(n==0):
                if(rowCount2>0):
                    self.hide()
                    self.displayUi.show()
                else :
                    self.error_dialog.setIcon(QMessageBox.Critical)
                    self.error_dialog.setText("Veuillez sélectionner des actions")
                    self.error_dialog.exec_()

            else :
                item1 = self.tableWidget.item(select_rows[0].row(), 0)
                item2 = self.tableWidget.item(select_rows[n-1].row(), 0)
                self.displayUi = self.bchild
                if ((item1 is None)|(item2 is None)) :
                    self.error_dialog.setIcon(QMessageBox.Critical)
                    self.error_dialog.setText("Veuillez renseigner les champs des différents actions")
                    self.error_dialog.exec_()
                else :
                    self.i +=1
                    item = QTableWidgetItem("boucle d'action - "+str(self.i))
                    self.bchild.tableWidget.insertRow(rowCount2)
                    self.bchild.tableWidget.setItem(rowCount2, 0, item)
                    self.bchild.tableWidget.setItem(rowCount2,1,item1.clone())
                    self.bchild.tableWidget.setItem(rowCount2, 2, item2.clone())
                    self.hide()
                    self.displayUi.show()
    
    @pyqtSlot()
    def _save_actions(self):
        r = self.tableWidget.rowCount()
        if (r == 0):
            self.error_dialog.setIcon(QMessageBox.Critical)
            self.error_dialog.setText("Aucune action saisie \n Entrez au moins une action")
            self.error_dialog.exec_()
        else:
            act_all = []
            for row in range(self.tableWidget.rowCount()):
                act = []
                for col in range(self.tableWidget.columnCount()):
                    if ((col == 3) |(col == 5)|(col == 6)) :
                        _item = self.tableWidget.cellWidget(row, col) 
                    else :
                        _item = self.tableWidget.item(row, col) 
                    if _item:    
                        if ((col == 3) |(col == 5)|(col == 6)):
                            item =  self.tableWidget.cellWidget(row, col).currentText()
                        else :
                            item = self.tableWidget.item(row, col).text()
                        act.append(item)
                if (len(act) < self.tableWidget.columnCount()) :
                    self.error_dialog.setIcon(QMessageBox.Critical)
                    self.error_dialog.setText("Remplissez tous les champs de la ligne " + str(row +1)+"\n Mettez N/A si non existant")
                    self.error_dialog.exec_()
                else :
                    act_all.append((Action(name_action =act[0], desc_action = act[1],true_false_action=true_false(act[5]), order = act[6], precondition = act[4]),[act[2],act[3]]))   
            if(len(act_all)==self.tableWidget.rowCount()) :
                act_all = map_action_actor(act_all) 
                for val in act_all :
                    u = Uplet()
                    u.action_all = val[1]
                    temp = Actor(name = val[0][0], role_actor = val[0][1])
                    u.actors_all = temp
                    self.pparent.save_protocol[self.bcreate].actor_list.append(u)
                self.pparent.uplets[self.bcreate] = self.pparent.save_protocol[self.bcreate]
                self.displayUi = self.pparent
                self.hide()
                self.displayUi.show()


class Boucle_child(QMainWindow, Boucle) :
    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)
        self.parent =parent
        self.pushButton.clicked.connect(self._back_action)
    
    def _back_action(self):
        self.displayUi = self.parent
        self.hide()
        self.displayUi.show()




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form =QMainWindow()
    app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    ui1 = Menuprincipal_child()
    #ui = Boucle()
    Form.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
    ui1.setupUi(Form)
    ui1.show()
    sys.exit(app.exec_())