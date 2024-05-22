from conan import ConanFile
from conan.tools.layout import basic_layout
from conan.tools.files import export_conandata_patches, apply_conandata_patches
from conan.tools import files
from os import path


class TracyConan(ConanFile):
    name = "tracy"
    license = "BSD-3-Clause"
    author = "Stepan Gatilov stgatilov@gmail.com"
    description = "A real time, nanosecond resolution, remote telemetry, hybrid frame and sampling profiler for games and other applications."
    topics = ("profiler", "trace")

    def export_sources(self):
        export_conandata_patches(self)

    def layout(self):
        basic_layout(self, src_folder = "fullsource")

    def source(self):
        files.get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def build(self):
        # generic patches (e.g. add RecreateQueries method)
        apply_conandata_patches(self)
        # replace glXXX with qglXXX
        for prefix in ['glGet', 'glGen', 'glQuery']:
            files.replace_in_file(self, path.join(self.source_folder, "TracyOpenGL.hpp"), prefix, 'q' + prefix)

    def package(self):
        for dirname in ['client', 'common', 'libbacktrace']:
            files.copy(self, "{0}/*.h".format(dirname), src=self.source_folder, dst=path.join(self.package_folder, "include"))
            files.copy(self, "{0}/*.hpp".format(dirname), src=self.source_folder, dst=path.join(self.package_folder, "include"))
            files.copy(self, "{0}/*.cpp".format(dirname), src=self.source_folder, dst=path.join(self.package_folder, "src"))
        files.copy(self, 'TracyVersion.hpp', src=path.join(self.source_folder, 'server'), dst=path.join(self.package_folder, "include/common"))
        for filename in ['Tracy.hpp', 'TracyC.h', 'TracyOpenGL.hpp']:
            files.copy(self, filename, src=self.source_folder, dst=path.join(self.package_folder, "include"))
        for filename in ['TracyClient.cpp']:
            files.copy(self, filename, src=self.source_folder, dst=path.join(self.package_folder, "src"))
        files.copy(self, "LICENSE", src=self.source_folder, dst=path.join(self.package_folder, "licenses"))
        files.copy(self, "libbacktrace/LICENSE", src=self.source_folder, dst=path.join(self.package_folder, "licenses"))
