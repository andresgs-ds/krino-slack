import numpy as np
import json
import os
import pandas as pd

def json_to_dataframe(path):
    """La funcion toma como argumento el directorio donde se encuentran los archivos .json y los transforma a una dataframe usando pandas. 
    Esta funcion toma todos los archivos .json de la carpeta!!!

    Args:
        path (string): direccion donde se encuentran los archivos .json
    """
    data_list = []
    base_dir = path

    for file in os.listdir(base_dir):
        if 'json' in file:
            json_path = os.path.join(base_dir, file)
            json_data = pd.read_json(json_path, dtype=False)
            data_list.append(json_data)

    return pd.concat(data_list)