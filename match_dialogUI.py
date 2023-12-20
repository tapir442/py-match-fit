# Form implementation generated from reading ui file 'ui/match_dialog.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Match_Dialog(object):
    def setupUi(self, Match_Dialog):
        Match_Dialog.setObjectName("Match_Dialog")
        Match_Dialog.resize(1116, 989)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=Match_Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(780, 90, 81, 241))
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.home_team = QtWidgets.QListWidget(parent=Match_Dialog)
        self.home_team.setGeometry(QtCore.QRect(100, 100, 231, 291))
        self.home_team.setObjectName("home_team")
        self.visiting_team = QtWidgets.QListWidget(parent=Match_Dialog)
        self.visiting_team.setGeometry(QtCore.QRect(340, 100, 241, 291))
        self.visiting_team.setObjectName("visiting_team")
        self.home_score = QtWidgets.QLCDNumber(parent=Match_Dialog)
        self.home_score.setGeometry(QtCore.QRect(170, 450, 121, 71))
        self.home_score.setObjectName("home_score")
        self.visiting_score = QtWidgets.QLCDNumber(parent=Match_Dialog)
        self.visiting_score.setGeometry(QtCore.QRect(410, 450, 131, 71))
        self.visiting_score.setObjectName("visiting_score")
        self.home_label = QtWidgets.QLabel(parent=Match_Dialog)
        self.home_label.setGeometry(QtCore.QRect(100, 70, 191, 17))
        self.home_label.setObjectName("home_label")
        self.visiting_label = QtWidgets.QLabel(parent=Match_Dialog)
        self.visiting_label.setGeometry(QtCore.QRect(350, 70, 181, 17))
        self.visiting_label.setObjectName("visiting_label")
        self.tabelle = QtWidgets.QTableWidget(parent=Match_Dialog)
        self.tabelle.setGeometry(QtCore.QRect(30, 530, 591, 361))
        self.tabelle.setObjectName("tabelle")
        self.tabelle.setColumnCount(5)
        self.tabelle.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tabelle.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabelle.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabelle.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabelle.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabelle.setHorizontalHeaderItem(4, item)
        self.scorer = QtWidgets.QTableWidget(parent=Match_Dialog)
        self.scorer.setGeometry(QtCore.QRect(640, 530, 451, 361))
        self.scorer.setObjectName("scorer")
        self.scorer.setColumnCount(4)
        self.scorer.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.scorer.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.scorer.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.scorer.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.scorer.setHorizontalHeaderItem(3, item)
        self.add_og_home = QtWidgets.QPushButton(parent=Match_Dialog)
        self.add_og_home.setGeometry(QtCore.QRect(170, 400, 21, 25))
        self.add_og_home.setObjectName("add_og_home")
        self.minus_og_home = QtWidgets.QPushButton(parent=Match_Dialog)
        self.minus_og_home.setGeometry(QtCore.QRect(210, 400, 21, 25))
        self.minus_og_home.setObjectName("minus_og_home")
        self.add_og_guest = QtWidgets.QPushButton(parent=Match_Dialog)
        self.add_og_guest.setGeometry(QtCore.QRect(410, 400, 21, 25))
        self.add_og_guest.setObjectName("add_og_guest")
        self.minus_og_guest = QtWidgets.QPushButton(parent=Match_Dialog)
        self.minus_og_guest.setGeometry(QtCore.QRect(450, 400, 21, 25))
        self.minus_og_guest.setObjectName("minus_og_guest")
        self.label = QtWidgets.QLabel(parent=Match_Dialog)
        self.label.setGeometry(QtCore.QRect(100, 400, 54, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(parent=Match_Dialog)
        self.label_2.setGeometry(QtCore.QRect(340, 400, 54, 21))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Match_Dialog)
        self.buttonBox.accepted.connect(Match_Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Match_Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Match_Dialog)

    def retranslateUi(self, Match_Dialog):
        _translate = QtCore.QCoreApplication.translate
        Match_Dialog.setWindowTitle(_translate("Match_Dialog", "Dialog"))
        self.home_label.setText(_translate("Match_Dialog", "TextLabel"))
        self.visiting_label.setText(_translate("Match_Dialog", "TextLabel"))
        item = self.tabelle.horizontalHeaderItem(0)
        item.setText(_translate("Match_Dialog", "Team"))
        item = self.tabelle.horizontalHeaderItem(1)
        item.setText(_translate("Match_Dialog", "Goals"))
        item = self.tabelle.horizontalHeaderItem(2)
        item.setText(_translate("Match_Dialog", "Got"))
        item = self.tabelle.horizontalHeaderItem(3)
        item.setText(_translate("Match_Dialog", "Diff"))
        item = self.tabelle.horizontalHeaderItem(4)
        item.setText(_translate("Match_Dialog", "Punkte"))
        item = self.scorer.horizontalHeaderItem(0)
        item.setText(_translate("Match_Dialog", "Nummer"))
        item = self.scorer.horizontalHeaderItem(1)
        item.setText(_translate("Match_Dialog", "Name"))
        item = self.scorer.horizontalHeaderItem(2)
        item.setText(_translate("Match_Dialog", "Team"))
        item = self.scorer.horizontalHeaderItem(3)
        item.setText(_translate("Match_Dialog", "Goals"))
        self.add_og_home.setText(_translate("Match_Dialog", "+"))
        self.minus_og_home.setText(_translate("Match_Dialog", "-"))
        self.add_og_guest.setText(_translate("Match_Dialog", "+"))
        self.minus_og_guest.setText(_translate("Match_Dialog", "-"))
        self.label.setText(_translate("Match_Dialog", "Eigentore"))
        self.label_2.setText(_translate("Match_Dialog", "Eigentore"))
