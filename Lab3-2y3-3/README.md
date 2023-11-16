# LAB 3-2 y 3-3: Implementación de un Data Warehouse con BigQuery.

| Información |  |
| --- | --- |
| Materia | Tópicos especiales en Telemática |
| Curso | ST0263 |
| Estudiante | Santiago Puerta (mailto:spuertaf@eafit.edu.co) |
| Profesor | Edwin Nelson Montoya Munera (mailto:emontoya@eafit.edu.co) |

# 1. Objetivo

Implementar un Data Warehouse con BigQuery.

---

# 2. Aspectos solucionados y no solucionados

- [x]  Creación de un bucket de GCP Cloud Storage.
- [x]  Subir datos a un bucket de Cloud Storage.
- [x]  Creación de un conjunto de datos y una tabla en BigQuery.
- [x]  Auto inferencia del esquema de los datos almacenados en Cloud Storage.
- [x]  Realizar consultas SQL por medio de BigQuery a  los datos almacenados en Cloud Storage.

---

# 5. Ambiente de ejecución

## Guía de uso

### Parte 1: Preparando lo necesario

Nota: 

1. Primeramente deberemos de descargar el archivo ‘[😾 data.zip’ y](https://github.com/spuertaf/spuertaf-st0263/blob/main/Lab3-2y3-3/data.zip) seleccionar el botón ‘Download raw file’:
    
    ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-2y3-3/img/Untitled.png)
    
2. Una vez descargado el archivo se deberá de descomprimir el mismo.

---

### Parte 2: Creación de un bucket de GCP Cloud Storage

1. Entrar a la consola de GCP y buscar el servicio ‘Cloud Storage’:
    
    ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-2y3-3/img/Untitled%201.png)
    
2. En la sección ‘Buckets’ seleccionar el botón ‘CREAR’:
    
    ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-2y3-3/img/Untitled%202.png)
    
3. Asigna un nombre al bucket y dirígete a la sección ‘Elige donde almacenar tus datos’; una vez allí, selecciona el campo ‘Región’  seguido por la opción ‘us-central1 (Iowa)’:
    
    ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-2y3-3/img/Untitled%203.png)
    
    1. Finalmente, selecciona el botón ‘CREAR’.
    
    ✅ ¡Listo! Ya posee un bucket de GCP Cloud Storage
    
    ---
    
    ### Parte 3: Subiendo datos a su bucket de Cloud Storage
    
    1. Entrar a la consola de GCP y buscar el servicio ‘Cloud Storage’.
    2. Seleccionar el nombre del bucket creado anteriormente:
        
        ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-2y3-3/img/Untitled%204.png)
        
    3. Seleccionar el botón ‘SUBIR ARCHIVOS’.
    4.  Buscar la carpeta descargada y descomprimida en la ‘Parte 1: Preparando lo necesario’ y seleccionar las diferentes particiones:
        
        ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-2y3-3/img/Untitled%205.png)
        
    
    ✅ ¡Listo! Ya ha podido subir datos a su bucket de Cloud Storage.
    
    ---
    
    ### Parte 4: Creación de un conjunto de datos y una tabla en BigQuery.
    
    1. Entrar a la consola de GCP y buscar el servicio ‘Big Query’:
        
        ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-2y3-3/img/Untitled%206.png)
        
    2. En el apartado con el nombre de su proyecto seleccione los tres (3) puntos; posteriormente, seleccione la opción ‘Crear un conjunto de datos’:
        
        ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-2y3-3/img/Untitled%207.png)
        
    3. Asígnele un nombre al conjunto de datos; dirigite a la sección ‘Región’ y selecciona el campo ‘us-central1 (Iowa)’; finalmente, seleccione el botón ‘CREAR CONJUNTO DE DATOS’:
        
        ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-2y3-3/img/Untitled%208.png)
        
    4. En el apartado con el nombre del conjunto de datos anteriormente creado seleccione la opción ‘Crear tabla’:
        
        ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-2y3-3/img/Untitled%209.png)
        
    5. En el campo ‘Crear tabla desde’ seleccione la opción ‘Google Cloud Storage’; seguidamente, en el campo ‘Selecciona un archivo del bucket de GCS o usa un patrón de URI’ seleccione la opción ‘EXPLORAR’, busque el nombre del bucket creado en la ‘Parte 2: Creación de un bucket de GCP Cloud Storage’ y seleccione uno (1) de los archivos cargados en la ‘Parte 3: Subiendo datos a su bucket de Cloud Storage’; finalmente, seleccione el botón ‘SELECCIONAR’:
        
        ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-2y3-3/img/Untitled%2010.png)
        
        ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-2y3-3/img/Untitled%2011.png)
        
    6. Borre todo el nombre del archivo a excepción de su extensión del campo ‘Selecciona un archivo del bucket de GCS o usa un patrón de URI’ y antes de su respectiva extensión inserte un asterisco (*):
        
        ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-2y3-3/img/Untitled%2012.png)
        
    7. Asígnele un nombre a su tabla en el campo ‘Tabla’ y en el campo ‘Tipo de tabla’ seleccione la opción ‘Tabla externa’:
        
        ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-2y3-3/img/Untitled%2013.png)
        
    8. En el apartado ‘Esquema’ marcar con ‘✅ check’ la casilla ‘Detección automática’; finalmente, seleccionar el botón ‘CREAR TABLA’:
        
        ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-2y3-3/img/Untitled%2014.png)
        
    
    ✅ ¡Listo! Ha podido crear exitosamente una tabla de BigQuery que apunta a los datos presente en un bucket de Cloud Storage.
    
    ---
    
    ### Parte 5: El auto inferido de los datos de BigQuery
    
    1. Entrar a la consola de GCP y buscar el servicio ‘Big Query’.
    2. En el apartado con el nombre de su proyecto seleccione el conjunto de datos y la tabla anteriormente creados en la ‘Parte 4: Creación de un conjunto de datos y una tabla en BigQuery’:
        
        ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-2y3-3/img/Untitled%2015.png)
        
    
    ‼️ Nota: BigQuery infiere automáticamente el esquema de los datos dados, el mismo, se puede ver en la sección ‘ESQUEMA’.
    
    ✅ ¡Listo! Ya sabe como usar BigQuery para el auto inferido del esquema de sus datos.
    
    ---
    
    ### Parte 6: Realizando consultas SQL a sus tablas.
    
    1. Entrar a la consola de GCP y buscar el servicio ‘Big Query’.
    2. En el apartado con el nombre de su proyecto seleccione el conjunto de datos y la tabla anteriormente creados en la ‘Parte 4: Creación de un conjunto de datos y una tabla en BigQuery’.
    3. Seleccione el apartado ‘CONSULTA’ y la opción ‘En una pestaña nueva’:
        
        ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-2y3-3/img/Untitled%2016.png)
        
    4. Haga una consulta SQL a la tabla seleccionado por medio del siguiente comando:
        
        ```sql
        SELECT * FROM `su_proyecto.su_conjunto_de_datos.su_tabla`;
        ```
        
        ```sql
        -- Comando para consultar la tabla creada en la 'Parte 4: Creación de un conjunto de datos y una tabla en BigQuery'
        SELECT * FROM `telematics-challenges.oline_retail_dataset.retail_table`;
        ```
        
        ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-2y3-3/img/Untitled%2017.png)
        
    
    ✅ ¡Listo! Ya sabe como usar BigQuery para hacer consultas SQL a sus tablas.