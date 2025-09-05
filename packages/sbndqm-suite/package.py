# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack.package import *

class SbndqmSuite(BundlePackage):
    """The sbndqm suite; sbndqm is a repository for online data quality monitoring in SBN"""

    homepage="https://sbnsoftware.github.io/"

    squals = ("128","131","132")

    version("develop")
    version("v1_04_00")

    variant("sbnd", default=False, description="Enable SBND-specific runtime code")
    variant("icarus", default=False, description="Enable ICARUS-specific runtime code")

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

     # Dependencies for development head
    with when("@develop"):
        depends_on("artdaq-suite@v3_13_02 cxxstd=17", when="cxxstd=17")
        depends_on("artdaq-suite@v3_13_02 cxxstd=20", when="cxxstd=20")
        depends_on("sbndqm@develop")
        depends_on("sbndaq-online@develop")
        depends_on("sbndcode@10.06.00.01", type="run", when="+sbnd")
        depends_on("icaruscode@10.06.00.01p04", type="run", when="+icarus")

    # Dependencies for v1_04_00 release
    with when("@v1_04_00"):
        depends_on("artdaq-suite@v3_13_02 cxxstd=17", when="cxxstd=17")
        depends_on("artdaq-suite@v3_13_02 cxxstd=20", when="cxxstd=20")
        depends_on("sbndqm@v1_04_00") 
        depends_on("sbndaq-online@v1_01_00")
        depends_on("sbndcode@10.06.00.01", type="run", when="+sbnd")
        depends_on("icaruscode@10.06.00.01p04", type="run", when="+icarus")

