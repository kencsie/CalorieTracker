# Create environment
conda env create -n depth_anything_metric --file ../environment.yml
source activate depth_anything_metric
pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cu118

#Prevent error message
apt-get update && apt-get install ffmpeg libsm6 libxext6  -y