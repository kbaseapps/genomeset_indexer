/*
A KBase module: genomeset_indexer
*/

module genomeset_indexer {
    typedef structure {
        string report_name;
        string report_ref;
    } ReportResults;

    /*
        This example function accepts any number of parameters and returns results in a KBaseReport
    */
    funcdef run_genomeset_indexer(mapping<string,UnspecifiedObject> params) returns (ReportResults output) authentication required;

};
