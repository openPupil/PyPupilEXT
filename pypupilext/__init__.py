from .stereo_calibration import StereoCalibration
from .single_calibration import SingleCalibration
import os
import sys

# Dynamisch site-packages Verzeichnis bestimmen
site_packages_path = os.path.join(sys.prefix, 'lib', 'python{}.{}'.format(
    sys.version_info.major, sys.version_info.minor), 'site-packages')

# Sicherstellen, dass site-packages im Pfad ist
if site_packages_path not in sys.path:
    sys.path.append(site_packages_path)

# print(f"Current sys.path: {sys.path}")
# print(f"Current __file__ path: {os.path.abspath(__file__)}")
pypupilext_path = os.path.dirname(os.path.abspath(__file__))
# print(f"Current pypupilext directory contents: {os.listdir(pypupilext_path)}")

# Importieren der Python-Module

# Versuch, das kompiliertes Modul zu importieren
try:
    from ._pypupil import *
    print("_pypupil module successfully imported.")
except ImportError as e:
    # Erweiterte Fehlermeldung
    print(f"Failed to import _pypupil module: {e}")
    import traceback
    traceback.print_exc()
    print(
        f"Current directory contents: {os.listdir(os.path.dirname(os.path.abspath(__file__)))}")
    raise
