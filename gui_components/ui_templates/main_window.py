# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(444, 576)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_4.setObjectName("gridLayout_4")
        spacerItem = QtWidgets.QSpacerItem(20, 15, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_4.addItem(spacerItem, 2, 0, 1, 1)
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.default_message = QtWidgets.QWidget()
        self.default_message.setObjectName("default_message")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.default_message)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.label_welcome_info_box = QtWidgets.QLabel(self.default_message)
        self.label_welcome_info_box.setStyleSheet("background-image: url(:/main-window/info_box_bg.png);")
        self.label_welcome_info_box.setScaledContents(True)
        self.label_welcome_info_box.setWordWrap(True)
        self.label_welcome_info_box.setIndent(7)
        self.label_welcome_info_box.setObjectName("label_welcome_info_box")
        self.gridLayout_8.addWidget(self.label_welcome_info_box, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.default_message)
        self.first_launch_message = QtWidgets.QWidget()
        self.first_launch_message.setObjectName("first_launch_message")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.first_launch_message)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.label_welcome_info_box_2 = QtWidgets.QLabel(self.first_launch_message)
        self.label_welcome_info_box_2.setStyleSheet("background-image: url(:/main-window/info_box_bg.png);")
        self.label_welcome_info_box_2.setScaledContents(True)
        self.label_welcome_info_box_2.setWordWrap(True)
        self.label_welcome_info_box_2.setIndent(7)
        self.label_welcome_info_box_2.setObjectName("label_welcome_info_box_2")
        self.gridLayout_9.addWidget(self.label_welcome_info_box_2, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.first_launch_message)
        self.gridLayout_4.addWidget(self.stackedWidget, 5, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_provider = QtWidgets.QLabel(self.centralwidget)
        self.label_provider.setScaledContents(True)
        self.label_provider.setObjectName("label_provider")
        self.gridLayout.addWidget(self.label_provider, 0, 0, 1, 1)
        self.toolButton_new_provider = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_new_provider.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/main-window/add_provider.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_new_provider.setIcon(icon)
        self.toolButton_new_provider.setObjectName("toolButton_new_provider")
        self.gridLayout.addWidget(self.toolButton_new_provider, 0, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 4, 1, 1)
        self.toolButton_refresh_providers = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_refresh_providers.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/main-window/reload.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_refresh_providers.setIcon(icon1)
        self.toolButton_refresh_providers.setObjectName("toolButton_refresh_providers")
        self.gridLayout.addWidget(self.toolButton_refresh_providers, 0, 3, 1, 1)
        self.comboBox_provider = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_provider.setObjectName("comboBox_provider")
        self.comboBox_provider.addItem("")
        self.comboBox_provider.addItem("")
        self.comboBox_provider.addItem("")
        self.gridLayout.addWidget(self.comboBox_provider, 0, 1, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout, 1, 0, 1, 1)
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.pushButton_startTransformation = QtWidgets.QPushButton(self.centralwidget)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/main-window/transformation_button_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_startTransformation.setIcon(icon2)
        self.pushButton_startTransformation.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_startTransformation.setObjectName("pushButton_startTransformation")
        self.gridLayout_5.addWidget(self.pushButton_startTransformation, 0, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem2, 0, 2, 1, 1)
        self.pushButton_startAnalyse = QtWidgets.QPushButton(self.centralwidget)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/main-window/analysis_button_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_startAnalyse.setIcon(icon3)
        self.pushButton_startAnalyse.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_startAnalyse.setObjectName("pushButton_startAnalyse")
        self.gridLayout_5.addWidget(self.pushButton_startAnalyse, 0, 1, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_5, 4, 0, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setMinimumSize(QtCore.QSize(420, 291))
        self.tab.setObjectName("tab")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.toolButton_metsmods_settings_dialog = QtWidgets.QToolButton(self.tab)
        self.toolButton_metsmods_settings_dialog.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/main-window/settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_metsmods_settings_dialog.setIcon(icon4)
        self.toolButton_metsmods_settings_dialog.setObjectName("toolButton_metsmods_settings_dialog")
        self.gridLayout_2.addWidget(self.toolButton_metsmods_settings_dialog, 3, 3, 1, 1)
        self.pushButton_provider_metadata = QtWidgets.QPushButton(self.tab)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/main-window/institution.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_provider_metadata.setIcon(icon5)
        self.pushButton_provider_metadata.setObjectName("pushButton_provider_metadata")
        self.gridLayout_2.addWidget(self.pushButton_provider_metadata, 0, 0, 1, 2)
        self.checkBox_binaries = QtWidgets.QCheckBox(self.tab)
        self.checkBox_binaries.setObjectName("checkBox_binaries")
        self.gridLayout_2.addWidget(self.checkBox_binaries, 2, 0, 1, 1)
        self.checkBox_metsmods = QtWidgets.QCheckBox(self.tab)
        self.checkBox_metsmods.setObjectName("checkBox_metsmods")
        self.gridLayout_2.addWidget(self.checkBox_metsmods, 3, 0, 1, 2)
        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setMaximumSize(QtCore.QSize(25, 25))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap(":/main-window/info_icon.png"))
        self.label_4.setScaledContents(True)
        self.label_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 1, 3, 1, 1)
        self.pushButton_provider_scripts = QtWidgets.QPushButton(self.tab)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/main-window/provider_modules.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_provider_scripts.setIcon(icon6)
        self.pushButton_provider_scripts.setObjectName("pushButton_provider_scripts")
        self.gridLayout_2.addWidget(self.pushButton_provider_scripts, 1, 0, 1, 2)
        self.gridLayout_6.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_2.sizePolicy().hasHeightForWidth())
        self.tab_2.setSizePolicy(sizePolicy)
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_5 = QtWidgets.QLabel(self.tab_2)
        self.label_5.setMaximumSize(QtCore.QSize(25, 25))
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap(":/main-window/info_icon.png"))
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 0, 2, 1, 1)
        self.checkBox_tektonik_enrichment = QtWidgets.QCheckBox(self.tab_2)
        self.checkBox_tektonik_enrichment.setObjectName("checkBox_tektonik_enrichment")
        self.gridLayout_3.addWidget(self.checkBox_tektonik_enrichment, 0, 0, 1, 2)
        self.checkBox_metadata_previews = QtWidgets.QCheckBox(self.tab_2)
        self.checkBox_metadata_previews.setObjectName("checkBox_metadata_previews")
        self.gridLayout_3.addWidget(self.checkBox_metadata_previews, 2, 0, 1, 2)
        self.checkBox_analysis = QtWidgets.QCheckBox(self.tab_2)
        self.checkBox_analysis.setObjectName("checkBox_analysis")
        self.gridLayout_3.addWidget(self.checkBox_analysis, 1, 0, 1, 2)
        self.toolButton_preview_testset = QtWidgets.QToolButton(self.tab_2)
        self.toolButton_preview_testset.setText("")
        self.toolButton_preview_testset.setIcon(icon4)
        self.toolButton_preview_testset.setObjectName("toolButton_preview_testset")
        self.gridLayout_3.addWidget(self.toolButton_preview_testset, 2, 2, 1, 1)
        self.gridLayout_7.addLayout(self.gridLayout_3, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout_4.addWidget(self.tabWidget, 3, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 444, 22))
        self.menubar.setObjectName("menubar")
        self.menuDatei = QtWidgets.QMenu(self.menubar)
        self.menuDatei.setObjectName("menuDatei")
        self.menu_ber = QtWidgets.QMenu(self.menubar)
        self.menu_ber.setObjectName("menu_ber")
        self.menuBearbeiten = QtWidgets.QMenu(self.menubar)
        self.menuBearbeiten.setObjectName("menuBearbeiten")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        self.menuValidierung = QtWidgets.QMenu(self.menubar)
        self.menuValidierung.setObjectName("menuValidierung")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionDatei_ffnen = QtWidgets.QAction(MainWindow)
        self.actionDatei_ffnen.setObjectName("actionDatei_ffnen")
        self.actionData_Preparation_Tool_beenden = QtWidgets.QAction(MainWindow)
        self.actionData_Preparation_Tool_beenden.setMenuRole(QtWidgets.QAction.TextHeuristicRole)
        self.actionData_Preparation_Tool_beenden.setObjectName("actionData_Preparation_Tool_beenden")
        self.actionStandard = QtWidgets.QAction(MainWindow)
        self.actionStandard.setCheckable(True)
        self.actionStandard.setChecked(True)
        self.actionStandard.setObjectName("actionStandard")
        self.actionKlassischer_Modus_altes_DPT = QtWidgets.QAction(MainWindow)
        self.actionKlassischer_Modus_altes_DPT.setCheckable(True)
        self.actionKlassischer_Modus_altes_DPT.setObjectName("actionKlassischer_Modus_altes_DPT")
        self.action_ber = QtWidgets.QAction(MainWindow)
        self.action_ber.setObjectName("action_ber")
        self.actionWeitere_Informationen_auf_DDBpro = QtWidgets.QAction(MainWindow)
        self.actionWeitere_Informationen_auf_DDBpro.setMenuRole(QtWidgets.QAction.TextHeuristicRole)
        self.actionWeitere_Informationen_auf_DDBpro.setObjectName("actionWeitere_Informationen_auf_DDBpro")
        self.menuInfoAbout = QtWidgets.QAction(MainWindow)
        self.menuInfoAbout.setObjectName("menuInfoAbout")
        self.menuInfoDDBpro = QtWidgets.QAction(MainWindow)
        self.menuInfoDDBpro.setObjectName("menuInfoDDBpro")
        self.actionEinstellungen = QtWidgets.QAction(MainWindow)
        self.actionEinstellungen.setObjectName("actionEinstellungen")
        self.menuGenerateDDBIDs = QtWidgets.QAction(MainWindow)
        self.menuGenerateDDBIDs.setEnabled(True)
        self.menuGenerateDDBIDs.setObjectName("menuGenerateDDBIDs")
        self.menuEnrichIDs = QtWidgets.QAction(MainWindow)
        self.menuEnrichIDs.setObjectName("menuEnrichIDs")
        self.actionLoadStandards = QtWidgets.QAction(MainWindow)
        self.actionLoadStandards.setObjectName("actionLoadStandards")
        self.menuInfoIntroscreen = QtWidgets.QAction(MainWindow)
        self.menuInfoIntroscreen.setObjectName("menuInfoIntroscreen")
        self.action_fetch_from_oai = QtWidgets.QAction(MainWindow)
        self.action_fetch_from_oai.setObjectName("action_fetch_from_oai")
        self.menuExcelMapping = QtWidgets.QAction(MainWindow)
        self.menuExcelMapping.setObjectName("menuExcelMapping")
        self.menuRightsInfo = QtWidgets.QAction(MainWindow)
        self.menuRightsInfo.setObjectName("menuRightsInfo")
        self.menuToggleRightsInfo = QtWidgets.QAction(MainWindow)
        self.menuToggleRightsInfo.setCheckable(True)
        self.menuToggleRightsInfo.setObjectName("menuToggleRightsInfo")
        self.menuToggleDdb2017Preprocessing = QtWidgets.QAction(MainWindow)
        self.menuToggleDdb2017Preprocessing.setCheckable(True)
        self.menuToggleDdb2017Preprocessing.setObjectName("menuToggleDdb2017Preprocessing")
        self.menuAggregatorInfo = QtWidgets.QAction(MainWindow)
        self.menuAggregatorInfo.setObjectName("menuAggregatorInfo")
        self.menuToggleAggregatorInfo = QtWidgets.QAction(MainWindow)
        self.menuToggleAggregatorInfo.setCheckable(True)
        self.menuToggleAggregatorInfo.setObjectName("menuToggleAggregatorInfo")
        self.menuToggleObsoleteObjects = QtWidgets.QAction(MainWindow)
        self.menuToggleObsoleteObjects.setCheckable(True)
        self.menuToggleObsoleteObjects.setObjectName("menuToggleObsoleteObjects")
        self.menuHeaderTransformationSettings = QtWidgets.QAction(MainWindow)
        self.menuHeaderTransformationSettings.setEnabled(False)
        self.menuHeaderTransformationSettings.setObjectName("menuHeaderTransformationSettings")
        self.menuHeaderAnalysisSettings = QtWidgets.QAction(MainWindow)
        self.menuHeaderAnalysisSettings.setEnabled(False)
        self.menuHeaderAnalysisSettings.setObjectName("menuHeaderAnalysisSettings")
        self.menuMappingDefinition = QtWidgets.QAction(MainWindow)
        self.menuMappingDefinition.setEnabled(False)
        self.menuMappingDefinition.setObjectName("menuMappingDefinition")
        self.menuToggleMappingDefinition = QtWidgets.QAction(MainWindow)
        self.menuToggleMappingDefinition.setCheckable(True)
        self.menuToggleMappingDefinition.setObjectName("menuToggleMappingDefinition")
        self.menuSelectMappingDefinition = QtWidgets.QAction(MainWindow)
        self.menuSelectMappingDefinition.setObjectName("menuSelectMappingDefinition")
        self.menuHeaderIdentifierTools = QtWidgets.QAction(MainWindow)
        self.menuHeaderIdentifierTools.setEnabled(False)
        self.menuHeaderIdentifierTools.setObjectName("menuHeaderIdentifierTools")
        self.menuHeaderMetadataEnrichment = QtWidgets.QAction(MainWindow)
        self.menuHeaderMetadataEnrichment.setEnabled(False)
        self.menuHeaderMetadataEnrichment.setObjectName("menuHeaderMetadataEnrichment")
        self.menuHeaderMappingSettings = QtWidgets.QAction(MainWindow)
        self.menuHeaderMappingSettings.setEnabled(False)
        self.menuHeaderMappingSettings.setObjectName("menuHeaderMappingSettings")
        self.menuOpenValidationDialog = QtWidgets.QAction(MainWindow)
        self.menuOpenValidationDialog.setObjectName("menuOpenValidationDialog")
        self.menuDatei.addAction(self.action_fetch_from_oai)
        self.menuDatei.addSeparator()
        self.menuDatei.addAction(self.actionData_Preparation_Tool_beenden)
        self.menu_ber.addAction(self.menuInfoAbout)
        self.menu_ber.addAction(self.menuInfoDDBpro)
        self.menu_ber.addSeparator()
        self.menu_ber.addAction(self.menuInfoIntroscreen)
        self.menuBearbeiten.addAction(self.actionLoadStandards)
        self.menuBearbeiten.addSeparator()
        self.menuBearbeiten.addAction(self.menuHeaderTransformationSettings)
        self.menuBearbeiten.addAction(self.menuToggleRightsInfo)
        self.menuBearbeiten.addAction(self.menuToggleDdb2017Preprocessing)
        self.menuBearbeiten.addAction(self.menuToggleAggregatorInfo)
        self.menuBearbeiten.addAction(self.menuToggleMappingDefinition)
        self.menuBearbeiten.addSeparator()
        self.menuBearbeiten.addAction(self.menuHeaderAnalysisSettings)
        self.menuBearbeiten.addAction(self.menuToggleObsoleteObjects)
        self.menuTools.addAction(self.menuHeaderIdentifierTools)
        self.menuTools.addAction(self.menuGenerateDDBIDs)
        self.menuTools.addAction(self.menuEnrichIDs)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.menuHeaderMetadataEnrichment)
        self.menuTools.addAction(self.menuRightsInfo)
        self.menuTools.addAction(self.menuAggregatorInfo)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.menuHeaderMappingSettings)
        self.menuTools.addAction(self.menuSelectMappingDefinition)
        self.menuTools.addAction(self.menuMappingDefinition)
        self.menuValidierung.addAction(self.menuOpenValidationDialog)
        self.menubar.addAction(self.menuDatei.menuAction())
        self.menubar.addAction(self.menuBearbeiten.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuValidierung.menuAction())
        self.menubar.addAction(self.menu_ber.menuAction())

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Data Preparation Tool neo"))
        self.label_welcome_info_box.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600; color:#000000;\">Willkommen beim Data Preparation Tool!</span></p><p><span style=\" font-size:10pt; color:#000000;\">Um Ihre Exportdateien im EAD-Format zu prüfen, wählen Sie den Menüpunkt </span><span style=\" font-size:10pt; font-style:italic; color:#000000;\">Validierung</span><span style=\" font-size:10pt; color:#000000;\">.<br/>Weitere Informationen finden Sie im Menü </span><span style=\" font-size:10pt; font-style:italic; color:#000000;\">Info</span><span style=\" font-size:10pt; color:#000000;\">.</span></p></body></html>"))
        self.label_welcome_info_box_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600; color:#000000;\">Willkommen beim Data Preparation Tool!</span></p><p><span style=\" font-size:10pt; color:#000000;\">Legen Sie zunächst ein Profil für Ihre erste Verarbeitung an.<br/>Wählen Sie dazu </span><span style=\" font-size:10pt; font-style:italic; color:#000000;\">Neuer Datengeber</span><span style=\" font-size:10pt; color:#000000;\">, um loszulegen.</span></p></body></html>"))
        self.label_provider.setText(_translate("MainWindow", "Datengeber:"))
        self.toolButton_new_provider.setToolTip(_translate("MainWindow", "Neuen Datengeber hinzufügen."))
        self.toolButton_refresh_providers.setToolTip(_translate("MainWindow", "Liste der Datengeber aktualisieren."))
        self.comboBox_provider.setItemText(0, _translate("MainWindow", "DE-labw"))
        self.comboBox_provider.setItemText(1, _translate("MainWindow", "DE-2410"))
        self.comboBox_provider.setItemText(2, _translate("MainWindow", "DE-1985"))
        self.pushButton_startTransformation.setText(_translate("MainWindow", "Transformation starten"))
        self.pushButton_startAnalyse.setText(_translate("MainWindow", "Analyse starten"))
        self.toolButton_metsmods_settings_dialog.setToolTip(_translate("MainWindow", "Einstellungen zur METS/MODS-Generierung."))
        self.pushButton_provider_metadata.setText(_translate("MainWindow", "Archiv-Metadaten bearbeiten"))
        self.checkBox_binaries.setText(_translate("MainWindow", "Binaries anziehen"))
        self.checkBox_metsmods.setText(_translate("MainWindow", "METS/MODS für DFGviewer generieren"))
        self.label_4.setToolTip(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Anpassungen: </span>Spezifische Anpassungen für einzelne Datengeber auswählen.</p></body></html>"))
        self.pushButton_provider_scripts.setText(_translate("MainWindow", "Providerspezifische Anpassungen"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Transformationseinstellungen"))
        self.label_5.setToolTip(_translate("MainWindow", "In der Tektonik fehlende Erschließungsinformationen werden aus den Findbüchern angereichert. Bei fehlender Tektonik wird aus den Bestandsdatensätzen eine provisorische Tektonik erzeugt."))
        self.checkBox_tektonik_enrichment.setText(_translate("MainWindow", "Anreicherung der Tektonik aus den Findbüchern"))
        self.checkBox_metadata_previews.setText(_translate("MainWindow", "Voransichten im Archivportal-Layout erstellen"))
        self.checkBox_analysis.setText(_translate("MainWindow", "Statistische Analyse und technische Validierung"))
        self.toolButton_preview_testset.setToolTip(_translate("MainWindow", "Einstellungen zur Generierung der Voransichten."))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Analyseeinstellungen"))
        self.menuDatei.setTitle(_translate("MainWindow", "Datei"))
        self.menu_ber.setTitle(_translate("MainWindow", "Info"))
        self.menuBearbeiten.setTitle(_translate("MainWindow", "Bearbeiten"))
        self.menuTools.setTitle(_translate("MainWindow", "Tools"))
        self.menuValidierung.setTitle(_translate("MainWindow", "Validierung"))
        self.actionDatei_ffnen.setText(_translate("MainWindow", "Datei öffnen ..."))
        self.actionData_Preparation_Tool_beenden.setText(_translate("MainWindow", "Data Preparation Tool beenden"))
        self.actionStandard.setText(_translate("MainWindow", "Standard"))
        self.actionKlassischer_Modus_altes_DPT.setText(_translate("MainWindow", "Klassischer Modus (altes DPT)"))
        self.action_ber.setText(_translate("MainWindow", "Über ..."))
        self.actionWeitere_Informationen_auf_DDBpro.setText(_translate("MainWindow", "Weitere Informationen auf DDBpro"))
        self.menuInfoAbout.setText(_translate("MainWindow", "Info zum Data Preparation Tool ..."))
        self.menuInfoDDBpro.setText(_translate("MainWindow", "Weitere Informationen auf DDBpro ..."))
        self.actionEinstellungen.setText(_translate("MainWindow", "Einstellungen ..."))
        self.menuGenerateDDBIDs.setText(_translate("MainWindow", "DDB-IDs generieren ..."))
        self.menuEnrichIDs.setText(_translate("MainWindow", "Fehlende Identifier anreichern ..."))
        self.actionLoadStandards.setText(_translate("MainWindow", "Standardeinstellungen laden ..."))
        self.menuInfoIntroscreen.setText(_translate("MainWindow", "Willkommensbildschirm einblenden ..."))
        self.action_fetch_from_oai.setText(_translate("MainWindow", "Dateien per OAI-PMH laden ..."))
        self.menuExcelMapping.setText(_translate("MainWindow", "Excel-Mapping bearbeiten"))
        self.menuRightsInfo.setText(_translate("MainWindow", "Rechte- und Lizenzangaben bearbeiten ..."))
        self.menuToggleRightsInfo.setText(_translate("MainWindow", "Rechte/Lizenz-Anreicherung aktivieren"))
        self.menuToggleDdb2017Preprocessing.setText(_translate("MainWindow", "DDB-2017-Vorprozessierung aktivieren"))
        self.menuAggregatorInfo.setText(_translate("MainWindow", "Aggregatoren-Zuordnung bearbeiten ..."))
        self.menuToggleAggregatorInfo.setText(_translate("MainWindow", "Aggregator-Anreicherung aktivieren"))
        self.menuToggleObsoleteObjects.setText(_translate("MainWindow", "Löschen obsoleter Objekte aktivieren"))
        self.menuHeaderTransformationSettings.setText(_translate("MainWindow", "Transformationseinstellungen:"))
        self.menuHeaderAnalysisSettings.setText(_translate("MainWindow", "Analyseeinstellungen:"))
        self.menuMappingDefinition.setText(_translate("MainWindow", "Mapping-Definition bearbeiten ..."))
        self.menuToggleMappingDefinition.setText(_translate("MainWindow", "Mapping-Definition anwenden"))
        self.menuSelectMappingDefinition.setText(_translate("MainWindow", "Mapping-Definition zuordnen ..."))
        self.menuHeaderIdentifierTools.setText(_translate("MainWindow", "Identifier-Tools:"))
        self.menuHeaderMetadataEnrichment.setText(_translate("MainWindow", "Metadaten-Anreicherung:"))
        self.menuHeaderMappingSettings.setText(_translate("MainWindow", "Mapping-Einstellungen:"))
        self.menuOpenValidationDialog.setText(_translate("MainWindow", "Validierung öffnen ..."))

from gui_components.ui_templates import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())