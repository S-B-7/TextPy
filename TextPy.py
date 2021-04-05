from PyQt5 import QtWidgets as pqw
from PyQt5 import QtCore as pqc
from PyQt5 import QtGui as pqg
import sys
import os
from CustomTabWidget import CustomTabWidget
from configChangeDialog import ConfigChangeDialog , DEFAULT_CONFIG
import datetime
from helpDialog import HelpDialog
import resources


class Tab(pqw.QWidget):

    CANCEL = "TAB.CANCEL"
    ERROR = "TAB.ERROR"
    EDITOR_BG = pqg.QColor("white")
    EDITOR_FG = pqg.QColor("black")
    EDITOR_HL_BG = pqg.QColor("red")
    EDITOR_HL_FG = pqg.QColor("blue")
    WORD_WRAP   = DEFAULT_CONFIG['wordWrap']

    def __init__(self,*args, **kwargs ):
        super().__init__ (*args, **kwargs)
        self.layout = pqw.QVBoxLayout(margin = 0)
        self.text = pqw.QTextEdit(self)
        self.text.setFrameStyle(pqw.QFrame.NoFrame)
        self.layout.addWidget(self.text)
        self.setLayout(self.layout)
        self.textFont = pqg.QFont()
        self.textFont.setPointSize(15)
        self.text.setFont(self.textFont)
        self.text.textChanged.connect(self.unSave)
        self.searching = False
        self.file=None
        self.saved = False
        self.untitledNo = None
        self.title = ''
        self.titleChangeFunc = None
        self.refreshAll()
        #self.refreshWrap()

    def unSave(self):
        if not self.saved: return
        self.saved = False
        self.setTitle( f"{self.title}*")

    def search(self, term: str , caseCheck = False ,reCheck  = False) :

        if reCheck:
            term = pqc.QRegularExpression(term)
        init_cur = self.text.textCursor()
        if not self.searching:
            cur = init_cur
            cur.setPosition(pqg.QTextCursor.Start - 1)
            self.text.setTextCursor(cur)
            self.searching = True
            found = self.text.find(term, pqg.QTextDocument.FindCaseSensitively)
            if not found:
                pass
            return

        if caseCheck:
            found = self.text.find(term, pqg.QTextDocument.FindCaseSensitively,)
        else:
            found = self.text.find(term, )
        if not found:
            self.searching = False
            self.search(term, caseCheck, reCheck)

    def setFont(self, font: pqg.QFont):
        self.textFont = font
        self.text.setFont(self.textFont)

        self.text.update()

    def font(self) ->pqg.QFont:
        return self.textFont

    def load(self,path:str = None):
        if path:
            self.text.clear()
            with open (path, 'r') as file:
                while True:
                    chunk = file.read(100)
                    if not chunk : return
                    self.text.insertPlainText(chunk)
                    self.file = path
                    self.saved = True
                    self.setTitle(os.path.basename(self.file))
            self.text.document().clearUndoRedoStacks()

    def save(self,path=None):
        if not path:
            path = self.file
        if not path :
            return self.saveAsFile()

        try:
            Text = self.text.toPlainText().strip()
            if Text:
                print(path)
                with open (path, 'w') as file:
                    file.write(Text)
                self.saved = True
                self.setTitle( os.path.basename(self.file))

        except  Exception as e :
            print(e)
            return Tab.ERROR

    def saveAsFile(self):
        path = pqw.QFileDialog.getSaveFileName(None, 'Save as', self.getTitle(), "Text File (*.txt);; All Files (*.*)")[0]
        if path :
            self.save(path)
        else:
            return Tab.CANCEL

    def setTitle(self,title:str):
        self.title = title
        if self.titleChangeFunc:
            self.titleChangeFunc(self.title)

    def setTitleChangeFunc(self,func):
        self.titleChangeFunc = func

    def getTitle(self):
        title = self.title.strip()
        if title.endswith("*"):
            return title[:len(title)-1]
        return self.title

    def refreshColor(self):
        palette = self.text.palette()
        palette.setColor(pqg.QPalette.Base, Tab.EDITOR_BG)
        palette.setColor(pqg.QPalette.Text, Tab.EDITOR_FG)
        palette.setColor(pqg.QPalette.Highlight, Tab.EDITOR_HL_BG)
        palette.setColor(pqg.QPalette.HighlightedText, Tab.EDITOR_HL_FG)

        self.text.setPalette(palette)


    def refreshWrap(self):
        self.text.setWordWrapMode(Tab.WORD_WRAP)

    def refreshAll(self):
        self.refreshColor()
        self.refreshWrap()

