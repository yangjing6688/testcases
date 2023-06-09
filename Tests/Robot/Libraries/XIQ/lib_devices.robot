#----------------------------------------------------------------------
# Copyright (C) 2021... 2021 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# This file contains keywords specific to Devices functionality.
#

*** Settings ***
Library     xiq/flows/common/Navigator.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/DevicesActions.py


*** Keywords ***
Navigate to Devices and Confirm Success
    [Documentation]     Navigates to the Manage> Devices view and confirms the action was successful

    ${result}=  Navigate to Devices
    Should Be Equal As Integers  ${result}  1

Select Table View Type and Confirm Success
    [Documentation]     Selects the view type for the Devices table and confirms the action was successful
    [Arguments]         ${view_type}

    Log To Console  Selecting ${view_type} for Devices Table
    ${result}=  Select Table View Type      ${view_type}
    Should Be Equal As Integers  ${result}  1

Delete Device and Confirm Success
    [Documentation]     Deletes the specified device from the Manage> Devices list and confirms the action was successful
    [Arguments]         ${serial}

    ${result}=  Delete Device       device_serial=${serial}
    Should Be Equal As Integers     ${result}  1

Confirm Device Serial Present
    [Documentation]     Confirms the device with the specified serial number is present in the Devices table
    [Arguments]         ${serial}  ${retry_duration}=30  ${retry_count}=10

    ${result}=  Wait Until Device Added    device_serial=${serial}  retry_duration=${retry_duration}  retry_count=${retry_count}
    Should Be Equal As Integers            ${result}    1

Confirm Device MAC Address Present
    [Documentation]     Confirms the device with the specified MAC address is present in the Devices table
    [Arguments]         ${mac}  ${retry_duration}=30  ${retry_count}=10

    ${result}=  Wait Until Device Added    device_mac=${mac}  retry_duration=${retry_duration}  retry_count=${retry_count}
    Should Be Equal As Integers            ${result}    1

Confirm Device Serial Not Present
    [Documentation]     Confirms the device with the specified serial number is not present in the Devices table
    [Arguments]         ${serial}  ${retry_duration}=30  ${retry_count}=10

    ${result}=  Wait Until Device Removed    device_serial=${serial}  retry_duration=${retry_duration}  retry_count=${retry_count}
    Should Be Equal As Integers              ${result}    1

Confirm Device MAC Address Not Present
    [Documentation]     Confirms the device with the specified MAC address is not present in the Devices table
    [Arguments]         ${mac}  ${retry_duration}=30  ${retry_count}=10

    ${result}=  Wait Until Device Removed    device_mac=${mac}  retry_duration=${retry_duration}  retry_count=${retry_count}
    Should Be Equal As Integers              ${result}    1

Confirm Device Serial Online
    [Documentation]     Confirms the specified serial number has a connected/online status in XIQ
    [Arguments]         ${serial}  ${retry_duration}=30  ${retry_count}=10

    ${result}=  Wait Until Device Online  ${serial}  retry_duration=${retry_duration}  retry_count=${retry_count}
    Should Be Equal As Integers           ${result}    1

Confirm Device Serial Offline
    [Documentation]     Confirms the specified serial number has a disconnected/offline status in XIQ
    [Arguments]         ${serial}  ${retry_duration}=30  ${retry_count}=10

    ${result}=  Wait Until Device Offline   ${serial}  retry_duration=${retry_duration}  retry_count=${retry_count}
    Should Be Equal As Integers             ${result}    1

Confirm Device OS Version Present
    [Documentation]     Confirms the "OS Version" field is populated for the device in the Devices table
    [Arguments]         ${serial}

    ${result}=  Wait Until Device Data Present  ${serial}   OS VERSION
    Should Be Equal As Integers                 ${result}   1

Confirm Device Serial Has Expected Status
    [Documentation]     Checks the status of the specified device and confirms it matches the expected value
    [Arguments]         ${serial}  ${expected_status}

    ${device_status}=  Get Device Status  device_serial=${serial}
    Should Contain     ${device_status}   ${expected_status}

Confirm Device Serial Managed
    [Documentation]     Confirms the specified serial number has the "Managed" option set to "Managed"
    [Arguments]         ${serial}   ${retry_duration}=30  ${retry_count}=10

    ${result}=    Wait Until Device Managed    ${serial}   retry_duration=${retry_duration}  retry_count=${retry_count}
    Should Be Equal As Integers                ${result}      1

Confirm Device Status Icon
    [Documentation]     Checks that the specified device has the expected Device Status icon
    [Arguments]         ${serial}   ${expected_icon}

    ${status_icon}=    Get Device Status Icon   ${serial}
    Should Be Equal As Strings                  ${status_icon}      ${expected_icon}

Confirm Actions Button Is Disabled
    [Documentation]     Confirm that the 'Actions' button is disabled

    ${result}=    Verify Actions Button Enable      expect_failure=True
    Should Be Equal As Strings                ${result}     -1
