#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider
from bokeh.layouts import row, widgetbox
from bokeh.io import curdoc
from scipy.stats import beta
import numpy as np


def set_prior(a, b):
    return beta(a, b)

def set_posterior(a, b, n_heads, n_tails):
    return beta(a + n_heads, b + n_tails)


# Set up data
a = 1
b = 1
n_heads = 0
n_tails = 0

x = np.linspace(0, 1, 500)
prior = set_prior(a, b)
posterior = set_posterior(a, b, n_heads, n_tails)

source = ColumnDataSource({'x': x, 'prior': prior.pdf(x), 'posterior': posterior.pdf(x)})

# Set up plot
p = figure(height=500, width=600, toolbar_location=None)
p.line(source=source, x='x', y='prior', line_width=3, alpha=0.6, legend='Prior')
p.line(source=source, x='x', y='posterior', color='firebrick', line_width=2, alpha=0.6, legend='Posterior')

p.xaxis.axis_label = 'Prob(Heads)'
p.yaxis.axis_label = 'Probability Density'
p.axis.axis_label_text_font_style = 'normal'
p.axis.axis_label_text_font_size = '18pt'
p.axis.major_label_text_font_size = '16pt'
p.outline_line_width = 1
p.outline_line_alpha = 1
p.outline_line_color = "black"

# Set up widgets
a_value = Slider(title="a", value=a, start=1, end=100, step=1)
b_value = Slider(title="b", value=b, start=1, end=100, step=1)
heads = Slider(title="heads", value=n_heads, start=0, end=200, step=1)
tails = Slider(title="tails", value=n_tails, start=0, end=200, step=1)

# Set up callbacks
def update_data(attrname, old, new):

    # Get the current slider values
    a = a_value.value
    b = b_value.value
    h = heads.value
    t = tails.value

    # Generate the new curve
    prior = set_prior(a, b)
    posterior = set_posterior(a, b, h, t)

    source.data = {'x': x, 'prior': prior.pdf(x), 'posterior': posterior.pdf(x)}

for w in [a_value, b_value, heads, tails]:
    w.on_change('value', update_data)

# Set up layouts and add to document
inputs = widgetbox(a_value, b_value, heads, tails, width=500)

layout = row(inputs, p, width=800, name='content')
curdoc().add_root(layout)
curdoc().title = "Bayesian Coin Flipping"
