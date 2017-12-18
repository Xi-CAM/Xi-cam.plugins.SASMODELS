from qtpy.QtCore import *
from qtpy.QtGui import QComboBox
from yapsy.IPlugin import IPlugin
from xicam.plugins import QWidgetPlugin


class SASModelsWidget(QWidgetPlugin):
    def __init__(self, *args, **kwargs):
        models_box = QComboBox()
        super(SASModelsWidget, self).__init__(*args, *kwargs)
