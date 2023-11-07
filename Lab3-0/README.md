# LAB 3-0: Creación de un Clúster EMR

| Información |  |
| --- | --- |
| Materia | Tópicos especiales en Telemática |
| Curso | ST0263 |
| Estudiante | Santiago Puerta (mailto:spuertaf@eafit.edu.co) |
| Profesor | Edwin Nelson Montoya Munera (mailto:emontoya@eafit.edu.co) |

# 1. Objetivo

Creación de un Clúster AWS EMR en Amazon para trabajar todos los laboratorios.

---

# 2. Aspectos solucionados y no solucionados

- [x]  Creación de un par de claves.
- [x]  Creación de un bucket de AWS S3 para almacenar los notebooks que crearemos en el clúster de AWS EMR.
- [x]  Creación de un Clúster AWS EMR versión 6.14.0
- [x]  Conexión por medio de SSH con el nodo maestro.
- [x]  Servicio Hue funcional.
- [x]  Servicio JupyterHub funcional.

---

# 5. Ambiente de ejecución

## Guía de uso

La siguiente guía brindará los pasos a seguir para una correcta creación del Cluster AWS EMR. 

### Parte 1: Creación de un par de claves

1. Entrar a la consola web de  AWS y buscar el servicio EC2:
    
    ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-0/docs/img/Untitled.png)
    
2. Seleccionar el botón ‘Pares de claves’:
    
    ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-0/docs/img/Untitled%201.png)
    
3. Seleccionar el botón ‘Crear pares de claves’:
    
    ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-0/docs/img/Untitled%202.png)
    
4. Registrar un nombre para el par de claves y seleccionar el botón ‘Crear par de claves’:
    
    ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-0/docs/img/Untitled%203.png)
    
5. Una vez creado el par de claves se descargarán en su ordenador.

---

### Parte 2: Creación de un bucket de AWS S3

Deberemos de crear un bucket de AWS S3 para almacenar los notebooks que crearemos en el clúster de AWS EMR.

1.  Entrar a la consola web de  AWS y buscar el servicio S3:
    
    ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-0/docs/img/Untitled%204.png)
    
2. Seleccionar el botón ‘Crear bucket’:
    
    ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-0/docs/img/Untitled%205.png)
    
3. Registrar un nombre para el bucket, dejar las opciones posteriores por defecto y seleccionar el botón ‘Crear Bucket’:
    
    ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-0/docs/img/Untitled%206.png)
    
    ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-0/docs/img/Untitled%207.png)
    

---

### Parte 3: Creación de un Clúster AWS EMR versión 6.14.0

1. Entrar a la consola web de  AWS y buscar el servicio EMR:
    
    ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-0/docs/img/Untitled%208.png)
    
2. Seleccionar el botón ‘Crear clúster’:
    
    ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-0/docs/img/Untitled%209.png)
    
3. Registrar un nombre para el clúster, seleccionar la versión ‘**emr-6.14.0**’ y seleccionar ‘Custom’
    
    ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-0/docs/img/Untitled%2010.png)
    
4. Seleccionar las siguientes aplicaciones en la opción ‘Paquete de Aplicaciones’ y habilitar ‘**usar para metadatos de la tabla Hive**’ y ‘**usar para metadatos de la tabla Spark**’:
    
    ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-0/docs/img/Untitled%2011.png)
    
5. Crear los grupos principales, centrales y de nodos de tareas con el tipo de instancia ‘**m5.xlarge**’:
    
    ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-0/docs/img/Untitled%2012.png)
    
6. Editar la sección ‘Terminación del clúster’ y asignar la terminación después de un tiempo de inactividad de tres (3) horas:
    
    ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-0/docs/img/Untitled%2013.png)
    
7. Dejar las opciones posteriores por defecto y dirigirse al apartado ‘Editar la configuración de software: *opcional*’:
8. Seleccionar la opción ‘Ingresar la configuración’ y pegar la siguiente configuración:
    
    ```json
    [
      {
        "Classification": "jupyter-s3-conf",
        "Properties": {
          "s3.persistence.enabled": "true",
          "s3.persistence.bucket": "nombre_bucket_creado_en_paso2"
        }
      }
    ]
    ```
    
    ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-0/docs/img/Untitled%2014.png)
    
9. Dirigirse a la sección ‘**Configuración de seguridad y par de claves de EC2: *opcional***’ y en la opción ‘**Par de claves de Amazon EC2 para el protocolo SSH al clúster**’ elegir el nombre del par de claves creado en ‘Parte 1: Creación de un par de claves’:
    
    ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-0/docs/img/Untitled%2015.png)
    
10. En la sección ‘**Roles de Identity and Access Management (IAM)**’ en las opciones ‘**Rol de servicio de Amazon EMR**’ seleccionar el rol de servicio ‘EMR_DefaultRole’, ‘**Perfil de instancia de EC2 para Amazon EMR**’ seleccionar el rol de servicio ‘EMR_EC2_DefaultRole’ y finalmente, en la opción ‘**Rol de escalamiento automático personalizado *- opcional***’ seleccionar el rol de servicio ‘LabRole’:
    
    ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-0/docs/img/Untitled%2016.png)
    
11. Finalmente seleccionar el botón ‘Crear clúster’:
    
    ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-0/docs/img/Untitled%2017.png)
    

