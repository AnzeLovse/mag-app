from pathlib import Path

import dash_bio as dashbio
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import scipy.stats as stats
from dash.dependencies import Input, Output

from app import app

tpm_path = Path("data/merged_tpm.tsv")
tpm = pd.read_csv(tpm_path, sep="\t").set_index("FEATURE_ID")

z_score = tpm.apply(stats.zscore, axis=1, result_type="expand").dropna()
z_score.columns = tpm.columns

layout = html.Div(
    [
        dcc.Graph(
            figure=dashbio.Clustergram(
                data=z_score,
                column_labels=list(tpm.columns.values),
                row_labels=list(tpm.index),
                hidden_labels="row",
                height=900,
                width=900,
                center_values=False,
                col_dist="correlation",
                row_dist="correlation",
                # optimal_leaf_order=True,
                color_map="rdbu",
            )
        )
    ]
)
