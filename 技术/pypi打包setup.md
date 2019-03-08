```python
from __future__ import print_function
from setuptools import setup, find_packages
import sys

setup(
    name="zhulong",

    version="1.1.43",

    author="lanmengfei",
    author_email="865377886@qq.com",
    description="兰孟飞深圳市筑龙科技的工作",
    long_description=open("README.txt",encoding="utf8").read(),
    

    url="https://github.com/lanmengfei/testdm",

    packages=find_packages(),

    package_data={#"zhulong.hunan":["profile"]
    "zhulong.util":["cfg_db"]
  
    },

    install_requires=[
        "pandas >= 0.13",
        "beautifulsoup4>=4.6.3",
        "cx-Oracle",
        "numpy",
        "psycopg2",
        "selenium",
        "xlsxwriter",
        "xlrd",
        "requests",
        "lxml",
        "sqlalchemy",
        "pymssql",
        "jieba",
        "mysqlclient",
        "pymssql",
        "lmf",
        "lmfscrap"
        ],

    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5"
    ],
)

```

