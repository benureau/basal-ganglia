import numpy as np
import colorsys

from bokeh import io
from bokeh.layouts import row, column
from bokeh import plotting as bkp
from bokeh.core.properties import value
from bokeh.models import FixedTicker
from bokeh.models.mappers import LinearColorMapper

import ipywidgets.widgets
from ipywidgets.widgets import fixed, IntSlider, FloatSlider, SelectionSlider


    ## Disable autoscrolling

from IPython.display import display, Javascript

disable_js = """
IPython.OutputArea.prototype._should_scroll = function(lines) {
    return false;
}
"""
display(Javascript(disable_js))


    ## Larger labels

from IPython.display import HTML

display(HTML('''<style>
    .widget-label { min-width: 20ex !important; }
</style>'''))


    ## Load bokeh for jupyter

bkp.output_notebook(hide_banner=True)


    ## Better default figures

def tweak_fig(fig):
    tight_layout(fig)
    disable_minor_ticks(fig)
    disable_grid(fig)
    fig.toolbar.logo = None

def tight_layout(fig):
    fig.min_border_top    = 35
    fig.min_border_bottom = 35
    fig.min_border_right  = 35
    fig.min_border_left   = 35

def disable_minor_ticks(fig):
    #fig.axis.major_label_text_font_size = value('8pt')
    fig.axis.minor_tick_line_color = None
    fig.axis.major_tick_in = 0

def disable_grid(fig):
    fig.xgrid.grid_line_color = None
    fig.ygrid.grid_line_color = None


def figure(*args, **kwargs):
    fig = bkp.figure(*args, **kwargs)
    tweak_fig(fig)
    return fig


    ## Removing returns

def show(*args, **kwargs):
    return bkp.show(*args, **kwargs)

def interact(*args, **kwargs):
    ipywidgets.widgets.interact(*args, **kwargs)

def select(name, options):
    return SelectionSlider(description=name,  options=list(options))

    ## Graphs

def best(records, fig=None, lines=None, handle=None, show=True):
    return graph_aux1(records, key='best', fig=fig, lines=lines, handle=handle, show=show)

def value(records, fig=None, lines=None, handle=None, show=True):
    return graph_aux2(records, key='value', fig=fig, lines=lines, handle=handle, show=show)


y_ranges = {'best': (0.0, 1.2), 'value': (0.25, 0.75)}

def graph_aux1(records, key, fig=None, lines=None, handle=None, show=True):
    """Display graph of best choice"""

    P_mean = np.mean(records[key], axis=0)
    assert len(P_mean.shape) == 1, "P_mean has the wrong shape. Use graph_aux2() instead."

    if fig is None:
        fig = figure(y_range=y_ranges.get(key, None), plot_width=900, plot_height=300, tools="")

    if lines is None:
        lines = {}
        lines['mean'] = fig.line(range(0, len(P_mean)), P_mean)
    else:
        lines['mean'].data_source.data['x'] = range(0, len(P_mean))
        lines['mean'].data_source.data['y'] = P_mean
        #io.push_notebook(handle=handle)

    if show: # new handle
        handle = bkp.show(fig, notebook_handle=True)

    return handle, fig, lines

def graph_aux2(records, key, fig=None, lines=None, handle=None, show=True):
    """Display graph of best choice"""

    P_mean = np.mean(records[key], axis=0)
    assert len(P_mean.shape) > 1, "P_mean has the wrong shape. Use graph_aux1() instead."

    if fig is None:
        fig = figure(y_range=y_ranges.get(key, None), plot_width=900, plot_height=300, tools="")


    line_colors = {'A': "#fa6900", 'B': "#69d2e7"}

    if lines is None:
        lines = {'mean': []}
        for j, stimulus in enumerate(['A', 'B']):
            lines['mean'].append(fig.line(range(0, len(P_mean[:,j])), P_mean[:,j],
                                          line_color=line_colors[stimulus], legend=stimulus), )
    else:
        for j, stimulus in enumerate(['A', 'B']):
            lines['mean'][j].data_source.data['x'] = range(0, len(P_mean[:,j]))
            lines['mean'][j].data_source.data['y'] = P_mean[:,j]
        #io.push_notebook(handle=handle)

    if show: # new handle
        handle = bkp.show(fig, notebook_handle=True)

    return handle, fig, lines
