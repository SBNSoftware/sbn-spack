# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack.package import *

class SbndaqSuite(BundlePackage):
    """The sbndaq suite; artdaq is a data acquisition framework that leverages the analysis capabilities of art"""

    homepage="https://sbnsoftware.github.io/"

    squals = ("128","131","132")


    version("v1_10_08")
    version("v1_10_07")
    version("v1_10_06")
    version("v1_10_05")
    version("v1_10_04")
    version("v1_10_03")
    version("v1_10_02")
    version("v1_10_01")
    version("v1_10_00")

    version("migration_artdaqv3_13_02")
    version("migration_artdaqv4_01_00")

    version("develop")

    variant("icarus", default=True, description="Build ICARUS-specific parts of the package")
    variant("sbnd", default=True, description="Build SBND-specific parts of the package")
    variant("gdb", default=False, description="Built with GDB version 14.2")


    variant(
        "cxxstd",
        default="17",
        values=("17", "20"),
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
    for squal in squals:
        depends_on(f"artdaq-suite s={squal}", when=f"s={squal}")
    depends_on("artdaq-suite", when="s=0")

    depends_on("root+spectrum", when="+sbnd")
    depends_on("artdaq-suite+db+epics+demo~pcp")
    depends_on("sbndaq+sbnd", when="+sbnd")
    depends_on("sbndaq+icarus", when="+icarus")

    depends_on("gdb@14.2+tui+source-highlight+ld+lto+quad", when="+gdb")
    depends_on("binutils@2.43.1+gas")

    with when("@migration_artdaqv4_01_00"):
        depends_on("artdaq-suite@v4_01_00 cxxstd=17", when="cxxstd=17")
        depends_on("artdaq-suite@v4_01_00 cxxstd=20", when="cxxstd=20")
        #
        depends_on("caenvmelib@4.0.2")
        depends_on("caencomm@1.7.0")
        depends_on("caendigitizer@2.17.3")
        #
        depends_on("wibtools@migration")
        depends_on("sbndaq-artdaq-core@migration")
        depends_on("sbndaq-artdaq@migration")
        depends_on("sbndaq@migration")
        depends_on("artdaq-runcontrol-gui@v1_03_06")

    with when("@migration_artdaqv3_13_02"):
        depends_on("artdaq-suite@v3_13_02 cxxstd=17", when="cxxstd=17")
        depends_on("artdaq-suite@v3_13_02 cxxstd=20", when="cxxstd=20")
        #
        depends_on("caenvmelib@4.0.2")
        depends_on("caencomm@1.7.0")
        depends_on("caendigitizer@2.17.3")
        #
        depends_on("wibtools@migration")
        depends_on("sbndaq-artdaq-core@migration")
        depends_on("sbndaq-artdaq@migration")
        depends_on("sbndaq@migration")
        depends_on("artdaq-runcontrol-gui@v1_03_06")

    with when("@develop"):
        depends_on("artdaq-suite@v3_13_02 cxxstd=17", when="cxxstd=17")
        depends_on("artdaq-suite@v3_13_02 cxxstd=20", when="cxxstd=20")
        #
        depends_on("caenvmelib@4.0.2")
        depends_on("caencomm@1.7.0")
        depends_on("caendigitizer@2.17.3")
        #
        depends_on("wibtools@develop")
        depends_on("sbndaq-artdaq-core@develop")
        depends_on("sbndaq-artdaq@develop")
        depends_on("sbndaq@develop")
        depends_on("artdaq-runcontrol-gui@develop")

##insert-here
    with when("@v1_10_08"):
        depends_on("artdaq-suite@v3_13_02 cxxstd=17", when="cxxstd=17")
        depends_on("artdaq-suite@v3_13_02 cxxstd=20", when="cxxstd=20")
        #
        depends_on("caenvmelib@4.0.2")
        depends_on("caencomm@1.7.0")
        depends_on("caendigitizer@2.17.3")
        #
        depends_on("wibtools@v1_10_08")
        depends_on("sbndaq-artdaq-core@v1_10_08")
        depends_on("sbndaq-artdaq@v1_10_08")
        depends_on("sbndaq@v1_10_08")
        depends_on("artdaq-runcontrol-gui@v1_03_06")

    with when("@v1_10_07"):
        depends_on("artdaq-suite@v3_13_02")
        #
        depends_on("caenvmelib@4.0.2")
        depends_on("caencomm@1.7.0")
        depends_on("caendigitizer@2.17.3")
        #
        depends_on("wibtools@v1_10_06")
        depends_on("sbndaq-artdaq-core@v1_10_06")
        depends_on("sbndaq-artdaq@v1_10_07")
        depends_on("sbndaq@v1_10_07")
        depends_on("artdaq-runcontrol-gui@v1_03_06")

    with when("@v1_10_06"):
        depends_on("artdaq-suite@v3_13_02")
        #
        depends_on("caenvmelib@4.0.2")
        depends_on("caencomm@1.7.0")
        depends_on("caendigitizer@2.17.3")
        #
        depends_on("wibtools@v1_10_06")
        depends_on("sbndaq-artdaq-core@v1_10_06")
        depends_on("sbndaq-artdaq@v1_10_06")
        depends_on("sbndaq@v1_10_06")
        depends_on("artdaq-runcontrol-gui@v1_03_06")

    with when("@v1_10_05"):
        depends_on("artdaq-suite@v3_13_02")
        #
        depends_on("caenvmelib@4.0.2")
        depends_on("caencomm@1.7.0")
        depends_on("caendigitizer@2.17.3")
        #
        depends_on("wibtools@v1_10_04")
        depends_on("sbndaq-artdaq-core@v1_10_04")
        depends_on("sbndaq-artdaq@v1_10_05")
        depends_on("sbndaq@v1_10_05")
        depends_on("artdaq-runcontrol-gui@v1_03_06")

    with when("@v1_10_04"):
        depends_on("artdaq-suite@v3_13_02")
        #
        depends_on("caenvmelib@4.0.2")
        depends_on("caencomm@1.7.0")
        depends_on("caendigitizer@2.17.3")
        #
        depends_on("wibtools@v1_10_04")
        depends_on("sbndaq-artdaq-core@v1_10_04")
        depends_on("sbndaq-artdaq@v1_10_04")
        depends_on("sbndaq@v1_10_04")
        depends_on("artdaq-runcontrol-gui@v1_03_06")

    with when("@v1_10_03"):
        depends_on("artdaq-suite@v3_13_02")
        #
        depends_on("caenvmelib@4.0.1")
        depends_on("caencomm@1.7.0")
        depends_on("caendigitizer@2.17.3")
        #
        depends_on("wibtools@v1_10_03")
        depends_on("sbndaq-artdaq-core@v1_10_03")
        depends_on("sbndaq-artdaq@v1_10_03")
        depends_on("sbndaq@v1_10_03")
        depends_on("artdaq-runcontrol-gui@v1_03_05")

    with when("@v1_10_02"):
        depends_on("artdaq-suite@v3_13_02")
        #
        depends_on("caenvmelib@4.0.1")
        depends_on("caencomm@1.7.0")
        depends_on("caendigitizer@2.17.3")
        #
        depends_on("wibtools@v1_10_02")
        depends_on("sbndaq-artdaq-core@v1_10_02")
        depends_on("sbndaq-artdaq@v1_10_02")
        depends_on("sbndaq@v1_10_02")
        depends_on("artdaq-runcontrol-gui@v1_03_05")

    with when("@v1_10_01"):
        depends_on("artdaq-suite@v3_13_00")
        #
        depends_on("caenvmelib@4.0.1")
        depends_on("caencomm@1.7.0")
        depends_on("caendigitizer@2.17.3")
        #
        depends_on("wibtools@v1_10_01")
        depends_on("sbndaq-artdaq-core@v1_10_01")
        depends_on("sbndaq-artdaq@v1_10_01")
        depends_on("sbndaq@v1_10_01")
        depends_on("artdaq-runcontrol-gui@v1_03_05")

    with when("@v1_10_00"):
        depends_on("artdaq-suite@v3_13_00")
        #
        depends_on("caenvmelib@4.0.1")
        depends_on("caencomm@1.7.0")
        depends_on("caendigitizer@2.17.3")
        #
        depends_on("wibtools@v1_10_00")
        depends_on("sbndaq-artdaq-core@v1_10_00")
        depends_on("sbndaq-artdaq@v1_10_00")
        depends_on("sbndaq@v1_10_00")
