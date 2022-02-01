# How to Install the AutoIQ framework and tools

## Step 1: Install python 3.x
Install [Python 3](https://www.python.org/downloads/) on your developement system. This is required to run these tests.

## Step 2: Install the Extreme Automation Framework Repository
You will need pull the GIT repository for the AutoIQ Framework [here](https://github.com/extremenetworks/extreme_automation_framework). For Example, choose a directory on your local system and use the following commands to pull down the AutoIQ and  repositories. From a command window:

    git clone git@github.com:extremenetworks/extreme_automation_framework.git
    git clone git@github.com:extremenetworks/extreme_automation_tests.git
    git clone git@github.extremenetworks.com:Engineering/cw_automation.git

Next you will need to set your system PYTHONPATH environment variable for the OS to the base directory of these repositories.

- Windows:

        PYTHONPATH=<Base Directory>/extreme_automation_framework;<Base Directory>/extreme_automation_tests;<Base Directory>/extauto

- Linux:

        PYTHONPATH=<Base Directory>/extreme_automation_framework:<Base Directory>/extreme_automation_tests:<Base Directory>/extauto


## Step 3: Create a Virtual Environment
### Creating a Virtual Environment on Windows
Install python 3 on your system https://www.python.org/downloads/ and 
Issue the following commands in a command prompt at the base root for the project extreme_automation_tests:

- Issue the following commands at the prompt:

        python -m venv venv
        venv\\Scripts\\activate.bat

### Creating a Virtual Environment on Linux
Install python 3 on your system https://www.python.org/downloads/ and 
Issue the following commands in a command prompt at the base root for the project extreme_automation_tests:

- Issue the following commands at the prompt:

        python -m venv venv
        source venv/bin/activate

## Step 4: Install the Framework Requirements in the Virtual Environment
You will need to install the requirements.txt file in your virtual enviroment so that all of the required python packages will be installed. To do this start your virtual environment located in the `extreme_automation_tests` directory. Cd to the `extreme_automation_tests` repository and run the following command in your virutal environment:

        pip install -r requirements.txt

This should install all of the requirements for the Automation Framework and pytest. You can verify this by typing `pip list` and see that the same packages located in [this](https://github.com/extremenetworks/extreme_automation_tests/blob/main/requirements.txt) file are installed. 

    
## Step 5: Install and Configuration an IDE
There are a numerous of ways that a new developer can set up this framework and tests.

- We have directions to install [PyCharm](../PYCHARM.md) IDE to develop test cases.
