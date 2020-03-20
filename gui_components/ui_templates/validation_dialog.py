# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'validation_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_validationDialog(object):
    def setupUi(self, validationDialog):
        validationDialog.setObjectName("validationDialog")
        validationDialog.resize(513, 465)
        self.gridLayout = QtWidgets.QGridLayout(validationDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_2 = QtWidgets.QGroupBox(validationDialog)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.comboBox_schema_selection = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox_schema_selection.setObjectName("comboBox_schema_selection")
        self.comboBox_schema_selection.addItem("")
        self.comboBox_schema_selection.addItem("")
        self.gridLayout_3.addWidget(self.comboBox_schema_selection, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox_2, 1, 0, 1, 1)
        self.buttonBox_validation_dialog = QtWidgets.QDialogButtonBox(validationDialog)
        self.buttonBox_validation_dialog.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox_validation_dialog.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox_validation_dialog.setObjectName("buttonBox_validation_dialog")
        self.gridLayout.addWidget(self.buttonBox_validation_dialog, 2, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(validationDialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.listWidget_validation_files = QtWidgets.QListWidget(self.groupBox)
        self.listWidget_validation_files.setEnabled(True)
        self.listWidget_validation_files.setObjectName("listWidget_validation_files")
        self.gridLayout_2.addWidget(self.listWidget_validation_files, 0, 0, 1, 3)
        self.toolButton_select_files = QtWidgets.QToolButton(self.groupBox)
        self.toolButton_select_files.setObjectName("toolButton_select_files")
        self.gridLayout_2.addWidget(self.toolButton_select_files, 1, 0, 1, 1)
        self.toolButton_remove_file_entry = QtWidgets.QToolButton(self.groupBox)
        self.toolButton_remove_file_entry.setObjectName("toolButton_remove_file_entry")
        self.gridLayout_2.addWidget(self.toolButton_remove_file_entry, 1, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(257, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 1, 2, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)

        self.retranslateUi(validationDialog)
        self.buttonBox_validation_dialog.accepted.connect(validationDialog.accept)
        self.buttonBox_validation_dialog.rejected.connect(validationDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(validationDialog)

    def retranslateUi(self, validationDialog):
        _translate = QtCore.QCoreApplication.translate
        validationDialog.setWindowTitle(_translate("validationDialog", "Validierung"))
        self.groupBox_2.setTitle(_translate("validationDialog", "Schema auswählen"))
        self.comboBox_schema_selection.setItemText(0, _translate("validationDialog", "EAD(DDB) Findbuch"))
        self.comboBox_schema_selection.setItemText(1, _translate("validationDialog", "EAD(DDB) Tektonik"))
        self.groupBox.setTitle(_translate("validationDialog", "Zu validierende Dateien wählen"))
        self.toolButton_select_files.setText(_translate("validationDialog", "Dateien auswählen"))
        self.toolButton_remove_file_entry.setText(_translate("validationDialog", "Eintrag entfernen"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    validationDialog = QtWidgets.QDialog()
    ui = Ui_validationDialog()
    ui.setupUi(validationDialog)
    validationDialog.show()
    sys.exit(app.exec_())
