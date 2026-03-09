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

    version("v10_06_00_01", commit="fb929f3d9ac910bec5da48ca8adcc1bad0412eb6", submodules=True)
    version("v10_04_07", commit="412514c73b41c88fcbd9ffcf0632ed186703a2d3", submodules=True)
    version("v10_04_06_p01",commit="41ef8493069b0f07287e43ed66873484c0a203d5", submodules=True)
    version("v10_04_04",commit="d49df6743d95631d6c9edc2ae01ee3f3e3a5c01f", submodules=True)
    version("v09_93_01_p01", commit="b67723df67c57e7325c4baf3825760c6683f1c7a", submodules=True)
    version("v09_93_01_p02", commit="45baa22ccf40934ca65f5c5229df4c52ad1f7fbb", submodules=True)
    version("09.91.02.01", commit="bf374b540b658d2d175e048da6f43ce2e4d9c509", submodules=True)
    version("09.91.01", commit="f3da8986c43f9d9d7e674b9ab7866da314db5745", submodules=True)

    version(
        "09.37.02.03", sha256="1d287d1dd3df5c2108154660f9846ce7776a69cb4861d0f89beea69e0c60fbce"
    )
    version("09.37.01.03", checksum="297eaedc009e7069da0427acc0af4f27")
    version(
        "09.37.01.02", sha256="a7811d95c816f112f3e320fbf2a15b199a6af3c385e1f53e14ddb6c04ace54cf"
    )
    version("09.35.00", sha256="6dc753dcc24e9583a261a70da99a1275835b70091c816dbbb0ddee60ad698686")

    patch("spack.patch")
    patch("v09_35_00.patch", when="@09.35.00")
    patch("v09_37_02_03.patch", when="@09.37.02.03")
    patch("v09_37_01_02.patch", when="@09.37.01.02")
    patch("v09_37_01_03.patch", when="@09.37.01.03")
    patch("v09_91_01.patch", when="@09.91.01")

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

    depends_on("larrecodnn")
    depends_on("larsoft")# added
    depends_on("genie-xsec") # added, pulled from fnal_art
    depends_on("sbndaq-artdaq-core")
    depends_on("larcv2")
    depends_on("nusystematics")
    depends_on("sbndata")

    depends_on("sbnalg", when="@v10_04_07:")

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
            "-DCMAKE_PREFIX_PATH={0}/lib/python{1}/site-packages/torch".format(
                self.spec["py-torch"].prefix, self.spec["python"].version.up_to(2)
            ),
            "-DZLIB_ROOT={0}".format(self.spec["zlib"].prefix),
            "-DIGNORE_ABSOLUTE_TRANSITIVE_DEPENDENCIES=1",
            "-DCMAKE_VERBOSE_MAKEFILE=1",
            "-DCMAKE_RULE_MESSAGES=1",
            "-DCMAKE_EXPORT_COMPILE_COMMANDS=1",
            self.define(
                "CMAKE_PREFIX_PATH",
                join_path(
                self.spec["py-tensorflow"].prefix.lib,
                "python{0}/site-packages/tensorflow".format(
                    self.spec["python"].version.up_to(2)
                ),
              )
            ),
            self.define(
                "TensorFlow_LIBRARIES",
                join_path(
                self.spec["py-tensorflow"].prefix.lib,
                "python{0}/site-packages/tensorflow".format(
                    self.spec["python"].version.up_to(2)
                ),
              ),
            ),
        ]
        return args

    def setup_build_environment(self, spack_env):
        spack_env.prepend_path("LD_LIBRARY_PATH", self.spec["root"].prefix.lib)
        spack_env.prepend_path("ROOT_X3d", self.spec["root"].prefix.include)
        spack_env.prepend_path("PATH", os.path.join(self.build_directory, "bin"))
        spack_env.prepend_path("CET_PLUGIN_PATH", os.path.join(self.build_directory, "lib"))

        # Perl modules.
        spack_env.prepend_path("PERL5LIB", os.path.join(self.build_directory, "perllib"))
        # Larcv modules
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
        # Cleaup.
        sanitize_environments(run_env)

    def setup_dependent_build_environment(self, spack_env, dependent_spec):
        # Binaries.
        spack_env.prepend_path("PATH", self.prefix.bin)
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        # Ensure Root can find headers for autoparsing.
        spack_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        spack_env.prepend_path("ROOT_LIBRARY_PATH", self.spec["root"].prefix.lib.root)
        # Perl modules.
        spack_env.prepend_path("PERL5LIB", os.path.join(self.prefix, "perllib"))
        # Larcv modules
        # Cleanup.
        sanitize_environments(spack_env)
