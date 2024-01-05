from conans import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, CMakeDeps, cmake_layout
from conan.tools.scm import Git


class MicrosoftGLTFSDKForkedConan(ConanFile):
    name = "rapidjson"
    url = "https://github.com/Tencent/rapidjson.git"
    homepage = url
    description = "Robust Parsers for Protocols & File Formats"
    license = "MIT License"
    settings = "os", "compiler", "build_type", "arch"

    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": True,
        "fPIC": True,
    }
    version = "only_for_msgltfsdk"

    def source(self):
        git = Git(self)
        git.fetch_commit(
            "https://github.com/Tencent/rapidjson.git", "232389d4f1012dddec4ef84861face2d2ba85709"
        )
        git.run("submodule update --init --recursive --recommend-shallow --depth 1")

    def layout(self):
        cmake_layout(self)

    def configure(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def requirements(self):
        pass

    def build_requirements(self):
        self.build_requires("cmake/[^3]")
        self.build_requires("ninja/[*]")

    def generate(self):
        tc = CMakeToolchain(self, "Ninja")
        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = self.collect_libs()
