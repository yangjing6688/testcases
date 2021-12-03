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
