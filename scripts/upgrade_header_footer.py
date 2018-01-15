import pathlib
import re

__here__ = pathlib.Path(__file__).parent
requirements_file = __here__ / ".." / "requirements.txt"

# print("Upgrading directory-header-footer dependency in all repos...")

# TODO:
# check in ./scripts for requirements* files
# replace version in all locations
# edit makefile command to add git commands

exp = r'(?:directory-header-footer\.git@v)(\d*\.\d*\.\d)'


def requirements():
    """Get string from requirements.txt file."""
    with open(requirements_file) as file:
        requirements = file.read()
    return str(requirements)


def current_version():
    reqs = requirements()
    regex = re.compile(exp)
    if regex.search(reqs) is not None:
        current_version = regex.search(reqs).group(1)
        print("Current directory-header-footer version:", current_version)
    else:
        print("Error finding directory-header-footer version.")


def upgrade():
    new_version = input("Version to upgrade to: ")
    replace = "directory-header-footer.git@v{}".format(new_version)
    replaced = re.sub(exp, replace, requirements())
    with open(requirements_file, "w") as file:
        file.write(replaced)
    print("Upgraded to version ", new_version)
    print("Written file ", requirements_file)


def main():
    """Run the upgrader."""
    upgrade()


if __name__ == '__main__':
    main()
