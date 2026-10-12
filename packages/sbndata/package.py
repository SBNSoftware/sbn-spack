# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install sbndata
#
# You can edit this file again by typing:
#
#     spack edit sbndata
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

import sys
from spack.package import *
import glob

class Sbndata(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    url = "https://github.com/SBNSoftware/sbndata/archive/refs/tags/v01_07.tar.gz"

    version("01_10", sha256="fd489b98e1f1fbb5475b6d1628e73d76ce8fa063e224cb78767ad52e9b02cb2f")
    version("01_07", sha256="a85f0a9fcd33a7a82688f000594161efcd765c73c139c54c004a36ae52469662")

    def url_for_version(self, version):
        return f"https://github.com/SBNSoftware/sbndata/archive/refs/tags/v{str(version).replace('.', '_')}.tar.gz"

    def install(self, spec, prefix):
        src = glob.glob(self.stage.source_path)[0]
        install_tree(src, prefix)

    def setup_run_environment(self, env):
        env.set("SBN_DATA_VERSION", "v%s" % self.version.underscored)
        env.prepend_path("FW_SEARCH_PATH", "%s/Calorimetry" % self.prefix)
        env.prepend_path("FW_SEARCH_PATH", "%s/beamData" % self.prefix)
        env.prepend_path("FW_SEARCH_PATH", "%s/triggerDatabase" % self.prefix)
        env.prepend_path("CMAKE_PREFIX_PATH", "%s" % self.prefix)
        env.prepend_path("PKG_CONFIG_PATH", "%s" % self.prefix)
