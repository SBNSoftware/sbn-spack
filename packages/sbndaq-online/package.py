# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack.package import *

def sanitize_environments(env, *vars):
    for var in vars:
        env.prune_duplicate_paths(var)
        env.deprioritize_system_paths(var)

class SbndaqOnline(CMakePackage):
    """Redis interface software for the online SBN framework"""

    homepage = "https://github.com/SBNSoftware"
    git_base = "https://github.com/SBNSoftware/sbndaq-online.git"
    list_url = "https://api.github.com/repos/SBNSoftware/sbndaq-online/tags"
    url      = "https://github.com/SBNSoftware/sbndaq-online"

    version("develop", git=git_base, branch="develop", get_full_repo=True)
    version("v1_01_00", git=git_base, tag="v1_01_00", get_full_repo=True)

    patch('spack_build.patch', when='@develop')
    patch('spack_build.patch', when='@v1_01_00')

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on('jsoncpp')

    with when("@develop"):
        depends_on("artdaq@v3_13_02")
        depends_on("cetmodules", type="build")

    with when("@v1_01_00"):
        depends_on("artdaq@v3_13_02")
        depends_on("cetmodules", type="build")

    def url_for_version(self, version):
        url = "https://github.com/SBNSoftware/{0}/archive/refs/tags/{1}.tar.gz"
        return url.format(self.name, version.underscored)

    def cmake_args(self):
        args = [
            "-DCMAKE_CXX_STANDARD={0}".format(self.spec.variants["cxxstd"].value),
            "-DWANT_UPS:BOOL=OFF"
        ]
        return args

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
