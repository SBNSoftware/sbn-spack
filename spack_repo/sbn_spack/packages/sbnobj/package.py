# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack.package import *

class Sbnobj(CMakePackage):
    """The eponymous package of the Sbn experiment
    framework for particle physics experiments.
    """

    homepage = "https://cdcvs.fnal.gov/redmine/projects/sbnobj"
    git_base = "https://github.com/SBNSoftware/sbnobj"
    git = f"{git_base}.git"
    url = f"{git_base}/archive/v10_03_00.tar.gz"
    list_url = "https://github.com/SBNSoftware/sbnobj/tags"

    version("develop", branch="develop", get_full_repo=True)
    version("10.23.00", sha256="0b6a9c6cd9941022defff78a83113f868c57e82ec855d29f38c7ecbde3f22889")
    version("10.22.00", sha256="2e23b47a1760ef23ae0cabce7982c864e221b756e9ec1f7ff9c8f44674bb5c50")
    version("10.21.01", sha256="4245d7870ab532930918299d2c6568ea20b3e3a8d8521c1505d347d0a32c96d0")
    version("10.20.09", sha256="dec45f14c5adf418014c12e72821e781b01622e38e97b709604a76aec2078cf6")
    version("10.20.03", sha256="906e10c498ac5a90490cbc67a732775711fdb675904795fabf1be9e38efe5c52")
    version("10.03.01", sha256="2c4e1c79a3b823d507ee9708aeec66951fb1539e31dc911fb02567acc809d24c")
    version("10.03.00", sha256="d5b96c6d63d2deec94a3abab426925303f4bde40209b6270b1fa41a9a83f2689")
    version("10.01.00", sha256="f0df159da2b94dbd77c61f065d18b3124d44b90aee229fa4ca67c9f3aadbff53")

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("cmake@3.11:")
    depends_on("cetmodules", type="build")
    depends_on("art")
    depends_on("boost")
    depends_on("canvas")
    depends_on("clhep")
    depends_on("fftw")
    depends_on("larcoreobj")
    depends_on("larcorealg")
    depends_on("larcore")
    depends_on("lardataobj")
    depends_on("lardataalg")
    depends_on("lardata")
    depends_on("messagefacility")
    depends_on("nusimdata")
    depends_on("dk2nudata")
    depends_on("root")

    if "SPACKDEV_GENERATOR" in os.environ:
        generator = os.environ["SPACKDEV_GENERATOR"]
        if generator.endswith("Ninja"):
            depends_on("ninja", type="build")

    def url_for_version(self, version):
        url = "https://github.com/SBNSoftware/{0}/archive/v{1}.tar.gz"
        return url.format(self.name, version.underscored)

    def cmake_args(self):
        # Set CMake args.
        args = ["-DCMAKE_CXX_STANDARD={0}".format(self.spec.variants["cxxstd"].value),
                "-DFFTW3_PREFIX={0}".format(self.spec['fftw'].prefix),
                "-DSQLite3_INCLUDE_DIR={0}".format(self.spec['sqlite'].prefix.include),
                "-DSQLite3_LIBRARY={0}".format(self.spec['sqlite'].prefix.lib),
                "-DPostgreSQL_INCLUDE_DIR={0}".format(self.spec['postgresql'].prefix.include),
                "-DPostgreSQL_LIBRARY={0}".format(self.spec['postgresql'].prefix.lib),
                "-DFFTW3_INCLUDE_DIR={0}".format(self.spec['fftw'].prefix.include),
                "-DFFTW3_LIBRARY={0}".format(self.spec['fftw'].prefix.lib),
                "-DVDT_INCLUDE_DIR={0}".format(self.spec['vdt'].prefix.include),
                "-DVDT_LIBRARY={0}".format(self.spec['vdt'].prefix.lib)]
        return args

    def setup_run_environment(self, run_env):
        run_env.prepend_path("PATH", os.path.join(self.prefix, "bin"))
        run_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        run_env.prepend_path("CMAKE_PREFIX_PATH", self.spec['catch2'].prefix.lib64.cmake)
        run_env.prepend_path("PERL5LIB", os.path.join(self.prefix, "perllib"))

    def setup_dependent_build_environment(self, spack_env, dependent_spec):
        spack_env.prepend_path("PATH", self.prefix.bin)
        spack_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        spack_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        spack_env.prepend_path("PERL5LIB", os.path.join(self.prefix, "perllib"))
