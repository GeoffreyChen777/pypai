# PyPAI

![](https://img.shields.io/badge/pypai-v1.0-green.svg)
![](https://img.shields.io/badge/Unix-pass-blue.svg)
![](https://img.shields.io/badge/Windows-Failed-blue.svg)

This is a python tool for Open Platform for AI. Linux and MacOS are working fine. Windows are not supported now.

# Installation

`pip install pypai`

# Demo

1. Create and run `submit.py` in **your project folder** to generate the configuration:

```python
from pypai import PAI

# Create a PAI cluster
pai = PAI(username='xxx', passwd='xxx')

# Generate the configuration
pai.generate_config()
```

2. Open `pai_configuration.json` and modify it.

3. Change and run `submit.py` to submit your job:

```python
from pypai import PAI

# Create a PAI cluster
pai = PAI(username='xxx', passwd='xxx')

# Generate the configuration
pai.submit()
```


# API

```
class PAI:
    @paremeters:
    username: (str) PAI username
    passwd: (str) PAI password
    url: (str) PAI master node IP
    worker: (int) worker num for upload code
    
function generate_config:
    @paremeters:
    jobName='test'
    image='192.168.193.253:5000/pytorch'
    dataDir=''
    outputDir=''
    codeDir='$PAI_DEFAULT_FS_URI/Users/$PAI_USER_NAME/$PAI_USER_NAME~$PAI_JOB_NAME'
    gpuType=''
    
function submit:
    @paremeters:
    config_path='./pai_configuration.json'
    dir_path='./'            code path
    dest_dir='/Users/'       code root path in the hdfs
