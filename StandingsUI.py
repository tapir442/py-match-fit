# Form implementation generated from reading ui file 'ui/Standings.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Standings(object):
    def setupUi(self, Standings):
        Standings.setObjectName("Standings")
        Standings.resize(615, 683)
        self.standingsView = QtWidgets.QTableView(Standings)
        self.standingsView.setGeometry(QtCore.QRect(60, 60, 481, 192))
        self.standingsView.setObjectName("standingsView")
        self.scorerView = QtWidgets.QColumnView(Standings)
        self.scorerView.setGeometry(QtCore.QRect(60, 360, 481, 192))
        self.scorerView.setObjectName("scorerView")
        self.label = QtWidgets.QLabel(Standings)
        self.label.setGeometry(QtCore.QRect(60, 320, 151, 16))
        self.label.setObjectName("label")

        self.retranslateUi(Standings)
        QtCore.QMetaObject.connectSlotsByName(Standings)

    def retranslateUi(self, Standings):
        _translate = QtCore.QCoreApplication.translate
        Standings.setWindowTitle(_translate("Standings", "Dialog"))
        self.label.setText(_translate("Standings", "Scorer"))
