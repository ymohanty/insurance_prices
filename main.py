import sys
from util.utilities import download
import util
import tabula
import pandas as pd
import zipfile
import os

def main(argv=None):
    if argv is None:
        argv = sys.argv
    
    # Prep data for cleaning
    #prep_data(argv[1],argv[2:])

    # Clean both GMC and medicare data
    clean_gmc_data()


def prep_data(gmc_data_source, medicare_data_sources):
    """
    Download and prepare raw data from GMC and Medicare sources and save them to the raw /intermediate data directory.
    
    :param gmc_data_source: The source URL for GMC data
    :param medicare_data_sources: The source URLs for Medicare data
    
    :return: None
    """
    
    # Download raw data
    if len(os.listdir(util.RAW_DATA)) < 2:
        print("Downloading raw data...")
        download(gmc_data_source, util.RAW_GMC_ZIP)
        download(medicare_data_sources[0], util.MEDICARE_LVL1_PDF)
        download(medicare_data_sources[1], util.MEDICARE_LVL2_PDF)
        download(medicare_data_sources[2], util.MEDICARE_LAB_PDF)

    # Unzip GMC data
    with zipfile.ZipFile(util.RAW_GMC_ZIP, 'r') as zip_ref:
        zip_ref.extractall(util.RAW_DATA)
    print("Unzipped GMC data.")

    # Remove metadata from GMC data
    print("Removing metadata...")
    with open(util.RAW_GMC_DATA, "r", encoding="windows-1252") as f:
        lines = f.readlines()
    
    with open(util.INT_GMC_DATA, "w") as f:
        f.writelines(lines[4:])

    # Convert medicare PDFs to CSV
    print("Converting PDF to CSV...")
    tabula.convert_into(util.MEDICARE_LVL1_PDF, util.INT_MEDICARE_LVL1_DATA, output_format="csv", pages="all")
    tabula.convert_into(util.MEDICARE_LVL2_PDF, util.INT_MEDICARE_LVL2_DATA, output_format="csv", pages="all")
    tabula.convert_into(util.MEDICARE_LAB_PDF, util.INT_MEDICARE_LAB_DATA, output_format="csv", pages="all")


def clean_gmc_data():
    """
    Clean GMC data by stripping nonstandard symbols, correcting types, turning data wide to long,
    replacing occurrences of ' - ' with '/', splitting out inpatient and outpatient charges,
    and renaming the "CPT/HCPCS" column. Save the cleaned data to a CSV file.
    """
    
    print("Cleaning GMC data...")

    # Strip nonstandard symbols from GMC data
    df = pd.read_csv(util.INT_GMC_DATA)
    df.replace('\$', '', regex=True, inplace=True)
    df.replace(',', '', regex=True, inplace=True)
    
    # Correct types
    numeric_part = df.iloc[:,8:]
    string_part = df.iloc[:,0:8]
    string_part = string_part.astype("string")
    numeric_part = numeric_part.applymap(lambda x: pd.to_numeric(x, errors='coerce'))
    df = pd.concat([string_part,numeric_part],axis=1)

    # Turn GMC data wide to long
    df = df.drop(["Hospital","Charge Code/NDC/Supply ID",
                  "MS-DRG","APR-DRG","Description","Mod","Rev Code", "Gross Charge"],axis=1)
    df = df.melt(id_vars=["CPT/HCPCS"],var_name="insurer_type",value_name="insurer_charge")

    # Replace the first occurrence of ' - ' with '/' if it occurs twice
    for i, row in df.iterrows():
        if row['insurer_type'].count(' - ') == 2:
            first_index = row['insurer_type'].find(' - ')
            df.at[i, 'insurer_type'] = row['insurer_type'][:first_index] + '/' + row['insurer_type'][first_index + 3:]

    # Split out inpatient and outpatient charges
    df[["insurer","type"]] = df["insurer_type"].str.split(' - ',expand=True)
    df = df.drop('insurer_type',axis=1)

    # Filter out "Self Pay" observations from the "insurer" column
    df = df[df["insurer"] != "Self Pay"]

    # Rename column "CPT/HCPCS" to "cpt_hcpcs"
    df.rename(columns={"CPT/HCPCS": "cpt_hcpcs"}, inplace=True)

    # Save cleaned GMC data
    df.to_csv(util.CLEAN_GMC_DATA, index=False)

def clean_medicare_data():
    print("Cleaning Medicare data...")


    


    

    









    

    
    

if __name__ == '__main__':
    main(sys.argv)