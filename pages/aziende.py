import dash
from dash import dcc, html, Input, Output, callback
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
import numpy as np

# pd.set_option('display.max_columns', None)
suppress_callback_exceptions = True
dash.register_page(__name__, path="/aziende")

dff = pd.read_csv(r'E:\tesi\tesi\apps\files\dataClean.csv')
df = dff.copy()

# ----------------------------------------------------------------------------------------------------------------------
# lettura preliminare dati

sceltautente = pd.read_csv(r'pages\files\selectedrow.txt', header=None)
dati_iniziali = sceltautente.iloc[0, 0]

if dati_iniziali == "":
    df_temp = df.sort_values(by='Redditività di tutto il capitale investito (ROI) (%)\n%\n2020', ascending=False)
    dati_iniziali = df_temp.loc[0, "ATECO 2007\ndescrizione"]

# --------------------------------------------------------------------------------------------------------------------
# TABELLA INIZIO PAGINA

ddf_ = []
for i in range(len(df)):
    if df.loc[i, "ATECO 2007\ndescrizione"] == dati_iniziali:
        ddf_.append(df.iloc[i, :])

ddf_ = pd.concat(ddf_, axis=1)
ddf_ = ddf_.transpose()
# ddf_ = ddf_.sort_values(by='Redditività di tutto il capitale investito (ROI) (%)\n%\n2020', ascending=False)
ddf_.reset_index(inplace=True)
ddf_.drop("index", axis=1, inplace=True)

dftables_ = ddf_.groupby(
    ["Ragione sociale", "ATECO 2007\ndescrizione"], as_index=False).agg(
    {'Redditività di tutto il capitale investito (ROI) (%)\n%\n2020': 'mean',
     'Indice di indebitam. a breve\n%\n2020': 'mean',
     'Indice di indebitam. a lungo\n%\n2020': 'mean',
     'EBITDA/Vendite (%)\n%\n2020': 'mean',
     'Posizione finanziaria netta\nEUR\n2020': 'mean',
     'Indirizzo sede legale - Latitudine': 'mean',
     'Indirizzo sede legale - Longitudine': 'mean',
     "Ricavi delle vendite\nEUR\n2020": 'mean',
     "Ricavi delle vendite\nEUR\n2019": 'mean',
     "Ricavi delle vendite\nEUR\n2018": 'mean',
     "Ricavi delle vendite\nEUR\n2017": 'mean',
     "Ricavi delle vendite\nEUR\n2016": 'mean',
     }
)
dftables_["Redditività di tutto il capitale investito (ROI) (%)\n%\n2020"] = dftables_[
    "Redditività di tutto il capitale investito (ROI) (%)\n%\n2020"].round(2)
dftables_["Indice di indebitam. a breve\n%\n2020"] = dftables_["Indice di indebitam. a breve\n%\n2020"].round(2)
dftables_["Indice di indebitam. a lungo\n%\n2020"] = dftables_["Indice di indebitam. a lungo\n%\n2020"].round(2)
dftables_["EBITDA/Vendite (%)\n%\n2020"] = dftables_["EBITDA/Vendite (%)\n%\n2020"].round(2)
dftables_["Posizione finanziaria netta\nEUR\n2020"] = dftables_["Posizione finanziaria netta\nEUR\n2020"].round(2)
dftables_["Ricavi delle vendite\nEUR\n2020"] = dftables_["Ricavi delle vendite\nEUR\n2020"].round(2)
dftables_["Ricavi delle vendite\nEUR\n2019"] = dftables_["Ricavi delle vendite\nEUR\n2019"].round(2)
dftables_["Ricavi delle vendite\nEUR\n2018"] = dftables_["Ricavi delle vendite\nEUR\n2018"].round(2)
dftables_["Ricavi delle vendite\nEUR\n2017"] = dftables_["Ricavi delle vendite\nEUR\n2017"].round(2)
dftables_["Ricavi delle vendite\nEUR\n2016"] = dftables_["Ricavi delle vendite\nEUR\n2016"].round(2)

dftables_.columns = ['Ragione sociale', 'Descrizione',
                     'ROI (%)', 'Indebitamento a breve', 'Indebitamento a lungo', 'Margine di EBITDA',
                     'Posizione finanziaria netta', 'Latitudine', 'Longitudine', "Ricavi 2020",
                     "Ricavi 2019", "Ricavi 2018", "Ricavi 2017", "Ricavi 2016", ]

datas = []
for i in range(len(df)):
    if df.loc[i, "ATECO 2007\ndescrizione"] == dati_iniziali:
        datas.append(df.iloc[i, :])

datas = pd.concat(datas, axis=1)
datas = datas.transpose()
datas.reset_index(inplace=True)
datas.drop("index", axis=1, inplace=True)

# incremento EBITDA(2020-2016)
incremento_EBITDA = datas.apply(
    lambda x: (x['EBITDA\nEUR\n2020'] - x['EBITDA\nEUR\n2016']) * (100 / (x['EBITDA\nEUR\n2016'] + 1)),
    axis=1)

dftables_["Incremento EBITDA"] = incremento_EBITDA
dftables_["Incremento EBITDA"] = dftables_["Incremento EBITDA"].round(2)

# Crescita fatturato(2020-2016)
crescita_fatturato = datas.apply(
    lambda x: (x['Ricavi delle vendite\nEUR\n2020'] - x['Ricavi delle vendite\nEUR\n2016']) * 100 / (
            x['Ricavi delle vendite\nEUR\n2016'] + 1),
    axis=1)

dftables_["Crescita fatturato (%)"] = crescita_fatturato
dftables_["Crescita fatturato (%)"] = dftables_["Crescita fatturato (%)"].round(2)

# quick ratio (denaro/DEBITI A BREVE\nEUR\n2020)
quick_ratio = datas.apply(
    lambda x: (x['Denaro in cassa\nEUR\n2020'] / (x['DEBITI A BREVE\nEUR\n2020'] + 1)),
    axis=1)
dftables_["Quick ratio"] = quick_ratio
dftables_["Quick ratio"] = dftables_["Quick ratio"].round(2)

# remove outlier
cols = ['ROI (%)', 'Margine di EBITDA', 'Posizione finanziaria netta', "Incremento EBITDA", "Quick ratio",
        "Crescita fatturato (%)", "Ricavi 2020", "Ricavi 2019", "Ricavi 2018", "Ricavi 2017", "Ricavi 2016"]
Q1 = dftables_[cols].quantile(0.25)
Q3 = dftables_[cols].quantile(0.75)
IQR = Q3 - Q1

fer = dftables_[
    ~((dftables_[cols] < (Q1 - 1.5 * IQR)) | (dftables_[cols] > (Q3 + 1.5 * IQR))).any(axis=1)]

dftables_ = fer
dftables_.reset_index(inplace=True)
dftables_.drop("index", axis=1, inplace=True)
dftables_ = dftables_.sort_values(by='Crescita fatturato (%)', ascending=False)

# ----------------------------------------------------------------------------------------------------------------------
#   POPOLA TABELLA

populate_table = df.groupby(
    ["Ragione sociale"], as_index=False).agg(
    {'Redditività di tutto il capitale investito (ROI) (%)\n%\n2020': 'mean',
     'Indice di indebitam. a breve\n%\n2020': 'mean',
     'Indice di indebitam. a lungo\n%\n2020': 'mean',
     'EBITDA/Vendite (%)\n%\n2020': 'mean',
     'Posizione finanziaria netta\nEUR\n2020': 'mean'
     }
)
populate_table.columns = ['Ragione sociale', 'ROI (%)', 'Indebitamento a breve', 'Indebitamento a lungo',
                          'Margine di EBITDA', 'Posizione finanziaria netta']
populate_table['Incremento EBITDA'] = np.nan
populate_table['Crescita fatturato (%)'] = np.nan
populate_table['Quick ratio'] = np.nan
populate_table['Incremento EBITDA'] = np.nan
# populate_table['ROE (%)'] = np.nan

# reassign the dataframes columns
# print(populate_table.columns.tolist())

cols = ['Ragione sociale', 'Crescita fatturato (%)', 'ROI (%)', 'Posizione finanziaria netta',
        'Incremento EBITDA', 'Margine di EBITDA', 'Quick ratio', 'Indebitamento a breve', 'Indebitamento a lungo']
populate_table = populate_table[cols]

# ----------------------------------------------------------------------------------------------------------------------
# SCATTERMAP BOX

map = df.groupby(
    ['Ragione sociale', 'ATECO 2007\ncodice', 'ATECO 2007\ndescrizione',
     'Indirizzo sede legale - Latitudine', 'Indirizzo sede legale - Longitudine'], as_index=False).agg(
    {'Redditività di tutto il capitale investito (ROI) (%)\n%\n2020': "mean",
     'EBITDA/Vendite (%)\n%\n2020': 'mean',
     'Posizione finanziaria netta\nEUR\n2020': 'mean',
     'Denaro in cassa\nEUR\n2020': 'mean',
     'DEBITI A BREVE\nEUR\n2020': 'mean'
     }
)
# map["ROE (%)"] = np.nan
map.columns = ['Ragione sociale', 'ATECO', 'Descrizione', 'Latitudine', 'Longitudine', 'ROI (%)',
               'Margine di EBITDA', 'Posizione finanziaria netta', 'Denaro in cassa', 'Debiti a breve']

