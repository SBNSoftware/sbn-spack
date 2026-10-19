# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack.package import *


def sanitize_environments(*args):
    for env in args:
        for var in (
            "PATH",
            "CET_PLUGIN_PATH",
            "LDSHARED",
            "LD_LIBRARY_PATH",
            "DYLD_LIBRARY_PATH",
            "LIBRARY_PATH",
            "CMAKE_PREFIX_PATH",
            "ROOT_INCLUDE_PATH",
        ):
            env.prune_duplicate_paths(var)
            env.deprioritize_system_paths(var)


class Icaruscode(CMakePackage):
    """The eponymous package of the Icarus experiment
    framework for particle physics experiments.
    """

    homepage = "https://cdcvs.fnal.gov/redmine/projects/icaruscode"
    git_base = "https://github.com/SBNSoftware/icaruscode"
    git = f"{git_base}.git"
    url = f"{git_base}/archive/v09_35_00.tar.gz"
    list_url = "https://github.com/SBNSoftware/icaruscode/tags"

    version(
        "develop",
        branch="develop",
        git= f"{git_base}.git" ,
        get_full_repo=True,
    )
    version("10.25.00", sha256="55f8e7750d176921b43e1d237d6096c2de0e9f6305d5b7599be2a267f104e8dc")
    version("10.06.00.01p04", sha256="4ae01238f61b326feb9d58d1b4a33c7ad8f42054ad661d012b6041bd72288c3e")
    version("09.35.00", sha256="9c265335bbfc728a5a9d47cc615475eb9e57d8871224ac0aee44ac763e166b54")

