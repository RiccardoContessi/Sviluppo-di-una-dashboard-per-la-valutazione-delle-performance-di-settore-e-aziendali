import dash

dash.register_page(__name__, path="/")

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import textwrap
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output
from mydata import df
from dash import Dash, dcc, html, Input, Output, State, callback, dash_table
import plotly.express as px
import pandas as pd
from scipy import stats
import numpy as np

# df.style.format('{:.2f}')
pd.options.mode.chained_assignment = None  # default='warn'

pd.options.display.float_format = "{:,.2f}".format

# app = Dash(__name__)
# app = dash.Dash(__name__)
# server = app.server


# ----------------------------------------------------------------------------------------------------------------------
#   TABELLA
dftable = df.groupby(
    ['ATECO 2007\ncodice', 'ATECO 2007\ndescrizione'], as_index=False).agg(
    {'ATECO 2007\ncodice': 'count',
     'Redditività di tutto il capitale investito (ROI) (%)\n%\n2020': 'mean',
     # "Posizione finanziaria netta\nEUR\n2020": "mean",
     "Indice di indebitam. a breve\n%\n2020": 'mean',
     "Indice di indebitam. a lungo\n%\n2020": 'mean'}
)
dftable.columns = ['ATECO', 'num aziende', 'ROI (%)', "Indici indebitamento a breve", "Indici indebitamento a lungo"]
# dftable['ROI medio'] = dftable['ROI medio'].apply(lambda x: (dftable['ROI medio'], "%"))
# dftable["Fatturato medio"] = dftable["Fatturato medio"].round(2)

dftable_clear = dftable[dftable["num aziende"] > 20]
dftable_clear.reset_index(inplace=True)

# livello di concentrazione per ateco: 1 / num aziende
lvlconcentrazione = []
for i in range(len(dftable_clear)):
    concentrazione = 1 / dftable_clear.loc[i, 'num aziende']
    lvlconcentrazione.append(concentrazione)

lvlconcentrazione = [round(num, 3) for num in lvlconcentrazione]
lvlconc = pd.DataFrame({'HHI': lvlconcentrazione})
dftable_clear["HHI"] = lvlconc

# pd.set_option('display.max_columns', None)


# CRESCITA TOTALE FATTURATO
ricavi2016 = df.groupby(
    ['ATECO 2007\ncodice', 'ATECO 2007\ndescrizione'], as_index=False).agg(
    {'Ricavi delle vendite\nEUR\n2020': "mean",
     'Ricavi delle vendite\nEUR\n2016': "mean",
     }
)

ricavi20_16 = ricavi2016.apply(
    lambda x: (x['Ricavi delle vendite\nEUR\n2020'] - x['Ricavi delle vendite\nEUR\n2016']) * 100 / (
            x['Ricavi delle vendite\nEUR\n2016'] + 1),
    axis=1)
dftable_clear["Crescita totale fatturato (%)"] = ricavi20_16

dftable_clear["Crescita totale fatturato (%)"] = dftable_clear["Crescita totale fatturato (%)"].round(2)
dftable_clear["ROI (%)"] = dftable_clear["ROI (%)"].round(2)
dftable_clear["Indici indebitamento a breve"] = dftable_clear["Indici indebitamento a breve"].round(2)
dftable_clear["Indici indebitamento a lungo"] = dftable_clear["Indici indebitamento a lungo"].round(2)

dftable_clear.drop("index", axis=1, inplace=True)

# remove outlier
cols = ['ROI (%)', 'Crescita totale fatturato (%)']
Q1 = dftable_clear[cols].quantile(0.25)
Q3 = dftable_clear[cols].quantile(0.75)
IQR = Q3 - Q1

fer = dftable_clear[~((dftable_clear[cols] < (Q1 - 1.5 * IQR)) | (dftable_clear[cols] > (Q3 + 1.5 * IQR))).any(axis=1)]

dftable_clear = fer
dftable_clear.reset_index(inplace=True)
dftable_clear.drop("index", axis=1, inplace=True)
dftable_clear = dftable_clear.sort_values(by='ROI (%)', ascending=False)

# print(dftable_clear.columns.tolist())
col = ['ATECO', 'ROI (%)', 'Crescita totale fatturato (%)', 'num aziende', 'Indici indebitamento a breve',
       'Indici indebitamento a lungo', 'HHI', ]
dftable_clear = dftable_clear[col]

# ----------------------------------------------------------------------------------------------------------------------
#   ROA medio per ATECO--> bar chart
sum_ = df.groupby(
    ['ATECO 2007\ncodice', 'ATECO 2007\ndescrizione'], as_index=False).agg(
    {'Redditività di tutto il capitale investito (ROI) (%)\n%\n2020': 'mean',
     'ATECO 2007\ncodice': 'count'}
)
sum_.columns = ['ATECO 2007\ndescrizione', "Redditività di tutto il capitale investito (ROI) (%)\n%\n2020",
                "num aziende"]

sum_["Redditività di tutto il capitale investito (ROI) (%)\n%\n2020"] = sum_[
    "Redditività di tutto il capitale investito (ROI) (%)\n%\n2020"].round(2)

ateco_medio_per_roa = sum_.sort_values(by='Redditività di tutto il capitale investito (ROI) (%)\n%\n2020',
                                       ascending=False)
ateco_medio_per_roa_best_five = ateco_medio_per_roa.iloc[0:11]
ateco_medio_per_roa_best_five.reset_index(inplace=True)
ateco_medio_per_roa_best_five.drop("index", axis=1, inplace=True)

# print(ateco_medio_per_roa_best_five)

# print(ateco_medio_per_roa_best_five.iloc[0, 3])
# print(ateco_medio_per_roa_best_five.iloc[1, 3])


# ----------------------------------------------------------------------------------------------------------------------
#   PIE CHART QUALITATIVO
# pd.set_option('display.max_columns', None)
# pie_df = pd.read_excel(r'files\NEWINDICIQUALITATIVI.xlsx', index_col=0, header=0)
# pie_df.to_csv(r'files\indiciqualitativi.csv', index=False)
pie_df = pd.read_csv(r'files\indiciqualitativi.csv')
# print(pie_df)
# print(pie_df)


# ----------------------------------------------------------------------------------------------------------------------
# sottraggo ricavi dei vari anni
dff = pd.read_csv(r'E:\tesi\tesi\apps\files\dataClean.csv')
dframe = dff.copy()

mean_ricavi = dframe.groupby(
    ['ATECO 2007\ncodice', 'ATECO 2007\ndescrizione'], as_index=False).agg(
    {'Ricavi delle vendite\nEUR\n2020': "mean",
     'Ricavi delle vendite\nEUR\n2019': "mean",
     'Ricavi delle vendite\nEUR\n2018': "mean",
     'Ricavi delle vendite\nEUR\n2017': "mean",
     'Ricavi delle vendite\nEUR\n2016': "mean",
     }
)

