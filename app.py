import dash
from dash import dcc, callback, Output, Input, dash_table  # pip install dash
import dash_labs as dl  # pip install dash-labs
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State, callback, dash_table
from mydata import df

app = dash.Dash(
    __name__, plugins=[dl.plugins.pages],
    # external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

navbar = dbc.NavbarSimple(
    children=[

        html.H2("DASHBOARD PER LA VALUTAZIONE DELLE PERFORMANCE DI SETTORE E AZIENDALI",
                style={'text-align': 'center', 'color': '#606060'}, className="titolo"),

        dcc.Link(html.Button('ANALISI SETTORI'), href="/", className="interno1"),
        dcc.Link(html.Button('ANALISI AZIENDE'), href="/aziende", className="interno2"),
        # dbc.NavItem(dbc.NavLink("ATECO", href="/"), className="interno1"),
        # dbc.NavItem(dbc.NavLink("AZIENDE", href="/tablebutton"), className="interno2"),
        # dbc.DropdownMenu(
        #     children=[
        #         dbc.DropdownMenuItem(page["name"], href=page["path"])
        #         for page in dash.page_registry.values()
        #         if page["module"] != "pages.not_found_404"
        #     ],
        #     in_navbar=True,
        #     label="More",
        # ),
    ],
    # brand="SVILUPPO DI UNA DASHBOARD PER LA VALUTAZIONE DELLE PERFORMANCE DI SETTORE E AZIENDALI",
    className="intestazione"
)

app.layout = dbc.Container(
    [navbar, dl.plugins.page_container,
     #dcc.Store(id="store-dropdown-value", data=None)
     ],
    fluid=True,
)

if __name__ == "__main__":
    app.run_server(debug=True, port=8003,
                   #dev_tools_ui=False, dev_tools_props_check=False
                   )