# quick ratio (denaro/DEBITI A BREVE\nEUR\n2020)
quick_ratio = map.apply(
    lambda x: (x['Denaro in cassa'] / (x['Debiti a breve'] + 1)),
    axis=1)
map["Quick ratio"] = quick_ratio
map["Quick ratio"] = map["Quick ratio"].round(2)


# ----------------------------------------------------------------------------------------------------------------------

def popola_df(data):
    ddf_ = []
    for i in range(len(df)):
        if df.loc[i, "ATECO 2007\ndescrizione"] == data:
            ddf_.append(df.iloc[i, :])

    ddf_ = pd.concat(ddf_, axis=1)
    ddf_ = ddf_.transpose()
    # ddf_ = ddf_.sort_values(by='Redditività di tutto il capitale investito (ROI) (%)\n%\n2020', ascending=False)
    ddf_.reset_index(inplace=True)
    ddf_.drop("index", axis=1, inplace=True)

    dftables_ = ddf_.groupby(
        ["Ragione sociale", "ATECO 2007\ndescrizione"], as_index=False).agg(
        {'Redditività di tutto il capitale investito (ROI) (%)\n%\n2020': 'mean',
         'Indice di indebitam. a breve\n%\n2020': 'mean',
         'Indice di indebitam. a lungo\n%\n2020': 'mean',
         'EBITDA/Vendite (%)\n%\n2020': 'mean',
         'Posizione finanziaria netta\nEUR\n2020': 'mean',
         'Indirizzo sede legale - Latitudine': 'mean',
         'Indirizzo sede legale - Longitudine': 'mean',
         "Ricavi delle vendite\nEUR\n2020": 'mean',
         "Ricavi delle vendite\nEUR\n2019": 'mean',
         "Ricavi delle vendite\nEUR\n2018": 'mean',
         "Ricavi delle vendite\nEUR\n2017": 'mean',
         "Ricavi delle vendite\nEUR\n2016": 'mean',
         }
    )
    dftables_["Redditività di tutto il capitale investito (ROI) (%)\n%\n2020"] = dftables_[
        "Redditività di tutto il capitale investito (ROI) (%)\n%\n2020"].round(2)
    dftables_["Indice di indebitam. a breve\n%\n2020"] = dftables_["Indice di indebitam. a breve\n%\n2020"].round(2)
    dftables_["Indice di indebitam. a lungo\n%\n2020"] = dftables_["Indice di indebitam. a lungo\n%\n2020"].round(2)
    dftables_["EBITDA/Vendite (%)\n%\n2020"] = dftables_["EBITDA/Vendite (%)\n%\n2020"].round(2)
    dftables_["Posizione finanziaria netta\nEUR\n2020"] = dftables_["Posizione finanziaria netta\nEUR\n2020"].round(2)
    dftables_["Ricavi delle vendite\nEUR\n2020"] = dftables_["Ricavi delle vendite\nEUR\n2020"].round(2)
    dftables_["Ricavi delle vendite\nEUR\n2019"] = dftables_["Ricavi delle vendite\nEUR\n2019"].round(2)
    dftables_["Ricavi delle vendite\nEUR\n2018"] = dftables_["Ricavi delle vendite\nEUR\n2018"].round(2)
    dftables_["Ricavi delle vendite\nEUR\n2017"] = dftables_["Ricavi delle vendite\nEUR\n2017"].round(2)
    dftables_["Ricavi delle vendite\nEUR\n2016"] = dftables_["Ricavi delle vendite\nEUR\n2016"].round(2)

    dftables_.columns = ['Ragione sociale', 'Descrizione',
                         'ROI (%)', 'Indebitamento a breve', 'Indebitamento a lungo', 'Margine di EBITDA',
                         'Posizione finanziaria netta', 'Latitudine', 'Longitudine', "Ricavi 2020",
                         "Ricavi 2019", "Ricavi 2018", "Ricavi 2017", "Ricavi 2016", ]

    datas = []
    for i in range(len(df)):
        if df.loc[i, "ATECO 2007\ndescrizione"] == data:
            datas.append(df.iloc[i, :])

    datas = pd.concat(datas, axis=1)
    datas = datas.transpose()
    datas.reset_index(inplace=True)
    datas.drop("index", axis=1, inplace=True)

    # incremento EBITDA(2020-2016)
    incremento_EBITDA = datas.apply(
        lambda x: (x['EBITDA\nEUR\n2020'] - x['EBITDA\nEUR\n2016']) * (100 / (x['EBITDA\nEUR\n2016'] + 1)),
        axis=1)

    dftables_["Incremento EBITDA"] = incremento_EBITDA
    dftables_["Incremento EBITDA"] = dftables_["Incremento EBITDA"].round(2)

    # Crescita fatturato(2020-2016)
    crescita_fatturato = datas.apply(
        lambda x: (x['Ricavi delle vendite\nEUR\n2020'] - x['Ricavi delle vendite\nEUR\n2016']) * 100 / (
                x['Ricavi delle vendite\nEUR\n2016'] + 1),
        axis=1)

    dftables_["Crescita fatturato (%)"] = crescita_fatturato
    dftables_["Crescita fatturato (%)"] = dftables_["Crescita fatturato (%)"].round(2)

    # quick ratio (denaro/DEBITI A BREVE\nEUR\n2020)
    quick_ratio = datas.apply(
        lambda x: (x['Denaro in cassa\nEUR\n2020'] / (x['DEBITI A BREVE\nEUR\n2020'] + 1)),
        axis=1)
    dftables_["Quick ratio"] = quick_ratio
    dftables_["Quick ratio"] = dftables_["Quick ratio"].round(2)

    # remove outlier
    cols = ['ROI (%)', 'Margine di EBITDA', 'Posizione finanziaria netta', "Incremento EBITDA", "Quick ratio",
            "Crescita fatturato (%)", "Ricavi 2020", "Ricavi 2019", "Ricavi 2018", "Ricavi 2017", "Ricavi 2016"]
    Q1 = dftables_[cols].quantile(0.25)
    Q3 = dftables_[cols].quantile(0.75)
    IQR = Q3 - Q1

    fer = dftables_[
        ~((dftables_[cols] < (Q1 - 1.5 * IQR)) | (dftables_[cols] > (Q3 + 1.5 * IQR))).any(axis=1)]

    dftables_ = fer
    dftables_.reset_index(inplace=True)
    dftables_.drop("index", axis=1, inplace=True)
    dftables_ = dftables_.sort_values(by='Crescita fatturato (%)', ascending=False)
    return dftables_


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

