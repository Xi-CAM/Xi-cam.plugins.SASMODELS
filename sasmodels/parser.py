#! /usr/bin/env python
# -*- coding: utf-8 -*-

import yaml
import pyqtgraph
from pyqtgraph.parametertree import Parameter, ParameterTree

cfg = 'config.yml'

class YParameter(yaml.YAMLObject):
    yaml_tag = u'!YMLParameter'
    def __init__(self, name, description, units, value):
        self.name = name
        self.units = units
        self.value = value
    def __repr__(self):
        return "%s (%r, value=%r)" % \
            (self.__class__.__name__, self.description, self.value)

    def pyqgtParam(self):
        return Parameter.create(name=self.name, value=self.value)

def load_models():
    fp = open(cfg)
    yml_fcns =  yaml.load(fp)
    fp.close()

    shape_fcns = dict()
    for key, val in yml_fcns['Shape Functions'].items():
        shape_fcns[key] = Parameter.create(name=key)
        ''' iterate over spacial cases of the shape '''
        for k, params in val.items():
            shape = Parameter.create(name=k)
            for p in params:
                shape.addChild(p['param'].pyqgtParam())
        shape_fcns[key].addChild(shape)

    return shape_fcns

if __name__ == '__main__':
    models = load_models()
    print(models)
