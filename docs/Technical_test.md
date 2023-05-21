# Prueba Técnica

## Alcance del proyecto y captura de datos

### **Fuentes**
Para el desarrollo de la prueba, consideré utilizar un data set relacionado a los precios y volúmenes de pares en el mercado de divisas.

El dataset lo conseguí en este [link](https://www.kaggle.com/datasets/mathurinache/dukascopy-forex-tick-data-20082019). Este cuenta con 65 GB de información pero solamente seleccioné 2 archivos de dos pares de divisas (2 del EURUSD y 2 del GBPUSD) del año 2019.

Son archivos csv donde cada uno tiene un poco más de un millón de filas. Así, cada archivo se considerará como una fuente.

Como esta información es antigua, utilizaré adicionalmente 2 API's relacionadas con el mismo tema.

Las fuentes serán:

LISTAR FUENTES FINALES

La idea es que con los archivos csv se haga una carga inicial de muestra del pipeline y posteriormente se empezarán a consumir las API's para tener la información más actualizada.

### **Uso final**
Para este tipo de datos, las columnas disponibles y la categoría, voy a generar unas tablas de análisis.

Las tablas, por ahora, estarán relacionadas con indicadores técnicos de trading.

Se crearían dos tablas, una para una media móvil simple de 5 días y la segunda para un RSI (Relative Strength Index).

Estos indicadores en el día a día, permiten tomar decisiones de inversión sobre los activos o divisas.

Estos datos de los indicadores se pueden utilizar posteriormente para graficarse y así tomar las decisones.

---
## **Análisis Exploratorio de los Datos**
Los archivos contienen las siguientes columnas:
- UTC (fecha en formato '%Y-%m-%dT%H:%M:%S.%f%z')
- Ask Price
- Bid Price
- Ask Volume
- Bid Volume

En una exploración inicial por los archivos csv, encontré que el único problema es el formato de la fecha.

Se encuentra en UTC por lo que se debería hacerle una transformación inicial para ajustarlo a los campos del modelo.

Respecto a los otros campos no se encontraron inconsistencias pero sería necesario que los campos de los precios no estuvieran vacíos por lo que son insumo necesario en el cálculo de las tablas finales.

Para estandarizar el formato de fecha al modelo, se deberían seguir los siguientes pasos:

1. Leer el archivo csv ya sea con pandas o pyspark.
2. Crear un nuevo dataframe en base al handler del paso anterior, adicionando las columnas de timestamp, day, month, y year.
3. Obtener la columna específicamente del UTC con el comando respectivo para la librería utilzada.
4. Aplicar el método fecha = datetime.strptime(&lt;Fecha original&gt;, '%Y-%m-%dT%H:%M:%S.%f%z') donde el primer argumento es la fecha como str (String) y el segundo el formato en el cuál esta.
5. Aplicar el método fecha.timestamp y los atributos fecha.day, fecha.month, fecha.year para obtener los valores respectivos.
6. Guardar estos valores junto con los datos originales en el dataframe creado en el paso 2.

Respecto a los precios de Ask y Bid, sacaré un promedio con estos valores y las columnas de Volume se eliminarán.

---
## **Definir Modelo de Datos**
### **Modelo**
![modelo_de_datos](./img/modelo_de_datos.png)

Es un modelo estrella sencillo que se ajusta a los datos porque no contienen más niveles de jerarquía después del ticker o la fecha.

Inicialmente consideré tener una tercera dimensión que se llamaría "Side Dimension", la cual contendría los valores y nombres para el tipo de precio (Bid y Ask), pero lo descarté porque me generaría llaves primarias duplicadas en la tabla de hechos para la dimensión de la fecha. Es decir, aparecería un date_timestamp para el ask y un date_timestamp para el bid, porque provienen de la misma línea en la fuente.

En el gráfico se distinguen las capas de Integration y Presentation.

### **Arquitectura**
Para este modelo, consideré tener 4 capas:
- Raw: Solamente aplicará para los archivos csv crudos como se obtuvieron del dataset.
- Staging: Consistirá de una base de datos donde se tendrán tablas separadas por fuente y por ticker.
    - Los datos de los archivos csv se cargarán a su respectiva tabla solamente eliminando las columnas del volúmen.
    - Los datos de las API's se cargarán a sus respectivas tablas, con la información como proviene de la respuesta al request.
- Integration: Se harán las primeras transformaciones para la limpieza de los datos:
    - Estandarización de las fechas.
    - Promedio de los precios bid y ask para las tablas provenientes de los csv.
- Presentation: Se harán las transformaciones y cálculos necesarios para obtener los indicadores mencionados en el [uso final](#uso-final). Esta será la capa final y la que estaría disponible para construir gráficos y ejecutar análisis para tomar las decisiones de inversión.