# Create environment
conda env create -n depth_anything_metric --file ../environment.yml
source activate depth_anything_metric
pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cu118

#Download necessary files(model)
mkdir ../checkpoints
wget -P ../checkpoints https://huggingface.co/spaces/LiheYoung/Depth-Anything/resolve/main/checkpoints/depth_anything_vitl14.pth

#Download necessary files(dataset)
mkdir -p ../data/nyu
pip install gdown
apt-get install unzip
cd ../data/nyu
gdown --fuzzy https://drive.google.com/file/d/1AysroWpfISmm-yRFGBgFTrLy6FjQwvwP/view?usp=sharing
unzip sync.zip

#Prevent error message
apt-get update && apt-get install ffmpeg libsm6 libxext6  -y