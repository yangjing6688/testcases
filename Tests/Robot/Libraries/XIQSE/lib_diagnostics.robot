#----------------------------------------------------------------------
# Copyright (C) 2021... 2021 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# This file contains keywords specific to the Diagnostics tab functionality.
#

*** Settings ***
Library     common/Screen.py
Library     xiqse/flows/admin/diagnostics/XIQSE_AdminDiagnostics.py
Library     xiqse/flows/common/XIQSE_CommonNavigator.py


*** Keywords ***
Navigate to Diagnostics and Confirm Success
    [Documentation]     Navigates to the Administration> Diagnostics page

    ${result}=  XIQSE Navigate to Admin Diagnostics Tab
    Should Be Equal As Integers  ${result}  1

Navigate to XIQ Device Message Details and Confirm Success
    [Documentation]     Navigates to the Administration> Diagnostics page amd selects XIQ Device Message Details

    Navigate to Diagnostics and Confirm Success
    ${result}=  XIQSE Select XIQ Device Message Details Tree Node
    Should Be Equal As Integers  ${result}  1

Navigate and Confirm XIQSE Onboarded Successfully
    [Documentation]     Confirms the XIQSE has a SUCCESS onboard status in the XIQ Device Message Details table
    [Arguments]         ${xiqse_ip}

    Navigate to XIQ Device Message Details and Confirm Success
    Confirm XIQSE Onboarded Successfully    ${xiqse_ip}

Enter XIQ Credentials to Auto Onboard XIQSE
    [Documentation]     Onboards the specified XIQ Site Engine using the Auto Onboard button
    [Arguments]         ${xiq_email}  ${xiq_pwd}

    Close All Banner Messages and Confirm Success

    ${onboard_result}=  XIQSE Auto Onboard XIQSE  ${xiq_email}  ${xiq_pwd}
    Should Be Equal As Integers         ${onboard_result}     1

Confirm Device Has Expected Onboard Status Using Refresh
    [Documentation]     Confirms the device has the expected onboard status in the XIQ Device Message Details table.
    ...                 This keyword uses the Refresh button to update the data which is sometimes failing, so a new
    ...                 keyword is being created to update the data performing navigation steps instead
    ...                 (the original name of "Confirm Device Has Expected Onboard Status").
    [Arguments]         ${ip}  ${type}  ${status}

    XIQSE XIQ Device Message Details Show Columns  Onboard Status  Onboard

    ${result}=  XIQSE Wait Until Device Has Expected Onboard Status  ${ip}  ${type}  ${status}
    Should Be Equal As Integers  ${result}  1

Confirm Device Has Expected Onboard Status
    [Documentation]     Confirms the device has the expected onboard status in the XIQ Device Message Details table
    [Arguments]         ${ip}  ${type}  ${status}

    XIQSE XIQ Device Message Details Show Columns  Onboard Status  Onboard

    Wait Until Keyword Succeeds  30x  10s
    ...  Confirm Device Has Expected Onboard Status Using Navigation  ${ip}  ${type}  ${status}

Confirm Device Has Expected Onboard Status Using Navigation
    [Documentation]     Confirms the device has the expected onboard status in the XIQ Device Message Details table
    ...                 using navigation (away from / back to the page) to force the data to update.  This is done
    ...                 instead of the refresh as sometimes the refresh was never completing, and causes failures.
    [Arguments]         ${ip}  ${type}  ${status}

    ${result}=  XIQSE Confirm Onboard Status  ${ip}  ${type}  ${status}
    Run Keyword If  '${result}' == '-1'  Refresh Device Message Details Using Navigation
    Should Be Equal As Integers  ${result}  1

Refresh Device Message Details Using Navigation
    [Documentation]     Performs a refresh of the Device Message Details view by navigating to the Server> Server Log
    ...                 view and then back to the System> ExtremeCloud IQ Device Message Details view.

    XIQSE Select Server Log Tree Node
    XIQSE Select XIQ Device Message Details Tree Node

Confirm XIQSE Has Expected Onboard Status
    [Documentation]     Confirms XIQSE has the expected onboard status in the XIQ Device Message Details table
    [Arguments]         ${xiqse_ip}  ${status}

    Confirm Device Has Expected Onboard Status  ${xiqse_ip}  XIQ_SE  ${status}

Confirm XIQSE Onboarded Successfully
    [Documentation]     Confirms the XIQSE has a SUCCESS onboard status in the XIQ Device Message Details table
    [Arguments]         ${xiqse_ip}

    Confirm XIQSE Has Expected Onboard Status  ${xiqse_ip}  SUCCESS

Onboard XIQSE if Not Onboarded
    [Documentation]     Onboards XIQSE to XIQ if it is not currently onboarded
    [Arguments]         ${xiqse_ip}  ${xiq_email}  ${xiq_pwd}

    XIQSE XIQ Device Message Details Show Columns  Onboard Status  Onboard

    ${result}=  XIQSE Onboard XIQSE if Not Onboarded  ${xiqse_ip}  ${xiq_email}  ${xiq_pwd}
    Should Be Equal As Integers  ${result}  1

Obtain Onboard Status Screenshot from Diagnostics
    [Documentation]     Navigates to the XIQ Device Message Details view, adds the Onboard Status columns, and obtains a screenshot

    Navigate to XIQ Device Message Details and Confirm Success
    XIQSE XIQ Device Message Details Show Columns  Onboard Status  Onboard
    Save Screen Shot
