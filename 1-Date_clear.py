import os 
import pandas as pd
import numpy as np
import time
from progress.bar import Bar
###----------------------------------------TIEMPO TOTAL DE EJECUCION: 3.5 MINUTOS APROX -----------------------------------###

###--------------------------------------------Tarea 1: Carga de datos-----------------------------------------------------###
# 0-Se creado un work space en vscode para poder trabajar
directory = os.getcwd()
NOTA_0 = "Se ha agregado el paquete progress, dado que la ejecución puede tardar mas de 1 minuto."

# 1-Leyendo el archivo csv y cargandolo con el nombre df en pandas
df = pd.read_csv('Airbnb_Open_Data.csv')

# 2-Visualiza las cinco primeras filas
Total_inicial_filas=len(df)
print("A continuación se muestran los 5 primeros registros y las propiedades de Dataframe:")
print(df.head(5))

# 3-Diferentes formas de mirar las propiedades del df.
print(df.dtypes)
print(df.info())
print(df.columns)
print("\n")
input("Presione ENTER para continuar...")


###------------------------------------------Tarea 2a: Limpieza de datos--------------------------------------------------------###
# 1-Eliminando las columnas no deseadas para realizar el análisis.
df.drop([
        'NAME', 'host id', 'host name', "country", 'country code', 'last review', 'house_rules',
         "number of reviews", "reviews per month"
        ], axis=1, inplace=True)

# 2-Razones por la cual se han eliminado estas columnas. 
Rpta_1="NAME, host id, host name : son campos mas personalizados, que permiten realizar seguimientos mas individuales ( este no es el caso)."
Rpta_2="Country, country code : información redundante, dado que los datos pertenecen al mismo país."
Rpta_3="house_rules: información no clasificable para un tratamiento estadístico"
Rpta_4="last review, number of review y reviews per month: estos campos estas englobados en el parámetro review rate number, que es el indicador."
Razon_columnas_eliminadas = {'NAME':Rpta_1, 'host id':Rpta_1, 'host name':Rpta_1, "country":Rpta_2, 'country code':Rpta_2,
                            'last review':Rpta_4,'house_rules':Rpta_3,"number of reviews":Rpta_4, "reviews per month":Rpta_4
                            }
def Consultar_columna_eliminada(campo): #Función para ingresar nombre de la columna y devolver el motivo por el cual se elimino esta. 
    Motivo_delete=Razon_columnas_eliminadas.get(campo)
    print("Se elimina la columna/s por el siguiente motivo:")
    print(Motivo_delete)
Consultar_columna_eliminada("house_rules")

# 3-Corrigiendo nombres de neighbourhood_group  que estan mal escritos: brookln/manhatan, remplazandolos por Brooklyn/Manhattan
df['neighbourhood group'] = df['neighbourhood group'].replace({"brookln": "Brooklyn", 'manhatan': "Manhattan"})
NOTA_1= "Al existir menos de 250 vecindarios, se ha llevado a cabo la agrupación de vecindarios y la revisión visual, observando que no existen vecindarios mal escritos."
print("Se han corregido los nombre de los grupos de barrios que estaban mal escritos, como brookln por Brooklyn y manhatan por Manhattan")
print("\n")
input("Presione ENTER para continuar...")


###------------------------------------------Tarea 2b: Limpieza de datos-----------------------------------------------------###
# 1-Valores nulos mostrados de forma ascendente.
Valores_nulos=df.isnull().sum().sort_values(ascending=True)
print("A continuación se muestran la cantidad de datos nulos por columna:")
print(Valores_nulos)

for col in df.columns: # Otra forma de comprobar los valores nulos
    Val_Null= df[col].isnull().sum()
    print("La columna " + col + " tiene : " + str(Val_Null) + " valores nulos.")

# 2-Comprobando filas duplicadas y eliminandolas.
Total_filas_duplicadas=df.duplicated().sum() 
print("Existen " + str(Total_filas_duplicadas) + "filas duplicadas")

df.drop_duplicates(inplace=True) 
Total_filas_elim=df.duplicated().sum()
print("El total de filas duplicadas es : " + str(Total_filas_elim))

