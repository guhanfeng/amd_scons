# -*- coding: utf-8 -*-
"""\
program Build-time Variables
----------------------------

This module defines the SCons variables used to control the compilation process
for program.

"""

import os
import platform
import getpass
from SCons.Environment import Environment
from SCons.Variables import (Variables, EnumVariable, PathVariable,
                             BoolVariable)
from SCons.Script import ARGUMENTS


def ostype():
    """Return the operating system type"""

    if os.name == 'nt':
        return 'windows'
    else:
        return os.uname()[0].lower()


program_vars = Variables('site_scons/build_config.py', ARGUMENTS)
program_vars.AddVariables(
    # Project specific variables
    EnumVariable('PLATFORM',
                 'build platforms',
                 ostype(),
                 allowed_values=('windows', 'linux', 'sw')),
    EnumVariable('BUILD_TYPE',
                 'Type of build',
                 'Opt',
                 allowed_values=('Opt', 'Debug', 'Prof')),
    EnumVariable('BUILD_ARCH',
                 'Build architecture',
                 '64',
                 allowed_values=('64', '32')),
    EnumVariable('PRECISION',
                 'Single/Double precision',
                 'DP',
                 allowed_values=('DP', 'SP')),
    EnumVariable('INT_TYPE', 'Integer size', '32',
                 allowed_values=('32', '64')),
    EnumVariable('FLOAT_TYPE', 'Float size', '64',
                 allowed_values=('32', '64')),
    BoolVariable('OMP', 'Use OpenMP multi-threading', False),
    EnumVariable('LIB_TYPE',
                 'library building type',
                 'static',
                 allowed_values=('shared', 'static', 'object')),
    BoolVariable('VERBOSE', 'Print verbosely when compiling', False),
)

ostype = Environment(variables=program_vars)['PLATFORM']
print('PLATFORM: ', ostype)

if ostype == "windows":
    program_vars.AddVariables(
        ('CC', 'C compiler', 'gcc'),
        ('CXX', 'C++ compiler', 'g++'),
        ('F90', 'fortran90 compiler', 'gfortran'),
        ('CXX_LINKER', 'C++ linker', 'g++'),
        ('F_LINKER', 'fortran linker', 'gfortran'),
        ('MPI_LIB_NAME', 'MPI library name', 'mpi'),
        PathVariable('MPI_INC_PATH', 'Path to MPI headers',
                     'C:\Program Files\MPICH2\include',
                     PathVariable.PathIsDir),
        PathVariable('MPI_LIB_PATH', 'Path to MPI libraries',
                     'C:\Program Files\MPICH2\lib', PathVariable.PathIsDir),
    )
elif ostype == "linux":
    program_vars.AddVariables(
        ('CC', 'C compiler', 'gcc'),
        ('CXX', 'C++ compiler', 'g++'),
        ('F90', 'fortran90 compiler', 'gfortran'),
        ('CXX_LINKER', 'C++ linker', 'mpiicxx'),
        ('F_LINKER', 'fortran linker', 'mpiif90'),
        ('MPI_LIB_NAME', 'MPI library name', 'mpi'),
        PathVariable('MPI_INC_PATH', 'Path to MPI headers',
                     '/usr/sw-cluster/mpi2/include', PathVariable.PathIsDir),
        PathVariable('MPI_LIB_PATH', 'Path to MPI libraries',
                     '/usr/sw-cluster/mpi2/lib', PathVariable.PathIsDir),
    )
elif ostype == "sw":
    program_vars.AddVariables(
        ('CC_HOST', 'c compiler on host', 'sw5gcc'),
        ('CC_SLAVE', 'c compiler on slave', 'sw5gcc'),
        ('CXX_HOST', 'cxx compiler on host', 'sw5g++'),
        ('CC', 'C compiler', 'sw5gcc'),
        ('CXX', 'C++ compiler', 'sw5g++'),
        ('F90', 'fortran90 compiler', 'sw5gfortran'),
        ('CXX_LINKER', 'C++ linker', 'mpicxx'),
        ('F_LINKER', 'fortran linker', 'mpif90'),
        ('MPI_LIB_NAME', 'MPI library name', 'mpi'),
        PathVariable('MPI_INC_PATH', 'Path to MPI headers',
                     '/usr/sw-mpp/swcc/new_compiler_710/mpi_install/include',
                     PathVariable.PathIsDir),
        PathVariable('MPI_LIB_PATH', 'Path to MPI libraries',
                     '/usr/sw-mpp/swcc/new_compiler_710/mpi_install/lib',
                     PathVariable.PathIsDir),
        BoolVariable('ATHREAD', 'Use Shenwei multi-threading', False),
    )
else:
    print('Unknown ostype')


def init_dependent_vars(env, prj_dir):
    """Initialize dependent variables based on user configuration"""
    from SCons.Script import Mkdir
    ostype = env['PLATFORM']
    BUILD_OPTION = (ostype + env['CXX'] + 'Int' + env['INT_TYPE'] + 'Float' +
                    env['FLOAT_TYPE'] + env['BUILD_TYPE'])
    PLATFORM_INSTALL = os.path.join(prj_dir, 'install', BUILD_OPTION)
    BIN_PLATFORM_INSTALL = os.path.join(PLATFORM_INSTALL, 'bin')
    LIB_PLATFORM_INSTALL = os.path.join(PLATFORM_INSTALL, 'lib')
    INC_PLATFORM_INSTALL = os.path.join(PLATFORM_INSTALL, 'include')
    LIB_SRC = os.path.join(prj_dir, 'src')
    # PROJECT_INC_DIR = os.path.join(prj_dir, 'build', 'lnInclude')
    PROJECT_INC_DIR = INC_PLATFORM_INSTALL
    EXTERNAL_DIR = os.path.join(prj_dir, 'external')
    EXTERNAL_WINDOWS_DIR = os.path.join(EXTERNAL_DIR, 'windows')
    env.Append(BUILD_OPTION=BUILD_OPTION,
               BIN_PLATFORM_INSTALL=BIN_PLATFORM_INSTALL,
               LIB_PLATFORM_INSTALL=LIB_PLATFORM_INSTALL,
               INC_PLATFORM_INSTALL=INC_PLATFORM_INSTALL,
               LIB_SRC=LIB_SRC,
               PROJECT_INC_DIR=PROJECT_INC_DIR,
               EXTERNAL_DIR=EXTERNAL_DIR,
               EXTERNAL_WINDOWS_DIR=EXTERNAL_WINDOWS_DIR,
               THIRDPARTY_INCS=[],
               THIRDPARTY_LIB_PATH=[],
               THIRDPARTY_LIBS=[])
