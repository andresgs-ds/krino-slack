import pandas as pd
import plotly.express as px  
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import dash_table
import dash_bootstrap_components as dbc
from graphs_slack import *

app = Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])
app.title = 'Dashboard Krino-Slack'
app._favicon = ("K-Logo.png")
server = app.server
# Funciones DataTable

estilo_sombra = {'box-shadow': '0 2px 4px 0 rgba(0, 0, 0, 0.2), 0 3px 10px 0 rgba(0, 0, 0, 0.19)'}


app.layout = html.Div([
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        dbc.Card(
                            dbc.CardBody([
                                html.Div([
                                    html.H1("Krino Tech---Ops Slack Data"),
                                ], style={'textAlign': 'center'}) 
                            ]), style = estilo_sombra
                        ),
                    ])
                ], width=12)
            ], align='center'), 
            html.Br(),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        dbc.Card(
                            dbc.CardBody([
                                dcc.Graph(id='cantidad ticket', figure=fig_cantidad_ticket, config={'displayModeBar': False}) 
                             ]), style = estilo_sombra
                        ),  
                    ]) 
                ], width=3),
                dbc.Col([
                    html.Div([
                        dbc.Card(
                            dbc.CardBody([
                                dcc.Graph(id='duracion-ticket-resueltos', figure=fig_duracion_ticket, config={'displayModeBar': False}) 
                            ]), style = estilo_sombra
                        ),  
                    ])
                ], width=3),
                dbc.Col([
                    html.Div([
                        dbc.Card(
                            dbc.CardBody([
                                dcc.Graph(id='funnel', figure=fig_funnel_ticket, config={'displayModeBar': False}) 
                            ]), style = estilo_sombra
                        ),  
                    ]) 
                ], width=6),
            ], align='center'), 
            html.Br(),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        dbc.Card(
                            dbc.CardBody([
                                dcc.Graph(id='nuevo req ops', figure=fig_duracion_nuevo_req_ops, config={'displayModeBar': False}) 
                            ]), style = estilo_sombra
                        ),  
                    ])
                ], width=3),
                dbc.Col([
                    html.Div([
                        dbc.Card(
                            dbc.CardBody([
                                dcc.Graph(id='urgente ops', figure=fig_duracion_urgente_ops, config={'displayModeBar': False}) 
                            ]), style = estilo_sombra
                        ),  
                    ])
                ], width=3),
                dbc.Col([
                    html.Div([
                        dbc.Card(
                            dbc.CardBody([
                                dcc.Graph(id='nuevo req tech', figure=fig_duracion_nuevo_req_tech, config={'displayModeBar': False}) 
                            ]), style = estilo_sombra
                        ),  
                    ])
                ], width=3),
                dbc.Col([
                    html.Div([
                        dbc.Card(
                            dbc.CardBody([
                                dcc.Graph(id='urgente tech', figure=fig_duracion_urgente_tech, config={'displayModeBar': False}) 
                            ]), style = estilo_sombra
                        ),  
                    ])
                ], width=3),
            ], align='center'),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        dbc.Card(
                            dbc.CardBody([
                                dcc.Graph(id='cantidad ticket urgente ops-tech', figure=fig_cantidad_ticket_urgentes_ops_tech, config={'displayModeBar': False}) 
                            ]), style = estilo_sombra
                        ),  
                    ])
                ], width=6),
                dbc.Col([
                    html.Div([
                        dbc.Card(
                            dbc.CardBody([
                                dcc.Graph(id='cantidad ticket nuevo req ops-tech', figure=fig_cantidad_ticket_req_ops_tech, config={'displayModeBar': False}) 
                            ]), style = estilo_sombra
                        ),  
                    ])
                ], width=6),
            ], align='center'),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        dbc.Card(
                            dbc.CardBody([
                                dcc.Graph(id='ticket abiertos colaboradores', figure=tickets_abiertos_tech_ops, config={'displayModeBar': False})
                            ]), style = estilo_sombra
                        ),  
                    ])
                ], width=6),
                dbc.Col([
                    html.Div([
                        dbc.Card(
                            dbc.CardBody([
                                dcc.Graph(id='ticket resueltos colaboradores', figure=tickets_resueltos_tech_ops, config={'displayModeBar': False}) 
                            ]), style = estilo_sombra
                        ),  
                    ])
                ], width=6),
            ], align='center'),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        dbc.Card(
                            dbc.CardBody([
                                html.Div([
                                    html.H2('Tickets Abiertos')
                                ]),
                                html.Br(),
                                dash_table.DataTable(
                                    id="table",
                                    columns=[{"name": i, "id": i} for i in data_table_dash_app.iloc[:, lambda data_table_dash_app: [0,1,2,3,13]]],
                                    data=data_table_dash_app.to_dict("records"),
                                    style_cell={'textAlign': 'center'},
                                    style_header={
                                        'backgroundColor': 'rgb(30, 30, 30)',
                                        'color': 'white',
                                        'height': 'auto',
                                        'textAlign': 'center'
                                    },
                                    style_data={
                                        'backgroundColor': 'rgb(255, 255, 255)',
                                        'color': 'black',
                                        'whiteSpace': 'normal',
                                        'height': 'auto'
                                    },
                                )  
                            ]), style = estilo_sombra
                        ),  
                    ])
                ], width=12),
            ], align='center'),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        dbc.Card(
                            dbc.CardBody([
                                html.Div([
                                    html.H2('Base de datos ticket Slack tech---ops')
                                ]),
                                html.Br(),
                                dash_table.DataTable(
                                    id="table2",
                                    columns=[{"name": i, "id": i} for i in df_copy],
                                    data=df_copy.to_dict("records"),
                                    sort_action= 'native',
                                    filter_action= 'native',
                                    filter_options={'case':'insensitive'},
                                    page_action="native",
                                    page_current= 0,
                                    page_size= 10,
                                    export_format="csv",
                                    style_data_conditional=[
                                        {
                                        'if': {
                                             'filter_query': '{t_finalizado} eq "True" && {t_resuelto} eq "True" && {t_revisado} eq "True"',
                                             'column_type': 'any',
                                         },
                                        'backgroundColor': '#3D9970',
                                        'color': 'white',
                                        },
                                        {
                                        'if': {
                                             'filter_query': '{t_finalizado} eq "False" && {t_resuelto} eq "True" && {t_revisado} eq "True"',
                                             'column_type': 'any',
                                         },
                                        'backgroundColor': 'yellow',
                                        'color': 'black',
                                        },
                                        {
                                        'if': {
                                             'filter_query': '{t_finalizado} eq "False" && {t_resuelto} eq "False" && {t_revisado} eq "True"',
                                             'column_type': 'any',
                                         },
                                        'backgroundColor': 'tomato',
                                        'color': 'white',
                                        } 
                                    ],
                                    style_cell={'textAlign': 'center',
                                        'backgroundColor': 'rgb(255, 255, 255)',
                                        'color': 'black'},
                                    style_header={
                                        'backgroundColor': 'rgb(30, 30, 30)',
                                        'color': 'white',
                                        'height': 'auto'
                                    },
                                    style_data={
                                        'backgroundColor': 'rgb(255, 255, 255)',
                                        'color': 'black',
                                        'whiteSpace': 'normal',
                                        'height': 'auto'
                                    },
                                    style_table={'overflowX': 'scroll'},
                                    style_filter={
                                        'backgroundColor': 'lightgrey',
                                    }
                                )  
                            ]), style = estilo_sombra
                        ),  
                    ])
                ], width=12),
            ], align='center'),
        ]), color = 'light'
    )
])

if __name__ == "__main__":
    app.run_server(debug=True)