layout = html.Div([

    html.Div(id="store-dropdown-value", children=[str(dati_iniziali)]),
    dcc.Interval(
        id='interval-component',
        interval=1 * 6000000000,  # in milliseconds
        n_intervals=0
    ),

    html.H3(f"Settore: {dati_iniziali}", id="h3", style={'text-align': 'center', 'color': '#606060'},
            className="sottotitolo"),

    html.Div([

        dash_table.DataTable(
            id="table-container",
            columns=[
                {'name': i, 'id': i, 'deletable': False} for i in populate_table.columns
                # omit the id column
                if i != 'id'
            ],
            # columns=[],
            # data=dffmap.to_dict('records'),
            data=dftables_.to_dict('records'),
            editable=False,
            selected_rows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],  # SELEZIONO LE PRIME 10 RIGHE PER INIZIARE
            # selected_rows=[],
            filter_action="native",
            # sort_action="native",
            # sort_mode='single',
            row_selectable='multi',
            column_selectable="single",
            # derived_virtual_selected_rows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            row_deletable=False,
            page_action='native',
            page_current=0,
            page_size=10,
            fill_width=False,
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
                'border': '1px solid #8EA9C1'
            },
            style_data_conditional=[
                {
                    'backgroundColor': '#F2F2F2',
                    'color': 'black',
                    'fontWeight': 'bold',
                    'fontSize': 14
                }],
            # style_data_conditional=[],
            style_cell={'fontSize': 13,
                        'font-family': 'sans-serif',
                        'fontWeight': 'bold',
                        'text_align': 'left',
                        'color': 'black',
                        'padding': '3px',
                        # 'minWidth': 25,
                        # 'width': 35,
                        # 'maxWidth': 135
                        },
            style_table={
                'display': 'inline-block',
                'float': 'center',
                'display': 'flex',
                'border': '1px solid #8EA9C1'},
            style_as_list_view=True,
            style_header={
                'backgroundColor': '#ebeef0',
                'fontWeight': 'bold',
                'align': 'left',
                'border-bottom': '2px solid #8EA9C1'},
        ),
        html.H3(f'➤  Dalla tabella selezionare le aziende che si desidera analizzare ',
                style={'text-align': 'left', 'color': 'black'},
                className="sottotitolo3"),

        html.H3([f'➤  Selezionare ', html.Span('"ANALISI SETTORI"', className="colorSpan"),
                 ' nell Header per tornare alla selezione del settore'],
                style={'text-align': 'left', 'color': 'black'},
                className="sottotitolo4"),
    ], className="tabella22"),

    html.Div([
        dcc.Dropdown(id="roidropdown",  # DROP DOWN CON 3 SCELTE
                     options=[
                         {"label": "ROI (%)", "value": "ROI (%)"},
                         {"label": "ROE (%)", "value": "ROE (%)"},
                         {"label": "Margine di EBITDA (%)", "value": "Margine EBITDA"},
                         {"label": "Quick ratio (%)", "value": "Quick ratio"},
                         {"label": "Posizione finanziaria netta (€)", "value": "Posizione finanziaria netta"},
                         {"label": "Crescita fatturato (%)", "value": "Crescita fatturato (%)"},
                     ],
                     multi=False,
                     value="Crescita fatturato (%)",
                     # style={'width': "98%"},
                     searchable=False,
                     clearable=False,
                     className="dropdownbar"
                     ),

        dcc.Graph(id='roibarchart', className="bar1"),  # BAR CHART SCELTA
    ], className="roibar"),

    html.Div([

        dcc.Graph(id="scattermap", className="scattermap"),  # MAPPA ITALIA

    ], className="divscattermap"),  # FINE SCATTER MAP

    # FINE PRIMI 2 GRAFICI

    # GRAFICO XY
    html.Div([
        dcc.RadioItems(
            id="checklistaziende",
            options=[{"label": "Ricavi migliori 20-19", "value": "ricavi migliori 20-19"},
                     {"label": "Ricavi migliori 19-18", "value": "ricavi migliori 19-18"},
                     {"label": "Ricavi migliori 18-17", "value": "ricavi migliori 18-17"},
                     {"label": "Ricavi migliori 17-16", "value": "ricavi migliori 17-16"},
                     ],
            # labelStyle={'display': 'inline-block'},
            className="check_list2",
            labelStyle={
                'display': 'inline-block',
                'margin-right': '7px',
                'font-weight': 300
            },
            style={
                'display': 'inline-block',
                'margin-left': '7px'
            },

        ),
        dcc.Graph(id="line-chart-aziende", className="graficoxy2"),  # GRAFICO XY
    ], className="xygraph"),

    # ULTIMo  GRAFICo xy

    html.Div(id='outputcontainer', children=[], className="spazio"),
    html.Div(id='provaaa', children=[]),
    html.P("-            ", className="spazio1")
], className="table")


# FINE LAYOUT
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# CARICA SCELTA
@callback(Output("store-dropdown-value", "children"),
          Input('interval-component', 'n_intervals')
          )
def update_metrics(n):
    # print(n)
    sceltautente = pd.read_csv(r'pages\files\selectedrow.txt', header=None)
    print(sceltautente.iloc[0, 0])
    return sceltautente.iloc[0, 0]


# ----------------------------------------------------------------------------------------------------------------------
#   TABELLA INIZIO PAGINA
@callback([Output("table-container", "data"),
           Output("table-container", "selected_rows"), Output("h3", "children"),
           # Output("table-container", "style_data_conditional")
           ],
          Input("store-dropdown-value", "children")
          )
def populate_checklist(data):  # data è solo stringa di codice ATECO descrizione

    # TABELLA INIZIO PAGINA
    dato = popola_df(data).sort_values(by='Crescita fatturato (%)', ascending=False)

    return dato.to_dict('records'), [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], f"Settore: {data}"


# ----------------------------------------------------------------------------------------------------------------------
# # COLORE SFONDO TABELLA
# @callback(Output("table-container", "style_data_conditional"),
#           [Input("store-dropdown-value", "children"), Input("table-container", "selected_rows")]
#           )
# def populate_checklist(data, selected_rows, ):
#     ddf_ = []
#     for i in range(len(df)):
#         if df.loc[i, "ATECO 2007\ndescrizione"] == data:
#             ddf_.append(df.iloc[i, :])
#
#     ddf_ = pd.concat(ddf_, axis=1)
#     ddf_ = ddf_.transpose()
#     # ddf_ = ddf_.sort_values(by='Redditività di tutto il capitale investito (ROI) (%)\n%\n2020', ascending=False)
#     ddf_.reset_index(inplace=True)
#     ddf_.drop("index", axis=1, inplace=True)
#
#     dftables_ = ddf_.groupby(
#         ["Ragione sociale", "ATECO 2007\ndescrizione"], as_index=False).agg(
#         {'Redditività di tutto il capitale investito (ROI) (%)\n%\n2020': 'mean',
#          'Indice di indebitam. a breve\n%\n2020': 'mean',
#          'Indice di indebitam. a lungo\n%\n2020': 'mean',
#          'EBITDA/Vendite (%)\n%\n2020': 'mean',
#          'Posizione finanziaria netta\nEUR\n2020': 'mean',
#          'Indirizzo sede legale - Latitudine': 'mean',
#          'Indirizzo sede legale - Longitudine': 'mean',
#          "Ricavi delle vendite\nEUR\n2020": 'mean',
#          "Ricavi delle vendite\nEUR\n2019": 'mean',
#          "Ricavi delle vendite\nEUR\n2018": 'mean',
#          "Ricavi delle vendite\nEUR\n2017": 'mean',
#          "Ricavi delle vendite\nEUR\n2016": 'mean',
#          }
#     )
#     dftables_["Redditività di tutto il capitale investito (ROI) (%)\n%\n2020"] = dftables_[
#         "Redditività di tutto il capitale investito (ROI) (%)\n%\n2020"].round(2)
#     dftables_["Indice di indebitam. a breve\n%\n2020"] = dftables_["Indice di indebitam. a breve\n%\n2020"].round(2)
#     dftables_["Indice di indebitam. a lungo\n%\n2020"] = dftables_["Indice di indebitam. a lungo\n%\n2020"].round(2)
#     dftables_["EBITDA/Vendite (%)\n%\n2020"] = dftables_["EBITDA/Vendite (%)\n%\n2020"].round(2)
#     dftables_["Posizione finanziaria netta\nEUR\n2020"] = dftables_["Posizione finanziaria netta\nEUR\n2020"].round(2)
#     dftables_["Ricavi delle vendite\nEUR\n2020"] = dftables_["Ricavi delle vendite\nEUR\n2020"].round(2)
#     dftables_["Ricavi delle vendite\nEUR\n2019"] = dftables_["Ricavi delle vendite\nEUR\n2019"].round(2)
#     dftables_["Ricavi delle vendite\nEUR\n2018"] = dftables_["Ricavi delle vendite\nEUR\n2018"].round(2)
#     dftables_["Ricavi delle vendite\nEUR\n2017"] = dftables_["Ricavi delle vendite\nEUR\n2017"].round(2)
#     dftables_["Ricavi delle vendite\nEUR\n2016"] = dftables_["Ricavi delle vendite\nEUR\n2016"].round(2)
#
#     dftables_.columns = ['Ragione sociale', 'Descrizione',
#                          'ROI (%)', 'Indebitamento a breve', 'Indebitamento a lungo', 'Margine di EBITDA',
#                          'Posizione finanziaria netta', 'Latitudine', 'Longitudine', "Ricavi 2020",
#                          "Ricavi 2019", "Ricavi 2018", "Ricavi 2017", "Ricavi 2016", ]
#
#     datas = []
#     for i in range(len(df)):
#         if df.loc[i, "ATECO 2007\ndescrizione"] == data:
#             datas.append(df.iloc[i, :])
#
#     datas = pd.concat(datas, axis=1)
#     datas = datas.transpose()
#     datas.reset_index(inplace=True)
#     datas.drop("index", axis=1, inplace=True)
#
#     # incremento EBITDA(2020-2016)
#     incremento_EBITDA = datas.apply(
#         lambda x: (x['EBITDA\nEUR\n2020'] - x['EBITDA\nEUR\n2016']) * (100 / (x['EBITDA\nEUR\n2016'] + 1)),
#         axis=1)
#
#     dftables_["Incremento EBITDA"] = incremento_EBITDA
#     dftables_["Incremento EBITDA"] = dftables_["Incremento EBITDA"].round(2)
#
#     # Crescita fatturato(2020-2016)
#     crescita_fatturato = datas.apply(
#         lambda x: (x['Ricavi delle vendite\nEUR\n2020'] - x['Ricavi delle vendite\nEUR\n2016']) * 100 / (
#                 x['Ricavi delle vendite\nEUR\n2016'] + 1),
#         axis=1)
#
#     dftables_["Crescita fatturato (%)"] = crescita_fatturato
#     dftables_["Crescita fatturato (%)"] = dftables_["Crescita fatturato (%)"].round(2)
#
#     # quick ratio (denaro/DEBITI A BREVE\nEUR\n2020)
#     quick_ratio = datas.apply(
#         lambda x: (x['Denaro in cassa\nEUR\n2020'] / (x['DEBITI A BREVE\nEUR\n2020'] + 1)),
#         axis=1)
#     dftables_["Quick ratio"] = quick_ratio
#     dftables_["Quick ratio"] = dftables_["Quick ratio"].round(2)
#
#     # remove outlier
#     cols = ['ROI (%)', 'Margine di EBITDA', 'Posizione finanziaria netta', "Incremento EBITDA", "Quick ratio",
#             "Crescita fatturato (%)", "Ricavi 2020", "Ricavi 2019", "Ricavi 2018", "Ricavi 2017", "Ricavi 2016"]
#     Q1 = dftables_[cols].quantile(0.25)
#     Q3 = dftables_[cols].quantile(0.75)
#     IQR = Q3 - Q1
#
#     fer = dftables_[
#         ~((dftables_[cols] < (Q1 - 1.5 * IQR)) | (dftables_[cols] > (Q3 + 1.5 * IQR))).any(axis=1)]
#
#     dftables_ = fer
#     dftables_.reset_index(inplace=True)
#     dftables_.drop("index", axis=1, inplace=True)
#     dftables_ = dftables_.sort_values(by='Crescita fatturato (%)', ascending=False)
#
#     # ---------------------------------------------------------------------------------------------------------
#
#     COLOR = ['#800000', '#9A6324', '#808000', '#469990', '#000075',
#              '#000000', '#e6194B', '#f58231', '#ffe119', '#bfef45',
#              '#3cb44b', '#42d4f4', '#4363d8', '#911eb4', '#f032e6',
#              '#a9a9a9', '#fabed4', '#ffd8b1', '#de3163', '#0B6623']
#     # print(len(COLOR))
#
#     # style_data_conditional = []
#     # # style_data_conditional=[{'if': {'row_index': i, 'column_id': 'COLOR'}, 'background-color': df['COLOR'][i], 'color': df['COLOR'][i]} for i in range(df.shape[0])]
#     #
#     # for i in selected_rows:
#     #     for x in selected_rows:
#     #         if i == x:
#     #             style_data_conditional = np.append(style_data_conditional, [
#     #                 {
#     #                     'if': {
#     #                         'row_index': x,
#     #                         'column_id': 'Ragione sociale'
#     #                     },
#     #                     'backgroundColor': 'dodgerblue',
#     #                     'color': 'black',
#     #                     'fontWeight': 'bold',
#     #                     'fontSize': 14,
#     #                 }])
#     # style_data_conditional = [
#     #     {'if': {'row_index': i, 'column_id': 'Ragione sociale'}, 'background-color': COLOR[i],
#     #      'color': 'black'}
#     #     for i in selected_rows]
#     # else:
#     #     style_data_conditional = np.append(style_data_conditional, [
#     #         {
#     #             'if': {
#     #                 'row_index': index,
#     #                 'column_id': 'Ragione sociale'
#     #             },
#     #             'backgroundColor': 'red',
#     #             'color': 'black',
#     #             'fontWeight': 'bold',
#     #             'fontSize': 14,
#     #         }])
#
#     # for x in selected_rows:
#     #     style_data_conditional = np.append(style_data_conditional, [
#     #         {
#     #             'if': {
#     #                 # 'column_id': 'Ragione sociale',
#     #                 # 'filter_query': f'{dftables_.loc[x,"Ragione sociale"]} == {x}',
#     #                 'row_index': x,  # number | 'odd' | 'even'
#     #                 'column_id': 'Ragione sociale'
#     #             },
#     #             'backgroundColor': 'dodgerblue',
#     #             'color': 'black',
#     #             'fontWeight': 'bold',
#     #             'fontSize': 14,
#     #             'else': {
#     #                 'backgroundColor': 'red',
#     #             },
#     #         }])
#     #         #     {
#     #         #     'else': {
#     #         #               # 'column_id': 'Ragione sociale',
#     #         #               # 'filter_query': f'{dftables_.loc[x,"Ragione sociale"]} == {x}',
#     #         #               'row_index': x,  # number | 'odd' | 'even'
#     #         #               'column_id': 'Ragione sociale'
#     #         #           },
#     #         #           'backgroundColor': 'red',
#     #         # 'color': 'black',
#     #         # 'fontWeight': 'bold',
#     #         # 'fontSize': 14
#     #         # },
#     #     ])
#
#     # style_data_conditional = [{
#     #     'backgroundColor': '#F2F2F2',
#     #     'color': 'black',
#     #     'fontWeight': 'bold',
#     #     'fontSize': 14
#     # }]
#     style_data_conditional = [
#         {
#             'backgroundColor': '#F2F2F2',
#             'color': 'black',
#             'fontWeight': 'bold',
#             'fontSize': 14
#         }]
#     return style_data_conditional


