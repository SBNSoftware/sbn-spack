# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Windriver(Package):
    """Windriver library"""

    homepage = "https://jungo.com/windriver/"

    version("v16_05_00", sha256="c5b06e494d9ce394fbbb0d403a0763460d47c9a3de3fa228d39a86e344fdd0c6")
    version("v16_04_00", sha256="827a6645f7e132136ddd057f52d71d4adfba2fcd34d27bf21e81f9547e797485")
    version("v12_06_00", sha256="ac8098822dbc0290a49c79d9f59c7552ad4410ca4e4880eb2e90bf2ade6c8720")

    def url_for_version(self, version):
        """Constructs the URL for a given version."""
        try:
            url = "https://scisoft.fnal.gov/scisoft/packages/windriver/{0}/windriver.tgz"
            return url.format(version)
        except Exception as e:
            raise SpackError(f"Could not construct URL for version {version}: {e}") from e

    def build(self, spec, prefix):
        pass

    def install(self, spec, prefix):
        try:
            install_tree("include", prefix.include)

            if self.spec.target.family == "aarch64":
                install_tree("lib/arm64", prefix.lib)
            elif self.spec.target.family == "x86":
                install_tree("lib/x86", prefix.lib)
            else:
                install_tree("lib/x64", prefix.lib)
        except Exception as e:
            raise InstallError(f"Failed to install Windriver: {e}") from e

    def setup_dependent_build_environment(self, spack_env, dependent_spec):
        spack_env.set("WINDRIVER_INC", self.prefix.include)
        spack_env.set("WINDRIVER_LIB", self.prefix.lib)
