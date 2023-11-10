# LAB 3-1: Gestión de archivos en HDFS y S3

| Información |  |
| --- | --- |
| Materia | Tópicos especiales en Telemática |
| Curso | ST0263 |
| Estudiante | Santiago Puerta (mailto:spuertaf@eafit.edu.co) |
| Profesor | Edwin Nelson Montoya Munera (mailto:emontoya@eafit.edu.co) |

# 1. Objetivo

Copiar todos los archivos disponibles en [😾 Datasets](https://github.com/st0263eafit/st0263-232/tree/main/bigdata/datasets) tanto HDFS (almacenamiento temporal) como en S3 (almacenamiento permanente).

---

# 2. Aspectos solucionados y no solucionados

- [x]  Creación de un bucket publico AWS S3.
- [x]  Gestión de archivos en HDFS vía terminal.
- [x]  Gestión de archivos en HDFS vía HUE.
- [x]  Gestión de arvhivos en S3 vía HUE.

---

# 5. Ambiente de ejecución

## Guía de uso

### Parte 1: Creación de un bucket publico de AWS S3

1. Entrar a la consola AWS y buscar el servicio S3:
2. Seleccionar el botón ‘Crear bucket’:
3. Primeramente registrar un nombre para el bucket;  posteriormente en la sección ‘****Object Ownership****’ seleccionar la opcion ‘ACLs enabled’ y seleccionar la casilla ‘Object writer’. 
    
    Seguidamente en la sección ‘**Block Public Access settings for this bucket**’ quitar el ‘✅ check’ a la opción ‘Block all public access’ y seleccionar la opción ‘I acknowledge that the current settings might result in this bucket and the objects within becoming public.’:
    
    ![Untitled](LAB%203-1%20Gestio%CC%81n%20de%20archivos%20en%20HDFS%20y%20S3%20928fbcdfe81343a2abe05fdd349afe93/Untitled.png)
    
    ![Untitled](LAB%203-1%20Gestio%CC%81n%20de%20archivos%20en%20HDFS%20y%20S3%20928fbcdfe81343a2abe05fdd349afe93/Untitled%201.png)
    
    ![Untitled](LAB%203-1%20Gestio%CC%81n%20de%20archivos%20en%20HDFS%20y%20S3%20928fbcdfe81343a2abe05fdd349afe93/Untitled%202.png)
    
4. Dejar las posteriores opciones por defecto y seleccionar el botón ‘Crear Bucket’:
    
    ![Untitled](LAB%203-1%20Gestio%CC%81n%20de%20archivos%20en%20HDFS%20y%20S3%20928fbcdfe81343a2abe05fdd349afe93/Untitled%203.png)
    
5. Una vez en el menú de S3, seleccionar el nombre del bucket anteriormente creado:
6. Seleccionar el apartado de ‘Permissions’ y buscar la sección ‘**Access control list (ACL)**’, una vez allí, seleccionar el botón ‘Edit’.
7. Marcar con ‘✅check’ las casillas ‘List’ y ‘Read’ de ‘Everyone (public access)’ y ‘Authenticated users group (anyone with an AWS account)’; posteriormente marcar con ‘✅ check’ la opción ‘I understand the effects of these changes on my objects and buckets.’; finalmente seleccionar el botón ‘Save changes’:
    
    ![Untitled](LAB%203-1%20Gestio%CC%81n%20de%20archivos%20en%20HDFS%20y%20S3%20928fbcdfe81343a2abe05fdd349afe93/Untitled%204.png)
    
8. Ingresa al siguiente enlace [✈️ airlines](https://github.com/st0263eafit/st0263-232/blob/main/bigdata/datasets/airlines.csv) y selecciona el botón ‘Download raw file’:
    
    ![Untitled](LAB%203-1%20Gestio%CC%81n%20de%20archivos%20en%20HDFS%20y%20S3%20928fbcdfe81343a2abe05fdd349afe93/Untitled%205.png)
    
9. Regresa a la interfaz principal de los buckets, selecciona el nombre del bucket anteriormente creado y arrastra el archivo descargado a el; seguidamente, selecciona el botón ‘Upload’
    
    ![Untitled](LAB%203-1%20Gestio%CC%81n%20de%20archivos%20en%20HDFS%20y%20S3%20928fbcdfe81343a2abe05fdd349afe93/Untitled%206.png)
    
10. Selecciona el nombre del archivo anteriormente cargado y posteriormente, en el apartado ‘Properties’ en la sección ‘****Object overview****’ copia el ‘Object URL’:
    
    ![Untitled](LAB%203-1%20Gestio%CC%81n%20de%20archivos%20en%20HDFS%20y%20S3%20928fbcdfe81343a2abe05fdd349afe93/Untitled%207.png)
    
11. En una ventana de tu navegador pega la URL anteriormente copiada dejando de lado ‘/airlines.csv’:
    
    ![Untitled](LAB%203-1%20Gestio%CC%81n%20de%20archivos%20en%20HDFS%20y%20S3%20928fbcdfe81343a2abe05fdd349afe93/Untitled%208.png)
    

✅ ¡Listo! Ya posee un bucket publico de AWS S3

‼️ Nota: Para poder leer los archivos del bucket publico creado anteriormente por medio de la CLI de AWS se puede usar el siguiente comando:

```bash
aws s3 ls s3://nombre-del-bucket
```

```bash
#Comando para leer el bucket anteriormente creado
aws s3 ls s3://datasetsspuertaf
```

---

### Parte 2: Gestión de archivos en HDFS vía terminal

Nota: 

1. Primeramente deberemos de descargar el archivo ‘[😾 datasets.zip](https://github.com/spuertaf/spuertaf-st0263/blob/main/Lab3-1/datasets.zip)’ y seleccionar el botón ‘Download raw file’:
    
    ![Untitled](LAB%203-1%20Gestio%CC%81n%20de%20archivos%20en%20HDFS%20y%20S3%20928fbcdfe81343a2abe05fdd349afe93/Untitled%209.png)
    
2. Una vez descargado el archivo se deberá de descomprimir el mismo.
3. Seguidamente deberemos de crear un clúster AWS EMR, visite la siguiente guía ‘[Creación de un Clúster EMR](https://github.com/spuertaf/spuertaf-st0263/tree/main/Lab3-0)’ con este propósito.
4. Una vez creado el clúster especificado anteriormente debemos de conectarnos a el por medio de SSH; el como conectarse al clúster por medio de SSH puede ser encontrado en la guía anterior en el apartado ‘[Parte 5: Entrando por SSH al nodo maestro](https://github.com/spuertaf/spuertaf-st0263/tree/main/Lab3-0)’.
5. Luego de establecer una conexión con el nodo maestro crearemos una carpeta llamada ‘gutenberg-small’ dentro de la ruta ‘/user/hadoop/datasets’ por medio de los siguientes comandos:
    
    ```bash
    #crear el directorio 'datasets' dentro de la ruta 'user/hadoop/'
    hdfs dfs -mkdir /user/hadoop/datasets
    ```
    
    ```bash
    #crear el directorio 'gutenber-small' dentro de la ruta 'user/hadoop/datasets/'
    hdfs dfs -mkdir /user/hadoop/datasets/gutenberg-small
    ```
    
    ```bash
    #listar directorios y archivos presentes en la ruta /user/hadoop/
    hdfs dfs -ls /user/hadoop/datasets
    ```
    
    ![Untitled](LAB%203-1%20Gestio%CC%81n%20de%20archivos%20en%20HDFS%20y%20S3%20928fbcdfe81343a2abe05fdd349afe93/Untitled%2010.png)
    
6. Ahora copiaremos el contenido de la carpeta local ‘datasets/gutenberg-small’ al directorio ‘/user/hadoop/datasets/gutenberg-small’ por medio del siguiente comando:
    
    ```bash
    hdfs dfs -put /home/spuertaf/Desktop/datasets/gutenberg-small/*.txt /user/hadoop/datasets/gutenberg-small/
    ```
    

✅ ¡Listo! Ya puede subir archivos a HDFS del clúster EMR por medio de la terminal.

---

### Parte 3: Gestión de archivos en HDFS vía HUE

1. Entrar a la consola AWS y buscar el servicio EMR.
2. Seleccionar el ‘ID del clúster’ que tenga el estado ‘Esperando; luego, seleccione la opción ‘**Aplicaciones**’.
3. Seleccionar la URL del campo ‘HUE’ e ingresar el usuario ‘hadoop’ y una contraseña de su gusto.
4. Seleccionar el apartado ‘Files’:
    
    ![Untitled](LAB%203-1%20Gestio%CC%81n%20de%20archivos%20en%20HDFS%20y%20S3%20928fbcdfe81343a2abe05fdd349afe93/Untitled%2011.png)
    
5. Seguidamente, seleccionar el botón ‘New’ seleccionar la opción ‘Directory’:
    
    ![Untitled](LAB%203-1%20Gestio%CC%81n%20de%20archivos%20en%20HDFS%20y%20S3%20928fbcdfe81343a2abe05fdd349afe93/Untitled%2012.png)
    
6. Crear el directorio ‘datasets’ si este aun no se encuentra creado:
    
    ![Untitled](LAB%203-1%20Gestio%CC%81n%20de%20archivos%20en%20HDFS%20y%20S3%20928fbcdfe81343a2abe05fdd349afe93/Untitled%2013.png)
    
7. En la ruta /user/admin/datasets/ crear el directorio onu/:
    
    ![Untitled](LAB%203-1%20Gestio%CC%81n%20de%20archivos%20en%20HDFS%20y%20S3%20928fbcdfe81343a2abe05fdd349afe93/Untitled%2014.png)
    
8. Seleccionar el botón ‘Upload’ una vez en la ruta ‘/user/admin/datasets/onu’:
    
    ![Untitled](LAB%203-1%20Gestio%CC%81n%20de%20archivos%20en%20HDFS%20y%20S3%20928fbcdfe81343a2abe05fdd349afe93/Untitled%2015.png)
    
    ![Untitled](LAB%203-1%20Gestio%CC%81n%20de%20archivos%20en%20HDFS%20y%20S3%20928fbcdfe81343a2abe05fdd349afe93/Untitled%2016.png)
    
9. Selecciona los archivos presenes en local de la carpeta onu/; posteriormente, seleccionar el botón ‘open’:
    
    ![Untitled](LAB%203-1%20Gestio%CC%81n%20de%20archivos%20en%20HDFS%20y%20S3%20928fbcdfe81343a2abe05fdd349afe93/Untitled%2017.png)
    

✅ ¡Listo! Ya puede subir archivos a HDFS del clúster EMR por medio de HUE.

---

### Parte 4: Gestión de archivos en S3 vía HUE

1. Entrar a la consola AWS y buscar el servicio EMR.
2. Seleccionar el ‘ID del clúster’ que tenga el estado ‘Esperando; luego, seleccione la opción ‘**Aplicaciones**’.
3. Seleccionar la URL del campo ‘HUE’ e ingresar el usuario ‘hadoop’ y una contraseña de su gusto.
4. Seleccionar el apartado ‘S3’:
    
    ![Untitled](LAB%203-1%20Gestio%CC%81n%20de%20archivos%20en%20HDFS%20y%20S3%20928fbcdfe81343a2abe05fdd349afe93/Untitled%2018.png)
    
5. Seleccionar el nombre del Bucket creado en la ‘Parte 1: Creación de un bucket publico de AWS S3’, en este caso particular el Bucket ‘datasetsspuertaf’.
6. Seleccionar el botón ‘Upload’, ‘Select Files’; y finalmente elegir los archivos que se deseen cargar.

✅ ¡Listo! Ya puede subir archivos a un bucket de S3 vía HUE