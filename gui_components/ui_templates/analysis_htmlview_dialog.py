# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'analysis_htmlview_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_analysisHtmlViewDialog(object):
    def setupUi(self, analysisHtmlViewDialog):
        analysisHtmlViewDialog.setObjectName("analysisHtmlViewDialog")
        analysisHtmlViewDialog.resize(1038, 753)
        self.gridLayout_2 = QtWidgets.QGridLayout(analysisHtmlViewDialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox = QtWidgets.QGroupBox(analysisHtmlViewDialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setScaledContents(True)
        self.label.setWordWrap(False)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.comboBox_statistics_file = QtWidgets.QComboBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_statistics_file.sizePolicy().hasHeightForWidth())
        self.comboBox_statistics_file.setSizePolicy(sizePolicy)
        self.comboBox_statistics_file.setObjectName("comboBox_statistics_file")
        self.horizontalLayout.addWidget(self.comboBox_statistics_file)
        self.label_filter_type = QtWidgets.QLabel(self.groupBox)
        self.label_filter_type.setScaledContents(True)
        self.label_filter_type.setObjectName("label_filter_type")
        self.horizontalLayout.addWidget(self.label_filter_type)
        self.comboBox_filter_type = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_filter_type.setObjectName("comboBox_filter_type")
        self.comboBox_filter_type.addItem("")
        self.comboBox_filter_type.addItem("")
        self.comboBox_filter_type.addItem("")
        self.horizontalLayout.addWidget(self.comboBox_filter_type)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.webEngineView = QtWebEngineWidgets.QWebEngineView(self.groupBox)
        self.webEngineView.setUrl(QtCore.QUrl("about:blank"))
        self.webEngineView.setObjectName("webEngineView")
        self.gridLayout.addWidget(self.webEngineView, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_open_statistics_in_browser = QtWidgets.QPushButton(analysisHtmlViewDialog)
        self.pushButton_open_statistics_in_browser.setObjectName("pushButton_open_statistics_in_browser")
        self.horizontalLayout_2.addWidget(self.pushButton_open_statistics_in_browser)
        self.buttonBox = QtWidgets.QDialogButtonBox(analysisHtmlViewDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_2.addWidget(self.buttonBox)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)

        self.retranslateUi(analysisHtmlViewDialog)
        self.buttonBox.accepted.connect(analysisHtmlViewDialog.accept)
        self.buttonBox.rejected.connect(analysisHtmlViewDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(analysisHtmlViewDialog)

    def retranslateUi(self, analysisHtmlViewDialog):
        _translate = QtCore.QCoreApplication.translate
        analysisHtmlViewDialog.setWindowTitle(_translate("analysisHtmlViewDialog", "Analyseergebnisse"))
        self.groupBox.setTitle(_translate("analysisHtmlViewDialog", "Analyseergebnisse"))
        self.label.setText(_translate("analysisHtmlViewDialog", "Statistische Auswertung auswählen:"))
        self.label_filter_type.setText(_translate("analysisHtmlViewDialog", "Nach Typ filtern:"))
        self.comboBox_filter_type.setItemText(0, _translate("analysisHtmlViewDialog", "Bestände"))
        self.comboBox_filter_type.setItemText(1, _translate("analysisHtmlViewDialog", "Gliederungsgruppen"))
        self.comboBox_filter_type.setItemText(2, _translate("analysisHtmlViewDialog", "Verzeichnungseinheiten"))
        self.pushButton_open_statistics_in_browser.setText(_translate("analysisHtmlViewDialog", "Im Browser öffnen ..."))

from PyQt5 import QtWebEngineWidgets

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    analysisHtmlViewDialog = QtWidgets.QDialog()
    ui = Ui_analysisHtmlViewDialog()
    ui.setupUi(analysisHtmlViewDialog)
    analysisHtmlViewDialog.show()
    sys.exit(app.exec_())

