import json
import os
from contextlib import contextmanager
from pathlib import Path
from tempfile import NamedTemporaryFile


CARPETA = Path(__file__).resolve().parent / "archivos"
PADRON = CARPETA / "matriz_alumnos.txt"
CURSADAS = CARPETA / "cursadas.jsonl"


@contextmanager
def reemplazo(ruta):
    """Publica el temporal solo después de escribirlo y cerrarlo sin errores."""
    archivo = NamedTemporaryFile(mode="w", dir=ruta.parent, delete=False, encoding="utf-8")
    try:
        with archivo:
            yield archivo
        os.replace(archivo.name, ruta)
    finally:
        Path(archivo.name).unlink(missing_ok=True)


class Padron:
    """Cada recorrido abre el TXT y entrega un estudiante por vez."""

    def __iter__(self):
        with PADRON.open(encoding="utf-8-sig") as archivo:
            for numero, linea in enumerate(archivo, 1):
                if linea.strip():
                    campos = linea.strip().split(",")
                    if len(campos) not in (2, 3) or (len(campos) == 3 and campos[2].strip() not in ("Activo", "Inactivo")):
                        raise ValueError(f"Registro incorrecto en la línea {numero} del padrón.")
                    legajo, nombre = int(campos[0]), campos[1].strip()
                    if legajo <= 0 or not nombre.replace(" ", "").isalpha():
                        raise ValueError(f"Estudiante inválido en la línea {numero}.")
                    yield [legajo, nombre]

    def agregar(self, legajo, nombre):
        with reemplazo(PADRON) as destino:
            for actual, registrado in self:
                if actual == legajo:
                    raise ValueError("El legajo ya está registrado.")
                destino.write(f"{actual},{registrado}\n")
            destino.write(f"{legajo},{nombre}\n")

    def cambiar_nombre(self, legajo, nombre):
        with reemplazo(PADRON) as destino:
            for actual, anterior in self:
                destino.write(f"{actual},{nombre if actual == legajo else anterior}\n")


def registros():
    with CURSADAS.open(encoding="utf-8") as archivo:
        for numero, linea in enumerate(archivo, 1):
            try:
                yield json.loads(linea)
            except json.JSONDecodeError as error:
                raise ValueError(f"JSON inválido en la línea {numero} de cursadas.") from error


def escribir(destino, registro):
    destino.write(json.dumps(registro, ensure_ascii=False) + "\n")


def agregar_registro(registro):
    with CURSADAS.open("a", encoding="utf-8") as destino:
        escribir(destino, registro)


def obtener_grupo(materia, nombre):
    for registro in registros():
        if registro.get("materia") == materia and registro.get("nombre") == nombre:
            return registro["datos"]
    raise ValueError("El grupo seleccionado ya no existe.")


def actualizar(materia_actual=None, nombre_actual=None, **cambios):
    # Una materia renombrada también cambia de nombre en sus registros de grupo.
    encontrado = False
    with reemplazo(CURSADAS) as destino:
        for registro in registros():
            if registro.get("materia") == materia_actual and (nombre_actual is None or registro.get("nombre") == nombre_actual):
                registro.update(cambios)
                encontrado = True
            escribir(destino, registro)
        if not encontrado:
            raise ValueError("No se encontró el registro que se quería actualizar.")


@contextmanager
def editar_grupo(materia, nombre):
    grupo = obtener_grupo(materia, nombre)
    anterior = json.dumps(grupo)
    yield grupo
    if json.dumps(grupo) != anterior:
        actualizar(materia, nombre, datos=grupo)
