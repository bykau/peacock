# Video Proccesing
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"br
brew tap homebrew/science
brew install opencv

# Poisson Experiment
The folder poisson contains the R code to re-run the poisson experiment.

munging.R prepare the data to Prof. Pearson's format.
main.R runs the experiment code. 

The original csv files are data/Frontal.csv, data/Back.csv and data/Female.csv. Note, that Female.csv has a renamed column TotalFemaleImageFrames (to be compatible with other columns of that kind).

The data/input folder consists of the data files in the format suitable for Prof. Pearson MCMC code.

The data/output folder contains the obtained quantile files.

All file names are in the format experiment type + '_' + directed + '_' + eye.

The following experiments are not run because they contain almost all zeros:
('Back NonDirected Both', 'Back NonDirected R', 'Female NonDirected Both', 'Female NonDirected R', 'Female NonDirected L'
