#----------------------------------------------------------------------
# Copyright (C) 2021... 2021 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# This file contains keywords specific to the basic CLI Credentials functionality.
#

*** Settings ***
Library     xiqse/flows/admin/profiles/XIQSE_AdminProfiles.py
Library     xiqse/flows/admin/profiles/cli_credentials/XIQSE_AdminProfilesCLICredentials.py
Library     xiqse/flows/common/XIQSE_CommonNavigator.py


*** Keywords ***
Navigate to CLI Credentials and Confirm Success
    [Documentation]   Navigates to the Administration> Profiles> CLI Credentials view in XIQ-SE and confirms success

    ${nav_result}=  XIQSE Navigate to Admin Profiles Tab
    Should Be Equal As Integers    ${nav_result}     1

    ${tab_result}=  XIQSE Profiles Select CLI Credentials Tab
    Should Be Equal As Integers    ${tab_result}     1

Navigate and Create CLI Credential
    [Documentation]   Navigates to the view and creates a CLI credential, confirming the action was successful
    [Arguments]       ${desc}  ${user}  ${type}=Telnet  ${login_pwd}=${None}  ${enable_pwd}=${None}  ${config_pwd}=${None}

    Navigate to CLI Credentials and Confirm Success
    Create CLI Credential and Confirm Success  ${desc}  ${user}  ${type}  ${login_pwd}  ${enable_pwd}  ${config_pwd}

Navigate and Delete CLI Credential
    [Documentation]     Navigates to the view and deletes a CLI credential, confirming the action was successful
    [Arguments]         ${desc}

    Navigate to CLI Credentials and Confirm Success
    Delete CLI Credential and Confirm Success  ${desc}

Create CLI Credential and Confirm Success
    [Documentation]   Creates a CLI credential and confirms the action was successful
    [Arguments]       ${desc}  ${user}  ${type}=Telnet  ${login_pwd}=${None}  ${enable_pwd}=${None}  ${config_pwd}=${None}

    ${result}=  XIQSE Create CLI Credential  ${desc}  ${user}  ${type}  ${login_pwd}  ${enable_pwd}  ${config_pwd}
    Should Be Equal As Integers              ${result}     1

    Confirm CLI Credential Exists            ${desc}

Confirm CLI Credential Exists
    [Documentation]   Confirms the specified CLI credential is present in the view
    [Arguments]       ${desc}

    ${result}=  XIQSE Find CLI Credential   ${desc}
    Should Be Equal As Integers             ${result}    1

Confirm CLI Credential Does Not Exist
    [Documentation]   Confirms the specified CLI credential is not present in the view
    [Arguments]       ${desc}

    ${result}=  XIQSE Find CLI Credential   ${desc}
    Should Be Equal As Integers             ${result}    -1

Delete CLI Credential and Confirm Success
    [Documentation]     Deletes the specified CLI credential and confirms the action was successful
    [Arguments]         ${desc}

    ${result}=  XIQSE Delete CLI Credential     ${desc}
    Should Be Equal As Integers                 ${result}     1

    Confirm CLI Credential Does Not Exist       ${desc}
