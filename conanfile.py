import os
from conan import ConanFile


class CompresstoolsConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeToolchain", "CMakeDeps"

    def requirements(self):
        self.requires("pybind11/2.13.6", force=True)
        self.requires("boost/1.75.0", force=True)
        self.requires("eigen/3.3.9", force=True)
        self.requires("ceres-solver/2.0.0", force=True)
        self.requires("opencv/4.5.1", force=True)
        self.requires("zlib/1.2.13", force=True)
        self.requires("libwebp/1.3.2", force=True)

    def build_requirements(self):
        if self.settings.os != "Windows":
            self.tool_requires("cmake/3.30.5")

    def configure(self):
        if self.settings.compiler == "apple-clang":
            self.settings.compiler.cppstd = "14"

    def layout(self):
        # We make the assumption that if the compiler is msvc the
        # CMake generator is multi-config
        multi = True if self.settings.get_safe("compiler") == "msvc" else False
        if multi:
            self.folders.generators = os.path.join("build", "generators")
            self.folders.build = "build"
        else:
            self.folders.generators = os.path.join(
                "build", str(self.settings.build_type), "generators")
            self.folders.build = os.path.join(
                "build", str(self.settings.build_type))
