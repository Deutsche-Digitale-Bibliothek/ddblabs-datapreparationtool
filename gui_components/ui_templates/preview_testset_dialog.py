# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'preview_testset_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_previewTestsetDialog(object):
    def setupUi(self, previewTestsetDialog):
        previewTestsetDialog.setObjectName("previewTestsetDialog")
        previewTestsetDialog.resize(377, 465)
        previewTestsetDialog.setModal(True)
        self.gridLayout = QtWidgets.QGridLayout(previewTestsetDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.radioButton_preview_all_objects = QtWidgets.QRadioButton(previewTestsetDialog)
        self.radioButton_preview_all_objects.setChecked(True)
        self.radioButton_preview_all_objects.setObjectName("radioButton_preview_all_objects")
        self.gridLayout.addWidget(self.radioButton_preview_all_objects, 0, 0, 1, 3)
        spacerItem = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(previewTestsetDialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setScaledContents(True)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 1, 1, 3)
        self.radioButton_preview_automatic_testset = QtWidgets.QRadioButton(previewTestsetDialog)
        self.radioButton_preview_automatic_testset.setObjectName("radioButton_preview_automatic_testset")
        self.gridLayout.addWidget(self.radioButton_preview_automatic_testset, 2, 0, 1, 3)
        spacerItem1 = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 3, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(previewTestsetDialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setScaledContents(True)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 1, 1, 3)
        spacerItem2 = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 4, 0, 1, 1)
        self.label_preview_count = QtWidgets.QLabel(previewTestsetDialog)
        self.label_preview_count.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_preview_count.setFont(font)
        self.label_preview_count.setScaledContents(True)
        self.label_preview_count.setWordWrap(True)
        self.label_preview_count.setObjectName("label_preview_count")
        self.gridLayout.addWidget(self.label_preview_count, 4, 1, 1, 2)
        self.radioButton_manual_testset = QtWidgets.QRadioButton(previewTestsetDialog)
        self.radioButton_manual_testset.setObjectName("radioButton_manual_testset")
        self.gridLayout.addWidget(self.radioButton_manual_testset, 5, 0, 1, 4)
        spacerItem3 = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 6, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(previewTestsetDialog)
        self.groupBox.setEnabled(False)
        self.groupBox.setCheckable(False)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.textEdit_testset_ids = QtWidgets.QTextEdit(self.groupBox)
        self.textEdit_testset_ids.setObjectName("textEdit_testset_ids")
        self.verticalLayout_2.addWidget(self.textEdit_testset_ids)
        self.label = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.gridLayout.addWidget(self.groupBox, 6, 1, 1, 3)
        self.buttonBox_preview_testset = QtWidgets.QDialogButtonBox(previewTestsetDialog)
        self.buttonBox_preview_testset.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox_preview_testset.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox_preview_testset.setObjectName("buttonBox_preview_testset")
        self.gridLayout.addWidget(self.buttonBox_preview_testset, 7, 2, 1, 2)
        self.comboBox_preview_count = QtWidgets.QComboBox(previewTestsetDialog)
        self.comboBox_preview_count.setEnabled(False)
        self.comboBox_preview_count.setObjectName("comboBox_preview_count")
        self.comboBox_preview_count.addItem("")
        self.comboBox_preview_count.addItem("")
        self.comboBox_preview_count.addItem("")
        self.comboBox_preview_count.addItem("")
        self.comboBox_preview_count.addItem("")
        self.comboBox_preview_count.addItem("")
        self.comboBox_preview_count.addItem("")
        self.comboBox_preview_count.addItem("")
        self.comboBox_preview_count.addItem("")
        self.comboBox_preview_count.addItem("")
        self.comboBox_preview_count.addItem("")
        self.comboBox_preview_count.addItem("")
        self.comboBox_preview_count.addItem("")
        self.comboBox_preview_count.addItem("")
        self.comboBox_preview_count.addItem("")
        self.comboBox_preview_count.addItem("")
        self.comboBox_preview_count.addItem("")
        self.comboBox_preview_count.addItem("")
        self.comboBox_preview_count.addItem("")
        self.comboBox_preview_count.addItem("")
        self.gridLayout.addWidget(self.comboBox_preview_count, 4, 3, 1, 1)

        self.retranslateUi(previewTestsetDialog)
        self.comboBox_preview_count.setCurrentIndex(4)
        self.buttonBox_preview_testset.accepted.connect(previewTestsetDialog.accept)
        self.buttonBox_preview_testset.rejected.connect(previewTestsetDialog.reject)
        self.radioButton_manual_testset.toggled['bool'].connect(self.groupBox.setEnabled)
        self.radioButton_preview_automatic_testset.toggled['bool'].connect(self.label_preview_count.setEnabled)
        self.radioButton_preview_automatic_testset.toggled['bool'].connect(self.comboBox_preview_count.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(previewTestsetDialog)

    def retranslateUi(self, previewTestsetDialog):
        _translate = QtCore.QCoreApplication.translate
        previewTestsetDialog.setWindowTitle(_translate("previewTestsetDialog", "Testset für Voransichten"))
        self.radioButton_preview_all_objects.setText(_translate("previewTestsetDialog", "Alle Objekte berücksichtigen"))
        self.label_2.setText(_translate("previewTestsetDialog", "Für jedes der Objekte auf allen Hierarchieebenen wird eine Vorschau erstellt. "))
        self.radioButton_preview_automatic_testset.setText(_translate("previewTestsetDialog", "Testset automatisch ermitteln"))
        self.label_3.setText(_translate("previewTestsetDialog", "Es wird automatisch eine repräsentative Menge von Datensätzen ausgewählt, für die Voransichten erstellt werden."))
        self.label_preview_count.setText(_translate("previewTestsetDialog", "Anzahl zu erstellender Datensätze pro Objekttyp:"))
        self.radioButton_manual_testset.setText(_translate("previewTestsetDialog", "Testset manuell definieren:"))
        self.groupBox.setTitle(_translate("previewTestsetDialog", "Testset-IDs für Voransichten"))
        self.textEdit_testset_ids.setPlaceholderText(_translate("previewTestsetDialog", "beispiel_id_001 | beispiel_id_002 | beispiel_id_003"))
        self.label.setText(_translate("previewTestsetDialog", "Durch die Übergabe von IDs kann bestimmt werden, zu welchen Datensätzen eine Voransicht erstellt wird. Die IDs sollten per \" | \" getrennt werden."))
        self.comboBox_preview_count.setItemText(0, _translate("previewTestsetDialog", "5"))
        self.comboBox_preview_count.setItemText(1, _translate("previewTestsetDialog", "10"))
        self.comboBox_preview_count.setItemText(2, _translate("previewTestsetDialog", "15"))
        self.comboBox_preview_count.setItemText(3, _translate("previewTestsetDialog", "20"))
        self.comboBox_preview_count.setItemText(4, _translate("previewTestsetDialog", "25"))
        self.comboBox_preview_count.setItemText(5, _translate("previewTestsetDialog", "30"))
        self.comboBox_preview_count.setItemText(6, _translate("previewTestsetDialog", "35"))
        self.comboBox_preview_count.setItemText(7, _translate("previewTestsetDialog", "40"))
        self.comboBox_preview_count.setItemText(8, _translate("previewTestsetDialog", "45"))
        self.comboBox_preview_count.setItemText(9, _translate("previewTestsetDialog", "50"))
        self.comboBox_preview_count.setItemText(10, _translate("previewTestsetDialog", "55"))
        self.comboBox_preview_count.setItemText(11, _translate("previewTestsetDialog", "60"))
        self.comboBox_preview_count.setItemText(12, _translate("previewTestsetDialog", "65"))
        self.comboBox_preview_count.setItemText(13, _translate("previewTestsetDialog", "70"))
        self.comboBox_preview_count.setItemText(14, _translate("previewTestsetDialog", "75"))
        self.comboBox_preview_count.setItemText(15, _translate("previewTestsetDialog", "80"))
        self.comboBox_preview_count.setItemText(16, _translate("previewTestsetDialog", "85"))
        self.comboBox_preview_count.setItemText(17, _translate("previewTestsetDialog", "90"))
        self.comboBox_preview_count.setItemText(18, _translate("previewTestsetDialog", "95"))
        self.comboBox_preview_count.setItemText(19, _translate("previewTestsetDialog", "100"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    previewTestsetDialog = QtWidgets.QDialog()
    ui = Ui_previewTestsetDialog()
    ui.setupUi(previewTestsetDialog)
    previewTestsetDialog.show()
    sys.exit(app.exec_())

