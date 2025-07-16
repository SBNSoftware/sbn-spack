# Copyright2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack import *
from spack.package import *
from spack.package import *

libdir = "%s/var/spack/repos/fnal_art/lib" % os.environ["SPACK_ROOT"]
if libdir not in sys.path:
    sys.path.append(libdir)


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


class Sbndcode(CMakePackage):
    """The eponymous package of the Sbn experiment
    framework for particle physics experiments.
    """

    git_base = "https://github.com/SBNSoftware/sbndcode.git"

    version("10.06.00.01", sha256="5ad9dfb9e96adf82a9f0a6fcbcb8042664b1349fe4f44374462f17fce2d95b51")
    version("10.04.07", tag="v10_04_07", git=git_base, get_full_repo=True)
    version("10.04.06.01",tag="v10_04_06_01", git=git_base, get_full_repo=True)
    version("09.93.01.02.01", tag="v09_93_01_02p01", git=git_base, get_full_repo=True)
    version("09.93.01.02", tag="v09_93_01_02rc0", git=git_base, get_full_repo=True)
    version("09.93.01.01", tag="v09_93_01_01", git=git_base, get_full_repo=True)
    version("09.93.01", tag="v09_93_01", git=git_base, get_full_repo=True)
    version("09.91.02.02", tag="v09_91_02_02", git=git_base, get_full_repo=True)
    version("09.91.02.01", tag="v09_91_02_01", git=git_base, get_full_repo=True)
    version("09.90.00", tag="v09_90_00", git=git_base, get_full_repo=True)
    version("09.32.00", tag="v09_32_00", git=git_base, get_full_repo=True)
    version("09.10.00", tag="v09_10_00", git=git_base, get_full_repo=True)
    version("09.10.01", tag="v09_10_01", git=git_base, get_full_repo=True)

    patch("spack.patch")
    patch("v09_32_00.patch", when="@9.32.00")
    patch("v09_90_00.patch", when="@9.90.00")
    patch("v09_91_02_02.patch", when="@9.91.02.02")
    patch("v09_91_02_01.patch", when="@9.91.02.01")
    patch("v09_93_01_01.patch", when="@09.93.01.01")
    patch("v09_93_01_02.patch", when="@09.93.01.02")

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("cmake@3.11:")
    depends_on("cetmodules", type="build")
    depends_on("cetbuildtools", type="build")
    depends_on("libjpeg", type="build")
    depends_on("libpng", type="build")
    depends_on("giflib", type="build")
    depends_on("eigen", type=("build", "run"))
    depends_on("libwda", type=("build", "run"))
    depends_on("marley", type=("build", "run"))
    depends_on("postgresql", type=("build", "run"))
    depends_on("dk2nudata", type=("build", "run"))

    #depends_on("larg4", type=("build", "run"))
    #depends_on("larcorealg", type=("build", "run"))
    #depends_on("nuevdb", type=("build", "run"))
    depends_on("cry", type=("build", "run"))
    depends_on("dk2nugenie", type=("build", "run"))
    #depends_on("log4cpp", type=("build", "run"))
    depends_on("rstartree", type=("build", "run"))
    #depends_on("wirecell", type=("build", "run"))
    #depends_on("hdf5", type=("build", "run"))
    #depends_on("hep-hpc", type=("build", "run"))
    #depends_on("genie-xsec", type=("build", "run"))
    #depends_on("nugen", type=("build", "run"))
    #depends_on("larsimdnn", type=("build", "run"))

    depends_on("vdt", type=("build", "run"))
    depends_on("sbncode", type=("build", "run"))
    depends_on("sbnd-data", type=("build", "run"))
    depends_on("cetmodules", type=("build", "run"))

    if "SPACKDEV_GENERATOR" in os.environ:
        generator = os.environ["SPACKDEV_GENERATOR"]
        if generator.endswith("Ninja"):
            depends_on("ninja", type="build")

    def patch(self):
        cetmodules_version = self.spec['cetmodules'].version.string
        sbndcode_version = self.version.string
        filter_file('cetmodules REQUIRED', 'cetmodules '+cetmodules_version+' REQUIRED','CMakeLists.txt')
        filter_file('sbndcode LANGUAGES', 'sbndcode VERSION '+sbndcode_version+' LANGUAGES','CMakeLists.txt')

    def url_for_version(self, version):
        url = "https://github.com/SBNSoftware/{0}/archive/v{1}.tar.gz"
        return url.format(self.name, version.underscored)

    def cmake_args(self):
        # Set CMake args.
        args = [
            "-DIGNORE_ABSOLUTE_TRANSITIVE_DEPENDENCIES=True",
            "-DCMAKE_CXX_STANDARD={0}".format(self.spec.variants["cxxstd"].value),
            "-Dsbndcode_FW_DIR=fw",
            "-Dsbndcode_WP_DIR={0}".format(self.spec["wirecell"].prefix),
            "-DCMAKE_PREFIX_PATH={0}".format(
                self.spec["sbnanaobj"].prefix),
            "-DCMAKE_PREFIX_PATH={0}/lib/python{1}/site-packages/torch".format(
                self.spec["py-torch"].prefix, self.spec["python"].version.up_to(2)
            ),
            "-DTensorFlow_INCLUDE_DIR={0}/lib/python{1}/site-packages/tensorflow/include".format(
                    self.spec["py-tensorflow"].prefix, "3.9"),
            "-DTensorFlow_LIBRARIES={0}/lib/python{1}/site-packages/tensorflow".format(
                    self.spec["py-tensorflow"].prefix, "3.9"),
            "-DTensorFlow_cc_LIBRARY={0}/lib/python{1}/site-packages/tensorflow/libtensorflow_framework.so".format(
                    self.spec["py-tensorflow"].prefix, "3.9"),
            "-DTensorFlow_framework_LIBRARY={0}/lib/python{1}/site-packages/tensorflow/libtensorflow_cc.so".format(
                    self.spec["py-tensorflow"].prefix, "3.9"),
            ]
        return args

    def setup_build_environment(self, spack_env):
        # Binaries.
        spack_env.prepend_path("PATH", os.path.join(self.build_directory, "bin"))
        spack_env.set("SBNDCODE_DIR", str(self.build_directory))
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", os.path.join(self.build_directory, "lib"))
        # Ensure Root can find headers for autoparsing.
        for d in self.spec.traverse(
            root=False, cover="nodes", order="post", deptype=("link"), direction="children"
        ):
            spack_env.prepend_path("ROOT_INCLUDE_PATH", str(self.spec[d.name].prefix.include))
        # Perl modules.
        spack_env.prepend_path("PERL5LIB", os.path.join(self.build_directory, "perllib"))
        spack_env.prepend_path("GENIE_INC", str(self.spec["genie"].prefix.include))
        spack_env.prepend_path("hep_hpc_DIR", str(self.spec["hep-hpc"].prefix))
        spack_env.prepend_path("LD_LIBRARY_PATH", "{0}/lib/python{1}/site-packages/tensorflow".format(self.spec["py-tensorflow"].prefix, "3.9"))
        # Cleaup.
        sanitize_environments(spack_env)

    def setup_run_environment(self, run_env):
        # Binaries.
        run_env.prepend_path("PATH", os.path.join(self.prefix, "bin"))
        # Ensure we can find plugin libraries.
        run_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        # Ensure Root can find headers for autoparsing.
        #for d in self.spec.traverse(
        #    root=False, cover="nodes", order="post", deptype=("link"), direction="children"
        #):
        #    run_env.prepend_path("ROOT_INCLUDE_PATH", str(self.spec[d.name].prefix.include))
        run_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        # Perl modules.
        run_env.prepend_path("PERL5LIB", os.path.join(self.prefix, "perllib"))
        # sbnd_data path       
        run_env.prepend_path("FW_SEARCH_PATH", os.path.join(self.spec['sbnd-data'].prefix))
        # fcl file prefix
        run_env.prepend_path("FHICL_FILE_PATH", self.prefix.fcl)
        run_env.prepend_path("FHICL_INCLUDE_PATH", self.prefix.fcl)
        # Add to wire-cell path
        run_env.prepend_path("WIRECELL_PATH", os.path.join(self.spec['wirecell'].prefix))
        # Cleaup.
        # sanitize_environments(run_env)


    def setup_dependent_build_environment(self, spack_env, dependent_spec):
        # Binaries.
        spack_env.prepend_path("PATH", self.prefix.bin)
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        # Ensure Root can find headers for autoparsing.
        spack_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        # Perl modules.
        spack_env.prepend_path("PERL5LIB", os.path.join(self.prefix, "perllib"))
        # Cleanup.
        sanitize_environments(spack_env) 
