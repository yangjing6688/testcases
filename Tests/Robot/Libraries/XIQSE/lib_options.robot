#----------------------------------------------------------------------
# Copyright (C) 2021... 2021 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# This file contains keywords specific to the basic Options tab functionality.
#

*** Settings ***
Library     xiqse/flows/admin/options/XIQSE_AdminOptions.py
Library     xiqse/flows/common/XIQSE_CommonNavigator.py


*** Keywords ***
Navigate to Options and Confirm Success
    [Documentation]     Navigates to the Administration> Options view in XIQ-SE and confirms the action was successful

    ${nav_result}=  XIQSE Navigate to Admin Options Tab
    Should Be Equal As Integers         ${nav_result}     1

Set Alarm Event Search Scope
    [Documentation]     Configures the Alarm/Event Event Search Scope to include Client/Event/Source Host Name columns
    [Arguments]         ${value}

    XIQSE Set Event Search Scope And Save    ${value}

Set Syslog Delay Engine Start and Confirm Success
    [Documentation]     Configures the syslog delay engine start option, saves the change, and confirms the action was successful
    [Arguments]         ${value}

    ${result}=  XIQSE Set Syslog Delay Engine Start and Save   ${value}
    Should Be Equal As Integers     ${result}     1

Set Trap Delay Engine Start and Confirm Success
    [Documentation]     Configures the trap delay engine start option, saves the change, and confirms the action was successful
    [Arguments]         ${value}

    ${result}=  XIQSE Set Trap Delay Engine Start and Save   ${value}
    Should Be Equal As Integers     ${result}     1

Set Option Web Server Session Timeout and Confirm Success
    [Documentation]     Configures the HTTP Session Timeout option, saves the change, and confirms the action was successful
    [Arguments]         ${value}  ${units}

    ${result}=  XIQSE Set Web Server Session Timeout and Save   ${value}  ${units}
    Should Be Equal As Integers     ${result}     1

Set Option Device Tree Name Format and Confirm Success
    [Documentation]     Configures the Device Tree Name Format option, saves the change, and confirms the action was successful
    [Arguments]         ${value}

    ${result}=  XIQSE Set Device Tree Name Format and Save   ${value}
    Should Be Equal As Integers     ${result}     1

Restore Web Server Options to Default and Confirm Success
    [Documentation]     Restores the default value for the HTTP Session Timeout option, saves the change, and confirms the action was successful

    ${result_ws}=  XIQSE Restore Default Web Server Options and Save
    Should Be Equal As Integers    ${result_ws}     1

Restore Site Engine General Options to Default and Confirm Success
    [Documentation]     Restores the default value for the Device Tree Name Format option, saves the change, and confirms the action was successful

    ${result_seg}=  XIQSE Restore Default Site Engine General Options and Save
    Should Be Equal As Integers    ${result_seg}     1

Disable XIQ Connection Sharing and Confirm Success
    [Documentation]     Disables the ExtremeCloud IQ Connection: Enable Sharing option, saves the change, and confirms the action was successful

    ${result}=  XIQSE Disable XIQ Connection Sharing and Save
    Should Be Equal As Integers         ${result}     1

Enable XIQ Connection Sharing and Confirm Success
    [Documentation]     Disables the ExtremeCloud IQ Connection: Enable Sharing option, saves the change, and confirms the action was successful

    ${result}=  XIQSE Enable XIQ Connection Sharing and Save
    Should Be Equal As Integers         ${result}     1

Confirm XIQ Connection Sharing Enabled
    [Documentation]     Confirms the ExtremeCloud IQ Connection: Enable Sharing option is currently enabled

    Navigate to Options and Confirm Success
    XIQSE Select XIQ Connection Option

    ${result}=  XIQSE Confirm XIQ Connection Enable Sharing Option  true
    Should Be Equal As Integers         ${result}     1

Confirm XIQ Connection Sharing Disabled
    [Documentation]     Confirms the ExtremeCloud IQ Connection: Enable Sharing option is currently disabled

    Navigate to Options and Confirm Success
    XIQSE Select XIQ Connection Option

    ${result}=  XIQSE Confirm XIQ Connection Enable Sharing Option  false
    Should Be Equal As Integers         ${result}     1

Confirm XIQSE Serial Number
    [Documentation]     Confirms the serial number displayed on the Options tab for XIQSE is what is expected
    [Arguments]         ${expected_value}

    ${serial}=  Get XIQSE Serial Number
    Should Be Equal As Strings  ${serial}  ${expected_value}


Navigate and Select Inventory Manager Option
    [Documentation]     Navigates and selects the Administration> Options> Inventory Manager view in XIQ-SE and confirms the action was successful

    Navigate to Options and Confirm Success
    Select Inventory Manager Option and Confirm Success

Select Inventory Manager Option and Confirm Success
    [Documentation]     Selects the Administration> Options> Inventory Manager view in XIQ-SE and confirms the action was successful

    ${result}=  XIQSE Select Inventory Manager Option
    Should Be Equal As Integers     ${result}     1

