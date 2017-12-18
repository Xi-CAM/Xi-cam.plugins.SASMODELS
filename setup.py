"""
Usage: pip install -e .
       python setup.py install
       python setup.py bdist_wheel
       python setup.py sdist bdist_egg
       twine upload dist/*
"""

from setuptools import setup

setup(
    name='xicam.plugins.sasmodels',
    version='1.0.0',
    description= """ write something useful here """,

    # The project's main homepage.
    url='https://github.com/lbl-camera/sasmodels',

    # Author details
    author='Dinesh Kumar',
    author_email='dkumar@lbl.gov',

    # Choose your license
    license='Xi-CAM License',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Physics',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.6'
    ],

    # What does your project relate to?
    keywords='synchrotron analysis x-ray scattering SAXS WAXS',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=['sasmodels'],
    package_dir={'sasmodels':'sasmodels'},
    install_requires=['Xicam'],
    setup_requires=[],

    #extras_require={
    #    # 'dev': ['check-manifest'],
    #    'tests': ['pytest', 'coverage'],
    #},

    package_data={'sasmodels': ['*.yapsy-plugin']},
    # data_files=[],
    #entry_points={},
    #ext_modules=[],
    include_package_data=True
)
