# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'provider_scripts_save_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_providerScriptsSaveDialog(object):
    def setupUi(self, providerScriptsSaveDialog):
        providerScriptsSaveDialog.setObjectName("providerScriptsSaveDialog")
        providerScriptsSaveDialog.setWindowModality(QtCore.Qt.WindowModal)
        providerScriptsSaveDialog.resize(400, 310)
        self.gridLayout = QtWidgets.QGridLayout(providerScriptsSaveDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox_save_providerscript_set = QtWidgets.QDialogButtonBox(providerScriptsSaveDialog)
        self.buttonBox_save_providerscript_set.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox_save_providerscript_set.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox_save_providerscript_set.setObjectName("buttonBox_save_providerscript_set")
        self.gridLayout.addWidget(self.buttonBox_save_providerscript_set, 1, 0, 1, 1)
        self.groupBox_providerscript_set_description = QtWidgets.QGroupBox(providerScriptsSaveDialog)
        self.groupBox_providerscript_set_description.setObjectName("groupBox_providerscript_set_description")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_providerscript_set_description)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.groupBox_providerscript_set_description)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit_providerscript_set_name = QtWidgets.QLineEdit(self.groupBox_providerscript_set_description)
        self.lineEdit_providerscript_set_name.setClearButtonEnabled(True)
        self.lineEdit_providerscript_set_name.setObjectName("lineEdit_providerscript_set_name")
        self.gridLayout_2.addWidget(self.lineEdit_providerscript_set_name, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox_providerscript_set_description)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)
        self.plainTextEdit_providerscript_set_description = QtWidgets.QPlainTextEdit(self.groupBox_providerscript_set_description)
        self.plainTextEdit_providerscript_set_description.setObjectName("plainTextEdit_providerscript_set_description")
        self.gridLayout_2.addWidget(self.plainTextEdit_providerscript_set_description, 3, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_providerscript_set_description, 0, 0, 1, 1)

        self.retranslateUi(providerScriptsSaveDialog)
        self.buttonBox_save_providerscript_set.accepted.connect(providerScriptsSaveDialog.accept)
        self.buttonBox_save_providerscript_set.rejected.connect(providerScriptsSaveDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(providerScriptsSaveDialog)

    def retranslateUi(self, providerScriptsSaveDialog):
        _translate = QtCore.QCoreApplication.translate
        providerScriptsSaveDialog.setWindowTitle(_translate("providerScriptsSaveDialog", "Neue Zuordnung speichern"))
        self.groupBox_providerscript_set_description.setTitle(_translate("providerScriptsSaveDialog", "Angaben zur Zuordnung"))
        self.label.setText(_translate("providerScriptsSaveDialog", "Name: "))
        self.lineEdit_providerscript_set_name.setPlaceholderText(_translate("providerScriptsSaveDialog", "Name, z.B. \"Vorprozessierung\""))
        self.label_2.setText(_translate("providerScriptsSaveDialog", "Beschreibung: "))
        self.plainTextEdit_providerscript_set_description.setPlaceholderText(_translate("providerScriptsSaveDialog", "Beschreibung (optional)"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    providerScriptsSaveDialog = QtWidgets.QDialog()
    ui = Ui_providerScriptsSaveDialog()
    ui.setupUi(providerScriptsSaveDialog)
    providerScriptsSaveDialog.show()
    sys.exit(app.exec_())
