import sys
from util.cleaning import prep_data, clean_gmc_data, clean_medicare_data, combine_data
import pandas as pd
import util
import util.plotting as plotting

def main(argv):
    if len(argv) == 1:
        print("Usage: python main.py <gmc_data_source> <medicare_data_sources>")
        print("We shall set default paths")
        argv.extend([util.GMC_DATA_SOURCE, util.MEDICARE_LVL1_SOURCE,
                     util.MEDICARE_LVL2_SOURCE, util.MEDICARE_LAB_SOURCE])
         
    # ==== DATA PREPARATION ===
    # Prep data for cleaning
    prep_data(argv[1],argv[2:])

    # Clean both GMC and medicare data
    clean_gmc_data()
    clean_medicare_data()

    # Combine cleaned GMC and medicare data
    combine_data()

    # ==== ANALYSIS =====

    # Load working data
    df = pd.read_csv(util.WORKING_DATA)

    # Save plots
    plotting.plot_bar(df,filename=util.OUT_PATH + "/barplot_ranked_charges_unweighted.pdf",weight=None, disagg=False)
    plotting.plot_bar(df,filename=util.OUT_PATH + "/barplot_ranked_charges_disagg_unweighted.pdf",weight=None, disagg=True)
    plotting.plot_bar(df,filename=util.OUT_PATH + "/barplot_ranked_charges_weighted.pdf",weight='charges_share', disagg=False)
    plotting.plot_bar(df,filename=util.OUT_PATH + "/barplot_ranked_charges_disagg_weighted.pdf",weight='charges_share', disagg=True)
    
    
if __name__ == '__main__':
    main(sys.argv)