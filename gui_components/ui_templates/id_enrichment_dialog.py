# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'id_enrichment_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_idEnrichmentDialog(object):
    def setupUi(self, idEnrichmentDialog):
        idEnrichmentDialog.setObjectName("idEnrichmentDialog")
        idEnrichmentDialog.setWindowModality(QtCore.Qt.WindowModal)
        idEnrichmentDialog.resize(575, 342)
        idEnrichmentDialog.setModal(True)
        self.gridLayout = QtWidgets.QGridLayout(idEnrichmentDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.toolButton_id_enrichment_path = QtWidgets.QToolButton(idEnrichmentDialog)
        self.toolButton_id_enrichment_path.setObjectName("toolButton_id_enrichment_path")
        self.gridLayout.addWidget(self.toolButton_id_enrichment_path, 1, 3, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 83, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 2, 1, 1)
        self.toolButton_id_enrichment_remove_entry = QtWidgets.QToolButton(idEnrichmentDialog)
        self.toolButton_id_enrichment_remove_entry.setObjectName("toolButton_id_enrichment_remove_entry")
        self.gridLayout.addWidget(self.toolButton_id_enrichment_remove_entry, 2, 2, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(idEnrichmentDialog)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.checkBox_id_enrichment_process_findbuch = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_id_enrichment_process_findbuch.setObjectName("checkBox_id_enrichment_process_findbuch")
        self.verticalLayout_3.addWidget(self.checkBox_id_enrichment_process_findbuch)
        self.checkBox_id_enrichment_process_tektonik = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_id_enrichment_process_tektonik.setObjectName("checkBox_id_enrichment_process_tektonik")
        self.verticalLayout_3.addWidget(self.checkBox_id_enrichment_process_tektonik)
        self.gridLayout.addWidget(self.groupBox_2, 0, 0, 2, 1)
        self.groupBox = QtWidgets.QGroupBox(idEnrichmentDialog)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.checkBox_id_enrichment_process_class = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_id_enrichment_process_class.setObjectName("checkBox_id_enrichment_process_class")
        self.verticalLayout.addWidget(self.checkBox_id_enrichment_process_class)
        self.checkBox_id_enrichment_process_series = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_id_enrichment_process_series.setObjectName("checkBox_id_enrichment_process_series")
        self.verticalLayout.addWidget(self.checkBox_id_enrichment_process_series)
        self.checkBox_id_enrichment_process_file = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_id_enrichment_process_file.setObjectName("checkBox_id_enrichment_process_file")
        self.verticalLayout.addWidget(self.checkBox_id_enrichment_process_file)
        self.checkBox_id_enrichment_process_item = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_id_enrichment_process_item.setObjectName("checkBox_id_enrichment_process_item")
        self.verticalLayout.addWidget(self.checkBox_id_enrichment_process_item)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.lineEdit_id_prefix = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_id_prefix.setClearButtonEnabled(True)
        self.lineEdit_id_prefix.setObjectName("lineEdit_id_prefix")
        self.horizontalLayout.addWidget(self.lineEdit_id_prefix)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addWidget(self.groupBox, 3, 0, 2, 1)
        self.line = QtWidgets.QFrame(idEnrichmentDialog)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 0, 1, 5, 1)
        self.listWidget_id_enrichment_files = QtWidgets.QListWidget(idEnrichmentDialog)
        self.listWidget_id_enrichment_files.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.listWidget_id_enrichment_files.setObjectName("listWidget_id_enrichment_files")
        self.gridLayout.addWidget(self.listWidget_id_enrichment_files, 1, 2, 1, 1)
        self.label = QtWidgets.QLabel(idEnrichmentDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 2, 1, 2)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.checkBox_id_enrichment_replace_existing = QtWidgets.QCheckBox(idEnrichmentDialog)
        self.checkBox_id_enrichment_replace_existing.setObjectName("checkBox_id_enrichment_replace_existing")
        self.verticalLayout_2.addWidget(self.checkBox_id_enrichment_replace_existing)
        self.buttonBox_id_enrichment = QtWidgets.QDialogButtonBox(idEnrichmentDialog)
        self.buttonBox_id_enrichment.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox_id_enrichment.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox_id_enrichment.setObjectName("buttonBox_id_enrichment")
        self.verticalLayout_2.addWidget(self.buttonBox_id_enrichment)
        self.gridLayout.addLayout(self.verticalLayout_2, 4, 2, 1, 2)

        self.retranslateUi(idEnrichmentDialog)
        self.buttonBox_id_enrichment.accepted.connect(idEnrichmentDialog.accept)
        self.buttonBox_id_enrichment.rejected.connect(idEnrichmentDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(idEnrichmentDialog)

    def retranslateUi(self, idEnrichmentDialog):
        _translate = QtCore.QCoreApplication.translate
        idEnrichmentDialog.setWindowTitle(_translate("idEnrichmentDialog", "Identifier anreichern"))
        self.toolButton_id_enrichment_path.setText(_translate("idEnrichmentDialog", "..."))
        self.toolButton_id_enrichment_remove_entry.setText(_translate("idEnrichmentDialog", "Eintrag entfernen"))
        self.groupBox_2.setTitle(_translate("idEnrichmentDialog", "eingrenzen auf:"))
        self.checkBox_id_enrichment_process_findbuch.setText(_translate("idEnrichmentDialog", "Findbuch"))
        self.checkBox_id_enrichment_process_tektonik.setText(_translate("idEnrichmentDialog", "Tektonik"))
        self.groupBox.setTitle(_translate("idEnrichmentDialog", "auf folgenden Ebenen anreichern:"))
        self.checkBox_id_enrichment_process_class.setText(_translate("idEnrichmentDialog", "Klassifikationsgruppen (\"class\")"))
        self.checkBox_id_enrichment_process_series.setText(_translate("idEnrichmentDialog", "Serien (\"series\")"))
        self.checkBox_id_enrichment_process_file.setText(_translate("idEnrichmentDialog", "Verzeichnungseinheiten (\"file\")"))
        self.checkBox_id_enrichment_process_item.setText(_translate("idEnrichmentDialog", "Teil / Vorgang (\"item\")"))
        self.label_2.setText(_translate("idEnrichmentDialog", "Präfix für Identifier: "))
        self.lineEdit_id_prefix.setPlaceholderText(_translate("idEnrichmentDialog", "prov_"))
        self.label.setText(_translate("idEnrichmentDialog", "Anzureichernden Dateien:"))
        self.checkBox_id_enrichment_replace_existing.setText(_translate("idEnrichmentDialog", "bestehende Identifier ersetzen"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    idEnrichmentDialog = QtWidgets.QDialog()
    ui = Ui_idEnrichmentDialog()
    ui.setupUi(idEnrichmentDialog)
    idEnrichmentDialog.show()
    sys.exit(app.exec_())

