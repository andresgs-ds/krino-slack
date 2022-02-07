def merge_dict(lista):
    """Funci'on que une diccionarios en uno solo a travez de listas

    Args:
        lista (list): toma como argumdento una lista no vacia!!! que contenga varios diccionarios
    """
    new_dict = {'name':[], 'users':[]}

    for elemento in lista:
        new_dict['name'].append(elemento['name'])
        new_dict['users'].append(elemento['users'])

    return new_dict