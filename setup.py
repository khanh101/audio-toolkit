import setuptools

if __name__ == "__main__":
    with open("README.md") as f:
        long_description = f.read()
    
    with open("version") as f:
        version = int(f.read())

    new_version = version+1
    with open("version", "w") as f:
        f.write(str(new_version))

    setuptools.setup(
        name="audio-toolkit",
        version=f"0.{version}.0",
        author="Nguyen Ngoc Khanh",
        author_email="khanh.nguyen.contact@gmail.com",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/khanh101/audio-tools",
        packages=setuptools.find_packages(),
        license="MIT",
        install_requires=[
            "tqdm==4.65.0",
            "sqlitedict==2.1.0",
        ],
    )
