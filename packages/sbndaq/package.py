# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.util.spack_json as sjson
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

    version("develop", git=git_base, branch="develop", get_full_repo=True)
    version("1.10.00", sha256="f0753c27bda6d5f81a8610ed6bee36286c16d4d24e844da626129f6c72340319")
    version("1.09.02", sha256="a3b30c878bdbc8fbabecae0035640c14d64ab07cc3405559d26eba9bc77b787f")
    version("1.09.01", sha256="6ff41011d1cee9bf6dcd2ee7919de6ff030fdf0387d052a57094d1d22227d613")
    version("1.09.00", sha256="d7c5b4d809a4838ec520c3afbe9ebb35bf20b0cfcc4fdcabff2a550fce2c99b2")
    version("1.08.06", sha256="84fb16af0a6581d5aeec325a7a2a2193fdb7e159a23ea0f68617fcf73beb7727")
    version("1.08.05", sha256="f03dc93293890b9b19215354f54abba9ad2b766bb2613e69b7baf8a28c31f195")
    version("1.08.04", sha256="e438f8bfcf72d285126c28275d9e93ea9b954dcadbc0c565f9f7561b44978610")
    version("1.08.01", sha256="dddb3f09e64635bd9cff416f183f393604bcdacac1f165427d0b66c847643b5c")
    version("1.08.00", sha256="8cdc92caf95566cbc85f099dd60a4f2dcd61d38161753cf7e3dcbe23e1ea1016")
    version("1.07.02", sha256="e6c47ba6e7004dde87c1791d9417ee3245508f272f208470435cec1ffe71998d")
    version("1.07.01", sha256="c590c494c16a264e7f79dc03595a2f15d0b486a3b629ce09742e14e8ea32ccc2")

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )
    
    variant("icarus", default=False, description="Build ICARUS-specific parts of the package")
    variant("sbnd", default=False, description="Build SBND-specific parts of the package")

    depends_on("sbndaq-artdaq")
    depends_on("sbndaq-artdaq+icarus", when="+icarus")
    depends_on("sbndaq-artdaq+sbnd", when="+sbnd")
    depends_on("cetmodules", type="build")

    def url_for_version(self, version):
        url = "https://github.com/SBNSoftware/{0}/archive/v{1}.tar.gz"
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
            "-DSPACK_BUILD=1"
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
