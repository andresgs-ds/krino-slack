import numpy as np
import json
import os
import pandas as pd
import re
import datetime
from json_to_dataframe import json_to_dataframe
from merge_dict import merge_dict

#---------------
directorio_archivos_json = 'data_slack/tech_ops_data-07-02-2022/' 
directorio_user_data = 'data_slack/user-data/'

df = json_to_dataframe(directorio_archivos_json) 
#---------------

#---------------
nuevas_columnas_reacciones = ['t_finalizado', 't_revisado', 't_resuelto']

df_columnas_reaccion = df.reindex(columns=df.columns.tolist() + nuevas_columnas_reacciones)
df_columnas_reaccion['reactions'].fillna('', inplace=True)
df_columnas_reaccion = df_columnas_reaccion.reset_index(drop=True)
#--------------

#--------------
# Se creo una lista vacia para almacenar todos los diccionarios de la columna reactions

lista_dict = []

# Se itero la columna reactions para almacenar los respectivos diccionarios usando la funcion anteriormente creada en lista_dict para despues generar un DataFrame con los datos

for i in df_columnas_reaccion.index:
    if df_columnas_reaccion['reactions'][i] != '':
        lista_dict.append(merge_dict(df_columnas_reaccion['reactions'][i]))
    else:
        lista_dict.append({'name': [], 'users': []})

df_reaction_provisoria = pd.DataFrame(lista_dict)
#--------------

#------------------------------------------------------------------------------------------------------------------------------------------
# Se creo una lista con los simbolos de reaccion

simbolos_reaccion = ['white_check_mark', 'eyes', 'raised_hands']

# Se itero la base de datos con el fin de almacenar True's & False's en las respectivas columnas de su reaccion

for i in df_reaction_provisoria.index:
    if simbolos_reaccion[0] in df_reaction_provisoria['name'][i]:
        df_columnas_reaccion['t_finalizado'][i] = True

for i in df_reaction_provisoria.index:
    if simbolos_reaccion[1] in df_reaction_provisoria['name'][i]:
        df_columnas_reaccion['t_revisado'][i] = True

for i in df_reaction_provisoria.index:
    if any(simbolos_reaccion[2] in s for s in df_reaction_provisoria['name'][i]):
        df_columnas_reaccion['t_resuelto'][i] = True

df_columnas_reaccion[['t_finalizado', 't_revisado', 't_resuelto']] = df_columnas_reaccion[['t_finalizado', 't_revisado', 't_resuelto']].fillna(value=False)
#----------------------------------------------------------------------------------------------------------------------------------------------

#---------------------------
# Seleccionamos las columnas utiles del df y ademas se elimnaron las filas duplicadas y se ordenaron segun la fecha y hora de la creacion de primer mensaje. 

df_clean = df_columnas_reaccion[['client_msg_id', 'text', 'user', 'ts', 'thread_ts', 'latest_reply', 't_finalizado', 't_revisado', 't_resuelto']].drop_duplicates().sort_values(['ts'])

df_clean = df_clean[df_clean['ts'] > '1642171431.027300'].reset_index(drop=True) 

# Columnas nuevas a agregar

nuevas_columnas = ['nuevo_req', 'ticket_ops', 'ticket_tech', 'urgente']

df_clean_new_columns = df_clean.reindex(columns=df_clean.columns.tolist() + nuevas_columnas)
df_clean_new_columns['latest_reply'].fillna('', inplace=True)
#--------------------------------------

#--------------------------------------
# Se creo una lista con los simbolos asociado a las nuevas columnas.

simbolos = [':writing_hand:', ':dart:', ':robot_face:',':rotating_light:']

# Se itero el df para asociarle un valor de True or False a las respectivas columnas segun la simbologia del mensaje principal del thread.

for i in df_clean_new_columns.index:
    if df_clean_new_columns['latest_reply'][i] != '':
            for j in range(len(simbolos)):
                if simbolos[j] in df_clean_new_columns['text'][i]:
                    df_clean_new_columns[df_clean_new_columns.columns[9 + j]][i] = True
                else:
                    df_clean_new_columns[df_clean_new_columns.columns[9 + j]][i] = False 

