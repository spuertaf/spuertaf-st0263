# Proyecto No 3.

| Información |  |
| --- | --- |
| Materia | Tópicos especiales en Telemática |
| Curso | ST0263 |
| Estudiantes | Santiago Puerta Florez (mailto:spuertaf@eafit.edu.co) |
|  | Juan David Echeverri (mailto:jdecheverv@eafit.edu.co) |
|  | Juan Sebastián Guerra (mailto:jsguerrah@eafit.edu.co) |
|  | Juan David Prieto (mailto:jdprietom@eafit.edu.co) |
| Profesor | Edwin Nelson Montoya Munera (mailto:emontoya@eafit.edu.co) |

# 1. Objetivo

---

Diseñar e implementar un sistema que implique la captura de datos en tiempo real y el traslado de los mismos a Apache Kafka; dichos datos deberán de ser llevados a una base de datos NoSQL y a un procesador de flujos que analice los datos conforme van llegando.

# 2. Video sustentación

[https://youtu.be/nybIcgaGzqU](https://youtu.be/nybIcgaGzqU)

# 3. Aspectos solucionados y no solucionados

---

- [x]  Captura de datos en tiempo real.
- [x]  Traslado de datos a un canalizador.
- [x]  Almacenamiento de datos en una base de datos NoSQL.
- [x]  Procesamiento de flujo de datos.
- [x]  Visualización en tiempo real.

# 4. Información general del diseño

---

## Sobre los servicios

En esta sección, se explican los servicios implementados para dar solución al reto propuesto, explicado en la sección: 1. Objetivo.

| Nombre del servicio | Rol que desempeña | IP y puertos de escucha |
| --- | --- | --- |
| TradeStreaming | Usa la API de Finnhub para obtener datos en tiempo real sobre tasas del mercado y monedas ofrecidas; posteriormente, envía los datos recolectados a un tópico de Apache Kafka.   | local |
| Apache Kafka | Almacena los datos crudos consultados por el servicio de TradeStreaming. | 34.27.126.27:9092 |
| DataBricks | Lee, procesa, transforma y carga a mongoDB los datos crudos, presentes en un tópico de Apache Kafka.  | - |
| MongoDB | Almacena los datos transformados por el servicio de DataBricks. | 34.27.126.27:27017 |
| Grafana | Permite la visualización de los datos presentes en MongoDB.   | - |

# 5. Ambiente de desarrollo

---

## Estructura del código

```
.
├── DATABRICKS
│   └── src
│       └── streaming_kafka_pipeline.ipynb
├── SERVICES
│   └── docker
│       ├── kafka.yaml
│       └── mongoDB.yaml
├── TRADESTREAMING
│   ├── requirements.txt
│   └── src
│       ├── kakfa_productor.py
│       └── trades_streaming.py
└── docs
    └── Trabajo3WhitePaper.pdf
```

## Configuración de parámetros del proyecto

Para la configuración de los parámetros del proyecto utilizamos un enfoque basado en variables de entorno. Esto nos brinda la flexibilidad necesaria para adaptar nuestro proyecto a diferentes entornos.

A continuación se muestra el contenido del archivo de variables de entorno. Este archivo actúa como un mapa que controla los aspectos esenciales de la aplicación.

```python
import os

os.environ['KAFKA_SEVER'] = '34.27.126.27:9092'
os.environ['API_SECRET'] = 'clbp1vpr01qp535t12mgclbp1vpr01qp535t12n0'
```

## Paquetes y dependencias

Las dependencias requeridas para la correcta ejecución del software desarrollado son las siguientes:

```python
asttokens==2.4.1
certifi==2023.11.17
charset-normalizer==3.3.2
colorama==0.4.6
comm==0.2.0
debugpy==1.8.0
decorator==5.1.1
executing==2.0.1
finnhub-python==2.4.19
idna==3.4
ipykernel==6.26.0
ipython==8.17.2
jedi==0.19.1
jupyter_client==8.6.0
jupyter_core==5.5.0
kafka-python==2.0.2
matplotlib-inline==0.1.6
nest-asyncio==1.5.8
packaging==23.2
parso==0.8.3
platformdirs==4.0.0
prompt-toolkit==3.0.41
psutil==5.9.6
pure-eval==0.2.2
Pygments==2.17.0
python-dateutil==2.8.2
pywin32==306
pyzmq==25.1.1
requests==2.31.0
six==1.16.0
stack-data==0.6.3
tornado==6.3.3
traitlets==5.13.0
urllib3==2.1.0
wcwidth==0.2.10
websocket-client==1.6.4
```

# 6. Ambiente de ejecución

---

## Arquitectura general

En la presente sección se mostrara la arquitectura de referencia recomendada para el proyecto, la arquitectura final y los servicios de Google Cloud Platform (GCP) empleados para el despliegue eficiente y escalable.

![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/main/Proyecto3ArquitecturaStreaming/docs/img/arqui_ref.png)

![Untitled](https://raw.githubusercontent.com/spuertaf/spuertaf-st0263/041b629459a04136ad8604129a3272eafb15cae9/Proyecto3ArquitecturaStreaming/docs/img/arqui_final.svg)

## Guía de uso

La siguiente guía brindará los pasos a seguir para un correcto funcionamiento y ejecución del software.

### Instalando requisitos previos

Primeramente deberemos de instalar los programas necesarios para la ejecución del proyecto; se instalarán Git y Python y se clonará el repositorio que contiene el código correspondiente.

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

Nos dirigiremos a la carpeta con el código correspondiente y crearemos un entorno virtual, accederemos a el e instalaremos las librerías y dependencias correspondientes.

```bash
#dirigiendome al directorio de codigo
cd spuertaf-st0263/Proyecto3ArquitecturaStreaming

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

## Ejecución del programa

Finalmente podremos ejecutar el programa.

```bash
#ejecucion del programa
python ./src/trades_streaming.py
```