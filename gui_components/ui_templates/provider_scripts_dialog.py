# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'provider_scripts_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_providerScriptsDialog(object):
    def setupUi(self, providerScriptsDialog):
        providerScriptsDialog.setObjectName("providerScriptsDialog")
        providerScriptsDialog.resize(771, 475)
        providerScriptsDialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(providerScriptsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_providerspecific_modules = QtWidgets.QGroupBox(providerScriptsDialog)
        self.groupBox_providerspecific_modules.setObjectName("groupBox_providerspecific_modules")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_providerspecific_modules)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 2, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.groupBox_providerspecific_modules)
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        spacerItem1 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem1)
        self.treeWidget = QtWidgets.QTreeWidget(self.groupBox_providerspecific_modules)
        self.treeWidget.setUniformRowHeights(False)
        self.treeWidget.setAnimated(True)
        self.treeWidget.setWordWrap(True)
        self.treeWidget.setObjectName("treeWidget")
        self.verticalLayout_2.addWidget(self.treeWidget)
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
        self.groupBox_providerspecific_modules.setTitle(_translate("providerScriptsDialog", "Verfügbare Anpassungen aller Datengeber"))
        self.label.setText(_translate("providerScriptsDialog", "Wählen Sie die providerspezifischen Anpassungen, die angewandt werden sollen, aus. Sie können alle Anpassungen eines Datengebers auswählen, indem sie die entsprechende ISIL auswählen."))
        self.treeWidget.headerItem().setText(0, _translate("providerScriptsDialog", "Anpassung"))
        self.treeWidget.headerItem().setText(1, _translate("providerScriptsDialog", "Beschreibung"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    providerScriptsDialog = QtWidgets.QDialog()
    ui = Ui_providerScriptsDialog()
    ui.setupUi(providerScriptsDialog)
    providerScriptsDialog.show()
    sys.exit(app.exec_())

