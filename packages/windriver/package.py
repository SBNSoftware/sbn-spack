# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Windriver(Package):
    """Windriver library"""

    homepage = "https://jungo.com/windriver/"
    #url = "https://jungo.com/windriver/#download"

    version("v12_06_00", sha256="ac8098822dbc0290a49c79d9f59c7552ad4410ca4e4880eb2e90bf2ade6c8720")

    def url_for_version(self, version):
        url = "https://scisoft.fnal.gov/scisoft/packages/windriver/v12_06_00/windriver.tgz"
        return url.format(version)

    def build(self, spec, prefix):
        pass

    def install(self, spec, prefix):
        install_tree("include", prefix.include)

        if self.spec.target.family == "aarch64":
            install_tree("lib/arm64", prefix.lib)
        elif self.spec.target.family == "x86":
            install_tree("lib/x86", prefix.lib)
        else:
            install_tree("lib/x64", prefix.lib)

        libs = find(prefix.lib, "lib*")
        print(libs)

    def setup_dependent_build_environment(self, spack_env, dependent_spec):
        spack_env.set("WINDRIVER_INC", self.prefix.include)
        spack_env.set("WINDRIVER_LIB", self.prefix.lib)
