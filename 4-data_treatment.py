import os 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from progress.bar import Bar
# inicio
# importamos nuestro nuevo csv modificado desde la carpeta de trabajo de vscode
df_calc = pd.read_csv('2-Final_Proyect_modificado.csv') 

# Convertimos los datos de la columna instant_bookable a strings.
def bollean_string(columna):
    bar = Bar('Processing', max=len(df_calc))
    for j in range(0,len(df_calc)):
        valor_st=str(df_calc[columna][j])
        df_calc[columna][j]=valor_st
        bar.next()
    bar.finish()
print(".......................Espere!!!!!......................, convirtiendo valores a strings.")
bollean_string("instant_bookable")
print(" Tipo de datos cambiado.")
print("\n") 

###------------------------------------------Tarea 4: Análisis exploratorio de datos ------------------------------------------###

# 1-Tipos de habitaciones disponibles en Airbnb.
lista_tipos_habitacion=df_calc["room_type"].unique() 
print("Tipos de habitación disponible :")
print(lista_tipos_habitacion)
Tipos_habitacion=df_calc['room_type'].value_counts()
print(Tipos_habitacion)
input("Presione ENTER para continuar...")

# 2-Tipo de habitación que se adhiere a una política de cancelación más estricta.
df_room_type_strict=df_calc[df_calc["cancellation_policy"]=="strict"]
tipo_hab_strict= df_room_type_strict['room_type'].value_counts().sort_values(ascending=False)
print("Tipos de habitación con política estricta (nº total por tipo strict) : la primera fila es el room_type que se adhiere a una política de cancelación mas estricta")
print(tipo_hab_strict)
input("Presione ENTER para continuar...")

# 3-Precios por barrio.
df_grlp=df_calc[['neighbourhood', 'price']][df_calc['price'] != "No Data"]
df_grlp["price"] = df_grlp["price"].astype(str).astype(float)
Neighbourhood_prices = df_grlp.groupby('neighbourhood').mean().sort_values(by="neighbourhood", ascending=True)
print("Agrupado de la media de precios por barrio ordenados de forma alfabética :")
for index, row in Neighbourhood_prices.iterrows():
    vale=round(Neighbourhood_prices.iloc[Neighbourhood_prices.index.get_loc(index), 0],2)
    print(index,vale) 
input("Presione ENTER para continuar...")

# 4-grupo de barrios con los alquileres mas caros.
df_grlp_2=df_calc[['neighbourhood_group', 'price']][(df_calc['neighbourhood_group'] != "No Data") & (df_calc['price'] != "No Data") ]
df_grlp_2["price"] = df_grlp_2["price"].astype(str).astype(float)
Neighbourhood_grouped_prices = df_grlp_2.groupby('neighbourhood_group').mean().sort_values(by="price", ascending=False)
print("Grupo de vecindarios ordenados por la media de precios, el grupo con los alquileres mas caros es:")
print(Neighbourhood_grouped_prices.head(1))
print("\n")
input("Presione ENTER para continuar...")

###--------------------------------------- Tarea 5a: Visualización de datos--------------------------------------------------------###

# 1-Los 10 barrios más caros (precio ascendente)(gráfico de barras horizontales).
Neighbourhood_prices_ascending = df_grlp.groupby('neighbourhood').mean().sort_values(by="price", ascending=False)
print("El barrio mas barato es :")
print(Neighbourhood_prices_ascending[-1:])
Neighbourhood_prices_top10=Neighbourhood_prices_ascending[:10].sort_values(by="price", ascending=True)

plt.figure(figsize=(14,6), dpi=80)
sns.barplot(data=Neighbourhood_prices_top10, x='price', y='neighbourhood', errorbar=None, palette="Blues_d") 
plt.xticks(rotation=45)
plt.yticks(rotation=35)
plt.xlabel("Precio del alquiler ($)")
plt.ylabel("Vecindarios de EEUU")
plt.title("10 Barrios con el alquiler de habitación mas caro según la media de precios", fontdict = {'fontsize': 14,'fontweight': 'bold', 'color': '#5A1FCC'})
plt.show()
print("\n")

# 2-Barrios que ofrecen alquileres a corto plazo de menos de 10 días (gráfico de barras verticales).
    # Suponemos que el corto plazo viene determinado por instant_bookable y los días por minimum_nights
