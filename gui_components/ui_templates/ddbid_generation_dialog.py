# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ddbid_generation_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ddbidGenerationDialog(object):
    def setupUi(self, ddbidGenerationDialog):
        ddbidGenerationDialog.setObjectName("ddbidGenerationDialog")
        ddbidGenerationDialog.setWindowModality(QtCore.Qt.WindowModal)
        ddbidGenerationDialog.resize(755, 400)
        ddbidGenerationDialog.setModal(True)
        self.gridLayout = QtWidgets.QGridLayout(ddbidGenerationDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label_provider_id = QtWidgets.QLabel(ddbidGenerationDialog)
        self.label_provider_id.setObjectName("label_provider_id")
        self.gridLayout.addWidget(self.label_provider_id, 0, 0, 1, 1)
        self.lineEdit_provider_id = QtWidgets.QLineEdit(ddbidGenerationDialog)
        self.lineEdit_provider_id.setObjectName("lineEdit_provider_id")
        self.gridLayout.addWidget(self.lineEdit_provider_id, 0, 1, 1, 1)
        self.line = QtWidgets.QFrame(ddbidGenerationDialog)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 0, 2, 5, 1)
        self.label = QtWidgets.QLabel(ddbidGenerationDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 3, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(ddbidGenerationDialog)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.checkBox_ddbid_generation_process_findbuch = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_ddbid_generation_process_findbuch.setObjectName("checkBox_ddbid_generation_process_findbuch")
        self.verticalLayout_3.addWidget(self.checkBox_ddbid_generation_process_findbuch)
        self.checkBox_ddbid_generation_process_tektonik = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_ddbid_generation_process_tektonik.setObjectName("checkBox_ddbid_generation_process_tektonik")
        self.verticalLayout_3.addWidget(self.checkBox_ddbid_generation_process_tektonik)
        self.gridLayout.addWidget(self.groupBox_2, 1, 0, 2, 2)
        self.listWidget_ddbid_generation_files = QtWidgets.QListWidget(ddbidGenerationDialog)
        self.listWidget_ddbid_generation_files.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.listWidget_ddbid_generation_files.setObjectName("listWidget_ddbid_generation_files")
        self.gridLayout.addWidget(self.listWidget_ddbid_generation_files, 1, 3, 1, 1)
        self.toolButton_ddbid_generation_path = QtWidgets.QToolButton(ddbidGenerationDialog)
        self.toolButton_ddbid_generation_path.setObjectName("toolButton_ddbid_generation_path")
        self.gridLayout.addWidget(self.toolButton_ddbid_generation_path, 1, 4, 1, 1)
        self.toolButton_ddbid_generation_remove_entry = QtWidgets.QToolButton(ddbidGenerationDialog)
        self.toolButton_ddbid_generation_remove_entry.setObjectName("toolButton_ddbid_generation_remove_entry")
        self.gridLayout.addWidget(self.toolButton_ddbid_generation_remove_entry, 2, 3, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(ddbidGenerationDialog)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.checkBox_ddbid_generation_process_class = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_ddbid_generation_process_class.setObjectName("checkBox_ddbid_generation_process_class")
        self.verticalLayout.addWidget(self.checkBox_ddbid_generation_process_class)
        self.checkBox_ddbid_generation_process_series = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_ddbid_generation_process_series.setObjectName("checkBox_ddbid_generation_process_series")
        self.verticalLayout.addWidget(self.checkBox_ddbid_generation_process_series)
        self.checkBox_ddbid_generation_process_file = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_ddbid_generation_process_file.setObjectName("checkBox_ddbid_generation_process_file")
        self.verticalLayout.addWidget(self.checkBox_ddbid_generation_process_file)
        self.checkBox_ddbid_generation_process_item = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_ddbid_generation_process_item.setObjectName("checkBox_ddbid_generation_process_item")
        self.verticalLayout.addWidget(self.checkBox_ddbid_generation_process_item)
        self.gridLayout.addWidget(self.groupBox, 3, 0, 2, 2)
        self.frame_ddbid_generation_infobox = QtWidgets.QFrame(ddbidGenerationDialog)
        self.frame_ddbid_generation_infobox.setEnabled(True)
        self.frame_ddbid_generation_infobox.setStyleSheet("background-color: rgba(164, 219, 255, 235);")
        self.frame_ddbid_generation_infobox.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_ddbid_generation_infobox.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_ddbid_generation_infobox.setObjectName("frame_ddbid_generation_infobox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_ddbid_generation_infobox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.icon_ddbid_generation_infobox = QtWidgets.QLabel(self.frame_ddbid_generation_infobox)
        self.icon_ddbid_generation_infobox.setMaximumSize(QtCore.QSize(40, 40))
        self.icon_ddbid_generation_infobox.setText("")
        self.icon_ddbid_generation_infobox.setPixmap(QtGui.QPixmap(":/transformation-status-dialog/ic_info_black_48dp.png"))
        self.icon_ddbid_generation_infobox.setScaledContents(True)
        self.icon_ddbid_generation_infobox.setWordWrap(False)
        self.icon_ddbid_generation_infobox.setObjectName("icon_ddbid_generation_infobox")
        self.horizontalLayout_2.addWidget(self.icon_ddbid_generation_infobox)
        self.label_ddbid_generation_infobox = QtWidgets.QLabel(self.frame_ddbid_generation_infobox)
        self.label_ddbid_generation_infobox.setScaledContents(True)
        self.label_ddbid_generation_infobox.setWordWrap(True)
        self.label_ddbid_generation_infobox.setObjectName("label_ddbid_generation_infobox")
        self.horizontalLayout_2.addWidget(self.label_ddbid_generation_infobox)
        self.gridLayout.addWidget(self.frame_ddbid_generation_infobox, 3, 3, 1, 2)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.buttonBox_ddbid_generation = QtWidgets.QDialogButtonBox(ddbidGenerationDialog)
        self.buttonBox_ddbid_generation.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox_ddbid_generation.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox_ddbid_generation.setObjectName("buttonBox_ddbid_generation")
        self.verticalLayout_2.addWidget(self.buttonBox_ddbid_generation)
        self.gridLayout.addLayout(self.verticalLayout_2, 4, 3, 1, 1)

        self.retranslateUi(ddbidGenerationDialog)
        self.buttonBox_ddbid_generation.accepted.connect(ddbidGenerationDialog.accept)
        self.buttonBox_ddbid_generation.rejected.connect(ddbidGenerationDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ddbidGenerationDialog)

    def retranslateUi(self, ddbidGenerationDialog):
        _translate = QtCore.QCoreApplication.translate
        ddbidGenerationDialog.setWindowTitle(_translate("ddbidGenerationDialog", "DDB-IDs generieren"))
        self.label_provider_id.setText(_translate("ddbidGenerationDialog", "Provider-ID: "))
        self.label.setText(_translate("ddbidGenerationDialog", "DDB-IDs aus Dateien berechnen:"))
        self.groupBox_2.setTitle(_translate("ddbidGenerationDialog", "eingrenzen auf:"))
        self.checkBox_ddbid_generation_process_findbuch.setText(_translate("ddbidGenerationDialog", "Findbuch"))
        self.checkBox_ddbid_generation_process_tektonik.setText(_translate("ddbidGenerationDialog", "Tektonik"))
        self.toolButton_ddbid_generation_path.setText(_translate("ddbidGenerationDialog", "..."))
        self.toolButton_ddbid_generation_remove_entry.setText(_translate("ddbidGenerationDialog", "Eintrag entfernen"))
        self.groupBox.setTitle(_translate("ddbidGenerationDialog", "auf folgenden Ebenen DDB-IDs berechnen:"))
        self.checkBox_ddbid_generation_process_class.setText(_translate("ddbidGenerationDialog", "Klassifikationsgruppen (\"class\")"))
        self.checkBox_ddbid_generation_process_series.setText(_translate("ddbidGenerationDialog", "Serien (\"series\")"))
        self.checkBox_ddbid_generation_process_file.setText(_translate("ddbidGenerationDialog", "Verzeichnungseinheiten (\"file\")"))
        self.checkBox_ddbid_generation_process_item.setText(_translate("ddbidGenerationDialog", "Teil / Vorgang (\"item\")"))
        self.label_ddbid_generation_infobox.setText(_translate("ddbidGenerationDialog", "<html><head/><body><p>Nach Klick auf &quot;OK&quot; wird für die ausgewählten Dateien auf den gewählten Ebenen eine DDB-ID-Liste als Textdatei sowie eine Konkordanz zwischen Origin-ID und DDB-ID im XML-Format erstellt.</p></body></html>"))

from gui_components.ui_templates import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ddbidGenerationDialog = QtWidgets.QDialog()
    ui = Ui_ddbidGenerationDialog()
    ui.setupUi(ddbidGenerationDialog)
    ddbidGenerationDialog.show()
    sys.exit(app.exec_())

