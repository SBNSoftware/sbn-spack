# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

def sanitize_environments(env, *vars):
    for var in vars:
        env.prune_duplicate_paths(var)
        env.deprioritize_system_paths(var)

class Sbndqm(CMakePackage):
    """Main Data Quality Monitoring (DQM) package for SBN"""

    homepage = "https://sbnsoftware.github.io/"
    git_base = "https://github.com/SBNSoftware/sbndqm.git"
    list_url = "https://api.github.com/repos/SBNSoftware/sbndqm/tags"
    url      = "https://github.com/SBNSoftware/sbndqm"

    squals = ("128","131","132")

    version("develop", git=git_base, branch="develop", get_full_repo=True)
    version("v1_04_00", git=git_base, tag="v1_04_00", get_full_repo=True)

    patch('artdaq-utilities.patch', when='@:')

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    variant(
        "s",
        default="0",
        values=("0",) + squals,
        multi=False,
        description="Artdaq suite version to use",
    )

    with when("@develop"):
        depends_on("sbndaq-online@v1_01_00")
        depends_on("sbndaq-artdaq-core@v1_10_06")
        depends_on("sbncode@v10_06_00_01")

    with when("@v1_04_00"):
        depends_on("sbndaq-online@v1_01_00")
        depends_on("sbndaq-artdaq-core@v1_10_06")
        depends_on("sbncode@v10_06_00_01")

    depends_on("artdaq-utilities")
    depends_on("fftw")
    depends_on("py-fhicl-py")
    depends_on("cetmodules", type="build")


    def url_for_version(self, version):
        url = "https://github.com/SBNSoftware/{0}/archive/v{1}.tar.gz"
        print("url for version: ", url.format(self.name, version.underscored))
        return url.format(self.name, version.underscored)

    def cmake_args(self):
        args = [
            "-DCMAKE_CXX_STANDARD={0}".format(self.spec.variants["cxxstd"].value),
            "-DSPACK_BUILD=1",
            "-Dsbndqm_FW_DIR=fw"
        ]
        return args

    def setup_build_environment(self, env):
        # Ensure we can find plugin libraries.
        env.prepend_path("CMAKE_PREFIX_PATH", self.spec['sbndaq-online'].prefix)
        env.prepend_path("CMAKE_PREFIX_PATH", self.spec['artdaq-utilities'].prefix)
        # Ensure we can find fhicl files

    def setup_run_environment(self, env):
        prefix = self.prefix
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        # Ensure we can find fhicl files
        env.prepend_path("FHICL_FILE_PATH", prefix + "/fcl")
        # Cleaup.
        sanitize_environments(env, "CET_PLUGIN_PATH", "FHICL_FILE_PATH")

    def setup_dependent_run_environment(self, env, dependent_spec):
        prefix = self.prefix
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        # Ensure we can find fhicl files
        env.prepend_path("FHICL_FILE_PATH", prefix + "/fcl")
        # Cleaup.
        sanitize_environments(env, "CET_PLUGIN_PATH", "FHICL_FILE_PATH")
