/*
A KBase module: genomeset_indexer
*/

module genomeset_indexer {
    typedef structure {
        string filepath;
    } ReportResults;

    typedef structure {
    	string obj_data_path;
    	string ws_info_path;
    	string obj_data_v1_path;
    } inputParams;

    /*
        This example function accepts any number of parameters and returns results in a KBaseReport
    */
    funcdef run_genomeset_indexer(inputParams params) returns (ReportResults output) authentication required;

};
