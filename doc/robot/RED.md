## Install the requirements and edit the virtual enviroment
While in your virtual environement, issue the following command to install the Extreme Automation Library requirements.


        pip install -r <path to econ-robot-automation>/requirements.txt

This should install all of the requriements for the Extreme Automation Library into your virtual environement. Open the `pyvenv.cfg` file (localed in venv directory) and edit the following line:

    From -> include-system-site-packages = false
	To   -> include-system-site-packages = true

This will allow RED to install the debugging package so that you will be able to use the debugger from robot to python.

## Install the RED Development Environment
The [RED development environment](https://nokia.github.io/RED/help/) will allow you to debug Robot test cases into the python library code. You will have the abltiy to set break points and be able to step through code. You can download the RED Editor 
[Windows](https://github.com/nokia/RED/releases/download/0.9.5/RED_0.9.5.20200724101746-win32.win32.x86_64.zip) or [Linux](https://github.com/nokia/RED/releases/download/0.9.5/RED_0.9.5.20200724101746-linux.gtk.x86_64.zip) 
or [Mac](https://github.com/nokia/RED/releases/download/0.9.5/RED_0.9.5.20200724101746-macosx.cocoa.x86_64.zip).
Once you have downloaded the RED editor unzip it locally on your machine. Start the RED Editor.

### Adding the workspace
Once RED is up, you will need to add the new workspace to include the Extreme Automation Library and the Test Repository.

![Import project](img/start_red.png)

Open up the project explorer and choose Import project.

![Import project](img/Red_import_project.png)

Under General choose Exsisting Project into Workspace.

![Import project](img/Red_import_project_select.png)

Import the project for econ_robot_automation.

![Import project](img/Red_import_project_finish_tests.png)

Import the project for econ_robot_tests ( repeat the import steps above).

![Import project](img/Red_import_project_finish.png)

### RED Preferences
Once the projects have been imported, you will need to set some preferences. On the top menu click on `Window->Preferences`.

![Import project](img/Red_preferences.png)

Select the Libraries and make sure the '`Add project modules recursively to PYTHONPATH\CLASSPATH during autodiscovery on virtualenv`' is checked.

![Import project](img/Red_preferences_python_path.png)

Next select the '`Installed frameworks`' option and click on the add button. Make sure to delete all of the ones that are currently in this list before you add the new one. Also make sure that you add the python3 version if a dialog appears. 

![Import project](img/Red_installed_frameworks.png)

Enter in the path to the virual environment that you created for the econ_robot_tests.

![Import project](img/Red_installed_frameworks_finished.png)

Select OK to rebuild the environement.


## RED Install PyDev

Next you will need to install PyDev into RED. Select '`Help->Eclipse Marketplace...`'

![Import project](img/Red_marketplace.png)

Enter in `pydev` in the search and press the `go` button. Once the search comes back click on the install button next to pydev.

![Import project](img/Red_install_pydev.png)

Make sure to accept the license.

![Import project](img/Red_install_pydev_finshed.png)

Once the PyDev has been installed elipse should ask to be restarted. When it comes back you may see this option appear. Click on Manual config.

![Import project](img/Red_python_config.png)

Add in the python interpreter for the econ_robot_automation virtual environment. You can select the python3 exe from the virtual environment and name it econ_robot_automation_python3.

![Import project](img/Red_python_config_interpreter.png)


Select the default packages and click ok.

![Import project](img/Red_pydev_python.png)

The completed interpretor should look this the image below. Exit out of this screen.

![Import project](img/Red_pydev_python_completed.png)

Once the pydev has been installed, you will need to set some preferences. On the top menu click on `Window->Preferences`. Select the PyDev Debug option and set the Remote debugger server activation to 'start when the plugin is started'. Exit out of this menu.


## Install the debugging package for Robot / Python
From the econ_robot_tests repository in the workspace, right click and select '`New->other`'

![Import project](img/Red_select_new_other.png)

Select the RED with PyDev debugging sesssion and press next.

![Import project](img/Red_select_new.png)

Select the Robot installed framework and press next.

![Import project](img/Red_select_new_framework.png)

Click next and take the default. Press the finished button and the python debugging package will be installed.

![Import project](img/Red_select_new_launch_config.png)

The following screen will appear. Continue to the [Running the Demo tests in RED](#Running_the_Demo_tests_in_RED) to configure the test to execute.

![Import project](img/Red_select_new_launch_config_execution.png)


## Running the Demo tests in RED
You will need to create a run configuration for your test. In this case we will use the demo vlan test. This is located here: /econ-robot-tests/Demos/NetworkElements/VLAN/TestCases/01_Vlan.robot

Either create a new run configuration or the new launch directions above will allow you to create one. 

-   Select the project, this case it will be econ-robot-tests
-   Select the test by using the Browse button and selecting the 01_Vlan.robot
-   Add the following Arguments:

    
        --variable TestBedVariable:Demos/NetworkElements/VLAN/Resources/demo_salem_1_node_exos.yaml

![Import project](img/Red_run_configuration.png)

-   Select the Executor tab and enter in the python exe and the additional executable file arguments. In this case the paths will be different. These are some examples below:


- Python EXE:

            C:\Users\elatour\ExtremeContinuum\econ-robot-automation\venv\Scripts\python.exe

- Additional executable file arguments:

        -m redpydevd --pydevd C:\Users\elatour\installed\RED_0.9.5.20200724101746-win32.win32.x86_64\plugins\org.python.pydev.core_8.2.0.202102211157\pysrc\pydevd.py

    Now you should be able to set breaks points in the Robot test case and the python library files and select debug to run. 

    ![Import project](img/Red_run_configuration.png)

## Install the GIT Plugin for RED
If you would like to have the GIT Plugin installed on RED, following the directions [here](git_plugin.md).