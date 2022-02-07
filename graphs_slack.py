import pandas as pd
import plotly.express as px  
import plotly.graph_objects as go
from calculos_graficos_data_slack import *

fig_cantidad_ticket = go.Figure()

fig_cantidad_ticket.add_trace(go.Indicator(
    mode = "number",
    value = df.describe()['Duracion_Ticket_horas']['count'],
    title = {"text": "<span style='font-size:1.5em'>Cantidad de Tickets</span><br><span style='font-size:1.5em'></span><br>"},
    domain = {'x': [1, 1], 'y': [1, 1]}))

fig_cantidad_ticket.update_layout(
    template='plotly_dark',
    plot_bgcolor = 'rgba(0,0,0,0)',
    paper_bgcolor= 'rgba(0, 0, 0, 0)')

fig_funnel_ticket = go.Figure(go.Funnel(
    y = df.columns[6:10] ,
    x = [df.t_revisado.value_counts().loc[True], df.t_resuelto.value_counts().loc[True], df.t_finalizado.value_counts().loc[True]]))

fig_funnel_ticket.update_layout(
    title={
        'text': "<b>Funnel Estado Tickets</b>",
        'xanchor': 'left',
        'yanchor': 'top'},
    template='plotly_dark',
    plot_bgcolor = 'rgba(0,0,0,0)',
    paper_bgcolor= 'rgba(0, 0, 0, 0)')
    
    

fig_duracion_ticket = go.Figure()

fig_duracion_ticket.add_trace(go.Indicator(
    mode = "number",
    value = df[df['t_resuelto'] == True].describe()['Duracion_Ticket_horas']['mean'],
    number = {'suffix' : ' Horas'},
    title = {"text": "<span style='font-size:1.5em'>Duracion Promedio</span><br><span style='font-size:1.5em'>Tickets Resueltos</span><br>"},
    domain = {'x': [1, 1], 'y': [1, 1]}))

fig_duracion_ticket.update_layout(
    template='plotly_dark',
    plot_bgcolor = 'rgba(0,0,0,0)',
    paper_bgcolor= 'rgba(0, 0, 0, 0)')

fig_duracion_nuevo_req_ops = go.Figure()

fig_duracion_nuevo_req_ops.add_trace(go.Indicator(
    mode = "number",
    value = tickets_req_ops_time[tickets_req_ops_time['t_resuelto'] == True].describe()['Duracion_Ticket_horas']['mean'],
    number = {'suffix' : ' Horas'},
    title = {"text": "<span style='font-size:1.5em'>Duracion Promedio Tickets</span><br><span style='font-size:1.4em'>Nuevo Requerimiento Ops</span><br>"},
    domain = {'x': [1, 1], 'y': [1, 1]}))

fig_duracion_nuevo_req_ops.update_layout(
    template='plotly_dark',
    plot_bgcolor = 'rgba(0,0,0,0)',
    paper_bgcolor= 'rgba(0, 0, 0, 0)')

fig_duracion_urgente_ops = go.Figure()

fig_duracion_urgente_ops.add_trace(go.Indicator(
    mode = "number",
    value = tickets_ops_time[tickets_ops_time['t_resuelto'] == True].describe()['Duracion_Ticket_horas']['mean'],
    number = {'suffix' : ' Horas'},
    title = {"text": "<span style='font-size:1.5em'>Duracion Promedio Tickets</span><br><span style='font-size:1.4em'>Urgente Ops</span><br>"},
    domain = {'x': [1, 1], 'y': [1, 1]}))

fig_duracion_urgente_ops.update_layout(
    template='plotly_dark',
    plot_bgcolor = 'rgba(0,0,0,0)',
    paper_bgcolor= 'rgba(0, 0, 0, 0)')

fig_duracion_nuevo_req_tech = go.Figure()

fig_duracion_nuevo_req_tech.add_trace(go.Indicator(
    mode = "number",
    value = tickets_req_tech_time[tickets_req_tech_time['t_resuelto'] == True].describe()['Duracion_Ticket_horas']['mean'],
    number = {'suffix' : ' Horas'},
    title = {"text": "<span style='font-size:1.5em'>Duracion Promedio Tickets</span><br><span style='font-size:1.4em'>Nuevo Requerimiento Tech</span><br>"},
    domain = {'x': [1, 1], 'y': [1, 1]}))

fig_duracion_nuevo_req_tech.update_layout(
    template='plotly_dark',
    plot_bgcolor = 'rgba(0,0,0,0)',
    paper_bgcolor= 'rgba(0, 0, 0, 0)')

fig_duracion_urgente_tech = go.Figure()

fig_duracion_urgente_tech.add_trace(go.Indicator(
    mode = "number",
    value = tickets_tech_time[tickets_tech_time['t_resuelto'] == True].describe()['Duracion_Ticket_horas']['mean'],
    number = {'suffix' : ' Horas'},
    title = {"text": "<span style='font-size:1.5em'>Duracion Promedio Tickets</span><br><span style='font-size:1.4em'>Urgente Tech</span><br>"},
    domain = {'x': [1, 1], 'y': [1, 1]}))

fig_duracion_urgente_tech.update_layout(
    template='plotly_dark',
    plot_bgcolor = 'rgba(0,0,0,0)',
    paper_bgcolor= 'rgba(0, 0, 0, 0)')

fig_cantidad_ticket_urgentes_ops_tech = go.Figure(data=[
    go.Bar(name='No Urgente', x=df.columns[10:12], y=[valor_ops - valor_ops_urgente, valor_tech - valor_tech_urgente]),
    go.Bar(name='Urgente', x=df.columns[10:12], y=[valor_ops_urgente, valor_tech_urgente])
])
fig_cantidad_ticket_urgentes_ops_tech.update_layout(barmode='group',
                                                    title_text='<b>Tickets No Urgentes vs Urgentes Tech-Ops</b>',
                                                    template='plotly_dark',
                                                    plot_bgcolor='rgba(0,0,0,0)',
                                                    paper_bgcolor='rgba(0,0,0,0)')

fig_cantidad_ticket_req_ops_tech = go.Figure(data=[
    go.Bar(name='Nuevo Requerimiento Ops', x=df.columns[10:11], y=[valor_req_ops]),
    go.Bar(name='Nuevo Requerimiento Tech', x=df.columns[11:12], y=[valor_req - valor_req_ops])
])
fig_cantidad_ticket_req_ops_tech.update_layout(barmode='group',
                                                title_text='<b>Tickets Nuevos Requerimientos Tech-Ops</b>', 
                                                template='plotly_dark',
                                                plot_bgcolor='rgba(0,0,0,0)',
                                                paper_bgcolor='rgba(0,0,0,0)')


tickets_resueltos_tech_ops = px.bar(df_count_owner_resueltos, x='ticket_owner', y='Count', title='<b>Tickets Resueltos</b>')
tickets_resueltos_tech_ops.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)', 'template': 'plotly_dark'})

tickets_abiertos_tech_ops = px.bar(df_count_owner_abiertos, x='ticket_owner', y='Count', title='<b>Tickets Abiertos</b>')
tickets_abiertos_tech_ops.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)', 'template': 'plotly_dark'})

data_table_dash_app = df[(df['t_revisado'] == False) & (df['t_resuelto'] == False) & (df['t_finalizado'] == False)]


