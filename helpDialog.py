from PyQt5 import QtWidgets as pqw
from PyQt5 import QtCore as pqc
from PyQt5 import QtGui as pqg

html = '''
<html>
<style>
body {
   color: black;
   font-family: 'Segoe UI', Tahoma, Geneva,Verdana, sans-serif;
}

#textpy{
text-align:center;
}

#logo{
    height : 100px;
    weight : 100px;
    transform : translate(-100px);
}
</style>

<h1 id="textpy">TextPy</h1>
<h2 id="about">About</h2>
<p>TextPy is a simple text editor made using python and PyQt5. It is essentialy notepad with some additional features i added like tabs, color customization ,etc.
<br><br></p>
<h2 id="features">Features</h2>
<ul>
<li>Text search with options for case sensitive search and regular expressions</li>
<li>Option to work on multiple files at once uisng different tabs</li>
<li>Auto-Save option for automatically saved any unsaved files</li>
<li>Options to customize the colors of the different elements of the UI</li>
<li>Option to position the tab bar and the tool bar according to user preference</li>
<li>Several keyboard shortcuts to perform different actions</li>
</ul>
<h2 id="keyboard-shortcuts">Keyboard shortcuts</h2>
<p><br></p>
<table>
<thead>
<tr>
<th>Shortcut</th>
<th>Action</th>
</tr>
</thead>
<tbody>
<tr>
<td>CTRL + &#39;+&#39;</td>
<td>increase font size by 2</td>
</tr>
<tr>
<td>CTRL + &#39;-&#39;</td>
<td>decrease font size by 2</td>
</tr>
<tr>
<td>CTRL + O</td>
<td>Open</td>
</tr>
<tr>
<td>CTRL + S</td>
<td>Save</td>
</tr>
<tr>
<td>CTRL + X</td>
<td>Cut</td>
</tr>
<tr>
<td>CTRL + C</td>
<td>Copy</td>
</tr>
<tr>
<td>CTRL + V</td>
<td>Paste</td>
</tr>
<tr>
<td>CTRL + Z</td>
<td>Undo</td>
</tr>
<tr>
<td>CTRL + Y</td>
<td>Redo</td>
</tr>
<tr>
<td>CTRL + F</td>
<td>Find</td>
</tr>
<tr>
<td>CTRL + SHIFT + T</td>
<td>Toggle View Tool bar</td>
</tr>
<tr>
<td>CTRL + SHIFT + R</td>
<td>Toggle View Tab bar</td>
</tr>
<tr>
<td>CTRL + Q</td>
<td>Close</td>
</tr>
</tbody>
</table>
<p><br><br></p>
<h2 id="upcoming-feature">Upcoming feature</h2>
<p>These are the features i am currently working on :</p>
<ul>
<li>Text Replace</li>
<li>Print file
<br><br></li>
</ul>
<h2 id="what-am-i-using-">What Am I Using?</h2>
<ul>
<li>Python</li>
<li>PyQt5 </li>
</ul>
</html>



'''

class HelpDialog(pqw.QDialog):

    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("TextPy-help")
        self.layout = pqw.QHBoxLayout()
        self.txt = pqw.QTextEdit()
        self.txt.setHtml(html)
        self.layout.addWidget(self.txt)
        self.setLayout(self.layout)

