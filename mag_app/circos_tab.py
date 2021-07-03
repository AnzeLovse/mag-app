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
hist_path = Path("data/pDG_M-1_coverage_pos.json")
with open(hist_path, "r") as f:
    histogram_data = json.load(f)

hist_path = Path("data/pDG_M-1_coverage_neg.json")
with open(hist_path, "r") as f:
    histogram_neg = json.load(f)

hist_pbtic_path = Path("data/pDG_M-1_coverage_pos_pbtic.json")
with open(hist_pbtic_path, "r") as f:
    histogram_pbtic = json.load(f)

hist_pbtic_path = Path("data/pDG_M-1_coverage_neg_pbtic.json")
with open(hist_pbtic_path, "r") as f:
    histogram_pbtic_neg = json.load(f)

hist_path = Path("data/pDG7_M-1_coverage_pos.json")
with open(hist_path, "r") as f:
    pdg7_pos = json.load(f)

hist_path = Path("data/pDG7_M-1_coverage_neg.json")
with open(hist_path, "r") as f:
    pdg7_neg = json.load(f)

hist_pbtic_path = Path("data/pDG7_M-1_coverage_pos_pbtic.json")
with open(hist_pbtic_path, "r") as f:
    pdg7_pbtic_pos = json.load(f)

hist_pbtic_path = Path("data/pDG7_M-1_coverage_neg_pbtic.json")
with open(hist_pbtic_path, "r") as f:
    pdg7_pbtic_neg = json.load(f)


annot_pos_path = Path("data/annotation_pos.json")
with open(annot_pos_path, "r") as f:
    annotation_pos = json.load(f)

annot_neg_path = Path("data/annotation_neg.json")
with open(annot_neg_path, "r") as f:
    annotation_neg = json.load(f)


def get_circos(
    layout, hist_pos, hist_neg, hist2_pos, hist2_neg, annotation_pos, annotation_neg
):
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
            "4": "click",
            "5": "click",
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
                    "innerRadius": 0.9,
                    "outerRadius": 0.99,
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
                    "innerRadius": 0.89,
                    "outerRadius": 0.8,
                },
            },
            {
                "type": "HISTOGRAM",
                "data": hist2_pos,
                "config": {
                    "tooltipContent": {"name": "value"},
                    "color": "#343d46",
                    "min": 0,
                    "innerRadius": 0.7,
                    "outerRadius": 0.79,
                },
            },
            {
                "type": "HISTOGRAM",
                "data": hist2_neg,
                "config": {
                    "tooltipContent": {"name": "value"},
                    "color": "#343d46",
                    "min": 0,
                    "innerRadius": 0.69,
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
        html.Div(id="igv-data"),
    ]
)


@app.callback(Output("circos-div", "children"), Input("tabs", "value"))
def render_circos(tab):
    if tab == "genome-tab":
        return get_circos(
            layout_genome,
            histogram_data,
            histogram_neg,
            pdg7_pos,
            pdg7_neg,
            annotation_pos,
            annotation_neg,
        )
    elif tab == "pbtic-tab":
        return get_circos(
            layout_pbtic,
            histogram_pbtic,
            histogram_pbtic_neg,
            pdg7_pbtic_pos,
            pdg7_pbtic_neg,
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


@app.callback(
    Output("igv-data", "children"),
    Input("circos", "eventDatum"),
)
def update_igv(value):
    locus = f"{value['block_id']}:{value['start']}-{value['end']}"
    return html.Div(
        [
            dashbio.Igv(
                id="reference-igv",
                locus=locus,
                reference={
                    "id": "BT",
                    "name": "Bacillus",
                    "fastaURL": "https://www.dropbox.com/s/d5l4y4l4jfdq1kb/genome.fasta?dl=0",
                    "indexURL": "https://www.dropbox.com/s/oszr2wplvcipg81/genome.fasta.fai?dl=0",
                    "order": 1000000,
                    "tracks": [
                        {
                            "name": "Annotations",
                            "url": "https://www.dropbox.com/s/uppcza47p94m4t0/annotation.gtf?dl=0",
                            "displayMode": "EXPANDED",
                            "nameField": "gene",
                            "height": 150,
                            "color": "rgb(176,141,87)",
                        }
                    ],
                },
            ),
        ]
    )