# 3-Reseteamos la columna de indices para futuros calculos
df.reset_index(inplace=True, drop=True)
print("Se han reseteado correctamente los indices.") 

# 4-Muestra el número total de registros antes y después de eliminar los duplicados.
Total_filas_sin_duplicados=len(df)
print   ("Filas iniciales - filas finales es " + str(Total_inicial_filas)+"-"+str(Total_filas_sin_duplicados) \
        + "=" +str(Total_inicial_filas-Total_filas_sin_duplicados) \
        + " , debe ser igual a "  + str(Total_filas_duplicadas) + " filas duplicadas"
        )
print("\n")
input("Presione ENTER para continuar...")


###------------------------------------------Tarea 2c: Limpieza de datos-------------------------------------------------------------###
# OBSERVACIÓN IMPORTANTE:
NOTA_2="Se ha llenado los campos nulos con No Data, ya que al no disponer de la información, preferimos realizar la estadística descriptiva \
                con los datos reales, ya que el remplazo de valores nulos por medias, modas, etc, puede llevar a conclusiones equivocas."
NOTA_3="En el momento de reaizar los calculos, se omitira el valor No Data en las columnas con variables númericas, y en algún caso en las \
                columnas con variables categoricas, se podría mostrar para ver la cantidad de campos no registrados."

# 1-Rellenando los NULL de la columna review rate number con el valor de cero, ya que es el único campo que se puede poner cero en lugar de Null.
df['review rate number'].fillna(0, inplace=True) 

# 2-Rellenando los NULL de la columna instant_bookable con False, asumimos nulos como falsos al carecer de información confirmada.
df['instant_bookable'].fillna("False", inplace=True) 

# 3-Rellenando los NULL de la columna host_identity_verified con unconfirmed , ya que asumimos que los nulos son no confirmados.
df['host_identity_verified'].fillna("unconfirmed", inplace=True) 

# 4-Cambiando campos booleanos por string
def bollean_string(columna):
    bar = Bar('Processing', max=len(df))
    for j in range(0,len(df)):
        valor_st=str(df[columna][j])
        df[columna][j]=valor_st
        bar.next()
    bar.finish()
inicio_0=time.time()
print(".......................Espere!!!!!......................, convirtiendo valores a strings.")
bollean_string("instant_bookable")
Fin_0=time.time()
tiempor_total_0=Fin_0-inicio_0
print(" Tipo de datos cambiado, tiempo de la ejecución : " + str(round((tiempor_total_0/60),2)) + " minutos.") 
print("\n")
# 5-Rellenando todos los nulos  del df con "No Data"
df.fillna("No Data", inplace=True)

# 6-Comprobando que no existan nulos en el df
Valores_nulos_final=df.isnull().sum().sort_values(ascending=True)
print(" La suma total de los valores nulos por columna ahora es")
print(Valores_nulos_final)
print("\n")
input("Presione ENTER para continuar...")


###------------------------------------------Tarea 3: Transformación de datos-----------------------------------------------------###
# 1-Cambiando el nombre de la columna `availability 365` a `days_booked`.
df.rename(columns={'availability 365': 'days_booked'}, inplace=True)
for columna in df:
    if columna == "days_booked":
        print("Nuevo nombre de la columna availability_365 es days booked")

# 2-Convirtiendo todos los nombres de las columnas a minúsculas y sustituyendo los espacios por un guión bajo "_".
df.columns = [col.lower().replace(" ", "_") for col in df.columns]
print("Nombres actualizados de las comunas sin espacios en blanco:")
print(df.columns)

# 3-Eliminando el signo $ y la coma de las columnas `price` y `service_fee`. Si es necesario, convierte estas dos columnas al tipo de datos adecuado.
NOTA_4="OBSERVACIÓN IMPORTANTE: dado que la columna es un objeto y existen datos númericos y strings, usamos el try para realizar el bucle y saltar los errores."
def remove_dollar_sign(columna):
    bar = Bar('Processing', max=len(df))
    for i in range (0,len(df)):
        try:
            a=df[columna][i].replace("$", "")
            df.loc[i, columna] = a
        except:
            pass
        try:
            a=df[columna][i].replace(",", "")
            df.loc[i, columna] = a
        except:
            pass
        bar.next()
    bar.finish()
