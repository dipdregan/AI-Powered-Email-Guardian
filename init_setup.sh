echo[$date] "Starting steup"
echo[$date] "Creating Conda Env and using python version -8.1"
conda create env --prefix python==3.8 -y
echo[$date] "activating env"
conda activate env/
echo[$date] "installing requiremets "
pip install -r requirements.txt



