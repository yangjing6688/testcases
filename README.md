# Welcome!
Welcome to the extreme_automation_test repository! This repostory uses the extreme_automation_test as the base for the tests that are contained in this repository. The tests are written in the [Python language](https://python.org/) and the [Robot language](https://robotframework.org/) executed with the [Pytest](https://docs.pytest.org/en/stable/) and [Robot](https://robotframework.org/) frameworks. For reporting we use the standard Robot reporting and for pytest we use a standard html file and [Allure](http://allure.qatools.ru/) for local runs. This provides a robost reporting for pytest using the [plugin allure-pytest](https://pypi.org/project/allure-pytest/). 

# Setup for Framework
There are three methods for setting up the AutoIQ python based framework.  Installing the tools natively will likely run faster on whichever system you are using but the instructions for this only contain the AutoIQ framework and tools.  If you intend to use the extAuto framework (UI Testing) and tools you'll need to install them as well.

The Virtual Machine and Docker setups contains the framework and tools for both AutoIQ as well as extAuto.  Using either of those methods to setup your framework allows you to use either Robot or python to create your tests.

## Installing tools natively

To install the AutoIQ framework and tools to your computer follow the instructions found [Here (in GitHub)](/doc/native_install).

## Using the Virtual Machine

To use a VM with all of the tools for AutoIQ and extAuto installed, follow the instructions found [Here (in MS Teams)](https://teams.microsoft.com/l/file/DF343077-C0DF-42A0-AB23-371A7AEEBB84?tenantId=fc8c2bf6-914d-4c1f-b352-46a9adb87030&fileType=docx&objectUrl=https%3A%2F%2Fextremenetworks2com.sharepoint.com%2Fsites%2Fqa-extauto%2FShared%20Documents%2FGeneral%2FDevelopment%20Environment%20Instructions%2FGetting%20the%20environment%20up%20and%20running.docx&baseUrl=https%3A%2F%2Fextremenetworks2com.sharepoint.com%2Fsites%2Fqa-extauto&serviceName=teams&threadId=19:9811efc2ec4e4a24bfaef6a88ecf79d0@thread.tacv2&groupId=55d5e532-9afd-4892-8119-df6ce68abfc1).

## Creating a docker environment

To use Docker containers with all of the tools for AutoIQ and extAuto installed, follow the instructions found [Here (in GitHub)](https://github.com/extremenetworks/econ-automation-framework/tree/main/vm_env/docker). 

# Test Case Creation Guidlines
Now that your development IDE is installed you can start to explore the Automation Framework. [Here (in GitHub)](doc/Test_Suite_Creation_Guidlines.md) is a guide that will help you understand the layout and design for you tests.

# Advanced Framework Features

## Special Low Level API Keyword args
There are special variables that you can pass into the low level keywords that will alter the behaivor the the keywords. Items like ignore failure or wait funtionality. See details [here (in GitHub)](doc/KeywordArguments.md)

