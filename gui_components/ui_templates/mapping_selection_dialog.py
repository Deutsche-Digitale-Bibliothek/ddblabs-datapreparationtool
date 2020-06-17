# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mapping_selection_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_mappingSelectionDialog(object):
    def setupUi(self, mappingSelectionDialog):
        mappingSelectionDialog.setObjectName("mappingSelectionDialog")
        mappingSelectionDialog.resize(400, 155)
        self.gridLayout = QtWidgets.QGridLayout(mappingSelectionDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.comboBox_mapping_selection = QtWidgets.QComboBox(mappingSelectionDialog)
        self.comboBox_mapping_selection.setObjectName("comboBox_mapping_selection")
        self.comboBox_mapping_selection.addItem("")
        self.comboBox_mapping_selection.setItemText(0, "")
        self.comboBox_mapping_selection.addItem("")
        self.comboBox_mapping_selection.addItem("")
        self.comboBox_mapping_selection.addItem("")
        self.gridLayout.addWidget(self.comboBox_mapping_selection, 0, 0, 1, 1)
        self.label = QtWidgets.QLabel(mappingSelectionDialog)
        self.label.setMaximumSize(QtCore.QSize(25, 25))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/mapping-selection-dialog/info_icon.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(mappingSelectionDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 2)

        self.retranslateUi(mappingSelectionDialog)
        self.buttonBox.accepted.connect(mappingSelectionDialog.accept)
        self.buttonBox.rejected.connect(mappingSelectionDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(mappingSelectionDialog)

    def retranslateUi(self, mappingSelectionDialog):
        _translate = QtCore.QCoreApplication.translate
        mappingSelectionDialog.setWindowTitle(_translate("mappingSelectionDialog", "Mapping-Definition auswählen"))
        self.comboBox_mapping_selection.setItemText(1, _translate("mappingSelectionDialog", "ead2002_eadddb"))
        self.comboBox_mapping_selection.setItemText(2, _translate("mappingSelectionDialog", "ead_leobw"))
        self.comboBox_mapping_selection.setItemText(3, _translate("mappingSelectionDialog", "ead_iiif-json"))
        self.label.setToolTip(_translate("mappingSelectionDialog", "An dieser Stelle können vorgefertigte Mappings gewählt werden. Für Excel-Mappings kann die Funktion \"Mapping-Definition bearbeiten\" verwendet werden."))

from gui_components.ui_templates import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mappingSelectionDialog = QtWidgets.QDialog()
    ui = Ui_mappingSelectionDialog()
    ui.setupUi(mappingSelectionDialog)
    mappingSelectionDialog.show()
    sys.exit(app.exec_())