# ----------------------------------------------------------------------------------------------------------------------
# BAR CHART PER RIGHE SCELTE DI TABELLA

@callback(Output("roibarchart", "children"),
          [Input("roidropdown", "value"), Input('table-container', 'selected_rows')]
          )
def clear_graph(scelta, selected_rows):  # SCELTA SE BEST/WORSE, DATA=SCELTA DI SETTORE
    return None


@callback([Output("outputcontainer", "children"), Output("roibarchart", "figure")],
          [Input("roidropdown", "value"), Input("store-dropdown-value", "children"),
           Input('table-container', 'selected_rows')]
          )
def update_graph(scelta, data, selected_rows):  # SCELTA SE BEST/WORSE, DATA=SCELTA DI SETTORE

    container = ""
    dftables_ = popola_df(data)

    # --------------------------------------------------------------------------------------------------------------
    # SCELTA 1
    if scelta == "ROI (%)":

        df_ = dftables_.sort_values(by='Crescita fatturato (%)', ascending=False)
        # df_ = df_.iloc[0:10]
        df_.reset_index(inplace=True)
        df_.drop("index", axis=1, inplace=True)

        df_selected = []
        for x in selected_rows:
            df_selected.append(df_.iloc[x, :])
        df_selected = pd.concat(df_selected, axis=1)
        df_selected = df_selected.transpose()

        df_selected = df_selected.sort_values(by='ROI (%)', ascending=False)
        df_selected = df_selected.loc[selected_rows]
        # print(df_selected)
        df_selected.reset_index(inplace=True)
        df_selected.drop("index", axis=1, inplace=True)
        df_selected = df_selected.sort_values(by='ROI (%)', ascending=False)

        # print(df_selected)

        fig = go.Figure()
        fig.data = []
        fig.layout = {}
        fig.add_trace(go.Bar(x=df_selected['Ragione sociale'],
                             y=df_selected["ROI (%)"],
                             name='',
                             text=df_selected["ROI (%)"],
                             legendgroup="group",
                             legendgrouptitle_text="ROI (%)",

                             marker=dict(
                                 color=['#800000', '#9A6324', '#808000', '#469990', '#000075',
                                        '#000000', '#e6194B', '#f58231', '#ffe119', '#bfef45',
                                        '#3cb44b', '#42d4f4', '#4363d8', '#911eb4', '#f032e6',
                                        '#a9a9a9', '#fabed4', '#ffd8b1', '#de3163', '#0B6623',
                                        ],
                             ),
                             hovertemplate='<br><b>Ragione sociale:</b> %{x}</br>' +
                                           '<b>ROI (%):</b>  %{y}%<br>',
                             ))

        fig.update_xaxes(visible=False, showticklabels=True)
        fig.update_yaxes(visible=True, showticklabels=True)

        fig.update_layout(
            legend=dict(
                x=1.025,
                y=1.2,
                font=dict(
                    size=12,
                    color="black"
                ),
                bgcolor="#ebeef0",
                bordercolor="#8EA9C1",
                borderwidth=1

            ),
            barmode='group',
            title={'text': 'ROI per aziende',
                   'font': {'size': 18}, 'x': 0.5, 'xanchor': 'center'},
        )
        return container, fig
    # -----------------------------------------------------------------------------------------------------------------
    # SCELTA 2
    elif scelta == "Margine EBITDA":

        df_ = dftables_.sort_values(by='Crescita fatturato (%)', ascending=False)
        # df_ = df_.iloc[0:10]
        df_.reset_index(inplace=True)
        df_.drop("index", axis=1, inplace=True)

        df_selected = []
        for x in selected_rows:
            df_selected.append(df_.iloc[x, :])
        df_selected = pd.concat(df_selected, axis=1)
        df_selected = df_selected.transpose()

        df_selected = df_selected.sort_values(by='Margine di EBITDA', ascending=False)
        df_selected = df_selected.loc[selected_rows]
        # print(df_selected)
        df_selected.reset_index(inplace=True)
        df_selected.drop("index", axis=1, inplace=True)
        df_selected = df_selected.sort_values(by='Margine di EBITDA', ascending=False)

        # print(df_selected)

        fig = go.Figure()
        fig.data = []
        fig.layout = {}
        fig.add_trace(go.Bar(x=df_selected['Ragione sociale'],
                             y=df_selected["Margine di EBITDA"],
                             name='',
                             text=df_selected["Margine di EBITDA"],
                             legendgroup="group",
                             legendgrouptitle_text="Margine di EBITDA",

                             marker=dict(
                                 # color=df_selected["ROI 2020"],
                                 # colorscale=px.colors.sequential.ice,
                                 # showscale=True,
                                 # color_discrete_sequence=px.colors.sequential.ice
                                 color=['#800000', '#9A6324', '#808000', '#469990', '#000075',
                                        '#000000', '#e6194B', '#f58231', '#ffe119', '#bfef45',
                                        '#3cb44b', '#42d4f4', '#4363d8', '#911eb4', '#f032e6',
                                        '#a9a9a9', '#fabed4', '#ffd8b1', '#de3163', '#0B6623',
                                        ],
                             ),
                             hovertemplate='<br><b>Ragione sociale:</b> %{x}</br>' +
                                           '<b>Margine di EBITDA:</b>  %{y}%<br>',
                             ))

        fig.update_xaxes(visible=False, showticklabels=True)
        fig.update_yaxes(visible=True, showticklabels=True)

        fig.update_layout(
            legend=dict(
                x=1.025,
                y=1.2,
                font=dict(
                    size=12,
                    color="black"
                ),
                bgcolor="#ebeef0",
                bordercolor="#8EA9C1",
                borderwidth=1

            ),
            barmode='group',
            title={'text': 'Margine di EBITDA per aziende',
                   'font': {'size': 18}, 'x': 0.5, 'xanchor': 'center'},
        )
        return container, fig

    # -----------------------------------------------------------------------------------------------------------------
    # SCELTA 3
    elif scelta == "Posizione finanziaria netta":

        df_ = dftables_.sort_values(by='Crescita fatturato (%)', ascending=False)
        # df_ = df_.iloc[0:10]
        df_.reset_index(inplace=True)
        df_.drop("index", axis=1, inplace=True)

        df_selected = []
        for x in selected_rows:
            df_selected.append(df_.iloc[x, :])
        df_selected = pd.concat(df_selected, axis=1)
        df_selected = df_selected.transpose()

        df_selected = df_selected.sort_values(by='Posizione finanziaria netta', ascending=False)
        df_selected = df_selected.loc[selected_rows]
        # print(df_selected)
        df_selected.reset_index(inplace=True)
        df_selected.drop("index", axis=1, inplace=True)
        df_selected = df_selected.sort_values(by='Posizione finanziaria netta', ascending=False)

        # print(df_selected)

        fig = go.Figure()
        fig.data = []
        fig.layout = {}
        fig.add_trace(go.Bar(x=df_selected['Ragione sociale'],
                             y=df_selected["Posizione finanziaria netta"],
                             name='',
                             text=df_selected["Posizione finanziaria netta"],
                             legendgroup="group",
                             legendgrouptitle_text="Posizione finanziaria netta",

                             marker=dict(
                                 color=['#800000', '#9A6324', '#808000', '#469990', '#000075',
                                        '#000000', '#e6194B', '#f58231', '#ffe119', '#bfef45',
                                        '#3cb44b', '#42d4f4', '#4363d8', '#911eb4', '#f032e6',
                                        '#a9a9a9', '#fabed4', '#ffd8b1', '#de3163', '#0B6623',
                                        ],
                             ),
                             hovertemplate='<br><b>Ragione sociale:</b> %{x}</br>' +
                                           '<b>Posizione finanziaria netta:</b>  %{y}€<br>',
                             ))

        fig.update_xaxes(visible=False, showticklabels=True)
        fig.update_yaxes(visible=True, showticklabels=True)

        fig.update_layout(
            legend=dict(
                x=1.025,
                y=1.2,
                font=dict(
                    size=12,
                    color="black"
                ),
                bgcolor="#ebeef0",
                bordercolor="#8EA9C1",
                borderwidth=1

            ),
            barmode='group',
            title={'text': 'Posizione finanziaria netta per aziende',
                   'font': {'size': 18}, 'x': 0.5, 'xanchor': 'center'},
        )
        return container, fig

    # -----------------------------------------------------------------------------------------------------------------
    # SCELTA 4
    elif scelta == "Quick ratio":

        df_ = dftables_.sort_values(by='Crescita fatturato (%)', ascending=False)
        # df_ = df_.iloc[0:10]
        df_.reset_index(inplace=True)
        df_.drop("index", axis=1, inplace=True)

        df_selected = []
        for x in selected_rows:
            df_selected.append(df_.iloc[x, :])
        df_selected = pd.concat(df_selected, axis=1)
        df_selected = df_selected.transpose()

        df_selected = df_selected.sort_values(by='Quick ratio', ascending=False)
        df_selected = df_selected.loc[selected_rows]
        # print(df_selected)
        df_selected.reset_index(inplace=True)
        df_selected.drop("index", axis=1, inplace=True)
        df_selected = df_selected.sort_values(by='Quick ratio', ascending=False)

        # print(df_selected)

        fig = go.Figure()
        fig.data = []
        fig.layout = {}
        fig.add_trace(go.Bar(x=df_selected['Ragione sociale'],
                             y=df_selected["Quick ratio"],
                             name='',
                             text=df_selected["Quick ratio"],
                             legendgroup="group",
                             legendgrouptitle_text="Quick ratio",

                             marker=dict(
                                 color=['#800000', '#9A6324', '#808000', '#469990', '#000075',
                                        '#000000', '#e6194B', '#f58231', '#ffe119', '#bfef45',
                                        '#3cb44b', '#42d4f4', '#4363d8', '#911eb4', '#f032e6',
                                        '#a9a9a9', '#fabed4', '#ffd8b1', '#de3163', '#0B6623',
                                        ],
                             ),
                             hovertemplate='<br><b>Ragione sociale:</b> %{x}</br>' +
                                           '<b>Quick ratio:</b>  %{y}%<br>',
                             ))

        fig.update_xaxes(visible=False, showticklabels=True)
        fig.update_yaxes(visible=True, showticklabels=True)

        fig.update_layout(
            legend=dict(
                x=1.025,
                y=1.2,
                font=dict(
                    size=12,
                    color="black"
                ),
                bgcolor="#ebeef0",
                bordercolor="#8EA9C1",
                borderwidth=1

            ),
            barmode='group',
            title={'text': 'Quick ratio per aziende',
                   'font': {'size': 18}, 'x': 0.5, 'xanchor': 'center'},
        )
        return container, fig

        # -----------------------------------------------------------------------------------------------------------------
        # SCELTA 5
    elif scelta == "Crescita fatturato (%)":

        df_ = dftables_.sort_values(by='Crescita fatturato (%)', ascending=False)
        # df_ = df_.iloc[0:10]
        df_.reset_index(inplace=True)
        df_.drop("index", axis=1, inplace=True)

        df_selected = []
        for x in selected_rows:
            df_selected.append(df_.iloc[x, :])
        df_selected = pd.concat(df_selected, axis=1)
        df_selected = df_selected.transpose()

        df_selected = df_selected.sort_values(by='Crescita fatturato (%)', ascending=False)
        df_selected = df_selected.loc[selected_rows]
        # print(df_selected)
        df_selected.reset_index(inplace=True)
        df_selected.drop("index", axis=1, inplace=True)
        df_selected = df_selected.sort_values(by='Crescita fatturato (%)', ascending=False)

        # print(df_selected)

        fig = go.Figure()
        fig.data = []
        fig.layout = {}
        fig.add_trace(go.Bar(x=df_selected['Ragione sociale'],
                             y=df_selected["Crescita fatturato (%)"],
                             name='',
                             text=df_selected["Crescita fatturato (%)"],
                             legendgroup="group",
                             legendgrouptitle_text="Crescita fatturato (%)",

                             marker=dict(
                                 color=['#800000', '#9A6324', '#808000', '#469990', '#000075',
                                        '#000000', '#e6194B', '#f58231', '#ffe119', '#bfef45',
                                        '#3cb44b', '#42d4f4', '#4363d8', '#911eb4', '#f032e6',
                                        '#a9a9a9', '#fabed4', '#ffd8b1', '#de3163', '#0B6623',
                                        ],
                             ),
                             hovertemplate='<br><b>Ragione sociale:</b> %{x}</br>' +
                                           '<b>Crescita fatturato (%):</b>  %{y}%<br>',
                             ))

        fig.update_xaxes(visible=False, showticklabels=True)
        fig.update_yaxes(visible=True, showticklabels=True)

        fig.update_layout(
            legend=dict(
                x=1.025,
                y=1.2,
                font=dict(
                    size=12,
                    color="black"
                ),
                bgcolor="#ebeef0",
                bordercolor="#8EA9C1",
                borderwidth=1

            ),
            barmode='group',
            title={'text': 'Crescita fatturato per aziende',
                   'font': {'size': 18}, 'x': 0.5, 'xanchor': 'center'},
        )
        return container, fig

        # -----------------------------------------------------------------------------------------------------------------
        # SCELTA 6
    elif scelta == "ROE (%)":

        df_ = dftables_.sort_values(by='Crescita fatturato (%)', ascending=False)
        # df_ = df_.iloc[0:10]
        df_.reset_index(inplace=True)
        df_.drop("index", axis=1, inplace=True)

        df_selected = []
        for x in selected_rows:
            df_selected.append(df_.iloc[x, :])
        df_selected = pd.concat(df_selected, axis=1)
        df_selected = df_selected.transpose()

        df_selected = df_selected.sort_values(by='ROE (%)', ascending=False)
        df_selected = df_selected.loc[selected_rows]
        # print(df_selected)
        df_selected.reset_index(inplace=True)
        df_selected.drop("index", axis=1, inplace=True)
        df_selected = df_selected.sort_values(by='ROE (%)', ascending=False)

        # print(df_selected)

        fig = go.Figure()
        fig.data = []
        fig.layout = {}
        fig.add_trace(go.Bar(x=df_selected['Ragione sociale'],
                             y=df_selected["ROE (%)"],
                             name='',
                             text=df_selected["ROE (%)"],
                             legendgroup="group",
                             legendgrouptitle_text="ROE (%)",

                             marker=dict(
                                 color=['#800000', '#9A6324', '#808000', '#469990', '#000075',
                                        '#000000', '#e6194B', '#f58231', '#ffe119', '#bfef45',
                                        '#3cb44b', '#42d4f4', '#4363d8', '#911eb4', '#f032e6',
                                        '#a9a9a9', '#fabed4', '#ffd8b1', '#de3163', '#0B6623',
                                        ],
                             ),
                             hovertemplate='<br><b>Ragione sociale:</b> %{x}</br>' +
                                           '<b>ROE (%):</b>  %{y}%<br>',
                             ))

        fig.update_xaxes(visible=False, showticklabels=True)
        fig.update_yaxes(visible=True, showticklabels=True)

        fig.update_layout(
            legend=dict(
                x=1.025,
                y=1.2,
                font=dict(
                    size=12,
                    color="black"
                ),
                bgcolor="#ebeef0",
                bordercolor="#8EA9C1",
                borderwidth=1

            ),
            barmode='group',
            title={'text': 'ROE (%) per aziende',
                   'font': {'size': 18}, 'x': 0.5, 'xanchor': 'center'},
        )
        return container, fig


