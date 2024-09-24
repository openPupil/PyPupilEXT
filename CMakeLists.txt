# Description
# When using find_package() it will search in the CMAKE_MODULE_PATH to find the Find<package-name>.cmake file of a lib
# When using find_package(<package-name> REQUIRED) , it will throw an error, if the package whas not found.
# When a package is found several env variables will be set: <package-name>_FOUND, <package-name>_INCLUDE_DIR, <package-name>_LIBRARIES, <package-name>_LINK_DIRECTORIES
# Source: http://wiki.icub.org/wiki/CMake_and_FIND_PACKAGE
# When using find_package() in config mode, the <package-name>Config.cmake must be added together with find_package(<package-name> CONFIG REQUIRED)
# CMAKE_PREFIX_PATH --> is the base folder for the search engine
# CMAKE_MODULE_PATH --> for find <package-name>.cmake. Note cmake does not search in CMAKE_PREFIX_PATH for <package-name>.cmake
# <package-name>_DIR --> It will be searched there for the <package-name>config.cmake file
# The variables should be chained together with the following command set(CMAKE_PREFIX_PATH ${CMAKE_PREFIX_PATH} "${PROJECT_SOURCE_DIR}/build/vcpkg_installed/${VCPKG_TARGET_TRIPLET}/share/opencv")
# In the modern way it can also be used list(APPEND CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake")

# A value can be set with set(OpenCV_INCLUDE_DIR "${PROJECT_SOURCE_DIR}/build/vcpkg_installed/${VCPKG_TARGET_TRIPLET}/include/")
# Messages can be printed out with message(STATUS "OpenCV library status:")

# The folders can be checked after compilation in the CMakeCache.txt in the build folder to check if anything is pointed correctly

# During build it is important to set the VCPKG_TARGET_TRIPLET env variable

cmake_minimum_required(VERSION 3.15)
project(PupilEXT)

#set(CMAKE_CXX_STANDARD 17)

# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# CUSTOM SETTINGS - PLEASE SPECIFY ACCORDING TO YOUR SYSTEM

# Build the spii lib manually or automatically by add_subdirectory()
# Please adjust with TRUE for automatic or FALSE for manually
set(SPII_BUILD_MODE_VAR TRUE)

# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

if(CMAKE_VERSION VERSION_LESS "3.15.0")
    set(CMAKE_INCLUDE_CURRENT_DIR ON)
endif()

# Output of initial values -----------------------------------------------
message("----- Output of initial values -----")
message("CMAKE_MODULE_PATH: ${CMAKE_MODULE_PATH}")
message("CMAKE_PREFIX_PATH: ${CMAKE_PREFIX_PATH}")
message(STATUS "--------------------------------------------------------" )
# ------------------------------------------------------------------------

set(VCPKG_TARGET_TRIPLET $ENV{VCPKG_TARGET_TRIPLET} CACHE STRING "")

if(NOT DEFINED ENV{VCPKG_TARGET_TRIPLET})
    message(FATAL_ERROR "VCPKG_TARGET_TRIPLET environment variable is not set.")
endif()


# The VCPKG_TARGET_TRIPLET should be commented out if you already set it during the cmake call in the settings.json
if(APPLE)
    message(STATUS "--------------------- SYSTEM MACOSX ---------------------")
    set(CMAKE_OSX_ARCHITECTURES $ENV{CMAKE_OSX_ARCHITECTURES} CACHE STRING "")

    if(NOT DEFINED ENV{CMAKE_OSX_ARCHITECTURES})
         message(FATAL_ERROR "CMAKE_OSX_ARCHITECTURES environment variable is not set.")
     endif()

elseif(MSVC OR WIN32 OR UNIX)
    message(STATUS "--------------------- SYSTEM WINDOWS ---------------------")
    set(VCPKG_TARGET_TRIPLET $ENV{VCPKG_TARGET_TRIPLET} CACHE STRING "")

endif()

# ========================================================================
# Output of environment variables ========================================
# ========================================================================
message("----- Output of environment variables -----")
message("VCPKG_TARGET_TRIPLET: ${VCPKG_TARGET_TRIPLET}")
if(APPLE)
    message("CMAKE_OSX_ARCHITECTURES: ${CMAKE_OSX_ARCHITECTURES}")
endif()
message(STATUS "--------------------------------------------------------" )
# ------------------------------------------------------------------------

