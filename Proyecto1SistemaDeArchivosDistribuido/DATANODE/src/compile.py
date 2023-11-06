import subprocess
import os
import configparser

# Configuración inicial
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config', '.config'))

PROTO_DIR = config['PATHS']['PROTO_DIR']
PROTO_FILE_DATA_NODE = config['PATHS']['PROTO_FILE_DATA_NODE']
PROTO_FILE_NAME_NODE = config['PATHS']['PROTO_FILE_NAME_NODE']
OUTPUT_DIR = config['PATHS']['OUTPUT_DIR']

def compile_proto_fsDataNode():
    try:
        command = ["python3",
                    "-m", "grpc_tools.protoc",
                    "-I", PROTO_DIR, f"--python_out={OUTPUT_DIR}",
                    f"--pyi_out={OUTPUT_DIR}", f"--grpc_python_out={OUTPUT_DIR}", PROTO_FILE_DATA_NODE]

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            print("Archivo .proto compilado exitosamente.")
        else:
            print("Error al compilar el archivo .proto:")
            print(result.stderr)
    except Exception as e:
        print("Ocurrió un error:", str(e))

def compile_proto_fNameNode():
    try:
        command = ["python3",
                    "-m", "grpc_tools.protoc",
                    "-I", PROTO_DIR, f"--python_out={OUTPUT_DIR}",
                    f"--pyi_out={OUTPUT_DIR}", f"--grpc_python_out={OUTPUT_DIR}", PROTO_FILE_NAME_NODE]

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            print("Archivo .proto compilado exitosamente.")
        else:
            print("Error al compilar el archivo .proto:")
            print(result.stderr)
    except Exception as e:
        print("Ocurrió un error:", str(e))

compile_proto_fsDataNode()
compile_proto_fNameNode()
