#----------------------------------------------------------------------
# Copyright (C) 2021... 2021 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# This file contains keywords specific to the basic SNMP Credentials functionality.
#

*** Settings ***
Library     xiqse/flows/admin/profiles/XIQSE_AdminProfiles.py
Library     xiqse/flows/admin/profiles/snmp_credentials/XIQSE_AdminProfilesSNMPCredentials.py
Library     xiqse/flows/common/XIQSE_CommonNavigator.py


*** Keywords ***
Navigate to SNMP Credentials and Confirm Success
    [Documentation]   Navigates to the Administration> Profiles> SNMP Credentials view in XIQ-SE and confirms success

    ${nav_result}=  XIQSE Navigate to Admin Profiles Tab
    Should Be Equal As Integers    ${nav_result}     1

    ${tab_result}=  XIQSE Profiles Select SNMP Credentials Tab
    Should Be Equal As Integers    ${tab_result}     1

Navigate and Create SNMP Credential
    [Documentation]   Navigates to the view and creates an SNMPv2 credential, confirming the action was successful
    [Arguments]       ${name}  ${version}  ${comm}

    Navigate to SNMP Credentials and Confirm Success
    Create SNMP Credential and Confirm Success  ${name}  ${version}  ${comm}

Navigate and Create SNMPv1 Credential
    [Documentation]   Navigates to the view and creates an SNMPv2 credential, confirming the action was successful
    [Arguments]       ${name}  ${comm}

    Navigate and Create SNMP Credential  ${name}  SNMPv1  ${comm}

Navigate and Create SNMPv2 Credential
    [Documentation]   Navigates to the view and creates an SNMPv2 credential, confirming the action was successful
    [Arguments]       ${name}  ${comm}

    Navigate and Create SNMP Credential  ${name}  SNMPv2  ${comm}

Navigate and Delete SNMP Credential
    [Documentation]     Navigates to the view and deletes an SNMP credential, confirming the action was successful
    [Arguments]         ${name}

    Navigate to SNMP Credentials and Confirm Success
    Delete SNMP Credential and Confirm Success  ${name}

Create SNMP Credential and Confirm Success
    [Documentation]   Creates an SNMP credential and confirms the action was successful
    [Arguments]       ${name}  ${version}  ${comm}

    ${add_result}=  XIQSE Create SNMP Credential  ${name}  ${version}  ${comm}
    Should Be Equal As Integers                   ${add_result}     1

    Confirm SNMP Credential Exists  ${name}

Create SNMPv1 Credential and Confirm Success
    [Documentation]   Creates an SNMPv1 credential and confirms the action was successful
    [Arguments]       ${name}  ${comm}

    Create SNMP Credential and Confirm Success  ${name}  SNMPv1  ${comm}

Create SNMPv2 Credential and Confirm Success
    [Documentation]   Creates an SNMPv2 credential and confirms the action was successful
    [Arguments]       ${name}  ${comm}

    Create SNMP Credential and Confirm Success  ${name}  SNMPv2  ${comm}

Confirm SNMP Credential Exists
    [Documentation]   Confirms the specified SNMP credential is present in the view
    [Arguments]       ${name}

    ${result}=  XIQSE Find SNMP Credential  ${name}
    Should Be Equal As Integers             ${result}    1

Confirm SNMP Credential Does Not Exist
    [Documentation]   Confirms the specified SNMP credential is not present in the view
    [Arguments]       ${name}

    ${result}=  XIQSE Find SNMP Credential  ${name}
    Should Be Equal As Integers             ${result}    -1

Delete SNMP Credential and Confirm Success
    [Documentation]     Deletes the specified SNMP credential and confirms the action was successful
    [Arguments]         ${name}

    ${result}=  XIQSE Delete SNMP Credential    ${name}
    Should Be Equal As Integers                 ${result}     1

    Confirm SNMP Credential Does Not Exist      ${name}
