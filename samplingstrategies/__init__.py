'''
This package contains all SamplingStrategy implementations meant for use by the Zoetrope web app.
In order to contribute a new SamplingStrategy, please complete the following steps:
    1) Add a file to this directory containing your SamplingStrategy subclass with a unique
       and descriptive name. See randombuildings.py as an example of how to do this.
    2) Add a line in this __init__.py file with an import for your SamplingStrategy
    3) Register your SamplingStrategy in the STRATEGIES dictionary under sample/views.py
'''

from .randombuildings import RandomBuildings
