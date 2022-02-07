import pandas as pd
import plotly.express as px  
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import dash_table
import dash_bootstrap_components as dbc
from calculos_graficos_data_slack import *

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# ------------------------------------------------------------------------------

GLOBAL_LAYOUT = dict(
    plot_bgcolor = '#09347a'
)

fig_cantidad_ticket = go.Figure()

fig_cantidad_ticket.add_trace(go.Indicator(
    mode = "number",
    value = df.describe()['Duracion_Ticket_horas']['count'],
    title = {"text": "<span style='font-size:1.5em'>Cantidad de Tickets</span><br><span style='font-size:1.5em'></span><br>"},
    domain = {'x': [1, 1], 'y': [1, 1]}))


fig_funnel_ticket = go.Figure(go.Funnel(
    y = df.columns[6:10] ,
    x = [df.t_revisado.value_counts().loc[True], df.t_resuelto.value_counts().loc[True], df.t_finalizado.value_counts().loc[True]]))

fig_funnel_ticket.update_layout(
    title={
        'text': "<b>Funnel Estado Tickets</b>",
        'xanchor': 'left',
        'yanchor': 'top'},
    plot_bgcolor = 'rgb(31,40,51)')
    

fig_duracion_ticket = go.Figure()

fig_duracion_ticket.add_trace(go.Indicator(
    mode = "number",
    value = df[df['t_resuelto'] == True].describe()['Duracion_Ticket_horas']['mean'],
    number = {'suffix' : ' Horas'},
    title = {"text": "<span style='font-size:1.5em'>Duracion Promedio Tickets Resueltos</span><br><span style='font-size:1.5em'></span><br>"},
    domain = {'x': [1, 1], 'y': [1, 1]}))

fig_duracion_nuevo_req_ops = go.Figure()

fig_duracion_nuevo_req_ops.add_trace(go.Indicator(
    mode = "number",
    value = tickets_req_ops_time[tickets_req_ops_time['t_resuelto'] == True].describe()['Duracion_Ticket_horas']['mean'],
    number = {'suffix' : ' Horas'},
    title = {"text": "<span style='font-size:1.5em'>Duracion Promedio Tickets</span><br><span style='font-size:1.4em'>Nuevo Requerimiento Ops</span><br>"},
    domain = {'x': [1, 1], 'y': [1, 1]}))

fig_duracion_urgente_ops = go.Figure()

fig_duracion_urgente_ops.add_trace(go.Indicator(
    mode = "number",
    value = tickets_ops_time[tickets_ops_time['t_resuelto'] == True].describe()['Duracion_Ticket_horas']['mean'],
    number = {'suffix' : ' Horas'},
    title = {"text": "<span style='font-size:1.5em'>Duracion Promedio Tickets</span><br><span style='font-size:1.4em'>Urgente Ops</span><br>"},
    domain = {'x': [1, 1], 'y': [1, 1]}))

fig_duracion_nuevo_req_tech = go.Figure()

fig_duracion_nuevo_req_tech.add_trace(go.Indicator(
    mode = "number",
    value = tickets_req_tech_time[tickets_req_tech_time['t_resuelto'] == True].describe()['Duracion_Ticket_horas']['mean'],
    number = {'suffix' : ' Horas'},
    title = {"text": "<span style='font-size:1.5em'>Duracion Promedio Tickets</span><br><span style='font-size:1.4em'>Nuevo Requerimiento Tech</span><br>"},
    domain = {'x': [1, 1], 'y': [1, 1]}))

fig_duracion_urgente_tech = go.Figure()

fig_duracion_urgente_tech.add_trace(go.Indicator(
    mode = "number",
    value = tickets_tech_time[tickets_tech_time['t_resuelto'] == True].describe()['Duracion_Ticket_horas']['mean'],
    number = {'suffix' : ' Horas'},
    title = {"text": "<span style='font-size:1.5em'>Duracion Promedio Tickets</span><br><span style='font-size:1.4em'>Urgente Tech</span><br>"},
    domain = {'x': [1, 1], 'y': [1, 1]}))

fig_cantidad_ticket_urgentes_ops_tech = go.Figure(data=[
    go.Bar(name='No Urgente', x=df.columns[10:12], y=[valor_ops - valor_ops_urgente, valor_tech - valor_tech_urgente]),
    go.Bar(name='Urgente', x=df.columns[10:12], y=[valor_ops_urgente, valor_tech_urgente])
])
fig_cantidad_ticket_urgentes_ops_tech.update_layout(barmode='group', title_text='<b>Tickets No Urgentes vs Urgentes Tech-Ops</b>')

fig_cantidad_ticket_req_ops_tech = go.Figure(data=[
    go.Bar(name='Nuevo Requerimiento Ops', x=df.columns[10:11], y=[valor_req_ops]),
    go.Bar(name='Nuevo Requerimiento Tech', x=df.columns[11:12], y=[valor_req - valor_req_ops])
])
fig_cantidad_ticket_req_ops_tech.update_layout(barmode='group', title_text='<b>Tickets Nuevos Requerimientos Tech-Ops</b>')


tickets_resueltos_tech_ops = px.bar(df_count_owner_resueltos, x='ticket_owner', y='Count', title='<b>Tickets Resueltos</b>')

tickets_abiertos_tech_ops = px.bar(df_count_owner_abiertos, x='ticket_owner', y='Count', title='<b>Tickets Abiertos</b>')

# App layout

app.layout = html.Div([
    html.H1("Krino Slack Data", style={'text-align': 'center'}),

    html.Div([
        html.Div([
            dcc.Graph(id='cantidad ticket', figure=fig_cantidad_ticket)
        ], className= 'six columns'),

        html.Div([
            dcc.Graph(id='funnel', figure=fig_funnel_ticket)
        ], className= 'six columns')
    ], className= 'row'),

    dcc.Graph(id='duracion-ticket-resueltos', figure=fig_duracion_ticket),

    html.Div([
        html.Div([
            dcc.Graph(id='nuevo req ops', figure=fig_duracion_nuevo_req_ops)
        ], className= 'six columns'),

        html.Div([
            dcc.Graph(id='urgente ops', figure=fig_duracion_urgente_ops)
        ], className= 'six columns')
    ], className= 'row'),

    html.Div([
        html.Div([
            dcc.Graph(id='nuevo req tech', figure=fig_duracion_nuevo_req_tech)
        ], className= 'six columns'),

        html.Div([
            dcc.Graph(id='urgente tech', figure=fig_duracion_urgente_tech)
        ], className= 'six columns')
    ], className= 'row'),

    html.Div([
        html.Div([
            dcc.Graph(id='cantidad ticket urgente ops-tech', figure=fig_cantidad_ticket_urgentes_ops_tech)
        ], className= 'six columns'),

        html.Div([
            dcc.Graph(id='cantidad ticket nuevo req ops-tech', figure=fig_cantidad_ticket_req_ops_tech)
        ], className= 'six columns')
    ], className= 'row'),

    dcc.Graph(id='ticket resueltos colaboradores', figure=tickets_resueltos_tech_ops),

    dcc.Graph(id='ticketm abiertos colaboradores', figure=tickets_abiertos_tech_ops),

    dash_table.DataTable(
    id="table",
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df[(df['t_revisado'] == False) & (df['t_resuelto'] == False) & (df['t_finalizado'] == False)].to_dict("records"),
    export_format="csv",
    )

])

if __name__ == '__main__':
    app.run_server(debug=True)







