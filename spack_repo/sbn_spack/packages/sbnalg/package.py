# Copyright2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack import *
from spack_repo.builtin.build_systems.cmake import CMakePackage
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

    version("develop", branch="develop", get_full_repo=True)
    version("10.23.00", sha256="68c5df50b37cb8c654d023bc988380edaf50c8b1b819d011760bc3b19d431005")
    version("10.22.00", sha256="f091c8b038712649db387327113be2958732f6d8f439fdef28552e92b2027812")
    version("10.20.09", sha256="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
    version("10.20.03", sha256="d64f1aea05c10430f8a30ae4cab8c825350bf3e2f38b203cc16b680058ce2cf9")
    version("10.12.02", sha256="887a1ebf0bf11da22159f185d922dc4ac60b26216fdb9b34694853bd66309137")
    version("10.11.01.01", sha256="035775680fc6ea0b28e7f186cdfc1dbbfc977de5eed70494406f93d928ddbb72")
    version("10.06.00.14lf01", sha256="cb988a3a728f51ab69970d608e5d7ba8e386f7a5bcfb5aa81e904e52cdb10706")
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
        sbndcode_version = self.version.string
        filter_file('cetmodules 3.27.00 REQUIRED', 'cetmodules '+cetmodules_version+' REQUIRED','CMakeLists.txt')


    def url_for_version(self, version):
        url = "https://github.com/SBNSoftware/{0}/archive/v{1}.tar.gz"
        return url.format(self.name, version.underscored)
