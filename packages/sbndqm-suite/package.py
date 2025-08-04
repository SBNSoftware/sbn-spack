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

    version("develop")
    version("v1_04_00")

    variant("sbnd", default=True, description="Enable SBND-specific runtime code")
    variant("icarus", default=True, description="Enable ICARUS-specific runtime code")

     # Dependencies for development head
    with when("@develop"):
        depends_on("sbndqm@develop")
        depends_on("sbndaq-online@develop")
        depends_on("sbndcode@v10_06_00_01", type="run", when="+sbnd")
        depends_on("icaruscode@v10_06_00_01p01", type="run", when="+icarus")

    # Dependencies for v1_04_00 release
    with when("@v1_04_00"):
        depends_on("sbndqm@v1_04_00") 
        depends_on("sbndaq-online@v1_01_00")
        depends_on("sbndcode@v10_06_00_01", type="run", when="+sbnd")
        depends_on("icaruscode@v10_06_00_01p01", type="run", when="+icarus")

