# LAB 3-4: Spark con Notebooks y PySpark.

| Información |  |
| --- | --- |
| Materia | Tópicos especiales en Telemática |
| Curso | ST0263 |
| Estudiante | Santiago Puerta (mailto:spuertaf@eafit.edu.co) |
| Profesor | Edwin Nelson Montoya Munera (mailto:emontoya@eafit.edu.co) |

# 5. Ambiente de ejecución

## Guía de uso

1. Se crea el cluster de AWS EMR (En mi caso solo clono) y pasamos a la consola del nodo master:

    ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-0/docs/img/Untitled%2029.png)

2. Crear el archivo wc-pyspark.py

3. Ejecutar el siguiente comando:
    
    ```bash
    spark-submit --master yarn --deploy-mode cluster wc-pyspark.py
    ```

4. Dirigirse a JupyterHub e ingresar:

5. Probamos con el Notebook sugerido en el Lab, asi que lo subimos:

6. Ingresamos al Notebook y editamos las rutas al bucket donde se encuentran los archivos y ejecutamos:



7. Ahora subimos el Notebook para las consultas de Covid19:

8. Ingresamos al Notebook y editamos las rutas al bucket donde se encuentran los archivos y ejecutamos obteniendo lo siguiente:

    a. Los 10 dias con mas casos de Covid en Colombia ordenados de mayor a menor:

    b. Los 10 departamentos con más casos de Covid en Colombia ordenados de mayor a menor:

    c. Distribución de casos por edades de covid en Colombia: 
