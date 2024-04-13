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

class SbndaqArtdaq(CMakePackage):
    """Readout software for the SBN experiments"""

    homepage = "https://github.com/SBNSoftware"
    url = "https://github.com/SBNSoftware/sbndaq-artdaq"
    git_base = "https://github.com/SBNSoftware/sbndaq-artdaq.git"
    list_url = "https://api.github.com/repos/SBNSoftware/sbndaq-artdaq/tags"


    version("develop", git=git_base, branch="develop", get_full_repo=True)

    version("v1_10_01", sha256="e343567c84c926aa9a247f9278d91bdc9566984b22d0115746807408d7ca7b40")
    version("v1_10_00", sha256="4bdf854e55fc23de385aafee01e3d658411bf0402fd87578a8efc77be0e18b7c")

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )
    
    variant("icarus", default=False, description="Build ICARUS-specific parts of the package")
    variant("sbnd", default=False, description="Build SBND-specific parts of the package")

    depends_on("artdaq")
    depends_on("sbndaq-artdaq-core")
    depends_on("sbndaq-artdaq-core+icarus", when="+icarus")
    depends_on("sbndaq-artdaq-core+sbnd", when="+sbnd")
    depends_on("caenvmelib")
    depends_on("caencomm")
    depends_on("caendigitizer")
    depends_on("libpqxx")
    depends_on("postgresql")
    depends_on("artdaq-epics-plugin") # For FindEPICS.cmake
    depends_on("epics-base")
    depends_on("cppzmq")
    depends_on("jsoncpp")
    depends_on("wibtools", when="+sbnd")
    depends_on("windriver@v12_06_00", when="+sbnd")
    depends_on("redis")
    depends_on("hiredis")
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
            "-DSPACK_BUILD=1"
        ]
        return args

    def flag_handler(self, name, flags):
        flags.append("-lpq")
        return inject_flags(name, flags)

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
    
