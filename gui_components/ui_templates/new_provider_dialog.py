# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'new_provider_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_newProviderDialog(object):
    def setupUi(self, newProviderDialog):
        newProviderDialog.setObjectName("newProviderDialog")
        newProviderDialog.resize(332, 183)
        newProviderDialog.setMinimumSize(QtCore.QSize(315, 164))
        newProviderDialog.setModal(True)
        self.gridLayout_2 = QtWidgets.QGridLayout(newProviderDialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lineEdit_newprovider_isil = QtWidgets.QLineEdit(newProviderDialog)
        self.lineEdit_newprovider_isil.setClearButtonEnabled(True)
        self.lineEdit_newprovider_isil.setObjectName("lineEdit_newprovider_isil")
        self.gridLayout_2.addWidget(self.lineEdit_newprovider_isil, 1, 2, 1, 1)
        self.label = QtWidgets.QLabel(newProviderDialog)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 3, 2, 1, 1)
        self.frame_new_provider_hint = QtWidgets.QFrame(newProviderDialog)
        self.frame_new_provider_hint.setStyleSheet("background-color: rgba(164, 219, 255, 235);")
        self.frame_new_provider_hint.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_new_provider_hint.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_new_provider_hint.setObjectName("frame_new_provider_hint")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_new_provider_hint)
        self.gridLayout.setObjectName("gridLayout")
        self.label_new_provider_hint = QtWidgets.QLabel(self.frame_new_provider_hint)
        self.label_new_provider_hint.setScaledContents(True)
        self.label_new_provider_hint.setWordWrap(True)
        self.label_new_provider_hint.setObjectName("label_new_provider_hint")
        self.gridLayout.addWidget(self.label_new_provider_hint, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame_new_provider_hint, 2, 2, 1, 1)
        self.buttonBox_new_provider = QtWidgets.QDialogButtonBox(newProviderDialog)
        self.buttonBox_new_provider.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox_new_provider.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox_new_provider.setObjectName("buttonBox_new_provider")
        self.gridLayout_2.addWidget(self.buttonBox_new_provider, 4, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(newProviderDialog)
        self.label_2.setMinimumSize(QtCore.QSize(64, 64))
        self.label_2.setMaximumSize(QtCore.QSize(64, 64))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap(":/main-window/institution.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setWordWrap(False)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 2, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 0, 1, 1, 1)

        self.retranslateUi(newProviderDialog)
        self.buttonBox_new_provider.accepted.connect(newProviderDialog.accept)
        self.buttonBox_new_provider.rejected.connect(newProviderDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(newProviderDialog)

    def retranslateUi(self, newProviderDialog):
        _translate = QtCore.QCoreApplication.translate
        newProviderDialog.setWindowTitle(_translate("newProviderDialog", "Neuer Datengeber"))
        self.lineEdit_newprovider_isil.setPlaceholderText(_translate("newProviderDialog", "DE-1951"))
        self.label.setText(_translate("newProviderDialog", "Bitte eine ISIL-Nummer für den neuen Datengeber eingeben: "))
        self.label_new_provider_hint.setText(_translate("newProviderDialog", "Alternativ können Sie auch einen anderen Bezeichner angeben, etwa den Namen der datengebenden Institution."))

from gui_components.ui_templates import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    newProviderDialog = QtWidgets.QDialog()
    ui = Ui_newProviderDialog()
    ui.setupUi(newProviderDialog)
    newProviderDialog.show()
    sys.exit(app.exec_())
