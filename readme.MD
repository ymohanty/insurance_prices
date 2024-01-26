# Ranking insurers at the GMC

## Software dependencies 
Note that you need `conda` with version at least `4.12.0`. You can check the version of `conda` you have by typing
```
conda -V
```
on your favourite shell. I also recommend you have `bash` or `zsh` installed. If you are on a Linux or Mac system, these are the default shells. If you are on Windows, you can use a Linux subsystem without a virtual machine. You can learn more about this [here](https://learn.microsoft.com/en-us/windows/wsl/install).

## Cloning the repository
First, you need to clone the project repository into the local directory of your choice.

```
git clone https://github.com/ymohanty/insurance_prices.git
```

## Running the project through main shell file (recommended)
To run the project entire project in one-step, you should `cd` into the directly you just cloned and run
```
./main.sh
```
If you find issues with permissions, you may need to change the file permissions as follows
```
chmod 777 main.sh
```
and then run the shell file with the command specified earlier.

## Running the project manually
If you are unable to use bash/zsh, you can set up the data folder and conda environment manually.

To create the conda environment, type
```
conda-env create --prefix venv --file=environment.yml 
```
which should generate a folder called `venv` which contains all the dependencies for the project.

You would then to create the data folder manually, with three subfolders. After you are done, the project directory should look this.

```
├── data
│   ├── clean
│   ├── intermediate
│   └── raw
├── environment.yml
├── figures
├── main.py
├── main.sh
├── output.tex
├── readme.MD
├── util
│   ├── __init__.py
│   ├── cleaning.py
│   ├── plotting.py
│   └── utilities.py
└── venv
```

To activate the conda environment, run
```
conda activate ./venv
```

Finally, run the main Python file
```
python main.py
```
You should compile the output file output.tex manually using pdflatex to view the write-up.