# remove outlier
cols = ['Ricavi delle vendite\nEUR\n2020', 'Ricavi delle vendite\nEUR\n2019', 'Ricavi delle vendite\nEUR\n2018',
        'Ricavi delle vendite\nEUR\n2017', 'Ricavi delle vendite\nEUR\n2016']
Q1 = mean_ricavi[cols].quantile(0.25)
Q3 = mean_ricavi[cols].quantile(0.75)
IQR = Q3 - Q1

fer = mean_ricavi[~((mean_ricavi[cols] < (Q1 - 1.5 * IQR)) | (mean_ricavi[cols] > (Q3 + 1.5 * IQR))).any(axis=1)]
mean_ricavi = fer
mean_ricavi.reset_index(inplace=True)
mean_ricavi.drop("index", axis=1, inplace=True)

ricavi20_19 = mean_ricavi.apply(
    lambda x: (x['Ricavi delle vendite\nEUR\n2020'] - x['Ricavi delle vendite\nEUR\n2019']) * 100 / (
            x['Ricavi delle vendite\nEUR\n2019'] + 1),
    axis=1)
mean_ricavi["Ricavi medi 2020 - 2019"] = ricavi20_19
mean_ricavi["Ricavi medi 2020 - 2019"] = mean_ricavi["Ricavi medi 2020 - 2019"].round(2)

ricavi19_18 = mean_ricavi.apply(
    lambda x: (x['Ricavi delle vendite\nEUR\n2019'] - x['Ricavi delle vendite\nEUR\n2018']) * 100 / (
            x['Ricavi delle vendite\nEUR\n2018'] + 1),
    axis=1)
mean_ricavi["Ricavi medi 2019 - 2018"] = ricavi19_18
mean_ricavi["Ricavi medi 2019 - 2018"] = mean_ricavi["Ricavi medi 2019 - 2018"].round(2)

ricavi18_17 = mean_ricavi.apply(
    lambda x: (x['Ricavi delle vendite\nEUR\n2018'] - x['Ricavi delle vendite\nEUR\n2017']) * 100 / (
            x['Ricavi delle vendite\nEUR\n2017'] + 1),
    axis=1)
mean_ricavi["Ricavi medi 2018 - 2017"] = ricavi18_17
mean_ricavi["Ricavi medi 2018 - 2017"] = mean_ricavi["Ricavi medi 2018 - 2017"].round(2)

ricavi17_16 = mean_ricavi.apply(
    lambda x: (x['Ricavi delle vendite\nEUR\n2017'] - x['Ricavi delle vendite\nEUR\n2016']) * 100 / (
            x['Ricavi delle vendite\nEUR\n2016'] + 1),
    axis=1)
mean_ricavi["Ricavi medi 2017 - 2016"] = ricavi17_16
mean_ricavi["Ricavi medi 2017 - 2016"] = mean_ricavi["Ricavi medi 2017 - 2016"].round(2)

mean_ricavi = mean_ricavi.sort_values('Ricavi medi 2020 - 2019', ascending=False)
mean_ricavi.reset_index(inplace=True)

# pd.set_option('display.max_columns', None)
# print(mean_ricavi)

cols = ['Ricavi medi 2020 - 2019', 'Ricavi medi 2019 - 2018', 'Ricavi medi 2018 - 2017',
        'Ricavi medi 2017 - 2016']
Q1 = mean_ricavi[cols].quantile(0.25)
Q3 = mean_ricavi[cols].quantile(0.75)
IQR = Q3 - Q1

fer = mean_ricavi[~((mean_ricavi[cols] < (Q1 - 1.5 * IQR)) | (mean_ricavi[cols] > (Q3 + 1.5 * IQR))).any(axis=1)]
mean_ricavi = fer
mean_ricavi.reset_index(inplace=True)
mean_ricavi.drop("index", axis=1, inplace=True)

y0 = mean_ricavi.loc[0, 'Ricavi medi 2020 - 2019':'Ricavi medi 2017 - 2016']
y1 = mean_ricavi.loc[1, 'Ricavi medi 2020 - 2019':'Ricavi medi 2017 - 2016']
y2 = mean_ricavi.loc[2, 'Ricavi medi 2020 - 2019':'Ricavi medi 2017 - 2016']
y3 = mean_ricavi.loc[3, 'Ricavi medi 2020 - 2019':'Ricavi medi 2017 - 2016']
y4 = mean_ricavi.loc[4, 'Ricavi medi 2020 - 2019':'Ricavi medi 2017 - 2016']
y5 = mean_ricavi.loc[5, 'Ricavi medi 2020 - 2019':'Ricavi medi 2017 - 2016']
y6 = mean_ricavi.loc[6, 'Ricavi medi 2020 - 2019':'Ricavi medi 2017 - 2016']
y7 = mean_ricavi.loc[7, 'Ricavi medi 2020 - 2019':'Ricavi medi 2017 - 2016']
y8 = mean_ricavi.loc[8, 'Ricavi medi 2020 - 2019':'Ricavi medi 2017 - 2016']
y9 = mean_ricavi.loc[9, 'Ricavi medi 2020 - 2019':'Ricavi medi 2017 - 2016']

# ----------------------------------------------------------------------------------------------------------------------

# BREVE
breve = df.groupby(
    ['ATECO 2007\ncodice', 'ATECO 2007\ndescrizione'], as_index=False).agg(
    {'Indice di indebitam. a breve\n%\n2020': "mean",
     'Indice di indebitam. a lungo\n%\n2020': "mean",
     'ATECO 2007\ncodice': 'count'}
)
breve.columns = ['ATECO', 'indice indebitam a breve', 'indice indebitam a lungo', 'num aziende']

# breve = breve.sort_values(by='indice indebitam a breve', ascending=True)
# print(breve.loc[:, 'indice indebitam a breve'])

breve_ = []
for i in range(len(breve)):
    if breve.loc[i, "indice indebitam a breve"] > 0.25 and breve.loc[i, "indice indebitam a breve"] < 0.50 and \
            breve.loc[i, 'num aziende'] > 20:
        breve_.append(breve.iloc[i, :])

breve_ = pd.concat(breve_, axis=1)
breve_ = breve_.transpose()

# pd.set_option('display.max_columns', None)
breve_ = breve_.sort_values(by='indice indebitam a breve', ascending=True)
breve_.reset_index(inplace=True)
breve_.drop("index", axis=1, inplace=True)
breve_barchart = breve_.iloc[0:10, :]

