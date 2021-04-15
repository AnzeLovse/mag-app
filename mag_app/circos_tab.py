from pathlib import Path
import numpy as np
import dash_bio as dashbio
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import json
from dash.dependencies import Input, Output

from app import app

layout_genome = [
    {
        "id": "NZ_CP051858.1",
        "label": "",
        "color": "#c0c5ce",
        "len": 4865236,
    },
]

layout_pbtic = [
    {
        "id": "NZ_CP051859.1",
        "label": "",
        "color": "#c0c5ce",
        "len": 235425,
    },
]
hist_path = Path("data/histogram.json")
with open(hist_path, "r") as f:
    histogram_data = json.load(f)

hist_pbtic_path = Path("data/histogram_pbtic.json")
with open(hist_pbtic_path, "r") as f:
    histogram_pbtic = json.load(f)

annot_pos_path = Path("data/annotation_pos.json")
with open(annot_pos_path, "r") as f:
    annotation_pos = json.load(f)

annot_neg_path = Path("data/annotation_neg.json")
with open(annot_neg_path, "r") as f:
    annotation_neg = json.load(f)


def get_circos(layout, hist_pos, hist_neg, annotation_pos, annotation_neg):
    return dashbio.Circos(
        id="circos",
        layout=layout,
        enableZoomPan=True,
        enableDownloadSVG=True,
        selectEvent={
            "0": "click",
            "1": "click",
            "2": "click",
            "3": "click",
        },
        size=800,
        config={
            "innerRadius": 300,
            "outerRadius": 330,
        },
        tracks=[
            {
                "type": "HISTOGRAM",
                "data": hist_pos,
                "config": {
                    "tooltipContent": {"name": "value"},
                    "color": "#343d46",
                    "min": 0,
                    "innerRadius": 1.01,
                    "outerRadius": 1.4,
                    "labels": {"display": False},
                },
            },
            {
                "type": "HISTOGRAM",
                "data": hist_neg,
                "config": {
                    "tooltipContent": {"name": "value"},
                    "color": "#343d46",
                    "min": 0,
                    "innerRadius": 0.99,
                    "outerRadius": 0.6,
                },
            },
            {
                "type": "STACK",
                "data": annotation_pos,
                "config": {
                    "innerRadius": 320,
                    "outerRadius": 330,
                    "direction": "in",
                    "thickness": 5,
                    "strokeWidth": 0,
                    "tooltipContent": {
                        "name": "all",
                        # "chromosome": "block_id",
                        # "start": "start",
                        # "end": "end",
                    },
                    "color": {"name": "color"},
                },
            },
            {
                "type": "STACK",
                "data": annotation_neg,
                "config": {
                    "innerRadius": 300,
                    "outerRadius": 310,
                    "direction": "out",
                    "thickness": 5,
                    "strokeWidth": 0,
                    "tooltipContent": {
                        "name": "all",
                        # "chromosome": "block_id",
                        # "start": "start",
                        # "end": "end",
                    },
                    "color": {"name": "color"},
                },
            },
        ],
    )


layout = html.Div(
    [
        html.H1("Circos plot"),
        dcc.Loading(
            id="loading-circos",
            type="circle",
            # debug=True,
            children=[html.Div(id="circos-div")],
        ),
        html.Div(id="event-data-select"),
    ]
)


@app.callback(Output("circos-div", "children"), Input("tabs", "value"))
def render_circos(tab):
    if tab == "genome-tab":
        return get_circos(
            layout_genome,
            histogram_data,
            histogram_data,
            annotation_pos,
            annotation_neg,
        )
    elif tab == "pbtic-tab":
        return get_circos(
            layout_pbtic,
            histogram_pbtic,
            histogram_pbtic,
            annotation_pos,
            annotation_neg,
        )


@app.callback(
    Output("event-data-select", "children"),
    [Input("circos", "eventDatum")],
)
def update_output(value):
    if value is not None:
        return [html.Div("{}: {}".format(v.title(), value[v])) for v in value.keys()]
    return "There is no event data. Click or hover on a data point to get more information."
