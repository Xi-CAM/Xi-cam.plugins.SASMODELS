#! /usr/bin/env python
# -*- coding: utf-8 -*- 

from yapsy.IPlugin import IPlugin
from xicam.plugins import QWidgetPlugin
form xicam.gui import threads
from qtpy.QtWidgets import QVboxLayout, QComboBox, QPushButton
from collections import OderedDict

from astropy.modeling import fitting
from factory import XicamSASModel
from loader import load_models, Categories



class SASModelsWidget(QWidgetPlugin):
    name = 'SASModel'

    fitters = OrderedDict({
        'LinearLSQFitter': fitting.LinearLSQFitter,
        'LevMarLSQFitter': fitting.LevMarLSQFitter,
        'SLSQPLSQFitter' : fitting.SLSQPLSQFitter
        })
    
    def __init__(self, *args, **kwargs):
        self.models = load_models()
        super().__init__(self, *args, *kwargs)

        # verticle layout
        vlayout = QVboxLayout()

        # add a dropdown list of fitting routines
        self.fitterbox = QComboBox()
        self.fitterox.addItems(list(fitters.keys()))
        vlayout.addWidget(self.fitterbox)

        # add a dropdown list of model catagories
        self.catbox = QComboBox()
        self.catbox.addItems(Categories)
        vlayout.addWidget(self.catbox)

        # add menu for sub-catagories 
        cat = self.catbox.currentText()
        self.subcatbox = QComboBox()
        self.subcatbox.addItems(list(self.models[cat]))
        vlayout.addWidget(self.subcatbox)

        # add list of models in subcategory
        subcat = self.subcatbox.currentText()
        self.modelsbox = QComboBox()
        self.modelsbox.addItems(list(self.models[cat][subcat]))
        vlayout.addWidget(self.modelsbox)

        # add parameter tree
        modelname = self.modelsbox.currentText()
        parameters = self.models[cat][subcat][modelname]['params']
        param_tree = ParameterTree(showTop=False)
        param_tree.addParameters(self.parameters)
        vlayout.addWidget(param_tree)
        self.fittable = XicamSASModel(modelname, parameters)

        # add fit-button 
        fit_button = QPushButton('Fit')
        fit_button.setToolTip('Fit model to the data')
        vlayout.addWidget(fit_button)
        fit_button.clicked.connect(self.run)

    def update_model(self):
        cat = self.catbox.currentText()
        subcat = self.subcatbox.currentText()
        modelname = self.modelsbox.currentText()
        parameters = self.models[cat][subcat][modelname]['params']
        self.fittable = XicamSASModel(modelname, parameters)
        for p in parameters:
            if not p.name() in self.fittable.param_names:
                raise KeyError
            # set fixed if true
            self.fittable.fixed[p.name()] = p.child('Fixed').value()
            # set bounds if available
            if p.child('Bounded').value():
                bounds = (p.child('Bounded').child('Lower').value(),
                            p.child('Bounded').child('Upper').value())        
                self.fittable.bounds[p.name()] = bounds 
            else:
                self.fittable.bounds[p.name()] = (-np.inf, np.inf)

    def update(self, t):
        self.opt = t

    def run(self, q, I):
        self.update_model()
        key = self.fitterbox.currentText()
        fitting_method = fitters[key]()
        threads.QThreadFuture(fitting_method, self.fittable, q, I, callback_slot=update)
