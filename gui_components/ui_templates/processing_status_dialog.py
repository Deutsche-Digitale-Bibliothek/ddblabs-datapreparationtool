# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'processing_status_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_processingStatusDialog(object):
    def setupUi(self, processingStatusDialog):
        processingStatusDialog.setObjectName("processingStatusDialog")
        processingStatusDialog.resize(460, 388)
        self.gridLayout = QtWidgets.QGridLayout(processingStatusDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(processingStatusDialog)
        self.label.setMaximumSize(QtCore.QSize(131, 131))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/main-window/transformation_button_icon.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.header_processing_status = QtWidgets.QLabel(processingStatusDialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.header_processing_status.setFont(font)
        self.header_processing_status.setScaledContents(True)
        self.header_processing_status.setWordWrap(True)
        self.header_processing_status.setObjectName("header_processing_status")
        self.horizontalLayout.addWidget(self.header_processing_status)
        self.label_processing_status = QtWidgets.QLabel(processingStatusDialog)
        self.label_processing_status.setObjectName("label_processing_status")
        self.horizontalLayout.addWidget(self.label_processing_status)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.groupBox_further_options = QtWidgets.QGroupBox(processingStatusDialog)
        self.groupBox_further_options.setObjectName("groupBox_further_options")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_further_options)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pushButton_open_processing_output = QtWidgets.QPushButton(self.groupBox_further_options)
        self.pushButton_open_processing_output.setObjectName("pushButton_open_processing_output")
        self.gridLayout_2.addWidget(self.pushButton_open_processing_output, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(214, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox_further_options, 1, 0, 1, 1)
        self.buttonBox_close_status_dialog = QtWidgets.QDialogButtonBox(processingStatusDialog)
        self.buttonBox_close_status_dialog.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox_close_status_dialog.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox_close_status_dialog.setObjectName("buttonBox_close_status_dialog")
        self.gridLayout.addWidget(self.buttonBox_close_status_dialog, 2, 0, 1, 1)

        self.retranslateUi(processingStatusDialog)
        self.buttonBox_close_status_dialog.accepted.connect(processingStatusDialog.accept)
        self.buttonBox_close_status_dialog.rejected.connect(processingStatusDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(processingStatusDialog)

    def retranslateUi(self, processingStatusDialog):
        _translate = QtCore.QCoreApplication.translate
        processingStatusDialog.setWindowTitle(_translate("processingStatusDialog", "Prozessierung abgeschlossen"))
        self.header_processing_status.setText(_translate("processingStatusDialog", "Prozessierung abgeschlossen:"))
        self.label_processing_status.setText(_translate("processingStatusDialog", "TextLabel"))
        self.groupBox_further_options.setTitle(_translate("processingStatusDialog", "Weiterführende Optionen"))
        self.pushButton_open_processing_output.setText(_translate("processingStatusDialog", "Ausgabe-Ordner öffnen"))

from gui_components.ui_templates import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    processingStatusDialog = QtWidgets.QDialog()
    ui = Ui_processingStatusDialog()
    ui.setupUi(processingStatusDialog)
    processingStatusDialog.show()
    sys.exit(app.exec_())