# ========================================================================
# Build TBB ==============================================================
# ========================================================================
message(STATUS "--------------------- TBB automatic mode ---------------------")
set(TBB_LIB_NAME 3rdparty/oneTBB)

add_subdirectory(${TBB_LIB_NAME})

include(ExternalProject)

ExternalProject_Add(Build_TBB
    PREFIX ${PROJECT_SOURCE_DIR}/3rdparty/oneTBB
    SOURCE_DIR ${PROJECT_SOURCE_DIR}/3rdparty/oneTBB
    TMP_DIR ${PROJECT_SOURCE_DIR}/3rdparty/oneTBB/tmp
    STAMP_DIR ${PROJECT_SOURCE_DIR}/3rdparty/oneTBB/stamp
    LOG_DIR ${PROJECT_SOURCE_DIR}/3rdparty/oneTBB/log
    BINARY_DIR ${PROJECT_SOURCE_DIR}/build/3rdparty/oneTBB/build
    INSTALL_DIR ${PROJECT_SOURCE_DIR}/build/3rdparty/oneTBB/install
    CMAKE_ARGS -DTBB_TEST=OFF -DCMAKE_INSTALL_PREFIX=${PROJECT_SOURCE_DIR}/build/3rdparty/oneTBB/build -DBUILD_SHARED_LIBS=OFF -DTBBMALLOC_BUILD=OFF -DTBBMALLOC_PROXY_BUILD=OFF -DCMAKE_OSX_ARCHITECTURES=${CMAKE_OSX_ARCHITECTURES}
    BUILD_BYPRODUCTS "3rdparty/oneTBB/build/lib/libtbb.a"
)

set(TBB_DIR "${PROJECT_SOURCE_DIR}build/3rdparty/oneTBB/build/lib/cmake/TBB/") # Setting the module paths to the <package-name>config.cmake files for each lib
set(TBB_INCLUDE_DIR "${PROJECT_SOURCE_DIR}/3rdparty/oneTBB/include")

# find_package will not work with externalProject_Add. The libs need to be added manually
# Source of the following code suggestion:
# https://stackoverflow.com/questions/6351609/cmake-linking-to-library-downloaded-from-externalproject-add

set(TBB_LIB_DIR "${PROJECT_SOURCE_DIR}/build/3rdparty/oneTBB/build/lib/")
if(APPLE)
    message(STATUS "--------------------- SYSTEM MACOSX ---------------------")
    set(prefix "lib")
    set(suffix ".a")
elseif(MSVC OR WIN32)
    message(STATUS "--------------------- SYSTEM WINDOWS ---------------------")
    set(prefix "")
    set(suffix ".lib")
elseif(UNIX AND NOT APPLE)
    message(STATUS "--------------------- SYSTEM LINUX ---------------------")
    find_package(OpenMP REQUIRED)  # Ensure OpenMP is found on Linux systems
    set(OpenMP_CXX_FLAGS "${OpenMP_CXX_FLAGS}")  # Set the OpenMP flags
    set(OpenMP_EXE_LINKER_FLAGS "${OpenMP_EXE_LINKER_FLAGS}")
    set(prefix "lib")
    set(suffix ".so")  # Shared library suffix for Linux
endif()

link_directories(${TBB_LIB_DIR})

# Source of the following code suggestion:
# https://stackoverflow.com/questions/6351609/cmake-linking-to-library-downloaded-from-externalproject-add
set(TBB_LIBRARIES # currently only libtbb.a (libtbbmalloc.a omitted as not needed)
  "${TBB_LIB_DIR}${prefix}tbb${suffix}")

# ========================================================================
# Other adjustments  =====================================================
# ========================================================================
set(CMAKE_PREFIX_PATH ${CMAKE_PREFIX_PATH} "${PROJECT_SOURCE_DIR}/build/vcpkg_installed/${VCPKG_TARGET_TRIPLET}/share")

# ========================================================================
# Setting the module paths to the <package-name>config.cmake files for each lib
# ========================================================================
set(OpenCV_DIR "${PROJECT_SOURCE_DIR}/build/vcpkg_installed/${VCPKG_TARGET_TRIPLET}/share/opencv")
set(Eigen3_DIR "${PROJECT_SOURCE_DIR}/build/vcpkg_installed/${VCPKG_TARGET_TRIPLET}/share/eigen3")
set(Ceres_DIR "${PROJECT_SOURCE_DIR}/build/vcpkg_installed/${VCPKG_TARGET_TRIPLET}/share/ceres")
set(glog_DIR "${PROJECT_SOURCE_DIR}/build/vcpkg_installed/${VCPKG_TARGET_TRIPLET}/share/glog")
set(pybind11_DIR "${PROJECT_SOURCE_DIR}/build/vcpkg_installed/${VCPKG_TARGET_TRIPLET}/share/pybind11")

