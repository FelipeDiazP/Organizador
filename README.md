# 📁 File Organizer

Script de automatización desarrollado en Python que organiza archivos automáticamente según su extensión.

## 🚀 Características

- Organiza imágenes, documentos, música y videos.
- Envía archivos desconocidos a `Otros`.
- Permite seleccionar cualquier carpeta.
- Evita sobrescribir archivos existentes.
- Permite ejecutar el programa en modo simulación con `--dry-run`.
- Muestra estadísticas de los archivos organizados.
- Muestra el tiempo de ejecución.
- Permite configurar las extensiones mediante `config.json`.

## 🛠️ Tecnologías

- Python 3
- pathlib
- shutil
- argparse
- json
- time

## 📂 Estructura

```text
organizador/
├── organizer.py
├── config.json
├── README.md
├── .gitignore
└── test-files/