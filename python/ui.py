# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import qt_data_rc
import qt_data_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(624, 504)
        MainWindow.setContextMenuPolicy(Qt.NoContextMenu)
        icon = QIcon()
        icon.addFile(u":/image/image/k1.ico", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_10 = QGridLayout(self.centralwidget)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setEnabled(True)
        self.tabWidget.setLayoutDirection(Qt.LeftToRight)
        self.tabWidget.setIconSize(QSize(32, 32))
        self.tab_6 = QWidget()
        self.tab_6.setObjectName(u"tab_6")
        self.verticalLayout_3 = QVBoxLayout(self.tab_6)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_13 = QLabel(self.tab_6)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setContextMenuPolicy(Qt.NoContextMenu)
        self.label_13.setTextFormat(Qt.AutoText)
        self.label_13.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_13)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_5, 1, 0, 1, 1)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer_5, 2, 1, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_6, 1, 2, 1, 1)

        self.label_5 = QLabel(self.tab_6)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setPixmap(QPixmap(u":/image/image/xx.jpg"))

        self.gridLayout_3.addWidget(self.label_5, 1, 1, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer_4, 0, 1, 1, 1)


        self.verticalLayout_3.addLayout(self.gridLayout_3)

        icon1 = QIcon()
        icon1.addFile(u":/image/image/8666691_home_icon.png", QSize(), QIcon.Normal, QIcon.Off)
        self.tabWidget.addTab(self.tab_6, icon1, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_2 = QGridLayout(self.tab)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.dr_button = QPushButton(self.tab)
        self.dr_button.setObjectName(u"dr_button")
        self.dr_button.setEnabled(True)

        self.horizontalLayout_3.addWidget(self.dr_button)

        self.dr_yz_pushButton = QPushButton(self.tab)
        self.dr_yz_pushButton.setObjectName(u"dr_yz_pushButton")

        self.horizontalLayout_3.addWidget(self.dr_yz_pushButton)

        self.change_account_pushButton = QPushButton(self.tab)
        self.change_account_pushButton.setObjectName(u"change_account_pushButton")

        self.horizontalLayout_3.addWidget(self.change_account_pushButton)


        self.gridLayout_2.addLayout(self.horizontalLayout_3, 0, 1, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.stu_box = QCheckBox(self.tab)
        self.stu_box.setObjectName(u"stu_box")
        self.stu_box.setEnabled(True)

        self.horizontalLayout_2.addWidget(self.stu_box)

        self.free_box = QCheckBox(self.tab)
        self.free_box.setObjectName(u"free_box")
        self.free_box.setEnabled(True)

        self.horizontalLayout_2.addWidget(self.free_box)

        self.auto_box = QCheckBox(self.tab)
        self.auto_box.setObjectName(u"auto_box")

        self.horizontalLayout_2.addWidget(self.auto_box)


        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 1, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.login_button = QPushButton(self.tab)
        self.login_button.setObjectName(u"login_button")
        self.login_button.setStyleSheet(u"color: green;")

        self.horizontalLayout_5.addWidget(self.login_button)

        self.logout_pushButton = QPushButton(self.tab)
        self.logout_pushButton.setObjectName(u"logout_pushButton")
        self.logout_pushButton.setStyleSheet(u"color: red;")

        self.horizontalLayout_5.addWidget(self.logout_pushButton)


        self.gridLayout_2.addLayout(self.horizontalLayout_5, 3, 0, 1, 2)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.gridLayout.setVerticalSpacing(40)
        self.gridLayout.setContentsMargins(-1, 20, -1, 20)
        self.label_2 = QLabel(self.tab)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.label_6 = QLabel(self.tab)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 0, 0, 1, 1)

        self.nc = QLineEdit(self.tab)
        self.nc.setObjectName(u"nc")
        self.nc.setEnabled(True)
        self.nc.setContextMenuPolicy(Qt.NoContextMenu)

        self.gridLayout.addWidget(self.nc, 0, 1, 1, 1)

        self.label_3 = QLabel(self.tab)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)

        self.operator_box = QComboBox(self.tab)
        self.operator_box.addItem("")
        self.operator_box.addItem("")
        self.operator_box.addItem("")
        self.operator_box.addItem("")
        self.operator_box.setObjectName(u"operator_box")
        self.operator_box.setContextMenuPolicy(Qt.NoContextMenu)
        self.operator_box.setEditable(False)

        self.gridLayout.addWidget(self.operator_box, 3, 1, 1, 1)

        self.password = QLineEdit(self.tab)
        self.password.setObjectName(u"password")
        self.password.setContextMenuPolicy(Qt.NoContextMenu)
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setPlaceholderText(u"\u8bf7\u8f93\u5165\u5bc6\u7801")
        self.password.setClearButtonEnabled(True)

        self.gridLayout.addWidget(self.password, 2, 1, 1, 1)

        self.label = QLabel(self.tab)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.username = QLineEdit(self.tab)
        self.username.setObjectName(u"username")
        self.username.setContextMenuPolicy(Qt.NoContextMenu)
        self.username.setLocale(QLocale(QLocale.Chinese, QLocale.China))
        self.username.setEchoMode(QLineEdit.Normal)

        self.gridLayout.addWidget(self.username, 1, 1, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setSizeConstraint(QLayout.SetMinimumSize)
        self.private_mm = QRadioButton(self.tab)
        self.private_mm.setObjectName(u"private_mm")
        self.private_mm.setContextMenuPolicy(Qt.NoContextMenu)
        self.private_mm.setLayoutDirection(Qt.LeftToRight)
        self.private_mm.setAutoFillBackground(False)

        self.horizontalLayout_6.addWidget(self.private_mm)


        self.gridLayout_2.addLayout(self.horizontalLayout_6, 1, 0, 1, 1)

        icon2 = QIcon()
        icon2.addFile(u":/image/image/user_icon.png", QSize(), QIcon.Disabled, QIcon.Off)
        icon2.addFile(u":/image/image/user_icon.png", QSize(), QIcon.Selected, QIcon.On)
        self.tabWidget.addTab(self.tab, icon2, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_5 = QGridLayout(self.tab_2)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.scrollArea_2 = QScrollArea(self.tab_2)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 580, 344))
        self.gridLayout_7 = QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.auto_start = QCheckBox(self.scrollAreaWidgetContents_2)
        self.auto_start.setObjectName(u"auto_start")

        self.gridLayout_7.addWidget(self.auto_start, 0, 0, 1, 1)

        self.up_v = QPushButton(self.scrollAreaWidgetContents_2)
        self.up_v.setObjectName(u"up_v")

        self.gridLayout_7.addWidget(self.up_v, 9, 0, 1, 1)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_10, 12, 1, 1, 3)

        self.button_del_all = QPushButton(self.scrollAreaWidgetContents_2)
        self.button_del_all.setObjectName(u"button_del_all")
        self.button_del_all.setStyleSheet(u"color: red;")

        self.gridLayout_7.addWidget(self.button_del_all, 12, 0, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.wait_time = QDoubleSpinBox(self.scrollAreaWidgetContents_2)
        self.wait_time.setObjectName(u"wait_time")
        self.wait_time.setContextMenuPolicy(Qt.NoContextMenu)
        self.wait_time.setAcceptDrops(False)
        self.wait_time.setMinimum(0.100000000000000)
        self.wait_time.setValue(1.000000000000000)

        self.horizontalLayout_4.addWidget(self.wait_time)

        self.wait_time_Button = QPushButton(self.scrollAreaWidgetContents_2)
        self.wait_time_Button.setObjectName(u"wait_time_Button")

        self.horizontalLayout_4.addWidget(self.wait_time_Button)


        self.gridLayout_7.addLayout(self.horizontalLayout_4, 5, 0, 1, 1)

        self.desktop_button = QPushButton(self.scrollAreaWidgetContents_2)
        self.desktop_button.setObjectName(u"desktop_button")

        self.gridLayout_7.addWidget(self.desktop_button, 7, 0, 1, 1)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_11, 0, 1, 1, 1)

        self.link_dr = QCommandLinkButton(self.scrollAreaWidgetContents_2)
        self.link_dr.setObjectName(u"link_dr")

        self.gridLayout_7.addWidget(self.link_dr, 0, 3, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_7.addItem(self.verticalSpacer_2, 11, 0, 1, 4)

        self.lzy_pushButton = QPushButton(self.scrollAreaWidgetContents_2)
        self.lzy_pushButton.setObjectName(u"lzy_pushButton")

        self.gridLayout_7.addWidget(self.lzy_pushButton, 7, 3, 1, 1)

        self.link_github = QCommandLinkButton(self.scrollAreaWidgetContents_2)
        self.link_github.setObjectName(u"link_github")

        self.gridLayout_7.addWidget(self.link_github, 5, 3, 1, 1)

        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)

        self.gridLayout_5.addWidget(self.scrollArea_2, 0, 0, 1, 2)

        icon3 = QIcon()
        icon3.addFile(u":/image/image/settings_icon.png", QSize(), QIcon.Active, QIcon.On)
        self.tabWidget.addTab(self.tab_2, icon3, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.gridLayout_6 = QGridLayout(self.tab_3)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_7, 0, 2, 1, 1)

        self.label_10 = QLabel(self.tab_3)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_6.addWidget(self.label_10, 0, 0, 1, 1)

        self.upadte_announcement_now = QPushButton(self.tab_3)
        self.upadte_announcement_now.setObjectName(u"upadte_announcement_now")

        self.gridLayout_6.addWidget(self.upadte_announcement_now, 2, 2, 1, 1)

        self.textBrowser_gg = QTextBrowser(self.tab_3)
        self.textBrowser_gg.setObjectName(u"textBrowser_gg")
        self.textBrowser_gg.setEnabled(True)
        self.textBrowser_gg.setContextMenuPolicy(Qt.NoContextMenu)

        self.gridLayout_6.addWidget(self.textBrowser_gg, 1, 0, 1, 3)

        self.up_announcement_day = QLabel(self.tab_3)
        self.up_announcement_day.setObjectName(u"up_announcement_day")

        self.gridLayout_6.addWidget(self.up_announcement_day, 0, 1, 1, 1)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_12, 2, 1, 1, 1)

        icon4 = QIcon()
        icon4.addFile(u":/image/image/message_square_icon.png", QSize(), QIcon.Active, QIcon.On)
        self.tabWidget.addTab(self.tab_3, icon4, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.gridLayout_9 = QGridLayout(self.tab_5)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_9, 2, 2, 1, 1)

        self.image_ds = QLabel(self.tab_5)
        self.image_ds.setObjectName(u"image_ds")
        self.image_ds.setEnabled(True)
        self.image_ds.setMinimumSize(QSize(152, 152))
        self.image_ds.setMaximumSize(QSize(250, 250))
        self.image_ds.setPixmap(QPixmap(u":/image/image/mm_reward_qrcode_1694960459674.png"))
        self.image_ds.setScaledContents(True)

        self.gridLayout_9.addWidget(self.image_ds, 2, 1, 1, 1)

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_9.addItem(self.verticalSpacer_7, 3, 1, 1, 1)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_9.addItem(self.verticalSpacer_6, 0, 1, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_8, 2, 0, 1, 1)

        self.da_tet = QLabel(self.tab_5)
        self.da_tet.setObjectName(u"da_tet")
        self.da_tet.setAlignment(Qt.AlignCenter)

        self.gridLayout_9.addWidget(self.da_tet, 1, 1, 1, 1)

        icon5 = QIcon()
        icon5.addFile(u":/image/image/8666647_heart_icon.png", QSize(), QIcon.Normal, QIcon.Off)
        self.tabWidget.addTab(self.tab_5, icon5, "")

        self.gridLayout_10.addWidget(self.tabWidget, 2, 0, 1, 3)

        self.label_11 = QLabel(self.centralwidget)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setContextMenuPolicy(Qt.NoContextMenu)
        self.label_11.setTextInteractionFlags(Qt.TextBrowserInteraction)

        self.gridLayout_10.addWidget(self.label_11, 4, 0, 1, 1)

        self.label_12 = QLabel(self.centralwidget)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setContextMenuPolicy(Qt.NoContextMenu)
        self.label_12.setTextInteractionFlags(Qt.TextBrowserInteraction)

        self.gridLayout_10.addWidget(self.label_12, 4, 2, 1, 1)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_10.addItem(self.horizontalSpacer_13, 4, 1, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout.addWidget(self.label_4)

        self.lineEdit_nc = QLineEdit(self.centralwidget)
        self.lineEdit_nc.setObjectName(u"lineEdit_nc")
        self.lineEdit_nc.setContextMenuPolicy(Qt.NoContextMenu)
        self.lineEdit_nc.setReadOnly(True)
        self.lineEdit_nc.setCursorMoveStyle(Qt.LogicalMoveStyle)

        self.horizontalLayout.addWidget(self.lineEdit_nc)

        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout.addWidget(self.label_7)

        self.days = QLabel(self.centralwidget)
        self.days.setObjectName(u"days")

        self.horizontalLayout.addWidget(self.days)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line)

        self.label_9 = QLabel(self.centralwidget)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout.addWidget(self.label_9)

        self.times = QLabel(self.centralwidget)
        self.times.setObjectName(u"times")

        self.horizontalLayout.addWidget(self.times)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_2)

        self.tuo = QPushButton(self.centralwidget)
        self.tuo.setObjectName(u"tuo")
        self.tuo.setStyleSheet(u"color: green;")

        self.horizontalLayout.addWidget(self.tuo)


        self.gridLayout_10.addLayout(self.horizontalLayout, 1, 0, 1, 3)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
