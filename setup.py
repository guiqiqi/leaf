"""打包发布文件"""

import setuptools

VERSION = "1.0.9.1.dev4"

# 读取项目说明
with open("README.md", "r", encoding="utf-8") as handler:
    long_description = handler.read()

# 读取依赖
with open("requirements.txt", "r") as handler:
    string = handler.read()
    pvs = string.split('\n')
    packages = [pv.split("==")[0] for pv in pvs if pv]
    # packages = [pv for pv in pvs if pv]

setuptools.setup(
    name="wxleaf",
    version=VERSION,
    author="Gui Qiqi",
    license="Apache Software License",
    install_requires=packages,
    author_email="guiqiqi187@gmail.com",
    description="一个开发友好、功能完备的开源微信商城框架",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/guiqiqi/leaf",
    packages=setuptools.find_packages(),
    package_data={
        "leaf.weixin": ["errcodes.json"]
    },
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Development Status :: 1 - Planning",
        "Framework :: Flask",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: Chinese (Simplified)",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.6"
)
