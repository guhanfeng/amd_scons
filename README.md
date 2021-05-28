# AMD_SCONS编译脚本

## 0 简介

本编译脚本基于开源的SCons库，采用Python语言，支持跨平台编译，包括Linux、神威、windows mingw。

## 1 文件说明

**build.py**：主要提供编译库和可执行文件的函数

* **build_object**：编译单个文件，返回.o文件，内部函数，一般不需要调用
* **build_objects**：批量编译文件，返回.o的列表
* **build_lib**：编译成lib文件
* **build_app**：编译成可执行文件
* **build_lninclude**：寻找编译目录下的头文件，集中至install下的include文件夹
* **add_source_files**：将文件添加至对应列表，不同的列表有对应的默认编译器编译，可选的列表有
  * cxx_source_files：c++文件列表
  * c_source_files：c文件列表
  * fortran_source_files：fortran文件列表
  * chost_source_files：c主核文件列表（只针对神威）
  * cslave_source_files：c从核文件列表（只针对神威）
  * cxxhost_source_files：c++主核文件列表（只针对神威）

**compiler.py**：编译器相关编译选项，一般为默认配置

* **BUILD_TYPE**：Opt、Debug、Prof
  * Opt：-O3 -g
  * Debug：-O0 -ggdb3 -DDEBUG -DTIMERS
  * Prof：-O2 -pg

* **general_flag**: -fPIC -rdynamic

* **warning_flags**（暂时注释）: -Wall -Wextra

**variables.py**：根据环境的默认编译器配置和编译路径设置
* **默认编译器配置**
  * **Linux x86**：默认使用 module load x86/gcc/7.3
    * c编译器：gcc
    * c++编译器：g++
    * fortran编译器：gfortran
    * c++链接器：mpiicxx
    * fortran链接器：mpiif90
    * mpi路径：/usr/sw-cluster/mpi2
  * **神威**：默认使用 module load sw/compiler/gcc710
    * c主核、从核编译器：sw5gcc
    * c++主核、从核编译器：sw5g++
    * fortran编译器：sw5gfortran
    * c++链接器：mpicxx
    * fortran链接器：mpif90
    * mpi路径：/usr/sw-mpp/swcc/new_compiler_710/mpi_install
  * **windows mingw**
    * c编译器：gcc
    * c++编译器: g++
    * fortran编译器: gfortran
    * c++链接器：g++
    * fortran链接器：gfortran
    * mpi路径：C:\Program Files\MPICH2

* **默认编译和安装路径**
  * **默认编译路径**：程序将在SConsStruct所在目录创建build文件夹，在build文件夹下创建“系统类型+c++编译器+Int类型+Float类型+编译选项”子文件夹，做到不同编译环境和选项的隔离，如"*build/linuxg++Int32Float64Opt*"
  * **默认安装路径**：程序将在SConsStruct所在目录创建install文件夹，在install文件夹下创建根据编译环境和选项设置的文件夹，命名规则同build文件下的编译文件夹，在此文件下，根据程序的编译过程分别创建include、lib和bin文件夹，如 "*install/linuxg++Int32Float64Opt/lib*"

**simple_prints.py**：简化输出设置，彩色显示，默认为简化输出，可以在编译时类似cmake方式，使用 "*scons VERBOSE=1*" 获得详细输出结果

## 2 简单使用示例

* amd_scons的公共脚本目录在 "*/home/export/online3/amd_share/guhf/amd_scons*"，使用时将其添加到python的系统环境变量或在SConstruct中引入 "*sys.path.append('/home/export/online3/amd_share/guhf/amd_scons')*"
* 一般模式：需要在程序下添加对应文件夹和文件，如
  * 程序主目录： site/build_config.py, SConstruct，编译启动目录，链接src和test下的SConscript
  * src目录： SConscript，编译lib，链接src子目录下的SConscript
    * src子目录 SConscript，编译文件，一般为最底层
  * test目录：SConscript，编译可执行文件

下面分别简单说明
* 程序主目录：创建site_scons文件夹，添加build_config.py文件，设置一些常用设置，如

