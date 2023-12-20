# Form implementation generated from reading ui file 'ui/mainWindow.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1131, 969)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.matchPlan = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.matchPlan.setGeometry(QtCore.QRect(200, 200, 581, 361))
        self.matchPlan.setMaximumSize(QtCore.QSize(1113, 16777215))
        self.matchPlan.setColumnCount(4)
        self.matchPlan.setObjectName("matchPlan")
        self.matchPlan.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.matchPlan.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.matchPlan.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.matchPlan.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.matchPlan.setHorizontalHeaderItem(3, item)
        self.finish_tournament = QtWidgets.QPushButton(parent=self.centralwidget)
        self.finish_tournament.setGeometry(QtCore.QRect(990, 900, 115, 25))
        self.finish_tournament.setObjectName("finish_tournament")
        self.contestor_label = QtWidgets.QLabel(parent=self.centralwidget)
        self.contestor_label.setGeometry(QtCore.QRect(9, 108, 62, 17))
        self.contestor_label.setObjectName("contestor_label")
        self.tournament_parameters = QtWidgets.QPushButton(parent=self.centralwidget)
        self.tournament_parameters.setGeometry(QtCore.QRect(9, 9, 146, 25))
        self.tournament_parameters.setObjectName("tournament_parameters")
        self.teams_and_schedule = QtWidgets.QPushButton(parent=self.centralwidget)
        self.teams_and_schedule.setGeometry(QtCore.QRect(9, 46, 124, 25))
        self.teams_and_schedule.setObjectName("teams_and_schedule")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(200, 170, 91, 17))
        self.label.setObjectName("label")
        self.logoLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.logoLabel.setGeometry(QtCore.QRect(930, 0, 200, 200))
        self.logoLabel.setObjectName("logoLabel")
        self.start_match = QtWidgets.QPushButton(parent=self.centralwidget)
        self.start_match.setGeometry(QtCore.QRect(790, 200, 171, 25))
        self.start_match.setObjectName("start_match")
        self.tabelle = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.tabelle.setGeometry(QtCore.QRect(10, 610, 641, 281))
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
        self.scorer = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.scorer.setGeometry(QtCore.QRect(660, 610, 421, 281))
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
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1131, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        item = self.matchPlan.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Beginn"))
        item = self.matchPlan.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Gast"))
        item = self.matchPlan.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Heim"))
        item = self.matchPlan.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Ergebnis"))
        self.finish_tournament.setText(_translate("MainWindow", "Finish Tournament"))
        self.contestor_label.setText(_translate("MainWindow", "Contestors"))
        self.tournament_parameters.setText(_translate("MainWindow", "Tournament Parameters"))
        self.teams_and_schedule.setText(_translate("MainWindow", "Teams and Schedule"))
        self.label.setText(_translate("MainWindow", "Match Plan"))
        self.logoLabel.setText(_translate("MainWindow", "TextLabel"))
        self.start_match.setText(_translate("MainWindow", "Start next match"))
        item = self.tabelle.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Team"))
        item = self.tabelle.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Goals"))
        item = self.tabelle.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Got"))
        item = self.tabelle.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Diff"))
        item = self.tabelle.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Punkte"))
        item = self.scorer.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Nummer"))
        item = self.scorer.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Name"))
        item = self.scorer.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Team"))
        item = self.scorer.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Goals"))
