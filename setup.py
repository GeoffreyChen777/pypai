from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='pypai',
      version='1.3',
      description='The python tool for Open Platform for AI',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/GeoffreyChen777/pypai',
      author='Geoffrey CHen',
      author_email='geoffreychen777@gmail.com',
      license='MIT',
      packages=['pypai'],
      zip_safe=False,
      install_requires=[
        'requests',
        'pyhdfs',
    ])
