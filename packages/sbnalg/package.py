# Copyright2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack import *
from spack.package import *

class Sbnalg(CMakePackage):
    """
    SBN software not depending on art framework
    """

    git_base = "https://github.com/SBNSoftware/sbnalg"
    git = f"{git_base}.git"
    url = f"{git_base}/archive/v10_03_00.tar.gz"
    list_url = "https://github.com/SBNSoftware/sbnalg/tags"
    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("lardataalg")
    depends_on("sbnobj")
    depends_on("sbnanaobj")
    depends_on("cetmodules")

    version("10.24.00", sha256="4df4c29b3991ba85327f5ca92200ad39d2a04f0030f05b7426d08ec04c7165c8")
    version("10.06.00.01", sha256="cdf8ef0b02e349918189a3b62de535f49f7c9c61035a7a15d592dd97dbaf0841")
    version("10.04.07", sha256="d52b8fc243596662f037f19fe6f9d61296c7673bf200a11023279a715d0729bc")

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    def cmake_args(self):
        # Set CMake args.
        args = [
            "-DCMAKE_CXX_STANDARD={0}".format(self.spec.variants["cxxstd"].value),
            ]
        return args

    def patch(self):
        cetmodules_version = self.spec['cetmodules'].version.string
        filter_file('cetmodules 3.27.00 REQUIRED', 'cetmodules '+cetmodules_version+' REQUIRED','CMakeLists.txt')


    def url_for_version(self, version):
        url = "https://github.com/SBNSoftware/{0}/archive/v{1}.tar.gz"
        return url.format(self.name, version.underscored)
