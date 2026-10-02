from pathlib import Path
import shutil
import argparse
import time
import json


def load_config():

    config_file = Path(__file__).parent / "config.json"

    with open(config_file, "r", encoding="utf-8") as file:

        return json.load(file)


def get_arguments():

    parser = argparse.ArgumentParser(
        description="Organiza archivos automáticamente por extensión."
    )

    parser.add_argument("folder", help="Carpeta que contiene los archivos a organizar.")

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Muestra qué archivos se organizarían sin moverlos.",
    )

    return parser.parse_args()


def create_categories(folder, categories):

    for category in categories:

        destination = folder / category

        destination.mkdir(exist_ok=True)


def is_category_folder(file, categories):

    return file.is_dir() and file.name in categories


def get_unique_destination(destination):

    if not destination.exists():

        return destination

    counter = 1

    while True:

        new_name = f"{destination.stem}_{counter}{destination.suffix}"

        new_destination = destination.parent / new_name

        if not new_destination.exists():

            return new_destination

        counter += 1


def organize_files(folder, dry_run, categories):

    organized_count = 0

    stats = {category: 0 for category in categories}

    for file in folder.iterdir():

        if is_category_folder(file, categories):
            continue

        if not file.is_file():
            continue

        extension = file.suffix.lower()

        category_found = False

        for category, extensions in categories.items():

            if extension in extensions:

                destination = folder / category

                new_destination = get_unique_destination(destination / file.name)

                if dry_run:

                    print(f"{file.name} → {category}")

                else:

                    shutil.move(str(file), str(new_destination))

                    print(f"{file.name} → {category}")

                organized_count += 1
                stats[category] += 1

                category_found = True

                break

        if not category_found:

            destination = folder / "Otros"

            new_destination = get_unique_destination(destination / file.name)

            if dry_run:

                print(f"{file.name} → Otros")

            else:

                shutil.move(str(file), str(new_destination))

                print(f"{file.name} → Otros")

            organized_count += 1
            stats["Otros"] += 1

    return organized_count, stats


def main():

    print("================================")
    print("        FILE ORGANIZER")
    print("================================")
    print()

    args = get_arguments()

    start_time = time.perf_counter()

    categories = load_config()

    folder = Path(args.folder)

    if not folder.exists():

        print("❌ La carpeta no existe.")

        return

    if not folder.is_dir():

        print("❌ La ruta indicada no es una carpeta.")

        return

    print(f"📁 Carpeta: {folder}")
    print()

    if args.dry_run:

        print("🔎 Modo simulación")
        print("No se modificarán archivos ni carpetas.")
        print()

    else:

        create_categories(folder, categories)

        print("📦 Moviendo archivos...")
        print()

    organized_count, stats = organize_files(folder, args.dry_run, categories)

    end_time = time.perf_counter()

    elapsed_time = end_time - start_time

    print()
    print("================================")
    print("          RESULTADO")
    print("================================")
    print()

    for category, count in stats.items():

        print(f"{category}: {count}")

    print()
    print(f"Total: {organized_count}")
    print(f"Tiempo de ejecución: {elapsed_time:.4f} segundos")

    print("================================")


if __name__ == "__main__":
    main()
