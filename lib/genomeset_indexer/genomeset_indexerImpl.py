# -*- coding: utf-8 -*-
#BEGIN_HEADER
import os
import json
import logging

from installed_clients.KBaseReportClient import KBaseReport
#END_HEADER


class genomeset_indexer:
    '''
    Module Name:
    genomeset_indexer

    Module Description:
    A KBase module: genomeset_indexer
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = ""
    GIT_COMMIT_HASH = ""

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        #END_CONSTRUCTOR
        pass


    def run_genomeset_indexer(self, ctx, params):
        """
        This example function accepts any number of parameters and returns results in a KBaseReport
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_genomeset_indexer
        with open(params['obj_data_path']) as fd:
            obj_data = json.load(fd)

        data = obj_data['data']
        doc = {
            'genomes': [{'label': d['label'], 'genome_ref': d['ref']} for d in data['items']],
            'description': data['description']
        }
        index = {
            'doc': doc
        }

        output_path = os.path.join(self.shared_folder, 'output.json')
        with open(output_path, 'w') as fd:
            fd.write(json.dumps(index))

        output = {'filepath': output_path}
        #END run_genomeset_indexer

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_genomeset_indexer return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