# ----------------------------------------------------------------------------------------------------------------------
# MAPPA ITALIA:
@callback(
    Output("scattermap", "figure"),
    [Input('table-container', 'selected_rows'), Input("store-dropdown-value", "children"),
     Input("roidropdown", "value")]
)
def populate_map(selected_rows, data, scelta):
    dftables_ = popola_df(data)

    df_ = dftables_.sort_values(by='Crescita fatturato (%)', ascending=False)
    # df_ = df_.iloc[0:10]
    df_.reset_index(inplace=True)
    df_.drop("index", axis=1, inplace=True)

    df_selected = []
    for x in selected_rows:
        df_selected.append(df_.iloc[x, :])
    df_selected = pd.concat(df_selected, axis=1)
    df_selected = df_selected.transpose()

    df_selected = df_selected.sort_values(by='Crescita fatturato (%)', ascending=False)
    df_selected = df_selected.loc[selected_rows]
    # print(df_selected)
    df_selected.reset_index(inplace=True)
    df_selected.drop("index", axis=1, inplace=True)

    # --------------------------------------------------------------------------------------------------------
    if scelta == "ROI (%)":
        df_selected = df_selected.sort_values(by='ROI (%)', ascending=False)

        # Create figure
        fig = go.Figure(go.Scattermapbox(
            lon=df_selected['Longitudine'],
            lat=df_selected['Latitudine'],
            mode='markers',
            marker={"color": ['#800000', '#9A6324', '#808000', '#469990', '#000075',
                              '#000000', '#e6194B', '#f58231', '#ffe119', '#bfef45',
                              '#3cb44b', '#42d4f4', '#4363d8', '#911eb4', '#f032e6',
                              '#a9a9a9', '#fabed4', '#ffd8b1', '#de3163', '#0B6623',
                              ],
                    # 'color': df_selected['ROI 2020'],
                    'size': 27,
                    'opacity': 0.8},
            unselected={'marker': {'opacity': 0.3, 'size': 27}},
            selected={'marker': {'opacity': 1, 'size': 39}},
            name="",
            hovertext=df_selected['Ragione sociale'],
            hovertemplate='<br><b>Ragione sociale:</b> %{hovertext}</br>',
        ))
        fig.update_layout(
            uirevision='foo',
            clickmode='event+select',
            height=1200,
            mapbox=dict(
                style='open-street-map',
                center=dict(
                    lat=43,
                    lon=12
                ),
                pitch=0,
                zoom=5.4
            ),

        )
        fig.update_yaxes(automargin=True)
        return fig

    # ----------------------------------------------------------------------------------------------------------------
    elif scelta == "Margine EBITDA":
        df_selected = df_selected.sort_values(by='Margine di EBITDA', ascending=False)

        # Create figure
        fig = go.Figure(go.Scattermapbox(
            lon=df_selected['Longitudine'],
            lat=df_selected['Latitudine'],
            mode='markers',
            marker={"color": ['#800000', '#9A6324', '#808000', '#469990', '#000075',
                              '#000000', '#e6194B', '#f58231', '#ffe119', '#bfef45',
                              '#3cb44b', '#42d4f4', '#4363d8', '#911eb4', '#f032e6',
                              '#a9a9a9', '#fabed4', '#ffd8b1', '#de3163', '#0B6623',
                              ],
                    # 'color': df_selected['ROI 2020'],
                    'size': 27,
                    'opacity': 0.8},
            unselected={'marker': {'opacity': 0.3, 'size': 27}},
            selected={'marker': {'opacity': 1, 'size': 39}},
            name="",
            hovertext=df_selected['Ragione sociale'],
            hovertemplate='<br><b>Ragione sociale:</b> %{hovertext}</br>',
        ))
        fig.update_layout(
            uirevision='foo',
            clickmode='event+select',
            height=1200,
            mapbox=dict(
                style='open-street-map',
                center=dict(
                    lat=43,
                    lon=12
                ),
                pitch=0,
                zoom=5.4
            ),

        )
        fig.update_yaxes(automargin=True)
        return fig
    # ----------------------------------------------------------------------------------------------------------------
    elif scelta == "Quick ratio":
        df_quickratio = []
        df_quickratio = df_selected.sort_values(by='Quick ratio', ascending=False)

        # Create figure
        fig = go.Figure(go.Scattermapbox(
            lon=df_quickratio['Longitudine'],
            lat=df_quickratio['Latitudine'],
            mode='markers',
            marker={"color": ['#800000', '#9A6324', '#808000', '#469990', '#000075',
                              '#000000', '#e6194B', '#f58231', '#ffe119', '#bfef45',
                              '#3cb44b', '#42d4f4', '#4363d8', '#911eb4', '#f032e6',
                              '#a9a9a9', '#fabed4', '#ffd8b1', '#de3163', '#0B6623',
                              ],
                    # 'color': df_selected['ROI 2020'],
                    'size': 27,
                    'opacity': 0.8},
            unselected={'marker': {'opacity': 0.3, 'size': 27}},
            selected={'marker': {'opacity': 1, 'size': 39}},
            name="",
            hovertext=df_quickratio['Ragione sociale'],
            hovertemplate='<br><b>Ragione sociale:</b> %{hovertext}</br>',
        ))
        fig.update_layout(
            uirevision='foo',
            clickmode='event+select',
            height=1200,
            mapbox=dict(
                style='open-street-map',
                center=dict(
                    lat=43,
                    lon=12
                ),
                pitch=0,
                zoom=5.4
            ),

        )
        fig.update_yaxes(automargin=True)
        return fig

    # ----------------------------------------------------------------------------------------------------------------
    elif scelta == "Posizione finanziaria netta":
        df_selected = df_selected.sort_values(by='Posizione finanziaria netta', ascending=False)

        # Create figure
        fig = go.Figure(go.Scattermapbox(
            lon=df_selected['Longitudine'],
            lat=df_selected['Latitudine'],
            mode='markers',
            marker={"color": ['#800000', '#9A6324', '#808000', '#469990', '#000075',
                              '#000000', '#e6194B', '#f58231', '#ffe119', '#bfef45',
                              '#3cb44b', '#42d4f4', '#4363d8', '#911eb4', '#f032e6',
                              '#a9a9a9', '#fabed4', '#ffd8b1', '#de3163', '#0B6623',
                              ],
                    # 'color': df_selected['ROI 2020'],
                    'size': 27,
                    'opacity': 0.8},
            unselected={'marker': {'opacity': 0.3, 'size': 27}},
            selected={'marker': {'opacity': 1, 'size': 39}},
            name="",
            hovertext=df_selected['Ragione sociale'],
            hovertemplate='<br><b>Ragione sociale:</b> %{hovertext}</br>',
        ))
        fig.update_layout(
            uirevision='foo',
            clickmode='event+select',
            height=1200,
            mapbox=dict(
                style='open-street-map',
                center=dict(
                    lat=43,
                    lon=12
                ),
                pitch=0,
                zoom=5.4
            ),

        )
        fig.update_yaxes(automargin=True)
        return fig

        # ----------------------------------------------------------------------------------------------------------------
    elif scelta == "Crescita fatturato (%)":
        df_quickratio = []
        df_quickratio = df_selected.sort_values(by='Crescita fatturato (%)', ascending=False)

        # Create figure
        fig = go.Figure(go.Scattermapbox(
            lon=df_quickratio['Longitudine'],
            lat=df_quickratio['Latitudine'],
            mode='markers',
            marker={"color": ['#800000', '#9A6324', '#808000', '#469990', '#000075',
                              '#000000', '#e6194B', '#f58231', '#ffe119', '#bfef45',
                              '#3cb44b', '#42d4f4', '#4363d8', '#911eb4', '#f032e6',
                              '#a9a9a9', '#fabed4', '#ffd8b1', '#de3163', '#0B6623',
                              ],
                    # 'color': df_selected['ROI 2020'],
                    'size': 27,
                    'opacity': 0.8},
            unselected={'marker': {'opacity': 0.3, 'size': 27}},
            selected={'marker': {'opacity': 1, 'size': 39}},
            name="",
            hovertext=df_quickratio['Ragione sociale'],
            hovertemplate='<br><b>Ragione sociale:</b> %{hovertext}</br>',
        ))
        fig.update_layout(
            uirevision='foo',
            clickmode='event+select',
            height=1200,
            mapbox=dict(
                style='open-street-map',
                center=dict(
                    lat=43,
                    lon=12
                ),
                pitch=0,
                zoom=5.4
            ),

        )
        fig.update_yaxes(automargin=True)
        return fig

        # ----------------------------------------------------------------------------------------------------------------
    elif scelta == "ROE (%)":
        df_selected = df_selected.sort_values(by='ROE (%)', ascending=False)

        # Create figure
        fig = go.Figure(go.Scattermapbox(
            lon=df_selected['Longitudine'],
            lat=df_selected['Latitudine'],
            mode='markers',
            marker={"color": ['#800000', '#9A6324', '#808000', '#469990', '#000075',
                              '#000000', '#e6194B', '#f58231', '#ffe119', '#bfef45',
                              '#3cb44b', '#42d4f4', '#4363d8', '#911eb4', '#f032e6',
                              '#a9a9a9', '#fabed4', '#ffd8b1', '#de3163', '#0B6623',
                              ],
                    # 'color': df_selected['ROI 2020'],
                    'size': 27,
                    'opacity': 0.8},
            unselected={'marker': {'opacity': 0.3, 'size': 27}},
            selected={'marker': {'opacity': 1, 'size': 39}},
            name="",
            hovertext=df_selected['Ragione sociale'],
            hovertemplate='<br><b>Ragione sociale:</b> %{hovertext}</br>',
        ))
        fig.update_layout(
            uirevision='foo',
            clickmode='event+select',
            height=1200,
            mapbox=dict(
                style='open-street-map',
                center=dict(
                    lat=43,
                    lon=12
                ),
                pitch=0,
                zoom=5.4
            ),

        )
        fig.update_yaxes(automargin=True)
        return fig


