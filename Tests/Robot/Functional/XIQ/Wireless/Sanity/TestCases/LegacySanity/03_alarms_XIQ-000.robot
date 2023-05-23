# Author        : hshivanagi
# Date          : June 2020
# Description   :  Generate Fake Alarms

# Topology      :
# AP --->XIQ Instance

# Pre-Condtion
# 1. AP should be onboarded and it is online

# Execution Command:
# robot -L INFO -v DEVICE:AP630 -v TOPO:g7r2 alarms.robot
# Select the "TOPO" and "DEVICE" variable based on Test bed

*** Variables ***


*** Settings ***
Library     common/Cli.py
# The keywords in Login.py have been moved to the keywords directory.
# If the moved keyword is not working correctly import the original library and remove the keywords/gui/login/KeywordsLogin.py version.
#Library     xiq/flows/common/Login.py
Library     keywords/gui/login/KeywordsLogin.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/Alarms.py

# The keywords in Login.py have been moved to the keywords directory.
# If the moved keyword is not working correctly import the original library and remove the keywords/gui/login/KeywordsLogin.py version.
#Library     xiq/flows/common/Login.py
Library     keywords/gui/login/KeywordsLogin.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/Alarms.py
Library     xiq/flows/manage/DeviceCliAccess.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}

Force Tags   testbed_1_node

Suite Teardown  Clean-up

*** Keywords ***

Clean-up
    [Documentation]         Cleanup script

    [Tags]                  cleanup     production

    ${LOGIN_STATUS}=                Login User              ${tenant_username}     ${tenant_password}
    should be equal as integers     ${LOGIN_STATUS}               1

    ${DELETE_DEVICE_STATUS}=            Delete Device                  device_serial=${ap1.serial}
    should be equal as integers     ${DELETE_DEVICE_STATUS}               1

    [Teardown]   run keywords        Logout User
    ...                              quit browser

*** Test Cases ***
TCCS-11616_Step1: Generate And Validate Fake Alarms
    [Documentation]    Chek the generation of alarms

    [Tags]             production     tccs_11616    tccs_11616_step1

    ${LOGIN_STATUS}=                    Login User      ${tenant_username}      ${tenant_password}      check_warning_msg=True
    should be equal as integers         ${LOGIN_STATUS}               1

    ${DEVICE_STATUS}=                   Get Device Status       device_serial=${ap1.serial}
    Should contain any                  ${DEVICE_STATUS}    green     config audit mismatch

    ${CLEAR_ALARM_STATUS}=              Clear Alarm                       CRITICAL

    ${SEND_CMD_STATUS}=                 Send Cmd On Device Advanced Cli    device_serial=${ap1.serial}    cmd=_test trap-case alert failure
    Should Not Be Equal As Strings      ${SEND_CMD_STATUS}          '-1'
    sleep                               60s
    ${ALARM_DETAILS}=                   Get Alarm Details                  CRITICAL
    should be equal as strings          '${ALARM_DETAILS}[severity]'       'CRITICAL'
    should be equal as strings          '${ALARM_DETAILS}[category]'       'System'
    should be equal as strings          '${ALARM_DETAILS}[description]'    'fan failure.'
    should be equal as strings          '${ALARM_DETAILS}[deviceMac]'      '${ap1.mac}'

    [Teardown]   run keywords        Logout User
    ...                              quit browser

