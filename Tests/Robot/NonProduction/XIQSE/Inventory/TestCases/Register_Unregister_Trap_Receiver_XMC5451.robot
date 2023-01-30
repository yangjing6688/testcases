#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : David Truesdell
# Description   : Test Suite for sanity testing of basic XIQSE register trap receiver functionality.
#                 This is qTest TC-874 in the XIQ-SE project.

*** Settings ***
Library     xiqse/flows/network/devices/site/actions/XIQSE_NetworkDevicesSiteActions.py

Resource    ../../Inventory/Resources/AllResources.robot

Force Tags      testbed_1_node

Suite Setup      Log In and Set Up Test
Suite Teardown   Tear Down Test and Close Session

*** Variables ***
${XIQSE_USERNAME}           ${xiqse.user}
${XIQSE_PASSWORD}           ${xiqse.password}
${XIQSE_IP_ADDRESS}         ${xiqse.ip}
${XIQSE_MAC}                ${xiqse.mac}
${XIQSE_URL}                ${xiqse.url}
${INSTALL_MODE}             ${upgrades.install_mode}

${XIQ_URL}                  ${xiq.test_url}
${XIQ_EMAIL}                ${xiq.tenant_username}
${XIQ_PASSWORD}             ${xiq.tenant_password}

${DUT_IP}                   ${netelem1.ip}
${DUT_PROFILE}              ${netelem1.profile}

${WORLD_SITE}               World
${SITE_ENGINE_ARCHIVE}      Site Engine Archive

*** Test Cases ***
Test 1: Register Trap Receiver
    [Documentation]     Confirms register trap receiver is successful
    [Tags]              nightly1    tcxe_874    xmc_5451    development    xiqse    acceptance    inventory    traps    test1    nightly4

    Clear Operations Panel and Confirm Success
    Navigate and Register Trap Receiver          ${DUT_IP}

Test 2: Verify Register Trap Receiver Completes
    [Documentation]     Checks the operations panel and waits for the register trap receiver to complete
    [Tags]              nightly1    tcxe_874    xmc_5451    development    xiqse    acceptance    inventory    traps    test2    nightly4

    Verify Register Trap Receiver Completes    Trap Configuration

Test 3: Create Backup After Register and Confirm Success
    [Documentation]     Creates a backup configuration on selected device
    [Tags]              nightly1    tcxe_874    xmc_5451    development    xiqse    acceptance    inventory    traps    test3    nightly4

    Log To Console  >> THIS IS FUTURE TEST SECTION TO BACKUP CONFIGURATION
#    Clear Operations Panel and Confirm Success
#    Create Backup Configuration and Confirm Success     ${DUT_IP}

Test 4: Check Backup Configuration For Trap Receiver Entries Added
    [Documentation]     Confirms the device configuration includes entries for register trap receiver
    [Tags]              nightly1    tcxe_874    xmc_5451    development    xiqse    acceptance    inventory    traps    test4    nightly4

    Log To Console  >> THIS IS FUTURE TEST SECTION TO CHECK CONFIGURATION FILE TO VERIFY TRAP ENTRIES ADDED

Test 5: Unregister Trap Receiver
    [Documentation]     Confirms unregister trap receiver is successful
    [Tags]              nightly1    tcxe_874    xmc_5451    development    xiqse    acceptance    inventory    traps    test5    nightly4

    Clear Operations Panel and Confirm Success
    Navigate and Unregister Trap Receiver            ${DUT_IP}

Test 6: Verify Unregister Trap Receiver Completes
    [Documentation]     Checks the operations panel and waits for the unregister trap receiver to complete
    [Tags]              nightly1    tcxe_874    xmc_5451    development    xiqse    acceptance    inventory    trap receiver    test6    nightly4

    Verify Unregister Trap Receiver Completes    Trap Configuration

Test 7: Create Backup After Unregister and Confirm Success
    [Documentation]     Creates a backup configuration on selected device
    [Tags]              nightly1    tcxe_874    xmc_5451    development    xiqse    acceptance    inventory    traps    test7    nightly4

    Log To Console  >> THIS IS FUTURE TEST SECTION TO BACKUP CONFIGURATION
#    Clear Operations Panel and Confirm Success
#    Create Backup Configuration and Confirm Success     ${DUT_IP}

Test 8: Check Backup Configuration To Verify Trap Receiver Entries Removed
    [Documentation]     Confirms the device configuration no longer includes entries for register trap receiver
    [Tags]              nightly1    tcxe_874    xmc_5451    development    xiqse    acceptance    inventory    trap receiver    test8    nightly4

    Log To Console  >> THIS IS FUTURE TEST SECTION TO CHECK CONFIGURATION FILE TO VERIFY TRAP ENTRIES REMOVED

Test 9: Delete Archive
    [Documentation]     Confirms an archive can be deleted
    [Tags]              nightly1    tcxe_874    xmc_5451    development    xiqse    acceptance    inventory    traps    test9    nightly4

    Log To Console  >> THIS IS FUTURE TEST SECTION TO DELETE BACKUP CONFIGURATION
#    Navigate and Delete Archive and Confirm Success     ${SITE_ENGINE_ARCHIVE}


*** Keywords ***
Log In and Set Up Test
    [Documentation]     Logs in and configures everything that is required for the test to run

    Log Into XIQSE and Confirm Success                 ${XIQSE_USERNAME}    ${XIQSE_PASSWORD}    url=${XIQSE_URL}
    Handle License Agreement If Displayed              ${XIQ_EMAIL}  ${XIQ_PASSWORD}
    Close Panels on Login If Displayed
    Set Option Web Server Session Timeout and Confirm Success  7  day(s)
    Set Alarm Event Search Scope    true
    Set Option Device Tree Name Format and Confirm Success     IP Address
    Disable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver    ${WORLD_SITE}
    Onboard XIQSE To XIQ If In Connected Mode        ${INSTALL_MODE}  ${XIQSE_IP_ADDRESS}  ${XIQ_EMAIL}  ${XIQ_PASSWORD}
    Navigate and Create Device                       ${DUT_IP}  ${DUT_PROFILE}

Tear Down Test and Close Session
    [Documentation]     Logs in and cleans up all items that were set up for the test

    Navigate to Devices and Confirm Success
    Delete Device and Confirm Success             ${DUT_IP}
    Restore Web Server Options to Default and Confirm Success
    Restore Site Engine General Options to Default and Confirm Success
    Set Alarm Event Search Scope    false
    Enable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver    ${WORLD_SITE}
    Log Out of XIQSE and Quit Browser
    Remove XIQSE From XIQ If In Connected Mode    ${INSTALL_MODE}  ${XIQ_EMAIL}  ${XIQ_PASSWORD}  ${XIQ_URL}  ${XIQSE_MAC}

Verify Register Trap Receiver Completes
    [Documentation]     Checks the operations panel and waits for the register trap receiver to complete
    [Arguments]         ${operation}

    ${wait_result}=  XIQSE Operations Wait Until Operation Complete    ${operation}
    Should Be Equal As Integers         ${wait_result}  1

Verify Unregister Trap Receiver Completes
    [Documentation]     Checks the operations panel and waits for the unregister trap receiver to complete
    [Arguments]         ${operation}

    ${wait_result}=  XIQSE Operations Wait Until Operation Complete    ${operation}
    Should Be Equal As Integers         ${wait_result}  1
