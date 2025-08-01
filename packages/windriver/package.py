# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Windriver(Package):
    """Windriver library"""

    homepage = "https://jungo.com/windriver/"

    version("v16_04_00", sha256="e683b4e4456afa5a17c5a3f4b44ffabf130559dff637b7a78a51a1c9f7d54b66")
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