# Cambiar el nombre de la columna user a Owner
df_clean_new_columns = df_clean_new_columns.rename(columns = {'user': 'Owner'}, inplace=False)
#---------------------------------------------

#--------------------------------------------
# Se creo una nueva DF para almacenar en una nueva columna el id de usuario del owner de cada ticket

df_owner = df_clean_new_columns.filter(items=['text', 'Owner', 'ts', 'thread_ts', 'latest_reply'])
df_owner = df_owner[df_owner['text'].str.contains('Owner', flags=re.IGNORECASE)]
columna_owner = df_owner['text']
df_owner['ticket_owner'] = columna_owner.apply(lambda st: st[st.find("@")+1:st.find(">")])
#--------------------------------------------

#-----------------------------------
# escfribir comentario
df_owner_transitoria = pd.merge(df_owner.filter(items=['thread_ts', 'ticket_owner']), df_clean_new_columns, on='thread_ts', how='outer')
#------------------------------------

#------------------------------------
# Se creo el DataFrame para los users
df_users = json_to_dataframe(directorio_user_data)
df_users = df_users[['id', 'name']]

# Cambiar el nombre de la columna id a ticket_owner

df_users = df_users.rename(columns = {'id': 'ticket_owner'}, inplace=False)

# Combinar el df de user con el df original para obtener los nombres de cada mensaje

data_clean1 = pd.merge(df_users, df_owner_transitoria, on='ticket_owner', how='outer')

data_clean1 = data_clean1[(data_clean1['ticket_ops'].notna()) & (data_clean1['ticket_tech'].notna())]
data_clean1 = data_clean1[data_clean1['latest_reply'] != ''].sort_values(['ts']).reset_index(drop=True)
#--------------------------------------

#-------------------------------------
# DataFrame transitoria para anadir la columna user_ticket que hace referencia al que genero el ticket

df_users_tickets = df_users[['ticket_owner', 'name']]
df_users_tickets = df_users_tickets.rename(columns = {'name': 'user_ticket', 'ticket_owner': 'Owner'}, inplace=False)

# Combine el df df_user_tickets con data_clean1 para anadirle la columna user_ticket
data_clean1 = pd.merge(df_users_tickets, data_clean1, on='Owner', how='outer')

# Eliminar columnas redundantes
data_clean1 = data_clean1.drop(['ticket_owner', 'client_msg_id', 'Owner'], axis=1)

# Se tranformo de Unix TimeStamp a Pandas Datetime las columnas ts, thread_ts y latest_reply
data_clean1[['ts', 'thread_ts', 'latest_reply']] = data_clean1[['ts', 'thread_ts', 'latest_reply']].apply(pd.to_datetime, unit='s')

# Agregar nueva columna para encontrar el tiempo que estuvo abierto cada ticket.
data_clean1['Duracion_Ticket_horas'] = (data_clean1.latest_reply - data_clean1.ts) / pd.Timedelta(hours=1)
data_clean1['Duracion_Ticket_horas'] = data_clean1['Duracion_Ticket_horas'].apply(lambda x:round(x,2))

# Ordenar las columnas
data_clean1 = data_clean1[['user_ticket','name','text','ts','thread_ts','latest_reply','t_revisado','t_resuelto','t_finalizado','nuevo_req','ticket_ops','ticket_tech','urgente','Duracion_Ticket_horas']]
data_clean1 = data_clean1.rename(columns = {'name': 'ticket_owner'}, inplace=False)
data_clean1 = data_clean1[data_clean1['text'].notna()].sort_values(['ts']).reset_index(drop=True)

# Exportando la data a excel en formato csv, ya que, en formato xlsx no permite exportarlo por el formato de las fechas
data_clean1.to_csv('data_clean_csv/' + datetime.datetime.now().strftime("data_slack_%Y-%m-%d_%H:%M:%S.csv"), index=False)

