'''
@Author: guhf
@Email: hanfenggu@gmail.com
@Date: 2020-07-30 16:54:06
@Brief:
'''
#!python
import sys
import os


def simple_prints(env):
    colors = {}
    colors['cyan'] = '\033[96m'
    colors['purple'] = '\033[95m'
    colors['blue'] = '\033[94m'
    colors['green'] = '\033[92m'
    colors['yellow'] = '\033[93m'
    colors['red'] = '\033[91m'
    colors['end'] = '\033[0m'

    #If the output is not a terminal, remove the colors
    if not sys.stdout.isatty():
        for key, value in colors.iteritems():
            colors[key] = ''

    compile_source_message = '%sCompiling %s==> %s$SOURCE%s' % \
      (colors['blue'], colors['purple'], colors['yellow'], colors['end'])

    compile_shared_source_message = '%sCompiling shared %s==> %s$SOURCE%s' % \
      (colors['blue'], colors['purple'], colors['yellow'], colors['end'])

    link_program_message = '%sLinking Program %s==> %s$TARGET%s' % \
      (colors['green'], colors['purple'], colors['yellow'], colors['end'])

    link_library_message = '%sLinking Static Library %s==> %s$TARGET%s' % \
      (colors['green'], colors['purple'], colors['yellow'], colors['end'])

    ranlib_library_message = '%sRanlib Library %s==> %s$TARGET%s' % \
      (colors['green'], colors['purple'], colors['yellow'], colors['end'])

    link_shared_library_message = '%sLinking Shared Library %s==> %s$TARGET%s' % \
      (colors['green'], colors['purple'], colors['yellow'], colors['end'])

    java_library_message = '%sCreating Java Archive %s==> %s$TARGET%s' % \
      (colors['red'], colors['purple'], colors['yellow'], colors['end'])

    install_message = '%sInstall file %s==> %s$SOURCE%s' % \
      (colors['blue'], colors['purple'], colors['yellow'], colors['end'])

    env.Append(CXXCOMSTR=compile_source_message,
               CCCOMSTR=compile_source_message,
               F90COMSTR=compile_source_message,
               SHCCCOMSTR=compile_shared_source_message,
               SHCXXCOMSTR=compile_shared_source_message,
               SHF90COMSTR=compile_shared_source_message,
               ARCOMSTR=link_library_message,
               RANLIBCOMSTR=ranlib_library_message,
               SHLINKCOMSTR=link_shared_library_message,
               LINKCOMSTR=link_program_message,
               JARCOMSTR=java_library_message,
               JAVACCOMSTR=compile_source_message,
               INSTALLSTR=install_message)
