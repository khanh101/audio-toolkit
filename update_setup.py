if __name__ == "__main__":
    version = int(open("version").read())
    new_version = version+1
    open("version", "w").write(str(new_version))

    version_str = f"version=\"0.{version}.0\""
    new_version_str = f"version=\"0.{new_version}.0\""

    setup_str = open("setup.py").read()
    new_setup_str = setup_str.replace(version_str, new_version_str)
    open("setup.py", "w").write(new_setup_str)
