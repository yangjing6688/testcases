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
Library     xiq/flows/common/Login.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/Alarms.py

Library     xiq/flows/common/Login.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/Alarms.py
Library     xiq/flows/manage/DeviceCliAccess.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}

Force Tags   testbed_1_node

*** Test Cases ***
TCCS-11616: Generate And Validate Fake Alarms
    [Documentation]    Chek the generation of alarms

    [Tags]             production     tccs_11616

    ${LOGIN_STATUS}=                 Login User              ${tenant_username}     ${tenant_password}
    should be equal as strings      '${LOGIN_STATUS}'        '1'

    ${AP_STATUS}=                   Get AP Status           ap_mac=${ap1.mac}
    Should Be Equal As Strings     '${AP_STATUS}'          'green'

    Clear Alarm                       CRITICAL

    Send Cmd On Device Advanced Cli    device_serial=${ap1.serial}    cmd=_test trap-case alert failure
    sleep                             30
    ${ALARM_DETAILS}=                 Get Alarm Details                  CRITICAL
    should be equal as strings       '${ALARM_DETAILS}[severity]'       'CRITICAL'
    should be equal as strings       '${ALARM_DETAILS}[category]'       'System'
    should be equal as strings       '${ALARM_DETAILS}[description]'    'fan failure.'
    should be equal as strings       '${ALARM_DETAILS}[deviceMac]'      '${ap1.mac}'
    [Teardown]   run keywords        Logout User
    ...                              quit browser

Clean-up
    [Documentation]         Cleanup script

    [Tags]                  cleanup
    Login User                     ${tenant_username}          ${tenant_password}
    Delete Device                  device_serial=${ap1.serial}

    [Teardown]   run keywords        Logout User
    ...                              quit browser

