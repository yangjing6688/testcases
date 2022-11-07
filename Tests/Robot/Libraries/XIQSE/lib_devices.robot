#----------------------------------------------------------------------
# Copyright (C) 2021... 2021 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# This file contains keywords specific to Devices functionality.
#

*** Settings ***
Library     xiqse/flows/common/XIQSE_CommonNavigator.py
Library     xiqse/flows/network/devices/XIQSE_NetworkDevices.py
Library     xiqse/flows/network/devices/devices/XIQSE_NetworkDevicesDevices.py


*** Keywords ***
Navigate to Devices and Confirm Success
    [Documentation]     Navigates to the Network> Devices> Devices view in XIQ-SE and confirms the action was successful

    ${nav_result}=  XIQSE Navigate to Network Devices Tab
    Should Be Equal As Integers         ${nav_result}     1

    ${sel_result}=  XIQSE Devices Select Devices Tab
    Should Be Equal As Integers         ${sel_result}     1

Navigate and Create Device
    [Documentation]     Navigates to the Devices tab and creates the specified device, confirming it was added
    [Arguments]         ${ip}  ${profile}

    Navigate to Devices and Confirm Success
    Create Device and Confirm Success           ${ip}  ${profile}

Navigate and Create Status Only Device
    [Documentation]     Navigates to the Devices tab and creates the specified status only device, confirming it was added
    [Arguments]         ${ip}  ${profile}

    Navigate to Devices and Confirm Success
    Create Status Only Device and Confirm Success       ${ip}  ${profile}

Navigate and Delete Device
    [Documentation]     Navigates to the Devices tab and deletes the specified device, confirming it was removed
    [Arguments]         ${ip}

    Navigate to Devices and Confirm Success
    Delete Device and Confirm Success           ${ip}

Navigate and Delete All Devices
    [Documentation]     Navigates to the Devices tab and deletes all of the devices, confirming they were removed

    Navigate to Devices and Confirm Success
    Delete All Devices and Confirm Success

Create Device and Confirm Success
    [Documentation]     Creates the specified device in XIQ-SE and confirms it was added successfully
    [Arguments]         ${ip}  ${profile}

    Add Device and Wait for Operation to Complete       ${ip}  ${profile}

    # Make sure we didn't get a license limit banner
    Confirm License Limit Warning Message Not Displayed

    # Make sure the device shows up in the Devices table
    ${confirm_result}=  XIQSE Wait Until Device Added   ${ip}
    Should Be Equal As Integers                         ${confirm_result}  1

Create Status Only Device and Confirm Success
    [Documentation]     Creates the specified device as Poll Status Only in XIQ-SE and confirms it was added successfully
    [Arguments]         ${ip}  ${profile}

    ${add_result}=  XIQSE Add Device                    ${ip}  ${profile}  status_only=True
    Should Be Equal As Integers                         ${add_result}      1

    # Wait until the Operations panel shows the add operation is completed
    ${wait_result}=  XIQSE Wait Until Device Add Operation Complete   retry_duration=10  retry_count=30
    Should Be Equal As Integers         ${wait_result}   1

    # Make sure we didn't get a license limit banner
    Confirm License Limit Warning Message Not Displayed

    # Make sure the device shows up in the Devices table
    ${confirm_result}=  XIQSE Wait Until Device Added   ${ip}
    Should Be Equal As Integers                         ${confirm_result}  1

Add Device and Wait for Device Add Operation to Complete
    [Documentation]     Adds the specified device in XIQ-SE and waits for the device add operations panel to show it is complete
    [Arguments]         ${ip}  ${profile}

    # Add the device
    ${add_result}=  XIQSE Add Device                    ${ip}  ${profile}
    Should Be Equal As Integers                         ${add_result}      1

    # Wait until the Operations panel shows the add operation is completed
    ${wait_result}=  XIQSE Wait Until Device Add Operation Complete   retry_duration=10  retry_count=30
    Should Be Equal As Integers         ${wait_result}   1

Add Device and Wait for Operation to Complete
    [Documentation]     Adds the specified device in XIQ-SE and waits for the device site action operations panel to show it is complete
    [Arguments]         ${ip}  ${profile}

    # Add the device
    ${add_result}=  XIQSE Add Device                    ${ip}  ${profile}
    Should Be Equal As Integers                         ${add_result}      1

    # Wait until the Operations panel shows the add operation is completed
    ${wait_result}=    Run Keyword If  '<Ping Only>' in '${profile}'
    ...    XIQSE Wait Until Device Add Operation Complete   retry_duration=10  retry_count=30
    ...    ELSE
    ...    XIQSE Wait Until Discover Site Actions Operation Complete   retry_duration=10  retry_count=30

    Should Be Equal As Integers         ${wait_result}   1

Search Device and Confirm Success
    [Documentation]     Performs a search and confirms the action was successful (does not confirm that something was found)
    [Arguments]         ${value}

    ${result}=  XIQSE Devices Perform Search  ${value}
    Should Be Equal As Integers               ${result}   1

Clear Search and Confirm Success
    [Documentation]     Clears the current search and confirms the action was successful

    ${result}=  XIQSE Devices Clear Search
    Should Be Equal As Integers             ${result}   1

Set Device Profile and Confirm Success
    [Documentation]     Sets the specified profile on the specified device and confirms the action was successful
    [Arguments]         ${ip}  ${profile}

    ${result}=  XIQSE Device Set Profile    ${ip}    ${profile}
    Should Be Equal As Integers             ${result}       1

Restart Device and Confirm Success
    [Documentation]     Restarts the specified device and confirms the action was successful
    [Arguments]         ${ip}

    ${result}=  XIQSE Perform Restart Device   ${ip}
    Should Be Equal As Integers                ${result}       1

