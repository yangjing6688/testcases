# **** PLEASE NOTE ****
The documentation on this page is deprecated and is no longer up-to-date.  It remains as a reference in the event someone wants to try to setup RED to use a debugger for robot scripts.

# **** PLEASE NOTE ****

# Test Case Creation Guidlines
In this document you will learn how to create a new Test Suite with test cases. To ensure that all tests are simliar in design and file strcuture, please use the following format defined in the default template located in the econ-robot-tests repository: `/econ-robot-tests/Demos/NetworkElements/DefaultTemplate`.

![Import project](img/TestDesignFileFormat.png)

The file strucution contains a top level directory ( the test suite name ) and two directories under it.

* Resources -  This is where the test resources are kept.
* Test Cases - This is where the test cases files are kept.

### Resources
The `Resources` directory will contain the AllResources.robot file that will import the main libraries from the ExtremeAutomation Libraray. It will also import any UDKs that are created locally for the test and the TestSuiteVariables.yaml file. A variable will be decleared for the test bed resource file that will be filled in at runtime `${TestBedVariable}`.

### Test Cases
The `Test Cases` directory will contain the test case files. We recommend that one test case should be contained in one test case file. The file format should be the folllowing:

	Format:
		<number>_<test case name>.robot

	Example:

		01_VLAN_CREATE.robot

## Understanding The Files Within the Test Suite
The core parts of a robot test suite are as follows:


The Resources Directory:

*	`AllResources.robot`: Contains robot imports for keyword files and other libraries.
*	`SuiteUdks.robot`: Location where all suite specific user defined keywords can be created such as test suite setup/teardown.
	*	`TestSuiteVariables.yaml`: Yaml file with all variables that are not specific to the test environment.


The TestCases Directory:

*	`__init__.robot`: Contains documentation, a link to the all resources, and special calls for suite setup and suite teardown.
*	`FunctionalTestTemplate.robot`: A robot test case.


## Understanding the Test Bed Yaml File
The test bed file consists of elements  (NetworkElements, Traffic Generators, End Systems ) and port configrations. The main types for elements are:

* netelem<number> - This is the network element (switch). The number after it is a unique identifier.
* tgen<number> - The Traffic Generator element (Ixia, Sprient, Jets). The number after it is a unique identifier.
* endsystem<number> - The end system (Linux box, or other system). The number after it is a unique identifier.

All element types have common attributes such as name, ip, port. Please refer to the [main_template.yaml](https://github.com/extremenetworks/econ-robot-tests/blob/main/TestEnvironments/Templates/main_template.yaml) file for details on the required and optional parameters for all element types.

## Variables in the YAML file in Robot
Any variables that you defined in the test bed yaml or test suite yaml file can be access in the robot test case file via this syntax:

	 ${netelem1.name}

The example above will access the following part of the test bed yaml file:

	netelem1:
		name:                     "EXOS"
		ip:                       "10.148.35.202"
		port:                     "23"
		mgmt_vlan:                "VLAN_4000"

The nested values in the yaml file are aceesed in robot by the dot notation surounded by ${...}. The value for  `${netelem1.name}` would be the string `EXOS`.

# Procedure:
1. 	Open the configured IDE (PyCharm or RED).
2.	Navigate to network element test suite template directory.
	(econ_robot_tests/Demo/NetworkElements/TestSuiteTemplates)
3.	Make a copy of this (TestSuiteTemplates) directory with a new directory name of your choice.
4.  Create a new test bed file or checkout a test bed for testing from the list of test bed located [here](https://github.com/extremenetworks/econ-robot-tests/tree/main/TestEnvironments/Swdev/Rdu) 
5. Now you should have a blank test structure and an environment to execute the test. 

## Creating a Test Case
1.	Rename FunctionalTestTemplate.robot to a name of your choice. See [guidlines](#test-cases). 
2.	Open the test case and replace <Test Case Name> at the top with the name of your test. We usually name the test case the name of the file without the extention (.robot).
3.	Remove log steps as we will be replacing them with other keywords.
4.	Modify the documentation to reflect the objective the test case.
5.	[Tags] can be used to tag the case with a string. For example, tag the case with EXOS to show that the case is supported by EXOS. `Note- The # is a comment and must be removed.` 

		***NOTE***: Two spaces are the delimiter in robot for a new argument so be sure to put two spaces between and keywords / arguments.
6.	[Setup] can be used to call a keyword that the start of the testcase. If the setup fails the case will not run.
7.	[Teardown] is where we defined the keywords we want to run at the end of the testcase even if there is a failure/exception. `Note- The # is a comment and must be removed.` 
9.	During the task of writing cases you will likely come across keywords you want to use that are not imported by default. In this case you will need to use the following methods to execute the commands:

ClI Methods:

		send_cmd 
		send_cmd_verify_output
		send_cmd_verify_output_regex
		send_cmd_verify_output_table


JSONRPC Methods:

		send_cmd_json_rpc
		verify_field
		get_field
		get_fields
		wait_for_field

## Connecting to a Device

Connect to a Network Element:

	Connect to Network Element  ${netelem1.name}  ${netelem1.ip}  ${netelem1.username}
	...                         ${netelem1.password}  ${netelem1.connection_method}  ${netelem1.os}

Connect to a Traffic Generator Element:

	Connect To Traffic Generator    ${tgen1.name}  ${tgen1.vendor}  ${tgen1.ip}
	
## Finding Lower Level APIs

	<protocol><action><event>

Actions:

- create
- delete
- set
- clear
- enable
- disable
- verify

example: Vlan Clear Egress



## Running a Test Suite
1.	In a command windows, navigate to the directory of your test suite above the Resources and TestCases directories. 
2.	Issue the command `pybot -v TestBedVariable:Resources/sample_env.yaml  -L trace TestCases` from a command prompt.

	- Pybot is the name of the application robot uses to run. In newer versions it is just robot.
	- -v TestBedVariable specifices what to substitute in place for the ${TestBedVariable} in your 		AllResources.robot file. We use this to be able to run on multiple environments.
	-	-L trace enables trace logging.
	-	TestCases is the location of the __init__.robot file for the test suite. This is considered the base of the test suite so to speak. If you were to run test case robot file directly it would not run the suite setup and suite teardown.
3.	After your test completes a log file will be generated and can be opened in a brower to see the results. The following files will be generated from the run. report.html, log.html and output.xml. Open the report.html file in a browser to see the results of the test.


![Import project](img/TestCaseExecutionReport.png)




