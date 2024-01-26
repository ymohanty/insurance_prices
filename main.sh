#!/bin/sh
# Main shell file
# Please run this 

###################################### PROJECT LEVEL GLOBALS ################################################

# Paths
project_root="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Verify directory structure
if [ ! -d "${project_root}/data" ]; then
    echo "Creating data folder"
    mkdir "${project_root}/data"
fi

if [ ! -d "${project_root}/figures" ]; then
    echo "Adding figures folder"
    sleep 1
    mkdir "${project_root}/figures"
fi

# Check/create conda Python environment
if [ -x "$(command -v conda)" ]; then
    if [ -d "./venv" ]; then
        echo "\n Activating conda virtual environment...\n"
        source activate ./venv
    else
        echo "Generating conda virtual environment...\n"
        conda-env create --prefix venv --file=environment.yml 

        echo "\n Activating conda virtual environment...\n"
        source activate ./venv
    fi
else
    echo "Error: please install conda version >= 4.12.0 !"
    exit 1
fi

###################################### EXECUTE ################################################

# Prepare args
medicare="https://www.cms.gov/files/document/cy-2021-top-200-level-ii-hcpcs-codes-ranked-charges.pdf"
data="https://www.geisinger.org/-/media/OneGeisinger/pdfs/ghs/patient-care/patients-and-visitors/billing-and-insurance/hosp-charges-csv/24-0795959_GeisingerMedicalCenter_standardcharges.zip?sc_lang=en&hash=072D5C5FAF045902CB9B58E93EB519EA"

# Run main python file
python "${project_root}/main.py" "${project_root}/data" "${data}" "${medicare}"