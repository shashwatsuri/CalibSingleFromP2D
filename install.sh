eval "$(conda shell.bash hook)"
echo "Creating conda environment CalibSingleFromP2D"
conda env create --name envname --file=environments.yml
echo "Activating coda env CalibSingleFromP2D"
conda activate CalibSingleFromP2D