#!/bin/bash
# run this script using the following command:
# chmod +x build_wheels.sh
# ././build_wheels.sh

# Funktion zum Erstellen und Verwalten der Umgebung
create_and_build () {
    local python_version=$1
    local env_name="env_py${python_version//./}" # z.B., env_py39, env_py310

    echo "Schritt 1: Erzeuge conda environment mit Python ${python_version}"
    conda create -y -n "$env_name" python="$python_version" numpy=1.26.4 matplotlib=3.8.4 pandas=2.2.2 pip
    source activate "$env_name" || conda activate "$env_name" # Sicherstellen, dass activation command funktioniert

    echo "Installiere pip Pakete (opencv-python)"
    pip install opencv-python==4.10.0.84

    echo "Schritt 3: Erstelle wheel Dateien"
    python setup.py sdist bdist_wheel

    echo "Schritt 4: Lösche build Ordner, ausser dist"
    rm -rf PyPupilEXT.egg-info .eggs build && mkdir build

    echo "Schritt 5: Lösche die conda Environment"
    conda deactivate
    conda remove -y --name "$env_name" --all
}

# Ausführung der Schritte für Python 3.9
create_and_build "3.9"

# Ausführung der Schritte für Python 3.10
create_and_build "3.10"

# Ausführung der Schritte für Python 3.11
create_and_build "3.11"