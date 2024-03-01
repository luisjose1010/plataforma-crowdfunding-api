import argparse
from scripts.run import run
from scripts.redoc_export import redoc_export


"""
Funcion para ejecutar las funciones de los scripts
Deben tener un parametro init y este será True, para prevenir
la ejecucion de codigo en caso de tener un decorador.
"""
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gestiona funcionalidades de la API con atajos en forma de scripts")
    parser.add_argument("arg1", type=str, help="Indica la funcion a utilizar")

    args = parser.parse_args()

    exec(f"{args.arg1}()")