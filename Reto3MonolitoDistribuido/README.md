# Reto No 3.

<aside>
📝 Notas

- Materia: Tópicos especiales en Telemática (ST0263)
- Estudiantes: Daniel Jaramillo Valencia ([djaramillv@eafit.edu.co](mailto:djaramillv@eafit.edu.co)) | Santiago Puerta Florez ([spuertaf@eafit.edu.co](mailto:spuertaf@eafit.edu.co)) 
- Profesor: Edwin Nelson Montoya Munera ([emontoya@eafit.edu.co](mailto:emontoya@eafit.edu.co))
</aside>

# 1. Objetivo

> Despliegue de un Sistema de gestión de contenidos (CMS), empleando la tecnología de contenedores (Docker), con su propio dominio. Hacer uso de NGINX como balanceador de cargas (LB) y almacenar tanto datos como configuraciones de forma remota, en dos (2) maquinas diferentes.
> 

---

# 2. Aspectos solucionados y no solucionados

> En esta sección se destacan los problemas que han sido resueltos ✅, así como los desafíos pendientes aún sin resolver ⬜.
> 
- [x]  Creación de las cinco (5) instancias requeridas para el despliegue.
- [x]  Despliegue del servicio de bases de datos.
- [x]  Despliegue del servicio de NFS.
- [x]  Despliegue de dos (2) servicios de Drupal.
- [x]  Instancias de Drupal compartiendo misma configuración.
- [x]  Despliegue del servicio de NGINX.
- [ ]  Asociar un dominio al servicio de NGINX.

---

# 3. Información general del diseño

## Sobre los servicios

