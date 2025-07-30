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


class Sbndaq(CMakePackage):
    """Common code and utilities for SBN DAQs"""

    homepage = "https://github.com/SBNSoftware"
    url = "https://github.com/SBNSoftware/sbndaq"
    git_base = "https://github.com/SBNSoftware/sbndaq.git"
    list_url = "https://api.github.com/repos/SBNSoftware/sbndaq/tags"

    version("v1_10_08", sha256="7b4c94727e3b711ab6a07c65050d6ae26f7b93b2692f181806ce70a48dd6a16c")
    version("v1_10_07", sha256="e22af191efad5e94e57c9fa84c98f372f125a210a0289186ab265ecc6fc4eb32")
    version("v1_10_06", sha256="a692a0f493cc0fbbc83c73b3d370669a583c8a1957538460d60baf2528fcb8a2")
    version("v1_10_05", sha256="25cb4f38335113b53ef39786adaf12dc1f2eaf998bec82afa944278c1faf0ec5")
    version("v1_10_04", sha256="a19f199b70753cdbf33ad251f52eeae18860bef6359b866f1084b613451045bf")
    version("v1_10_03", sha256="b6c25ef4ca475dd7fff2d5c12f5242045f37801ae20948954b19daf88a9a8f41")
    version("v1_10_02", sha256="ec0b142cb2625015afa7c7c970f5be9980dc96eaf3f868651d4546e89ecdac32")
    version("v1_10_01", sha256="d6bea502d1b577451ee2e27eb4678c588bfe8820140f30ab76f2f7f240a0e1f6")
    version("v1_10_00", sha256="f0753c27bda6d5f81a8610ed6bee36286c16d4d24e844da626129f6c72340319")
    
    version("migration", git=git_base, branch="feature/upgrade_gcc13.1.0", get_full_repo=True)
    version("develop", git=git_base, branch="develop", get_full_repo=True)

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    variant(
        "icarus",
        default=False,
        description="Build ICARUS-specific parts of the package",
    )
    variant(
        "sbnd", default=False, description="Build SBND-specific parts of the package"
    )

    depends_on("sbndaq-artdaq")
    depends_on("sbndaq-artdaq+icarus", when="+icarus")
    depends_on("sbndaq-artdaq+sbnd", when="+sbnd")
    depends_on("cetmodules", type="build")

    def url_for_version(self, version):
        url = "https://github.com/SBNSoftware/{0}/archive/refs/tags/{1}.tar.gz"
        return url.format(self.name, version.underscored)

    def fetch_remote_versions(self, concurrency=None):
        return dict(
            map(
                lambda v: (v.dotted, self.url_for_version(v)),
                [
                    Version(d["name"][1:])
                    for d in sjson.load(
                        spack.util.web.read_from_url(
                            self.list_url, accept_content_type="application/json"
                        )[2]
                    )
                    if d["name"].startswith("v")
                ],
            )
        )

    def cmake_args(self):
        args = [
            "-DCMAKE_CXX_STANDARD={0}".format(self.spec.variants["cxxstd"].value),
            "-DICARUS_BUILD={0}".format(int("+icarus" in self.spec)),
            "-DSBND_BUILD={0}".format(int("+sbnd" in self.spec)),
            "-DSPACK_BUILD=1",
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
