# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'html_info_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_htmlInfoDialog(object):
    def setupUi(self, htmlInfoDialog):
        htmlInfoDialog.setObjectName("htmlInfoDialog")
        htmlInfoDialog.resize(1017, 582)
        self.gridLayout = QtWidgets.QGridLayout(htmlInfoDialog)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.webEngineView_info_dialog = QtWebEngineWidgets.QWebEngineView(htmlInfoDialog)
        self.webEngineView_info_dialog.setUrl(QtCore.QUrl("about:blank"))
        self.webEngineView_info_dialog.setObjectName("webEngineView_info_dialog")
        self.gridLayout.addWidget(self.webEngineView_info_dialog, 0, 0, 1, 1)

        self.retranslateUi(htmlInfoDialog)
        QtCore.QMetaObject.connectSlotsByName(htmlInfoDialog)

    def retranslateUi(self, htmlInfoDialog):
        _translate = QtCore.QCoreApplication.translate
        htmlInfoDialog.setWindowTitle(_translate("htmlInfoDialog", "Willkommen"))
from PyQt5 import QtWebEngineWidgets


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    htmlInfoDialog = QtWidgets.QDialog()
    ui = Ui_htmlInfoDialog()
    ui.setupUi(htmlInfoDialog)
    htmlInfoDialog.show()
    sys.exit(app.exec_())
