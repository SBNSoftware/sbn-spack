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
    version("1.10.00", sha256="4bdf854e55fc23de385aafee01e3d658411bf0402fd87578a8efc77be0e18b7c")
    version("1.09.02", sha256="25f74b2d6e199ab64c077c001a03827fc20ea42ee1f0685a7b3d85ef2cb6fa79")
    version("1.09.01", sha256="7b38e3a673ffcf668139da2bec01728b29a234acc610dcbdb6603d6aa4ed8f64")
    version("1.09.00", sha256="2dd654d110587871857e3e6b94e52807f371113880386647c2af28100428c50c")
    version("1.08.06", sha256="43676381b7387a9fff957acbacd438b7b080f9dfeafa01d6a4bd6cde50979265")
    version("1.08.05", sha256="217debd9f36e82a5426c839704530e9c0d1d504bbe5f904eead9e9999d324cf9")
    version("1.08.04", sha256="34c873db09580481602b290b267296e19eb3ff8f19200c75765cb932da1e597a")
    version("1.08.03", sha256="e8b6984dd8b91756aa63bda7c28d67f0ae4be10cacee908d739d5cd7f1bb7d37")
    version("1.08.01", sha256="8c636599ef5d4e02771a82e3e19c65676665df5f789b8bee60a83d4b42779d29")
    version("1.08.00", sha256="156554958cc4894b1fc0c506f512bd4ae3ff69a2ca694ba5c03a1795587ef66a")
    version("1.07.02", sha256="899ff79d5369a6d54462016537e366c9f4439723b6836ad91464b954c646135b")
    version("1.07.01", sha256="d4eb0f9cf5187c0059eef80234d27e96ca29938317c049833caddb624903ed62")

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
    #depends_on("windriver", when="+sbnd")
    depends_on("redis")
    depends_on("hiredis")
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

#    def flag_handler(self, name, flags):
#        flags.append("-lpq")
#        return env_flags(name, flags)
#
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
    
