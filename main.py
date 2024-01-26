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
    #clean_gmc_data()
    #clean_medicare_data()

    # Combine cleaned GMC and medicare data
    combine_data()


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
    print("Removing metadata from GMC data..")
    with open(util.RAW_GMC_DATA, "r", encoding="windows-1252") as f:
        lines = f.readlines()
    
    with open(util.INT_GMC_DATA, "w") as f:
        f.writelines(lines[4:])

    # Convert medicare PDFs to CSV
    print("Converting PDF to CSV...")
    tabula.convert_into(util.MEDICARE_LVL1_PDF, util.INT_MEDICARE_LVL1_DATA, output_format="csv", pages="all")
    tabula.convert_into(util.MEDICARE_LVL2_PDF, util.INT_MEDICARE_LVL2_DATA, output_format="csv", pages="all")
    tabula.convert_into(util.MEDICARE_LAB_PDF, util.INT_MEDICARE_LAB_DATA, output_format="csv", pages="all")

    # Remove metadata from medicare data
    print("Removing metadata from medicare data..")
    with open(util.INT_MEDICARE_LAB_DATA, "r") as f:
        lines = f.readlines()
    
    with open(util.INT_MEDICARE_LAB_DATA, "w") as f:
        f.writelines(lines[3:])


def clean_gmc_data():
    """
    Clean GMC data by stripping nonstandard symbols, correcting types, turning data wide to long,
    replacing occurrences of ' - ' with '/', splitting out inpatient and outpatient charges,
    and renaming the "CPT/HCPCS" column. Save the cleaned data to a CSV file.
    """
    
    print("Cleaning GMC data...")
    df = pd.read_csv(util.INT_GMC_DATA)

    # Strip nonstandard symbols from GMC data
    df = df.replace({'\$': '', ',': ''}, regex=True)
    
    # Correct types
    string_columns = df.iloc[:, :8].astype(str)
    numeric_columns = df.iloc[:, 8:].apply(pd.to_numeric, errors='coerce')
    df = pd.concat([string_columns, numeric_columns], axis=1)

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
    df = df["Maximum" not in df["insurer"]]

    # Rename column "CPT/HCPCS" to "cpt_hcpcs"
    df.rename(columns={"CPT/HCPCS": "cpt_hcpcs"}, inplace=True)

    # Save cleaned GMC data
    df.to_csv(util.CLEAN_GMC_DATA, index=False)

def clean_medicare_data():
    """
    Clean and standardize Medicare dataframes, concatenate them, fix variable types, and save the cleaned data to a CSV file.
    """
    
    print("Cleaning Medicare data...")

    # Load medicare dataframes
    lvl1 = pd.read_csv(util.INT_MEDICARE_LVL1_DATA)
    lvl2 = pd.read_csv(util.INT_MEDICARE_LVL2_DATA)
    lab = pd.read_csv(util.INT_MEDICARE_LAB_DATA)

    # Standardize variables names in medicare data
    lvl1.columns = lvl1.columns.str.replace('\W', '', regex=True)
    lvl1.columns = lvl1.columns.str.replace('\d', '', regex=True)
    lvl2.columns = lvl2.columns.str.replace('\W', '', regex=True)
    lab.columns = lab.columns.str.replace('\W', '', regex=True)
    lvl1 = lvl1.drop(['RankbyCharges'],axis=1)
    lvl2 = lvl2.drop(['RankbyCharges'],axis=1)
    lab = lab.drop(['RankedbyCharges'],axis=1)
    lvl1.rename(columns={"HCPCSCode": "cpt_hcpcs",
                         "QCYAllowedServicesQ":"allowed_services", 
                         "AllowedCharges":"allowed_charges"},inplace=True)
    lvl2.rename(columns={"HCPCSCode":"cpt_hcpcs","AllowedCharges":"allowed_charges",
                "AllowedServices":"allowed_services"},inplace=True)
    lab.rename(columns={"HCPCSCode":"cpt_hcpcs",
                        "AllowedCharges":"allowed_charges",
                        "AllowedServices":"allowed_services",
                        "Desciption":"description"},inplace=True)
    
    # Concatenate vertically
    df = pd.concat([lvl1,lvl2,lab],axis=0)

    # Fix variable types
    df = df.replace(',', '', regex=True)
    df['allowed_services'] = pd.to_numeric(df['allowed_services'], errors='coerce')
    df['allowed_charges'] = pd.to_numeric(df['allowed_charges'], errors='coerce')
    df['cpt_hcpcs'] = df['cpt_hcpcs'].astype(str)
    print(df)

    # Compute shares spent on each service
    total_services = df['allowed_services'].sum()
    total_charges = df['allowed_charges'].sum()
    df['services_share'] = (df['allowed_services'] / total_services) 
    df['charges_share'] = (df['allowed_charges'] / total_charges) 

    # Save cleaned medicare data
    df.to_csv(util.CLEAN_MEDICARE_DATA, index=False)

def combine_data():
    """
    Combine cleaned GMC and Medicare data and save it to a CSV file.
    """
    
    print("Combining cleaned GMC and Medicare data...")

    # Load cleaned GMC and Medicare data
    gmc = pd.read_csv(util.CLEAN_GMC_DATA)
    medicare = pd.read_csv(util.CLEAN_MEDICARE_DATA)

    # Merge on CPT/HCPCS codes
    df = pd.merge(gmc, medicare, on='cpt_hcpcs', how='left')
    
    # Filter out rows with "minimum negotiated charge" and "maximum negotiated charge" under "insurer"
    df = df[~df["insurer"].isin(["Minimum Negotiated Charge", "Maximum Negotiated Charge"])]
    print(df['insurer'].unique())

    # Save combined data
    df.to_csv(util.WORKING_DATA, index=False)
    
    
    
    






    


    

    









    

    
    

if __name__ == '__main__':
    main(sys.argv)