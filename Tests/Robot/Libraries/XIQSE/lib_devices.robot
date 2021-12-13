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
    ${wait_result}=  XIQSE Wait Until Device Add Operation Complete   retry_duration=10  retry_count=6
    Should Be Equal As Integers         ${wait_result}   1

    # Make sure we didn't get a license limit banner
    Confirm License Limit Warning Message Not Displayed

    # Make sure the device shows up in the Devices table
    ${confirm_result}=  XIQSE Wait Until Device Added   ${ip}
    Should Be Equal As Integers                         ${confirm_result}  1

Add Device and Wait for Operation to Complete
    [Documentation]     Adds the specified device in XIQ-SE and waits for the operations panel to show it is complete
    [Arguments]         ${ip}  ${profile}

    # Add the device
    ${add_result}=  XIQSE Add Device                    ${ip}  ${profile}
    Should Be Equal As Integers                         ${add_result}      1

    # Wait until the Operations panel shows the add operation is completed
    ${wait_result}=  XIQSE Wait Until Device Add Operation Complete   retry_duration=10  retry_count=6
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

Delete Device and Confirm Success
    [Documentation]     Deletes the specified device from XIQ-SE and confirms it was removed successfully
    [Arguments]         ${ip}

    ${del_result}=  XIQSE Delete Device                     ${ip}
    Should Be Equal As Integers                             ${del_result}      1

    ${confirm_result}=  XIQSE Wait Until Device Removed     ${ip}
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