#! /usr/bin/env python

from sasmodels.core import load_model
from astropy.modeling import Parameter
from xicam.plugins import Fittable1DModelPlugin



def XicamModel(name, params):
    """
    XicamModel wraps sasmdoels from sasview (https://github.com/SasView/sasmodles),
    in a fittable 1-D plugin for Xi-cam. This object can be passed to astropy for
    data fitting.
    
    Args: 
        name (str) : name of the sasmoels (http://www.sasview.org/sasmodels/index.html)
        params (dict): key : value pairs of fittable parameters
    Returns:
        func (XicamFittable) : function that takes q-values and returns intensity values

"""
    inputs = [p.name for p in params]
    m = load_model(name)

    # evaluate callback
    def saxs_curve(q, *args):
        kernel = m.make_kernel([q])
        p_fit = dict(zip(inputs, args))
        return call_kernel(kernel, p_fit)

    # create an astropy fittable model
    names = {
        'inputs': inputs,
        'outputs': ['Iq'],
        'evaluate': staticmethod(saxs_curve)
    }
    p = dict((p.name, p) for p in params)
    names.update(p)
    return type('XicamFittable', (Fittable1DModelPlugin,), names)()

def main():
    import matplotlib.pyplot as plt
    import numpy as np
    q = np.linspace(0, 1, 512)
    name = 'cylinder'
    params =  { 'radius': 200., 'height':1000. }
    func = XicamModel(name, params)
    Iq = func(q)
    plt.loglog(q, Iq)
    plt.show()

if __name__ == '__main__':
    main()
