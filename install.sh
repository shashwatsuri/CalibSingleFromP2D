eval "$(conda shell.bash hook)"
conda create --prefix ./env/CalibSingle2DP python=3.9
conda activate ./env/CalibSingle2DP

conda install pytorch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 cpuonly -c pytorch

echo "Installing dependencies"
pip install -r requirements.txt