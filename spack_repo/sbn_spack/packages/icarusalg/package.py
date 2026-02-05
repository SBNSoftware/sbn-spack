# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *
from spack_repo.builtin.build_systems.cmake import CMakePackage


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


class Icarusalg(CMakePackage):
    """SignalProcessing for icarus
    framework for particle physics experiments.
    """

    homepage = "https://cdcvs.fnal.gov/redmine/projects/icarusalg"
    git_base = "https://github.com/SBNSoftware/icarusalg.git"
    git = git_base
    url = "https://github.com/SBNSoftware/icarusalg/archive/refs/tags/v10_06_00_01.tar.gz"
    list_url = "https://github.com/SBNSoftware/icarusalg/tags"

    version(
        "develop",
        git=git_base,
        get_full_repo=True,
    )
    version("10.06.00.06", sha256="932cbb3198819b1a6c8eb63f3af65f8ff5edd21dfdb05d09dcb743c2ff18a5f1")
    version("10.06.00.04", sha256="87dcfd9168426a5a371494740243ab5dd0b310473cab68db7e238d0cdc12f71f")
    version("10.04.08", sha256="21e4e39c8491c2cda0b299fdc34d9f368d1340f0537d5e5b20c2e311107d1fa9")
    version("10.04.07", sha256="2d2e2036c902c89ee4e37a4c6436d360fcabd6358b82288219fcc6f173db5e6a")
    version("10.04.06", sha256="bdb241b7d1429d8704aeda51465b28529dde621441f7b5136237992a124426cf")
    version("10.04.04", sha256="23f7f222f63cd27bf37b6931a2fc138130b0aed6933a41789b6715de7cbf4b6f")
    version("09.92.00", sha256="4d586a113b16be85c848e44b099feb35a185d7ce3c0ced5401fdc69fcd5d4045")
    version("09.91.02.01", sha256="c8bf89286de902edbd99224f9064caebc588fc30d6a35e169df716b99c9e54a7")
    version("09.89.02.01", sha256="788c8f5b07ce0998f94b303b6d432867ca83e977ac0c733599475f63c84f1750")
    version("09.62.00.02", sha256="7de4033d38030a8c6fddcb4caaa5d059d839f015e08dda8fd717b416e91877f1")
    version("09.62.00", sha256="1fc355403b034d473b7fab120740904de199d9295253342433544ac7ae19dbbf")
    version("09.58.00", sha256="699443a03bee6765fa008f5d9a753c74b416dee0b9abea97d34493f8f16e155b")
    version("09.53.01", sha256="3739a1d9c8473c9c858141a265dd3021b997354a399453fefe94609b13dd5dbe")
    version("09.52.01", sha256="d72278e81e8d7cc93ce6f584c9b0aaaa01e5cc7f005ad157ec2c1a531ade58ba")
    version("09.49.00", sha256="feeca0196cb5a113ebc0e75d3541fbab705470262eed7a19370d7bed6181074a")
    version("09.48.00", sha256="0cdb01ed5f1f0cf7258bf93041b45d5232de1784debc98087b5ba34fd8b62811")
    version("09.47.00", sha256="d25ed342181ea5df4fef2c5ad5fd48335fedc183d963641bfa655ff5c6acb84f")
    version("09.41.00", sha256="9cbbd55c42120812609e0166bfea5125034f8752fdddff62e744d2e527cc5e8a")
    version("09.37.02.09", sha256="85a3b7018e4ee45841273e30fe1630ffe13d28d83fd039c7c9d8dbfca0654099")

    version("10.06.00.01", sha256="1ea71b17bc2877b3d617d21cd9b95523152e19917ce7ae66f48412398fcbcc59")

    version(
        "09.37.02.01", sha256="717678d1015441349b892bb19efd2b09c5b5f6349dfb25a484bc9101d761b4eb"
    )
    version("09.37.01", sha256="048f3a88ebd66dd8ba6b8fbc536ea68bb58b7b48b3ffaa5ff555a301a838b11d")
    version("09.34.00", sha256="b55ab020b0a3239e0492183d7eb55501102693ee8123ca5ccef0d40a4f11b1d9")
    version("09.33.00", sha256="b61f8a2eb23405d151b69b3ee2d7d76f30ed35da9ff12426e680994cf7a3461a")
    version("09.32.01", sha256="2e5a7d1f41bfea02721a2f3d75ba5aae97587325fde143c4d0f608b1b929aafc")
    version("09.28.01", sha256="b97e6dc10c609604850ee2a5fcf1802c7288462a8c1081cc222157656952cadb")
    version("09.28.00", sha256="ad67ed3fd1b3bfee5a8c02fee64da6548fcdfa7021bcd9025f9f32fefd7ac9c2")

    patch("mwm.patch", when="@09.28.01")
    patch("cetmodules2.patch", when="@develop")
    patch("v09_34_00.patch", when="@09.34.00")
    patch("v09_37_01.patch", when="@09.37.01")
    patch("v09_37_02_01.patch", when="@09.37.02.01")

    def patch(self):
        # we need the backwards compat stuff turned on
        filter_file(
                '(find_package\\( *cetmodules .*\\))',
                '\\1\nset(CET_CETBUILDTOOLS_COMPAT TRUE)\ninclude(compat/CetMakeCommand)\nset(CET_WARN_DEPRECATED)',
                'CMakeLists.txt',
            )
        filter_file(
                'find_package\\( *celib *\\)',
                'find_package( cetlib )',
                'CMakeLists.txt',
            )

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    # Build-only dependencies.
    depends_on("cmake@3.11:")
    depends_on("cetmodules", type="build")
    depends_on("c", type="build")
    depends_on("cxx", type="build")

    # Build and link dependencies.
    depends_on("boost", type=("build", "run"))
    depends_on("canvas-root-io", type=("build", "run"))
    depends_on("canvas", type=("build", "run"))
    depends_on("catch2", type=("build", "run"))
    depends_on("cetlib-except", type=("build", "run"))
    depends_on("cetlib", type=("build", "run"))
    depends_on("clhep", type=("build", "run"))
    depends_on("cppgsl", type=("build", "run"))
    depends_on("dk2nudata", type=("build", "run"))
    depends_on("fhicl-cpp", type=("build", "run"))
    depends_on("gallery", type=("build", "run"))
    depends_on("gsl", type=("build", "run"))
    depends_on("hep-concurrency", type=("build", "run"))
    depends_on("larcorealg", type=("build", "run"))
    depends_on("larcoreobj", type=("build", "run"))
    depends_on("lardataalg", type=("build", "run"))
    depends_on("lardataobj", type=("build", "run"))
    depends_on("messagefacility", type=("build", "run"))
    depends_on("nlohmann-json", type=("build", "run"))
    depends_on("nufinder", type=("build", "run"))
    depends_on("nusimdata", type=("build", "run"))
    depends_on("range-v3", type=("build", "run"))
    depends_on("root", type=("build", "run"))
    depends_on("tbb", type=("build", "run"))
    depends_on("vdt", type=("build", "run"))

    if "SPACKDEV_GENERATOR" in os.environ:
        generator = os.environ["SPACKDEV_GENERATOR"]
        if generator.endswith("Ninja"):
            depends_on("ninja", type="build")

    def url_for_version(self, version):
        # url = 'https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/{0}.v{1}.tbz2'
        url = "https://github.com/SBNSoftware/{0}/archive/v{1}.tar.gz"
        return url.format(self.name, version.underscored)

    def cmake_args(self):
        # Set CMake args        args = ['-DCMAKE_CXX_STANDARD={0}'.
        args = [
            "-DCMAKE_CXX_STANDARD={0}".format(self.spec.variants["cxxstd"].value),
            "-DCPPGSL_INC={0}".format(self.spec["cppgsl"].prefix.include),
            "-DVDT_INCLUDE_DIR={0}".format(self.spec["vdt"].prefix.include),
            "-DVDT_LIBRARY={0}".format(self.spec["vdt"].prefix.lib),
        ]
        return args

    def setup_build_environment(self, spack_env):

        # easier to set these than patch the CMakeLists.txts for now
        # but there sure are a lot of them...
        spack_env.set("BOOST_INC", self.spec["boost"].prefix.include)
        spack_env.set("CANVAS_INC", self.spec["canvas"].prefix.include)
        spack_env.set("CANVAS_ROOT_IO_INC", self.spec["canvas-root-io"].prefix.include)
        spack_env.set("CETLIB_EXCEPT_INC", self.spec["cetlib-except"].prefix.include)
        spack_env.set("CETLIB_INC", self.spec["cetlib"].prefix.include)
        spack_env.set("CLHEP_INC", self.spec["clhep"].prefix.include)
        spack_env.set("FHICLCPP_INC", self.spec["fhicl-cpp"].prefix.include)
        spack_env.set("GALLERY_INC", self.spec["gallery"].prefix.include)
        spack_env.set("ICARUSALG_INC", self.spec.prefix.include)
        spack_env.set("HEP_CONCURRENCY_INC", self.spec["hep-concurrency"].prefix.include)
        spack_env.set("LARCOREALG_INC", self.spec["larcorealg"].prefix.include)
        spack_env.set("LARCOREOBJ_INC", self.spec["larcoreobj"].prefix.include)
        spack_env.set("LARDATAALG_INC", self.spec["lardataalg"].prefix.include)
        spack_env.set("LARDATAOBJ_INC", self.spec["lardataobj"].prefix.include)
        spack_env.set("MESSAGEFACILITY_INC", self.spec["messagefacility"].prefix.include)
        spack_env.set("NUSIMDATA_INC", self.spec["nusimdata"].prefix.include)
        spack_env.set("ROOT_INC", self.spec["root"].prefix.include)

        spack_env.prepend_path("LD_LIBRARY_PATH", str(self.spec["root"].prefix.lib))
        # Binaries.
        spack_env.prepend_path("PATH", os.path.join(self.build_directory, "bin"))
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", os.path.join(self.build_directory, "lib"))
        # Ensure Root can find headers for autoparsing.
        for d in self.spec.traverse(
            root=False, cover="nodes", order="post", deptype=("link"), direction="children"
        ):
            spack_env.prepend_path("ROOT_INCLUDE_PATH", str(self.spec[d.name].prefix.include))
        # Perl modules.
        spack_env.prepend_path("PERL5LIB", os.path.join(self.build_directory, "perllib"))
        # Cleaup.
        sanitize_environments(spack_env)

    def setup_run_environment(self, run_env):
        run_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        # Ensure Root can find headers for autoparsing.
        for d in self.spec.traverse(
            root=False, cover="nodes", order="post", deptype=("link"), direction="children"
        ):
            run_env.prepend_path("ROOT_INCLUDE_PATH", str(self.spec[d.name].prefix.include))
        run_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        # Perl modules.
        run_env.prepend_path("PERL5LIB", os.path.join(self.prefix, "perllib"))
        # Cleaup.
        sanitize_environments(run_env)

    def setup_dependent_build_environment(self, spack_env, dependent_spec):
        # Binaries.
        spack_env.prepend_path("PATH", self.prefix.bin)
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        # Ensure Root can find headers for autoparsing.
        spack_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        # Perl modules.
        spack_env.prepend_path("PERL5LIB", os.path.join(self.prefix, "perllib"))
        #
        spack_env.append_path("FW_SEARCH_PATH", "{0}/gdml".format(self.prefix))
        # Cleanup.
        sanitize_environments(spack_env)

    def setup_dependent_run_environment(self, run_env, dependent_spec):
        # Binaries.
        run_env.prepend_path("PATH", self.prefix.bin)
        # Ensure we can find plugin libraries.
        run_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        # Ensure Root can find headers for autoparsing.
        run_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        # Perl modules.
        run_env.prepend_path("PERL5LIB", os.path.join(self.prefix, "perllib"))
        #
        run_env.append_path("FW_SEARCH_PATH", "{0}/gdml".format(self.prefix))
        # Cleanup.
        sanitize_environments(run_env)
