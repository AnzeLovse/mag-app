import dash
from pathlib import Path
import dash_bio as dashbio
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objects as go

from app import app
from igv_tracks import tracks


DATASETS = {
    "t5": {
        "label": "DGE 5 min",
        "dataframe": None,
        "datafile": Path("data/timecourse_t5_shrunken.tsv"),
    },
    "t10": {
        "label": "DGE 10 min",
        "dataframe": None,
        "datafile": Path("data/timecourse_t10_shrunken.tsv"),
    },
    "t20": {
        "label": "DGE 20 min",
        "dataframe": None,
        "datafile": Path("data/timecourse_t20_shrunken.tsv"),
    },
    "t30": {
        "label": "DGE 30 min",
        "dataframe": None,
        "datafile": Path("data/timecourse_t30_shrunken.tsv"),
    },
}

for timepoint in DATASETS.keys():
    DATASETS[timepoint]["dataframe"] = pd.read_csv(
        DATASETS[timepoint]["datafile"], sep="\t"
    ).drop(["baseMean", "pvalue"], axis=1)
    DATASETS[timepoint]["dataframe"]["padj"] = DATASETS[timepoint]["dataframe"][
        "padj"
    ].fillna(1)
    # DATASETS[timepoint]["dataframe"] = DATASETS[timepoint]["dataframe"].set_index(
    #     "geneid", drop=False
    # )

diffexp_path = Path("data/timecourse_LRT.tsv")
df = pd.read_csv(diffexp_path, sep="\t")
df["padj"] = df["padj"].fillna(1)

dge_genes = df[df["padj"] < 0.05]["geneid"].to_list()
fold_changes = [
    DATASETS[timepoint]["dataframe"]
    .set_index("geneid", drop=False)
    .loc[dge_genes, "log2FoldChange"]
    .rename(timepoint)
    for timepoint in DATASETS
]
fc_df = pd.concat(fold_changes, axis=1)

tpms = pd.read_csv(Path("data/merged_tpm.tsv"), sep="\t").set_index("FEATURE_ID")

annotation = pd.read_csv(
    Path("data/annotation_with_gil01.bed"),
    sep="\t",
    header=None,
    names=["chr", "start", "end", "geneid", "type", "strand"],
).set_index("geneid", drop=False)

hm_df = annotation.loc[dge_genes]
hm_df[["chr", "start", "end"]].apply(lambda x: ".".join(str(x)), axis=1)
hm_df["coordinates"] = hm_df.chr.astype(str).str.cat(hm_df.start.astype(str), sep=":")
hm_df["coordinates"] = hm_df.coordinates.astype(str).str.cat(
    hm_df.end.astype(str), sep="-"
)
hm_df = hm_df.drop(columns=["chr", "start", "end", "strand"])

