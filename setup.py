#!/usr/bin/env python
# MolMod is a collection of molecular modelling tools for python.
# Copyright (C) 2007 - 2008 Toon Verstraelen <Toon.Verstraelen@UGent.be>
#
# This file is part of MolMod.
#
# MolMod is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# MolMod is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
#
# --

if __name__ == "__main__":
    import glob
    from distutils.core import setup

    setup(
        name='MolMod',
        version='0.003',
        description='MolMod is a collection of molecular modelling tools for python.',
        author='Toon Verstraelen',
        author_email='Toon.Verstraelen@UGent.be',
        url='http://molmod.ugent.be/code/',
        package_dir = {'molmod': 'lib/molmod'},
        packages=[
            'molmod',
            'molmod.data',
            'molmod.io',
            'molmod.io.gaussian03',
            'molmod.io.mpqc',
        ],
        data_files=[
            ('share/molmod', glob.glob('share/*.csv') + [
                "share/mass.mas03", "share/nubtab03.asc",
            ]),
        ],
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Console',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python',
            'Topic :: Science/Engineering :: Molecular Science'
        ],
    )




