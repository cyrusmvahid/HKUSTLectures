# Note
***in order to download new material every session run the following***
```
git submodule update --init --recursive
```
# Environmnet set up
To install Conda please refer to [this link](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)
```
 conda create -n HUB python=3.6 anaconda
 source activate HUB
 pip install numpy mxnet jupyter seaborn matplotlib pandas scipy gluoncv gluonnlp scikit-learn
 #test your environment
 which python
 # shoud result in <your conda path>//envs/HUB/bin/python
 python --version
 #Python 3.6.8 :: Anaconda, Inc.
 #To leave the environment
 conda deactivate
 ```
 
 To get this repository, please run:
 git clone --recurse-submodules https://github.com/cyrusmvahid/HKUSTLectures.git
 
# HKUSTLectures
- [slides for day 1 introduction to deep learning lecture](https://cyrusmv-toshare.s3.amazonaws.com/AIM418.pptx?AWSAccessKeyId=AKIAIYUU6IVJLMR5GNQA&Expires=1556542979&Signature=nN7iuihAUIe8dy3QwhscbnD73mY%3D)