#    patch("cetmodules2.patch", when="@develop")
    patch("spack.patch", when="@10.06.00.01p04")
    # gateway build: no PandoraMonitoring (root ~x~opengl), no quad/long-double FFTW in icaruscode
    patch("v10_25_00.patch", when="@10.25.00")


    def patch(self):
        filter_file("WireCellRoot", "spdlog::spdlog", "icaruscode/Overlays/CMakeLists.txt")
        filter_file(r"(^\s*)jsoncpp", "jsoncpp_lib", "icaruscode/Overlays/CMakeLists.txt")
        filter_file("find_package\(larsoft REQUIRED \)", "", "CMakeLists.txt")
        # icarusutil is not installed with a CMake config (see icarusutil patches)
        filter_file("find_package\(icarusutil REQUIRED \)", "", "CMakeLists.txt")
        # checkClassVersion sets ROOT_INCLUDE_PATH from the dictionary target only, which misses
        # headers of autoloaded dependency dictionaries (nusimdata, larcoreobj, ...): use the
        # build environment's ROOT_INCLUDE_PATH (all link dependencies) as well
        for f in find(".", "CMakeLists.txt"):
            filter_file(
                r"^(\s*(?:art|build)_dictionary\s*\()",
                r'\1CCV_ENVIRONMENT "ROOT_INCLUDE_PATH=${PROJECT_SOURCE_DIR}:${PROJECT_BINARY_DIR}:$ENV{ROOT_INCLUDE_PATH}" ',
                f,
                ignore_absent=True,
                backup=False,
            )

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    # Build-only dependencies.
    depends_on("cmake@3.11:")
    depends_on("cetmodules", type="build")
    depends_on("c", type="build")
    depends_on("cxx", type="build")

    # Build and link dependencies.
    depends_on("root+spectrum", type=("build", "run"))
    depends_on("icarusalg", type=("build", "run"))
    depends_on("icarus-data", type=("build", "run"))
    depends_on("artdaq-core", type=("build", "run"))
    depends_on("art-root-io", type=("build", "run"))
    depends_on("art", type=("build", "run"))
    depends_on("boost", type=("build", "run"))
    depends_on("canvas-root-io", type=("build", "run"))
    depends_on("canvas", type=("build", "run"))
    depends_on("cetlib", type=("build", "run"))
    depends_on("cetlib-except", type=("build", "run"))
    depends_on("messagefacility", type=("build", "run"))
    depends_on("catch2", type=("build", "run"))
    depends_on("gallery", type=("build", "run"))
    depends_on("clhep", type=("build", "run"))
    depends_on("cppgsl", type=("build", "run"))
    depends_on("eigen", type=("build", "run"))
    depends_on("fftw", type=("build", "run"))
    depends_on("fhicl-cpp", type=("build", "run"))
    depends_on("hep-concurrency", type=("build", "run"))
    depends_on("ifdh-art", type=("build", "run"))
    depends_on("ifdhc", type=("build", "run"))
    depends_on("ifbeam", type=("build", "run"))
    depends_on("tbb", type=("build", "run"))
    depends_on("geant4", type=("build", "run"))
    depends_on("icarus-signal-processing", type=("build", "run"))
    depends_on("larana", type=("build", "run"))
    depends_on("larcoreobj", type=("build", "run"))
    depends_on("larcorealg", type=("build", "run"))
    depends_on("larcore", type=("build", "run"))
    depends_on("lardataobj", type=("build", "run"))
    depends_on("lardataalg", type=("build", "run"))
    depends_on("lardata", type=("build", "run"))
    depends_on("larevt", type=("build", "run"))
    depends_on("pandorasdk", type=("build", "run"))
    depends_on("larpandora", type=("build", "run"))
    depends_on("larpandoracontent", type=("build", "run"))
    depends_on("larreco", type=("build", "run"))
    depends_on("larvecutils", type=("build", "run"))
    depends_on("larsim", type=("build", "run"))
    depends_on("larexamples", type=("build", "run"))
    depends_on("larwirecell", type=("build", "run"))
    depends_on("wire-cell-toolkit", type=("build", "run"))
    depends_on("jsoncpp", type=("build", "run"))
    depends_on("nlohmann-json", type=("build", "run"))
    depends_on("vdt", type=("build", "run"))
    depends_on("libwda", type=("build", "run"))
    depends_on("marley", type=("build", "run"))
    depends_on("dk2nudata", type=("build", "run"))
    depends_on("dk2nugenie", type=("build", "run"))
    depends_on("genie", type=("build", "run"))
    depends_on("cry", type=("build", "run"))
    depends_on("rstartree", type=("build", "run"))
    depends_on("artg4tk", type=("build", "run"))
    depends_on("nug4", type=("build", "run"))
    depends_on("nucondb", type=("build", "run"))
    depends_on("nutools", type=("build", "run"))
    depends_on("nurandom", type=("build", "run"))
    depends_on("nusimdata", type=("build", "run"))
    depends_on("nufinder", type=("build", "run"))
    depends_on("postgresql", type=("build", "run"))
    depends_on("range-v3", type=("build", "run"))
    depends_on("sbndaq-artdaq-core", type=("build", "run"))
    depends_on("sbnobj", type=("build", "run"))
    depends_on("sbnalg", type=("build", "run"))
    depends_on("sbncode", type=("build", "run"))
    depends_on("sqlite", type=("build", "run"))
    depends_on("trace", type=("build", "run"))
    depends_on("protobuf", type=("build", "run"))
    depends_on("py-torch", type=("build", "run"))
    depends_on("spdlog", type=("build", "run"))
    depends_on("fmt", type=("build", "run"))
    depends_on("py-tensorflow", type=("build", "run"))
    depends_on("larcv2", type=("build", "run"), when="@10:")

    # versions from ups/product_deps of v10_25_00
    with when("@10.25.00"):
        depends_on("icarus-data@10.06.06", type=("build", "run"))
        depends_on("icarus-signal-processing@10.25.00", type=("build", "run"))
        depends_on("icarusalg@10.25.00", type=("build", "run"))
        depends_on("sbncode@v10_24_00", type=("build", "run"))

    if "SPACKDEV_GENERATOR" in os.environ:
        generator = os.environ["SPACKDEV_GENERATOR"]
        if generator.endswith("Ninja"):
            depends_on("ninja", type="build")

    def url_for_version(self, version):
        # url = 'https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/{0}.v{1}.tbz2'
        url = "https://github.com/SBNSoftware/{0}/archive/v{1}.tar.gz"
        return url.format(self.name, version.underscored)

    @property
    def cmake_prefix_paths(self):
        return [ self.prefix,
                "{0}/lib/python{1}/site-packages/torch;{2}/lib64/python{3}/site-packages/torch".format(
                self.spec["py-torch"].prefix, self.spec["python"].version.up_to(2),self.spec["py-torch"].prefix, self.spec["python"].version.up_to(2))
                ]

    def cmake_args(self):
        # Set CMake args.
        tdir = "{0}/lib/python{1}/site-packages/tensorflow".format(
                self.spec["py-tensorflow"].prefix, self.spec["python"].version.up_to(2)
                )
        args = [
            "-DCMAKE_CXX_STANDARD={0}".format(self.spec.variants["cxxstd"].value),
            "-Dicaruscode_FW_DIR=fw",
            "-Dicaruscode_WP_DIR=wire-cell-cfg",
            "-Dicaruscode_WIRECELL_PATH={0}".format(self.spec["wire-cell-toolkit"].prefix),
            "-DCPPGSL_INC={0}".format(self.spec["cppgsl"].prefix.include),
            "-DTRACE_INC={0}".format(self.spec["trace"].prefix.include),
            "-DLIBWDA_INC={0}".format(self.spec["libwda"].prefix.include),
            self.define(
                "TensorFlow_INC",
                join_path(
                self.spec["py-tensorflow"].prefix.lib,
                "python{0}/site-packages/tensorflow/include".format(
                    self.spec["python"].version.up_to(2)
                ),)
                + ";" +
                join_path(
                self.spec["py-tensorflow"].prefix.lib64,
                "python{0}/site-packages/tensorflow/include".format(
                    self.spec["python"].version.up_to(2)
                ),)
            ),
            self.define(
                "TensorFlow_DIR",
                join_path(
                self.spec["py-tensorflow"].prefix.lib,
                "python{0}/site-packages/tensorflow".format(
                    self.spec["python"].version.up_to(2)
                ),)
                + ";" +
                join_path(
                self.spec["py-tensorflow"].prefix.lib64,
                "python{0}/site-packages/tensorflow".format(
                    self.spec["python"].version.up_to(2)
                ),)
            ),
        ]
        return args

    def setup_build_environment(self, spack_env):
        spack_env.prepend_path("CMAKE_PREFIX_PATH", join_path(self.spec["py-tensorflow"].prefix.lib, "python{0}/site-packages/tensorflow".format(self.spec["python"].version.up_to(2))))
        spack_env.prepend_path("CMAKE_PREFIX_PATH", join_path(self.spec["py-tensorflow"].prefix.lib64, "python{0}/site-packages/tensorflow".format(self.spec["python"].version.up_to(2))))
        spack_env.set("CETBUILDTOOLS_VERSION", self.spec["cetmodules"].version.string)
        spack_env.set("CETBUILDTOOLS_DIR", self.spec["cetmodules"].prefix)
        spack_env.append_path("CMAKE_PREFIX_PATH", self.spec["cetmodules"].prefix)
        spack_env.prepend_path("LD_LIBRARY_PATH", self.spec["root"].prefix.lib)
        # Binaries.
        spack_env.prepend_path("PATH", os.path.join(self.build_directory, "bin"))
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", os.path.join(self.build_directory, "lib"))
        # Ensure Root can find headers for autoparsing.
        for d in self.spec.traverse(
            root=False, cover="nodes", order="post", deptype=("link"), direction="children"
        ):
            spack_env.prepend_path("ROOT_INCLUDE_PATH", str(self.spec[d.name].prefix.include))
        # Perl modules.
        spack_env.prepend_path("PERL5LIB", os.path.join(self.build_directory, "perllib"))
        # FW search path
        spack_env.append_path("FW_SEARCH_PATH", os.path.join(self.build_directory, "fw"))
        #wirecell vars
        spack_env.set("WIRECELL_INC", str(self.spec["wire-cell-toolkit"].prefix.include))
        spack_env.set("WIRECELL_LIB", str(self.spec["wire-cell-toolkit"].prefix.lib))
        spack_env.set("LARWIRECELL_INC", str(self.spec["larwirecell"].prefix.include))
        spack_env.set("SPDLOG_INC", str(self.spec["spdlog"].prefix.include))
        spack_env.set("JSONCPP_INC", str(self.spec["jsoncpp"].prefix.include))

        # Cleaup.
        sanitize_environments(spack_env)

    def setup_run_environment(self, run_env):
        # Ensure we can find plugin libraries.
        run_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        # Ensure Root can find headers for autoparsing.
        for d in self.spec.traverse(
            root=False, cover="nodes", order="post", deptype=("link"), direction="children"
        ):
            run_env.prepend_path("ROOT_INCLUDE_PATH", str(self.spec[d.name].prefix.include))
        run_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        run_env.prepend_path("PERL5LIB", os.path.join(self.prefix, "perllib"))
        # FW search path
        run_env.append_path("FW_SEARCH_PATH", os.path.join(self.prefix, "fw"))
        # Cleaup.
        sanitize_environments(run_env)

    def setup_dependent_build_environment(self, spack_env, dependent_spec):
        # Binaries.
        spack_env.prepend_path("PATH", self.prefix.bin)
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        # Ensure Root can find headers for autoparsing.
        spack_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        # Perl modules.
        spack_env.prepend_path("PERL5LIB", os.path.join(self.prefix, "perllib"))
        # FW search path
        spack_env.append_path("FW_SEARCH_PATH", os.path.join(self.prefix, "fw"))
        # Cleanup.
        sanitize_environments(spack_env)

    def setup_dependent_run_environment(self, run_env, dependent_spec):
        # Binaries.
        run_env.prepend_path("PATH", self.prefix.bin)
        # Ensure we can find plugin libraries.
        run_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        # Ensure Root can find headers for autoparsing.
        run_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        # Perl modules.
        run_env.prepend_path("PERL5LIB", os.path.join(self.prefix, "perllib"))
        # FW search path
        run_env.append_path("FW_SEARCH_PATH", os.path.join(self.prefix, "fw"))
        # Cleanup.
        sanitize_environments(run_env)
