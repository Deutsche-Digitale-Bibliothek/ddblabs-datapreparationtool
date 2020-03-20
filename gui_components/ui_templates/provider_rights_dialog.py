# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'provider_rights_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_provider_rights_Dialog(object):
    def setupUi(self, provider_rights_Dialog):
        provider_rights_Dialog.setObjectName("provider_rights_Dialog")
        provider_rights_Dialog.resize(473, 367)
        self.gridLayout = QtWidgets.QGridLayout(provider_rights_Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(provider_rights_Dialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit_rights_metadata_uri = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_rights_metadata_uri.setObjectName("lineEdit_rights_metadata_uri")
        self.gridLayout_2.addWidget(self.lineEdit_rights_metadata_uri, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.lineEdit_rights_metadata_label = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_rights_metadata_label.setObjectName("lineEdit_rights_metadata_label")
        self.gridLayout_2.addWidget(self.lineEdit_rights_metadata_label, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 2)
        self.buttonBox = QtWidgets.QDialogButtonBox(provider_rights_Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 2)
        self.groupBox_2 = QtWidgets.QGroupBox(provider_rights_Dialog)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 0, 0, 1, 1)
        self.lineEdit_rights_binaries_uri = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_rights_binaries_uri.setObjectName("lineEdit_rights_binaries_uri")
        self.gridLayout_3.addWidget(self.lineEdit_rights_binaries_uri, 0, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 1, 0, 1, 1)
        self.lineEdit_rights_binaries_label = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_rights_binaries_label.setObjectName("lineEdit_rights_binaries_label")
        self.gridLayout_3.addWidget(self.lineEdit_rights_binaries_label, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox_2, 1, 0, 1, 2)
        self.lineEdit_rights_information = QtWidgets.QLineEdit(provider_rights_Dialog)
        self.lineEdit_rights_information.setObjectName("lineEdit_rights_information")
        self.gridLayout.addWidget(self.lineEdit_rights_information, 2, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(provider_rights_Dialog)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        self.toolButton_open_rights_info = QtWidgets.QToolButton(provider_rights_Dialog)
        self.toolButton_open_rights_info.setObjectName("toolButton_open_rights_info")
        self.gridLayout.addWidget(self.toolButton_open_rights_info, 3, 1, 1, 1)

        self.retranslateUi(provider_rights_Dialog)
        self.buttonBox.accepted.connect(provider_rights_Dialog.accept)
        self.buttonBox.rejected.connect(provider_rights_Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(provider_rights_Dialog)

    def retranslateUi(self, provider_rights_Dialog):
        _translate = QtCore.QCoreApplication.translate
        provider_rights_Dialog.setWindowTitle(_translate("provider_rights_Dialog", "Rechte- und Lizenzangaben bearbeiten"))
        self.groupBox.setTitle(_translate("provider_rights_Dialog", "Lizenz für Metadaten"))
        self.label.setText(_translate("provider_rights_Dialog", "URI:"))
        self.lineEdit_rights_metadata_uri.setPlaceholderText(_translate("provider_rights_Dialog", "http://creativecommons.org/publicdomain/zero/1.0/"))
        self.label_2.setText(_translate("provider_rights_Dialog", "Label:"))
        self.lineEdit_rights_metadata_label.setPlaceholderText(_translate("provider_rights_Dialog", "CC0 1.0 Universal (CC0 1.0) Public Domain Dedication"))
        self.groupBox_2.setTitle(_translate("provider_rights_Dialog", "Lizenz für Digitalisate"))
        self.label_3.setText(_translate("provider_rights_Dialog", "URI:"))
        self.label_4.setText(_translate("provider_rights_Dialog", "Label:"))
        self.lineEdit_rights_information.setPlaceholderText(_translate("provider_rights_Dialog", "Rechteinformation beim Datengeber zu klären."))
        self.label_5.setText(_translate("provider_rights_Dialog", "Rechteinformation:"))
        self.toolButton_open_rights_info.setText(_translate("provider_rights_Dialog", "Weitere Informationen zu in der DDB verwendbaren Lizenzen ..."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    provider_rights_Dialog = QtWidgets.QDialog()
    ui = Ui_provider_rights_Dialog()
    ui.setupUi(provider_rights_Dialog)
    provider_rights_Dialog.show()
    sys.exit(app.exec_())

