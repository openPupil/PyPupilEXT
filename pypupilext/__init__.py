import os
import sys

from .single_calibration import SingleCalibration
from .stereo_calibration import StereoCalibration

try:
    from ._pypupil import *
    print("_pypupil module successfully imported.")
except ImportError as e:
    print(f"Failed to import _pypupil module: {e}")
    raise
