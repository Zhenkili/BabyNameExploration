import os

import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
from dash import Dash

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'baby-names-state.csv')
training_file = os.path.join(dirname, 'NationalNames.csv')

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
df = pd.read_csv(filename)
training_df = pd.read_csv(training_file, dtype={'Count': np.int32})