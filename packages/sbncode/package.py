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


class Sbncode(CMakePackage):
    """The eponymous package of the Sbn experiment
    framework for particle physics experiments.
    """

    url = "https://github.com/SBNSoftware/sbncode/archive/refs/tags/v09_35_01.tar.gz"
    git = "https://github.com/SBNSoftware/sbncode.git"

    version("v10_24_00", commit="3576c2aadd9ac5a86619aae20e2f22df5ff29848", submodules=True)
    version("v10_06_00_01", commit="fb929f3d9ac910bec5da48ca8adcc1bad0412eb6", submodules=True)
    version("v10_04_07", commit="412514c73b41c88fcbd9ffcf0632ed186703a2d3", submodules=True)
    version("v10_04_06_p01",commit="41ef8493069b0f07287e43ed66873484c0a203d5", submodules=True)
    version("v10_04_04",commit="d49df6743d95631d6c9edc2ae01ee3f3e3a5c01f", submodules=True)
    version("v09_93_01_p01", commit="b67723df67c57e7325c4baf3825760c6683f1c7a", submodules=True)
    version("v09_93_01_p02", commit="45baa22ccf40934ca65f5c5229df4c52ad1f7fbb", submodules=True)


    patch("spack.patch", when="@v10_06_00_01")
    # gateway build: ROOT::X3d / ROOT::Eve targets are not available (root ~x~opengl)
    patch("v10_24_00.patch", when="@v10_24_00")

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    def patch(self):
        filter_file('find_package\( art REQUIRED \)', 'find_package( art REQUIRED )\nfind_package( Eigen3 REQUIRED )\nfind_package( larrecodnn REQUIRED )','CMakeLists.txt')

    # Build-only dependencies.
    depends_on("cmake@3.11:")
    depends_on("cetmodules", type="build")
    depends_on("cetbuildtools", type="build")
    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("larana")
    depends_on("larreco")
    depends_on("larrecodnn")
    depends_on("larpandora")
    depends_on("larwirecell")
    depends_on("larfinder", type="build")
    depends_on("genie-xsec")
    depends_on("sbndaq-artdaq-core")
    depends_on("larcv2")
    depends_on("nusystematics")
    depends_on("geant4reweight")

    depends_on("sbndata")
    depends_on("sbnalg", when="@v10_04_07:")

    # versions from ups/product_deps of v10_24_00 (as used by icaruscode v10_25_00)
    with when("@v10_24_00"):
        depends_on("larsoft@10.24.00")
        depends_on("sbnalg@10.24.00")
        depends_on("sbndaq-artdaq-core@v1_10_06_01")
        depends_on("genie-xsec@3.06.00")
        depends_on("larcv2@2_2_6")
        depends_on("sbndata@01_10")
        depends_on("nusystematics@1.05.15")
        depends_on("geant4reweight@01.21.04")

    if "SPACKDEV_GENERATOR" in os.environ:
        generator = os.environ["SPACKDEV_GENERATOR"]
        if generator.endswith("Ninja"):
            depends_on("ninja", type="build")

    def url_for_version(self, version):
        url = "https://github.com/SBNSoftware/{0}/archive/v{1}.tar.gz"
        return url.format(self.name, version.underscored)

    def cmake_args(self):
        # Set CMake args.
        args = [
            "-DCMAKE_CXX_STANDARD={0}".format(self.spec.variants["cxxstd"].value),
            "-DCMAKE_PREFIX_PATH={0}/lib/python{1}/site-packages/torch;{2}/lib64/python{3}/site-packages/torch".format(
                self.spec["py-torch"].prefix, self.spec["python"].version.up_to(2),self.spec["py-torch"].prefix, self.spec["python"].version.up_to(2)
            ),
            "-DZLIB_ROOT={0}".format(self.spec["zlib"].prefix),
            "-DIGNORE_ABSOLUTE_TRANSITIVE_DEPENDENCIES=1",
            "-DCMAKE_VERBOSE_MAKEFILE=1",
            "-DCMAKE_RULE_MESSAGES=1",
            "-DCMAKE_EXPORT_COMPILE_COMMANDS=1",
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
            "--debug-find"
        ]
        return args

    def setup_build_environment(self, spack_env):
        spack_env.prepend_path("CMAKE_PREFIX_PATH", join_path(self.spec["py-tensorflow"].prefix.lib, "python{0}/site-packages/tensorflow".format(self.spec["python"].version.up_to(2))))
        spack_env.prepend_path("CMAKE_PREFIX_PATH", join_path(self.spec["py-tensorflow"].prefix.lib64, "python{0}/site-packages/tensorflow".format(self.spec["python"].version.up_to(2))))
        spack_env.prepend_path("LD_LIBRARY_PATH", self.spec["root"].prefix.lib)
        spack_env.prepend_path("ROOT_X3d", self.spec["root"].prefix.include)
        spack_env.prepend_path("PATH", os.path.join(self.build_directory, "bin"))
        spack_env.prepend_path("CET_PLUGIN_PATH", os.path.join(self.build_directory, "lib"))

        # Perl modules.
        spack_env.prepend_path("PERL5LIB", os.path.join(self.build_directory, "perllib"))
        # Larcv modules
        if os.path.exists(self.spec["py-tensorflow"].prefix.lib64):
            spack_env.set(
                "Torch_DIR",
                "{0}/lib64/python{1}/site-packages/torch/share/cmake/Torch".format(
                    self.spec["py-torch"].prefix, self.spec["python"].version.up_to(2)
                ),
                )
        else: 
            spack_env.set(
                "Torch_DIR",
                "{0}/lib/python{1}/site-packages/torch/share/cmake/Torch".format(
                    self.spec["py-torch"].prefix, self.spec["python"].version.up_to(2)
                ),
            )


    def setup_run_environment(self, run_env):
        run_env.prepend_path("LD_LIBRARY_PATH", self.spec["python"].prefix.lib)
        # Binaries.
        run_env.prepend_path("PATH", os.path.join(self.prefix, "bin"))
        # Ensure we can find plugin libraries.
        run_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        # Perl modules.
        run_env.prepend_path("PERL5LIB", os.path.join(self.prefix, "perllib"))
        # Larcv modules
        run_env.prepend_path("FHICL_FILE_PATH", self.prefix.fcl)
        run_env.prepend_path("FHICL_INCLUDE_PATH", self.prefix.fcl)
        run_env.prepend_path("ROOT_INCLUDE_PATH", self.spec['artdaq-core'].prefix.include)
        run_env.prepend_path("ROOT_LIBRARY_PATH", self.spec['artdaq-core'].prefix.lib)

    def setup_dependent_build_environment(self, spack_env, dependent_spec):
        spack_env.prepend_path("CMAKE_PREFIX_PATH", join_path(self.spec["py-tensorflow"].prefix.lib, "python{0}/site-packages/tensorflow".format(self.spec["python"].version.up_to(2))))
        # Binaries.
        spack_env.prepend_path("PATH", self.prefix.bin)
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        # Ensure Root can find headers for autoparsing.
        spack_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        spack_env.prepend_path("ROOT_LIBRARY_PATH", self.spec["root"].prefix.lib.root)
        # Perl modules.
        spack_env.prepend_path("PERL5LIB", os.path.join(self.prefix, "perllib"))
