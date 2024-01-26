import sys
from util.utilities import download

def main(argv=None):
    if argv is None:
        argv = sys.argv
    
    # Prep data
    prep_data(argv[2],argv[3],argv[1])



def prep_data(main_data_source, medicare_data_source, destination):
    
    # Download raw data
    print("Downloading raw data...")
    main_data_dest=destination+"/main_data.csv"
    medicare_data_dest=destination+"/medicare_data.pdf"
    download(main_data_source, main_data_dest)
    download(medicare_data_source, medicare_data_dest)

    

    
    

if __name__ == '__main__':
    main(sys.argv)