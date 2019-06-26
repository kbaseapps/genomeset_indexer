# -*- coding: utf-8 -*-
import os
import time
import json
import unittest
from configparser import ConfigParser

from genomeset_indexer.genomeset_indexerImpl import genomeset_indexer
from genomeset_indexer.genomeset_indexerServer import MethodContext
from genomeset_indexer.authclient import KBaseAuth as _KBaseAuth

from installed_clients.WorkspaceClient import Workspace


class genomeset_indexerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = os.environ.get('KB_AUTH_TOKEN', None)
        config_file = os.environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('genomeset_indexer'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'genomeset_indexer',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = Workspace(cls.wsURL)
        cls.serviceImpl = genomeset_indexer(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']
        suffix = int(time.time() * 1000)
        cls.wsName = "test_ContigFilter_" + str(suffix)
        ret = cls.wsClient.create_workspace({'workspace': cls.wsName})  # noqa

    def _check_file_formatting(self, filepath):
        ''''''
        def check_datatypes(d):
            if isinstance(d, dict):
                for key, val in d.items():
                    self.assertTrue(isinstance(key, str))
                    check_datatypes(val)
            elif isinstance(d, list):
                for val in d:
                    check_datatypes(val)
            else:
                self.assertTrue(isinstance(d, str) or isinstance(d, int) or \
                    isinstance(d, float) or d is None or isinstance(d, bool))

        with open(filepath) as fd:
            for line in fd.readlines():
                data = json.loads(line)
                check_datatypes(data['doc'])

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    def test_your_method(self):
        """"""
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        params = {
            'obj_data_path': os.path.join(curr_dir, 'data', "obj_data.json"),
            'ws_info_path': "",
            'obj_data_v1_path': "" 
        }
        ret = self.serviceImpl.run_genomeset_indexer(self.ctx, params)[0]
        self._check_file_formatting(ret['filepath'])
