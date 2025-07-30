# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack.package import *

class Wibtools(CMakePackage):
    """Tools for communicating with the WIB hardware"""

    homepage = "https://github.com/SBNSoftware"
    url = "https://github.com/SBNSoftware/wibtools"
    git_base = "https://github.com/SBNSoftware/wibtools.git"
    list_url = "https://api.github.com/repos/SBNSoftware/wibtools/tags"

    version("v1_10_08", sha256="9271865422e2b50836bed0443e338e7f441c752da585311f6c1b860f704fc65b")
    version("v1_10_06", sha256="9421a3a4c224c02703b4920cac9fe12160014902512759fbfca816d65182ef4e")
    version("v1_10_04", sha256="73b03bc288d63b6fd09d54c326c934afe6522a4749e9664206c3175e2c6582d7")
    version("v1_10_03", sha256="cb44b6d53cc3f241ccd1a9f80f6400a4f881a5344ec2ab2ee73436194d2b637a")
    version("v1_10_02", sha256="367bfd9ed1ed227592075a1a2ebcc3aeb8dd43aed19f1cbfe3ae539b5b19035d")
    version("v1_10_01", sha256="66d85edb4516c01adc85378427776fc85ca001eb27613cf32ab819275d058975")
    version("v1_10_00", sha256="d729cd877212b5e2138930f645657e37ac21d013398a6ffdd2ccb97194d03876")
    
    version("migration", git=git_base, branch="feature/upgrade_gcc13.1.0", get_full_repo=True)
    version("develop", git=git_base, branch="develop", get_full_repo=True)

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("boost")
    depends_on("trace", type="build")
    depends_on("messagefacility")
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
        ]
        return args

    def setup_run_environment(self, env):
        prefix = self.prefix
        env.set("WIBTOOLS_BIN", prefix.bin)
        env.set("WIB_ADDRESS_TABLE_PATH", prefix + "/tables")
        env.set("WIB_CONFIG_PATH", prefix + "/config")

    def setup_dependent_run_environment(self, env, dependent_spec):
        prefix = self.prefix
        env.set("WIBTOOLS_BIN", prefix.bin)
        env.set("WIB_ADDRESS_TABLE_PATH", prefix + "/tables")
        env.set("WIB_CONFIG_PATH", prefix + "/config")