---

### Parte 4: Abrir los puertos requeridos por las aplicaciones

‼️ Nota: Los siguientes pasos solo se deben de realizar una vez, cada vez que se crea, destruye o clona un clúster.

1. Entrar a la consola web de  AWS y buscar el servicio EMR:
    
    ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-0/docs/img/Untitled%208.png)
    
2. Seleccionar el ‘ID del clúster’ que tenga el estado ‘Esperando’
    
    ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-0/docs/img/Untitled%2018.png)
    
3. Dentro del menú de Amazon EMR seleccionar la opción ‘**Bloquear el acceso público**’
    
    ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-0/docs/img/Untitled%2019.png)
    
4. Seleccionar el botón ‘Editar’, en la sección ‘**Bloquear el acceso público**’ seleccionar la opción ‘**Desactivar**’ y seleccionar el botón ‘**Guardar**’:
    
    ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-0/docs/img/Untitled%2020.png)
    
5. Dentro del menú de Amazon EMR seleccionar la opción ‘Clústeres’ y seleccione el ‘ID del clúster’ que tenga el estado ‘Esperando’; luego, seleccione la opción ‘**Aplicaciones**’:
    
    ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-0/docs/img/Untitled%2021.png)
    

 Se deberán de abrir los puertos TCP señalados anteriormente, además de abrir los puertos TCP 22, 14000 y 9878. 

6. Entrar a la consola web de  AWS y buscar el servicio EC2 y seleccionar el botón ‘Instancias en ejecución’:
    
    ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-0/docs/img/Untitled%2022.png)
    
7. Seleccionar el ‘ID de la instancia’ que tenga el ‘Nombre de grupo de seguridad’ ‘ElasticMapReduce-master’:
    
    ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-0/docs/img/Untitled%2023.png)
    
8. Seleccionar la opción ‘Seguridad’ y ‘Grupos de seguridad’ :
    
    ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-0/docs/img/Untitled%2024.png)
    
9. Seleccionar el botón ‘Editar reglas de entrada’:
    
    ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-0/docs/img/Untitled%2025.png)
    
10. Para cada uno de los puertos mostrados anteriormente (paso 5), realizar lo siguiente:
    1. Seleccionar el botón ‘Agregar regla’:
        
        ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-0/docs/img/Untitled%2026.png)
        
    2. Seleccionar la opción ‘TCP Personalizado’, registrar el numero del puerto y seleccionar la opción ‘Anywhere-IPv4’:
        
        ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-0/docs/img/Untitled%2027.png)
        
    3. Agregar cada uno de los puertos mostrados en el paso 5.
    4. Seleccionar el botón ‘Guardar reglas’

---

### Parte 5: Entrando por SSH al nodo maestro

1. Entrar a la consola web de  AWS y buscar el servicio EMR y seleccionar el ‘ID del clúster’ que tenga el estado ‘Esperando’:
2. Seleccionar la URL ‘Conectarse al nodo principal mediante SSH’ y siga las instrucciones estipuladas allí. 
    
    ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-0/docs/img/Untitled%2028.png)
    
3. Una conexión exitosa por medio de SSH con el nodo master del clúster se vera de la siguiente forma:
    
    ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-0/docs/img/Untitled%2029.png)
    
4. Deberá de editar el archivo ‘hue.ini’ para ello siga los siguientes pasos: 
    1. Escriba el siguiente comando en la terminal:
        
        ```bash
        sudo nano /etc/hue/conf/hue.ini
        ```
        
    2. Busque la linea que contenga ‘webhdfs_url’ y cambiar el puerto de 14000 a 9870:
        
        ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-0/docs/img/Untitled%2030.png)
        
    3. Presione las teclas control + X y Y + enter, para guardar los cambios.
    4. Reinicie el servicio Hue mediante el siguiente comando:
        
        ```bash
        sudo systemctl restart hue.service
        ```
        

---

### Parte 6: Utilizando Hue

1. Entrar a la consola web de  AWS y buscar el servicio EMR, seleccionar el ‘ID del clúster’ que tenga el estado ‘Esperando’; luego, seleccione la opción ‘**Aplicaciones**’:
    
    ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-0/docs/img/Untitled%2021.png)
    
2. Seleccionar la URL del campo ‘Tonalidad’ e ingresar el usuario ‘hadoop’ y una contraseña de su gusto:
    
    ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-0/docs/img/Untitled%2031.png)
    

✅ ¡Listo! Ya puede gestionar archivos por medio de Hue para HDFS.

---

### Parte 7: Utilizando JupyterHub

1. Entrar a la consola web de  AWS y buscar el servicio EMR, seleccionar el ‘ID del clúster’ que tenga el estado ‘Esperando’; luego, seleccione la opción ‘**Aplicaciones**’
2. Seleccionar la URL del campo ‘JupyterHub’ e ingresar el usuario ‘jovyan’ y la contraseña ‘jupyter’.
3. Seleccionar el botón ‘New’ y la opción ‘PySpark’:
    
    ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-0/docs/img/Untitled%2032.png)
    
4. Verifique las variables de contexto de Spark se encuentran instaladas:
    
    ![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Lab3-0/docs/img/Untitled%2033.png)
    

✅ ¡Listo! Ya puede realizar notebooks PySpark.