```python
PLATFORM = 'sw'
INT_TYPE = '32'
FLOAT_TYPE = '64'
# LIB_TYPE = 'static'

ATHREAD = 'True'
VERBOSE = 'False'

# CXX = 'swg++453'
# F90 = 'mpif90'

# CXX_LINKER = 'swld453'
# F_LINKER = 'swld453-fort'
# MPI_INC_PATH = 'C:\Program Files\MPICH2\include'
# MPI_LIB_PATH = 'C:\Program Files\MPICH2\lib'
```
* 程序主目录：创建SConstruct文件，如

```python
import os
import sys
### 添加scons公共配置
sys.path.append('/home/export/online3/amd_share/guhf/amd_scons')
from variables import program_vars, init_dependent_vars
from compiler import update_compiler_settings
from simple_prints import simple_prints

### Initialize toolsets based on operating system
ostype = Environment(variables=program_vars)['PLATFORM']
tools = ['default']
if ostype == 'windows':
    tools += ['mingw']

### Base SCons environment
env = Environment(variables=program_vars, tools=tools, ENV=os.environ)
# env.SomeTool(targets, sources)
Help(program_vars.GenerateHelpText(env))
current_dir = os.getcwd()
init_dependent_vars(env, current_dir)
update_compiler_settings(env)

### Isolate build environments based on build options
build_dir = os.path.join(Dir("#").abspath, "build", env['BUILD_OPTION'])

program_src = ['src', 'test'] ### 此处添加需要编译的文件夹

for d in program_src:
    SConscript('%s/SConscript' % d,
               exports=['env'],
               src_dir=Dir("#").srcnode().abspath,
               variant_dir=build_dir)

### Remove buid directory when cleaning
Clean(".", build_dir)
```

* 根据前述设置，在src文件夹下创建SConscript文件，如

```python
import os
from build import build_lninclude, build_lib, cxx_source_files,\ 
chost_source_files, cslave_source_files, cxxhost_source_files, \ 
fortran_source_files, build_objects

Import('env')

target = 'utilities' ##lib名

subdirs = Split("""
    common
    rcm
    swacc
""")

src_include = list(build_lninclude(env))

for d in subdirs:
    SConscript(os.path.join(d, 'SConscript'), exports=['env', 'src_include'])

objs_all = []

objs_all = build_objects(env,
                         cxx_source=cxx_source_files,
                         fortran_source=fortran_source_files,
                         chost_source=chost_source_files,
                         cslave_source=cslave_source_files,
                         cxxhost_source=cxxhost_source_files)

build_lib(env,
          target=target,
          sources=objs_all,
          program_inc=env['THIRDPARTY_INCS'],
          program_libs=env['THIRDPARTY_LIBS'])
```

* 进入src下任一文件夹，添加要编译的文件，如

```python
from build import add_source_files, cxx_source_files

cxxfiles = ['utilityMpiWrapper.cpp',
            'communicationManager/utilityCommunicationManager.cpp',
            'communicator/utilityCommunicator.cpp']

add_source_files(cxxfiles, cxx_source_files)
```

* test目录：编译可执行程序，在编译目录下创建SConscript文件，如

```python
from build import build_app
Import('env')

env.Append(THIRDPARTY_LIBS='unap')

### 添加链接库的路径
env.Append(LIBPATH=env['THIRDPARTY_LIB_PATH'])

env.Append(THIRDPARTY_LIBS='utilities')
env.Append(THIRDPARTY_LIBS='stdc++')

### 添加你要链接的库
if env['PLATFORM'] == 'sw':
    env.Append(THIRDPARTY_LIBS='unat')
    env.Append(THIRDPARTY_LIBS='swArrays')
    env.Append(THIRDPARTY_LIBS='metis')
    env.Append(THIRDPARTY_LIBS='swlu')

if env['PLATFORM'] == 'windows':
    env.Append(THIRDPARTY_LIBS='mpi')
    env.Append(THIRDPARTY_LIBS='fmpich2g')

### 编译可执行文件
appfile = 'test_amg'
build_app(env,
          target=appfile,
          sources=appfile + '.cpp',
          program_inc=env['THIRDPARTY_INCS'],
          program_libs=env['THIRDPARTY_LIBS'],
          linker=env['CXX_LINKER'])
```