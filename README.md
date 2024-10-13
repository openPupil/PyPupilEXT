# PyPupilEXT: A pupil size detection computer vision software for python
</div>
<div align="center">
 <a href="https://github.com/openPupil/Open-PupilEXT" alt="Version">
        <img src="https://img.shields.io/badge/Python-3.9%20|%203.10-blue"/></a>
 <a href="https://github.com/openPupil/Open-PupilEXT" alt="Version">
        <img src="https://img.shields.io/badge/Version-0.0.1%20Beta-green"/></a>
 <a href="https://github.com/openPupil/Open-PupilEXT" alt="Contribution">
        <img src="https://img.shields.io/badge/PR-Welcome-green"/></a>
</div>

<p align="center">
    <img src="Misc/img/StartupAnim.gif" align="center" width="55%" height="20%">
  </p>


This repository provides a python wrapper to the open-source pupillometry system PupilEXT ([Link](https://github.com/openPupil/)). The binding module is created using [Pybind11](https://github.com/pybind/pybind11). PyPupilEXT allows to measure the pupil diameter from images that were captured by stereo- and mono camera systems. The pupil diameter can be detected using one of the state-of-the-art open-source algorithms, Starburst [[1\]](#1), Swirski2D [[2\]](#2), ExCuSe [[3\]](#3), ElSe [[4\]](#4), PuRe [[5\]](#5), and PuReST [[6\]](#6).<br/>

The PyPupilEXT package is authored by Moritz Lode and Babak Zandi from the Technical University of Darmstadt..<br/>


More information about our open-source pupillometry project can be found here: [https://github.com/openPupil/Open-PupilEXT](https://github.com/openPupil/Open-PupilEXT)<br/>

## 1. Installation

### 1.1 Install PyPupilEXT using pip

This feature is forthcoming. Currently, users must compile their own wheel files to utilize PyPupilEXT (see below for instructions).

### 1.2 Build and install PyPupilEXT from source

#### Step 1: Clone this repository including the submodules

```shell
git clone --recurse-submodules https://github.com/openPupil/PyPupilEXT
```

The `--recurse-submodules` option is vital as vcpkg is nested as a submodule. Without it, the 3rdparty folder will lack the vcpkg package manager.

#### Step 2: Set up a Python environment on your machine using conda

```shell
cd PyPupilEXT
conda env create -f environment.yml
conda activate pypupilenv
```

#### Step 3: Build and install an installation wheel from source via pip

In PyPupilEXT, the pupil detection algorithms are included as C++ files. Therefore, it is necessary to load different C++ libraries to build the pupil detection algorithms. This process is fully automated with vcpkg. You only need to open the PyPupilEXT folder and call a one-liner. Note that the build process will take a while because the C++ libs need to be downloaded and compiled.

The PupilEXT project contains a vcpkg.json file in which all the required C++ libraries are defined. To download and build the libraries, we use the package management software vcpkg (https://vcpkg.io/en/index.html). We have placed the vcpkg GitHub repository as a submodule under 3rdparty/vcpkg, meaning that the required libraries will be downloaded automatically to the PupilEXT project folder, regardless of your system. This has the advantage that the PupilEXT folder can be easily deleted when the C++ libraries are no longer needed. However, as the libraries are downloaded and built, care must be taken to ensure that at least 6 GB are available on the disc for the PupilEXT folder (on windows ~13 GB).

**Instruction for macOS (Apple Silicon & Intel)**

Follow step 1 & 2. Next, make sure to install homebrew before running these commands.

```shell
brew install pkg-config
brew install cmake
brew install nasm
brew install gcc
brew install llvm
brew install libomp
brew install libmpc
brew install tree
brew install libxcb

python setup.py sdist bdist_wheel
```
Then, in the folder ``PyPupilEXT/dist``, there should be a new *.whl file, which is on a mac machine, for example ``PyPupilEXT-0.0.1-cp37-cp37m-macosx_10_15_x86_64.whl``. This file can be used to install the python package. For this, locate the dist folder and pip install it. If you experience any platform compability error, then you need to rename the file ``PyPupilEXT-0.0.1-cp37-cp37m-macosx_10_15_x86_64.whl``to ``PyPupilEXT-0.0.1-cp37-none-any.whl`

```shell
cd dist && pip install *.whl
```

**Instruction for Ubuntu**

Follow step 1 & 2. Next, make sure to install the necessary libs before running the build process.

```shell
sudo apt-get update
sudo apt-get install -y gcc g++ make cmake
sudo apt-get install -y wget git build-essential curl zip unzip tar pkg-config libopencv-dev ninja-build autoconf \
    automake libtool bison gperf libx11-dev libxft-dev libxext-dev libegl1-mesa-dev libgles2-mesa-dev libxrandr-dev \
    libglib2.0-dev libxrandr-dev libxcursor-dev libxinerama-dev libxi-dev libxcomposite-dev libatk1.0-dev libcairo2-dev libpango1.0-dev \
    libgdk-pixbuf2.0-dev libxdamage-dev nasm libomp-dev libomp5 libeigen3-dev

python setup.py sdist bdist_wheel
cd dist && pip install *.whl
```

**Instruction for Windows**

Visual Studio 2019 is required. During installation, ensure "Desktop development with C++" is selected along with the English language package. Visual Studio can be downloaded from [here](https://visualstudio.microsoft.com/downloads/).

Launch the "x64 Native Tools Command Prompt for VS 2019." Then, navigate to the PyPupilEXT folder and input the following commands:

```shell
cd PyPupilEXT
conda env create -f environment.yml
conda activate pypupilenv

python setup.py sdist bdist_wheel

cd dist
pip install <...filename.whl...>
```

### 1.3 Build and Install PyPupilEXT Using Podman or Docker Container (Automated Process)

Before starting, ensure you have Podman or Docker installed on your system. This automated method handles dependencies and builds the package in a containerized environment.

#### Step 1: Build the Image

Navigate to the PyPupilEXT directory and build the container image:

```bash
cd PyPupilEXT
podman build -t pypupilext .

# Alternatively, using Docker
# docker build -t pypupilext .
```
This command creates a container image named `pypupilext` using the Dockerfile in the current directory.

#### Step 2: Run and Start the Container

Create and start a container instance from the image:

```bash
# Create a new container and run it interactively
podman run -it --name pypupilext_container localhost/pypupilext:latest

# Alternatively, using Docker
# docker run -it --name pypupilext_container pypupilext

# Note: If the container already exists, use the following commands to start and access it
podman start pypupilext_container
podman exec -it pypupilext_container /bin/bash

# For Docker
# docker start pypupilext_container
# docker exec -it pypupilext_container /bin/bash
```

This process involves creating a container named `pypupilext_container`, starting it, and providing access to an interactive shell within the container environment.

#### Step 3: Activate the Conda Environment

After entering the container, you need to activate the preconfigured conda environment. This ensures that all necessary dependencies for PyPupilEXT are available:

```bash
conda activate pypupilenv
```

Once activated, you can utilize the `PyPupilEXT` package within this environment. For example, you can import and explore the package's functionalities:

```python
import pypupilext as pp
# Refer to example scripts for usage
```

### 1.4 Build and Install PyPupilEXT Using a Podman or Docker Container (Manual Setup)

For users interested in a hands-on approach, or for testing custom configurations, you can manually set up a Podman or Docker environment with the following steps:

#### Step 1: Start and Configure the Container

Start a container using an Ubuntu base image and install essential development tools and dependencies:

```shell
podman run -it --memory=8g --shm-size=8g --arch amd64 ubuntu:22.04 /bin/bash

apt-get update

apt-get install -y wget git build-essential cmake g++ gcc make curl zip unzip tar pkg-config libopencv-dev ninja-build libeigen3-dev autoconf automake libtool bison gperf libx11 libxft-dev libxext-dev libegl1-mesa-dev libgles2-mesa-dev libxrandr-dev
apt-get install -y libglib2.0-dev libxrandr-dev libxcursor-dev libxinerama-dev libxi-dev libxcomposite-dev libatk1.0-dev libcairo2-dev libpango1.0-dev libgdk-pixbuf2.0-dev libxdamage-dev nasm libomp-dev

apt-get clean

```

#### Step 2: Install Miniconda

Download and install Miniconda to manage Python environments effectively:

```shell
wget -O /tmp/miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod +x /tmp/miniconda.sh
/bin/bash /tmp/miniconda.sh -b -p /opt/miniconda
rm /tmp/miniconda.sh
```

#### Step 3: Clone the PyPupilEXT Repository

Retrieve the latest source code from the repository:

```shell
git clone --recurse-submodules https://github.com/openPupil/PyPupilEXT.git /PyPupilEXT
```

#### Step 4: Initialize Conda and Environment

```shell
conda init
bash # Restart shell
cd /PyPupilEXT
conda env create -f environment.yml
conda activate pypupilenv
```

#### Step 5: Build the Wheel and Install

Compile the package into a Python wheel file and install it:

```shell
cd /PyPupilEXT
python setup.py sdist bdist_wheel
pip install dist/*.whl
```

#### Additional commands for Podman that might be usefull

Save the podman image if you like

```shell
podman ps # Note the current image-id
podman commit <container_id> ubuntu-base-image-x86_64

# You can check the available images using the command
podman images
```

Start a container using an existing image

```shell
podman run -it --memory=8g --shm-size=8 --arch amd64 ubuntu-base-image-x86_64 podman run -it --arch amd64 <container_name_or_id>
```

If you like to switch to the container, you can use the following commands.

```shell
podman container ls
podman exec -it <container_name_or_id> /bin/bash
```

Other usefull commands while building the *.whl file on ubuntu

```shell
# Clean up build directories for a fresh start
rm -rf PyPupilEXT.egg-info .eggs build dist && mkdir build && cd build
```

### 1.5 The advanced way of installing PyPupilEXT when nothing works

If the build process fails, it may be due to the setup.py file. In such a case, it could be useful to compile the C++ files manually. Firstly, you need to find the path to the C++ NumPy header, which is necessary during the compilation. For this, type the following in your shell

```shell
conda activate pypupilenv
python
import numpy as np
print(np.get_include())
exit()
```

Copy the printed path, which is in my case ``/Users/papillonmac/miniconda3/envs/pypupilENV/lib/python3.7/site-packages/numpy/core/include``. This path needs to be included in the ``PyPupilEXT/CMakeLists.txt`` file. In the ``CMakeLists.txt`` file, you need to find the following line:

```cmake
set(Python_NumPy_INCLUDE_DIR "/Users/papillonmac/miniconda3/envs/TestENV/lib/python3.9/site-packages/numpy/core/include")
```

Update this path with your own path to the C++ NumPy header. Now you are ready to build the C++ files. For this, open your terminal, locate the PyPupilEXT folder and make sure you are in the right conda env as specified previously.

```shell
cd PyPupilEXT

cd build

cmake .. -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release -DVCPKG_TARGET_TRIPLET=x64-osx -DCMAKE_TOOLCHAIN_FILE=3rdparty/vcpkg/scripts/buildsystems/vcpkg.cmake

cmake --build . --config Release
```

This process will again take a while as the libs need to be downloaded and compiled. However, if you are on a Windows machine, use the following code instead:

```shell
cd PyPupilEXT

cd build

cmake .. -DCMAKE_BUILD_TYPE=Release -DVCPKG_TARGET_TRIPLET=x64-windows-static-md -DCMAKE_TOOLCHAIN_FILE=3rdparty/vcpkg/scripts/buildsystems/vcpkg.cmake

cmake --build . --config Release
```

Then, go to the ``PyPupilEXT/build`` folder and copy the ``_pypupil.cpython-37m-darwin.so`` file (it may be labeled different on your system) into the ``PyPupilEXT/pypupilext`` folder. Next, you can install the package into your python env using the following command

```shell
python -m pip install . -v
```

## 2. Examples: How to use PyPupilEXT (under construction)

PyPupilEXT contains the pupil detection algorithms Starburst [[1\]](#1), Swirski2D [[2\]](#2), ExCuSe [[3\]](#3), ElSe [[4\]](#4), PuRe [[5\]](#5), and PuReST [[6\]](#6). Each algorithm is implemented using the PupilDetectionMethod interface, exposing the function ``run`` and ``runWithConfidence`` for pupil detection on an image. The method ``runWithConfidence`` additionally applies an outline confidence measure in the range of [0, 1] on the pupil detection, accessible by the field pupil.outline_confidence.

The algorithms can be instantiated by creating objects of the classes ``ElSe, ExCuSe, PuRe, PuReST, Starburst, and Swirski2D``. Further image undistortion and stereo triangulation procedures are available in which a camera calibration from the [PupilEXT](https://github.com/openPupil/Open-PupilEXT) software platform is loaded and used to calculate undistorted images, or in the stereo camera case, a stereo triangulation of the physical pupil size.

**Example 1:** Loading an image file using OpenCV and applying a pupil detection algorithm to it:

```python
import pypupilext as pp
import cv2

algorithm = pp.PuRe()

# Images are read in grayscale, as the pupil detection algorithms usually operate on grayscale images
image = cv2.imread('tests/1.bmp', cv2.IMREAD_GRAYSCALE)

# Images can be undistorted by loading a calibration file from the PupilEXT software either creating a SingleCalibration or StereoCalibration calibration object
calibration = pp.SingleCalibration('single_calibration.xml')

# Undistort the image using the calibration object
image = calibration.undistortImage(image)

# Result of the pupil detection is a Pupil object
# pupil = algorithm.run(image)

# Run the algorithm with an outline confidence measure, which is independend of the used algorithm. A value of 1 indicates a perfect ellipse fit around the pupil's contour fit.
pupil = algorithm.runWithConfidence(image)

print(pupil.diameter())
print(pupil.outline_confidence)
# Some algorithms also deliver their own confidence measure
# print(pupil.confidence)
```

**Example 2:**  Run a pupil detection algorithm on an eye image and fit an ellipse around the pupil contour.

For this example, you can use the provided test image in this repository in ``tests/1.bmp``. Note that if you use your own images, you need to adjust the parameters of the pupil detection algorithm to match your image resolution. For this, adjust the ``pure.maxPupilDiameterMM`` and ``pure.pure.minPupilDiameterMM`` appropriately. The ``pupil.outline_confidence`` value can be used as an estimate of how well the pupil fit worked. A value of 1 indicates a perfect ellipse fit around the pupil's contour. It is also possible to adjust the parameters of pupil detection algorithm in the GUI of PupilEXT (Link: [https://github.com/openPupil/Open-PupilEXT](https://github.com/openPupil/Open-PupilEXT)) and then transfer the values into your python script.

```python
import pypupilext as pp
import cv2
import pandas as pd
import time
import matplotlib.pyplot as plt

def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]
    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))
    return cv2.resize(image, dim, interpolation=inter)

img = cv2.imread("tests/1.bmp", cv2.IMREAD_GRAYSCALE)

pupilClass = pp.Pupil()
assert pupilClass.confidence == -1

pure = pp.PuRe()
pure.maxPupilDiameterMM = 7

im_reized = img
pupil = pure.runWithConfidence(im_reized)
data = pd.DataFrame([{'Outline Conf': pupil.outline_confidence, 'PupilDiameter': pupil.diameter()}])
print(data)

img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
img_plot = cv2.ellipse(img,
                       (int(pupil.center[0]), int(pupil.center[1])),
                       (int(pupil.minorAxis()/2), int(pupil.majorAxis()/2)), pupil.angle,
                       0, 360, (0, 0, 255), 1)

resize = ResizeWithAspectRatio(img_plot, width=800)

fig = plt.figure(figsize=(20, 8))
ax1 = plt.subplot(1, 2, 1)
im1 = ax1.imshow(cv2.cvtColor(resize, cv2.COLOR_BGR2RGB))
fig.tight_layout()

plt.show()
# If you want to show the image using an opencv window instead of matplotlib
#cv2.imshow("window", resize)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
#cv2.waitKey(1)
```

## 3. Documentation PyPupilEXT

### A. PupilDetectionMethod

Class representing a pupil detection algorithm.
Each of the available algorithms, implements the following functions.

### Functions:

#### run(image)

Applies pupil detection on a given image and returns a pupil result.

Parameters:

| Name  | Description                                                  |
| ----- | ------------------------------------------------------------ |
| image | *Numpy.array*<br>Array representing an image from i.e. cv2.imread. |

##### Returns

*Pupil* object representing the pupil detection


#### runWithConfidence(image)

Applies pupil detection on a given image and returns a pupil result.
The pupil result contains an additional outline_confidence value,
representing the goodness of the detection in the range [0, 1].

Parameters:

| Name  | Description                                                  |
| ----- | ------------------------------------------------------------ |
| image | *Numpy.array*<br>Array representing an image from i.e. cv2.imread. |

##### Returns

*Pupil* object representing the pupil detection


### B. Pupil

Class representing a pupil detection result.
The pupil contains all ellipse parameter with which the pupil contour ellipse can be reconstructed.

### Fields:

| Name                | Description                                                 |
| ------------------- | ----------------------------------------------------------- |
| center              | *int*<br>Diameter of the ellipse defined as its major axis. |
| undistortedDiameter | *int*<br>Diameter of the ellipse defined as its major axis. |
| physicalDiameter    | *int*<br>Diameter of the ellipse defined as its major axis. |
| eyelid              | *int*<br>Diameter of the ellipse defined as its major axis. |
| size                | *int*<br>Diameter of the ellipse defined as its major axis. |
| angle               | *int*<br>Diameter of the ellipse defined as its major axis. |
| confidence          | *int*<br>Diameter of the ellipse defined as its major axis. |
| outline_confidence  | *int*<br>Diameter of the ellipse defined as its major axis. |

### C. Functions:

| Name                        | Returns, Description                                         |
| --------------------------- | ------------------------------------------------------------ |
| rectPoints()                | *list*<br>Returns list of point tuples, representing the corner points of the ellipse rectangle (bounding box). |
| shift(point)                | *None*<br>Shifts the pupil center according to the given point. |
| valid(confidence_threshold) | *bool*<br>Checks wherever the pupil is valid based on a given confidence threshold, and size of the ellipse > 0. |
| resize(x, y)                | *int*<br>Scale the pupil ellipse by the given factors.       |
| width()                     | *int*<br>Width of the ellipse defined as the width of the ellipse rectangle. |
| height()                    | *int*<br>Height of the ellipse defined as the width of the ellipse rectangle. |
| diameter()                  | *int*<br>Diameter of the ellipse defined as its major axis.  |
| majorAxis()                 | *int*<br>Large value of the two fields width and height.     |
| majorAxis()                 | *int*<br>Smaller value of the two fields width and height.   |
| circumference()             | *float*<br>Circumference of the ellipse.                     |
| clear()                     | *None*<br>Resets the pupil ellipse parameter to -1 (invalid). A reset pupil always returns false on valid(). |

### D. SingleCalibration

Class representing a calibration for a single camera.
Images undistorted by this object must be recorded by the same camera for which the calibration was loaded.

### Functions:

#### __init__(calibration_file)

Loads a given calibration file for a single camera. The calibration file should be in OpenCV's file storage format and be created using the PupilEXT software for correct formats.

Parameters:

| Name             | Description                                                |
| ---------------- | ---------------------------------------------------------- |
| calibration_file | *S*tr<br>Path to the calibration file for a single camera. |




#### undistortImage(image)

Applies image undistortion on a given image and returns the new undistorted image.
If no valid calibration is loaded, the unchanged image is returned.

Parameters:

| Name  | Description                                                  |
| ----- | ------------------------------------------------------------ |
| image | *Numpy.array*<br>Array representing an image from i.e. cv2.imread. |

##### Returns

Image undistorted.

#### undistortPupilSize(pupil)

Applies point undistortion on a given detected pupil and returns the undistorted pupil size.
If no valid calibration is loaded, the unchanged pupil size is returned.

This method is faster than complete image distortion as only contour points of the pupil are undistorted.

Parameters:

| Name  | Description                                                  |
| ----- | ------------------------------------------------------------ |
| pupil | *Pupil*<br>Array representing an image from i.e. cv2.imread. |

##### Returns

Pupil size undistorted, float

### E. StereoCalibration

Class representing a calibration for a stereo camera system.
Images undistorted by this object must be recorded by the same camera system for which the calibration was loaded.

### Functions:

#### __init__(calibration_file)

Loads a given calibration file for a single camera. The calibration file should be in OpenCV's file storage format and be created using the PupilEXT software for correct formats.

Parameters:

| Name             | Description                                                |
| ---------------- | ---------------------------------------------------------- |
| calibration_file | *S*tr<br>Path to the calibration file for a single camera. |




#### undistortImages(image, image_secondary)

Applies image undistortion on a given set of images and returns the new undistorted images.
If no valid calibration is loaded, the unchanged images are returned.

Image describes the image from the main camera, image_secondary from the secondary camera in the stereo system.

Parameters:

| Name            | Description                                                  |
| --------------- | ------------------------------------------------------------ |
| image           | *Numpy.array*<br>Array representing an image from i.e. cv2.imread. |
| image_secondary | *Numpy.array*<br/>Array representing an image from i.e. cv2.imread. |

##### Returns

Images undistorted, tuple

#### undistortPupilSizes(pupil, pupil_secondary)

Applies point undistortion on a given detected pupils and returns the undistorted pupil sizes.
If no valid calibration is loaded, the unchanged pupil sizes are returned.

This method is faster than complete image distortion as only contour points of the pupil are undistorted.

Parameters:

| Name            | Description                                                  |
| --------------- | ------------------------------------------------------------ |
| pupil           | *Pupil*<br/>Array representing an image from i.e. cv2.imread. |
| pupil_secondary | *Pupil*<br>Array representing an image from i.e. cv2.imread. |

##### Returns

Pupil sizes undistorted, tuple of floats

#### triangulatePupilSize(pupil, pupil_secondary)

Based on the pupil detection on a set of stereo images capturing the pupil at the same time, the function triangulates the two pupil contours and returns a physical pupil size in *mm*. (Or whatever metric was used in the calibration)

If no valid calibration was loaded, or one of the two pupil detections were invalid, the value -1 is returned.

Parameters:

| Name            | Description                                                  |
| --------------- | ------------------------------------------------------------ |
| pupil           | *Pupil*<br/>Array representing an image from i.e. cv2.imread. |
| pupil_secondary | *Pupil*<br>Array representing an image from i.e. cv2.imread. |

##### Returns

Physical pupil size, float

## 4. Developer Notes: Create relase in GithUb

Example:

Change the version number inside the following files:
- Create a new file in the folder realese_notes, conataining the notes.
- Change the version in the file setup.py
- Change `body_path: release_notes/release_notes_v0.0.1.md`` in .github/workflows/action.yml

```bash
# Hinzufügen einer Datei mit der bezeichnung release_notes_v0.0.1.md in release_notes/
git commit -m "Release v1.0.0: Initial version with major features"
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

## 5. Citation
Please consider to cite our work if you find this repository  useful for your research:

B. Zandi, M. Lode, A. Herzog, G. Sakas, and T. Q. Khanh, “PupilEXT: Flexible Open-Source Platform for High-Resolution Pupillometry in Vision Research,” Front. Neurosci., vol. 15, Jun. 2021, doi: 10.3389/fnins.2021.676220.

```bib
@Article{10.3389/fnins.2021.676220,
AUTHOR = {Zandi, Babak and Lode, Moritz and Herzog, Alexander and Sakas, Georgios and Khanh, Tran Quoc},
TITLE = {PupilEXT: Flexible Open-Source Platform for High-Resolution Pupillometry in Vision Research},
JOURNAL = {Frontiers in Neuroscience},
VOLUME={15},
PAGES={603},
YEAR={2021},
URL={https://www.frontiersin.org/article/10.3389/fnins.2021.676220},
DOI={10.3389/fnins.2021.676220},
ISSN={1662-453X}}
```


## 5. References
<a id="1">**[1]**</a> Dongheng Li and Derrick J. Parkhurst. Starburst: A robust algorithm for video-based eye tracking. IEEE Computer Society Conference on Computer Vision and Pattern Recognition (CVPR), September 2005.

<a id="2">**[2]**</a> Lech Swirski, Andreas Bulling, and Neil Dodgson. Robust real-time pupil tracking in highly off-axis images. In Proceedings - 2012 ACM Symposium on Eye Tracking Research and Applications (ETRA), pages 173–176, 2012.

<a id="3">**[3]**</a> Wolfgang Fuhl, Thomas Kübler, Katrin Sippel, Wolfgang Rosenstiel, and Enkelejda Kasneci. Excuse: robust pupil detection in real-world scenarios. In International Conference on Computer Analysis of Images and Patterns, pages 39–51. Springer, 2015.

<a id="4">**[4]**</a> Wolfgang Fuhl, Thiago C. Santini, Thomas Kübler, and Enkelejda Kasneci. ElSe: Ellipse selection for robust pupil detection in real-world environments. In Proceedings - 2016 ACM Symposium on Eye Tracking Research and Applications (ETRA), volume 14, pages 123–130, 2016.

<a id="5">**[5]**</a> Thiago Santini, Wolfgang Fuhl, and Enkelejda Kasneci. PuRe: Robust pupil detection for real-time pervasive eye tracking. Computer Vision and Image Understanding, 170:40–50, 2018.

<a id="6">**[6]**</a> Thiago Santini, Wolfgang Fuhl, and Enkelejda Kasneci. PuReST: Robust pupil tracking for real-time pervasive eye tracking. In Proceedings - 2018 ACM Symposium on Eye Tracking Research and Applications (ETRA). ACM, 2018.

<a id="7">**[7]**</a> Thiago Santini, Wolfgang Fuhl, David Geisler and Enkelejda Kasneci. EyeRecToo: Open-source Software for Real-time Pervasive Head-mounted Eye Tracking. VISIGRAPP 2017.

## 6. Open source projects inside PupilEXT

PyPupilEXT integrates several open source libraries. This document provides a list of the used libraries. The respective licenses of the libraries are provided as *.txt file in in the subfolder `3rdparty/PupilEXT_Third_Party_Licenses`.

### List of Pupil Detection Libraries

<a id="EyeRecToo" href="https://github.com/tcsantini/EyeRecToo"><b>EyeRecToo</b></a> is an open-source eye tracking software for head-mounted eye tracker and integrates the most advanced state-of-the-art open-source pupil detection algorithms.  We used the implementation of the EyeRecToo’s pupil class and the integrated detection methods for PupilEXT. (License: Copyright (c) 2018, Thiago Santini / University of Tübingen). **License:** For academic and non-commercial use only ([Link License](https://github.com/tcsantini/EyeRecToo/blob/master/LICENSE) | [Project Page](https://github.com/tcsantini/EyeRecToo)).

<a id="PuRe" href="https://www.sciencedirect.com/science/article/abs/pii/S1077314218300146?via%3Dihub"><b>PuRe</b></a> Thiago Santini, Wolfgang Fuhl, Enkelejda Kasneci, PuRe: Robust pupil detection for real-time pervasive eye tracking. *Computer Vision and Image Understanding*. **2018**, ISSN 1077-3142. https://doi.org/10.1016/j.cviu.2018.02.002. Part of the [EyeRecToo](https://github.com/tcsantini/EyeRecToo) software. Copyright (c) 2018, Thiago Santini, University of Tübingen. **License:** For non-commercial purposes only ([Link](https://github.com/tcsantini/EyeRecToo/blob/master/EyeRecToo/src/pupil-detection/PuRe.h)).

<a id="PuReST" href="https://github.com/tcsantini/EyeRecToo/blob/master/EyeRecToo/src/pupil-tracking/PuReST.h"><b>PuReST</b></a> Thiago Santini, Wolfgang Fuhl, Enkelejda Kasneci. PuReST: Robust pupil tracking for real-time pervasive eye tracking. *Symposium on Eye Tracking Research and Applications (ETRA)*. **2018**. https://doi.org/10.1145/3204493.3204578. Part of the [EyeRecToo](https://github.com/tcsantini/EyeRecToo) software. Copyright (c) 2018, Thiago Santini, University of Tübingen. **License:** For non-commercial purposes ([Link](https://github.com/tcsantini/EyeRecToo/blob/master/EyeRecToo/src/pupil-tracking/PuReST.h)).

<a id="ElSe" href="https://dl.acm.org/doi/10.1145/3204493.3204578"><b>ElSe</b></a> Wolfgang Fuhl, Thiago Santini, Thomas Kübler, Enkelejda Kasneci. ElSe: Ellipse Selection for Robust Pupil Detection in Real-World Environments. *ETRA 2016 : Eye Tracking Research and Application.* **2016.** Part of the [EyeRecToo](https://github.com/tcsantini/EyeRecToo) software. Copyright (c) 2018, Thiago Santini, University of Tübingen. **License:** For non-comercial use only ([Link](https://github.com/tcsantini/EyeRecToo/blob/master/EyeRecToo/src/pupil-detection/ElSe.h)).

<a id="ExCuSe" href="https://link.springer.com/chapter/10.1007/978-3-319-23192-1_4"><b>ExCuSe</b></a> Wolfgang Fuhl, Thomas Kübler, Katrin Simpel, Wolfgang Rosenstiel, Enkelejda Kasneci. ExCuSe: Robust Pupil Detection in Real-World Scenarios. *CAIP 2015 : Computer Analysis of Images and Patterns*. **2015**. Part of the [EyeRecToo](https://github.com/tcsantini/EyeRecToo) software. Copyright (c) 2018, Thiago Santini, University of Tübingen. **License:** For non-comercial use only ([Link](https://github.com/tcsantini/EyeRecToo/blob/master/EyeRecToo/src/pupil-detection/ExCuSe.h)).

<a id="Starburst" href="https://ieeexplore.ieee.org/document/1565386"><b>Starburst</b></a> Dongheng Li, Winfield, D., Parkhurst, D. J. Starburst: A hybrid algorithm for video-based eye tracking combining feature-based and model-based approaches. in *2005 IEEE Computer Society Conference on Computer Vision and Pattern Recognition (CVPR’05) - Workshops* vol. 3 79–79 (IEEE, 2005). https://doi.org/10.1109/CVPR.2005.531. Based on the [cvEyeTracker](https://github.com/thirtysixthspan/cvEyeTracker) Version 1.2.5 implementation. **License:** GNU General Public License ([Link](https://github.com/thirtysixthspan/cvEyeTracker/blob/master/ransac_ellipse.cpp))

<a id="Swirski2D" href="https://dl.acm.org/doi/10.1145/2168556.2168585"><b>Swirski2D</b></a>  Lech Swirski, Andreas Bulling, Neil Dodgson. Robust real-time pupil tracking in highly off-axis images. *ETRA 2012: Proceedings of the Symposium on Eye Tracking Research and Applications*. **2012**. https://doi.org/10.1145/2168556.2168585.  **License:** MIT License, Copyright (c) 2014 Lech Swirski ([Link](https://github.com/LeszekSwirski/pupiltracker/blob/master/LICENSE.md))

<a id="Swirski3D" href="https://www.cl.cam.ac.uk/research/rainbow/projects/eyemodelfit/"><b>Swirski2D</b></a> Lech Swirski, Neil Dodgson. A fully-automatic, temporal approach to single camera, glint-free 3D eye model fitting. *Proceedings of ECEM 2013*. **2013**.  **License:** MIT License, Copyright (c) 2014 Lech Swirski ([Link](https://github.com/LeszekSwirski/singleeyefitter/blob/master/LICENSE.md))

### List of Software Libraries

<a id="QT" href="https://www.qt.io/"><b>QT</b></a>  is an open-source widget toolkit for creating graphical user interfaces as well as cross-platform applications that run on various software and hardware platforms such as Linux, Windows, macOS, Android or embedded systems. (License: GPL 3.0)

<a id="QCustomPlot" href="https://www.qcustomplot.com/"><b>QCustomPlot</b></a> is a Qt C++ widget for plotting and data visualization. It has no further dependencies and is well documented. (License: GPL 3.0)

<a id="OpenCV" href="https://opencv.org/"><b>OpenCV</b></a> is a highly optimized computer vision library with focus on real-time applications. In this repository it is used for image manipulation and plotting of ellipse pupil detections. (License: Apache 2 / BSD)

<a id="Glog" href="https://github.com/google/glog"><b>Glog</b></a> is a library for logging. ([License](https://github.com/google/glog/blob/master/COPYING))

<a id="Boost" href="https://www.boost.org"><b>Boost</b></a> is a set of various C++ libraries for processing tasks. ([License](https://www.boost.org/users/license.html))

<a id="Ceres-Solver" href="http://ceres-solver.org"><b>Ceres-Solver</b></a> is a optimisation library. ([License](https://github.com/ceres-solver/ceres-solver/blob/master/LICENSE))

<a id="Eigen" href="https://eigen.tuxfamily.org/index.php?title=Main_Page#License"><b>Eigen</b></a> is a library for linear algebra. ([License](https://eigen.tuxfamily.org/index.php?title=Main_Page#License))

<a id="Spii" href="https://github.com/PetterS/spii"><b>Spii</b></a> is a library for optimisation. ([License](https://github.com/PetterS/spii/blob/master/LICENSE))

<a id="Tbb" href="https://github.com/oneapi-src/oneTBB"><b>Tbb</b></a> is for parallel programming. ([License](https://github.com/oneapi-src/oneTBB/blob/master/LICENSE.txt))

<a id="Breeze-Icons" href="https://github.com/KDE/breeze-icons"><b>Breeze Icons</b></a> is a set of icons. ([License](https://github.com/KDE/breeze-icons/blob/master/icons/LICENSE))

<a id="Gflags" href="https://github.com/gflags/gflags"><b>Gflags</b></a> is a library for comandline processing. ([License](https://github.com/gflags/gflags/blob/master/COPYING.txt))

<a id="Pybind11" href="https://github.com/pybind/pybind11"><b>pybind11</b></a> is a lightweight header-only library that exposes C++ types in Python and vice versa, mainly to create Python bindings of existing C++ code. In this repository it is used to create Python bindings for the C++ pupil detection algorithm implementation. ([License](https://github.com/pybind/pybind11/blob/master/LICENSE))

## 7. Acknowledgment
We thank the German Research Foundation (DFG) by funding the research (grant number: 450636577).

This project was made possible by the outstanding previous published open-source projects in the field of pupil detection and eye-tracking. Therefore, we would like to thank the authors of the ground-breaking algorithms PuRe, PuReST, ElSe, ExCuSe, Starburst and Swirski, who made their methods available to the public. Namely, we have to thank Wolfgang Fuhl, Thiago Santini, Thomas Kübler, Enkelejda Kasneci, Katrin Sippel, Wolfgang Rosenstiel, Dongheng Li, D. Winfield, D. Parkhurst, Lech Swirski, Andreas Bulling and Neil Dodgson for their open-source contributions which are part of PyPupilEXT. Additionally, we would like to thank the outstanding developers of the software EyeRecToo, whose open-source eye-tracking software inspired us for this work. We used the implementation of the EyeRecToo’s pupil class and the integrated detection methods for PyPupilEXT.

## 8. License

The software PyPupilEXT is licensed under [GNU General Public License v.3.0.](https://github.com/openPupil/Open-PupilEXT/blob/main/Misc/LICENSE), Copyright (c) 2021 Technical University of Darmstadt. The pupil detection functionalities of PyPupilEXT are for academic and **non-commercial** use only. Please note that third-party libraries used in PyPupilEXT may be distributed under other open-source licenses. Please read the above section about the open source projects inside PyPupilEXT.

This program is distributed in the hope that it will be useful, but without any warranty, without even the implied warranty of fitness for a particular purpose.
