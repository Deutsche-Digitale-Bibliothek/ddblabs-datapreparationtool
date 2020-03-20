# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_aboutDialog(object):
    def setupUi(self, aboutDialog):
        aboutDialog.setObjectName("aboutDialog")
        aboutDialog.setEnabled(True)
        aboutDialog.resize(400, 446)
        aboutDialog.setMinimumSize(QtCore.QSize(400, 446))
        aboutDialog.setAutoFillBackground(False)
        aboutDialog.setSizeGripEnabled(False)
        aboutDialog.setModal(False)
        self.gridLayout_2 = QtWidgets.QGridLayout(aboutDialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_about_dialog_version = QtWidgets.QLabel(aboutDialog)
        self.label_about_dialog_version.setScaledContents(True)
        self.label_about_dialog_version.setAlignment(QtCore.Qt.AlignCenter)
        self.label_about_dialog_version.setWordWrap(False)
        self.label_about_dialog_version.setObjectName("label_about_dialog_version")
        self.gridLayout.addWidget(self.label_about_dialog_version, 2, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(aboutDialog)
        self.label_7.setMinimumSize(QtCore.QSize(131, 51))
        self.label_7.setMaximumSize(QtCore.QSize(131, 51))
        self.label_7.setText("")
        self.label_7.setPixmap(QtGui.QPixmap(":/about-dialog/apd-logo.png"))
        self.label_7.setScaledContents(True)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 2, 1, 1, 1, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.label = QtWidgets.QLabel(aboutDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(151, 151))
        self.label.setMaximumSize(QtCore.QSize(151, 151))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/about-dialog/list.png"))
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setOpenExternalLinks(False)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 1, 1, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_6 = QtWidgets.QLabel(aboutDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setMinimumSize(QtCore.QSize(111, 51))
        self.label_6.setMaximumSize(QtCore.QSize(111, 51))
        self.label_6.setText("")
        self.label_6.setPixmap(QtGui.QPixmap(":/about-dialog/ddb-logo.png"))
        self.label_6.setScaledContents(True)
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.gridLayout.addLayout(self.verticalLayout, 3, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(aboutDialog)
        self.label_2.setScaledContents(True)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.pushButton_opensource_components = QtWidgets.QPushButton(aboutDialog)
        self.pushButton_opensource_components.setObjectName("pushButton_opensource_components")
        self.gridLayout.addWidget(self.pushButton_opensource_components, 4, 0, 1, 1)
        self.label_about_dialog_revision = QtWidgets.QLabel(aboutDialog)
        self.label_about_dialog_revision.setAlignment(QtCore.Qt.AlignCenter)
        self.label_about_dialog_revision.setObjectName("label_about_dialog_revision")
        self.gridLayout.addWidget(self.label_about_dialog_revision, 3, 0, 1, 1)
        self.buttonOpenGithub = QtWidgets.QPushButton(aboutDialog)
        self.buttonOpenGithub.setEnabled(True)
        self.buttonOpenGithub.setAutoDefault(False)
        self.buttonOpenGithub.setDefault(False)
        self.buttonOpenGithub.setFlat(False)
        self.buttonOpenGithub.setObjectName("buttonOpenGithub")
        self.gridLayout.addWidget(self.buttonOpenGithub, 5, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)

        self.retranslateUi(aboutDialog)
        QtCore.QMetaObject.connectSlotsByName(aboutDialog)

    def retranslateUi(self, aboutDialog):
        _translate = QtCore.QCoreApplication.translate
        aboutDialog.setWindowTitle(_translate("aboutDialog", "Über Data Preparation Tool"))
        self.label_about_dialog_version.setText(_translate("aboutDialog", "Version x.y (Pre-Release)"))
        self.label_2.setText(_translate("aboutDialog", "<html><head/><body><p><span style=\" font-weight:600;\">Data Preparation Tool</span></p><p>Ein Werkzeug zur Analyse und Aufbereitung von EAD(DDB)-Dateien für die Lieferung an DDB und Archivportal-D. </p><p>Entwickelt und zur Verfügung gestellt durch die DDB-Fachstelle Archiv.</p></body></html>"))
        self.pushButton_opensource_components.setText(_translate("aboutDialog", "Open-Source-Komponenten"))
        self.label_about_dialog_revision.setText(_translate("aboutDialog", "Revision: f28a591"))
        self.buttonOpenGithub.setText(_translate("aboutDialog", "Fork me on Github"))

from gui_components.ui_templates import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    aboutDialog = QtWidgets.QDialog()
    ui = Ui_aboutDialog()
    ui.setupUi(aboutDialog)
    aboutDialog.show()
    sys.exit(app.exec_())