# ========================================================================
# Using the find package commands ========================================
# ========================================================================
find_package(OpenCV CONFIG REQUIRED)
find_package(Eigen3 CONFIG REQUIRED)
find_package(Ceres CONFIG REQUIRED)
find_package(glog CONFIG REQUIRED)
find_package(pybind11 CONFIG REQUIRED)
find_package(OpenMP)

# ========================================================================
# Check if everything was found correctly for each used package ==========
# ========================================================================
if(OPENCV_FOUND)
message(STATUS "----- OpenCV was found with the following status: -----")
message(STATUS "Version: ${OpenCV_VERSION}")
message(STATUS "Libraries: ${OpenCV_LIBS}")
message(STATUS "Include path: ${OpenCV_INCLUDE_DIRS}")
message(STATUS "Dir path: ${OpenCV_DIR}")
message(STATUS "Lib path: ${OpenCV_LIB_DIR}")
message(STATUS "--------------------------------------------------------" )
else()
message(STATUS "----- OpenCV packageconfig was not found! -----")
endif()

if(TBB_FOUND)
message(STATUS "----- TBB was found -----")
else()
message(STATUS "----- TBB packageconfig was not found! -----")
endif()

if(EIGEN3_FOUND)
message(STATUS "----- EIGEN3 was found -----")
else()
message(STATUS "----- EIGEN3 packageconfig was not found! -----")
endif()

if(Ceres_FOUND)
message(STATUS "----- Ceres was found -----")
else()
message(STATUS "----- Ceres packageconfig was not found! -----")
endif()

if(Boost_FOUND)
message(STATUS "----- Boost was found -----")
else()
message(STATUS "----- Boost packageconfig was not found! -----")
endif()

if(glog_FOUND)
message(STATUS "----- Glog was found -----")
else()
message(STATUS "----- Glog packageconfig was not found! -----")
endif()


# ========================================================================
# Adjust include dirs ====================================================
# ========================================================================
set(Boost_INCLUDE_DIR "${PROJECT_SOURCE_DIR}/build/vcpkg_installed/${VCPKG_TARGET_TRIPLET}/include/")
set(EIGEN_INCLUDE_DIR "${PROJECT_SOURCE_DIR}/build/vcpkg_installed/${VCPKG_TARGET_TRIPLET}/include/")
set(CERES_INCLUDE_DIRS "${PROJECT_SOURCE_DIR}/build/vcpkg_installed/${VCPKG_TARGET_TRIPLET}/include/")

# ========================================================================
# Adjustments for spii -==================================================
# ========================================================================
set(spii_INCLUDE_DIR "${PROJECT_SOURCE_DIR}/3rdparty/spii/include/")
set(spii_LIB_DIR lib)
set(SPII_INSTALL_DIR "3rdparty/spii/build")
set(spii_LIB_NAME 3rdparty/spii)

if(SPII_BUILD_MODE_VAR)
# Automatic build for spii
    message(STATUS "--------------------- SPII automatic mode ---------------------")
    # Check install status of the library
    find_library(spii_LIBRARY_RELEASE
    spii
    PATHS ${CMAKE_BINARY_DIR}/lib/)

    find_library(meschach_LIBRARY_RELEASE
    meschach
    PATHS ${CMAKE_BINARY_DIR}/lib/)

    if(spii_LIBRARY_RELEASE AND meschach_LIBRARY_RELEASE)
        message(STATUS "--------------------- SPII found (automatic) ---------------------")
        set(spii_LIBRARIES ${spii_LIBRARY_RELEASE} ${meschach_LIBRARY_RELEASE})
        message(STATUS "Libraries: ${spii_LIBRARIES}")
        set(SPII_BUILD_FOUND TRUE)
    else()
        message(STATUS "--------------------- SPII not found, will be installed (automatic) ---------------------")
        add_subdirectory(${spii_LIB_NAME})
        link_directories(${CMAKE_BINARY_DIR}/lib)
        set(spii_LIBRARIES "")
    endif()
