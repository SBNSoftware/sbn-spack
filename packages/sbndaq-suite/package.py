# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class SbndaqSuite(BundlePackage):
    """The sbndaq suite; artdaq is a data acquisition framework that leverages the analysis capabilities of art"""

    homepage="https://sbnsoftware.github.io/"
    
    squals = ("120a", "120b", "130")

    version("develop")
    
    version("v1_10_01")
    version("v1_10_00")

    variant("icarus", default=True, description="Build ICARUS-specific parts of the package")
    variant("sbnd", default=True, description="Build SBND-specific parts of the package")
    
    variant(
        "s",
        default="130",
        values=("0",) + squals,
        multi=False,
        description="Artdaq suite version to use",
    )
    for squal in squals:
        depends_on(f"artdaq-suite s={squal}", when=f"s={squal}")

    depends_on("elfutils+nls ldflags=-lintl")
    depends_on("libxpm ldflags=-lintl")
    depends_on("krb5 ldflags=-lintl")
    depends_on("root+spectrum", when="+sbnd")
    depends_on("artdaq-suite+db+epics+demo~pcp")
    depends_on("sbndaq+sbnd", when="+sbnd") 
    depends_on("sbndaq+icarus", when="+icarus") 

    with when("@develop"):
        depends_on("artdaq-suite@v3_13_00")
        #
        depends_on("wibtools@develop")
        depends_on("sbndaq-artdaq-core@develop")
        depends_on("sbndaq-artdaq@develop")
        depends_on("sbndaq@develop")
    
    with when("@v1_10_01"):
        depends_on("artdaq-suite@v3_13_00")
        #
        depends_on("wibtools@v1_10_01")
        depends_on("sbndaq-artdaq-core@v1_10_01")
        depends_on("sbndaq-artdaq@v1_10_01")
        depends_on("sbndaq@v1_10_01")
    
    with when("@v1_10_00"):
        depends_on("artdaq-suite@v3_13_00")
        #
        depends_on("wibtools@v1_10_00")
        depends_on("sbndaq-artdaq-core@v1_10_00")
        depends_on("sbndaq-artdaq@v1_10_00")
        depends_on("sbndaq@v1_10_00")
