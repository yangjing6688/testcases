# Author        : Rameswar
# Date          : January 15th 2020
# Description   : Basic Login Test Cases
#
# Modified by   : Shreen Banu
# Date          : Oct 4 2022

# Topology      :
# Host ----- Cloud

*** Variables ***
${LOCATION}                 auto_location_01, Santa Clara, building_02, floor_04

*** Settings ***
# The keywords in Login.py have been moved to the keywords directory.
# If the moved keyword is not working correctly import the original library and remove the keywords/gui/login/KeywordsLogin.py version.
#Library     extauto/xiq/flows/common/Login.py
Library     keywords/gui/login/KeywordsLogin.py
Library     extauto/xiq/flows/manage/Devices.py

Variables    Environments/${TOPO}
Variables    Environments/${ENV}

Force Tags   testbed_none
Suite Teardown    Run Keyword And Warn On Failure     Test Suite Teardown

*** Keywords ***

Test Suite Teardown
    ${DELETE_AP}=                   Delete Devices              ${SIM_SERIAL}
    should be equal as integers     ${DELETE_AP}               1

    ${LOGOUT_RESULT}=               Logout User
    Should Be Equal As Integers     ${LOGOUT_RESULT}                1

    ${QUIT_BROWSER_RESULT}=         Quit Browser
    Should Be Equal As Integers     ${QUIT_BROWSER_RESULT}          1

*** Test Cases ***
TCCS-13211: Quick Add Onboard Simulated Device
    [Documentation]         Quick Onboarding - Add Simulated Devices
    [Tags]                  production      tccs_7651       tccs_13211

    ${device}=      Create Dictionary
    ...     name=simulated_dut08
    ...     model=AP122
    ...     simulated_count=1
    ...     onboard_device_type=Simulated
    ...     location=auto_location_01, Santa Clara, building_02, floor_04

    set suite variable    ${device}
    ${LOGIN_STATUS}=                Login User          ${tenant_username}          ${tenant_password}
    should be equal as integers     ${LOGIN_STATUS}               1

    ${ONBOARD_RESULT}=                  onboard device quick    ${device}
    Should Be Equal As Strings          ${ONBOARD_RESULT}       1

    ${SIM_SERIAL}=     set variable    ${${device.name}.serial}
    Set Suite Variable         ${SIM_SERIAL}