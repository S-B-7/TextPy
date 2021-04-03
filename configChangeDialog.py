from PyQt5 import QtWidgets as pqw
from PyQt5 import QtCore as pqc
from PyQt5 import QtGui as pqg
import sys

from uis.configChangeDialog_Ui import Ui_Dialog

DEFAULT_FONT= pqg.QFont()
DEFAULT_FONT.setPointSize(15)

DEFAULT_CONFIG = {
        'font' : DEFAULT_FONT,
        'toolBarCheck': True,
        'toolBarPosition': pqc.Qt.TopToolBarArea,
        'tabBarCheck': True,
        'tabBarPosition': pqc.Qt.TopToolBarArea,
        'editorBg': pqg.QColor('white'),
        'editorFg': pqg.QColor('black'),
        'editorHlBg' : pqg.QColor("#3D9FEE"),
        'editorHlFg' : pqg.QColor("white"),
        'wordWrap' : pqg.QTextOption.WrapAtWordBoundaryOrAnywhere,
        'autoSave' : False,
        'toolBarBg' :pqg.QColor("black"),#pqg.QColor.fromRgb(240,240,240),
        'toolBarFg' : pqg.QColor("white"),
        'toolBarSrchBg' : pqg.QColor("white"),
        'tabBarBg' :pqg.QColor("black"),
    }