#if QT_CONFIG(shortcut)
        self.label_2.setBuddy(self.password)
        self.label_6.setBuddy(self.nc)
        self.label_3.setBuddy(self.operator_box)
        self.label.setBuddy(self.username)
#endif // QT_CONFIG(shortcut)
        QWidget.setTabOrder(self.nc, self.username)
        QWidget.setTabOrder(self.username, self.password)
        QWidget.setTabOrder(self.password, self.operator_box)
        QWidget.setTabOrder(self.operator_box, self.lineEdit_nc)
        QWidget.setTabOrder(self.lineEdit_nc, self.tabWidget)
        QWidget.setTabOrder(self.tabWidget, self.scrollArea_2)
        QWidget.setTabOrder(self.scrollArea_2, self.auto_start)
        QWidget.setTabOrder(self.auto_start, self.textBrowser_gg)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u81ea\u52a8\u767b\u5165\u6821\u56ed\u7f51\u2014\u2014ECJTU", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"\u5343\u91cc\u4e4b\u9065\uff0c\u79ef\u4e8e\u4e00\u65f6\u4e4b\u8dec\u6b65", None))
        self.label_5.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), "")
#if QT_CONFIG(tooltip)
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.tab_6), QCoreApplication.translate("MainWindow", u"\u4e3b\u9875", None))
#endif // QT_CONFIG(tooltip)
        self.dr_button.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u8d26\u6237", None))
        self.dr_yz_pushButton.setText(QCoreApplication.translate("MainWindow", u"\u9a8c\u8bc1\u8d26\u6237", None))
        self.change_account_pushButton.setText(QCoreApplication.translate("MainWindow", u"\u4fee\u6539\u8d26\u6237", None))
        self.stu_box.setText(QCoreApplication.translate("MainWindow", u"ECJTU-Stu", None))
        self.free_box.setText(QCoreApplication.translate("MainWindow", u"EcjtuLib_Free", None))
        self.auto_box.setText(QCoreApplication.translate("MainWindow", u"\u81ea\u52a8\u9009\u62e9", None))
        self.login_button.setText(QCoreApplication.translate("MainWindow", u"\u7acb\u5373\u7528\u6b64\u8d26\u6237\u767b\u5165\u6821\u56ed\u7f51", None))
        self.logout_pushButton.setText(QCoreApplication.translate("MainWindow", u"\u767b\u51fa\u6821\u56ed\u7f51\uff08\u6ce8\u9500\uff09", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u5bc6\u7801", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u8d26\u6237\u6635\u79f0", None))
        self.nc.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u9ed8\u8ba4\u4e3a\u5b66\u53f7", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u8fd0\u8425\u5546", None))
        self.operator_box.setItemText(0, QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u8fd0\u8425\u5546", None))
        self.operator_box.setItemText(1, QCoreApplication.translate("MainWindow", u"\u4e2d\u56fd\u79fb\u52a8", None))
        self.operator_box.setItemText(2, QCoreApplication.translate("MainWindow", u"\u4e2d\u56fd\u8054\u901a", None))
        self.operator_box.setItemText(3, QCoreApplication.translate("MainWindow", u"\u4e2d\u56fd\u7535\u4fe1", None))

        self.label.setText(QCoreApplication.translate("MainWindow", u"\u5b66\u53f7", None))
        self.username.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u8bf7\u8f93\u5165\u5b66\u53f7", None))
        self.private_mm.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a\u5bc6\u7801", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), "")
#if QT_CONFIG(tooltip)
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"\u8d26\u6237", None))
#endif // QT_CONFIG(tooltip)
        self.auto_start.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u673a\u81ea\u542f\uff08\u63a8\u8350\u6253\u5f00\uff09", None))
        self.up_v.setText(QCoreApplication.translate("MainWindow", u"\u68c0\u67e5\u66f4\u65b0", None))
        self.button_del_all.setText(QCoreApplication.translate("MainWindow", u"\u521d\u59cb\u5316\u7a0b\u5e8f", None))
        self.wait_time_Button.setText(QCoreApplication.translate("MainWindow", u"\u8bf4\u660e", None))
        self.desktop_button.setText(QCoreApplication.translate("MainWindow", u"\u521b\u5efa\u684c\u9762\u5feb\u6377\u65b9\u5f0f", None))
        self.link_dr.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00\u767b\u5165\u9875\u9762", None))