df_grlp_3=df_calc[['neighbourhood', 'instant_bookable', 'minimum_nights']] [(df_calc['neighbourhood'] != "No Data") &
                                                                            (df_calc['instant_bookable'] == "True") &
                                                                            (df_calc['minimum_nights'] != "No Data")
                                                                            ]
df_grlp_3["minimum_nights"] = df_grlp_3["minimum_nights"].astype(str).astype(int)
df_grlp_3=df_grlp_3[['neighbourhood', 'minimum_nights']][df_grlp_3['minimum_nights']<10]
alquileres_corto_plazo = df_grlp_3.groupby('neighbourhood').count().sort_values(by="minimum_nights", ascending=False).head(25)
print(alquileres_corto_plazo)
plt.rcParams.update({'font.size': 6})
alquileres_corto_plazo.plot(kind= 'bar', figsize=(14,6))
plt.xlabel('Vecindario')
plt.ylabel('nº de habitaciones')
plt.xticks(rotation=90)
#plt.yticks(rotation=30)
plt.title('Alquileres por vecindario con reserva instantanea y mínimo de noches menor a 10 días', fontdict = {'fontsize': 12,'fontweight': 'bold', 'color': '#5A1FCC'})
plt.show()

# 3-Precios con respecto al tipo de habitación (gráfico de barras).
df_grlp_4=df_calc[['room_type', 'price']][df_calc['price'] != "No Data"]
df_grlp_4["price"] = df_grlp_4["price"].astype(str).astype(float)
precios_tipo_habitacion = df_grlp_4.groupby('room_type').mean().sort_values(by="price", ascending=True)
print(precios_tipo_habitacion)

plt.figure(figsize=(10,6), dpi=80)
sns.barplot(data=precios_tipo_habitacion, x='room_type', y='price', errorbar=None, hue="room_type") 
#plt.xticks(rotation=45)
#plt.yticks(rotation=35)
plt.xlabel('Tipo de habitación')
plt.ylabel('Media de precios ($)')
plt.title('Media de precios de alquiler de habitación según su tipo', fontdict = {'fontsize': 14,'fontweight': 'bold', 'color': '#5A1FCC'})
plt.show()
print("\n")

# 4-Distribución de los días reservados para cada grupo de barrios (gráfico circular).
df_grlp_5=df_calc[['neighbourhood_group', 'days_booked']][(df_calc['neighbourhood_group'] != "No Data") &
                                                                            (df_calc['days_booked'] != "No Data")  
                                                                            ]
df_grlp_5["days_booked"] = df_grlp_5["days_booked"].astype(str).astype(int)
DiasLibres_grupo_vec = df_grlp_5.groupby('neighbourhood_group').sum().sort_values(by="days_booked", ascending=True)
Lista_ag_vec=[]
Lista_ag_days=[]
for index, row in DiasLibres_grupo_vec.iterrows():
    val=DiasLibres_grupo_vec.iloc[DiasLibres_grupo_vec.index.get_loc(index), 0]
    Lista_ag_vec.append(index)
    Lista_ag_days.append(val)

Total_dias_libres = Lista_ag_days
Grupo_vecindario = Lista_ag_vec
plt.figure(figsize=(8, 6))
plt.pie(Total_dias_libres, labels=Grupo_vecindario, autopct="%0.1f %%")
plt.axis("equal")
plt.title("Distribución anual del total de los días reservados por grupo de barrio", fontdict = {'fontsize': 14,'fontweight': 'bold', 'color': '#5A1FCC'})
plt.show()
print("\n")

#-------------------------------------------------Tarea 5b: Visualización de datos-----------------------------------------------------#

# 1-Impacto entre el precio del servicio y el precio de la habitación (gráfico de dispersión).
df_grlp_6=df_calc[['room_type','service_fee', 'price']][df_calc['price'] != "No Data"][df_calc['service_fee'] != "No Data"]
df_grlp_6["price"] = df_grlp_6["price"].astype(str).astype(float)
df_grlp_6["service_fee"] = df_grlp_6["service_fee"].astype(str).astype(float)

