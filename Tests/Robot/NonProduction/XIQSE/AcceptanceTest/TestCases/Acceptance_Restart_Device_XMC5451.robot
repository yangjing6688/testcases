#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : David Truesdell
# Description   : Test Suite for sanity testing of restart device functionality in XIQSE.
#                 This is qTest TC-876 in the XIQ-SE project.

*** Settings ***
Library         xiqse/flows/network/devices/site/actions/XIQSE_NetworkDevicesSiteActions.py
Library         xiqse/flows/network/devices/devices/XIQSE_NetworkDevicesDevicesRestartDevice.py

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
${OPS_PANEL_RESTART}        Device Restart - Operation Complete


*** Test Cases ***
Test 1: Restart Switch
    [Documentation]     Restarts the switch
    [Tags]              csit_tc_876    xmc_5451    development    xiqse    acceptance    restart    test1

    Clear Operations Panel and Confirm Success
    XIQSE Select Device   ${DUT_IP}
    XIQSE Restart Device  ${DUT_IP}
    XIQSE Click Start Restart Button
    XIQSE Click Start Restart Yes Button
    XIQSE Click Restart Devices Close Button

Test 2: Confirm Events
    [Documentation]     Confirms the events view contains the expected event
    [Tags]              csit_tc_876    xmc_5451    development    xiqse    acceptance    restart    test6

    Navigate to Events and Confirm Success
    Set Event Time Range and Confirm Success        Last 30 Minutes
    Set Event Type and Confirm Success              Inventory
    Set Event Search String and Confirm Success     Device Restart

    Confirm Event Row Contains Text                 Device Restart Timed Reset: ${DUT_IP} - Operation Complete
    Clear Event Search String and Confirm Success

Test 3: Verify Device Is Up After Restart
    [Documentation]     Confirms device status is up after restart
    [Tags]              csit_tc_876    xmc_5451    development    xiqse    acceptance    restart    test3

    Navigate to Devices and Confirm Success
    Confirm Device Status Up     ${DUT_IP}


*** Keywords ***
Log In and Set Up Test
    [Documentation]     Logs in and configures everything that is required for the test to run

    Log Into XIQSE and Close Panels                  ${XIQSE_USERNAME}    ${XIQSE_PASSWORD}    url=${XIQSE_URL}
    Set Option Web Server Session Timeout and Confirm Success  7  day(s)
    Set Option Device Tree Name Format and Confirm Success     IP Address
    Disable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver    ${WORLD_SITE}
    Onboard XIQSE To XIQ If In Connected Mode        ${INSTALL_MODE}  ${XIQSE_IP_ADDRESS}  ${XIQ_EMAIL}  ${XIQ_PASSWORD}
    Navigate and Create Device                       ${DUT_IP}  ${DUT_PROFILE}
    Clear Operations Panel and Confirm Success

Tear Down Test and Close Session
    [Documentation]     Logs in and cleans up all items that were set up for the test

    Navigate to Devices and Confirm Success
    Delete Device and Confirm Success             ${DUT_IP}
    Restore Option Web Server Session Timeout To Default and Confirm Success
    Restore Option Device Tree Name Format To Default and Confirm Success
    Enable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver    ${WORLD_SITE}
    Log Out of XIQSE and Quit Browser
    Remove XIQSE From XIQ If In Connected Mode    ${INSTALL_MODE}  ${XIQ_EMAIL}  ${XIQ_PASSWORD}  ${XIQ_URL}  ${XIQSE_MAC}

Disable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver
    [Documentation]     In the Sites Actions tab, uncheck the boxes for Add Trap Receiver & Add Syslog Receiver
    [Arguments]         ${site}

    Navigate to Site Tab and Confirm Success    ${site}

    ${actions_result}=  XIQSE Site Select Actions Tab
    Should Be Equal As Integers         ${actions_result}     1

    XIQSE Actions Set Add Trap Receiver         false
    XIQSE Actions Set Add Syslog Receiver       false
    XIQSE Actions Set Add To Archive            false
    Save Site Changes

Enable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver
    [Documentation]     In the Sites Actions tab, check the boxes for Add Trap Receiver & Add Syslog Receiver
    [Arguments]         ${site}

    Navigate to Site Tab and Confirm Success    ${site}

    ${actions_result}=  XIQSE Site Select Actions Tab
    Should Be Equal As Integers         ${actions_result}     1

    XIQSE Actions Set Add Trap Receiver         true
    XIQSE Actions Set Add Syslog Receiver       true
    XIQSE Actions Set Add To Archive            true
    Save Site Changes

Restore Option Web Server Session Timeout To Default and Confirm Success
    [Documentation]     Restores the default value for the HTTP Session Timeout option, saves the change, and confirms the action was successful

    ${result_ws}=  XIQSE Restore Default Web Server Options and Save
    Should Be Equal As Integers    ${result_ws}     1

Restore Option Device Tree Name Format To Default and Confirm Success
    [Documentation]     Restores the default value for the Device Tree Name Format option, saves the change, and confirms the action was successful

    ${result_seg}=  XIQSE Restore Default Site Engine General Options and Save
    Should Be Equal As Integers    ${result_seg}     1