# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'provider_aggregator_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_provider_aggregator_Dialog(object):
    def setupUi(self, provider_aggregator_Dialog):
        provider_aggregator_Dialog.setObjectName("provider_aggregator_Dialog")
        provider_aggregator_Dialog.resize(551, 144)
        self.gridLayout = QtWidgets.QGridLayout(provider_aggregator_Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(provider_aggregator_Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 2)
        self.groupBox = QtWidgets.QGroupBox(provider_aggregator_Dialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.comboBox_aggregator_selection = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_aggregator_selection.setObjectName("comboBox_aggregator_selection")
        self.gridLayout_2.addWidget(self.comboBox_aggregator_selection, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.checkBox_use_aggregator_logo = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_use_aggregator_logo.setChecked(True)
        self.checkBox_use_aggregator_logo.setObjectName("checkBox_use_aggregator_logo")
        self.gridLayout_2.addWidget(self.checkBox_use_aggregator_logo, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 2)

        self.retranslateUi(provider_aggregator_Dialog)
        self.buttonBox.accepted.connect(provider_aggregator_Dialog.accept)
        self.buttonBox.rejected.connect(provider_aggregator_Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(provider_aggregator_Dialog)

    def retranslateUi(self, provider_aggregator_Dialog):
        _translate = QtCore.QCoreApplication.translate
        provider_aggregator_Dialog.setWindowTitle(_translate("provider_aggregator_Dialog", "Aggregator-Zuordnung bearbeiten"))
        self.groupBox.setTitle(_translate("provider_aggregator_Dialog", "Zuordnung des Aggregators"))
        self.label.setText(_translate("provider_aggregator_Dialog", "Aggregator auswählen:"))
        self.checkBox_use_aggregator_logo.setText(_translate("provider_aggregator_Dialog", "Logo des Aggregators auf DDB-Objektseiten anzeigen"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    provider_aggregator_Dialog = QtWidgets.QDialog()
    ui = Ui_provider_aggregator_Dialog()
    ui.setupUi(provider_aggregator_Dialog)
    provider_aggregator_Dialog.show()
    sys.exit(app.exec_())