plt.figure(figsize=(12, 6))
sns.scatterplot(data=df_grlp_6, x='service_fee', y='price', hue='room_type', s=36)
plt.xlabel('Tarifa de limpieza ($)')
plt.ylabel('Precio de la habitación ($)')
plt.title('Relación entre la tarifa de limpieza y el precio de la habitación', fontdict = {'fontsize': 14,'fontweight': 'bold', 'color': '#5A1FCC'}) 
plt.show()

correlation = df_grlp_6['service_fee'].corr(df_grlp_6['price'])
print('Coeficiente de correlación: ', correlation)

# 2-Distribución de construcción de habitaciones por año (gráfico de líneas).
# cada habitación tiene asignada una id única, ya que un mismo lugar tiene varia habitaciones.
df_grlp_7=df_calc[['construction_year', 'id']][df_calc['construction_year'] != "No Data"]
Habitaciones_x_agno = df_grlp_7.groupby('construction_year').count().sort_values(by="construction_year")

plt.figure(figsize=(12, 6))
sns.lineplot(data=Habitaciones_x_agno)
plt.xlabel('Año de construcción')
plt.ylabel('Habitaciones construidas')
plt.title('Cantidad total de habitaciones habilitadas por año', fontdict = {'fontsize': 14,'fontweight': 'bold', 'color': '#5A1FCC'})
plt.xticks(rotation=35)
plt.show()
print("\n")

###-----------------------------------------------Tarea 5c: Visualización de datos-------------------------------------------------###

# 1-Efecto del número de tasa de revisión en el precio (gráfico de caja).
df_grlp_8=df_calc[['review_rate_number', 'price']][df_calc['price'] != "No Data"]
df_grlp_8["price"] = df_grlp_8["price"].astype(str).astype(float)
plt.figure(figsize=(8, 6))
sns.boxplot(x='review_rate_number', y='price', data=df_grlp_8)
plt.xlabel('review_rate_number')
plt.ylabel('Precio del alquiler de habitación ($)')
plt.title('Efecto del número de tasa de revisión en el precio', fontdict = {'fontsize': 14,'fontweight': 'bold', 'color': '#5A1FCC'})
plt.show()

# 2-Efecto de la identidad del host verificada en el precio (gráfico de caja).
df_grlp_9=df_calc[['host_identity_verified', 'price']][df_calc['price'] != "No Data"]
df_grlp_9["price"] = df_grlp_9["price"].astype(str).astype(float)

plt.figure(figsize=(8, 6))
sns.boxplot(x='host_identity_verified', y='price', data=df_grlp_9)
plt.xlabel('Identidad del anfitrion')
plt.ylabel('Precio del alquiler de la habitación ($)')
plt.title('Efecto de la verificación de identidad del anfitrión en el precio', fontdict = {'fontsize': 12,'fontweight': 'bold', 'color': '#5A1FCC'})
plt.show()

# 3-Calculando los cuartiles.
df_grlp_10=df_calc[['host_identity_verified', 'price']][df_calc['price'] != "No Data"][df_calc['host_identity_verified'] != "verified"]
df_grlp_11=df_calc[['host_identity_verified', 'price']][df_calc['price'] != "No Data"][df_calc['host_identity_verified'] != "unconfirmed"]
df_grlp_10["price"] = df_grlp_10["price"].astype(str).astype(float)
df_grlp_11["price"] = df_grlp_11["price"].astype(str).astype(float)

print(df_grlp_10["price"].quantile([.25, .5, .75, 1]))
print(df_grlp_11["price"].quantile([.25, .5, .75, 1]))
print("\n")
# 4-Calculando la ecuación de la recta correspondiente a la gráfica de la dependencia de variables (Price/service_fee)
x = df_grlp_6["service_fee"]
y = df_grlp_6["price"]
slope, intercept = np.polyfit(x, y, 1)
pendiente = slope
X_media=x.mean()
y_media=y.mean()
ordenada_origen = y_media - slope * X_media
print(f"La ecuación de la recta de las variables dependientes price/service_fee es:  price = '{round(slope,2)}' x service_fee + '{round(ordenada_origen,2)}'")
print(f"Podemos afirmar que es precio del servicio de habitaciones es un '{round((100/slope),0)}'% del precio del alquiler.")