layout = html.Div(
    [
        html.Div(
            id="volcano-wrapper",
            className="five columns",
            children=[
                dcc.Tabs(
                    id="tabs",
                    value="volcano-tab",
                    children=[
                        dcc.Tab(
                            label="Volcano",
                            value="volcano-tab",
                            children=[
                                html.Div(
                                    id="vp-controls-block",
                                    children=[
                                        html.Div(
                                            id="dataset-control", children="Dataset: "
                                        ),
                                        dcc.Dropdown(
                                            id="vp-dataset-dropdown",
                                            options=[
                                                {
                                                    "label": DATASETS[dset]["label"],
                                                    "value": dset,
                                                }
                                                for dset in DATASETS
                                            ],
                                            value="t30",
                                        ),
                                        html.Div(
                                            id="logfc-control",
                                            children="Log2 Fold Change: ",
                                        ),
                                        dcc.Input(
                                            id="vp-log2fc",
                                            type="number",
                                            min=-3,
                                            max=3,
                                            value=2,
                                        ),
                                        html.Div(
                                            id="padj-control",
                                            children="Adjusted p-value: ",
                                        ),
                                        dcc.Input(
                                            id="vp-padj",
                                            type="number",
                                            min=1e-16,
                                            max=1,
                                            value=0.01,
                                        ),
                                    ],
                                ),
                                html.Div(id="volcano-div"),
                                html.Div(id="dge-table-div"),
                            ],
                        ),
                        # Heatmap tab
                        dcc.Tab(
                            label="Clustergram",
                            value="clustergram-tab",
                            children=[
                                html.Div(
                                    id="heatmap-div",
                                    children=[
                                        dcc.Graph(
                                            id="heatmap",
                                            figure=dashbio.Clustergram(
                                                data=fc_df,
                                                column_labels=list(
                                                    fc_df.columns.values
                                                ),
                                                width=700,
                                                height=900,
                                                row_labels=list(fc_df.index),
                                                # hidden_labels="row",
                                                center_values=False,
                                                cluster="row",
                                                row_dist="euclidean",
                                                optimal_leaf_order=True,
                                                color_map="orrd",
                                            ),
                                        )
                                    ],
                                ),
                                html.Div(
                                    id="heatmap-table-div",
                                    children=[
                                        dash_table.DataTable(
                                            id="heatmap_table",
                                            columns=[
                                                {"name": i, "id": i}
                                                for i in hm_df.columns
                                            ],
                                            data=hm_df.to_dict("records"),
                                            fixed_rows={"headers": True},
                                            style_table={"height": 400},
                                            filter_action="native",
                                            row_selectable="single",
                                            page_size=20,
                                        )
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
        html.Div(
            id="igv-div",
            className="five columns",
            children=[
                html.P(id="locus-sequence"),
                dashbio.Igv(
                    id="reference-igv",
                    locus="all",
                    reference={
                        "id": "BT",
                        "name": "Bacillus",
                        "fastaURL": "https://www.dropbox.com/s/ov34nkfx9lwozlh/genome_with_gil01.fasta?dl=0",
                        "indexURL": "https://www.dropbox.com/s/4qwskj15f34stc0/genome_with_gil01.fasta.fai?dl=0",
                        "order": 1000000,
                        "tracks": tracks,
                    },
                ),
                dcc.Graph(id="tpm-scatter"),
                dcc.Store(id="memory"),
                html.Div(id="test"),
            ],
        ),
    ],
)


@app.callback(
    Output("volcano-div", "children"),
    [
        Input("vp-log2fc", "value"),
        Input("vp-padj", "value"),
        Input("vp-dataset-dropdown", "value"),
    ],
)
def update_volcanoplot(log2fc, padj, timepoint):
    if padj < 1e-16:
        padj = 1e-16

    return [
        # html.B("Volcano plot"),
        # html.Hr(),
        dcc.Graph(
            id="volcanoplot",
            figure=dashbio.VolcanoPlot(
                dataframe=DATASETS[timepoint]["dataframe"],
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
        ),
    ]


@app.callback(
    Output("dge-table-div", "children"),
    [
        Input("vp-dataset-dropdown", "value"),
        Input("volcanoplot", "clickData"),
    ],
)
def update_table(timepoint, click):
    df = DATASETS[timepoint]["dataframe"]
    if click is not None:
        clicked_gene = click["points"][0]["text"].strip("<br>GENE: ")
        df["new"] = range(1, len(df) + 1)
        df.loc[df.geneid == clicked_gene, "new"] = 0
        df = df.sort_values("new").drop("new", axis=1)

        style_condition = {
            "if": {
                "filter_query": f"{{geneid}} = {clicked_gene}",
            },
            "backgroundColor": "rgb(192, 188, 188)",
        }
    else:
        style_condition = {}

    return (
        dash_table.DataTable(
            id="dge_table",
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict("records"),
            fixed_rows={"headers": True},
            sort_action="native",
            sort_mode="multi",
            style_table={"height": 400},
            filter_action="native",
            row_selectable="single",
            selected_rows=[0],
            page_size=20,
            style_data_conditional=[style_condition],
        ),
    )


@app.callback(
    Output("locus-sequence", "children"),
    [Input("memory", "data")],
)
def update_igv(data):
    clicked_gene = data["geneid"]
    gene_ann = annotation.loc[clicked_gene]
    return f"{gene_ann['chr']}:{gene_ann['start']}-{gene_ann['end']}"


@app.callback(
    Output("tpm-scatter", "figure"),
    [Input("memory", "data")],
)
def update_scatter(data):
    clicked_gene = data["geneid"]
    fig = go.Figure()
    x = [0, 0, 5, 5, 10, 10, 20, 20, 30, 30]
    y = tpms.loc[clicked_gene].iloc[0:10] + 1

    # Add traces
    fig.add_trace(go.Scatter(x=x, y=y, mode="markers", name="Control"))
    fig.add_trace(
        go.Scatter(
            x=[5, 5, 10, 10, 20, 20, 30, 30],
            y=tpms.loc[clicked_gene].iloc[10:18] + 1,
            mode="markers",
            name="MMC",
        )
    )
    fig.update_xaxes(title_text="Time")
    fig.update_yaxes(title_text="TPM + 1", type="log")
    fig.update_layout(title=f"TPMs in log scale of {clicked_gene}")

    return fig


@app.callback(
    Output("memory", "data"),
    [
        Input("dge_table", "derived_virtual_data"),
        Input("dge_table", "derived_virtual_selected_rows"),
        Input("heatmap_table", "derived_virtual_data"),
        Input("heatmap_table", "derived_virtual_selected_rows"),
    ],
)
def update_selection(data, row, data_ht, row_ht):
    trigger = dash.callback_context.triggered[0]["prop_id"]
    if trigger in ["dge_table.derived_virtual_selected_rows", "dge_table.derived_virtual_data"]:
        return data[row[0]]
    elif trigger == "heatmap_table.derived_virtual_selected_rows":
        return data_ht[row_ht[0]]


@app.callback(Output("test", "children"), Input("memory", "data"))
def update_selection(data):
    print(data)
