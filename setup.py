# -*- coding: utf-8 -*-
# The following GitHub repos were used for this setup.py file
# Used the example in https://github.com/pybind/cmake_example/blob/master/setup.py
# License: https://github.com/pybind/cmake_example/blob/master/LICENSE

# Used the modification in the "class CMakeBuild(build_ext):" from https://github.com/edmBernard/pybind11_opencv_numpy/blob/master/setup.py
# License: https://github.com/edmBernard/pybind11_opencv_numpy/blob/master/LICENSE

# Used also the adaptation from
# https://github.com/safijari/apriltags2_ethz/blob/master/setup.py
# License: https://github.com/safijari/apriltags2_ethz/blob/master/LICENSE

# Update 05/2022
# To fully automate the build process mostly the code from the following GitHub repo was used
# https://github.com/safijari/apriltags2_ethz/blob/master/setup.py
# License: https://github.com/safijari/apriltags2_ethz/blob/master/LICENSE

import sys
import os
import platform
import subprocess

from packaging.version import Version
from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext

import numpy as np


def get_system_architecture():
    """
    Determine the VCPKG_TARGET_TRIPLET and CMAKE_OSX_ARCHITECTURES based on host OS.
    """
    system = platform.system()
    machine = platform.machine()

    if system == "Darwin":
        if machine == "arm64":
            return "arm64-osx", "arm64"
        else:
            return "x64-osx", "x86_64"
    elif system == "Linux":
        return "x64-linux", "x86_64"
    elif system == "Windows":
        return "x64-windows-static-md", "x86_64"
    else:
        raise RuntimeError(f"Unsupported platform: {system}")


class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        super().__init__(name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def run(self):
        try:
            out = subprocess.check_output(['cmake', '--version'])
            print(out.decode())
        except OSError:
            raise RuntimeError("CMake must be installed to build the following extensions: "
                               ", ".join(e.name for e in self.extensions))

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(
            self.get_ext_fullpath(ext.name)))
        cmake_args = [
            '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={}'.format(extdir),
            '-DPYTHON_EXECUTABLE={}'.format(sys.executable),
            '-DVERSION_INFO={}'.format(self.distribution.get_version()),
            '-DCMAKE_BUILD_TYPE=Release',
            '-DCMAKE_TOOLCHAIN_FILE=3rdparty/vcpkg/scripts/buildsystems/vcpkg.cmake',
            f'-DVCPKG_TARGET_TRIPLET={vcpkg_triplet}',
            '-DPython_NumPy_INCLUDE_DIR={}'.format(np.get_include()),
            '-DTBB_TEST=OFF',
            '-DTBBMALLOC_BUILD=OFF',
            '-DTBBMALLOC_PROXY_BUILD=OFF',
            '-DBUILD_SHARED_LIBS=OFF'
        ]

        if osx_arch:
            cmake_args.append('-DCMAKE_OSX_ARCHITECTURES={}'.format(osx_arch))

        build_args = ['--config', 'Release']

        if platform.system() == "Windows":
            cmake_args += [
                '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_RELEASE={}'.format(extdir)]
            build_args += ['--', '/m']
        else:
            cmake_args += ['-DCMAKE_BUILD_TYPE=Release']
            build_args += ['--', '-j1']

        env = os.environ.copy()
        env['VCPKG_TARGET_TRIPLET'] = vcpkg_triplet

        if osx_arch:
            env['CMAKE_OSX_ARCHITECTURES'] = osx_arch
        else:
            env['CMAKE_SYSTEM_PROCESSOR'] = osx_arch

        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)

        subprocess.check_call(['cmake', ext.sourcedir] +
                              cmake_args, cwd=self.build_temp, env=env)
        subprocess.check_call(['cmake', '--build', '.'] +
                              build_args, cwd=self.build_temp)


vcpkg_triplet, osx_arch = get_system_architecture()

setup(
    name='PyPupilEXT',
    version='0.0.1',
    author='Moritz Lode, Babak Zandi',
    author_email='',
    description='Pupil detection library for Python including algorithms and camera calibration routines.',
    long_description='',
    ext_modules=[CMakeExtension('pypupilext._pypupil', sourcedir='')],
    cmdclass={'build_ext': CMakeBuild},
    zip_safe=False,
    packages=find_packages(),
    setup_requires=['wheel', 'cmake'],
    install_requires=[
        'numpy',
        'opencv-python'
    ],
    python_requires='>=3.7',
    include_package_data=True,
    package_data={'pypupilext': ['*.so', '*.dylib']}
)
