# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------

from spack.package import *


class SbnMlCafmaker(CMakePackage):
    """The sbn_ml_cafmaker package provides code for merging the ML 
       reconstruction outputs into existing CAF files (enforcing event-by-event 
       matching) and for producing standalone CAF files with only ML 
       reconstruction outputs."""

    git = "https://github.com/justinjmueller/sbn_ml_cafmaker.git"

    version("v1_0_0", branch="main")

    depends_on("hdf5+cxx")
    depends_on("sbnanaobj")

    def cmake_args(self):
        return [
            self.define("HDF5_INSTALL", self.spec['hdf5'].prefix),
        ]

    def install(self, spec, prefix):
        install_tree(self.stage.source_path, prefix)
