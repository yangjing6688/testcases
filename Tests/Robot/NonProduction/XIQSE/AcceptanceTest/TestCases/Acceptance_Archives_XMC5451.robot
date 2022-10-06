#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : David Truesdell
# Description   : Test Suite for acceptance testing of basic XIQSE archives functionality.
#                 This is qTest TC-866 in the XIQSE project.

*** Settings ***
Library         xiqse/flows/network/devices/site/actions/XIQSE_NetworkDevicesSiteActions.py

Resource        ../../AcceptanceTest/Resources/AllResources.robot

Force Tags      testbed_1_node

Suite Setup      Log In and Set Up Test
Suite Teardown   Tear Down Test and Close Session

*** Variables ***
${XIQSE_URL}                ${xiqse.url}
${XIQSE_USERNAME}           ${xiqse.user}
${XIQSE_PASSWORD}           ${xiqse.password}
${XIQSE_IP_ADDRESS}         ${xiqse.ip}
${XIQSE_MAC}                ${xiqse.mac}
${INSTALL_MODE}             ${upgrades.install_mode}

${XIQ_URL}                  ${xiq.test_url}
${XIQ_EMAIL}                ${xiq.tenant_username}
${XIQ_PASSWORD}             ${xiq.tenant_password}

${DUT_IP}                   ${netelem1.ip}
${DUT_PROFILE}              ${netelem1.profile}

${WORLD_SITE}               World
${TEST_ARCHIVE}             AUTO_ARCHIVE
${OPS_PANEL_RETRIEVED}      AUTO_ARCHIVE - Configuration Retrieved
${OPS_PANEL_EQUAL}          AUTO_ARCHIVE - Configurations Are Equal


*** Test Cases ***
Test 1: Create Archive and Confirm Success
    [Documentation]     Confirms an archive can be created
    [Tags]              nightly1    tcxe_866    xmc_5451    development    xiqse    acceptance    archives    test1

    Navigate and Create Archive        ${TEST_ARCHIVE}    ${DUT_IP}

Test 2: Confirm Operations Panel Message - Retrieved
    [Documentation]     Confirms the operations panel contains the expected message
    [Tags]              nightly1    tcxe_866    xmc_5451    development    xiqse    acceptance    archives    test2

    Confirm Operations Panel Message For Type      Inventory Audit  ${OPS_PANEL_RETRIEVED}

Test 3: Confirm Events - Create Archive
    [Documentation]     Confirms the events view contains the expected event
    [Tags]              nightly1    tcxe_866    xmc_5451    development    xiqse    acceptance    archives    test3

    Navigate to Events and Confirm Success
    Set Event Time Range and Confirm Success        Last 30 Minutes
    Set Event Type and Confirm Success              Inventory
    Set Event Search String and Confirm Success     Archive Save
    Confirm Event Row Contains Text                 Archive Save AUTO_ARCHIVE
    Clear Event Search String and Confirm Success

Test 4: Stamp New Version and Confirm Success
    [Documentation]     Confirms stamp new version on existing archive can be created
    [Tags]              nightly1    tcxe_866    xmc_5451    development    xiqse    acceptance    archives    test4

    Navigage and Stamp New Version     ${TEST_ARCHIVE}

Test 5: Confirm Operations Panel Message - Equal
    [Documentation]     Confirms the operations panel contains the expected message
    [Tags]              nightly1    tcxe_866    xmc_5451    development    xiqse    acceptance    archives    test5

    Confirm Operations Panel Message For Type      Inventory Audit  ${OPS_PANEL_EQUAL}

Test 6: Confirm Events - Stamp New Version
    [Documentation]     Confirms the events view contains the expected event
    [Tags]              nightly1    tcxe_866    xmc_5451    development    xiqse    acceptance    archives    test6

    Navigate to Events and Confirm Success
    Set Event Search String and Confirm Success     Archive Save
    Confirm Event Row Contains Text                 Archive Save AUTO_ARCHIVE
    Clear Event Search String and Confirm Success

Test 7: Delete Archive and Confirm Success
    [Documentation]     Confirms an archive can be deleted
    [Tags]              nightly1    tcxe_866    xmc_5451    development    xiqse    acceptance    archives    test7

    Navigate and Delete Archive     ${TEST_ARCHIVE}


*** Keywords ***
Log In and Set Up Test
    [Documentation]     Logs in and configures everything that is required for the test to run

    Log Into XIQSE and Confirm Success                 ${XIQSE_USERNAME}    ${XIQSE_PASSWORD}    url=${XIQSE_URL}
    Handle License Agreement If Displayed              ${XIQ_EMAIL}  ${XIQ_PASSWORD}
    Close Panels on Login If Displayed
    Set Option Web Server Session Timeout and Confirm Success  7  day(s)
    Set Alarm Event Search Scope    true
    Set Option Device Tree Name Format and Confirm Success   IP Address
    Disable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver    ${WORLD_SITE}
    Onboard XIQSE To XIQ If In Connected Mode        ${INSTALL_MODE}  ${XIQSE_IP_ADDRESS}  ${XIQ_EMAIL}  ${XIQ_PASSWORD}
    Navigate and Create Device                       ${DUT_IP}  ${DUT_PROFILE}
    Clear Operations Panel and Confirm Success

Tear Down Test and Close Session
    [Documentation]     Logs in and cleans up all items that were set up for the test

    # Delete the test device
    Navigate to Devices and Confirm Success
    Delete Device and Confirm Success           ${DUT_IP}
    Restore Web Server Options to Default and Confirm Success
    Restore Site Engine General Options to Default and Confirm Success
    Set Alarm Event Search Scope    false
    Enable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver    ${WORLD_SITE}
    Log Out of XIQSE and Quit Browser
    Remove XIQSE From XIQ If In Connected Mode        ${INSTALL_MODE}  ${XIQ_EMAIL}  ${XIQ_PASSWORD}  ${XIQ_URL}  ${XIQSE_MAC}
