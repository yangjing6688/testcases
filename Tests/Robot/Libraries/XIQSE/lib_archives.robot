#----------------------------------------------------------------------
# Copyright (C) 2021... 2021 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# This file contains keywords specific to the basic Archives functionality.
#

*** Settings ***
Library     xiqse/flows/network/archives/XIQSE_NetworkArchives.py
Library     xiqse/flows/network/archives/XIQSE_NetworkArchivesCreateArchive.py
Library     xiqse/flows/common/XIQSE_CommonNavigator.py


*** Keywords ***
Navigate to Archives and Confirm Success
    [Documentation]     Navigates to the Network> Archives panel in XIQ-SE and confirms the action was successful
    [Arguments]

    ${nav_result}=  XIQSE Navigate to Network Archives Tab
    Should Be Equal As Integers         ${nav_result}     1

Navigate and Create Archive
    [Documentation]     Creates a new archive from the Network> Archives panel in XIQ-SE and confirms the action was successful
    [Arguments]         ${archive_name}    ${ip_list}    ${frequency}=${NONE}

    Navigate to Archives and Confirm Success
    Create Archive and Confirm Success          ${archive_name}    ${ip_list}    frequency=${frequency}

Create Archive and Confirm Success
    [Documentation]     Creates a new archive from the Network> Archives panel in XIQ-SE and confirms the action was successful
    [Arguments]         ${archive_name}    ${ip_list}    ${frequency}=${NONE}

    Clear Operations Panel and Confirm Success

    ${create_result}=  XIQSE Archives Create Archive    ${archive_name}    ${ip_list}    frequency=${frequency}
    Should Be Equal As Integers  ${create_result}  1

    ${wait_result}=  XIQSE Wait Until Archive Added     ${archive_name}
    Should Be Equal As Integers  ${wait_result}  1

    ${wait_result}=  XIQSE Wait Until Archive Complete
    Should Be Equal As Integers  ${wait_result}  1

    ${confirm_result}=  XIQSE Confirm Archive Exists    ${archive_name}
    Should Be Equal As Integers  ${confirm_result}  1

Navigage and Stamp New Version
    [Documentation]     Stamp New Version on existing archive from the Network> Archives panel in XIQ-SE and confirms the action was successful
    [Arguments]         ${archive_name}

    Navigate to Archives and Confirm Success
    Stamp New Version and Confirm Success       ${archive_name}

Stamp New Version and Confirm Success
    [Documentation]     Stamp New Version on existing archive from the Network> Archives panel in XIQ-SE and confirms the action was successful
    [Arguments]         ${archive_name}

    Clear Operations Panel and Confirm Success

    ${create_result}=  XIQSE Archives Stamp New Version     ${archive_name}
    Should Be Equal As Integers  ${create_result}  1

    ${wait_result}=  XIQSE Wait Until Archive Complete
    Should Be Equal As Integers  ${wait_result}  1

    ${confirm_result}=  XIQSE Confirm Archive Exists        ${archive_name}
    Should Be Equal As Integers  ${confirm_result}  1

Navigate and Delete Archive
    [Documentation]     Confirms an archive can be deleted from the Network> Archives panel in XIQ-SE and confirms the action was successful
    [Arguments]         ${archive_name}

    Navigate to Archives and Confirm Success
    Delete Archive and Confirm Success          ${archive_name}

Delete Archive and Confirm Success
    [Documentation]     Confirms an archive can be deleted from the Network> Archives panel in XIQ-SE and confirms the action was successful
    [Arguments]         ${archive_name}

    ${delete_result}=  XIQSE Archives Delete Archive    ${archive_name}
    # check for not -1 since if it was already deleted "2" will be returned
    Should Not Be Equal As Integers  ${delete_result}  -1

    ${wait_result}=  XIQSE Wait Until Archive Removed   ${archive_name}
    Should Be Equal As Integers  ${wait_result}  1

    ${confirm_result}=  XIQSE Confirm Archive Exists    ${archive_name}  false
    Should Be Equal As Integers  ${confirm_result}  1

Navigate and Create Backup Configuration
    [Documentation]     Creates a backup configuration archive from Network> Devices panel in XIQ-SE and confirms the action was successful
    [Arguments]         ${device_ip}

    Navigate to Devices and Confirm Success
    Create Backup Configuration and Confirm Success     ${device_ip}

Create Backup Configuration and Confirm Success
    [Documentation]     Creates a backup configuration archive from Network> Devices panel in XIQ-SE and confirms the action was successful
    [Arguments]         ${device_ip}

    Clear Operations Panel and Confirm Success
    XIQSE Device Select Backup Configuration    ${device_ip}

    ${archive_complete}=  XIQSE Wait Until Archive Complete
    Should Be Equal As Integers  ${archive_complete}  1

Navigate and Restore Configuration
    [Documentation]     Executes a restore configuration archive from Network> Devices panel in XIQ-SE and confirms the action was successful
    [Arguments]         ${device_ip}  ${archive_name}

    Navigate to Devices and Confirm Success
    Restore Configuration and Confirm Success   ${device_ip}  ${archive_name}

Restore Configuration and Confirm Success
    [Documentation]     Executes a restore configuration archive from Network> Devices panel in XIQ-SE and confirms the action was successful
    [Arguments]         ${device_ip}  ${archive_name}

    Clear Operations Panel and Confirm Success

    ${restore_complete}=  XIQSE Device Restore Configuration      ${device_ip}  ${archive_name}
    Should Be Equal As Integers  ${restore_complete}  1

    ${archive_complete}=  XIQSE Wait Until Restore Complete
    Should Be Equal As Integers  ${archive_complete}  1

Navigate and Confirm Archive Exists In Tree
    [Documentation]     Confirms an archive exists in the Network> Archives tree in XIQ-SE and confirms the action was successful
    [Arguments]         ${archive_name}

    Navigate to Archives and Confirm Success
    Confirm Archive Exists In Tree                      ${archive_name}

Confirm Archive Exists In Tree
    [Documentation]     Confirms an archive exists in the Network> Archives tree in XIQ-SE and confirms the action was successful
    [Arguments]         ${archive_name}

    ${confirm_result}=  XIQSE Confirm Archive Exists    ${archive_name}
    Should Be Equal As Integers  ${confirm_result}  1
