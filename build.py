# -*- coding: utf-8 -*-
"""\
SCons build rules
"""

import os

cxx_source_files = []
c_source_files = []
fortran_source_files = []
chost_source_files = []
cslave_source_files = []
cxxhost_source_files = []


def build_object(baseenv,
                 sources,
                 program_inc,
                 program_libs,
                 sources_type='none',
                 prepend_args=None,
                 append_args=None):
    libenv = baseenv.Clone()
    libenv.Prepend(CPPPATH=program_inc)

    if sources_type == 'chost':
        libenv.Replace(OBJSUFFIX='_host.o',
                       CCCOM='$CC_HOST -mhost -mieee -DLABEL_INT$INT_TYPE \
                  -DSCALAR_FLOAT$FLOAT_TYPE -g -O2 $_CPPINCFLAGS \
                  -c -o $TARGET $SOURCES')
    elif sources_type == 'cslave':
        libenv.Replace(
            OBJSUFFIX='_slave.o',
            CCCOM='$CC_SLAVE -mslave -mieee -msimd -DLABEL_INT$INT_TYPE \
            -DSCALAR_FLOAT$FLOAT_TYPE -g -O2 $_CPPINCFLAGS -fgnu89-inline \
            -D_SW_COMPILER_VERSION -c -o $TARGET $SOURCES')
    elif sources_type == 'cxxhost':
        libenv.Replace(CXXCOM='$CXX_HOST -mhost -mieee -DLABEL_INT$INT_TYPE \
            -DSCALAR_FLOAT$FLOAT_TYPE -g -O2 $_CPPINCFLAGS \
            -c -o $TARGET $SOURCES')

    objs = libenv.Object(source=sources)
    return objs


def build_objects(baseenv,
                  c_source=None,
                  cxx_source=None,
                  fortran_source=None,
                  chost_source=None,
                  cslave_source=None,
                  cxxhost_source=None):
    objenv = baseenv.Clone()
    objs = []
    if c_source is None:
        c_source = []
    if cxx_source is None:
        cxx_source = []
    if fortran_source is None:
        fortran_source = []
    if chost_source is None:
        chost_source = []
    if cslave_source is None:
        cslave_source = []
    if cxxhost_source is None:
        cxxhost_source = []
    objs = objs + build_object(objenv,
                               sources=fortran_source,
                               program_inc=objenv['THIRDPARTY_INCS'],
                               program_libs=objenv['THIRDPARTY_LIBS'])

    objs = objs + build_object(objenv,
                               sources=cxx_source,
                               program_inc=objenv['THIRDPARTY_INCS'],
                               program_libs=objenv['THIRDPARTY_LIBS'])

    objs = objs + build_object(objenv,
                               sources=c_source,
                               program_inc=objenv['THIRDPARTY_INCS'],
                               program_libs=objenv['THIRDPARTY_LIBS'])
    if objenv['PLATFORM'] == 'sw':
        if objenv['ATHREAD']:
            objs = objs + build_object(objenv,
                                       sources=chost_source,
                                       program_inc=objenv['THIRDPARTY_INCS'],
                                       program_libs=objenv['THIRDPARTY_LIBS'],
                                       sources_type='chost')

            objs = objs + build_object(objenv,
                                       sources=cslave_source,
                                       program_inc=objenv['THIRDPARTY_INCS'],
                                       program_libs=objenv['THIRDPARTY_LIBS'],
                                       sources_type='cslave')

            objs = objs + build_object(objenv,
                                       sources=cxxhost_source,
                                       program_inc=objenv['THIRDPARTY_INCS'],
                                       program_libs=objenv['THIRDPARTY_LIBS'],
                                       sources_type='cxxhost')
    return objs


