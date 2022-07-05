# Welcome!
Welcome to the extreme_automation_test repository! This repostory uses the extreme_automation_test as the base for the tests that are contained in this repository. The tests are written in the [Python language](https://python.org/) and the [Robot language](https://robotframework.org/) executed with the [Pytest](https://docs.pytest.org/en/stable/) and [Robot](https://robotframework.org/) frameworks. For reporting we use the standard Robot reporting and for pytest we use a standard html file and [Allure](http://allure.qatools.ru/) for local runs. This provides a robost reporting for pytest using the [plugin allure-pytest](https://pypi.org/project/allure-pytest/).

# Setup for Framework
There are three methods for setting up the AutoIQ python based framework.  Installing the tools natively will likely run faster on whichever system you are using but the instructions for this only contain the AutoIQ framework and tools. The AutoIQ framework includes both the XIQ UI, Switch testing and Traffic generation keywords. There are 3 paths that must be included in the PYTHONPATH in order to get the tests cases to work.  Note: Once you have configured your PYTHONPATH correctly you'll want to ensure the path persists by adding it to your startup or setup scripts.

Linux:

      PYTHONPATH=<path to repo>/extreme_automation_framework:<path to repo>/extreme_automation_framework/extauto:<path to repo>/extreme_automation_tests

Windows:

      PYTHONPATH=<path to repo>/extreme_automation_framework;<path to repo>/extreme_automation_framework/extauto;<path to repo>/extreme_automation_tests


The Virtual Machine and Docker setups contains the framework and tools for both AutoIQ as well as extAuto.  Using either of those methods to setup your framework allows you to use either Robot or python to create your tests.

## Installing tools natively

To install the AutoIQ framework and tools to your computer follow the instructions found [Here (in GitHub)](doc/native_install/README.md).

## Using the Virtual Machine

To use a VM with all of the tools for AutoIQ and extAuto installed, follow the instructions found [Here (in MS Teams)](https://teams.microsoft.com/l/file/DF343077-C0DF-42A0-AB23-371A7AEEBB84?tenantId=fc8c2bf6-914d-4c1f-b352-46a9adb87030&fileType=docx&objectUrl=https%3A%2F%2Fextremenetworks2com.sharepoint.com%2Fsites%2Fqa-extauto%2FShared%20Documents%2FGeneral%2FDevelopment%20Environment%20Instructions%2FGetting%20the%20environment%20up%20and%20running.docx&baseUrl=https%3A%2F%2Fextremenetworks2com.sharepoint.com%2Fsites%2Fqa-extauto&serviceName=teams&threadId=19:9811efc2ec4e4a24bfaef6a88ecf79d0@thread.tacv2&groupId=55d5e532-9afd-4892-8119-df6ce68abfc1).

## Creating a docker environment

To use Docker containers with all of the tools for AutoIQ and extAuto installed, follow the instructions found [Here (in GitHub)](https://github.com/extremenetworks/extreme_automation_framework/tree/main/vm_env/docker).

# Test Case Creation Guidlines

Now that your development IDE is installed you can start to explore the Automation Framework. [Here (in GitHub)](doc/Test_Suite_Creation_Guidlines.md) is a guide that will help you understand the layout and design for your tests.

# Test Bed Information
An explaination of test bed files can be found [here](Testbeds/README.md). Details on the required and optional parameters for creating test bed files can be found in the [Test Bed Templates Directory](Testbeds/Templates/).

# How to bypass CI checks

### Instructions
1. Request access. Skipping CI checks requires authorization. You are unable to perform a skip unless your username is on the list of authorized users.
    - If you need the ongoing ability to skip CI checks please email the repository admins with a request for authorization. Please include the specific reasons why you need to be able to skip CI checks.
    - If this is a special circumstance and you only need to bypass the CI checks once you can send an email request to one of the repository admins. We are happy to take care of that for you.
1. Add `[Skip Checks: <check to skip>, <check to skip>]` to the *beginning* of the title for your pull request.
    - If you have already created a pull request, you can edit the title by going to your pull request page and clicking edit in the top right corner of the page. The title will then become editable.
    - This string is not case sensitive, but the spacing does matter.
    - Example title: `[Skip Checks: Tags] XIQ-1000: do something`
    - Example multi-skip title: `[Skip Checks: Tags, Testbed] XIQ-1000: do something`
1. The skip only applies to your GitHub username. So, if you are working with multiple people on a PR or are performing a skip for someone else you will need to be the last person to have commited a change to the PR. This can be a real change or a dummy change that is just for the purposes of skipping the CI check.

### More info on the supported skips
The currently supported skips are: `Testbed`, `Dir`, `File`, `Reserved Tags`, `Tags`, `Func`

`Testbed`
    - Skips the entire "Testbed file validation" section of the CI

`Dir`
    - Skips the entire "Directory structure validation" section of the CI

`File`
    - Skips the entire "File name and location validation" section of the CI

`Reserved Tags`
    - Removes the restriction that disallowes adding certain reserved tags/markers to a testcase. ( production, regression, nightly, sanity, p1, p2, p3, p4 )
    - Also, removes the need to have a "development" tag on each testcase

`Tags`
    - Skips the entire "Tags/Markers validation" section of the CI


`Func`
    - Skips the entire "Test functionality validation" section of the CI

# Advanced Framework Features

## Special Low Level API Keyword args

There are special variables that you can pass into the low level keywords that will alter the behaivor of the keywords. Items like ignore failure or wait funtionality. See details [here (in GitHub)](doc/KeywordArguments.md)


