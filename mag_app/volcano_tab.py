from pathlib import Path
import dash_bio as dashbio
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output

from app import app

diffexp_path = Path("data/p7-vs-empty.diffexp.tsv")
df = pd.read_csv(diffexp_path, sep=" ")
df["padj"] = df["padj"].fillna(1)


layout = html.Div(
    [
        "Log2 Fold Change",
        dcc.Input(
            id="volcanoplot-log2fc",
            type="number",
            min=-3,
            max=3,
            value=2,
        ),
        html.Br(),
        "Adjusted p-value",
        dcc.Input(
            id="volcanoplot-padj",
            type="number",
            min=1e-16,
            max=1,
            value=0.01,
        ),
        html.Br(),
        html.Div(id="volcano-div"),
    ]
)


@app.callback(
    Output("volcano-div", "children"),
    [
        Input("volcanoplot-log2fc", "value"),
        Input("volcanoplot-padj", "value"),
    ],
)
def update_volcanoplot(log2fc, padj):
    if padj < 1e-16:
        padj = 1e-16
    return dcc.Graph(
        id="volcanoplot",
        figure=dashbio.VolcanoPlot(
            dataframe=df,
            effect_size="log2FoldChange",
            p="padj",
            snp=None,
            gene="geneid",
            xlabel="Log2 Fold Change",
            ylabel="-log10(p-adjusted)",
            genomewideline_value=-np.log10(padj),
            effect_size_line=[-log2fc, log2fc],
            logp=True,
            title="",
        ),
    )
