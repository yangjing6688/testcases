#----------------------------------------------------------------------
# Copyright (C) 2021... 2021 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# This file contains keywords specific to the basic login/logout functionality.
#

*** Settings ***
Library     xiq/flows/common/Login.py


*** Keywords ***
Log Into XIQ and Confirm Success
    [Documentation]     Logs into XIQ and confirms the action was successful
    [Arguments]         ${user}  ${pwd}  ${url}

    ${result}=  Login User          ${user}  ${pwd}  url=${url}
    Should Be Equal As Integers     ${result}     1

Log Into XIQ with Incognito Mode and Confirm Success
    [Documentation]     Logs into XIQ with incognito mode and confirms the login was successful
    [Arguments]         ${user}  ${pwd}  ${url}

    ${result}=      Login User      ${user}  ${pwd}  url=${url}  incognito_mode=True
    Should Be Equal As Integers     ${result}     1

Log Out of XIQ and Confirm Success
    [Documentation]     Logs out of XIQ and confirms the action was successful

    ${result}=  Logout User
    Should Be Equal As Integers     ${result}     1

Quit Browser and Confirm Success
    [Documentation]     Closes the browser and confirms the action was successful

    ${result}=  Quit Browser
    Should Be Equal As Integers     ${result}     1

Log Out of XIQ and Quit Browser
    [Documentation]     Logs out of XIQ, confirms the action was successful, and closes the browser

    Log Out of XIQ and Confirm Success
    Quit Browser and Confirm Success
