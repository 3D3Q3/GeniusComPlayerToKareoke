from PyQt5 import QtCore, QtGui

resources = QtCore.QResource()
resources.registerResource(":/resources.qrc")

def load_icon(name):
    return QtGui.QIcon(":/icons/{}".format(name))

def load_image(name):
    return QtGui.QImage(":/images/{}".format(name))