
*** Variables ***

*** Settings ***
Resource    Tests/Robot/Functional/XIQ/Wireless/External_Admin/Resources/AllResources.robot

Force Tags   testbed_none
Suite Setup     Test Suite Setup
Suite Teardown    Run Keyword And Warn On Failure     Test Suite Teardown


*** Keywords ***
Test Suite Setup
    # log in the user
    ${LOGIN_RESULT}=                Login User                  ${tenant_username}      ${tenant_password}      check_warning_msg=True
    Should Be Equal As Integers     ${LOGIN_RESULT}         1

    ${simulated_device}=      Create Dictionary
    ...     name=simulated_dut
    ...     model=AP460C
    ...     simulated_count=1
    ...     onboard_device_type=Simulated
    ...     location=auto_location_01, Santa Clara, building_02, floor_04

    set global variable  ${simulated_device}

Test Suite Teardown
    ${DELETE_AP}=                   Delete Devices       ${simulated_device.serial}
    should be equal as integers     ${DELETE_AP}               1
    Logout User
    Quit Browser

*** Test Cases ***
TCCS-13631: Login as External Admin account(Administrator role) and onboard a simulated-device to the external-VIQ
    [Documentation]         Check for Simulated Device onboarding in External admin account
    [Tags]                  development   tccs-13631

    ${ONBOARD_SIM_AP}=              Onboard Device Quick    ${simulated_device}
    Should Be Equal As Strings      ${ONBOARD_SIM_AP}       1
