from pathlib import Path
import numpy as np
import dash_bio as dashbio
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import json
from dash.dependencies import Input, Output

from app import app
import circos_tab
import volcano_tab
import heatmap_tab


app.layout = html.Div(
    [
        dcc.Tabs(
            id="tabs",
            value="volcano-tab",
            children=[
                dcc.Tab(label="Volcano", value="volcano-tab"),
                dcc.Tab(label="Genome", value="genome-tab"),
                dcc.Tab(label="pBtic", value="pbtic-tab"),
                dcc.Tab(label="Clustergram", value="clustergram-tab"),
            ],
        ),
        html.Br(),
        html.Div(id="tab-content"),
    ]
)


@app.callback(Output("tab-content", "children"), Input("tabs", "value"))
def render_tab(tab):
    if tab == "pbtic-tab":
        return circos_tab.layout
    elif tab == "genome-tab":
        return circos_tab.layout
    elif tab == "volcano-tab":
        return volcano_tab.layout
    elif tab == "clustergram-tab":
        return heatmap_tab.layout


if __name__ == "__main__":
    app.run_server(debug=True)