# ----------------------------------------------------------------------------------------------------------------------
# CHECK LIST PER AZIENDE CON RICAVI MIGLIORI
@callback(
    Output("line-chart-aziende", "figure"),
    [Input("checklistaziende", "value"), Input('table-container', 'selected_rows'),
     Input("store-dropdown-value", "children")]
    # scelta anno, righe selezionate tabella, data
)
def update_line_chart(scelta, selected_rows, data):
    ddf_ = []
    for i in range(len(df)):
        if df.loc[i, "ATECO 2007\ndescrizione"] == data:
            ddf_.append(df.iloc[i, :])

    ddf_ = pd.concat(ddf_, axis=1)
    ddf_ = ddf_.transpose()
    ddf_.reset_index(inplace=True)
    ddf_.drop("index", axis=1, inplace=True)

    dftables_ = ddf_.groupby(
        ["Ragione sociale", "ATECO 2007\ndescrizione"], as_index=False).agg(
        {'Redditività di tutto il capitale investito (ROI) (%)\n%\n2020': 'mean',
         'Indice di indebitam. a breve\n%\n2020': 'mean',
         'Indice di indebitam. a lungo\n%\n2020': 'mean',
         'EBITDA/Vendite (%)\n%\n2020': 'mean',
         'Posizione finanziaria netta\nEUR\n2020': 'mean',
         'Indirizzo sede legale - Latitudine': 'mean',
         'Indirizzo sede legale - Longitudine': 'mean',
         "Ricavi delle vendite\nEUR\n2020": 'mean',
         "Ricavi delle vendite\nEUR\n2019": 'mean',
         "Ricavi delle vendite\nEUR\n2018": 'mean',
         "Ricavi delle vendite\nEUR\n2017": 'mean',
         "Ricavi delle vendite\nEUR\n2016": 'mean',
         }
    )
    dftables_["Redditività di tutto il capitale investito (ROI) (%)\n%\n2020"] = dftables_[
        "Redditività di tutto il capitale investito (ROI) (%)\n%\n2020"].round(2)
    dftables_["Indice di indebitam. a breve\n%\n2020"] = dftables_["Indice di indebitam. a breve\n%\n2020"].round(2)
    dftables_["Indice di indebitam. a lungo\n%\n2020"] = dftables_["Indice di indebitam. a lungo\n%\n2020"].round(2)
    dftables_["EBITDA/Vendite (%)\n%\n2020"] = dftables_["EBITDA/Vendite (%)\n%\n2020"].round(2)
    dftables_["Posizione finanziaria netta\nEUR\n2020"] = dftables_["Posizione finanziaria netta\nEUR\n2020"].round(2)
    dftables_["Ricavi delle vendite\nEUR\n2020"] = dftables_["Ricavi delle vendite\nEUR\n2020"].round(2)
    dftables_["Ricavi delle vendite\nEUR\n2019"] = dftables_["Ricavi delle vendite\nEUR\n2019"].round(2)
    dftables_["Ricavi delle vendite\nEUR\n2018"] = dftables_["Ricavi delle vendite\nEUR\n2018"].round(2)
    dftables_["Ricavi delle vendite\nEUR\n2017"] = dftables_["Ricavi delle vendite\nEUR\n2017"].round(2)
    dftables_["Ricavi delle vendite\nEUR\n2016"] = dftables_["Ricavi delle vendite\nEUR\n2016"].round(2)

    dftables_.columns = ['Ragione sociale', 'Descrizione',
                         'ROI (%)', 'Indebitamento a breve', 'Indebitamento a lungo', 'Margine di EBITDA',
                         'Posizione finanziaria netta', 'Latitudine', 'Longitudine', "Ricavi 2020",
                         "Ricavi 2019", "Ricavi 2018", "Ricavi 2017", "Ricavi 2016", ]

    datas = []
    for i in range(len(df)):
        if df.loc[i, "ATECO 2007\ndescrizione"] == data:
            datas.append(df.iloc[i, :])

    datas = pd.concat(datas, axis=1)
    datas = datas.transpose()
    datas.reset_index(inplace=True)
    datas.drop("index", axis=1, inplace=True)

    # incremento EBITDA(2020-2016)
    incremento_EBITDA = datas.apply(
        lambda x: (x['EBITDA\nEUR\n2020'] - x['EBITDA\nEUR\n2016']) * (100 / (x['EBITDA\nEUR\n2016'] + 1)),
        axis=1)

    dftables_["Incremento EBITDA"] = incremento_EBITDA
    dftables_["Incremento EBITDA"] = dftables_["Incremento EBITDA"].round(2)

    # Crescita fatturato(2020-2016)
    crescita_fatturato = datas.apply(
        lambda x: (x['Ricavi delle vendite\nEUR\n2020'] - x['Ricavi delle vendite\nEUR\n2016']) * 100 / (
                x['Ricavi delle vendite\nEUR\n2016'] + 1),
        axis=1)

    dftables_["Crescita fatturato (%)"] = crescita_fatturato
    dftables_["Crescita fatturato (%)"] = dftables_["Crescita fatturato (%)"].round(2)

    # quick ratio (denaro/DEBITI A BREVE\nEUR\n2020)
    quick_ratio = datas.apply(
        lambda x: (x['Denaro in cassa\nEUR\n2020'] / (x['DEBITI A BREVE\nEUR\n2020'] + 1)),
        axis=1)
    dftables_["Quick ratio"] = quick_ratio
    dftables_["Quick ratio"] = dftables_["Quick ratio"].round(2)

    newnames = []
    for index, row in dftables_.iterrows():
        inp1 = str(dftables_.loc[index, "Ragione sociale"])
        new_input1 = " "
        for i, letter in enumerate(inp1):
            if i % 34 == 0:
                new_input1 += '<br>'
            new_input1 += letter
        new_input1 = new_input1[1:]
        newnames.append(new_input1)

    dftables_["Ragione sociale new"] = newnames
    # print(len(dftables_["Ragione sociale new"]))

    # remove outlier
    cols = ['ROI (%)', 'Margine di EBITDA', 'Posizione finanziaria netta', "Incremento EBITDA", "Quick ratio",
            "Crescita fatturato (%)", "Ricavi 2020", "Ricavi 2019", "Ricavi 2018", "Ricavi 2017", "Ricavi 2016"]
    Q1 = dftables_[cols].quantile(0.25)
    Q3 = dftables_[cols].quantile(0.75)
    IQR = Q3 - Q1

    fer = dftables_[
        ~((dftables_[cols] < (Q1 - 1.5 * IQR)) | (dftables_[cols] > (Q3 + 1.5 * IQR))).any(axis=1)]

    dftables_ = fer
    dftables_.reset_index(inplace=True)
    dftables_.drop("index", axis=1, inplace=True)
    dftables_ = dftables_.sort_values(by='Crescita fatturato (%)', ascending=False)

    # --------------------------------------------

    df_ = dftables_.sort_values(by='Crescita fatturato (%)', ascending=False)
    # df_ = df_.iloc[0:10]
    df_.reset_index(inplace=True)
    df_.drop("index", axis=1, inplace=True)

    df_selected = []
    for x in selected_rows:
        df_selected.append(df_.iloc[x, :])
    df_selected = pd.concat(df_selected, axis=1)
    df_selected = df_selected.transpose()

    df_selected = df_selected.sort_values(by='Crescita fatturato (%)', ascending=False)
    df_selected = df_selected.loc[selected_rows]
    # print(df_selected)
    df_selected.reset_index(inplace=True)
    df_selected.drop("index", axis=1, inplace=True)

    newnames = []
    for index, row in df_.iterrows():
        inp1 = str(df_.loc[index, "Ragione sociale"])
        new_input1 = " "
        for i, letter in enumerate(inp1):
            if i % 34 == 0:
                new_input1 += '<br>'
            new_input1 += letter
        new_input1 = new_input1[1:]
        newnames.append(new_input1)

    df_["Ragione sociale new"] = newnames
    # print(len(dftables_["Ragione sociale new"]))

    # -----------------------------------------------------------------------------------------------------

    ricavi20_19 = df_selected.apply(
        lambda x: (x['Ricavi 2020'] - x['Ricavi 2019']) * 100 / (
                x['Ricavi 2019'] + 1),
        axis=1)
    df_selected["Ricavi medi 2020 - 2019"] = ricavi20_19
    df_selected["Ricavi medi 2020 - 2019"] = df_selected["Ricavi medi 2020 - 2019"].round(2)

    ricavi19_18 = df_selected.apply(
        lambda x: (x['Ricavi 2019'] - x['Ricavi 2018']) * 100 / (
                x['Ricavi 2018'] + 1),
        axis=1)
    df_selected["Ricavi medi 2019 - 2018"] = ricavi19_18
    df_selected["Ricavi medi 2019 - 2018"] = df_selected["Ricavi medi 2019 - 2018"].round(2)

    ricavi18_17 = df_selected.apply(
        lambda x: (x['Ricavi 2018'] - x['Ricavi 2017']) * 100 / (
                x['Ricavi 2017'] + 1),
        axis=1)
    df_selected["Ricavi medi 2018 - 2017"] = ricavi18_17
    df_selected["Ricavi medi 2018 - 2017"] = df_selected["Ricavi medi 2018 - 2017"].round(2)

    ricavi17_16 = df_selected.apply(
        lambda x: (x['Ricavi 2017'] - x['Ricavi 2016']) * 100 / (
                x['Ricavi 2016'] + 1),
        axis=1)
    df_selected["Ricavi medi 2017 - 2016"] = ricavi17_16
    df_selected["Ricavi medi 2017 - 2016"] = df_selected["Ricavi medi 2017 - 2016"].round(2)

    # ------------------------------------------------------------------------------------------------------
    ricavi20_19 = df_.apply(
        lambda x: (x['Ricavi 2020'] - x['Ricavi 2019']) * 100 / (
                x['Ricavi 2019'] + 1),
        axis=1)
    df_["Ricavi medi 2020 - 2019"] = ricavi20_19
    df_["Ricavi medi 2020 - 2019"] = df_["Ricavi medi 2020 - 2019"].round(2)

    ricavi19_18 = df_.apply(
        lambda x: (x['Ricavi 2019'] - x['Ricavi 2018']) * 100 / (
                x['Ricavi 2018'] + 1),
        axis=1)
    df_["Ricavi medi 2019 - 2018"] = ricavi19_18
    df_["Ricavi medi 2019 - 2018"] = df_["Ricavi medi 2019 - 2018"].round(2)

    ricavi18_17 = df_.apply(
        lambda x: (x['Ricavi 2018'] - x['Ricavi 2017']) * 100 / (
                x['Ricavi 2017'] + 1),
        axis=1)
    df_["Ricavi medi 2018 - 2017"] = ricavi18_17
    df_["Ricavi medi 2018 - 2017"] = df_["Ricavi medi 2018 - 2017"].round(2)

    ricavi17_16 = df_.apply(
        lambda x: (x['Ricavi 2017'] - x['Ricavi 2016']) * 100 / (
                x['Ricavi 2016'] + 1),
        axis=1)
    df_["Ricavi medi 2017 - 2016"] = ricavi17_16
    df_["Ricavi medi 2017 - 2016"] = df_["Ricavi medi 2017 - 2016"].round(2)

    # ---------------------------------------------------------------------------------------------------------
    data1 = pd.to_datetime(2020, format='%Y')
    data2 = pd.to_datetime(2019, format='%Y')
    data3 = pd.to_datetime(2018, format='%Y')
    data4 = pd.to_datetime(2017, format='%Y')

    # ---------------------------------------------------------------------------------------------------------
    colors_ = ['#800000', '#9A6324', '#808000', '#469990', '#000075',
               '#000000', '#e6194B', '#f58231', '#ffe119', '#bfef45',
               '#3cb44b', '#42d4f4', '#4363d8', '#911eb4', '#f032e6',
               '#a9a9a9', '#fabed4', '#ffd8b1', '#de3163', '#0B6623',
               ]

    fig = go.Figure()
    fig.data = []
    fig.layout = {}
    for index, row in df_.iterrows():
        for x in selected_rows:
            if x == index:
                y = df_.loc[x, 'Ricavi medi 2020 - 2019':'Ricavi medi 2017 - 2016']

                fig.add_trace(go.Scatter(x=[data1, data2, data3, data4],
                                         y=[y.iloc[0], y.iloc[1], y.iloc[2], y.iloc[3]],
                                         mode='lines+markers',
                                         customdata=[df_.loc[x, "Ricavi medi 2020 - 2019"],
                                                     df_.loc[x, "Ricavi medi 2019 - 2018"],
                                                     df_.loc[x, "Ricavi medi 2018 - 2017"],
                                                     df_.loc[x, "Ricavi medi 2017 - 2016"]],
                                         name=df_.loc[x, "Ragione sociale new"],
                                         text=df_.loc[x, "Ragione sociale new"],
                                         hovertemplate='<br><b>Ricavi:</b> %{customdata}',
                                         line=dict(color=colors_[x]),
                                         # showlegend=False,
                                         )
                              )

    if scelta == "ricavi migliori 20-19":
        fig.add_vline(x=data1, line_width=2, line_dash="dash", line_color="blue")
    elif scelta == "ricavi migliori 19-18":
        fig.add_vline(x=data2, line_width=2, line_dash="dash", line_color="blue")
    elif scelta == "ricavi migliori 18-17":
        fig.add_vline(x=data3, line_width=2, line_dash="dash", line_color="blue")
    elif scelta == "ricavi migliori 17-16":
        fig.add_vline(x=data4, line_width=2, line_dash="dash", line_color="blue")
    else:
        fig.add_vline(x=data1, line_width=2, line_dash="dash", line_color="blue")

    fig.update_layout(yaxis={'title': 'Ricavi(%) '},
                      title={'text': 'Crescita dei ricavi (%)',
                             'font': {'size': 18}, 'x': 0.5, 'xanchor': 'center'},
                      font=dict(
                          # family="Courier New, monospace",
                          size=12,
                          color="black"
                      ),
                      legend=dict(
                          x=1,
                          y=1,
                          font=dict(
                              # family="Courier",
                              size=12,
                              color="black"
                          ),
                          bgcolor="#ebeef0",
                          bordercolor="#8EA9C1",
                          borderwidth=1
                      ),
                      # hovermode="x unified",
                      )
    fig.update_traces(mode='lines+markers')

    return fig
