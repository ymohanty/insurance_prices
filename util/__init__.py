from pathlib import Path

# ~~~~~~~~~ Data paths ~~~~~~~~~~~~
_PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Directories
RAW_DATA = str (_PROJECT_ROOT / "data/raw/")
INT_DATA = str (_PROJECT_ROOT / "data/intermediate/")
CLEAN_DATA = str( _PROJECT_ROOT / "data/clean/")

# Files
RAW_GMC_DATA = str( RAW_DATA + '/24-0795959_GeisingerMedicalCenter_standardcharges.csv')
RAW_GMC_ZIP = str( RAW_DATA + "/gmc_data.zip" )
MEDICARE_LVL2_PDF = str( RAW_DATA + "/medicare_lvl1_data.pdf")
MEDICARE_LVL1_PDF = str( RAW_DATA + "/medicare_lvl2_data.pdf")
MEDICARE_LAB_PDF = str( RAW_DATA + "/medicare_lab_data.pdf")
INT_GMC_DATA = str (INT_DATA + "/gmc_data.csv")
INT_MEDICARE_LVL2_DATA = str( INT_DATA + "/medicare_lvl2_data.csv")
INT_MEDICARE_LVL1_DATA = str( INT_DATA + "/medicare_lvl1_data.csv")
INT_MEDICARE_LAB_DATA = str( INT_DATA + "/medicare_lab_data.csv")
CLEAN_GMC_DATA = str ( CLEAN_DATA + "/gmc_data.csv")
CLEAN_MEDICARE_DATA = str( CLEAN_DATA + "/medicare_data.csv") 
WORKING_DATA = str( CLEAN_DATA + "/working_data.csv")

# Output paths
OUT_PATH = str( Path(__file__).resolve().parent.parent / 'figures')