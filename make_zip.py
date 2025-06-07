import os
import zipfile


def zip_build_directory():
    base_dir = "build/exe.win-amd64-3.13"
    zip_name = "HexAPI.zip"

    with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                filepath = os.path.join(root, file)
                arcname = os.path.relpath(
                    filepath, base_dir
                )  # chemin relatif dans le zip
                zipf.write(filepath, arcname)

    print(f"✅ Archive '{zip_name}' créée avec succès depuis '{base_dir}'.")


if __name__ == "__main__":
    zip_build_directory()
