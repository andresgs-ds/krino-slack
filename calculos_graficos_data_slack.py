import pandas as pd
from df_variable import *

# Tiempo Duracion Ticket Urgente - Ops

tickets_ops = df[df['urgente'] == True]

tickets_ops_time = tickets_ops[tickets_ops['ticket_ops'] == True]

valor_ref_ops = df_old[df_old['urgente'] == True]

valor_ref_ops_time = valor_ref_ops[valor_ref_ops['ticket_ops'] == True]

# Tiempo Duracion Ticket Urgente - Tech

tickets_tech = df[df['urgente'] == True]

tickets_tech_time = tickets_tech[tickets_tech['ticket_tech'] == True]

valor_ref_tech = df_old[df_old['urgente'] == True]

tickets_ref_tech_time = valor_ref_tech[valor_ref_tech['ticket_tech'] == True]

# Tiempo Duracion Ticket Nuevo Requerimiento - Ops

tickets_req_ops = df[df['nuevo_req'] == True]

tickets_req_ops_time = tickets_req_ops[tickets_req_ops['ticket_ops'] == True]

valor_ref_req_ops = df_old[df_old['nuevo_req'] == True]

valor_ref_req_ops_time = valor_ref_req_ops[valor_ref_req_ops['ticket_ops'] == True]

# Tiempo Duracion Ticket Nuevo Requerimiento - Tech

tickets_req_tech = df[df['nuevo_req'] == True]

tickets_req_tech_time = tickets_req_tech[tickets_req_tech['ticket_tech'] == True]

valor_ref_req_tech = df_old[df_old['nuevo_req'] == True]

valor_ref_req_tech_time = valor_ref_req_tech[valor_ref_req_tech['ticket_tech'] == True]

# Se calcularon la cantidad de tickets Urgentes recibidos por Tech y Ops

valor_ops = df.ticket_ops.value_counts().loc[True]
df_suma_provisoria_ops = df[['ticket_ops', 'urgente']]
df_suma_provisoria_ops['suma'] = df[['ticket_ops', 'urgente']].sum(1)
valor_ops_urgente =df_suma_provisoria_ops['suma'].value_counts().loc[2.0]

# escribir comentario

valor_tech = df.ticket_tech.value_counts().loc[True]
df_suma_provisoria_tech = df[['ticket_tech', 'urgente']]
df_suma_provisoria_tech['suma'] = df[['ticket_tech', 'urgente']].sum(1)
valor_tech_urgente = df_suma_provisoria_tech['suma'].value_counts().loc[2.0]

# Se calcularon la cantidad de Nuevos Requerimientos recibidos por Tech y Operaciones

valor_req = df.nuevo_req.value_counts().loc[True]
df_suma_provisoria_req = df[['nuevo_req','ticket_ops']]
df_suma_provisoria_req['suma'] = df[['nuevo_req','ticket_ops']].sum(1)
valor_req_ops =df_suma_provisoria_req['suma'].value_counts().loc[2.0]

# Se calcularon la cantidad de tickes resueltos por colaborador

tickets_resueltos = df[df['t_resuelto'] == True]
df_count_owner_resueltos = tickets_resueltos['ticket_owner'].value_counts().to_frame().reset_index()
df_count_owner_resueltos = df_count_owner_resueltos.rename(columns= {'index': 'ticket_owner', 'ticket_owner': 'Count'}, inplace= False)

# Se calcularon la cantidad de tickes abiertos por colaborador

tickets_abiertos = df[(df['t_resuelto'] == False) & (df['t_finalizado'] == False)]
df_count_owner_abiertos = tickets_abiertos['ticket_owner'].value_counts().to_frame().reset_index()
df_count_owner_abiertos = df_count_owner_abiertos.rename(columns= {'index': 'ticket_owner', 'ticket_owner': 'Count'}, inplace= False)

# Se calcularon la cantidad de tickes Creados por colaborador

tickets_creados = df
df_count_ticket_creados = tickets_creados['user_ticket'].value_counts().to_frame().reset_index()
df_count_ticket_creados = df_count_ticket_creados.rename(columns= {'index': 'user_ticket', 'user_ticket': 'Count'}, inplace= False)

