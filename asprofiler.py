#!/usr/bin/env python3

import analyse
import download
import argparse
import lib

def main():
    parser = argparse.ArgumentParser(description="A tool to profile Autonomous Systems based on publicly available datasets")
    parser.add_argument('-if', '--input_file', type=str, help='csv file containing the total list of ASNs (e.g. 1,2,3,4)', required=True)
    parser.add_argument('-of', '--output_file', type=str, help='.json output filename containing all the available data for the profiled ASes', required=True)
    args = parser.parse_args()

    # Step 1: Import all the ASes based on the given input file
    asns = lib.import_csv(args.input_file)

    # Step 2: Download all the appropriate datasets from the puplicly available databases
    download_ = download.Download()
    
    # Step 3: Sort and categorize downloaded datasets
    analyse_ = analyse.Analyse(
                download_.ixp_filename,
                download_.as_to_ixp_filename, 
                download_.peeringdb_filename, 
                download_.as_relations_v4_filename, 
                download_.as_relations_v6_filename, 
                download_.as_cust_cone_filename,
                asns)
    
    # Step 4: Profile the ASes and export the available data
    analyse_.export_data(args.output_file)

if __name__ == '__main__':
    main()
