#----------------------------------------------------------------------
# Copyright (C) 2021... 2021 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# This file contains keywords specific to the basic login/logout functionality.
#

*** Settings ***
Library     xiqse/flows/common/XIQSE_CommonHelp.py
Library     xiqse/flows/common/XIQSE_CommonLogin.py


*** Keywords ***
Load XIQSE and Log In
    [Documentation]     Loads the specified XIQSE login URL, enters the user name and password, and clicks the LOGIN button
    [Arguments]         ${user}  ${pwd}  ${url}  ${check_creds}=True

    ${result}=  XIQSE Load Page and Log In  ${user}    ${pwd}    url=${url}    check_credentials=${check_creds}
    Should Be Equal As Integers             ${result}     1

    # Make sure the XIQSE version is set
    Get XIQSE Version

Log Into XIQSE and Confirm Success
    [Documentation]     Logs into XIQSE and confirms the action was successful
    [Arguments]         ${user}  ${pwd}  ${url}

    Load XIQSE and Log In    ${user}  ${pwd}  ${url}

Log Into XIQSE and Skip Credential Check
    [Documentation]     Logs into XIQSE and confirms the action was successful
    [Arguments]         ${user}  ${pwd}  ${url}

    Load XIQSE and Log In    ${user}  ${pwd}  ${url}  False

Log Into XIQSE and Close Panels
    [Documentation]     Logs into XIQSE and closes any banner messages and the help panel
    [Arguments]         ${user}  ${pwd}  ${url}

    Log Into XIQSE and Confirm Success  ${user}    ${pwd}    url=${url}
    Close Panels on Login and Confirm Success

Close Panels on Login and Confirm Success
    [Documentation]     Closes any Banner Messages seen upon login and closes the help panel - fails if panels are not present

    # Close any banner messages (Connection Lost with XIQ, License Expiration, etc.)
    Close All Banner Messages and Confirm Success

    # Close the Help panel if it is open
    ${result}=  XIQSE Close Help Panel
    Should Be Equal As Integers             ${result}     1

Close Panels on Login If Displayed
    [Documentation]     Closes any Banner Messages seen upon login and closes the help panel - does not check for success

    # Close any banner messages (Connection Lost with XIQ, License Expiration, etc.)
    XIQSE Close All Banner Messages

    # Close the Help panel if it is open
    XIQSE Close Help Panel

Log Out of XIQSE and Confirm Success
    [Documentation]     Logs out of XIQSE and confirms the action was successful

    ${result}=  XIQSE Logout User
    Should Be Equal As Integers     ${result}     1

Quit Browser and Confirm Success
    [Documentation]     Closes the browser and confirms the action was successful

    ${result}=  XIQSE Quit Browser
    Should Be Equal As Integers     ${result}     1

Log Out of XIQSE and Quit Browser
    [Documentation]     Logs out of XIQSE, confirms the action was successful, and closes the browser

    Log Out of XIQSE and Confirm Success
    Quit Browser and Confirm Success

Get XIQSE Version
    [Documentation]     Determines the XIQSE version and sets the suite variable

    ${version}=  XIQSE Get Version
    Set Suite Variable  ${XIQSE_OS_VERSION}  ${version}

Confirm User Is Logged Into XIQSE
    [Documentation]     Confirms the user is logged into XIQSE

    ${result}=  XIQSE Confirm User Logged In
    Should Be Equal As Integers     ${result}     1
