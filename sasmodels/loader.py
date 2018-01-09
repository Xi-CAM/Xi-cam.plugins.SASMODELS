#! /usr/bin/env python
# -*- coding: utf-8 -*-

import yaml
from collections import OrderedDict
from pyqtgraph.parametertree import Parameter
#from xicam.plugins import Fittable1DModelPlugin
#from factory import XicamModel

cfg = 'config.yml'

Categories = [\
    u'Shape Functions', \
#    u'Shape-Independent Functions', \
#    u'Structure Factors' \
    ]


# resolve metaclass conflict
class XiMetaParam(type(yaml.YAMLObject), type(Parameter)):
    pass

class XiCamParameter(yaml.YAMLObject, Parameter, metaclass=XiMetaParam):
    yaml_tag = u'!YMLParameter'
    def __init__(self, name, description, value, units, **kwags):
        self.value = value
        self.description = description
        Parameter.__init__(self, name=name, value = value, title = description)

    def __repr__(self):
        return "%s (%r, value=%r)" % \
            (self.__class__.__name__, self.description, self.value)

    @classmethod
    def from_yaml(cls, loader, node):
        tmp = loader.construct_mapping(node)
        return cls(**tmp)

def load_models():
    fp = open(cfg)
    yml =  yaml.load(fp)
    fp.close()
    fittables = []
    for cat in Categories:
        model_tree = OrderedDict()
        for key, val in yml[cat].items():
            models = OrderedDict()
            for name, params in val.items():
                params = [ p['param'] for p in params ]
                models[name] = params
            model_tree[key] = models
        fittables.append(model_tree)
    return fittables

if __name__ == '__main__':
    models = load_models()
    for key, val in models[0].items():
        print(str(key)+' : '+str(val))