> En esta sección, se explican los servicios implementados para dar solución al reto propuesto, explicado en la sección: [1. Objetivo](https://www.notion.so/Reto-No-3-6e49511c40b44c60abf2ecbb7aa396f4?pvs=21).
> 

| Nombre del servicio | Rol que desempeña | IP y puertos de escucha |
| --- | --- | --- |
| NGINX Service | Sistema balanceador de cargas. Redirecciona las peticiones de los clientes de forma round-robin a los servicios Drupal. | 34.198.41.234 : 80 |
| Drupal Service 1 | Sistema de gestión de contenido; almacena sus datos en una base de datos PostgreSQL y sus configuraciones en un sistema de archivos NFS.  | 54.198.110.83 : 80 |
| Drupal Service 2 | Sistema de gestión de contenido; almacena sus datos en una base de datos PostgreSQL y sus configuraciones en un sistema de archivos NFS.  | 54.87.255.57 : 80 |
| NFS Service | Sistema NFS para el almacenamiento de las configuraciones de las replicas Drupal.  | 54.172.26.93 : 2049 |
| Database Service | Sistema de base de datos para el almacenamiento de los datos requeridos por los servicios Drupal. | 54.198.168.76 : 5432 |

---

# 4. Ambiente de desarrollo

> En esta sección se proporciona una visión general fundamental para el desarrollo del proyecto. En ella, se detalla la "Estructura del Código", delineando la organización jerárquica de archivos y directorios que sustenta el proyecto.
> 

## Estructura del código

> A continuación, exploraremos la disposición de archivos y carpetas en nuestro proyecto. A continuación, se muestra una visión general de cómo se organizan los archivos y las subcarpetas en relación con el directorio principal del proyecto.
> 

```
Reto3MonolitoDistribuido
├── conf
│   └── nginx.conf
├── docker
│   ├── NGINX.yaml
│   ├── drupal.yaml
│   ├── postgres.yaml
│   └── simple_drupal.yaml
└── make.sh
```

---

# 5. Ambiente de ejecución

> En esta sección, se explorara el entorno de ejecución que sustenta la solución.
> 

## Arquitectura general

> El siguiente diagrama destaca que servicios de Amazon Web Services (AWS) son empleados para lograr un despliegue eficiente y escalable.
> 

![Diagrama de despliegue: Infraestructura de AWS usada.](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/dd2bc232b1d98b8cc3c042bdfb498558c7d55d46/Reto3MonolitoDistribuido/docs/ArquitecturaMonolitica.svg)

Diagrama de despliegue: Infraestructura de AWS usada.

## Guía de implementación

> La siguiente guía brindará los pasos a seguir para una correcta implementación de la arquitectura.
> 
1. Crear las cinco (5) maquinas virtuales.
2. Instalar Docker en cuatro (4) de ellas.
3. Crear servidor NFS en una (1) de ellas; preferiblemente aquella que no tenga Docker.
4. Instalar cliente NFS en dos (2) de las maquinas virtuales; estas serán los servicios Drupal.
5. Crear en una de las maquinas un docker-compose.yaml con la plantilla simple_drupal.yaml presente en GitHub.
6. En la maquina donde se creo el docker-compose.yaml, descrito en el paso anterior, ejecutar el comando:
    
    ```bash
    sudo docker-compose up -d
    ```
    
7. Configurar el servicio de base de datos
    1. Situarse en la maquina virtual destinada para el servicio de bases de datos.
    2. Habilitar el puerto 5432 requerido por PostgreSQL mediante las reglas de seguridad.
    3. Crear el archivo docker-compose.yaml con la plantilla postgres.yaml presente en GitHub.
    4. Ejecutar el siguiente comando con el fin de montar el servicio de bases de datos.
        
        ```bash
        sudo docker-compose up -d
        ```
        
    5.  Ejecutaremos el contenedor de PostgreSQL creado anteriormente con el siguiente comando: 
        
        ```bash
        sudo docker exec -it nombre_contenedor bash
        ```
        
    6. Instalamos la extensión pg_trgm necesaria para la ejecución de Drupal.
        
        ```bash
        apk update
        apk add postgresql-contrib
        ```
        
    7. Crearemos la base de datos para el almacenamiento de la informacion de Drupal.  
        
        ```bash
        psql -U postgres -c "CREATE DATABASE basededatos";
        ```
        
    8. Creamos y vinculamos la extensión pg_trgm a la base de datos creada anteriormente.
        
        ```bash
        psql -U postgres -d basededatos -c "CREATE DATABASE basededatos";
        ```
        
8. Digitar en el navegador la dirección http://ip_publica_drupal.
9. Realizar la configuración de Drupal querida. 
10. Seguir los pasos estipulados en la guía [🐋 **How To Set Up an NFS Mount on Ubuntu 22.04**](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-nfs-mount-on-ubuntu-22-04)
11. En ambas maquinas virtuales de los servicios Drupal crear un punto de montaje con el servicio File Server System - NFS.
12. En una de las maquinas virtuales de los servicios Drupal dirigirse a la ruta donde se encuentra el punto de montaje.
13. Copiaremos las configuraciones necesarias para el funcionamiento de Drupal en el punto de montaje por medio del siguiente comando:
    
    ```bash
    sudo docker cp nombre_contenedor_drupal:/opt/drupal/web ./
    ```
    
14. En aquella maquina virtual que no se ha creado aun un docker-compose destinada para alojar uno (1) de los servicios Drupal, crear el archivo docker-compose.yaml con la plantilla drupal.yaml presente en GitHub.  
15. Cambiar la línea diez (10) del código de la plantilla anteriormente creada, por lo siguiente:
    
    ```yaml
    volumes:
    	- punto_de_montaje_local:/var/www/html
    ```
    
16. Ejecutar el siguiente comando con el fin de montar el segundo (2ndo) servicio de Drupal.
    
    ```bash
    sudo docker-compose up -d
    ```
    
17. Dirigirnos a la maquina virtual donde creamos un docker-compose.yaml con la plantilla simple_drupal.yaml
18. Con el fin de que ambos servicios de Drupal compartan configuraciones ejecutaremos los siguientes comandos.
    
    ```bash
    sudo docker stop nombre_contenedor_drupal
    sudo docker rm nombre_contenedor_drupal
    ```
    
    - Copiar el contenido del docker-compose creado en el paso catorce (14) y modificado en el paso quince (15).
    
    ```bash
    nano docker-compose.yaml
    ```
    
    - Una vez se abre la terminal pegar el contenido copiado; salir con Ctrl + X y luego ENTER.
    - Ejecutar el siguiente comando con el fin de montar el primer (1er) servicio de Drupal.
    
    ```bash
    sudo docker-compose up -d
    ```
    

# 6. Referencias

[The C4 model for visualising software architecture](https://c4model.com/)

Diagrama de despliegue.

[How To Set Up an NFS Mount on Ubuntu 22.04  | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-nfs-mount-on-ubuntu-22-04)

Guía de despliegue de servidor NFS.

# 🌐 Enlaces externos

<aside>
<img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" alt="https://cdn-icons-png.flaticon.com/512/25/25231.png" width="40px" /> [Repositorio GitHub.](https://github.com/spuertaf/spuertaf-st0263)

</aside>

# 🔻 Descargas

<aside>
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Diagrams.net_Logo.svg/2048px-Diagrams.net_Logo.svg.png" alt="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Diagrams.net_Logo.svg/2048px-Diagrams.net_Logo.svg.png" width="40px" /> Modelo C4: Diagramas de arquitectura.

[C4ModelMonolitica.drawio](Reto%20No%203%206e49511c40b44c60abf2ecbb7aa396f4/C4ModelMonolitica.drawio)

</aside>
