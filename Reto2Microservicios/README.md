# Reto No 2.

<aside>
📝 Notas

- Materia: Tópicos especiales en Telemática (ST0263)
- Estudiante: Santiago Puerta Florez ([spuertaf@eafit.edu.co](mailto:spuertaf@eafit.edu.co))
- Profesor: Edwin Nelson Montoya Munera ([emontoya@eafit.edu.co](mailto:emontoya@eafit.edu.co))
</aside>

# 1. Objetivo

> Diseño e implementación de tres (3) microservicios básicos que ofrecen un servicio al API Gateway y que se deben comunicar por un middleware RPC y por un middleware MOM. Cada uno de los microservicios debe soportar concurrencia. Usando el middleware API REST y gRPC para la comunicación RPC entre servicios, por su parte Apacha Kafka o RabbitMQ para la comunicación MOM.
> 

---

# 2. Aspectos solucionados y no solucionados

> En esta sección se destacan los problemas que han sido resueltos ✅, así como los desafíos pendientes aún sin resolver ⬜.
> 

- [x]  Diseño de mínimo dos (2) microservicios.
- [x]  Implementación de mínimo dos (2) microservicios.
- [x]  Mserv1: Listar archivos funcional.
- [x]  Mserv1: Listar archivos activo.
- [x]  Mserv2: Buscar archivos funcional.
- [x]  Mserv2: Buscar archivos activo.
- [x]  Middleware RPC funcional.
- [x]  Middleware RPC activo.
- [x]  Comunicación RPC Mserv1 funcional.

- [x]  Comunicación RPC Mserv1 activa.
- [x]  Comunicación RPC Mserv2 funcional.
- [x]  Comunicación RPC Mserv2 activa.
- [x]  Middleware MOM activo.
- [x]  Middleware MOM funcional.
- [x]  Comunicación MOM en caso de fallos.
- [x]  Archivo de configuración.
- [x]  Mecanismo de notificación para recibir los resultados de las consultas por el MOM.

---

# 3. Información general del diseño

## Sobre los microservicios

