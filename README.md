# dessia_bot_template
A template to build a dessia-compatible bot.

## Usage

### 1. Clone the Repository

First, clone this repository to your local machine using the following command:

```
git clone https://github.com/Dessia-tech/dessia_bot_template.git
cd dessia_bot_template

2. Execute the Quickstart Script
Run the quickstart Python script to set up your bot project. Depending on your operating system, you might need to use python or python3. Choose the appropriate command for your system:

On Linux/macOS:
python3 quickstart.py

On Windows:
python quickstart.py

The quickstart script will ask you a series of questions to configure your bot project.

3. Answer the Questions:

The quickstart script will prompt you with questions to customize your bot project. Here's what each question is about:

Package Name: Enter a name for your bot's package. This should be a lowercase name without special characters except for underscores.

Git Integration: Decide if you want to use Git for version control. If you choose "yes," make sure you have a Git repository set up and cloned to your computer.

Parent Folder: Specify the parent folder where your bot project will be generated. You can choose an existing folder or create a new one.

Module Name: Choose a name for the main module of your bot. The default is "core."

Short Description: Provide a short description of your bot.

Author Name: Enter your name.

Author Email: Enter your mail address.

Required Packages: List any required Python packages separated by commas. You can use the default requirements or specify your own.

Python Version: Specify the minimum Python version your bot requires. The default is ">=3.8."

Version from Git Tags: Decide whether you want to enable versioning based on Git tags (example v0.0.1).

Gitignore File: Choose whether to create a Python-specific .gitignore file.

Readme File: Choose whether to create a README file. This file will be used as the description of your project.

Tests: Decide whether to include code coverage and CI tests.

Code Quality Checks: Choose whether to include code quality checks like PEP8 and pylint.

CI (Continuous integraton): Decide whether to generate a .drone.yml file for drone.io CI.