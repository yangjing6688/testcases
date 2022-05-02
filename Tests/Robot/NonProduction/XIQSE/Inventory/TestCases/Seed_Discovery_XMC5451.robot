#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : David Truesdell
# Description   : Test Suite for sanity testing of basic XIQSE sites seed discovery functionality.
#                 This is qTest TC-950 in the XIQ-SE project.

*** Settings ***
Library         xiqse/flows/network/devices/site/actions/XIQSE_NetworkDevicesSiteActions.py

Resource        ../../Inventory/Resources/AllResources.robot

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

${SEED_ADDRESS}             ${netelem1.ip}
${DISCOVER_PROFILE}         ${netelem1.profile}

${WORLD_SITE}               World
${TEST_SITE}                AutomationSite
${TEST_ARCHIVE}             /World/AutomationSite


*** Test Cases ***
Test 1: Discover Seed Address
    [Documentation]     Confirms a seed discovery can be performed
    [Tags]              nightly1    xiqse_tc_950    xmc_5451    development    xiqse    inventory    discovery    sites    test3

    Clear Operations Panel and Confirm Success
    Navigate to Site Tab and Confirm Success                    ${TEST_SITE}
    Perform Seed Discovery and Confirm Success                  ${SEED_ADDRESS}  ${DISCOVER_PROFILE}  auto_add=true  trap=false  syslog=false  archive=true
    Wait Until Device License Check Completes
    Wait Until Discover Site Actions Completes
    Clean Up Seed Discovery Settings and Confirm Success        ${SEED_ADDRESS}  ${DISCOVER_PROFILE}
    Save Site Changes and Confirm Success

Test 2: Navigate and Confirm IP Address Present in Devices Table
    [Documentation]     Confirms the specified IP address is present in the Devices table
    [Tags]              nightly1    xiqse_tc_950    xmc_5451    development    xiqse    inventory    discovery    sites    test4

    Navigate to Devices and Confirm Success
    Confirm IP Address Present in Devices Table    ${DUT_IP}

Test 3: Confirm Archive Exists In Tree
    [Documentation]     Confirms an archive exists in the Network> Archives tree in XIQ-SE and confirms the action was successful
    [Tags]              nightly1    xiqse_tc_950    xmc_5451    development    xiqse    inventory    discovery    sites    test5

    Navigate and Confirm Archive Exists In Tree     ${TEST_ARCHIVE}

Test 4: Confirm Events - Site Discovery
    [Documentation]     Confirms the events view contains the expected event
    [Tags]              nightly1    xiqse_tc_950    xmc_5451    development    xiqse    inventory    discovery    sites    test6

    Navigate to Events and Confirm Success
    Set Event Time Range and Confirm Success        Last 30 Minutes
    Set Event Type and Confirm Success              Console View,Inventory
    Set Event Search String and Confirm Success     ${DUT_IP}
    Confirm Event Row Contains Text                Device Discovery ${DUT_IP} - Operation Complete


*** Keywords ***
Log In and Set Up Test
    [Documentation]     Logs in and configures everything that is required for the test to run

    Log Into XIQSE and Close Panels                  ${XIQSE_USERNAME}    ${XIQSE_PASSWORD}    url=${XIQSE_URL}
    Set Option Web Server Session Timeout and Confirm Success  7  day(s)
    Set Option Device Tree Name Format and Confirm Success     IP Address
    Navigate and Create Site                         ${TEST_SITE}
    Select Site and Confirm Success                  ${TEST_SITE}
    Onboard XIQSE To XIQ If In Connected Mode        ${INSTALL_MODE}  ${XIQSE_IP_ADDRESS}  ${XIQ_EMAIL}  ${XIQ_PASSWORD}

Tear Down Test and Close Session
    [Documentation]     Logs in and cleans up all items that were set up for the test

    Restore Web Server Options to Default and Confirm Success
    Restore Site Engine General Options to Default and Confirm Success
    Navigate to Site Devices and Confirm Success        ${TEST_SITE}
    Delete All Devices and Confirm Success
    Navigate and Delete Site                            ${TEST_SITE}
    Navigate and Delete Archive                         ${TEST_ARCHIVE}
    Log Out of XIQSE and Quit Browser
    Remove XIQSE From XIQ If In Connected Mode          ${INSTALL_MODE}  ${XIQ_EMAIL}  ${XIQ_PASSWORD}  ${XIQ_URL}  ${XIQSE_MAC}

Wait Until Device License Check Completes
    [Documentation]     Checks operations panel and waits until the Device License Check operation completes

    ${wait_result}=  XIQSE Operations Wait Until Operation Complete    Device License Check
    Should Be Equal As Integers         ${wait_result}  1

Wait Until Discover Site Actions Completes
    [Documentation]     Checks operations panel and waits until the Discover Site Actions operation completes

    ${wait_result}=  XIQSE Operations Wait Until Operation Complete    Discover Site Actions    retry_duration=10    retry_count=60
    Should Be Equal As Integers         ${wait_result}  1
