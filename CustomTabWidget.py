from PyQt5 import QtWidgets as pqw
from PyQt5 import QtCore as pqc
from PyQt5 import QtGui as pqg
import sys


class CustomTabWidget(pqw.QStackedWidget):

    CANCEL = "CUSTOMTABWIDGET.CANCEL"

    def __init__(self, parent=None, *args,**kwargs):
        super().__init__(parent , *args, **kwargs)
        self.tabBar = pqw.QTabBar(parent)
        self.tabBar.setMovable(True)
        self.tabBar.currentChanged.connect(self.changeTabFromTabBar)
        self.currentChanged.connect(self.changeTab)
        self.tabBar.tabBarDoubleClicked.connect(lambda : self.delTab(self.tabBar.currentIndex()) if self.doubleTapDel else None)
        self.addBt=False
        self.addTabFunc = None
        self.doubleTapDel =False
        self.delFunc = None
        self.onCurrentTabChange = None

    def addTab(self, widget : pqw.QWidget, title):

        self.addWidget(widget)
        if self.addBt:
            self.tabBar.insertTab(self.lastTabIndex()+1,title)
        else:
            self.tabBar.addTab(title)



    def changeTabFromTabBar(self):
        if self.onCurrentTabChange:
            self.onCurrentTabChange(self.tabBar.currentIndex())
        if self.tabBar.currentIndex() == self.lastTabIndex() and self.tabBar.tabText(self.lastTabIndex()) == "+":
            current = self.currentIndex()
            self.tabBar.removeTab(self.lastTabIndex())
            if self.addTabFunc:
                self.addTabFunc()
            self.tabBar.addTab('+')
            self.tabBar.setCurrentIndex(current)


        self.setCurrentIndex(self.tabBar.currentIndex())

    def changeTab(self):
        self.tabBar.setCurrentIndex(self.currentIndex())

    def setAddBt(self, addBt:bool):

        if self.addBt and not addBt:
            self.tabBar.removeTab(self.tabBar.count()-1)

        if not self.addBt and addBt:
            self.tabBar.addTab('+')
        self.addBt = addBt

    def lastTabIndex(self):
        return self.tabBar.count()-1

    def setAddTabFunc(self, func=None):
        self.addTabFunc = func

    def getAddTAbFunc(self):
        return self.addTabFunc

    def getAddBt(self) ->bool:
        return self.addBt

    def getDoubleTapDel(self) -> bool:
        return  self.doubleTapDel

    def setDoubleTapDel(self, doubleTapCheck :bool = False):
        self.doubleTapDel = doubleTapCheck

    def getDelFunc(self):
        return self.delFunc

    def setDelFunc(self, func):
        self.delFunc = func

    def delTab(self, index:int):
      
        if self.addBt:
           
            if index == self.lastTabIndex():
               
                return
            self.tabBar.removeTab(self.lastTabIndex())
       
        if self.delFunc:
            if self.delFunc(index) is CustomTabWidget.CANCEL:
                
                if self.addBt:
                    self.tabBar.addTab('+')
                  
               
                return CustomTabWidget.CANCEL

      
        self.tabBar.removeTab(index)
        self.removeWidget(self.widget(index))
        if self.addBt:
            self.tabBar.addTab('+')


    def setOnCurrentTabChange(self, func):
        self.onCurrentTabChange = func

    def getOnCurrentTabChange(self):
        return self.onCurrentTabChange


if __name__ == '__main__':

    app = pqw.QApplication(sys.argv)
    win = pqw.QWidget()
    lay = pqw.QVBoxLayout()
    c = CustomTabWidget(win)
    lay.addWidget(c)
    lay.addWidget(c.tabBar)
    win.setLayout(lay)

    c.addTab( pqw.QLabel(text = "1" ), "1")
    c.addTab(pqw.QLabel(text = "2") , "2")
    c.addTab(pqw.QLabel(text = "3") , "3")

    win.show()
    win.setStyleSheet('''
        QLabel{background-color:red;}
    ''')
    app.exec_()