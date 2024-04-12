# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.util.spack_json as sjson
from spack.package import *


class Wibtools(CMakePackage):
    """Tools for communicating with the WIB hardware"""

    homepage = "https://github.com/SBNSoftware"
    url = "https://github.com/SBNSoftware/wibtools"
    git_base = "https://github.com/SBNSoftware/wibtools.git"
    list_url = "https://api.github.com/repos/SBNSoftware/wibtools/tags"

    version("develop", git=git_base, branch="develop", get_full_repo=True)

    version("v1_10_01", sha256="66d85edb4516c01adc85378427776fc85ca001eb27613cf32ab819275d058975") 
    version("v1_10_00", sha256="d729cd877212b5e2138930f645657e37ac21d013398a6ffdd2ccb97194d03876")   
    version("v1_09_01", sha256="0702a5c8bf7cfa936557a95d6320e872651b90bbc9457e853f25e9048fbdda0f")
    version("v1_09_00", sha256="4835bf6185481bf500551042a6cb9e2e28811262745a497f92bb409a525cf557")
    version("v1_08_06", sha256="9e9e0c46dc082a2f0de5abd1f6054c31e60cbdcb43ea8a796249a8b5cce1ea80")
    version("v1_08_05", sha256="9f0a26689bcb2acebb34f315989c8c7ebda8d80fcc0f531879628aa1128a3d47")
    version("v1_08_04", sha256="1088189c0e66c32547d381ceb6d9ddcaa054438e0dcec8e82dc443369d77f46b")
    version("v1_08_03", sha256="1ec4d4bb2f508069eaf56d619486b19b9ccc4aaca93141846c4bcac8c6266d6c")
    version("v1_08_02", sha256="3034d12ad162090ede7476c4dc9867c1ee5bbdfc1b6d377dd1b49eca0ff131ce")
    version("v1_08_00", sha256="1c496184d30f3c5aa633add614c6ccd517b9c46a7d128e6c2049fcbe445b2190")

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
        ]
        return args
 
    def setup_run_environment(self, env):
        prefix = self.prefix
        env.set("WIBTOOLS_BIN", prefix.bin)
        env.set("WIB_ADDRESS_TABLE_PATH", prefix + "/tables")
        env.set("EIB_CONFIG_PATH", prefix + "/config")
        
    def setup_dependent_run_environment(self, env, dependent_spec):
        prefix = self.prefix
        env.set("WIBTOOLS_BIN", prefix.bin)
        env.set("WIB_ADDRESS_TABLE_PATH", prefix + "/tables")
        env.set("EIB_CONFIG_PATH", prefix + "/config")
