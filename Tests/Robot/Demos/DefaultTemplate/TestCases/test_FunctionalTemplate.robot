*** Settings ***
Resource        ../Resources/AllResources.robot
Suite Setup     Test Suite Setup
Suite Teardown  Test Suite Cleanup
Force Tags      testbed_1_node


Resource    ExtremeAutomation/Resources/Libraries/DefaultLibraries.robot

*** Test Cases ***
01 do_something
    [Documentation]  Test Objective: Run Test Case

    [Tags]   F-12345678902

    Log  Running Test Case



