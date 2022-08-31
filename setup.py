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

import os
import re
import sys
import subprocess
import platform

from distutils.version import LooseVersion
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

import numpy as np


class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=""):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def run(self):
        try:
            out = subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError("CMake must be installed to build the following extensions: " +
                               ", ".join(e.name for e in self.extensions))

        if platform.system() == "Windows":
            cmake_version = LooseVersion(re.search(r'version\s*([\d.]+)', out.decode()).group(1))
            if cmake_version < '3.1.0':
                raise RuntimeError("CMake >= 3.1.0 is required on Windows")

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))

        #cfg = 'Debug' if self.debug else 'Release'
        cfg = 'Release'  # We build only in release mode
        cmake_args = [
            '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={}'.format(extdir),
            '-DPYTHON_EXECUTABLE={}'.format(sys.executable),
            '-DEXAMPLE_VERSION_INFO={}'.format(self.distribution.get_version()),
            '-DCMAKE_BUILD_TYPE={}'.format(cfg),  # not used on MSVC, but no harm
            '-DCMAKE_TOOLCHAIN_FILE=3rdparty/vcpkg/scripts/buildsystems/vcpkg.cmake',
            '-DPython_NumPy_INCLUDE_DIR={}'.format(np.get_include()),
            '-DTBB_TEST=OFF',
            '-DTBBMALLOC_BUILD=OFF'
            '-DTBBMALLOC_PROXY_BUILD=OFF'
            '-DBUILD_SHARED_LIBS=OFF']

        build_args = ['--config', cfg]

        if platform.system() == "Windows":
            cmake_args += ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}'.format(cfg.upper(), extdir)]
            build_args += ['--', '/m']
            cmake_args += ['-DVCPKG_TARGET_TRIPLET=x64-windows-static-md']
        else:
            cmake_args += ['-DCMAKE_BUILD_TYPE=' + cfg]
            build_args += ['--', '-j2']

        if platform.system() == "Darwin":
            cmake_args += ['-DVCPKG_TARGET_TRIPLET=x64-osx']

        if platform.system() == "Linux":
            cmake_args += ['-DVCPKG_TARGET_TRIPLET=x64-linux']

        env = os.environ.copy()
        env['CXXFLAGS'] = '{} -DVERSION_INFO=\\"{}\\"'.format(env.get('CXXFLAGS', ''),
                                                              self.distribution.get_version())
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        subprocess.check_call(['cmake', ext.sourcedir] + cmake_args, cwd='build/',
                              env=env)  # Previously: cwd=self.build_temp
        subprocess.check_call(['cmake', '--build', '.'] + build_args, cwd='build/')


version = 'dev'

commit_var = 'APPVEYOR_REPO_COMMIT'
tag_name_var = 'APPVEYOR_REPO_TAG_NAME'

if commit_var in os.environ and os.environ[commit_var]:
    version = "0.0.0-" + os.environ[commit_var]

if tag_name_var in os.environ and os.environ[tag_name_var]:
    version = os.environ[tag_name_var]


setup(
    name="PyPupilEXT",
    version="0.0.1",
    author="Moritz Lode, Babak Zandi",
    author_email="",
    description="Pupil detection library for Python inlcuding algorithms and camera calibration routines.",
    long_description="",
    ext_modules=[CMakeExtension("pypupilext._pypupil")],
    cmdclass={"build_ext": CMakeBuild},
    zip_safe=False,
    packages=['pypupilext'],
    setup_requires=['cmake', 'wheel'],
    install_requires=[
        'numpy',
        'opencv-python'
    ],
    python_requires='>=3.7',
    include_package_data=True,
    package_data={'pypupilext': ['*.dylib']},
)