class ConfigChangeDialog(pqw.QDialog):

    ERROR = "CONFIGCHANGEDIALOG.ERROR"
    CANCEL = "CONFIGCHANGEDIALOG.CANCEL"


    def __init__(self , configs= DEFAULT_CONFIG,*args, **kwargs):
        super().__init__(*args, **kwargs)

        self.configs = configs

        self. ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.fontChosserButton.clicked.connect(self.changeFont)
        self.ui.toolBarAreaSelecter.currentTextChanged.connect(self.changeToolBarPos)
        self.ui.tabBarAreaSelector.currentTextChanged.connect(self.changeTabBarPos)
        self.ui.editorBgChooser.clicked.connect(self.changeEditorBgColor)
        self.ui.editorFgChooser.clicked.connect(self.changeEditorFgColor)
        self.ui.editorhlBgChooser.clicked.connect(self.changeEditorHlBgColor)
        self.ui.editorhlFgChooser.clicked.connect(self.changeEditorHlFgColor)
        self.ui.toolBarBgChooser.clicked.connect(self.changeToolBarBgColor)
        self.ui.toolBarFgChooser.clicked.connect(self.changeToolBarFgColor)
        self.ui.toolBarSrchBgChooser.clicked.connect(self.changeToolBarSrchBgColor)
        self.ui.tabBarBgChooser.clicked.connect(self.changeTabBarBgColor)
        self.ui.saveBt.clicked.connect(self.save)
        
        self.load()

    def load(self):
        self.font = self.configs['font']
        self.ui.toolBarCheck.setChecked(self.configs['toolBarCheck'])
        self.ui.tabBarCheck.setChecked(self.configs['tabBarCheck'])

        self.tabBarPos = self.configs['tabBarPosition']
        self.toolBarPos = self.configs['toolBarPosition']

        if self.configs['tabBarPosition'] == pqc.Qt.TopToolBarArea:
            self.ui.tabBarAreaSelector.setCurrentText('TOP')
        elif self.configs['tabBarPosition'] == pqc.Qt.BottomToolBarArea:
            self.ui.tabBarAreaSelector.setCurrentText('BOTTOM')
        elif self.configs['tabBarPosition'] == pqc.Qt.RightToolBarArea:
           self.ui.tabBarAreaSelector.setCurrentText('RIGHT')
        elif self.configs['tabBarPosition'] == pqc.Qt.LeftToolBarArea:
            self.ui.tabBarAreaSelector.setCurrentText('LEFT')

        if self.configs['toolBarPosition'] == pqc.Qt.TopToolBarArea:
            self.ui.toolBarAreaSelecter.setCurrentText('TOP')
        elif self.configs['toolBarPosition'] == pqc.Qt.BottomToolBarArea:
            self.ui.toolBarAreaSelecter.setCurrentText('BOTTOM')
        elif self.configs['toolBarPosition'] == pqc.Qt.RightToolBarArea:
            self.ui.toolBarAreaSelecter.setCurrentText('RIGHT')
        elif self.configs['toolBarPosition'] == pqc.Qt.LeftToolBarArea:
            self.ui.toolBarAreaSelecter.setCurrentText('LEFT')


        self.ui.editorBgChooser.setStyleSheet(f'background-color: {self.configs["editorBg"].name()} ;')
        self.ui.editorFgChooser.setStyleSheet(f'background-color: {self.configs["editorFg"].name()} ;')
        self.editorBg = self.configs["editorBg"]
        self.editorFg = self.configs["editorFg"]

        self.ui.editorhlBgChooser.setStyleSheet(f'background-color: {self.configs["editorHlBg"].name()} ;')
        self.ui.editorhlFgChooser.setStyleSheet(f'background-color: {self.configs["editorHlFg"].name()} ;')


        self.editorHlBgColor = self.configs['editorHlBg']
        self.editorHlFgColor = self.configs['editorHlFg']

        self.toolBarBg = self.configs['toolBarBg']
        self.ui.toolBarBgChooser.setStyleSheet(f"background-color: {self.toolBarBg.name()}")

        self.toolBarFg = self.configs['toolBarFg']
        self.ui.toolBarFgChooser.setStyleSheet(f"background-color : {self.toolBarFg.name()}")

        self.toolBarSrchBg = self.configs['toolBarSrchBg']
        self.ui.toolBarSrchBgChooser.setStyleSheet(f"background-color: {self.toolBarSrchBg.name()}")

        self.tabBarBg = self.configs['tabBarBg']
        self.ui.tabBarBgChooser.setStyleSheet(f"background-color: {self.tabBarBg.name()}")


        if self.configs['wordWrap'] == pqg.QTextOption.NoWrap:
            self.ui.wordWrapCheck.setChecked(False)
        else:
            self.ui.wordWrapCheck.setChecked(True)

        self.ui.AutoSaveCheck.setChecked(self.configs['autoSave'])

    def getConfigs(self):

        self.show()
        self.exec()
        try:
            return self.configs
        except:
            return ConfigChangeDialog.ERROR

    def changeFont(self):
        fontDialog = pqw.QFontDialog(self.font)
        fontDialog.setCurrentFont(self.font)
        font = fontDialog.getFont(self.font)
        if font[1]:
            self.font = font[0]

    def changeToolBarPos(self):
        if self.ui.toolBarAreaSelecter.currentText() == "TOP":
            self.toolBarPos = pqc.Qt.TopToolBarArea
        elif self.ui.toolBarAreaSelecter.currentText() == "BOTTOM":
            self.toolBarPos = pqc.Qt.BottomToolBarArea
        elif self.ui.toolBarAreaSelecter.currentText() == "RIGHT":
            self.toolBarPos = pqc.Qt.RightToolBarArea
        elif self.ui.toolBarAreaSelecter.currentText() == "LEFT":
            self.toolBarPos = pqc.Qt.LeftToolBarArea

    def changeTabBarPos(self):
        if self.ui.tabBarAreaSelector.currentText() == "TOP":
            self.tabBarPos = pqc.Qt.TopToolBarArea
        elif self.ui.tabBarAreaSelector.currentText() == "BOTTOM":
            self.tabBarPos = pqc.Qt.BottomToolBarArea
        elif self.ui.tabBarAreaSelector.currentText() == "RIGHT":
            self.tabBarPos= pqc.Qt.RightToolBarArea
        elif self.ui.tabBarAreaSelector.currentText() == "LEFT":
            self.tabBarPos= pqc.Qt.LeftToolBarArea

    def changeEditorBgColor(self):

        color = pqw.QColorDialog().getColor(self.editorBg)

        if color :
            rgb = color.getRgb()
            self.editorBg = color
            self.ui.editorBgChooser.setStyleSheet(f'''
                background-color:rgb({rgb[0]}, {rgb[1]}, {rgb[2]});
                border :0px;
           ''')

    def changeEditorFgColor(self):

        color = pqw.QColorDialog().getColor( self.editorFg )
        if color :
            rgb = color.getRgb()
            self.editorFg = color
            self.ui.editorFgChooser.setStyleSheet(f'''
                background-color: rgb({rgb[0]}, {rgb[1]}, {rgb[2]});
                border :0px;
           ''')

    def changeEditorHlBgColor(self):
        color = pqw.QColorDialog().getColor( self.editorHlBgColor )

        if color:
            rgb = color.getRgb()
            self.editorHlBgColor = color
            self.ui.editorhlBgChooser.setStyleSheet(f'''
                        background-color:rgb({rgb[0]}, {rgb[1]}, {rgb[2]});
                        border :0px;
                   ''')

    def changeEditorHlFgColor(self):
        color = pqw.QColorDialog().getColor( self.editorHlFgColor)

        if color:
            rgb = color.getRgb()
            self.editorHlFgColor = color
            self.ui.editorhlFgChooser.setStyleSheet(f'''
                        background-color:rgb({rgb[0]}, {rgb[1]}, {rgb[2]});
                        border :0px;
                   ''')

    def changeToolBarBgColor(self):

        color = pqw.QColorDialog().getColor( self.toolBarBg)

        if color:
            rgb = color.getRgb()
            self.toolBarBg = color
            self.ui.toolBarBgChooser.setStyleSheet(f'''
                   background-color:rgb({rgb[0]}, {rgb[1]}, {rgb[2]});
                   border :0px;
              ''')

    def changeToolBarFgColor(self):

        color = pqw.QColorDialog().getColor( self.toolBarFg)
        if color:
            rgb = color.getRgb()
            self.toolBarFg = color
            self.ui.toolBarFgChooser.setStyleSheet(f'''
                   background-color: rgb({rgb[0]}, {rgb[1]}, {rgb[2]});
                   border :0px;
              ''')

    def changeToolBarSrchBgColor(self):
        color = pqw.QColorDialog().getColor(self.toolBarSrchBg)

        if color:
            rgb = color.getRgb()
            self.toolBarSrchBg = color
            self.ui.toolBarSrchBgChooser.setStyleSheet(f'''
                      background-color:rgb({rgb[0]}, {rgb[1]}, {rgb[2]});
                      border :0px;
                 ''')

    def changeTabBarBgColor(self):
        color = pqw.QColorDialog().getColor( self.tabBarBg)
        if color:
            rgb = color.getRgb()
            self.tabBarBg = color
            self.ui.tabBarBgChooser.setStyleSheet(f'''
                   background-color: rgb({rgb[0]}, {rgb[1]}, {rgb[2]});
                   border :0px;
              ''')


    def save(self):
        self.configs = {
                'editorBg': self.editorBg,
                'editorFg': self.editorFg,
                'font': self.font,
                'toolBarCheck': self.ui.toolBarCheck.isChecked(),
                'toolBarPosition': self.toolBarPos,
                'tabBarCheck': self.ui.tabBarCheck.isChecked(),
                'tabBarPosition': self.tabBarPos,
                'editorHlBg': self.editorHlBgColor,
                'editorHlFg' : self.editorHlFgColor,
                'autoSave' : self.ui.AutoSaveCheck.isChecked(),
                'toolBarBg' : self.toolBarBg,
                'toolBarFg' : self.toolBarFg,
                'toolBarSrchBg' : self.toolBarSrchBg,
                'tabBarBg' : self.tabBarBg
        }
        if self.ui.wordWrapCheck.isChecked():

            self.configs['wordWrap'] = pqg.QTextOption.WrapAtWordBoundaryOrAnywhere
        else:
            self.configs['wordWrap'] = pqg.QTextOption.NoWrap
        self.close()








if __name__ == '__main__':
    app = pqw.QApplication(sys.argv)
    settings = pqc.QSettings("TextiPy", "Configs")
    settings.setValue('config', DEFAULT_CONFIG)
    c = ConfigChangeDialog()
    print (c.getConfigs())
