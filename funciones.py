#Punto 1: Cargar los archivos .csv y .html
def cargar_dataset(archivo):
    import pandas as pd
    import os
    import numpy as np
    #Si se desea agregar un input se coloca:
    #archivo = input("Por favor, ingresa el nombre del archivo: ")
    extension = os.path.splitext(archivo)[1].lower()
    #Cargar el carchivo según su extención
    if extension == '.csv':
        df = pd.read_csv(archivo)
        return (df)
    elif extension == '.html':
        df = pd.read_html(archivo)
        return(df)
    else:
        raise ValueError(f"Hola, acabas de ingresar un documento que desconozco, con extension: {extension}")

#Punto 2: Sustituir los valores nulos de las variables de:
def reemplazar_nulos(df):
    import pandas as pd
    import os
    import numpy as np
    # Obtener índices primos
    primos = []
    for num in range(len(df.columns)):
        if num > 1 and all(num % div != 0 for div in range(2, int(num**0.5) + 1)):
            primos.append(num)
    
    column_names = df.columns.to_list()
    
    for i in range(len(column_names)):
        col = column_names[i]
        if df[col].dtype in [np.int64, np.float64, np.int32, np.float32]:  # Columnas numéricas
            if i in primos:
                df[col].fillna(1111111, inplace=True)
            else:
                df[col].fillna(1000001, inplace=True)
        else:  # Columnas no numéricas
            df[col].fillna("Valor Nulo", inplace=True)
    
    return df



#Punto 3: Identifica los valores nulos
def cuenta_nulos(df):
    #Valores nulos por columna
    valores_nulos_cols = df.isnull().sum()
    #Valores nulos por dataframe
    valores_nulos_df = df.isnull().sum().sum()
    
    return("Valores nulos por columna", valores_nulos_cols,
            "Valores nulos por dataframe", valores_nulos_df)

#Punto 4: Valores atipicos sustitucion
def limpiar_atipicos(df):
    import pandas as pd
    import os
    import numpy as np
    df_nuevo = df.copy()
    
    for col in df.select_dtypes(include=[np.number]).columns:  # Solo en columnas numéricas
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        
        limite_inferior = Q1 - 1.5 * IQR
        limite_superior = Q3 + 1.5 * IQR
        
        indices = df.index[df[col] < limite_inferior].append(df.index[df[col] > limite_superior])
        for i in indices:
            df_nuevo.loc[i, col] = "Valor Atípico"
    
    return df_nuevo