class MainWinodw(pqw.QMainWindow):

    def __init__(self, app,*args, **kwargs):

        super().__init__(*args, **kwargs)
        self.settings = pqc.QSettings("TextPy", "Configs")
        
        self.config = DEFAULT_CONFIG

        self.app = app
        self.setWindowTitle('TextPy')
        self.setWindowIcon(pqg.QIcon( ":/icon.ico" ))
        self.setGeometry(0, 0, 800, 600)
        self.tabBrowser = CustomTabWidget(self)
        self.textFont = pqg.QFont()
        self.untitledNo = 0

        self.setCentralWidget(self.tabBrowser)
        if not self.startup() : self.addTab()
        self.tabBrowser.setAddBt(True)
        self.tabBrowser.setDoubleTapDel(True)
        self.tabBrowser.setAddTabFunc(self.addTab)
        self.tabBrowser.setDelFunc(self.delTab)
        self.makeMenuBar()
        self.makeTabBar()
        self.addToolBarBreak()
        self.makeToolBar()
        self.keyShortcuts()
        self.changeFont()
        self.config['font'] = self.textFont
        self.loadConfig()
        self.searchBox.setFrame(pqw.QFrame.NoFrame)

        self.fontBox.currentFontChanged.connect(self.fontChange)
        self.sizeBox.currentTextChanged.connect(self.fontChange)
        self.toolbar.topLevelChanged.connect(lambda: self.toolbarPositionChanged("toolBarPosition",self.toolbar))
        self.tabBar.topLevelChanged.connect(lambda: self.toolbarPositionChanged("tabBarPosition", self.tabBar))
        self.tabBrowser.setOnCurrentTabChange(
            lambda index: self.setWindowTitle
                (f"{self.tabBrowser.widget(index).title} - TextPy")
            if self.tabBrowser.widget(index)
            else None
        )
        self.setWindowTitle(f"{self.tabBrowser.widget(0).title} - TextPy")

    def makeTabBar(self):
        self.tabBar = self.addToolBar('TabBar')
        self.tabBar.addWidget(self.tabBrowser.tabBar)


    def fontChange(self):

        try:

            self.textFont.setFamily(self.fontBox.currentFont().family())
            self.textFont.setPointSize(int(self.sizeBox.currentText()))
            self.changeFont()
        except:
            pass

    def makeToolBar(self):


        def makeBold():
            self.textFont.setBold(not self.textFont.bold())
            self.changeFont()

        def makeItalic():
            self.textFont.setItalic(not self.textFont.italic())
            self.changeFont()

        def makeUnderline():
            self.textFont.setUnderline(not self.textFont.underline())
            self.changeFont()

        def searchTermChange():
            if not (self.searchBox.text()):
                self.tabBrowser.currentWidget().searching = False
            self.search()

        self.toolbar = self.addToolBar('Tool')

        self.fontBox = pqw.QFontComboBox(self.toolbar)
        self.fontBox.setFixedSize(200, 30)
        self.fontBox.setCurrentText(self.config['font'].family())

        self.sizeBox = pqw.QComboBox(self.toolbar)
        self.sizeBox.setFixedHeight(30)
        self.sizeBox.setFont(pqg.QFont('', 13))
        self.sizeBox.setEditable(True)

        for i in range(1, 1000):
            self.sizeBox.addItem(str(i))
        self.textFont.setPointSize(15)
        self.sizeBox.setCurrentText('15')


        self.toolbar.addWidget(pqw.QLabel(text="Font :"))
        self.toolbar.addWidget(self.fontBox)
        self.toolbar.addWidget(self.sizeBox)


        self.toolbar.addSeparator()

        wrapper = pqw.QWidget()
        layout = pqw.QHBoxLayout()

        self.boldBT = pqw.QPushButton(text="B", clicked=makeBold)
        p = pqg.QPalette()

        self.boldBT.setPalette(p)
        self.boldBT.setFixedSize(30, 30)
        self.boldBT.setFont(pqg.QFont('', 13, pqg.QFont.Bold))
        layout.addWidget(self.boldBT)

        self.italicBt = pqw.QPushButton(text="I", clicked=makeItalic)
        self.italicBt.setFixedSize(30, 30)
        self.italicBt.setFont(pqg.QFont('', 13, italic=True))
        layout.addWidget(self.italicBt)

        self.underBt = pqw.QPushButton(text="U", clicked=makeUnderline)
        self. underBt.setFixedSize(30, 30)
        underFont = pqg.QFont('', 13)
        underFont.setUnderline(True)
        self.underBt.setFont(underFont)

        layout.addWidget(self.underBt)

        wrapper.setLayout(layout)
        self.toolbar.addWidget(wrapper)
        wrapper2 = pqw.QWidget(self.toolbar)
        layout2 = pqw.QHBoxLayout()
        wrapper2.setLayout(layout2)
        self.toolbar.addSeparator()

        self.toolbar.addWidget(pqw.QLabel(text="Search : "))

        self.searchBox = pqw.QLineEdit(wrapper, )
        self.searchBox.setMinimumWidth(180)
        self.searchBox.textChanged.connect(searchTermChange)
        self.searchBox.returnPressed.connect(self.search)

        self.toolbar.addWidget(self.searchBox)

        wrapper2 = pqw.QWidget(self.toolbar)
        layout2 = pqw.QHBoxLayout()
        wrapper2.setLayout(layout2)

        self.reCheck = pqw.QCheckBox(text="RE")
        self.caseCheck = pqw.QCheckBox(text="match Case")
        self.reCheck.stateChanged.connect(searchTermChange)
        self.caseCheck.stateChanged.connect(searchTermChange)
        layout2.addWidget(self.caseCheck)
        layout2.addWidget(self.reCheck)
        self.toolbar.addWidget(wrapper2)


        self.toolbar.setAutoFillBackground(True)

    def makeMenuBar(self):
        file_menu = self.menuBar().addMenu('File')
        file_menu.addAction('Open', self.openFile, shortcut='Ctrl+O')
        file_menu.addAction('Save', self.saveFile, shortcut='Ctrl+S')
        file_menu.addAction('Save As', lambda : self.tabBrowser.currentWidget().saveAsFile() )

        file_menu.addSeparator()
        file_menu.addAction('Close', self.exit,shortcut='Ctrl+Q')

        edit_menu = self.menuBar().addMenu('Edit')
        edit_menu.addAction('Cut', self.textCut, shortcut="Ctrl+X")
        edit_menu.addAction('Copy', self.textCopy, shortcut='Ctrl+C')
        edit_menu.addAction('Paste', self.textPaste, shortcut='Ctrl+P')
        edit_menu.addSeparator()
        edit_menu.addAction('Undo', self.textUndo, shortcut='Ctrl+Z')
        edit_menu.addAction('Redo', self.textRedo, shortcut='Ctrl+Y')
        edit_menu.addSeparator()
        edit_menu.addAction('Find', lambda: self.searchBox.setFocus(), shortcut="Ctrl+F")
        edit_menu.addAction('Replace')

        view_menu = self.menuBar().addMenu('View')
        view_menu.addAction('font', self.fontDialog)
        view_menu.addAction('Toggle view tool bar', self.toggleViewToolbar, shortcut = "Ctrl+shift+T")
        view_menu.addAction('Toggle view Tab bar', self.toggleViewTabbar, shortcut="Ctrl+shift+R")

        settings_menu = self.menuBar().addMenu('Settings')
        settings_menu.addAction('change settings', self.changeSettings)

        help_menu = self.menuBar().addMenu('Help')
        help_menu.addAction('Help',self.help)
    

    def textCut(self):
        self.tabBrowser.currentWidget().text.cut()
    def textCopy(self):
        self.tabBrowser.currentWidget().text.copy()
    def textPaste(self):
        self.tabBrowser.currentWidget().text.paste()
    def textUndo(self):
        self.tabBrowser.currentWidget().text.undo()
    def textRedo(self):
        self.tabBrowser.currentWidget().text.redo()
    def search(self):
        self.tabBrowser.currentWidget().search(self.searchBox.text() , self.caseCheck.isChecked(), self.reCheck.isChecked())

    def changeFont(self):
        font = self.textFont


        self.fontBox.setCurrentFont(font)
        self.sizeBox.setCurrentIndex(font.pointSize() - 1)


        self.textFont = font
        for i in range(self.tabBrowser.count()):
            tab = self.tabBrowser.widget(i)
            tab.setFont(self.textFont)


    def fontDialog(self):
        fontDialog = pqw.QFontDialog()
        fontDialog.setCurrentFont(self.textFont)
        font = fontDialog.getFont(self.textFont)

        if font[1]:
            self.textFont = font[0]
            self.changeFont()

    def openFile(self):
        path = pqw.QFileDialog.getOpenFileName(None, 'Open File', '', "Text Files (*.txt);; All Files (*.*)")[0]
        if path:
            self.load(path)

    def load(self, path:str):
        self.tabBrowser.currentWidget().load(path)
        self.tabBrowser.tabBar.setTabText(self.tabBrowser.currentIndex() , os.path.basename(path))

    def saveFile(self):
        self.tabBrowser.currentWidget().save()
        pass

    def exit(self):
        self.close()

    def keyShortcuts(self):

        def fontShort(incriment):
            self.textFont.setPointSize(self.textFont.pointSize() + incriment)
            self.sizeBox.setCurrentIndex(self.textFont.pointSize() - 1)
            self.changeFont()

        pqw.QShortcut(pqg.QKeySequence('Ctrl++'), self.tabBrowser).activated.connect(lambda: fontShort(2))
        pqw.QShortcut(pqg.QKeySequence('Ctrl+-'), self.tabBrowser).activated.connect(lambda: fontShort(-2))

    def addTab(self, path:str = None):
        tab = Tab()

        tab.load(path)
        tab.setTitleChangeFunc(lambda title : self.changeTitle(tab, title))
        if path :
            title = os.path.basename(path)
        else:
            self.untitledNo+=1
            title = f"Untitled-{self.untitledNo}*"
            tab.untitledNo = self.untitledNo
            tab.setTitle(title)
        tab.setFont(self.textFont)
        self.tabBrowser.addTab(tab,title)

    def delTab(self, index: int):
        if self.config['autoSave'] and not self.tabBrowser.widget(index).file :
            file_name = datetime.datetime.now().strftime(
                "Unsaved File  %H-%M-%S on %d %d-%m-%y.txt"
            )

            unsaved_files_path = os.path.join(
                    os.path.dirname(__file__),
                    "Unsaved Files",
                    )

            if not os.path.isdir(unsaved_files_path):
                os.mkdir(unsaved_files_path)

            self.tabBrowser.currentWidget().save(
                os.path.join(
                    unsaved_files_path,
                    file_name,
                )
            )
            return
       

        if not self.tabBrowser.widget(index).saved:
          
            notSavedDialog = pqw.QMessageBox()
            notSavedDialog.setWindowTitle(f"{self.tabBrowser.widget(index).getTitle()} Not saved")
            notSavedDialog.setIcon(pqw.QMessageBox.Warning)
            notSavedDialog.setText(f"Do You Want to Save {self.tabBrowser.widget(index).title} ?")
            notSavedDialog.setStandardButtons(pqw.QMessageBox.Save |
                                              pqw.QMessageBox.No |
                                              pqw.QMessageBox.Cancel)

            exit_code = notSavedDialog.exec_()
            if exit_code==pqw.QMessageBox.Save:
                save_exit_code =    self.tabBrowser.widget(index).save()
                if save_exit_code is Tab.CANCEL or save_exit_code is Tab.ERROR:
                    return CustomTabWidget.CANCEL

            elif exit_code==pqw.QMessageBox.Cancel:
                return CustomTabWidget.CANCEL

            if self.tabBrowser.widget(index).untitledNo == self.untitledNo:
                self.untitledNo-=1

    def changeTitle(self,tab, title):
        index = self.tabBrowser.indexOf(tab)
        self.tabBrowser.tabBar.setTabText(index, title)

    def changeSettings(self):
        config = ConfigChangeDialog(self.config).getConfigs()
        if config:
            self.setConfig(config)

    def setConfig(self , config : dict):

        self.textFont = config['font']

        self.changeFont()
        if  not config['toolBarCheck']  == self.config['toolBarCheck'] :
           if  config['toolBarCheck'] :
               self.toolbar.setVisible(True)
           else:
               self.toolbar.setVisible(False)

        if  not config['tabBarCheck']  == self.config['tabBarCheck'] :
           if  config['tabBarCheck'] :
               self.tabBar.setVisible(True)
           else:
               self.tabBar.setVisible(False)


        if config['tabBarCheck'] :
            self.removeToolBar(self.tabBar)
            self.addToolBar(config['tabBarPosition'], self.tabBar)
            self.tabBar.show()
            self.addToolBarBreak()
        if config['toolBarCheck']:
            self.removeToolBar(self.toolbar)
            self.addToolBar( config['toolBarPosition'], self.toolbar)
            self.toolbar.show()


        Tab.EDITOR_BG = config['editorBg']
        Tab.EDITOR_FG = config['editorFg']

        Tab.EDITOR_HL_BG = config['editorHlBg']
        Tab.EDITOR_HL_FG = config['editorHlFg']

        Tab.WORD_WRAP = config['wordWrap']




        for index in range( self.tabBrowser.count()):
            tab = self.tabBrowser.widget(index)
            tab.refreshAll()

        palette = self.toolbar.palette()

        palette.setColor( self.toolbar.backgroundRole(), config['toolBarBg'])
        palette.setColor(pqg.QPalette.Active, pqg.QPalette.Button, config['toolBarBg'])
        palette.setColor(pqg.QPalette.Active, pqg.QPalette.ButtonText, config['toolBarFg'])
        palette.setColor(pqg.QPalette.Active, pqg.QPalette.WindowText, config['toolBarFg'])
        palette.setColor(pqg.QPalette.Base, self.config['toolBarSrchBg'])

        p = self.searchBox.palette()
        p.setColor(pqg.QPalette.Base, config['toolBarSrchBg'])
        self.searchBox.setPalette(p)
        self.searchBox.update()
        self.fontBox.update()
        self.sizeBox.update()
        self.searchBox.show()
        self.fontBox.show()
        self.sizeBox.show()


        self.toolbar.setFloatable(False)
        self.toolbar.setAutoFillBackground(True)
        self.toolbar.setPalette(palette)
        self.toolbar.update()
        self.toolbar.show()



        self.boldBT.setAutoFillBackground(True)
        self.boldBT.setPalette(palette)
        self.boldBT.setFlat(True)
        self.italicBt.setAutoFillBackground(True)
        self.italicBt.setPalette(palette)
        self.italicBt.setFlat(True)
        self.underBt.setAutoFillBackground(True)
        self.underBt.setPalette(palette)
        self.underBt.setFlat(True)


        palette2= self.tabBar.palette()
        palette2.setColor(self.tabBar.backgroundRole(),config['tabBarBg'])
        self.tabBar.setAutoFillBackground(True)
        self.tabBar.update()
        self.tabBar.show()
        self.tabBar.setPalette(palette2)

      

        self.config = config
        self.saveConfig()

    def saveConfig(self):
        self.config['font'] = self.textFont

        self.settings.setValue('config', self.config)

    def loadConfig(self):
        config = self.settings.value('config')
        if config:
            self.setConfig(config)
            self.fontBox.setCurrentText(config['font'].family())


    def closeEvent(self, event: pqg.QCloseEvent) :
        toBeDel = 0
        for i in range (self.tabBrowser.count()):
           
            if self.tabBrowser.delTab(toBeDel) is CustomTabWidget.CANCEL:
                event.ignore()
                toBeDel+=1
            
        self.saveConfig()

    def toolbarPositionChanged(self,key,toolbar):
        self.config[key] = self.toolBarArea(toolbar)

    def toggleViewToolbar(self):
        if self.config['toolBarCheck']:
            self.toolbar.close()
        else:
            self.addToolBar(self.toolbar)
            self.toolbar.show()
        self.addToolBarBreak()
        self.config['toolBarCheck']= not self.config['toolBarCheck']

    def toggleViewTabbar(self):
        if self.config['tabBarCheck']:
            self.tabBar.close()
        else:
            self.toolbar.close()
            self.addToolBar(self.tabBar)
            self.tabBar.show()
            self.addToolBarBreak()
            self.addToolBar(self.toolbar)
            self.toolbar.show()
        self.config['tabBarCheck'] = not self.config['tabBarCheck']

    def startup (self) -> bool:
        return_ = False
        if sys.argv[1:]:
            for file in sys.argv[1:]:
                if  os.path.isfile(file):
                    return_ = True
                    self.addTab(file)
        return return_

    def help(self):
        print("sa")
        hw = HelpDialog()
        hw.show()
        hw.exec_()


if __name__ == '__main__':
    TextPy = pqw.QApplication(sys.argv)
    win = MainWinodw(TextPy)
    win.show()
    sys.exit(TextPy.exec_())

