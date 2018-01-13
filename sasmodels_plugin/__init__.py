#! /usr/bin/env python
# -*- coding: utf-8 -*- 

from yapsy.IPlugin import IPlugin
from xicam.plugins import QWidgetPlugin
from qtpy.QtWidgets import QVboxLayout, QComboBox, QPushButton
from collections import OderedDict

from astropy.modeling import fitting
from loader import load_models, Categories



class SASModelsWidget(QWidgetPlugin):
    name = 'SASModel'

    fitters = OrderedDict({
        'LinearLSQFitter': fitting.LinearLSQFitter,
        'LevMarLSQFitter': fitting.LevMarLSQFitter,
        'SLSQPLSQFitter' : fitting.SLSQPLSQFitter
        })
    
    def __init__(self, *args, **kwargs):
        models = load_models()
        super().__init__(self, *args, *kwargs)

        # verticle layout
        self.vlayout = QVboxLayout()

        # add a dropdown list of fitting routines
        self.fitterbox = QComboBox()
        self.fitterox.addItems(list(fitters.keys()))
        self.vlayout.addWidget(self.fitterbox)

        # add a dropdown list of model catagories
        self.catbox = QComboBox()
        self.catbox.addItems(Categories)
        self.vlayout.addWidget(self.catbox)

        # add menu for sub-catagories 
        cat = self.catbox.currentText()
        self.subcatbox = QComboBox()
        self.subcatbox.addItems(list(models[cat]))
        self.vlayout.addWidget(self.subcatbox)

        # add list of models in subcategory
        subcat = self.subcatbox.currentText()
        self.modelsbox = QComboBox()
        self.modelsbox.addItems(list(models[cat][subcat]))
        self.vlayout.addWidget(self.modelsbox)

        # add parameter tree
        model = self.modelsbox.currentText()
        self.fittable = models[cat][subcat][model]._model
        self.param_tree = ParameterTree(showTop=False)
        self.param_tree.addParameters(models[cat][subcat][model]['params'])  
        self.vlayout.addWidget(self.param_tree)

        # add fit-button 
        fit_button = QPushButton('Fit')
        fit_button.setToolTip('Fit model to the data')
        self.vlayout.addWidget(fit_button)
        self.fit_button.clicked.connect(self.run)

    def run(self, x, y):
        key = self.fitterbox.currentText()
        fit = self.fitters[key]()
        self._opt = fit(self.fittable, x, y) 
 