Delete Device and Confirm Success
    [Documentation]     Deletes the specified device from XIQ-SE and confirms it was removed successfully
    [Arguments]         ${ip}

    ${del_result}=  XIQSE Delete Device                     ${ip}
    Should Be Equal As Integers                             ${del_result}      1

    ${confirm_result}=  XIQSE Wait Until Device Removed     ${ip}
    Should Be Equal As Integers                             ${confirm_result}  1

Delete All Devices and Confirm Success
    [Documentation]     Deletes all devices from XIQ-SE and confirms they were removed successfully

    ${del_result}=  XIQSE Delete All Devices
    Should Be Equal As Integers                             ${del_result}      1

    ${confirm_result}=  XIQSE Confirm Table Empty
    Should Be Equal As Integers                             ${confirm_result}  1

Confirm IP Address Present in Devices Table
    [Documentation]     Confirms the specified IP address is present in the Devices table
    [Arguments]         ${ip}

    ${result}=  XIQSE Wait Until Device Added   ${ip}
    Should Be Equal As Integers                 ${result}   1

Confirm IP Address Not Present in Devices Table
    [Documentation]     Confirms the specified IP address is not present in the Devices table
    [Arguments]         ${ip}

    ${result}=  XIQSE Wait Until Device Removed     ${ip}
    Should Be Equal As Integers                     ${result}   1

Confirm Device Archived
    [Documentation]     Confirms the specified device is archived by checking the Archived column
    [Arguments]         ${ip}

    ${result}=  XIQSE Wait Until Device Archived  ${ip}
    Should Be Equal As Integers     ${result}     1

Confirm Device Not Archived
    [Documentation]     Confirms the specified device is not archived by checking the Archived column
    [Arguments]         ${ip}

    ${result}=  XIQSE Wait Until Device Not Archived  ${ip}
    Should Be Equal As Integers     ${result}     1

Confirm XIQSE Device Onboarded to XIQ
    [Documentation]     Confirms the specified XIQSE device is onboarded to XIQ by checking the XIQ Onboarded column
    [Arguments]         ${ip}

    ${result}=  XIQSE Wait Until Device Onboarded to XIQ  ${ip}

    Run Keyword If  "${result}" == "-1"  Obtain Onboard Status Screenshot from Diagnostics
    Should Be Equal As Integers     ${result}     1

Confirm Device Status Up
    [Documentation]     Confirms the specified device has a device status of "up"
    [Arguments]         ${ip}

    ${result}=  XIQSE Wait Until Device Status Up    ${ip}
    Should Be Equal As Integers                      ${result}     1

Confirm Device Status Down
    [Documentation]     Confirms the specified device has a device status of "down"
    [Arguments]         ${ip}

    ${result}=  XIQSE Wait Until Device Status Down    ${ip}
    Should Be Equal As Integers                        ${result}     1

Navigate and Confirm Device Historical Statistics
    [Documentation]     Navigates and verifies the device historical statistics status on the specified device
    [Arguments]         ${device_ip}    ${expected_value}

    Navigate to Devices and Confirm Success
    Confirm Device Historical Statistics                ${device_ip}

Confirm Device Historical Statistics
    [Documentation]     Verifies the device historical statistics status on the specified device
    [Arguments]         ${device_ip}

    # Make sure the Stats column is being displayed
    ${col}=  XIQSE Devices Show Columns  Stats
    Should Be Equal As Integers          ${col}     1

    ${returned_value}=  XIQSE Wait Until Device Stats Historical      ${device_ip}
    Should Be Equal As Integers         ${returned_value}     1

Navigate and Confirm Device Threshold Alarms Statistics
    [Documentation]     Navigates and verifies the device threshold alarms statistics status on the specified device
    [Arguments]         ${device_ip}    ${expected_value}

    Navigate to Devices and Confirm Success
    Confirm Device Threshold Alarms Statistics                ${device_ip}

Confirm Device Threshold Alarms Statistics
    [Documentation]     Verifies the device threshold alarms statistics status on the specified device
    [Arguments]         ${device_ip}

    # Make sure the Stats column is being displayed
    ${col}=  XIQSE Devices Show Columns  Stats
    Should Be Equal As Integers          ${col}     1

    ${returned_value}=  XIQSE Wait Until Device Stats Threshold Alarms      ${device_ip}
    Should Be Equal As Integers         ${returned_value}     1

Navigate and Confirm Device Statistics Disabled
    [Documentation]     Navigates and verifies the device statistics status is disabled on the specified device
    [Arguments]         ${device_ip}    ${expected_value}

    Navigate to Devices and Confirm Success
    Confirm Device Statistics Disabled                ${device_ip}

Confirm Device Statistics Disabled
    [Documentation]     Verifies the device statistics status is disabled on the specified device
    [Arguments]         ${device_ip}

    # Make sure the Stats column is being displayed
    ${col}=  XIQSE Devices Show Columns  Stats
    Should Be Equal As Integers          ${col}     1

    ${returned_value}=  XIQSE Wait Until Device Stats Not Collecting      ${device_ip}
    Should Be Equal As Integers         ${returned_value}     1

Navigate and Confirm Device License
    [Documentation]     Navigates and verifies the device license on the specified device
    [Arguments]         ${device_ip}    ${license}

    Navigate to Devices and Confirm Success
    Confirm Device License               ${device_ip}    ${license}

Confirm Device License
    [Documentation]     Verifies the device license on the specified device
    [Arguments]         ${device_ip}    ${expected_value}

    # Make sure the Stats column is being displayed
    ${col}=  XIQSE Devices Show Columns  License
    Should Be Equal As Integers          ${col}     1

    ${returned_value}=  XIQSE Get Device License       ${device_ip}
    Should Be Equal As Strings             ${returned_value}    ${expected_value}    ignore_case=True
