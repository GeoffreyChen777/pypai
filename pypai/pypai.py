import requests
import pyhdfs
import json
import collections
import os
import threading
import uuid
from sys import platform

class PAI(object):
    def __init__(self, username, passwd, url='192.168.193.1', worker=4):
        self.url = url
        self.username = username
        self.passwd = passwd
        self.token = self.get_token()

        self.worker = worker
        self.hdfs = pyhdfs.HdfsClient(hosts='{}:50070'.format(self.url), user_name=self.username)


    @staticmethod
    def handle_error(response):
        print("[X] Error: {}".format(response['message']))
        exit()

    def generate_config(self, jobName='test', image='192.168.193.253:5000/pytorch',
                        dataDir='', outputDir='', codeDir='$PAI_DEFAULT_FS_URI/Users/$PAI_USER_NAME/$PAI_USER_NAME~$PAI_JOB_NAME',
                        gpuType=''):
        config = collections.OrderedDict()
        config["jobName"] = "{}_00000000".format(jobName)
        config["image"] = "{}".format(image)
        config["authFile"] = ""
        config["dataDir"] = "{}".format(dataDir)
        config["outputDir"] = "{}".format(outputDir)
        config["codeDir"] = "{}".format(codeDir)
        config["virtualCluster"] = "default"
        config["gpuType"] = "{}".format(gpuType)
        config["retryCount"] = 0
        role = collections.OrderedDict()
        role["name"] = "task"
        role["taskNumber"] = 1
        role["cpuNumber"] = 3
        role["memoryMB"] = 4000
        role["gpuNumber"] = 1
        role["command"] = "bash mount.sh"
        config["taskRoles"] = [role]
        self.write_configuration('./pai_configuration.json', config)


    def get_token(self):
        data = {"username": self.username, "password": self.passwd}
        response = json.loads(requests.post('http://{}/rest-server/api/v1/token'.format(self.url), json=data).text)

        if 'token' not in response:
            self.handle_error(response)
        else:
            return response['token']

    @staticmethod
    def write_configuration(config_path, data):
        with open(config_path, 'w') as writer:
            output = json.dumps(data, indent=4)
            writer.write(output)

    def submit(self, config_path='./pai_configuration.json', dir_path='./', dest_dir='/Users/', exclude_file=[], exclude_dir=[]):
        if not os.path.exists(config_path):
            print('[x] Can not find the configuration of the job. Please run generate_json() to make the default job configuration!')
            exit()
        else:

            with open(config_path, 'r') as reader:
                config = json.load(reader, object_pairs_hook=collections.OrderedDict)
                config['jobName'] = self.create_jobname(config['jobName'])
                self.write_configuration(config_path, config)
            job_dest_path = self._process_path(os.path.join(dest_dir, self.username, self.username + '~' + config['jobName']))
            self.upload(dir_path, job_dest_path, exclude_file, exclude_dir)

            headers = {"Content-Type": "application/json",
                       "Authorization": "Bearer {}".format(self.token)}
            response = json.loads(requests.post('http://{}/rest-server/api/v1/user/{}/jobs'.format(self.url, self.username), json=config, headers=headers).text)

            if 'code' in response:
                self.handle_error(response)
            else:
                print("=> Upload Job Name: {} Successfully!".format(config['jobName']))

    @staticmethod
    def create_jobname(old_name):
        new_name = ''.join(old_name.split('_')[:-1]) + '_' + str(uuid.uuid4().fields[-1])[:8]
        return new_name

    @staticmethod
    def if_is_exclude_file(name, exclude):
        return '.' + name.split('.')[-1] in exclude

    @staticmethod
    def if_is_exclude_dir(name, exclude):
        for e in exclude:
            if name.startswith(e):
                return True


    def get_file_list(self, dir_path, exclude_file, exclude_dir):
        file_list = []
        for p, d, fl in os.walk(dir_path):
            if self.if_is_exclude_dir(p, exclude_dir):
                continue
            for f in fl:
                if self.if_is_exclude_file(f, exclude_file):
                    continue
                if p.startswith('./'):
                    p = p[2:]
                file_list.append(self._process_path(os.path.join(p, f)))
        return file_list

    @staticmethod
    def _process_path(path):
        if platform == 'win32' or platform == 'win64':
            path = path.split("\\")
            path = '/'.join(path)
        return path

    @staticmethod
    def upload_func(hdfs, src, dest):
        hdfs.copy_from_local(src, dest)

    def upload_list(self, upload_func, hdfs, file_list, dest_dir):
        try:
            for src in file_list:
                upload_file = self._process_path(os.path.join(dest_dir, src))
                upload_func(hdfs, src, upload_file)
        except Exception as e:
            print("[x] Upload failed!")
            print(e)
            exit()
            

    def upload(self, dir_path, dest_dir, exclude_file, exclude_dir):
        file_list = self.get_file_list(dir_path, exclude_file, exclude_dir)
        print("=> Uploading...")
        if len(file_list) < self.worker:
            self.upload_list(self.upload_func, self.hdfs, file_list, dest_dir)
        else:
            file_count = len(file_list)
            threads = []
            for i in range(self.worker):
                t = threading.Thread(target=self.upload_list,
                                     args=(self.upload_func, self.hdfs,
                                     file_list[int(i/self.worker*file_count):int((i+1)/self.worker*file_count)],
                                     dest_dir,))
                threads.append(t)

            for t in threads:
                t.start()
                t.join()

