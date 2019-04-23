# Downloading new material
***in order to download new material every session run the following***
```
git submodule update --init --recursive
git pull --recursive-submodules
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
 
# Study Materials:
- gluon tutorials: http://mxnet.incubator.apache.org/versions/master/tutorials/index.html 
- reference book: http://d2l.ai/
- related repos:
  - https://github.com/cyrusmvahid/GluonBootcamp
  - https://github.com/cyrusmvahid/KDD18-Gluon
  - https://github.com/cyrusmvahid/MXNetWorkshopHongKong
