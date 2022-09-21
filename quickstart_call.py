import quickstart_lib as qs
import os

from pathlib import Path


def start_text():
    print('=======================')
    print(' DessiA Bot quickstart')
    print('=======================\n')
    print('This script will generate for you the files needed to create a python package respecting DessiA guidelines.')
    print("If you don't understand a question or have no preference just type enter to have the default choice "
          "selected.")
    print('Most questions have to be answered with y=yes or n=no. Default value if nothing is answered '
          'is written in capital\n')
    input('Type any key to begin the process...')


def create_package_base(parent_folder):
    package_name = qs.enter_valid_name('Package')

    git_use = input('Do you want to use git in this project (eventually through a service like Github, Gitlab, Gitea, '
                    'Gogs)?: (Y/n): ')
    git_use = git_use.lower() != 'n'
    project_path = qs.check_git_use(git_use, package_name, parent_folder)
    module_name = qs.enter_valid_name('Module', 'core')
    setup_path, module_path = qs.create_base(project_path, package_name, module_name)
    return project_path, package_name, module_path, module_name, setup_path


def get_misc():
    short_description = input('Enter a short description : ')
    author_name = input('Enter your name : ')
    author_mail = input('Enter your e-mail : ')
    default_requirements = ['dessia_common>=0.7.2', 'volmdlr>=0.4.0']
    requirements = input("Enter required packages, separated by a comma (default : {})".format(default_requirements))
    python_version = input('Enter Python version (default : >=3.8) : ')
    return short_description, author_name, author_mail, requirements, python_version


def misc(project_path, package_name, auth_name, auth_mail, s_desc, reqs, py_ver):
    default_requirements = ['dessia_common>=0.7.2', 'volmdlr>=0.4.0']
    # Git tags
    from_git_tags = input('Do you want to enable version from git tags? (Y/n): ')
    from_git_tags = from_git_tags.lower() != 'n'
    # Gitignore
    create_gitignore = input('Do you want to create a python gitignore file? (Y/n): ')
    create_gitignore = create_gitignore.lower() != 'n'
    # README
    create_readme = input('Do you want to create a README file? It will be used as long description. (Y/n): ')
    create_readme = create_readme.lower() != 'n'
    # Code quality
    code_quality = input('Do you want to have some code quality checks? (Y/n): ')
    code_quality = code_quality.lower() != 'n'
    # CI
    drone = input('Do you want to generate a .drone.yml file for drone.io CI? (Y/n): ')
    drone = drone.lower() != 'n'

    qs.create_gitignore(create_gitignore, project_path)
    qs.create_readme(create_readme, project_path, package_name, auth_name, auth_mail, s_desc)
    qs.create_tests(project_path, package_name)
    qs.code_quality(code_quality, project_path, package_name)
    qs.create_drone(drone, project_path, package_name)

    requirements, python_version = qs.change_requirements(reqs, default_requirements, py_ver)
    package_version = qs.change_from_git_tags(from_git_tags)

    return requirements, python_version, package_version, s_desc


def main():
    parent_folder = Path(os.getcwd()).parent
    start_text()
    project_path, pkg_name, module_path, module_name, setup_path = create_package_base(parent_folder)
    s_desc, auth_name, auth_mail, reqs, py_ver = get_misc()
    requirement, python_version, pkg_version, short_desc = \
        misc(project_path, pkg_name, auth_name, auth_mail, s_desc, reqs, py_ver)
    qs.create_project(setup_path, project_path, pkg_name, pkg_version, short_desc, auth_name, auth_mail, reqs, py_ver)
    print('Project generated to {}'.format(project_path))


if __name__ == '__main__':
    main()