> En esta sección, se explican los microservicios implementados para dar solución al reto propuesto, explicado en la sección: [1. Objetivo](https://www.notion.so/Reto-No-2-c4b32e3bb5494781a5b2305455845dd1?pvs=21).
> 

| Nombre del microservicio | Rol que desempeña | IP y puertos de escucha |
| --- | --- | --- |
| Manager | Ofrece un servicio API Gateway al cliente y actúa como middleware RPC. Se encarga de ser el punto de entrada para las peticiones del cliente y solicitar recursos a los servicios List Files y Search Files. En caso de que la comunicación RPC con los servicios List Files o Search Files falle deberá de enviar las peticiones pendientes al Kafka Broker. | 44.218.162.196:8080 |
| List Files | Atiende las peticiones asignadas por el manager y da respuesta listando todos los archivos presentes en una carpeta de datos definida. | 34.198.41.234:8080 |
| Search Files | Atiende las peticiones asignadas por el manager y da respuesta listando los archivos buscados, presentes en una carpeta de datos definida. | 52.54.127.116:8080 |
| Kafka Broker | Ofrece un servicio de comunicación MOM con la finalidad de almacenar las peticiones pendientes a los servicios List Files y Search Files, en caso de que la comunicación RPC con estos servicios falle.  | 54.235.255.168:5672 |

## Patrones de diseño usados

> Esta sección aborda cómo y qué patrones de diseño se han aplicado para la estructuración y construcción del software.
> 

### Builder

> Es un patrón de diseño creacional, el cual permite la construcción de objetos complejos paso a paso.
> 
> 
> El patrón Builder se ha aplicado para la creación paso a paso de los diferentes microservicios, lo que en caso de cambios en la creación de estos objetos, permite tener un único modulo encargado de la misma; un único lugar donde cambiar la construcción de dichos objetos. 
> 

![Diagrama de código: Patrón de diseño Builder](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/4d5188e85c41ca423864c82ccf630cea77bf2337/docs/Patr%C3%B3n%20Builder.svg)

Diagrama de código: Patrón de diseño Builder

### Adapter

> Es un patrón de diseño estructural que permite la colaboración entre objetos con interfaces incompatibles.
> 
> 
> El patrón Adapter se ha aplicado para comunicarle al Builder según los argumentos pasados por consola que tipo de microservicio debía de construir.   
> 

![Diagrama de código: Patrón de diseño Adapter](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/4d5188e85c41ca423864c82ccf630cea77bf2337/docs/Patr%C3%B3n%20Adapter.svg)

Diagrama de código: Patrón de diseño Adapter

---

# 4. Ambiente de desarrollo

> En esta sección se proporciona una visión general fundamental para el desarrollo del proyecto. En ella, se detalla la "Estructura del Código", delineando la organización jerárquica de archivos y directorios que sustenta el proyecto. Además, se exploran aspectos clave de la "Configuración de Parámetros del Proyecto", destacando cómo ajustar y personalizar los elementos esenciales que guiarán el desarrollo y funcionamiento del software.
> 

## Estructura del código

> A continuación, exploraremos la disposición de archivos y carpetas en nuestro proyecto. A continuación, se muestra una visión general de cómo se organizan los archivos y las subcarpetas en relación con el directorio principal del proyecto.
> 

```
spuertaf-st0263:.
¦   .gitignore
¦   code_organization.jpg
¦   code_structure.txt
¦   requirements.txt
¦   settings.json
¦   setup.sh
¦   
+---src
    ¦   adapter.py
    ¦   builder.py
    ¦   main.py
    ¦   service.py
    ¦   utils.py
    ¦   
    +---data
    ¦       arquitectura.png
    ¦       customer.csv
    ¦       historiasUsuarios.txt
    ¦       lorem.txt
    ¦       sales_order.csv
    ¦       sales_territory.csv
    ¦       
    +---services
        ¦   list_files.py
        ¦   manager.py
        ¦   search_files.py
        ¦   
        +---configs
            +---contracts
            ¦       list_files_service_pb2.py
            ¦       list_files_service_pb2.pyi
            ¦       list_files_service_pb2_grpc.py
            ¦       search_files_service_pb2.py
            ¦       search_files_service_pb2.pyi
            ¦       search_files_service_pb2_grpc.py
            ¦       
            +---proto
                    list_files_service.proto
                    search_files_service.proto
```

## Configuración de parámetros del proyecto

> Para la configuración de los parámetros del proyecto utilizamos un enfoque basado en JSON. Esto nos brinda la flexibilidad necesaria para adaptar nuestro proyecto a diferentes entornos.
> 
> 
>  A continuación se muestra el contenido del archivo de configuraciones JSON. Este archivo actúa como un mapa que controla los aspectos esenciales de la aplicación.
> 

```json
{
    "list-files-service":{
        "data-folder-name" : "data",
        "end-point" : "[::]:8080",
        "response" : {
            "OK-status":200,
            "ERROR-status":400
        },
        "kafka-server" : ""
    },

    "search-files-service":{
        "data-folder-name" : "data",
        "end-point" : "[::]:8081",
        "response" : {
            "OK-status":200,
            "ERROR-status":400
        },
        "kafka-server" : ""
    },

    "manager-service":{
        "end-points" : {
            "/list-files" : ["service", "arguments"]
        },
        "services" : ["list-files","search-files"],
        "redirect": {
            "list-files" : "35.175.214.8:8080",
            "search-files" : "127.0.0.1:8080"
        },
        "response" : {
            "OK-status":200,
            "ERROR-status":400
        },
        "host" : "0.0.0.0",
        "port" : 8080
    },

    "command" : {
        "services" : ["list-files","search-files","manager"]
    }
}
```

## Paquetes y dependencias

> En esta sección, exploraremos los paquetes y las dependencias del proyecto, proporcionando una visión general de cómo los distintos componentes se organizan y relacionan entre sí.
> 
> 
> El siguiente diagrama proporcionará una comprensión rápida de cómo los paquetes se organizan y cómo interactúan entre sí en el contexto general del sistema.
> 

![Diagrama de paquetes: Dependencias y versiones. ](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/4d5188e85c41ca423864c82ccf630cea77bf2337/docs/Diagrama%20de%20paquetes.svg)

Diagrama de paquetes: Dependencias y versiones. 

> Las dependencias requeridas para la correcta ejecución del software desarrollado son las siguientes:
> 

```
blinker==1.6.2
click==8.1.7
dynaconf==3.2.2
Flask==2.3.3
grpcio==1.57.0
itsdangerous==2.1.2
Jinja2==3.1.2
MarkupSafe==2.1.3
protobuf==4.24.2
typeguard==4.1.2
typing_extensions==4.7.1
Werkzeug==2.3.7
```

---

# 5. Ambiente de ejecución

> En esta sección, se explorara el entorno de ejecución que sustenta nuestra solución de software; además se detallará cómo usar el mismo.
> 

## Arquitectura general

> El siguiente diagrama destaca que servicios de Amazon Web Services (AWS) son empleados para lograr un despliegue eficiente y escalable.
> 

![Diagrama de despliegue: Infraestructura de AWS usada.](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/4d5188e85c41ca423864c82ccf630cea77bf2337/docs/Diagrama%20de%20despliegue.svg)

Diagrama de despliegue: Infraestructura de AWS usada.

## Guía de uso

> La siguiente guía brindará los pasos a seguir para un correcto funcionamiento y ejecución del software.
> 

### Instalando requisitos previos

> Primeramente deberemos de instalar los programas necesarios para la ejecución del proyecto; se instalarán Git y Python y se clonará el repositorio que contiene el código correspondiente.
> 

```bash
#instalando git
sudo apt-get install git
echo "[x] Git instalado"

#instalando python
sudo apt install python3
echo "[x] Python instalado"

#clonando repositorio del codigo
git clone https://github.com/spuertaf/spuertaf-st0263.git
echo "[x] Repositorio de codigo clonado"
```

### Instalación de dependencias

> Nos dirigiremos a la carpeta con el código correspondiente y crearemos un entorno virtual, accederemos a el e instalaremos las librerías y dependencias correspondientes.
> 

```bash
#dirigiendome al directorio de codigo
cd spuertaf-st0263

#instalando dependencia para creacion de entornos virtuales
sudo apt install python3-venv

#creando un nuevo entorno virtual
python3 -m venv venv
echo "[x] Nuevo entorno virtual creado"

#ejecutando el entorno virtual
source venv/bin/activate

#instalando librerias necesarias
pip install -r requirements.txt
echo "[x] Librerias necesarias instaladas"
```

### Ejecución del programa

> Finalmente podremos ejecutar el programa especificándole al argumento ‘—service’ que tipo de servicio queremos crear.
> 
> 
> Cabe recalcar que los servicios permitidos por el programa son los siguientes: manager, list_files, search_files.
> 

```bash
#ejecucion del programa para el servicio list_files
python -m src.main --service list_files
```

# 6. Referencias

[Builder](https://refactoring.guru/es/design-patterns/builder)

Patrón de diseño Builder.

[Adapter](https://refactoring.guru/es/design-patterns/adapter)

Patrón de diseño Adapter.

[Introducing EdrawMax 10](https://www.edrawsoft.com/es/article/package-diagram-uml.html)

Diagrama de paquetes.

[The C4 model for visualising software architecture](https://c4model.com/)

Diagrama de despliegue.

# Contenido

# Enlaces externos

<aside>
<img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" alt="https://cdn-icons-png.flaticon.com/512/25/25231.png" width="40px" /> [Repositorio GitHub.](https://github.com/spuertaf/spuertaf-st0263)

</aside>

# Descargas

<aside>
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Diagrams.net_Logo.svg/2048px-Diagrams.net_Logo.svg.png" alt="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Diagrams.net_Logo.svg/2048px-Diagrams.net_Logo.svg.png" width="40px" /> Modelo C4: Diagramas de arquitectura.

[Diagramas de arquitectura.drawio](Reto%20No%202%20c4b32e3bb5494781a5b2305455845dd1/Diagramas_de_arquitectura.drawio)

</aside>

<aside>
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Python_Windows_source_code_icon_2016.svg/768px-Python_Windows_source_code_icon_2016.svg.png?20220830130654" alt="https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Python_Windows_source_code_icon_2016.svg/768px-Python_Windows_source_code_icon_2016.svg.png?20220830130654" width="40px" /> Código implementado.

[releasev.1.zip](Reto%20No%202%20c4b32e3bb5494781a5b2305455845dd1/releasev.1.zip)

</aside>