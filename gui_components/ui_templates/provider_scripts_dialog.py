# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'provider_scripts_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_providerScriptsDialog(object):
    def setupUi(self, providerScriptsDialog):
        providerScriptsDialog.setObjectName("providerScriptsDialog")
        providerScriptsDialog.resize(771, 821)
        providerScriptsDialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(providerScriptsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_saved_providerspecific_modules = QtWidgets.QGroupBox(providerScriptsDialog)
        self.groupBox_saved_providerspecific_modules.setMaximumSize(QtCore.QSize(16777215, 200))
        self.groupBox_saved_providerspecific_modules.setObjectName("groupBox_saved_providerspecific_modules")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_saved_providerspecific_modules)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.groupBox_saved_providerspecific_modules)
        self.label_2.setScaledContents(True)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 4)
        self.comboBox_select_saved_providerscript_definition = QtWidgets.QComboBox(self.groupBox_saved_providerspecific_modules)
        self.comboBox_select_saved_providerscript_definition.setObjectName("comboBox_select_saved_providerscript_definition")
        self.gridLayout.addWidget(self.comboBox_select_saved_providerscript_definition, 1, 0, 1, 1)
        self.pushButton_apply_definition = QtWidgets.QPushButton(self.groupBox_saved_providerspecific_modules)
        self.pushButton_apply_definition.setObjectName("pushButton_apply_definition")
        self.gridLayout.addWidget(self.pushButton_apply_definition, 1, 1, 1, 1)
        self.pushButton_delete_definition = QtWidgets.QPushButton(self.groupBox_saved_providerspecific_modules)
        self.pushButton_delete_definition.setObjectName("pushButton_delete_definition")
        self.gridLayout.addWidget(self.pushButton_delete_definition, 1, 3, 1, 1)
        self.textView_providerscript_set_description = QtWidgets.QPlainTextEdit(self.groupBox_saved_providerspecific_modules)
        self.textView_providerscript_set_description.setReadOnly(True)
        self.textView_providerscript_set_description.setObjectName("textView_providerscript_set_description")
        self.gridLayout.addWidget(self.textView_providerscript_set_description, 2, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_saved_providerspecific_modules)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.groupBox_providerspecific_modules = QtWidgets.QGroupBox(providerScriptsDialog)
        self.groupBox_providerspecific_modules.setMinimumSize(QtCore.QSize(0, 400))
        self.groupBox_providerspecific_modules.setObjectName("groupBox_providerspecific_modules")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_providerspecific_modules)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.treeWidget = QtWidgets.QTreeWidget(self.groupBox_providerspecific_modules)
        self.treeWidget.setUniformRowHeights(False)
        self.treeWidget.setAnimated(True)
        self.treeWidget.setWordWrap(True)
        self.treeWidget.setObjectName("treeWidget")
        self.gridLayout_2.addWidget(self.treeWidget, 2, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(60, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButton_save_definition = QtWidgets.QPushButton(self.groupBox_providerspecific_modules)
        self.pushButton_save_definition.setObjectName("pushButton_save_definition")
        self.horizontalLayout.addWidget(self.pushButton_save_definition)
        self.gridLayout_2.addLayout(self.horizontalLayout, 3, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox_providerspecific_modules)
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem2, 1, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_providerspecific_modules)
        self.buttonBox_providerspecific_modules = QtWidgets.QDialogButtonBox(providerScriptsDialog)
        self.buttonBox_providerspecific_modules.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox_providerspecific_modules.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox_providerspecific_modules.setObjectName("buttonBox_providerspecific_modules")
        self.verticalLayout.addWidget(self.buttonBox_providerspecific_modules)

        self.retranslateUi(providerScriptsDialog)
        self.buttonBox_providerspecific_modules.accepted.connect(providerScriptsDialog.accept)
        self.buttonBox_providerspecific_modules.rejected.connect(providerScriptsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(providerScriptsDialog)

    def retranslateUi(self, providerScriptsDialog):
        _translate = QtCore.QCoreApplication.translate
        providerScriptsDialog.setWindowTitle(_translate("providerScriptsDialog", "Providerspezifische Anpassungen"))
        self.groupBox_saved_providerspecific_modules.setTitle(_translate("providerScriptsDialog", "Zuvor gespeicherte Zuordnungen"))
        self.label_2.setText(_translate("providerScriptsDialog", "<html><head/><body><p>Für jeden Datengeber können mehrere Zuordnungen providerspezifischer Anpassungen gespeichert werden. Dabei können ein Titel sowie eine Beschreibung ergänzt werden.</p><p>Bei Klick auf &quot;Anwenden&quot; wird die Selektion im Auswahlbaum unten entsprechend aktualisiert.</p></body></html>"))
        self.pushButton_apply_definition.setText(_translate("providerScriptsDialog", "Anwenden"))
        self.pushButton_delete_definition.setText(_translate("providerScriptsDialog", "Löschen"))
        self.textView_providerscript_set_description.setPlaceholderText(_translate("providerScriptsDialog", "Beschreibung der Zuordnung"))
        self.groupBox_providerspecific_modules.setTitle(_translate("providerScriptsDialog", "Verfügbare Anpassungen aller Datengeber"))
        self.treeWidget.headerItem().setText(0, _translate("providerScriptsDialog", "Anpassung"))
        self.treeWidget.headerItem().setText(1, _translate("providerScriptsDialog", "Beschreibung"))
        self.pushButton_save_definition.setText(_translate("providerScriptsDialog", "Aktuelle Zuordnung speichern"))
        self.label.setText(_translate("providerScriptsDialog", "Wählen Sie die providerspezifischen Anpassungen, die angewandt werden sollen, aus. Sie können alle Anpassungen eines Datengebers auswählen, indem sie die entsprechende ISIL auswählen."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    providerScriptsDialog = QtWidgets.QDialog()
    ui = Ui_providerScriptsDialog()
    ui.setupUi(providerScriptsDialog)
    providerScriptsDialog.show()
    sys.exit(app.exec_())
