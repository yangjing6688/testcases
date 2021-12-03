#----------------------------------------------------------------------
# Copyright (C) 2021... 2021 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# This file contains keywords specific to the basic Profiles functionality.
#

*** Settings ***
Library     xiqse/flows/admin/profiles/XIQSE_AdminProfiles.py
Library     xiqse/flows/common/XIQSE_CommonNavigator.py


*** Keywords ***
Navigate to Profiles and Confirm Success
    [Documentation]   Navigates to the Administration> Profiles view in XIQ-SE and confirms success

    ${nav_result}=  XIQSE Navigate to Admin Profiles Tab
    Should Be Equal As Integers    ${nav_result}     1

Navigate and Create Profile
    [Documentation]   Navigates to the view and creates a profile, confirming the action was successful
    [Arguments]       ${name}  ${version}="SNMPv1"  ${read}=${None}  ${write}=${None}  ${max}=${None}  ${cli}=${None}
    ...               ${read_sec}=${None}  ${write_sec}=${None}  ${max_sec}=${None}

    Navigate to Profiles and Confirm Success
    Create Profile and Confirm Success  ${name}  ${version}  ${read}  ${write}  ${max}  ${cli}
    ...                                 ${read_sec}  ${write_sec}  ${max_sec}

Navigate and Edit Profile
    [Documentation]   Navigates to the view and edits a profile, confirming the action was successful
    [Arguments]       ${name}  ${read}=${None}  ${write}=${None}  ${max}=${None}  ${cli}=${None}

    Navigate to Profiles and Confirm Success
    Edit Profile and Confirm Success  ${name}  ${read}  ${write}  ${max}  ${cli}

Navigate and Delete Profile
    [Documentation]     Navigates to the view and deletes a profile, confirming the action was successful
    [Arguments]         ${name}

    Navigate to Profiles and Confirm Success
    Delete Profile and Confirm Success  ${name}

Create Profile and Confirm Success
    [Documentation]   Creates a profile and confirms the action was successful
    [Arguments]       ${name}  ${version}="SNMPv1"  ${read}=${None}  ${write}=${None}  ${max}=${None}  ${cli}=${None}
    ...               ${read_sec}=${None}  ${write_sec}=${None}  ${max_sec}=${None}

    ${result}=  XIQSE Create Profile  ${name}  ${version}  ${read}  ${write}  ${max}  ${cli}
    ...                               ${read_sec}  ${write_sec}  ${max_sec}
    Should Be Equal As Integers       ${result}     1

    Confirm Profile Exists            ${name}

Edit Profile and Confirm Success
    [Documentation]   Edits a profile and confirms the action was successful
    [Arguments]       ${name}  ${read}=${None}  ${write}=${None}  ${max}=${None}  ${cli}=${None}

    ${result}=  XIQSE Edit Profile  ${name}  ${read}  ${write}  ${max}  ${cli}
    Should Be Equal As Integers     ${result}     1

Confirm Profile Exists
    [Documentation]   Confirms the specified profile is present in the view
    [Arguments]       ${name}

    ${result}=  XIQSE Find Profile   ${name}
    Should Be Equal As Integers      ${result}    1

Confirm Profile Does Not Exist
    [Documentation]   Confirms the specified profile is not present in the view
    [Arguments]       ${name}

    ${result}=  XIQSE Find Profile  ${name}
    Should Be Equal As Integers     ${result}    -1

Delete Profile and Confirm Success
    [Documentation]     Deletes the specified profile and confirms the action was successful
    [Arguments]         ${name}

    ${result}=  XIQSE Delete Profile    ${name}
    Should Be Equal As Integers         ${result}     1

    Confirm Profile Does Not Exist      ${name}
