#!/bin/bash

# actualizando todas las dependencias
sudo apt-get update
echo "[x] Todas las dependencias actualizadas!"


#instalando git
sudo apt-get install git
echo "[x] Git instalado"

#instalando python
sudo apt install python3
echo "[x] Python instalado"

#clonando repositorio del codigo
git clone https://github.com/spuertaf/spuertaf-st0263.git
echo "[x] Repositorio de codigo clonado"

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
