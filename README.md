# PyPAI

This is a python tool for Open Platform for AI.

# Installation

`pip install pypai`

# Demo

```python
from pypai import PAI

# Create a PAI cluster
pai = PAI(username='xxx', passwd='xxx')

# Generate the configuration
pai.generate_config()

# Submit the job
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