inicio=time.time()
print(".......................Espere!!!!!...............,removiendo signo $ y espacios en blanco en columna price y en service fee.")
remove_dollar_sign("price")
remove_dollar_sign("service_fee")
Fin=time.time()
tiempor_total=Fin-inicio
print("$ y espacios removidos, tiempo de la ejecución : " + str(round((tiempor_total/60),2)) + " minutos.")

Dicc_col_df={
            "price":1, "service_fee":1, "lat":1, "long":1, "construction_year":2, "minimum_nights":2,
            "days_booked":2, "calculated_host_listings_count":2, "review_rate_number":2
            }
def convert_col(columna, opcion):
    bar = Bar('Processing', max=len(df))
    for i in range (0,len(df)):
        if opcion == 1:
            try:
                a=float(df[columna][i])
                df.loc[i, columna] = a
            except:
                pass
        if opcion == 2:
            try:
                a=int(df[columna][i])
                df.loc[i, columna] = a
            except:
                pass
        bar.next()
    bar.finish()   
inicio_2=time.time()
print(".......................Espere!!!!!.................,convirtiendo campo a float/int, en 9 columnas.")

for clave, valor in Dicc_col_df.items():
    convert_col(clave, valor)
Fin_2=time.time()
tiempor_total_2=Fin_2-inicio_2
print("Campos cambiados a int/float, tiempo de la ejecución : " + str(round((tiempor_total_2/60),2)) + " minutos.")
input("Presione ENTER para continuar...")


# 4-Cambiando numeros negativos por 1 en las columnas minimun_nights y days_booked.
print(".......................Espere!!!!!......................, cambiando negativos por unos en columna minimun_nights y days_booked.")
def remove_boolean(columna1, columna2):
    bar = Bar('Processing', max=len(df))
    for i in range (0,len(df)):
        try:
            b=df[columna1][i]
            if b < 0:
                df.loc[i, columna1] = 1
        except:
            pass
        try:
            d=df[columna2][i]
            if d < 0:
                df.loc[i, columna2] = 1
        except:
            pass
        bar.next()
    bar.finish()
inicio_3=time.time()
remove_boolean("minimum_nights", "days_booked")
Fin_3=time.time()
tiempor_total_3=Fin_3-inicio_3
print(" Tipo de datos cambiado, tiempo de la ejecución : " + str(round((tiempor_total_3/60),2)) + " minutos.") 
print("\n")
input("Presione ENTER para continuar...")


###------------------------------------------Tarea 4: Busqueda de datos faltantes-----------------------------------------------------###
# 1-Completando campos nulos de la columna nieghbourhood group con datos de otros registros correspondientes al mismo vecindario, lo contrario no se puede hacer.
lista_neighbourhood=df["neighbourhood"].unique()
vecindario_grupoVecindarios={}
def dicc_neight():
    for m in lista_neighbourhood:
        for n in range(0, len(df)):
            com1 = df["neighbourhood"][n]
            com2 = df["neighbourhood_group"][n]
            if com1 != "No Data" and com2 != "No Data":
                vecindario_grupoVecindarios[com1] = com2
        break 
def agregar_valores():
    for z in range (len(df)):
        if (df["neighbourhood_group"][z] == "No Data") and (df["neighbourhood"][z] != "No Data") :
            val_buscar= df["neighbourhood"][z]
            remplazo=vecindario_grupoVecindarios[val_buscar]
            df.loc[z, 'neighbourhood_group'] = remplazo
dicc_neight()
agregar_valores()
print("Se ha rellenado los campos nulos de la columna nieghbourhood group con datos de otros registros correspondientes al mismo vecindario")
print("\n")
input("Presione ENTER para continuar...")


###----------------------- Guardamos el df como un csv modificado para realizar el tratamiento estadístico-------------------------###
print("Espere!!!!!...... exportando df como archivo .csv y .xlsx")
df.to_csv("2-Final_Proyect_modificado.csv")
df.to_excel("3-Final_Proyect_modificado.xlsx", index=False)
print("df exportado como archivo csv y xlsx.")




