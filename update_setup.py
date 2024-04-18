
version = int(open("version").read())
version +=1
open("version", "w").write(str(version))

setup_str = f"""
import setuptools

setuptools.setup(
    name="audio-toolkit",
    version="0.{version}.0",
    author="Nguyen Ngoc Khanh",
    author_email="khanh.nguyen.contact@gmail.com",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/khanh101/audio-toolkit",
    packages=setuptools.find_packages(),
    license="MIT",
    install_requires=[
        "tqdm==4.65.0",
        "sqlitedict==2.1.0",
    ],
)
"""


open("setup.py", "w").write(setup_str)