# --------------------------------------------------------------------------------------------------------------------
# LUNGO
lungo = df.groupby(
    ['ATECO 2007\ncodice', 'ATECO 2007\ndescrizione'], as_index=False).agg(
    {'Indice di indebitam. a breve\n%\n2020': "mean",
     'Indice di indebitam. a lungo\n%\n2020': "mean",
     'ATECO 2007\ncodice': 'count'}
)
lungo.columns = ['ATECO', 'indice indebitam a breve', 'indice indebitam a lungo', 'num aziende']

lungo_ = []
for i in range(len(lungo)):
    if lungo.loc[i, "indice indebitam a lungo"] > 0.25 and lungo.loc[i, "indice indebitam a lungo"] < 0.50 and \
            lungo.loc[i, 'num aziende'] > 20:
        lungo_.append(lungo.iloc[i, :])

lungo_ = pd.concat(lungo_, axis=1)
lungo_ = lungo_.transpose()

lungo_ = lungo_.sort_values(by='indice indebitam a lungo', ascending=True)

# pd.set_option('display.max_columns', None)
# print(lungo_.iloc[0:10, :])

lungo_.reset_index(inplace=True)
lungo_.drop("index", axis=1, inplace=True)
lungo_barchart = lungo_.iloc[0:10, :]
# print(lungo_.loc[0:35,'indice indebitam a lungo' ])
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# App layout --> HTML ELEMENT
# from app import app
layout = html.Div([
    # html.Div([
    #     html.H2("SVILUPPO DI UNA DASHBOARD PER LA VALUTAZIONE DELLE PERFORMANCE DI SETTORE E AZIENDALI",
    #             style={'text-align': 'center', 'color': '#606060'}, className="titolo"),
    # #     # html.Img(src='/assets/image.png', className="logo"),
    # #
    # ], className="intestazione"),
    html.Div(id="store", className="store"),
    html.H3("Visualizzazione settori per ATECO 2007", style={'text-align': 'center', 'color': '#606060'},
            className="sottotitolo"),

    html.Div([
        dash_table.DataTable(
            id="datatable",
            columns=[
                {'name': i, 'id': i, 'deletable': False} for i in dftable_clear.columns
                # omit the id column
                if i != 'id'
            ],
            data=dftable_clear.to_dict('records'),
            editable=False,
            filter_action="native",
            sort_action="native",
            sort_mode='single',
            row_selectable='single',
            column_selectable="single",
            row_deletable=False,
            selected_rows=[],
            selected_row_ids=[],
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
            style_cell={'fontSize': 13,
                        'font-family': 'sans-serif',
                        'fontWeight': 'bold',
                        'text_align': 'left',
                        'color': 'black',
                        'padding': '3px',
                        # 'minWidth': 25,
                        # 'width': 25,
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
        html.Div(id='datatable-row-ids-container'),
        # FINE DATA TABLE
        html.H3(
            [f'➤  Scegliere il settore desiderato in tabella e selezionare ',
             html.Span('"ANALISI AZIENDE"', className="colorSpan"),
             ' nell Header per analizzare tale settore'],
            style={'text-align': 'left', 'color': 'black'},
            className="sottotitolo2"),

    ], className="prova4"),
    # FINE DIV CON TABELLA E BOTTONE

    html.Div([
        # dcc.Dropdown(id="slct_year",
        #              options=[
        #                  {"label": "best ATECO for ROI", "value": "ascending"},
        #                  {"label": "worse ATECO for ROI", "value": "descending"},
        #                  ],
        #              multi=False,
        #              value="ascending",
        #              style={'width': "98%"},
        #              className="prova33"
        #              ),
    ], className="prova3"),
    # FINE DIV CON DROPDOWN ANNO

    html.Div([
        html.Div([
            dcc.Dropdown(id="slct_year",
                         options=[
                             {"label": "Settori migliori per ROI", "value": "ascending"},
                             {"label": "Settori peggiori per ROI", "value": "descending"},
                             {"label": "Settori migliori per ROE", "value": "ascendingROE"},
                             {"label": "Settori peggiori per ROE", "value": "descendingROE"},
                         ],
                         multi=False,
                         value="ascending",
                         # style={'width': "98%"},
                         searchable=False,
                         clearable=False,
                         className="dropdown"
                         ),

            dcc.Graph(id='histogram', className="prova1"),
        ], className="six columns"),

        html.Div([
            # dcc.Graph(id='histogramx', className="prova2"),
            # html.P("titolo qui:", style={'text-align': 'center'}),
            dcc.Dropdown(
                id='indici',
                value='INNOVAZIONE(migliaia€)',
                # style={"backgroundColor": "#D6E4EA", "color": "black"},
                # options=[{'value': x, 'label': x}
                #          for x in ['innovazione', 'digitalizzazione', '"green propensity"']],
                options=[
                    {"label": "Investimento dei settori in innovazione   (migliaia di Euro)",
                     "value": "INNOVAZIONE(migliaia€)"},
                    {"label": "Investimento dei settori in digitalizzazione   (%)", "value": "DIGITALIZZAZIONE(%)"},
                    {"label": "Investimento dei settori in green propensity   (migliaia di Euro)",
                     "value": "GREEN PROPENSITY(migliaia€)"},
                ],
                searchable=False,
                clearable=False,
                className="dropdown2"
            ),

            dcc.Graph(id="pie-chart", className="prova2"),
        ], className="six columns")  # FINE PIE CHART QUALITATIVO
    ], className="div12"),
    # FINE PRIMI 2 GRAFICI

    html.Div([
        # GRAFICO XY
        html.Div([
            dcc.RadioItems(
                id="checklist",
                options=[{"label": "Ricavi migliori 20-19", "value": "ricavi migliori 20-19"},
                         {"label": "Ricavi migliori 19-18", "value": "ricavi migliori 19-18"},
                         {"label": "Ricavi migliori 18-17", "value": "ricavi migliori 18-17"},
                         {"label": "Ricavi migliori 17-16", "value": "ricavi migliori 17-16"},
                         ],
                # labelStyle={'display': 'inline-block'},
                className="check_list",
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
            dcc.Graph(id="line-chart", className="graficoxy"),
        ], className="six columns"),

        # DOPPIO BAR CHART
        html.Div([
            dcc.Dropdown(
                id='xaxis_raditem',
                options=[
                    {'label': 'Indebitamento a breve', 'value': 'Indebitamento a breve'},
                    {'label': 'Indebitamento a lungo', 'value': 'Indebitamento a lungo'},
                ],
                # style={"width": "50%"},
                value="Indebitamento a breve",
                clearable=False,
                searchable=False,
                className="dropdownIndici",
            ),
            dcc.Graph(id='the_graph', className="doppiobarchart")
        ], className="six columns")
    ], className="div34"),
    # FINE ULTIMI 2 GRAFICI

    html.Div(id='output_container', children=[], className="spazio"),
    html.P("-            ", className="spazio")
], className="table")


# FINE LAYOUT

# ----------------------------------------------------------------------------------------------------------------------
# BAR CHART ( GRAFICO 1 )
@callback(

    [Output(component_id='output_container', component_property='children'),
     Output(component_id='histogram', component_property='figure')],
    [Input(component_id='slct_year', component_property='value')]
)
def update_graph(option_slctd):  # come argomento ci va il component_id di INPUT e seleziono la proprietà value

    if option_slctd == "ascending":
        df_barchart_clear = sum_[sum_["num aziende"] > 20]
        df_barchart_clear.reset_index(inplace=True)
        histo_df = df_barchart_clear
        histo_df = histo_df.sort_values(by='Redditività di tutto il capitale investito (ROI) (%)\n%\n2020',
                                        ascending=False)

        histo_df = histo_df.iloc[0:10]
        histo_df.reset_index(inplace=True)
        histo_df.drop("index", axis=1, inplace=True)

        container = ""

        dfff = histo_df.copy()
        dfff = dfff.rename(columns={'Redditività di tutto il capitale investito (ROI) (%)\n%\n2020': 'ROI 2020'})

        fig = go.Figure()
        fig.add_trace(go.Bar(x=dfff['ATECO 2007\ndescrizione'],
                             y=dfff["ROI 2020"],
                             name='',
                             text=dfff["ROI 2020"],
                             legendgroup="group",
                             legendgrouptitle_text="ROI",
                             # marker_color='#37536d',
                             # marker_color=dfff["ROI 2020"],
                             marker=dict(
                                 color=dfff["ROI 2020"],
                                 # colorscale=px.colors.sequential.ice,
                                 showscale=True,
                                 # color_discrete_sequence=px.colors.sequential.ice
                                 colorscale=['#91c8ff', '#5c9cdb', '#1079e3', '#1a70c7', '#2e6aa6',
                                             '#10569c', '#245382', '#093969', '#041a30']
                             ),
                             customdata=[dfff.loc[0, "num aziende"], dfff.loc[1, "num aziende"],
                                         dfff.loc[2, "num aziende"],
                                         dfff.loc[3, "num aziende"], dfff.loc[4, "num aziende"],
                                         dfff.loc[5, "num aziende"],
                                         dfff.loc[6, "num aziende"], dfff.loc[7, "num aziende"],
                                         dfff.loc[8, "num aziende"],
                                         dfff.loc[9, "num aziende"], ],
                             hovertemplate='<br><b>Descrizione:</b> %{x}</br>' +
                                           '<b>ROI 2020:</b>  %{y}%<br>' +
                                           '<b>Num. aziende:</b> %{customdata}<br>',
                             # showlegend=True

                             ))

        fig.update_xaxes(visible=False, showticklabels=True)
        fig.update_yaxes(visible=True, showticklabels=True)

        fig.update_layout(

            # # title='indice indebitam a breve',
            # xaxis_tickfont_size=14,
            # # xaxis={'visible': False, 'showticklabels': False},
            # yaxis={'visible': True, 'showticklabels': True},

            legend=dict(
                x=1.025,
                y=1.2,
                # bgcolor='rgba(255, 255, 255, 0)',
                # bordercolor='rgba(255, 255, 255, 0)',

                # title_font_family="Times New Roman",
                font=dict(
                    # family="Courier",
                    size=12,
                    color="black"
                ),
                bgcolor="#ebeef0",
                bordercolor="#8EA9C1",
                borderwidth=1

            ),
            barmode='group',
            # bargap=0.15,  # gap between bars of adjacent location coordinates.
            # bargroupgap=0.1  # gap between bars of the same location coordinate.
            title={'text': 'Miglior ROI medio per settore ATECO',
                   'font': {'size': 18}, 'x': 0.5, 'xanchor': 'center'},
        )
        return container, fig

    elif option_slctd == "descending":
        df_barchart_clear = sum_[sum_["num aziende"] > 20]
        df_barchart_clear.reset_index(inplace=True)
        histo_df = df_barchart_clear
        histo_df = histo_df.sort_values(by='Redditività di tutto il capitale investito (ROI) (%)\n%\n2020',
                                        ascending=True)

        histo_df = histo_df.iloc[0:10]
        histo_df.reset_index(inplace=True)
        histo_df.drop("index", axis=1, inplace=True)

        container = ""

        dfff = histo_df.copy()
        dfff = dfff.rename(columns={'Redditività di tutto il capitale investito (ROI) (%)\n%\n2020': 'ROI 2020'})

        fig = go.Figure()
        fig.add_trace(go.Bar(x=dfff['ATECO 2007\ndescrizione'],
                             y=dfff["ROI 2020"],
                             name=' ',
                             text=dfff["ROI 2020"],
                             # marker_color='#4d7499',
                             # marker_color= dfff["ROI 2020"],
                             marker=dict(
                                 color=dfff["ROI 2020"],
                                 # colorscale='ice',
                                 showscale=True,
                                 # colorscale=px.colors.sequential.ice,
                                 colorscale=['#91c8ff', '#5c9cdb', '#1079e3', '#1a70c7', '#2e6aa6',
                                             '#10569c', '#245382', '#093969', '#041a30']
                                 # colorscale=['#041a30', '#093969', '#245382','#10569c',  '#2e6aa6',
                                 # '#1a70c7','#1079e3','#5c9cdb','#91c8ff']
                             ),
                             customdata=[dfff.loc[0, "num aziende"], dfff.loc[1, "num aziende"],
                                         dfff.loc[2, "num aziende"],
                                         dfff.loc[3, "num aziende"], dfff.loc[4, "num aziende"],
                                         dfff.loc[5, "num aziende"],
                                         dfff.loc[6, "num aziende"], dfff.loc[7, "num aziende"],
                                         dfff.loc[8, "num aziende"],
                                         dfff.loc[9, "num aziende"], ],
                             hovertemplate='<br><b>Descrizione:</b> %{x}</br>' +
                                           '<b>ROI 2020:</b>  %{y}%<br>' +
                                           '<b>Num. aziende:</b> %{customdata}<br>',
                             showlegend=False

                             ))
        fig.update_xaxes(visible=False, showticklabels=True)
        fig.update_layout(
            # title='ROI medio per settore ATECO',
            xaxis_tickfont_size=14,
            # xaxis={'visible': False, 'showticklabels': False},
            yaxis=dict(
                titlefont_size=16,
                tickfont_size=14,
            ),

            legend=dict(
                x=1,
                y=1,
                # bgcolor='rgba(255, 255, 255, 0)',
                # bordercolor='rgba(255, 255, 255, 0)',

                # title_font_family="Times New Roman",
                font=dict(
                    # family="Courier",
                    size=12,
                    color="black"
                ),
                bgcolor="#ebeef0",
                bordercolor="#8EA9C1",
                borderwidth=1

            ),
            barmode='group',
            # bargap=0.15,  # gap between bars of adjacent location coordinates.
            # bargroupgap=0.1  # gap between bars of the same location coordinate.
            title={'text': 'Peggior ROI medio per settore ATECO',
                   'font': {'size': 18}, 'x': 0.5, 'xanchor': 'center'},
        )
        return container, fig

    # -----------------------------------------------------------------------------------------------------------------
    elif option_slctd == "ascendingROE":
        df_barchart_clear = sum_[sum_["num aziende"] > 20]
        df_barchart_clear.reset_index(inplace=True)
        histo_df = df_barchart_clear
        histo_df = histo_df.sort_values(by='Redditività di tutto il capitale investito (ROI) (%)\n%\n2020',
                                        ascending=True)

        histo_df = histo_df.iloc[0:10]
        histo_df.reset_index(inplace=True)
        histo_df.drop("index", axis=1, inplace=True)

        container = ""

        dfff = histo_df.copy()
        dfff = dfff.rename(columns={'Redditività di tutto il capitale investito (ROI) (%)\n%\n2020': 'ROI 2020'})

        fig = go.Figure()
        fig.add_trace(go.Bar(x=dfff['ATECO 2007\ndescrizione'],
                             y=dfff["ROI 2020"],
                             name=' ',
                             text=dfff["ROI 2020"],
                             # marker_color='#4d7499',
                             # marker_color= dfff["ROI 2020"],
                             marker=dict(
                                 color=dfff["ROI 2020"],
                                 # colorscale='ice',
                                 showscale=True,
                                 # colorscale=px.colors.sequential.ice,
                                 colorscale=['#91c8ff', '#5c9cdb', '#1079e3', '#1a70c7', '#2e6aa6',
                                             '#10569c', '#245382', '#093969', '#041a30']
                                 # colorscale=['#041a30', '#093969', '#245382','#10569c',  '#2e6aa6',
                                 # '#1a70c7','#1079e3','#5c9cdb','#91c8ff']
                             ),
                             customdata=[dfff.loc[0, "num aziende"], dfff.loc[1, "num aziende"],
                                         dfff.loc[2, "num aziende"],
                                         dfff.loc[3, "num aziende"], dfff.loc[4, "num aziende"],
                                         dfff.loc[5, "num aziende"],
                                         dfff.loc[6, "num aziende"], dfff.loc[7, "num aziende"],
                                         dfff.loc[8, "num aziende"],
                                         dfff.loc[9, "num aziende"], ],
                             hovertemplate='<br><b>Descrizione:</b> %{x}</br>' +
                                           '<b>ROE 2020:</b>  %{y}%<br>' +
                                           '<b>Num. aziende:</b> %{customdata}<br>',
                             showlegend=False

                             ))
        fig.update_xaxes(visible=False, showticklabels=True)
        fig.update_layout(
            # title='ROI medio per settore ATECO',
            xaxis_tickfont_size=14,
            # xaxis={'visible': False, 'showticklabels': False},
            yaxis=dict(
                titlefont_size=16,
                tickfont_size=14,
            ),

            legend=dict(
                x=1,
                y=1,
                # bgcolor='rgba(255, 255, 255, 0)',
                # bordercolor='rgba(255, 255, 255, 0)',

                # title_font_family="Times New Roman",
                font=dict(
                    # family="Courier",
                    size=12,
                    color="black"
                ),
                bgcolor="#ebeef0",
                bordercolor="#8EA9C1",
                borderwidth=1

            ),
            barmode='group',
            # bargap=0.15,  # gap between bars of adjacent location coordinates.
            # bargroupgap=0.1  # gap between bars of the same location coordinate.
            title={'text': 'Miglior ROE medio per settore ATECO',
                   'font': {'size': 18}, 'x': 0.5, 'xanchor': 'center'},
        )
        return container, fig

        # -----------------------------------------------------------------------------------------------------------------
    elif option_slctd == "descendingROE":
        df_barchart_clear = sum_[sum_["num aziende"] > 20]
        df_barchart_clear.reset_index(inplace=True)
        histo_df = df_barchart_clear
        histo_df = histo_df.sort_values(by='Redditività di tutto il capitale investito (ROI) (%)\n%\n2020',
                                        ascending=True)

        histo_df = histo_df.iloc[0:10]
        histo_df.reset_index(inplace=True)
        histo_df.drop("index", axis=1, inplace=True)

        container = ""

        dfff = histo_df.copy()
        dfff = dfff.rename(columns={'Redditività di tutto il capitale investito (ROI) (%)\n%\n2020': 'ROI 2020'})

        fig = go.Figure()
        fig.add_trace(go.Bar(x=dfff['ATECO 2007\ndescrizione'],
                             y=dfff["ROI 2020"],
                             name=' ',
                             text=dfff["ROI 2020"],
                             # marker_color='#4d7499',
                             # marker_color= dfff["ROI 2020"],
                             marker=dict(
                                 color=dfff["ROI 2020"],
                                 # colorscale='ice',
                                 showscale=True,
                                 # colorscale=px.colors.sequential.ice,
                                 colorscale=['#91c8ff', '#5c9cdb', '#1079e3', '#1a70c7', '#2e6aa6',
                                             '#10569c', '#245382', '#093969', '#041a30']
                                 # colorscale=['#041a30', '#093969', '#245382','#10569c',  '#2e6aa6',
                                 # '#1a70c7','#1079e3','#5c9cdb','#91c8ff']
                             ),
                             customdata=[dfff.loc[0, "num aziende"], dfff.loc[1, "num aziende"],
                                         dfff.loc[2, "num aziende"],
                                         dfff.loc[3, "num aziende"], dfff.loc[4, "num aziende"],
                                         dfff.loc[5, "num aziende"],
                                         dfff.loc[6, "num aziende"], dfff.loc[7, "num aziende"],
                                         dfff.loc[8, "num aziende"],
                                         dfff.loc[9, "num aziende"], ],
                             hovertemplate='<br><b>Descrizione:</b> %{x}</br>' +
                                           '<b>ROE 2020:</b>  %{y}%<br>' +
                                           '<b>Num. aziende:</b> %{customdata}<br>',
                             showlegend=False

                             ))
        fig.update_xaxes(visible=False, showticklabels=True)
        fig.update_layout(
            # title='ROI medio per settore ATECO',
            xaxis_tickfont_size=14,
            # xaxis={'visible': False, 'showticklabels': False},
            yaxis=dict(
                titlefont_size=16,
                tickfont_size=14,
            ),

            legend=dict(
                x=1,
                y=1,
                # bgcolor='rgba(255, 255, 255, 0)',
                # bordercolor='rgba(255, 255, 255, 0)',

                # title_font_family="Times New Roman",
                font=dict(
                    # family="Courier",
                    size=12,
                    color="black"
                ),
                bgcolor="#ebeef0",
                bordercolor="#8EA9C1",
                borderwidth=1

            ),
            barmode='group',
            # bargap=0.15,  # gap between bars of adjacent location coordinates.
            # bargroupgap=0.1  # gap between bars of the same location coordinate.
            title={'text': 'Peggior ROE medio per settore ATECO',
                   'font': {'size': 18}, 'x': 0.5, 'xanchor': 'center'},
        )
        return container, fig


# ----------------------------------------------------------------------------------------------------------------------
# TREEMAP + CHECK BOK (GRAFICO 2)

@callback(
    Output("pie-chart", "figure"),
    [Input("indici", "value")]
)
def generate_chart(values):
    if values == 'INNOVAZIONE(migliaia€)':
        simbolo = "migliaia€"
    elif values == 'DIGITALIZZAZIONE(%)':
        simbolo = "%"
    elif values == 'GREEN PROPENSITY(migliaia€)':
        simbolo = "migliaia€"

    pieUnique = pie_df.groupby(['ATECO', 'DESCRIZIONE'], as_index=False).agg(
        {'INNOVAZIONE(migliaia€)': 'sum',
         'DIGITALIZZAZIONE(%)': 'sum',
         'GREEN PROPENSITY(migliaia€)': 'sum'}
    )
    pieUnique["INNOVAZIONE(migliaia€)"] = pieUnique["INNOVAZIONE(migliaia€)"].round(2)
    pieUnique["DIGITALIZZAZIONE(%)"] = pieUnique["DIGITALIZZAZIONE(%)"].round(2)
    pieUnique["GREEN PROPENSITY(migliaia€)"] = pieUnique["GREEN PROPENSITY(migliaia€)"].round(2)

    df_pie = pieUnique.sort_values(by=values, ascending=False)
    df_pie = df_pie.iloc[0:30]
    df_pie.reset_index(inplace=True)

    fig = go.Figure(go.Treemap(
        labels=df_pie['ATECO'],
        values=df_pie[values],
        name="",
        parents=["", "", "", "", "", "", "", "", "", "",
                 "", "", "", "", "", "", "", "", "", "",
                 "", "", "", "", "", "", "", "", "", "", ],
        root_color="#D6E4EA",
        textinfo="label+value+percent root",
        customdata=[simbolo, simbolo, simbolo, simbolo, simbolo, simbolo, simbolo, simbolo, simbolo, simbolo,
                    simbolo, simbolo, simbolo, simbolo, simbolo, simbolo, simbolo, simbolo, simbolo, simbolo,
                    simbolo, simbolo, simbolo, simbolo, simbolo, simbolo, simbolo, simbolo, simbolo, simbolo, ],
        text=df_pie['DESCRIZIONE'],
        hovertemplate='<b>codice ATECO:</b> %{label}<br><b>descrizione:</b> %{text}<br> <b>valore:</b> %{value} %{customdata}</b>'

        # marker_colorscale='Blues'
    ))
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25),
                      title={'text': 'Investimento in Indici qualitativi per settore ATECO',
                             'font': {'size': 18}, 'x': 0.5, 'xanchor': 'center'},
                      treemapcolorway=['#274B9F', '#4662AC', '#5D7AB9', '#7694CB', '#A3C0E4',
                                       '#274B9F', '#4662AC', '#5D7AB9', '#7694CB', '#A3C0E4',
                                       '#274B9F', '#4662AC', '#5D7AB9', '#7694CB', '#A3C0E4',
                                       '#274B9F', '#4662AC', '#5D7AB9', '#7694CB', '#A3C0E4',
                                       '#274B9F', '#4662AC', '#5D7AB9', '#7694CB', '#A3C0E4',
                                       '#274B9F', '#4662AC', '#5D7AB9', '#7694CB', '#A3C0E4']
                      )

    return fig


# ----------------------------------------------------------------------------------------------------------------------
# CHECK BOX + LINE CHART (GRAFICO 3)

@callback(
    Output("line-chart", "figure"),
    [Input("checklist", "value")])
def update_line_chart(continents):
    global mean_ricavi
    if continents == "ricavi migliori 20-19":
        mean_ricavi = mean_ricavi.sort_values('Ricavi medi 2020 - 2019', ascending=False)
        mean_ricavi.reset_index(inplace=True, drop=True)
    elif continents == "ricavi migliori 19-18":
        mean_ricavi = mean_ricavi.sort_values('Ricavi medi 2019 - 2018', ascending=False)
        mean_ricavi.reset_index(inplace=True, drop=True)
    elif continents == "ricavi migliori 18-17":
        mean_ricavi = mean_ricavi.sort_values('Ricavi medi 2018 - 2017', ascending=False)
        mean_ricavi.reset_index(inplace=True, drop=True)
    elif continents == "ricavi migliori 17-16":
        mean_ricavi = mean_ricavi.sort_values('Ricavi medi 2017 - 2016', ascending=False)
        mean_ricavi.reset_index(inplace=True, drop=True)
    else:
        mean_ricavi = mean_ricavi.sort_values('Ricavi medi 2020 - 2019', ascending=False)
        mean_ricavi.reset_index(inplace=True, drop=True)

    y0 = mean_ricavi.loc[0, 'Ricavi medi 2020 - 2019':'Ricavi medi 2017 - 2016']
    y1 = mean_ricavi.loc[1, 'Ricavi medi 2020 - 2019':'Ricavi medi 2017 - 2016']
    y2 = mean_ricavi.loc[2, 'Ricavi medi 2020 - 2019':'Ricavi medi 2017 - 2016']
    y3 = mean_ricavi.loc[3, 'Ricavi medi 2020 - 2019':'Ricavi medi 2017 - 2016']
    y4 = mean_ricavi.loc[4, 'Ricavi medi 2020 - 2019':'Ricavi medi 2017 - 2016']
    # y5 = mean_ricavi.loc[5, 'Ricavi medi 2020 - 2019':'Ricavi medi 2017 - 2016']
    # y6 = mean_ricavi.loc[6, 'Ricavi medi 2020 - 2019':'Ricavi medi 2017 - 2016']
    # y7 = mean_ricavi.loc[7, 'Ricavi medi 2020 - 2019':'Ricavi medi 2017 - 2016']
    # y8 = mean_ricavi.loc[8, 'Ricavi medi 2020 - 2019':'Ricavi medi 2017 - 2016']
    # y9 = mean_ricavi.loc[9, 'Ricavi medi 2020 - 2019':'Ricavi medi 2017 - 2016']

    data1 = pd.to_datetime(2020, format='%Y')
    data2 = pd.to_datetime(2019, format='%Y')
    data3 = pd.to_datetime(2018, format='%Y')
    data4 = pd.to_datetime(2017, format='%Y')

    fig = px.line(mean_ricavi,
                  x=[data1, data2, data3, data4],
                  y=[[y0.iloc[0], y0.iloc[1], y0.iloc[2], y0.iloc[3]],
                     [y1.iloc[0], y1.iloc[1], y1.iloc[2], y1.iloc[3]],
                     [y2.iloc[0], y2.iloc[1], y2.iloc[2], y2.iloc[3]],
                     [y3.iloc[0], y3.iloc[1], y3.iloc[2], y3.iloc[3]],
                     [y4.iloc[0], y4.iloc[1], y4.iloc[2], y4.iloc[3]],
                     # [y5.iloc[0], y5.iloc[1], y5.iloc[2], y5.iloc[3]],
                     # [y6.iloc[0], y6.iloc[1], y6.iloc[2], y6.iloc[3]],
                     ],
                  # width=1200,
                  # height=400,
                  labels={
                      "x": "Periodo temporale",
                      "variable": "Codici ATECO",
                  },
                  # text=["ATECO 2007\ndescrizione"],

                  )

    if continents == "ricavi migliori 20-19":
        fig.add_vline(x=data1, line_width=2, line_dash="dash", line_color="blue")
    elif continents == "ricavi migliori 19-18":
        fig.add_vline(x=data2, line_width=2, line_dash="dash", line_color="blue")
    elif continents == "ricavi migliori 18-17":
        fig.add_vline(x=data3, line_width=2, line_dash="dash", line_color="blue")
    elif continents == "ricavi migliori 17-16":
        fig.add_vline(x=data4, line_width=2, line_dash="dash", line_color="blue")
    else:
        fig.add_vline(x=data1, line_width=2, line_dash="dash", line_color="blue")

    fig.update_layout(yaxis={'title': 'Ricavi(%) '},
                      title={'text': 'Settori con maggiore crescita dei ricavi (%)',
                             'font': {'size': 18}, 'x': 0.5, 'xanchor': 'center'},
                      font=dict(
                          # family="Courier New, monospace",
                          size=12,
                          color="black"
                      ),
                      # legend=dict(title_font_family="Times New Roman",
                      #             font=dict(size=10))
                      legend=dict(
                          x=1,
                          y=1,

                          # title_font_family="Times New Roman",
                          font=dict(
                              # family="Courier",
                              size=12,
                              color="black"
                          ),
                          bgcolor="#ebeef0",
                          bordercolor="#8EA9C1",
                          borderwidth=1
                      )
                      )
    fig.update_traces(mode='lines+markers')

    # ------------------------------------------------------------
    inp1 = str(mean_ricavi.iloc[0, 2])
    new_input1 = " "
    for i, letter in enumerate(inp1):
        if i % 34 == 0:
            new_input1 += '<br>'
        new_input1 += letter
    new_input1 = new_input1[1:]
    # ------------------------------------------------------------
    inp2 = str(mean_ricavi.iloc[1, 2])
    new_input2 = " "
    for i, letter in enumerate(inp2):
        if i % 34 == 0:
            new_input2 += '<br>'
        new_input2 += letter
    new_input2 = new_input2[1:]
    # ------------------------------------------------------------
    inp3 = str(mean_ricavi.iloc[2, 2])
    new_input3 = " "
    for i, letter in enumerate(inp3):
        if i % 34 == 0:
            new_input3 += '<br>'
        new_input3 += letter
    new_input3 = new_input3[1:]
    # ------------------------------------------------------------
    inp4 = str(mean_ricavi.iloc[3, 2])
    new_input4 = " "
    for i, letter in enumerate(inp4):
        if i % 34 == 0:
            new_input4 += '<br>'
        new_input4 += letter
    new_input4 = new_input4[1:]
    # ------------------------------------------------------------
    inp5 = str(mean_ricavi.iloc[4, 2])
    new_input5 = " "
    for i, letter in enumerate(inp5):
        if i % 34 == 0:
            new_input5 += '<br>'
        new_input5 += letter
    new_input5 = new_input5[1:]
    # ------------------------------------------------------------
    inp6 = str(mean_ricavi.iloc[5, 2])
    new_input6 = " "
    for i, letter in enumerate(inp6):
        if i % 34 == 0:
            new_input6 += '<br>'
        new_input6 += letter
    new_input6 = new_input6[1:]
    # ------------------------------------------------------------

    newnames = {'wide_variable_0': new_input1, 'wide_variable_1': new_input2,
                'wide_variable_2': new_input3, 'wide_variable_3': new_input4,
                'wide_variable_4': new_input5,
                # 'wide_variable_5': str(mean_ricavi.iloc[5, 1]),
                # 'wide_variable_6': str(mean_ricavi.iloc[6, 1])
                }

    fig.for_each_trace(lambda t: t.update(name=newnames[t.name],
                                          legendgroup=newnames[t.name],
                                          hovertemplate=t.hovertemplate.replace(t.name, newnames[t.name])
                                          ))
    return fig


# ----------------------------------------------------------------------------------------------------------------------

@callback(
    Output(component_id='the_graph', component_property='figure'),
    Input(component_id='xaxis_raditem', component_property='value')
)
def update_graph(scelta):
    # ----------------------------------------SCELGO INDICE A BREVE------------------------------------------------
    if scelta == "Indebitamento a breve":
        breve_barchart['indice indebitam a breve'] = breve_barchart['indice indebitam a breve'].astype(float)
        breve_barchart["indice indebitam a breve"] = breve_barchart["indice indebitam a breve"].round(4)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=breve_barchart.loc[:, "ATECO"],
                             y=breve_barchart.loc[:, "indice indebitam a breve"],
                             name='',
                             marker=dict(
                                 color=breve_barchart["indice indebitam a breve"],
                                 showscale=True,
                                 colorscale=['#011930', '#082b4d', '#1a456e', '#2f5c87', '#497299', ]
                             ),
                             customdata=[breve_barchart.loc[0, "num aziende"], breve_barchart.loc[1, "num aziende"],
                                         breve_barchart.loc[2, "num aziende"], breve_barchart.loc[3, "num aziende"],
                                         breve_barchart.loc[4, "num aziende"], breve_barchart.loc[5, "num aziende"],
                                         breve_barchart.loc[6, "num aziende"], breve_barchart.loc[7, "num aziende"],
                                         breve_barchart.loc[8, "num aziende"], breve_barchart.loc[9, "num aziende"], ],
                             text=breve_barchart.loc[:, "indice indebitam a breve"],
                             hovertemplate='<b>Descrizione:</b> %{x}' +
                                           '<br><b>Indice</b>: %{y}<br>' +
                                           '<b>Num. aziende</b>: %{customdata}',

                             ))

        # fig.add_trace(go.Bar(x=breve_barchart.loc[:, "ATECO"],
        #                      y=breve_barchart.loc[:, "indice indebitam a lungo"],
        #                      name='indice indebitam a lungo',
        #                      marker_color="#37536d",
        #                      text=breve_barchart.loc[:, "num aziende"],
        #                      hovertemplate='<br></br> <b>%{x}</b>' +
        #                                    '<br><b>indice</b>: %{y}<br>' +
        #                                    '<b>num aziende</b>: %{text}',
        #                      ))

        fig.update_layout(
            # title='indice indebitam a breve',
            xaxis_tickfont_size=14,
            xaxis={'visible': False, 'showticklabels': False},
            yaxis=dict(
                titlefont_size=16,
                tickfont_size=14,
            ),

            legend=dict(
                x=1,
                y=1,
                # bgcolor='rgba(255, 255, 255, 0)',
                # bordercolor='rgba(255, 255, 255, 0)',

                # title_font_family="Times New Roman",
                font=dict(
                    # family="Courier",
                    size=12,
                    color="black"
                ),
                bgcolor="#ebeef0",
                bordercolor="#8EA9C1",
                borderwidth=1

            ),
            barmode='group',
            # bargap=0.15,  # gap between bars of adjacent location coordinates.
            # bargroupgap=0.1  # gap between bars of the same location coordinate.
            title={'text': 'Rapporto di indebitamento a Breve periodo',
                   'font': {'size': 18}, 'x': 0.5, 'xanchor': 'center'},
        )

        # breve_barchart['indice indebitam a breve'] = breve_barchart['indice indebitam a breve'].astype(float)
        # breve_barchart['indice indebitam a breve'] = breve_barchart['indice indebitam a breve'].map("{:,.2f}".format)
        # breve_barchart['indice indebitam a lungo'] = breve_barchart['indice indebitam a lungo'].astype(float)
        # breve_barchart['indice indebitam a lungo'] = breve_barchart['indice indebitam a lungo'].map("{:,.2f}".format)

        return fig

    # ----------------------------------------SCELGO INDICE A LUNGO------------------------------------------------
    if scelta == "Indebitamento a lungo":
        lungo_barchart['indice indebitam a lungo'] = lungo_barchart['indice indebitam a lungo'].astype(float)
        lungo_barchart["indice indebitam a lungo"] = lungo_barchart["indice indebitam a lungo"].round(4)

        fig = go.Figure()
        fig.add_trace(go.Bar(x=lungo_barchart.loc[:, "ATECO"],
                             y=lungo_barchart.loc[:, "indice indebitam a lungo"],
                             name='',
                             marker=dict(
                                 color=breve_barchart["indice indebitam a lungo"],
                                 showscale=True,
                                 colorscale=['#497299', '#2f5c87', '#1a456e', '#082b4d', '#011930', ]
                             ),
                             customdata=[lungo_barchart.loc[0, "num aziende"], lungo_barchart.loc[1, "num aziende"],
                                         lungo_barchart.loc[2, "num aziende"], lungo_barchart.loc[3, "num aziende"],
                                         lungo_barchart.loc[4, "num aziende"], lungo_barchart.loc[5, "num aziende"],
                                         lungo_barchart.loc[6, "num aziende"], lungo_barchart.loc[7, "num aziende"],
                                         lungo_barchart.loc[8, "num aziende"], lungo_barchart.loc[9, "num aziende"], ],
                             text=lungo_barchart.loc[:, "indice indebitam a lungo"],
                             hovertemplate='<b>Descrizione:</b> %{x}' +
                                           '<br><b>Indice</b>: %{y}<br>' +
                                           '<b>Num. aziende</b>: %{customdata}',

                             ))
        # fig.add_trace(go.Bar(x=lungo_barchart.loc[:, "ATECO"],
        #                      y=lungo_barchart.loc[:, "indice indebitam a breve"],
        #                      name='indice indebitam a breve',
        #                      marker_color="#37536d",
        #                      text=lungo_barchart.loc[:, "num aziende"],
        #                      hovertemplate='<br></br> <b>%{x}</b>' +
        #                                    '<br><b>indice</b>: %{y}<br>' +
        #                                    '<b>num aziende</b>: %{text}',
        #                      ))
        fig.update_layout(
            # title='indice indebitam a lungo',
            xaxis_tickfont_size=10,
            xaxis={'visible': False, 'showticklabels': False},
            yaxis=dict(
                titlefont_size=16,
                tickfont_size=14,
            ),
            legend=dict(
                x=1,
                y=1,
                # bgcolor='rgba(255, 255, 255, 0)',
                # bordercolor='rgba(255, 255, 255, 0)',

                # title_font_family="Times New Roman",
                font=dict(
                    # family="Courier",
                    size=12,
                    color="black"
                ),
                bgcolor="#ebeef0",
                bordercolor="#8EA9C1",
                borderwidth=1

            ),
            barmode='group',
            # bargap=0.15,  # gap between bars of adjacent location coordinates.
            # bargroupgap=0.1  # gap between bars of the same location coordinate.
            title={'text': 'Rapporto di indebitamento a Lungo periodo',
                   'font': {'size': 18}, 'x': 0.5, 'xanchor': 'center'},
        )
        # lungo_barchart['indice indebitam a breve'] = lungo_barchart['indice indebitam a breve'].astype(float)
        # lungo_barchart['indice indebitam a lungo'] = lungo_barchart['indice indebitam a lungo'].astype(float)
        # lungo_barchart['indice indebitam a breve'] = lungo_barchart['indice indebitam a breve'].map("{:,.2f}".format)
        # lungo_barchart['indice indebitam a lungo'] = lungo_barchart['indice indebitam a lungo'].map("{:,.2f}".format)

        return fig


# ----------------------------------------------------------------------------------------------------------------------
@callback(
    #Output("store-dropdown-value", "data"),
    Output("store", "data"),# children= {dictionary} e riempie datatable
    Input('datatable', 'selected_rows')
    # Input('datatable', 'derived_virtual_row_ids'),
    # selected_row_ids= Indices of selected rows if part of table after filtering

)
def update_graphs(selected_rows):
    # print(selected_rows)
    selected_row = dftable_clear.iloc[selected_rows, 0]
    selectedrow = selected_row

    if selected_row.size != 0:
        selectedrow = selectedrow.iat[0]
        # print(selectedrow)
    else:
        selectedrow = dftable_clear.iloc[0, 0]
        # print(selectedrow)

    # print(type(selectedrow))
    # dfdf = "Commercio al dettaglio di confezioni per bambini e neonati"
    tfile = open(r'pages\files\selectedrow.txt', 'w')
    tfile.write(selectedrow)
    tfile.close()

    return selectedrow

# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
