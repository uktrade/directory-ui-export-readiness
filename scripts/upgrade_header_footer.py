import pathlib
import re
import os

__here__ = pathlib.Path(__file__).parent
project_root = __here__ / ".."
dirs = [
    project_root / ".." / "directory-sso",
    project_root / ".." / "directory-sso-profile",
    project_root / ".." / "help",
    project_root / ".." / "directory-ui-buyer",
    project_root / ".." / "directory-ui-export-readiness",
    project_root / ".." / "navigator",
]
req_files = [
    "requirements.txt",
    "requirements.in",
    "requirements_test.txt",
    "requirements_test.in",
]

# print("Upgrading directory-header-footer dependency in all repos...")

# TODO:
# check in ./scripts for requirements* files
# edit makefile command to add git commands

exp = r'(?:directory-header-footer\.git@v)(\d*\.\d*\.\d)'


def get_file_string(filepath):
    """Get string from file."""
    with open(os.path.abspath(filepath)) as file:
        return file.read()


def current_version():
    filepath = os.path.abspath(project_root / "requirements.txt")
    reqs = get_file_string(filepath)
    regex = re.compile(exp)
    if regex.search(reqs) is not None:
        current_version = regex.search(reqs).group(1)
        print("Current directory-header-footer version:", current_version)
        upgrade()
    else:
        print("Error finding directory-header-footer version.")


def upgrade():
    new_version = input("Version to upgrade to: ")
    replace_in_dirs(new_version)


def done(version):
    print("Upgraded to version ", version)


def header_footer_exists(filepath):
    with open(filepath) as file:
        return re.search(exp, file.read())


def replace_in_files(dirname, replace):
    for filename in req_files:
        filepath = os.path.abspath(dirname / filename)
        if os.path.isfile(filepath) and header_footer_exists(filepath):
            replaced = re.sub(exp, replace, get_file_string(filepath))
            with open(filepath, "w") as file:
                file.write(replaced)
            # print(replaced)
            print(
                "Written to file: ",
                filepath)
        # else:
        #     print("Didn't find file: " + filepath + " Moving on.")


def replace_in_dirs(version):
    for dirname in dirs:
        replace = "directory-header-footer.git@v{}".format(version)
        replace_in_files(dirname, replace)
    done(version)


if __name__ == '__main__':
    # main()
    current_version()
