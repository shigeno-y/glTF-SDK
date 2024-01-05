from conans import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, CMakeDeps, cmake_layout
from conan.tools.files import apply_conandata_patches
from conan.tools.scm import Git


class MicrosoftGLTFSDKForkedConan(ConanFile):
    name = "msgltfsdk"
    url = "https://github.com/shigeno-y/glTF-SDK"
    homepage = url
    description = "Robust Parsers for Protocols & File Formats"
    license = "MIT License"
    settings = "os", "build_type", "arch"

    options = {
        # library option
        "shared": [True, False],
        "fPIC": [True, False],
        # this lib
        "with_unittest": [True, False],
        "with_sample": [True, False],
    }
    default_options = {
        "shared": True,
        "fPIC": True,
        "with_unittest": False,
        "with_sample": False,
    }
    version = "0.1.0"

    def source(self):
        git = Git(self)
        git.fetch_commit(
            "https://github.com/shigeno-y/glTF-SDK.git", "feature/vrm"
        )
        git.run("submodule update --init --recursive --recommend-shallow --depth 1")

    def layout(self):
        cmake_layout(self)

    def configure(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def requirements(self):
        self.requires("gtest/[^1.10]")
        self.requires("rapidjson/[^1]")

    def build_requirements(self):
        self.build_requires("cmake/[^3]")
        self.build_requires("ninja/[*]")

    def generate(self):
        tc = CMakeToolchain(self, "Ninja")

        tc.cache_variables["ENABLE_UNIT_TESTS"] = self.options.with_unittest
        tc.cache_variables["ENABLE_SAMPLES"] = self.options.with_sample
        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        apply_conandata_patches(self)
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = self.collect_libs()
