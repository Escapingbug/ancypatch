from setuptools import setup, find_packages

setup(
    name='ancypatch',
    version='0.1.1',
    packages=find_packages('src'),
    package_dir={'ancypatch':'src/ancypatch'},
    package_data={
        '': ['*.c', '*.h']
    },
    install_requires=['keystone-engine', 'capstone', 'unicorn'],
    entry_points={
        'console_scripts': [
            'ancypatch = ancypatch.scripts.patch:main',
            'ancybindiff = ancypatch.scripts.bindiff:main',
            'ancyrun = ancypatch.scripts.patch:run',
            'ancyexplore = ancypatch.scripts.explore:run',
        ]
    },
    author='Anciety',
    author_email='ding641880047@126.com',
    description='helper scripts to patch a binary, forked version of patchkit',
    keywords='patch binary',
    url='http://anciety.cn/ancypatch/index.html',
)