Set Option SCP Login Information Anonymous and Confirm Success
    [Documentation]     Configures the SCP Anonymous checkbox and confirms the action was successful
    [Arguments]         ${value}

    ${result}=  XIQSE Set SCP Login Information Anonymous    ${value}
    Should Be Equal As Integers     ${result}     1

Set Option SFTP Login Information Anonymous and Confirm Success
    [Documentation]     Configures the SFTP Anonymous checkbox and confirms the action was successful
    [Arguments]         ${value}

    ${result}=  XIQSE Set SFTP Login Information Anonymous    ${value}
    Should Be Equal As Integers     ${result}     1

Navigate and Set Option SCP Login Information Anonymous and Confirm Success
    [Documentation]     Navigates and configures the SCP Anonymous checkbox and confirms the action was successful
    [Arguments]         ${value}

    Navigate and Select Inventory Manager Option
    Set Option SCP Login Information Anonymous and Confirm Success    ${value}

Navigate and Set Option SFTP Login Information Anonymous and Confirm Success
    [Documentation]     Navigates and configures the SFTP Anonymous checkbox and confirms the action was successful
    [Arguments]         ${value}

    Navigate and Select Inventory Manager Option
    Set Option SFTP Login Information Anonymous and Confirm Success    ${value}

Set Option SCP Username and Password Login Information and Confirm Success
    [Documentation]     Configures the SCP Username and Password, saves the change, and confirms the action was successful
    [Arguments]         ${username}  ${password}

    ${result}=  XIQSE Set SCP Login Information Username    ${username}
    Should Be Equal As Integers     ${result}     1

    ${result}=  XIQSE Set SCP Login Information Password    ${password}
    Should Be Equal As Integers     ${result}     1

    Save Options and Confirm Success

Set Option SFTP Username and Password Login Information and Confirm Success
    [Documentation]     Configures the SFTP Username and Password, saves the change, and confirms the action was successful
    [Arguments]         ${username}  ${password}

    ${result}=  XIQSE Set SFTP Login Information Username    ${username}
    Should Be Equal As Integers     ${result}     1

    ${result}=  XIQSE Set SFTP Login Information Password    ${password}
    Should Be Equal As Integers     ${result}     1

    Save Options and Confirm Success

Navigate and Set Option SCP Username and Password Login Information and Confirm Success
    [Documentation]     Navigates and configures the SCP Username and Password, saves the change, and confirms the action was successful
    [Arguments]         ${username}  ${password}

    Navigate and Select Inventory Manager Option
    Set Option SCP Username and Password Login Information and Confirm Success
    Save Options and Confirm Success

Navigate and Set Option SFTP Username and Password Login Information and Confirm Success
    [Documentation]     Navigates and configures the SFTP Username and Password, saves the change, and confirms the action was successful
    [Arguments]         ${username}  ${password}

    XIQSE Navigate To Admin Options Tab
    XIQSE Select Inventory Manager Option

    ${result}=  XIQSE Set SFTP Login Information Username    ${value}
    Should Be Equal As Integers     ${result}     1

    ${result}=  XIQSE Set SFTP Login Information Password    ${value}
    Should Be Equal As Integers     ${result}     1

    Save Options and Confirm Success

Save Options and Confirm Success
    [Documentation]  Clicks Save on the selected tab to save the changes

    ${save_result}=  XIQSE Save Options
    Should Be Equal As Integers      ${save_result}    1

Set Option Status Polling Group 2 Interval and Save
    [Documentation]     Configures the Group 2 Interval option, saves the change, and confirms the action was successful
    [Arguments]         ${value}

    ${result}=  XIQSE Set Status Polling Group 2 Interval Value   ${value}
    Should Be Equal As Integers     ${result}     1

    Save Options and Confirm Success

Navigate and Select Status Polling Option
    [Documentation]     Navigates and selects the Administration> Options> Status Polling view and confirms the action was successful

    Navigate to Options and Confirm Success
    Select Status Polling Option and Confirm Success

Select Status Polling Option and Confirm Success
    [Documentation]     Selects the Administration> Options> Status Polling view and confirms the action was successful

    ${result}=  XIQSE Select Status Polling Option
    Should Be Equal As Integers     ${result}     1

Navigate and Set Option Status Polling Group 2 Interval and Confirm Success
    [Documentation]     Navigates and sets the Group 2 Interval option, saves the change, and confirms the action was successful
    [Arguments]         ${value}

    Navigate and Select Status Polling Option
    Set Option Status Polling Group 2 Interval and Save    ${value}

Restore Status Polling Options to Default and Confirm Success
    [Documentation]     Restores the default value for the Status Polling option, saves the change, and confirms the action was successful

    ${result}=  XIQSE Restore Default Status Polling Options and Save
    Should Be Equal As Integers    ${result}     1

Restore Default Inventory Manager Options and Confirm Success
    [Documentation]      Restores the default value for the Inventory Manager option, saves the change, and confirms the action was successful

    ${result}=  XIQSE Restore Default Inventory Manager Options and Save
    Should Be Equal As Integers    ${result}     1
