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
from modif_case import *
from sqlalchemy.pool import NullPool
engine = create_engine('sqlite:///hippocrate.db', poolclass=NullPool)

class model :
    def __init__(self, eng):
        self.engine = eng
        self.session  = None
    def create_session(self) :
        self.engine.dispose()
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session = Session()
        return self.session

class Modif_case_child(Modif_case, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.case_list = []
        self.link_button ={}
        self.blist = []
        self.case_map ={}
        self.session = model(engine).create_session()
        self.pushButton_3.clicked.connect(self._back)
    def _back(self):
        self.displayUi = Menuprincipal_child()
        self.hide()
        self.displayUi.show()
        self.session.close()
    @pyqtSlot()    
    def _load_page(self) :
        n = len(self.case_list)
        for i in range(n):
            c = self.case_list[i]
            info = c.name_patient +" - "+ str(c.age_patient) + " - "+ c.gender_patient
            h = c.hypothesis_list
            h = [e.name_hypothesis for e in h]
            button = QtWidgets.QPushButton()
            item = QTableWidgetItem(info)
            item2 = QTableWidgetItem(transform(h))
            button.setText("Modifier")
            self.tableWidget.insertRow(i)
            self.tableWidget.setCellWidget(i, 2, button)
            self.tableWidget.setItem(i, 1, item)
            self.tableWidget.setItem(i, 0, item2)
            self.blist.append(button)
            self.link_button[button] = Addcase_child()
            self.case_map[button] = c
            self.blist[i].clicked.connect(self._go_case)


    def load_case_editor(self):
        for i in range(len(self.blist)):
            button = self.blist[i]
            interface = self.link_button[button]
            case = self.case_list[i]
            if (case.type_case =='Urgence'):
                interface.radioButton.setChecked(True)
            if (case.type_case =='Normal') :
                interface.radioButton_2.setChecked(True)
            if (case.gender_patient =='Homme'):
                interface.radioButton_3.setChecked(True)
            if (case.gender_patient =='Femme') :
                interface.radioButton_4.setChecked(True)
            interface.lineEdit.setText(case.name_patient)
            interface.comboBox.setCurrentIndex(case.age_patient-1)
            interface.textEdit.setPlainText(case.desc_case)
          

    @pyqtSlot()
    def _go_case (self) :
        #declarations
        button = self.sender()
        hlist = self.case_map[button].hypothesis_list
        self.displayUi = self.link_button[button]
        lcase = self.link_button[button]
        lcase.save_case = self.case_map[button]
        lcase.child = Addsymptom_child(lcase, load_h=hlist)
        lcase.child.flag =  True
        lsmp = lcase.child
        lsmp.fulltable(self.case_map[button].symptoms) 
        lsmp.updateID = [s.id for s in self.case_map[button].symptoms]
        lsmp.updatelen = len(self.case_map[button].symptoms)   
        lsmp.child = Hypothese_child(lsmp, flag = True)  
        lsmp.child.updateflag = False
        lsmp.child.id_tosave = self.case_map[button].id
        self.hide()
        self.displayUi.show()


class Del_case(Modif_case, QMainWindow) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.case_list = []
        self.link_button ={}
        self.blist = []
        self.case_map ={}
        self.pushButton_3.clicked.connect(self._back)
        self.session = model(engine).create_session()
    def _back(self):
        self.displayUi = Menuprincipal_child()
        self.hide()
        self.displayUi.show()
        self.session.close()
    def _load_page(self) :
        n = len(self.case_list)
        for i in range(n):
            c = self.case_list[i]
            info = c.name_patient +" - "+ str(c.age_patient) + " - "+ c.gender_patient
            h = c.hypothesis_list
            h = [e.name_hypothesis for e in h]
            button = QtWidgets.QPushButton()
            item = QTableWidgetItem(info)
            item2 = QTableWidgetItem(transform(h))
            button.setText("Supprimer")
            self.tableWidget.insertRow(i)
            self.tableWidget.setCellWidget(i, 2, button)
            self.tableWidget.setItem(i, 1, item)
            self.tableWidget.setItem(i, 0, item2)
            self.blist.append(button)
            self.case_map[button]=c
            self.blist[i].clicked.connect(self._delete)
    @pyqtSlot()
    def _delete(self):
        button = self.sender()
        case = self.case_map[button]
        self.session.flush()
        self.session.delete(case)
        self.session.commit()
        self.session.close()
        self.displayUi = Menuprincipal_child()
        self.hide()
        self.displayUi.show()


class Menuprincipal_child(QMainWindow, Menupricipal):
    def __init__(self):
        super().__init__()
        self.addcase = Addcase_child()
        self.modifcase = Modif_case_child()
        self.delcase = Del_case()
        self.setupUi(self)
        self.pushButton.clicked.connect(self._click_addcase)
        self.pushButton_2.clicked.connect(self._click_modif_case)
        self.pushButton_3.clicked.connect(self._click_delete)
    
    @pyqtSlot()
    def _click_addcase(self):
        if self.addcase.isVisible():
            self.addcase.hide()
        else :
            self.hide()
            self.addcase.show()
    @pyqtSlot()
    def _click_modif_case(self):
        session = self.modifcase.session 
        case_result = session.query(Case).all()
        self.modifcase.case_list = case_result
        self.modifcase._load_page()
        self.modifcase.load_case_editor()
        if self.modifcase.isVisible():
            self.modifcase.hide()
        else :
            self.hide()
            self.modifcase.show()
    @pyqtSlot()
    def _click_delete(self) :
        session =self.delcase.session
        case_result = session.query(Case).all()
        print(session)
        self.delcase.case_list = case_result
        self.delcase._load_page()
        if self.delcase.isVisible():
            self.delcase.hide()
        else :
            self.hide()
            self.delcase.show()
           

class Addcase_child(QMainWindow, Addcase):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.child = None
        self.save_case = None
        self.infos =[]
        self.pushButton.clicked.connect(self._back_menu)
        self.pushButton_2.clicked.connect(self._go_symptom)
        self.model = model(engine)
        self.session = self.model.create_session()
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
                b11 = b2.text()
            if (b3.isChecked()) :
                b22 = b3.text()
            if (b4.isChecked()) :
                b22 = b4.text()
            if self.save_case is None :
                self.save_case = Case(name_patient = name_patient, age_patient =age, gender_patient = b22, type_case =b11, desc_case= descr )
            self.infos =[name_patient, age, b22,b11, descr]
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
    def __init__(self, parent, load_h = None):
        super().__init__()
        self.setupUi(self)
        self.parent = parent
        self.child = None
        self.flag = False
        self.updateID = []
        self.load_h = load_h
        self.updatelen = 0
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
    
    def fulltable(self, mtable) :
        for i in range(len(mtable)):
            row = mtable[i]
            self.tableWidget.insertRow(i)
            item1, item2, item3, item4 = QTableWidgetItem(row.name_symptom), QTableWidgetItem(row.type_symptom), QTableWidgetItem(row.desc_symptom), QTableWidgetItem(row.val_symptom)
            self.tableWidget.setItem(i, 0, item1)
            self.tableWidget.setItem(i, 1, item2)
            self.tableWidget.setItem(i, 2, item3)
            self.tableWidget.setItem(i, 3, item4)

    
    @pyqtSlot()
    def _go_hypothese(self):
        if(self.flag) :
            self.child.fullhtable(self.load_h)
            self.flag = False
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
                if self.updatelen <= 0:
                    for i in range(row):                     
                            smp.append(Symptom(name_symptom = self.tableWidget.item(i,0).text(), desc_symptom= self.tableWidget.item(i,1).text(),
                            type_symptom = self.tableWidget.item(i, 2).text(), val_symptom =self.tableWidget.item(i,3).text()))
                    self.parent.save_case.symptoms = smp
                else :
                    session = self.parent.session
                   
                    if row == self.updatelen :
                        for i in range(row):
                            session.query(Symptom).filter(Symptom.id == self.updateID[i]).update({Symptom.name_symptom : self.tableWidget.item(i,0).text(), Symptom.desc_symptom : self.tableWidget.item(i,1).text(),
                                Symptom.type_symptom : self.tableWidget.item(i, 2).text(), Symptom.val_symptom  : self.tableWidget.item(i,3).text()})
                            session.commit()
                    if row < self.updatelen :
                        for i in range(row):
                            session.query(Symptom).filter(Symptom.id == self.updateID[i]).update({Symptom.name_symptom : self.tableWidget.item(i,0).text(), Symptom.desc_symptom : self.tableWidget.item(i,1).text(),
                                Symptom.type_symptom : self.tableWidget.item(i, 2).text(), Symptom.val_symptom  : self.tableWidget.item(i,3).text()})
                            session.commit()
                        for j in range(row, self.updatelen):
                            x = session.query(Symptom).get(self.updateID[j])
                            session.delete(x)
                            session.commit()                          
                    if row > self.updatelen :
                        for i in range(self.updatelen):
                            session.query(Symptom).filter(Symptom.id == self.updateID[i]).update({Symptom.name_symptom : self.tableWidget.item(i,0).text(), Symptom.desc_symptom : self.tableWidget.item(i,1).text(),
                                Symptom.type_symptom : self.tableWidget.item(i, 2).text(), Symptom.val_symptom  : self.tableWidget.item(i,3).text()})
                            session.commit()
                        for j in range(self.updatelen, row):
                            print(j)
                            s = Symptom(name_symptom = self.tableWidget.item(j,0).text(), desc_symptom= self.tableWidget.item(j,1).text(),
                                                type_symptom = self.tableWidget.item(j, 2).text(), val_symptom =self.tableWidget.item(j,3).text())
                            s.case_id = self.parent.save_case.id 
                            session.add(s)
                            session.commit()                    
                if(self.child is None) :
                    self.child = Hypothese_child(self)
                    self.displayUi = self.child          
                else :
                    self.displayUi = self.child
                self.hide()
                self.displayUi.show()


class Hypothese_child(QMainWindow, Hypothese) :
    def __init__(self,sparent, flag = False) :
        super().__init__()
        self.setupUi(self)
        self.sparent = sparent
        self.error_dialog =QMessageBox()
        self.pchild_list = {}
        self.counter = 0
        self.id_tosave =None
        self.updateflag = True
        self.load_p = {}
        self.flag= flag
        self.pushButton.clicked.connect(self._back_symptom)
        self.pushButton_2.clicked.connect(self._save_case_final)
    
    @pyqtSlot()
    def _save_case_final(self) :
        row =  self.tableWidget.rowCount()
        n = len(self.save_hp2)
        if not self.updateflag :
            n = len(self.save_hp)
        if (row ==0) :
            self.error_dialog.setIcon(QMessageBox.Critical)
            self.error_dialog.setText("Veuillez formuler au moins une hypothèse avant de sauvegarder le cas")
            self.error_dialog.exec_()
        else :
            if (n<row):
                self.error_dialog.setIcon(QMessageBox.Critical)
                self.error_dialog.setText("Veuillez terminer d'éditer toutes les hypothèses avant de sauvegarder le cas")
                self.error_dialog.exec_()
            else :
                hp_list =[]
                for h in self.save_hp2.keys() :
                    hp_list.append(self.save_hp2[h])
                case = self.sparent.parent.save_case
                session = self.sparent.parent.session
                if self.updateflag :
                    case.hypothesis_list = hp_list
                    session.add(case)
                    session.commit()
                else :
                    for elem in self.save_hp.keys() :
                        if elem in self.hupdate.keys() :
                            temp = self.hupdate[elem]
                            hid =temp[0]
                            actodo = temp[1]
                            print(actodo)
                            if actodo == "UPDATE" :
                                index = temp[2]
                                hcol1, hcol2, hcol3 = self.tableWidget.item(index, 0), self.tableWidget.cellWidget(index, 1), self.tableWidget.item(index, 2)      
                                session.query(Hypothesis).filter(Hypothesis.id==hid).update({Hypothesis.name_hypothesis : hcol1.text(), Hypothesis.desc_hypothesis :hcol3.text(),
                                         Hypothesis.true_false_hypothesis : true_false(hcol2.currentText())})
                                session.commit()
                            if actodo == "DELETE" :         
                                x = session.query(Hypothesis).get(hid)
                                session.delete(x)
                                session.commit()
                        else :
                            hp = self.save_hp[elem]
                            hp.case_id =case.id
                            session.add(hp)
                            session.commit()
                    infos = self.sparent.parent.infos
                    session.query(Case).filter(Case.id ==self.id_tosave).update({Case.name_patient:infos[0],Case.age_patient:infos[1],
                                            Case.gender_patient:infos[2], Case.type_case : infos[3], Case.desc_case :infos[4]},synchronize_session=False)
                    session.commit()
                session.close()
                self.sparent.parent.model.engine.dispose()
                self.displayUi = Menuprincipal_child()
                self.hide()
                self.displayUi.show()

    def fullhtable(self, htable = None,  load_p = None):
        if (htable is not None):
            self.pushButton_2.setText('Mettre à jour')
            for i in range(len(htable)) :
                row = htable[i]
                self.tableWidget.insertRow(i)
                item1, item2, item3 = QTableWidgetItem(row.name_hypothesis),  QtWidgets.QComboBox(), QTableWidgetItem(row.desc_hypothesis)
                item4 = QtWidgets.QPushButton()
                item2.addItem("Faux")
                item2.addItem("Vrai")
                item2.setCurrentText(detransform(row.true_false_hypothesis))
                item4.setText('Protocoles')
                self.tableWidget.setItem(i, 0, item1)
                self.tableWidget.setCellWidget(i, 1, item2)
                self.tableWidget.setItem(i, 2, item3)
                self.tableWidget.setCellWidget(i, 3, item4)
                self.bl.append(item4)
                self.load_p[self.bl[i]] = htable[i].protocol_list
                self.save_hp[item4] = htable[i]
                self.hupdate[item4] = [htable[i].id, 'UPDATE', i]
                self.pchild_list[self.bl[i]] = Protocole_child(hparent=self, button= self.bl[i], flag=True)
                self.pchild_list[self.bl[i]].numId = len(htable[i].protocol_list)
                self.pchild_list[self.bl[i]].hid = row.id
                self.pchild_list[self.bl[i]].prot_updateflag = False
                self.bl[i].clicked.connect(self._go_protocole)

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
        if (self.flag) & (self.pchild_list[button].flag2):
            if (button in self.load_p.keys()) :
                self.pchild_list[button].fullptable(self.load_p[button])

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
    def __init__(self, hparent, button, flag=False):
        super().__init__()
        self.setupUi(self)
        self.hparent = hparent
        self.action_list = {}
        self.hbcreate = button
        self.load_a = {}
        self.flag = flag
        self.flag2 = True
        self.hid = 0
        self.pushButton.clicked.connect(self._back_hp)
        self.error_dialog = QMessageBox()
        self.pushButton_2.clicked.connect(self._save_protocols)

    def fullptable (self, ptable =None ): 
        if (ptable is not None):
            for i in range(len(ptable)) :
                row = ptable[i]
                self.tableWidget.insertRow(i)
                item1, item2, item3 = QTableWidgetItem(row.name_protocol),  QtWidgets.QComboBox(), QTableWidgetItem(row.desc_protocol)
                item4 = QtWidgets.QPushButton()
                item2.addItem("Haut niveau")
                item2.addItem("Bas niveau")
                item2.setCurrentText(row.type_protocol)
                item4.setText('Modifier Actions')
                self.ba.append(item4)
                self.tableWidget.setItem(i, 0, item1)
                self.tableWidget.setCellWidget(i, 1, item2)
                self.tableWidget.setItem(i, 2, item3)
                self.tableWidget.setCellWidget(i, 3, item4)
                self.action_list[self.ba[i]] = Action_child(self, self.ba[i])
                self.action_list[self.ba[i]].update_create_flag = False
                session = self.hparent.sparent.parent.session
                uplets = session.query(Uplet).filter(Uplet.protocol_id==row.id).all()
                self.prot_update[item4] = [row, "UPDATE", i]
                f = []
                for u in uplets :
                    r1 = session.query(Actor).join(Uplet).filter(Actor.id==u.actor_id).all()
                    r2 = u.action_all
                    for ac in r2 :
                        p = [ac.name_action, ac.desc_action, r1[0].name, r1[0].role_actor, ac.precondition,ac.true_false_action, ac.order, ac.boucle_id, ac.id, r1[0].id, u.protocol_id]
                        f.append(p)
                self.load_a[item4] = f
                self.save_protocol[item4] = row
                self.ba[i].clicked.connect(self._go_action) 
                self.action_list[self.ba[i]].nId = len(f)
            self.flag2 = False

    @pyqtSlot()
    def _back_hp(self) :
        self.displayUi = self.hparent
        self.hparent = self.hparent
        self.hide()
        self.displayUi.show()

    @pyqtSlot()
    def _save_protocols(self):
        n = 0
        if self.prot_updateflag :
            n =len(self.uplets)
        else :
            n = len(self.save_protocol)
        if(n==0):
            self.error_dialog.setIcon(QMessageBox.Critical)
            self.error_dialog.setText("Ajouter et éditer au moins un protocole avant de sauvegarder")
            self.error_dialog.exec_()
        else :
            if n < self.tableWidget.rowCount() :
                self.error_dialog.setIcon(QMessageBox.Critical)
                self.error_dialog.setText("Veuillez terminer l'édition des actions de tous les protocoles ")
                self.error_dialog.exec_()
            else :
                if (not self.prot_updateflag) :
                    session = self.hparent.sparent.parent.session
                    for elem in self.prot_update.keys():
                        if self.prot_update[elem][1]=="UPDATE":
                            currentprot = self.prot_update[elem][0]
                            row = self.prot_update[elem][2]
                            p1,p2,p3 = self.tableWidget.item(row, 0), self.tableWidget.cellWidget(row, 1),self.tableWidget.item(row, 2)
                            session.query(Protocol).filter(Protocol.id==currentprot.id).update({Protocol.name_protocol:p1.text(),
                                Protocol.desc_protocol:p3.text(), Protocol.type_protocol : p2.currentText()})
                            session.commit()         
                        else :
                            x = session.query(Protocol).get(self.prot_update[elem][0].id)
                            session.delete(x) 
                            session.commit()
                    if len(self.uplets)>0 :
                        for elem in self.uplets.keys():
                            p = self.uplets[elem]
                            p.hpothes_id = self.hid
                            session.add(p)
                            session.commit()
                else:
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
        if (self.flag) & (self.action_list[button].flag2):
            if button in self.load_a :
                self.action_list[button].fullatable(self.load_a[button])
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
            if (not self.prot_updateflag) :
                self.action_list[self.ba[row]].update_create_flag = True
            self.ba[0].clicked.connect(self._go_action)
        else : 
            if(len(self.save_protocol)==row) :
                super()._addRow()
                self.action_list[self.ba[row]] = Action_child(self, self.ba[row])
                if not self.prot_updateflag :
                    self.action_list[self.ba[row]].update_create_flag = True
                self.ba[row].clicked.connect(self._go_action)     
            else :
                self.error_dialog.setIcon(QMessageBox.Critical)
                self.error_dialog.setText("Veuillez terminer l'édition de la ligne " + str(row))
                self.error_dialog.exec_()                   

class Action_child(Actions, QMainWindow) :
    def __init__(self, pparent, button, flag = False):
        super().__init__()
        self.setupUi(self)
        self.pparent = pparent
        self.bchild = None
        self.bcreate = button
        self.flag = flag
        self.flag2 =  True
        self.update_create_flag = True
        self.i = 0
        self.load_b = []
        self.nId = 0
        self.delete =[]
        self.update_flag_act =[]
        self.uplid =[]
        self.counter= 0
        self.error_dialog =QMessageBox()
        self.pushButton.clicked.connect(self._back_protocole)
        self.pushButton_4.clicked.connect(self._add_boucle)
        self.pushButton_2.clicked.connect(self._save_actions)
        self.pushButton_5.clicked.connect(self._removeRow)


    def fullatable (self, atable = None):
        if (atable is not None):
            for i in range(len(atable)) :
                self.tableWidget.insertRow(i)
                row = atable[i]
                l = [-20, -19, -18,-17, -16, -15, -14, -13, -12, -11, -10,  -9,  -8,  -7,  -6, 
                    -5, -4,  -3,  -2,   1,   2,   3,   4,   5,   6, 
                7,   8, 9,  10,  11,  12,  13,  14,  15,  16,  17,  18,  19, 20]
                l = [str(x) for x in l ]
                i1,i2,i3,i4,i5 = QTableWidgetItem(row[0]), QTableWidgetItem(row[1]), QTableWidgetItem(row[2]), QtWidgets.QComboBox(), QTableWidgetItem(row[4])
                i6,i7 = QtWidgets.QComboBox(), QtWidgets.QComboBox()
                i4.addItems(['Médécin', 'Infirmier', 'Ambulancier'])
                i6.addItem("Vrai")
                i6.addItem("Faux")
                i7.addItems(l)
                i4.setCurrentText(row[3])
                i6.setCurrentText(detransform(row[5]))
                i7.view().setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
                i7.setStyleSheet("QComboBox {combobox-popup: 0;}")
                i7.setCurrentIndex(i7.findText(str(row[6]), QtCore.Qt.MatchFixedString))
                self.tableWidget.setItem(i, 0, i1)
                self.tableWidget.setItem(i, 1, i2)
                self.tableWidget.setItem(i, 2, i3)
                self.tableWidget.setCellWidget(i, 3, i4)
                self.tableWidget.setItem(i, 4, i5)
                self.tableWidget.setCellWidget(i, 5, i6)
                self.tableWidget.setCellWidget(i, 6, i7)
                self.delete.append(row[8])
                self.update_flag_act.append([row[8], i, "UPDATE", row[9]])
                self.uplid.append(row[10])
                if (row[7] is not None) :
                    self.load_b.append(row[7])
            if (len(self.load_b) >0) :
                self.bchild = Boucle_child(self)     
                self.bchild.fullbtable(self.load_b)    
            self.flag2 =  False
            

    @pyqtSlot()
    def _add_action_row(self) :
        rowCount = self.tableWidget.rowCount()
        if (rowCount == 0):
            super()._add_action_row()
            if ( not self.update_create_flag) :
                self.update_flag_act.append([0, "ADD"])
        else :
            item = self.tableWidget.item(rowCount-1, 0)
            if(item is None) :
                self.error_dialog.setIcon(QMessageBox.Critical)
                self.error_dialog.setText("Veuillez terminer l'édition de l'action précédente \n avant d'ajouter une nouvelle")
                self.error_dialog.exec_()
            else :
                super()._add_action_row()
                if (not self.update_create_flag) :
                    self.update_flag_act.append([rowCount, "ADD"])
    @pyqtSlot()
    def _removeRow(self):
        current = self.tableWidget.currentRow()
        row = self.tableWidget.rowCount()
        if (current==-1) :
            if  row > 0:
                self.tableWidget.removeRow(row-1)
                if( not self.update_create_flag) :
                    if self.nId>=row :
                        a =self.delete[row-1]
                        self.update_flag_act[row-1]= [a, row-1, "DELETE"]
                        self.delete.pop(row-1)
                    else :
                        del self.update_flag_act[row-1]
                   
        else :
            self.tableWidget.removeRow(current) 
            if(not self.update_create_flag) :
                if self.nId>=row :
                    if current <len(self.delete):
                        a =self.delete[current]
                        self.update_flag_act[current+self.counter] = [a, current, "DELETE"]
                        self.delete.pop(current)
                        self.counter +=1
                else :
                    del self.update_flag_act[current]
 
    @pyqtSlot()
    def _back_protocole(self):
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
                    self.bchild.tableWidget.setItem(rowCount2, 3, QTableWidgetItem("2"))
                    self.bchild.boucle.append([select_rows[0].row(), select_rows[n-1].row()])
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
                    item3 =  QTableWidgetItem("2")
                    self.bchild.tableWidget.insertRow(rowCount2)
                    self.bchild.tableWidget.setItem(rowCount2, 0, item)
                    self.bchild.tableWidget.setItem(rowCount2,1,item1.clone())
                    self.bchild.tableWidget.setItem(rowCount2, 2, item2.clone())
                    self.bchild.tableWidget.setItem(rowCount2, 3, item3)
                    self.hide()
                    self.displayUi.show()
                    self.bchild.boucle.append([select_rows[0].row(), select_rows[n-1].row()])

    
    @pyqtSlot()
    def _save_actions(self):
        r = self.tableWidget.rowCount()
        session = self.pparent.hparent.sparent.parent.session
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
                if (not self.update_create_flag) :
                    cop = self.update_flag_act.copy()
                    check = []
                    for elem in cop :
                        if len(elem)==4:
                            if len(act_all)>elem[1] :
                                val = act_all[elem[1]]
                                temp = val[0]
                                temp2 =val[1]
                                session.query(Action).filter(Action.id == elem[0]).update({Action.name_action : temp.name_action ,
                                                        Action.desc_action : temp.desc_action , Action.true_false_action :temp.true_false_action, Action.order : temp.order, Action.precondition : temp.precondition})
                                a = session.query(Actor).get(elem[3])
                                if (a.name != temp2[0])|(a.role_actor != temp2[1]) :
                                    c = session.query(Action).filter(Action.id == elem[0]).all()
                                    session.delete(session.query(Action).get(c[0].id))
                                    u = Uplet()
                                    u.u_veracity = temp.true_false_action
                                    acc = Actor(name =temp2[0], role_actor =temp2[1])
                                    u.action_all.append(temp)
                                    u.protocol_id = self.uplid[0]
                                    u.actors_all = acc
                                    session.add(u)
                                session.commit()
                                self.update_flag_act.append([elem[0], elem[1],"UPDATE",elem[3]]) 
                                check.append(elem[0])                                                    
                        if len(elem)==3 :
                            x = session.query(Action).get(elem[0]) 
                            u = session.query(Uplet).get(x.uplet_id)
                            if (x is not None) :                  
                                if len(u.action_all)==1:
                                    session.delete(u)
                                else :
                                    session.delete(x)
                                session.commit()
                        if len(elem)==2:
                            val = act_all[elem[0]]
                            temp = val[0]
                            temp2 =val[1]
                            p = self.uplid[0]
                            x = session.query(Actor).filter((Actor.name==temp2[0])&(Actor.role_actor==temp2[1])).all()
                            if (len(x)==0) :
                                u =  Uplet()
                                u.action_all.append(temp)
                                u.u_veracity = temp.true_false_action
                                u.protocol_id = p
                                a = Actor(name =temp2[0], role_actor = temp2[1])
                                u.actors_all = a
                                session.add(u)
                                session.flush()
                                self.update_flag_act.append([temp.id, self.tableWidget.rowCount()-1,"UPDATE",a.id])  
                                check.append(temp.id)                     
                            else :
                                u = session.query(Uplet).filter((Uplet.protocol_id==p)&(Uplet.actor_id==x[0].id)).all()
                                print(u)
                                if len(u)>0 :
                                    temp.uplet_id = u[0].id
                                    if (temp.true_false_action==0) :
                                        session.query(Uplet).filter(Uplet.id == u[0].id).update({Uplet.u_veracity:0})
                                    u[0].action_all.append(temp)
                                    session.add(u[0])
                                else :
                                    u =  Uplet()
                                    u.actors_all = x[0]
                                    u.action_all.append(temp)
                                    u.u_veracity = temp.true_false_action
                                    u.protocol_id = p
                                    print(u)
                                    print(session)
                                    session.add(u)
                                session.flush()
                                self.update_flag_act.append([temp.id, self.tableWidget.rowCount()-1,"UPDATE",x[0].id])
                                check.append(temp.id) 
                            session.commit()
                        self.update_flag_act.remove(elem)
                    self.delete = check.copy()
                    self.nId = self.tableWidget.rowCount()
                    self.counter = 0
                else :
                    if(self.bchild is not None) :
                        if (len(self.bchild.boucle)>0):
                            for x in range(len(self.bchild.boucle)) :
                                self.bchild.list_boucle[x].acts.append(act_all[self.bchild.boucle[x][0]][0])
                                self.bchild.list_boucle[x].acts.append(act_all[self.bchild.boucle[x][1]][0])
                                session.add(self.bchild.list_boucle[x])
                    act_all = map_action_actor(act_all)
                    for val in act_all :
                        u = Uplet()
                        u.action_all = val[1]
                        u.u_veracity = u_veracity_compute([e.true_false_action for e in val[1]])
                        x =session.query(Actor).filter((Actor.name==val[0][0])&(Actor.role_actor==val[0][1])).all()
                        if (len(x)>0) :
                            u.actors_all = x[0]
                        else :
                            temp = Actor(name = val[0][0], role_actor = val[0][1])
                            u.actors_all = temp
                        self.pparent.save_protocol[self.bcreate].actor_list.append(u)
                        self.delete.append(temp.id)
                    self.pparent.uplets[self.bcreate] = self.pparent.save_protocol[self.bcreate]
                
                self.displayUi = self.pparent
                self.hide()
                self.displayUi.show()

class Boucle_child(QMainWindow, Boucle) :
    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)
        self.parent =parent
        self.pushButton_3.clicked.connect(self._removeRow)
        self.pushButton.clicked.connect(self._back_action)
        self.pushButton_2.clicked.connect(self._saveboucle)
        self.flag = True
    def _back_action(self):
        self.displayUi = self.parent
        self.hide()
        self.displayUi.show()
    
    @pyqtSlot()
    def _removeRow(self) :
        super()._removeRow()
        self.parent.i -= 1

    def _saveboucle(self) :
        self.list_boucle.clear()
        row = self.tableWidget.rowCount() 
        if row >0 :
            for i in range(row):
                self.list_boucle.append(Boucles(nbiter = self.tableWidget.item(i, 3).text()))
        self.hide()
        self.parent.show()

    def fullbtable(self, btable  = None) :
        if  btable is not None :
            for j in range(len(btable)) :
                row = btable[j]
                self.tableWidget.insertRow(j)
                result = session.query(Boucles).get(row)
                self.list_boucle.append(result)
                actions = result.acts
                n = len(actions)
                if n ==1 :
                    self.tableWidget.setItem(j, 1, QTableWidgetItem(actions[0].name_action))
                    self.tableWidget.setItem(j, 2, QTableWidgetItem(actions[0].name_action))
                    p= actions[0].id % self.parent.tableWidget.rowCount()
                    self.boucle.append([p,p])
                if n==2:
                    if (actions[0].order<=actions[1].order) :
                        self.tableWidget.setItem(j, 1, QTableWidgetItem(actions[0].name_action))
                        self.tableWidget.setItem(j, 2, QTableWidgetItem(actions[1].name_action))
                        p1= actions[0].id % self.parent.tableWidget.rowCount()
                        p2= actions[1].id % self.parent.tableWidget.rowCount()
                        self.boucle.append([p1,p2])
                    else :
                        self.tableWidget.setItem(j, 1, QTableWidgetItem(actions[1].name_action))
                        self.tableWidget.setItem(j, 2, QTableWidgetItem(actions[0].name_action))
                self.tableWidget.setItem(j,3, QTableWidgetItem(result.nbiter))
                self.tableWidget.setItem(j,0, QTableWidgetItem("Boucle d'action - " + str(j+1)))
            self.flag =  False
            self.parent.i = len(btable)

            


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form =QMainWindow()
    app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    ui1 = Menuprincipal_child()
    #ui = Modif_case()
    Form.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
    ui1.setupUi(Form)
    ui1.show()
    sys.exit(app.exec_())