# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'oai_sets_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_oaiSetsDialog(object):
    def setupUi(self, oaiSetsDialog):
        oaiSetsDialog.setObjectName("oaiSetsDialog")
        oaiSetsDialog.resize(609, 406)
        self.gridLayout = QtWidgets.QGridLayout(oaiSetsDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(oaiSetsDialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.treeWidget = QtWidgets.QTreeWidget(self.groupBox)
        self.treeWidget.setObjectName("treeWidget")
        self.gridLayout_2.addWidget(self.treeWidget, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(oaiSetsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(oaiSetsDialog)
        self.buttonBox.accepted.connect(oaiSetsDialog.accept)
        self.buttonBox.rejected.connect(oaiSetsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(oaiSetsDialog)

    def retranslateUi(self, oaiSetsDialog):
        _translate = QtCore.QCoreApplication.translate
        oaiSetsDialog.setWindowTitle(_translate("oaiSetsDialog", "Verfügbare Sets des OAI-Providers"))
        self.groupBox.setTitle(_translate("oaiSetsDialog", "Sets des OAI-Providers"))
        self.treeWidget.headerItem().setText(0, _translate("oaiSetsDialog", "Set-identifier"))
        self.treeWidget.headerItem().setText(1, _translate("oaiSetsDialog", "Set-Name"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    oaiSetsDialog = QtWidgets.QDialog()
    ui = Ui_oaiSetsDialog()
    ui.setupUi(oaiSetsDialog)
    oaiSetsDialog.show()
    sys.exit(app.exec_())

