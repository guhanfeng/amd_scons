def add_thirdparties(env):

    dev1_home = '/home/export/online3/amd_dev1'
    amd_share = '/home/export/online3/amd_share'
    utility_home = dev1_home + '/guhf/test/scons/utilities/install/' + env['BUILD_OPTION']
    env.Append(THIRDPARTY_INCS=utility_home + '/include')
    env.Append(THIRDPARTY_LIB_PATH=utility_home + '/lib')
    # env.Append(THIRDPARTY_LIBS = 'utilities')

    if env['PLATFORM'] == 'sw':
        if env['ATHREAD']:
            unat_home = dev1_home + '/guhf/test/scons/unat/install/' + env['BUILD_OPTION']
            env.Append(THIRDPARTY_INCS=unat_home + '/include')
            env.Append(THIRDPARTY_LIB_PATH=unat_home + '/lib')

            swArrays_home = dev1_home + '/guhf/test/scons/swArrays/install/' + env['BUILD_OPTION']
            env.Append(THIRDPARTY_INCS=swArrays_home + '/include')
            env.Append(THIRDPARTY_LIB_PATH=swArrays_home + '/lib')

            metis_home = amd_share + '/guhf/ParMETIS/sw/gcc710Int' + env[
                'INT_TYPE'] + 'Float' + env['FLOAT_TYPE']
            env.Append(THIRDPARTY_INCS=metis_home + '/include')
            env.Append(THIRDPARTY_LIB_PATH=metis_home + '/lib')

            swlu_home = amd_share + '/guhf/swlu/gcc710'
            env.Append(THIRDPARTY_INCS=swlu_home + '/include')
            env.Append(THIRDPARTY_LIB_PATH=swlu_home + '/lib')
            # nothing

    # if env['PLATFORM'] == 'linux':
    ## nothing


def add_thirdparties_include_dir(env, dir):

    env.Append(THIRDPARTY_INCS=dir)

def add_thirdparties_lib_dir(env, dir):

    env.Append(THIRDPARTY_LIB_PATH=dir)