#if QT_CONFIG(tooltip)
        self.lzy_pushButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u70b9\u51fb\u8be5\u6309\u94ae\uff0c\u7a0b\u5e8f\u4f1a\u81ea\u52a8\u5e2e\u4f60\u590d\u5236\u63d0\u53d6\u7801\uff0c\u5728\u84dd\u594f\u4e91\u7f51\u76d8\u754c\u9762\u53ef\u76f4\u63a5\u7c98\u8d34", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(whatsthis)
        self.lzy_pushButton.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.lzy_pushButton.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00\u84dd\u594f\u4e91\u7f51\u76d8\uff08\u63d0\u53d6\u7801\uff1aecjt\uff09", None))
        self.link_github.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00\u5f00\u6e90\u5730\u5740", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), "")
#if QT_CONFIG(tooltip)
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e", None))
#endif // QT_CONFIG(tooltip)
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"\u4e0a\u6b21\u66f4\u65b0\u65f6\u95f4:", None))
        self.upadte_announcement_now.setText(QCoreApplication.translate("MainWindow", u"\u7acb\u5373\u66f4\u65b0\u516c\u544a", None))
        self.textBrowser_gg.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u68c0\u6d4b\u5230\u516c\u544a\u672a\u52a0\u8f7d\uff0c\u8bf7\u5728\u8054\u7f51\u73af\u5883\u4e0b\uff0c\u624b\u52a8\u70b9\u51fb\u201c\u7acb\u523b\u66f4\u65b0\u516c\u544a\u201d\u6309\u94ae", None))
        self.up_announcement_day.setText(QCoreApplication.translate("MainWindow", u"\u672a\u66f4\u65b0", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), "")
