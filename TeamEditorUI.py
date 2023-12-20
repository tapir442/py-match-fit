# Form implementation generated from reading ui file 'ui/TeamEditor.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_TeamAndScheduleEditor(object):
    def setupUi(self, TeamAndScheduleEditor):
        TeamAndScheduleEditor.setObjectName("TeamAndScheduleEditor")
        TeamAndScheduleEditor.resize(840, 780)
        self.ok_cancel = QtWidgets.QDialogButtonBox(parent=TeamAndScheduleEditor)
        self.ok_cancel.setGeometry(QtCore.QRect(400, 480, 81, 61))
        self.ok_cancel.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.ok_cancel.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.ok_cancel.setObjectName("ok_cancel")
        self.team_list = QtWidgets.QListWidget(parent=TeamAndScheduleEditor)
        self.team_list.setGeometry(QtCore.QRect(20, 20, 256, 192))
        self.team_list.setObjectName("team_list")
        self.create_schedule_button = QtWidgets.QPushButton(parent=TeamAndScheduleEditor)
        self.create_schedule_button.setGeometry(QtCore.QRect(20, 240, 141, 24))
        self.create_schedule_button.setObjectName("create_schedule_button")
        self.scheduleEditor = QtWidgets.QTableWidget(parent=TeamAndScheduleEditor)
        self.scheduleEditor.setGeometry(QtCore.QRect(20, 280, 331, 471))
        self.scheduleEditor.setObjectName("scheduleEditor")
        self.scheduleEditor.setColumnCount(3)
        self.scheduleEditor.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.scheduleEditor.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.scheduleEditor.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.scheduleEditor.setHorizontalHeaderItem(2, item)
        self.team = QtWidgets.QLineEdit(parent=TeamAndScheduleEditor)
        self.team.setGeometry(QtCore.QRect(310, 20, 231, 25))
        self.team.setObjectName("team")
        self.addTeam = QtWidgets.QPushButton(parent=TeamAndScheduleEditor)
        self.addTeam.setGeometry(QtCore.QRect(380, 60, 71, 25))
        self.addTeam.setObjectName("addTeam")
        self.switch_matches = QtWidgets.QPushButton(parent=TeamAndScheduleEditor)
        self.switch_matches.setGeometry(QtCore.QRect(380, 310, 161, 25))
        self.switch_matches.setObjectName("switch_matches")
        self.switch1 = QtWidgets.QLineEdit(parent=TeamAndScheduleEditor)
        self.switch1.setGeometry(QtCore.QRect(560, 310, 31, 25))
        self.switch1.setObjectName("switch1")
        self.switch2 = QtWidgets.QLineEdit(parent=TeamAndScheduleEditor)
        self.switch2.setGeometry(QtCore.QRect(600, 310, 31, 25))
        self.switch2.setObjectName("switch2")
        self.switch_teams = QtWidgets.QPushButton(parent=TeamAndScheduleEditor)
        self.switch_teams.setGeometry(QtCore.QRect(380, 350, 161, 25))
        self.switch_teams.setObjectName("switch_teams")
        self.switch_team_idx = QtWidgets.QLineEdit(parent=TeamAndScheduleEditor)
        self.switch_team_idx.setGeometry(QtCore.QRect(560, 350, 31, 25))
        self.switch_team_idx.setObjectName("switch_team_idx")
        self.meinturnierplan = QtWidgets.QPushButton(parent=TeamAndScheduleEditor)
        self.meinturnierplan.setGeometry(QtCore.QRect(180, 240, 161, 25))
        self.meinturnierplan.setObjectName("meinturnierplan")

        self.retranslateUi(TeamAndScheduleEditor)
        self.ok_cancel.accepted.connect(TeamAndScheduleEditor.accept) # type: ignore
        self.ok_cancel.rejected.connect(TeamAndScheduleEditor.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(TeamAndScheduleEditor)

    def retranslateUi(self, TeamAndScheduleEditor):
        _translate = QtCore.QCoreApplication.translate
        TeamAndScheduleEditor.setWindowTitle(_translate("TeamAndScheduleEditor", "Dialog"))
        self.create_schedule_button.setText(_translate("TeamAndScheduleEditor", "Create Schedule"))
        item = self.scheduleEditor.horizontalHeaderItem(0)
        item.setText(_translate("TeamAndScheduleEditor", "Beginn"))
        item = self.scheduleEditor.horizontalHeaderItem(1)
        item.setText(_translate("TeamAndScheduleEditor", "Heim"))
        item = self.scheduleEditor.horizontalHeaderItem(2)
        item.setText(_translate("TeamAndScheduleEditor", "Gast"))
        self.addTeam.setText(_translate("TeamAndScheduleEditor", "Add Team"))
        self.switch_matches.setText(_translate("TeamAndScheduleEditor", "Switch matches "))
        self.switch_teams.setText(_translate("TeamAndScheduleEditor", "Switch teams"))
        self.meinturnierplan.setText(_translate("TeamAndScheduleEditor", "Turnierplan.de"))
