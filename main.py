import sys
from util.cleaning import prep_data, clean_gmc_data, clean_medicare_data, combine_data
import pandas as pd


def main(argv):
    if len(argv) == 1:
        print("Usage: python main.py <gmc_data_source> <medicare_data_sources>")
        print("We shall set default paths")
        argv.extend([util.GMC_DATA_SOURCE, util.MEDICARE_LVL1_SOURCE,
                     util.MEDICARE_LVL2_SOURCE, util.MEDICARE_LAB_SOURCE])
         
    
    # Prep data for cleaning
    prep_data(argv[1],argv[2:])

    # Clean both GMC and medicare data
    clean_gmc_data()
    clean_medicare_data()

    # Combine cleaned GMC and medicare data
    combine_data()

    # Analysis
    




    
    
    
    






    


    

    









    

    
    

if __name__ == '__main__':
    main(sys.argv)