#if QT_CONFIG(tooltip)
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"\u516c\u544a", None))
#endif // QT_CONFIG(tooltip)
        self.image_ds.setText("")
        self.da_tet.setText(QCoreApplication.translate("MainWindow", u"\u6d69\u701a\u6c5f\u6d77\uff0c\u6e90\u4e8e\u70b9\u6ef4\u7684\u6c47\u805a", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), "")
#if QT_CONFIG(tooltip)
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.tab_5), QCoreApplication.translate("MainWindow", u"\u6253\u8d4f", None))
#endif // QT_CONFIG(tooltip)
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"\u6709\u4efb\u4f55\u5efa\u8bae\u3001\u610f\u89c1\u6216BUG\u53cd\u9988\uff0c\u8bf7\u901a\u8fc7\u4ee5\u4e0b\u65b9\u5f0f\u4e0e\u6211\u8054\u7cfb", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"\u90ae\u7bb1\uff1aatuzkb@outlook.com", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u5f53\u524d\u767b\u5165\u8d26\u6237\uff1a", None))
#if QT_CONFIG(whatsthis)
        self.lineEdit_nc.setWhatsThis(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.lineEdit_nc.setText(QCoreApplication.translate("MainWindow", u"\u65e0", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u5df2\u63d0\u4f9b\u670d\u52a1\uff1a", None))
        self.days.setText(QCoreApplication.translate("MainWindow", u"\u5929\u6570", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"\u5df2\u4f7f\u7528\uff1a", None))
        self.times.setText(QCoreApplication.translate("MainWindow", u"\u6b21\u6570", None))
#if QT_CONFIG(tooltip)
        self.tuo.setToolTip(QCoreApplication.translate("MainWindow", u"\u6258\u76d8\u8fd0\u884c\uff0c\u540e\u53f0\u76d1\u6d4b\u6821\u56ed\u7f51\u7edc\u72b6\u6001\uff0c\u4ee5\u9632\u65ad\u5f00", None))
#endif // QT_CONFIG(tooltip)
        self.tuo.setText(QCoreApplication.translate("MainWindow", u"\u6258\u76d8\u8fd0\u884c", None))
    # retranslateUi

