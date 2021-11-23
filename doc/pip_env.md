## Configure the Development Environment
In order to download and install the latest Extreme Automation Framework you will need to add the artifactory pypi repos to your pip.conf or pip.ini file. Issue the following command to see where your virtual env is looking for the pip files:

    pip config -v list

If you get an error for the command above make sure that you have the correct PATH set for python in your environment to ensure that python and pip are found. You can use the following commands to set the version that are being used:

    python --version
        Python 3.9.1

    pip --version
        pip 20.3.3 from c:\python\lib\site-packages\pip (python 3.9)


Add the following configration to the pip configuration file in order to be able to download the Extreme Automation Framework.

Choose the file to edit from the  pip config -v list above. Given the example below of the output:

    pip config -v list
        For variant 'global', will try loading 'C:\ProgramData\pip\pip.ini'
        For variant 'user', will try loading 'C:\<User directory>\pip\pip.ini'

Edit the user directory file.

1. Cd to the home directory
2. Create the directory called pip if it doesn't exist.
3. Cd to the pip directory
4. Create the file pip.ini if is doesn't exist
5. Add the following content to this file and save it:


        [global]
        trusted-host = engartifacts1.extremenetworks.com
        extra-index-url =   http://engartifacts1.extremenetworks.com:8081/artifactory/api/pypi/econ-automation/simple

This will instruct pip to look for extra packages in the artifactory URL speificed in the extra-index-url argument which will allow you to install the Extreme Automation framework.


### Install C++ Build Tools (Windows Only)
 If you are installing this framework on windows you will need to install the C++ Compiler from this [page](https://wiki.python.org/moin/WindowsCompilers). First check if you already have C++ build tools installed. It will show up in program files as 'Microsoft Visual C++ Compiler Package'. If you have this installed you can skip this step. If it isn't installed, downloading the [build tools for visual studio 2019](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2019) and install it.

 Issue this command to ensure that the setup tools are correct.

    pip install --upgrade setuptools