def build_lib(baseenv,
              target,
              sources,
              program_inc,
              program_libs,
              prepend_args=None,
              append_args=None):
    """Build a shared library

    Args:
        baseenv (env): program SCons build environment
        target (str): Name of the build target
        sources (list): List of sources for this target
        program_inc (list): List of program include paths
        program_libs (list): List of libraries to be linked

        prepend_args (dict): Set of (key, value) pairs to be prepended
        append_args (dict): Set of (key, value) pairs to be appended
    """
    libenv = baseenv.Clone()
    lib_type = libenv['LIB_TYPE']
    lib_src = libenv['LIB_SRC']
    inc_dirs = [os.path.join(lib_src, d) for d in program_inc]
    libenv.Prepend(CPPPATH=inc_dirs)
    libenv.Append(LIBS=program_libs)
    libenv.Append(LIBPATH=libenv['LIBPATH_COMMON'] + libenv['LIBPATH_LIBS'])

    if lib_type == "shared":
        exe = libenv.SharedLibrary(target=target, source=sources)
    elif lib_type == "static":
        exe = libenv.StaticLibrary(target=target, source=sources)

    install_dir = libenv['LIB_PLATFORM_INSTALL']
    libenv.Alias('install', install_dir)
    libenv.Install(install_dir, exe)

    if prepend_args is not None:
        libenv.Prepend(**prepend_args)
    if append_args is not None:
        libenv.Append(**append_args)

    return libenv


def build_app(baseenv,
              target,
              sources,
              program_inc,
              program_libs,
              prepend_args=None,
              append_args=None,
              linker=None):
    """Build an executable application

    Args:
        baseenv (env): program SCons build environment
        target (str): Name of the build target
        sources (list): List of sources for this target
        program_inc (list): List of program include paths
        program_libs (list): List of libraries to be linked

        prepend_args (dict): Set of (key, value) pairs to be prepended
        append_args (dict): Set of (key, value) pairs to be appended
    """
    appenv = baseenv.Clone()

    lib_src = appenv['LIB_SRC']
    inc_dirs = [os.path.join(lib_src, d) for d in program_inc]
    appenv.Prepend(CPPPATH=inc_dirs)
    appenv.Prepend(F90PATH=inc_dirs)
    appenv.Append(LIBS=program_libs)
    appenv.Append(LIBPATH=appenv['LIBPATH_COMMON'] + appenv['LIBPATH_APPS'])

    exe = appenv.Program(target=target, source=sources)
    install_dir = appenv['BIN_PLATFORM_INSTALL']
    appenv.Alias('install', install_dir)
    appenv.Install(install_dir, exe)

    if prepend_args is not None:
        appenv.Prepend(**prepend_args)
    if append_args is not None:
        appenv.Append(**append_args)

    if linker is not None:
        appenv['LINK'] = linker

    return appenv


def build_lninclude(env):
    """Create lnInclude directories

    Args:
        env (Environment): program SCons build environment
    """

    from SCons.Script import Copy, Mkdir, Dir

    ostype = "windows" if env['PLATFORM'] == "windows" else "posix"
    include_patterns = [".hpp", ".H", ".hxx", ".h", ".hh"]

    inc_env = env.Clone()
    inc_dir = inc_env['PROJECT_INC_DIR']
    Mkdir(inc_dir)
    src_dir = inc_env['LIB_SRC']
    if os.path.exists(inc_dir):
        inc_env.Alias("install", inc_dir)

    for root, dlist, files in os.walk(src_dir):
        if "lnInclude" in dlist:
            dlist.remove("lnInclude")

        dbase = os.path.basename(root)
        if "OSspecific" in dbase:
            for d in dlist:
                if d != ostype:
                    dlist.remove(d)

        for f in files:
            if any(f.endswith(pat) for pat in include_patterns):
                src = os.path.join(root, f)
                dest = os.path.join(inc_dir, f)
                yield inc_env.Install(inc_dir, src)


def add_source_files(source_files, all_source_files):
    for filename in source_files:
        fullDir = os.path.join(os.getcwd(), filename)
        all_source_files.append(fullDir)