else()
# Manual build for spii
message(STATUS "--------------------- SPII manual mode ---------------------")
    find_library(spii_LIBRARY_RELEASE
            spii
            PATHS ${spii_LIB_NAME}/lib/)
    find_library(meschach_LIBRARY_RELEASE
            meschach
            PATHS ${spii_LIB_NAME}/lib/)
    if (spii_LIBRARY_RELEASE AND meschach_LIBRARY_RELEASE)
        set(spii_LIBRARIES ${spii_LIBRARY_RELEASE} ${meschach_LIBRARY_RELEASE})
        set(SPII_BUILD_FOUND TRUE)
        message(STATUS "--------------------- SPII was found ---------------------")
        message(STATUS "Libraries: ${spii_LIBRARIES}")
        message(STATUS "--------------------------------------------------------" )
    else()
        set(spii_LIBRARIES "")
        set(SPII_BUILD_FOUND TRUE)
        message(STATUS "-------------- WARNING SPII NOT FOUND: PLEASE INSTALL SPII LIBS! ---------------------")
        message(STATUS "-------------- WARNING SPII NOT FOUND: PLEASE INSTALL SPII LIBS! ---------------------")
    endif()
endif()


# ========================================================================
# Define all parameters ==================================================
# ========================================================================

include_directories(${OpenCV_INCLUDE_DIRS}
        ${Python_NumPy_INCLUDE_DIR}
        ${Boost_INCLUDE_DIR}
        ${TBB_INCLUDE_DIR}
        ${spii_INCLUDE_DIR}
        ${EIGEN_INCLUDE_DIR}
        ${CERES_INCLUDE_DIRS}
        ${pybind11_INCLUDE_DIR}
        ${OMP_INCLUDE_DIRS}
        "src/singleeyefitter"
        "src/pupil-detection-methods")

pybind11_add_module(_pypupil
        src/main.cpp
        src/type_converter.cpp
        src/dataWriter.cpp
        src/pupil-detection-methods/Pupil.h
        src/pupil-detection-methods/PupilDetectionMethod.cpp
        src/pupil-detection-methods/ElSe.cpp
        src/pupil-detection-methods/ExCuSe.cpp
        src/pupil-detection-methods/PuRe.cpp
        src/pupil-detection-methods/PuReST.cpp
        src/pupil-detection-methods/Starburst.cpp
        src/pupil-detection-methods/Swirski2D.cpp
        )

target_link_libraries(_pypupil PRIVATE
        ${OpenCV_LIBS}
        ${Boost_LIBRARIES}
        ${TBB_LIBRARIES}
        ${spii_LIBRARIES}
        ${CERES_LIBRARIES})

# See here for more information:
# https://stackoverflow.com/questions/48142082/cmake-externalproject-add-project-not-building-before-targets-that-depend-on-it
add_dependencies(_pypupil Build_TBB)


# ========================================================================
# Final output ===========================================================
# ========================================================================
message(STATUS "")
message(STATUS "--- Include directories ---" )
message(STATUS "OpenCV_INCLUDE_DIRS: ${OpenCV_INCLUDE_DIRS}")
message(STATUS "Boost_INCLUDE_DIR: ${Boost_INCLUDE_DIR}")
message(STATUS "TBB_INCLUDE_DIR: ${TBB_INCLUDE_DIR}")
message(STATUS "TBB_LIB: ${TBB_LIBRARIES}")
message(STATUS "spii_INCLUDE_DIR: ${spii_INCLUDE_DIR}")
message(STATUS "EIGEN_INCLUDE_DIR: ${EIGEN_INCLUDE_DIR}")
message(STATUS "CERES_INCLUDE_DIRS: ${CERES_INCLUDE_DIRS}")
message(STATUS "pybind11_INCLUDE_DIR: ${pybind11_INCLUDE_DIR}")
message(STATUS "---------------------------")
message(STATUS "")

# ========================================================================
# Check cmake version ===================================================
# ========================================================================
# Code snippet from:
# https://stackoverflow.com/questions/43697154/detect-current-cmake-version-using-cmake
if(${CMAKE_VERSION} VERSION_LESS "3.21.0")
    message("Please consider switching to CMake 3.21.0")
    message("CMAKE_VERSION: ${CMAKE_VERSION}")
endif()
