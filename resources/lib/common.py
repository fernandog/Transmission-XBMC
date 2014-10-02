# -*- coding: utf-8 -*-
# Copyright (c) 2013 Artem Glebov

import sys
import transmissionrpc

__settings__ = sys.modules[ "__main__" ].__settings__

def get_settings():
    params = {
        'address': __settings__.getSetting('rpc_host'),
        'port': __settings__.getSetting('rpc_port'),
        'user': __settings__.getSetting('rpc_user'),
        'password': __settings__.getSetting('rpc_password'),
        'action_on_playback': __settings__.getSetting('action_on_playback'),
        'seconds_playback_finished': __settings__.getSetting('seconds_playback_finished')		
    }
    return params

def get_params():
    params = {
        'address': __settings__.getSetting('rpc_host'),
        'port': __settings__.getSetting('rpc_port'),
        'user': __settings__.getSetting('rpc_user'),
        'password': __settings__.getSetting('rpc_password'),
    }
    return params

def get_rpc_client():
    params = get_params()
    return transmissionrpc.Client(**params)
