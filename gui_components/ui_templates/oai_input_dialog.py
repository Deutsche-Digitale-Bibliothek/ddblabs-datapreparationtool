# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'oai_input_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_oaiInputDialog(object):
    def setupUi(self, oaiInputDialog):
        oaiInputDialog.setObjectName("oaiInputDialog")
        oaiInputDialog.resize(486, 509)
        self.gridLayout_3 = QtWidgets.QGridLayout(oaiInputDialog)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label = QtWidgets.QLabel(oaiInputDialog)
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 2)
        self.lineEdit_oai_url = QtWidgets.QLineEdit(oaiInputDialog)
        self.lineEdit_oai_url.setObjectName("lineEdit_oai_url")
        self.gridLayout_3.addWidget(self.lineEdit_oai_url, 0, 2, 1, 2)
        self.label_6 = QtWidgets.QLabel(oaiInputDialog)
        self.label_6.setMaximumSize(QtCore.QSize(25, 25))
        self.label_6.setText("")
        self.label_6.setPixmap(QtGui.QPixmap(":/oai-input-dialog/info_icon.png"))
        self.label_6.setScaledContents(True)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 0, 4, 1, 1)
        self.label_2 = QtWidgets.QLabel(oaiInputDialog)
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 1, 0, 1, 2)
        self.lineEdit_metadata_prefix = QtWidgets.QLineEdit(oaiInputDialog)
        self.lineEdit_metadata_prefix.setObjectName("lineEdit_metadata_prefix")
        self.gridLayout_3.addWidget(self.lineEdit_metadata_prefix, 1, 2, 1, 2)
        self.label_7 = QtWidgets.QLabel(oaiInputDialog)
        self.label_7.setMaximumSize(QtCore.QSize(25, 25))
        self.label_7.setText("")
        self.label_7.setPixmap(QtGui.QPixmap(":/oai-input-dialog/info_icon.png"))
        self.label_7.setScaledContents(True)
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 1, 4, 1, 1)
        self.radioButton_oai_multiple = QtWidgets.QRadioButton(oaiInputDialog)
        self.radioButton_oai_multiple.setChecked(True)
        self.radioButton_oai_multiple.setObjectName("radioButton_oai_multiple")
        self.gridLayout_3.addWidget(self.radioButton_oai_multiple, 2, 0, 1, 3)
        spacerItem = QtWidgets.QSpacerItem(13, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 3, 0, 1, 1)
        self.groupBox_oai_multiple = QtWidgets.QGroupBox(oaiInputDialog)
        self.groupBox_oai_multiple.setEnabled(True)
        self.groupBox_oai_multiple.setObjectName("groupBox_oai_multiple")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_oai_multiple)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit_oai_set = QtWidgets.QLineEdit(self.groupBox_oai_multiple)
        self.lineEdit_oai_set.setObjectName("lineEdit_oai_set")
        self.gridLayout.addWidget(self.lineEdit_oai_set, 0, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox_oai_multiple)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox_oai_multiple)
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.toolButton_list_available_sets = QtWidgets.QToolButton(self.groupBox_oai_multiple)
        self.toolButton_list_available_sets.setObjectName("toolButton_list_available_sets")
        self.gridLayout.addWidget(self.toolButton_list_available_sets, 2, 1, 1, 1)
        self.lineEdit_oai_from_date = QtWidgets.QLineEdit(self.groupBox_oai_multiple)
        self.lineEdit_oai_from_date.setText("")
        self.lineEdit_oai_from_date.setObjectName("lineEdit_oai_from_date")
        self.gridLayout.addWidget(self.lineEdit_oai_from_date, 1, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.groupBox_oai_multiple)
        self.label_8.setMaximumSize(QtCore.QSize(25, 25))
        self.label_8.setText("")
        self.label_8.setPixmap(QtGui.QPixmap(":/oai-input-dialog/info_icon.png"))
        self.label_8.setScaledContents(True)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 0, 2, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.groupBox_oai_multiple)
        self.label_9.setMaximumSize(QtCore.QSize(25, 25))
        self.label_9.setText("")
        self.label_9.setPixmap(QtGui.QPixmap(":/oai-input-dialog/info_icon.png"))
        self.label_9.setScaledContents(True)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 1, 2, 1, 1)
        self.label_4.raise_()
        self.label_3.raise_()
        self.toolButton_list_available_sets.raise_()
        self.lineEdit_oai_set.raise_()
        self.lineEdit_oai_from_date.raise_()
        self.label_8.raise_()
        self.label_9.raise_()
        self.gridLayout_3.addWidget(self.groupBox_oai_multiple, 3, 1, 1, 3)
        self.radioButton_oai_single = QtWidgets.QRadioButton(oaiInputDialog)
        self.radioButton_oai_single.setObjectName("radioButton_oai_single")
        self.gridLayout_3.addWidget(self.radioButton_oai_single, 4, 0, 1, 3)
        spacerItem1 = QtWidgets.QSpacerItem(13, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem1, 5, 0, 1, 1)
        self.groupBox_oai_single = QtWidgets.QGroupBox(oaiInputDialog)
        self.groupBox_oai_single.setEnabled(False)
        self.groupBox_oai_single.setObjectName("groupBox_oai_single")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_oai_single)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_10 = QtWidgets.QLabel(self.groupBox_oai_single)
        self.label_10.setMaximumSize(QtCore.QSize(25, 25))
        self.label_10.setText("")
        self.label_10.setPixmap(QtGui.QPixmap(":/oai-input-dialog/info_icon.png"))
        self.label_10.setScaledContents(True)
        self.label_10.setObjectName("label_10")
        self.gridLayout_2.addWidget(self.label_10, 0, 2, 1, 1)
        self.lineEdit_oai_identifier = QtWidgets.QLineEdit(self.groupBox_oai_single)
        self.lineEdit_oai_identifier.setObjectName("lineEdit_oai_identifier")
        self.gridLayout_2.addWidget(self.lineEdit_oai_identifier, 0, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox_oai_single)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_oai_single, 5, 1, 1, 3)
        self.frame_oai_background_processing = QtWidgets.QFrame(oaiInputDialog)
        self.frame_oai_background_processing.setEnabled(True)
        self.frame_oai_background_processing.setStyleSheet("background-color: rgba(164, 219, 255, 235);")
        self.frame_oai_background_processing.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_oai_background_processing.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_oai_background_processing.setObjectName("frame_oai_background_processing")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_oai_background_processing)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.icon_oai_background_processing = QtWidgets.QLabel(self.frame_oai_background_processing)
        self.icon_oai_background_processing.setMaximumSize(QtCore.QSize(40, 40))
        self.icon_oai_background_processing.setText("")
        self.icon_oai_background_processing.setPixmap(QtGui.QPixmap(":/transformation-status-dialog/ic_info_black_48dp.png"))
        self.icon_oai_background_processing.setScaledContents(True)
        self.icon_oai_background_processing.setWordWrap(False)
        self.icon_oai_background_processing.setObjectName("icon_oai_background_processing")
        self.horizontalLayout_2.addWidget(self.icon_oai_background_processing)
        self.label_oai_background_processing = QtWidgets.QLabel(self.frame_oai_background_processing)
        self.label_oai_background_processing.setScaledContents(True)
        self.label_oai_background_processing.setWordWrap(True)
        self.label_oai_background_processing.setObjectName("label_oai_background_processing")
        self.horizontalLayout_2.addWidget(self.label_oai_background_processing)
        self.gridLayout_3.addWidget(self.frame_oai_background_processing, 6, 1, 1, 3)
        self.buttonBox = QtWidgets.QDialogButtonBox(oaiInputDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_3.addWidget(self.buttonBox, 7, 3, 1, 1)

        self.retranslateUi(oaiInputDialog)
        self.buttonBox.accepted.connect(oaiInputDialog.accept)
        self.buttonBox.rejected.connect(oaiInputDialog.reject)
        self.radioButton_oai_multiple.toggled['bool'].connect(self.groupBox_oai_multiple.setEnabled)
        self.radioButton_oai_single.toggled['bool'].connect(self.groupBox_oai_single.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(oaiInputDialog)

    def retranslateUi(self, oaiInputDialog):
        _translate = QtCore.QCoreApplication.translate
        oaiInputDialog.setWindowTitle(_translate("oaiInputDialog", "Dateien per OAI-PMH laden"))
        self.label.setText(_translate("oaiInputDialog", "URL des OAI-Endpoints:"))
        self.label_6.setToolTip(_translate("oaiInputDialog", "<html><head/><body><p><span style=\" font-weight:600;\">URL des OAI-Servers</span>, von dem Daten geladen werden sollen. Diese Angabe erhalten Sie von der jeweiligen Institution. Z.B.: <span style=\" font-style:italic;\">https://www.example.com/OAIHandler</span></p></body></html>"))
        self.label_2.setText(_translate("oaiInputDialog", "Metadata-Prefix:"))
        self.lineEdit_metadata_prefix.setPlaceholderText(_translate("oaiInputDialog", "ead"))
        self.label_7.setToolTip(_translate("oaiInputDialog", "<html><head/><body><p><span style=\" font-weight:600;\">Metadatenformat</span> der zu ladenden Daten. Standardmäßig wird &quot;<span style=\" font-weight:600;\">ead</span>&quot; verwendet. Nicht alle Server unterstützen EAD - im Zweifelsfall versuchen Sie es mit &quot;<span style=\" font-weight:600;\">oai_dc</span>&quot;.</p></body></html>"))
        self.radioButton_oai_multiple.setText(_translate("oaiInputDialog", "Mehrere Datensätze laden"))
        self.groupBox_oai_multiple.setTitle(_translate("oaiInputDialog", "Auswahl der Datensätze"))
        self.lineEdit_oai_set.setPlaceholderText(_translate("oaiInputDialog", "(alle Sets laden)"))
        self.label_4.setText(_translate("oaiInputDialog", "Zeitraum:"))
        self.label_3.setText(_translate("oaiInputDialog", "Set:"))
        self.toolButton_list_available_sets.setText(_translate("oaiInputDialog", "Verfügbare Sets ermitteln"))
        self.lineEdit_oai_from_date.setPlaceholderText(_translate("oaiInputDialog", "YYYY-MM-DD"))
        self.label_8.setToolTip(_translate("oaiInputDialog", "<html><head/><body><p>Über die Angabe eines Set-Identifiers können einzelne, <span style=\" font-weight:600;\">durch den Datengeber bestimmte Sets</span>, z.B. einzelne Bestandsgruppen, abgerufen werden. Sets werden nicht von jedem OAI-Repository unterstützt. Wählen Sie &quot;<span style=\" font-weight:600;\">Verfügbare Sets ermitteln</span>&quot;, um eine Auflistung der verfügbaren Partitionen zu erhalten.</p></body></html>"))
        self.label_9.setToolTip(_translate("oaiInputDialog", "<html><head/><body><p>Datensätze <span style=\" font-weight:600;\">ab einem bestimmten Datum</span> laden, z.B.: <span style=\" font-style:italic;\">2017-01-01</span>. Standardmäßig wird keine zeitliche Einschränkung vorgenommen.</p></body></html>"))
        self.radioButton_oai_single.setText(_translate("oaiInputDialog", "Einzelnen Datensatz laden"))
        self.groupBox_oai_single.setTitle(_translate("oaiInputDialog", "Datensatz-ID"))
        self.label_10.setToolTip(_translate("oaiInputDialog", "Identifier eines einzelnen Datensatzes, der geladen werden soll. Z.B.: oai:ead-DE1234-00001. "))
        self.label_5.setText(_translate("oaiInputDialog", "Identifier:"))
        self.label_oai_background_processing.setText(_translate("oaiInputDialog", "Nach Klick auf \"OK\" werden die Daten geladen. Den Fortschritt können Sie über die Statusleiste und die Logdatei verfolgen."))

from gui_components.ui_templates import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    oaiInputDialog = QtWidgets.QDialog()
    ui = Ui_oaiInputDialog()
    ui.setupUi(oaiInputDialog)
    oaiInputDialog.show()
    sys.exit(app.exec_())

