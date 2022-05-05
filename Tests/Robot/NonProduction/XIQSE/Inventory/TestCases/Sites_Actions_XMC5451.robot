#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : David Truesdell
# Description   : Test Suite for sanity testing of basic XIQSE sites actions functionality.
#                 This is qTest TC-949 in the XIQ-SE project.

*** Settings ***
#Library         xiqse/flows/network/devices/site/actions/XIQSE_NetworkDevicesSiteActions.py

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

${DISCOVER_IP_START}        ${netelem1.ip}
${DISCOVER_IP_END}          ${netelem1.ip}
${DISCOVER_PROFILE}         ${netelem1.profile}

${WORLD_SITE}               World
${TEST_SITE}                AutomationSite
${TEST_ARCHIVE}             /World/AutomationSite
${TRAP_REGISTERED}          Trap Receiver Registered
${TRAP_UNREGISTERED}        Trap Receiver Unregistered
${SYSLOG_REGISTERED}        Syslog Receiver Registered
${SYSLOG_UNREGISTERED}      Syslog Receiver Unregistered


*** Test Cases ***
Test 1: Perform Site Discovery with Auto Add Devices True
    [Documentation]     Sets Site Actions Automatically Add Devices to True and confirms device was automatically added to Devices table
    [Tags]              nightly1    xiqse_tc_949    xmc_5451    development    xiqse    acceptance    sites    discovery    add_actions    test1

    Clear Operations Panel and Confirm Success
    Navigate to Site Tab and Confirm Success            ${TEST_SITE}
    Perform IP Range Discovery and Confirm Success      ${DISCOVER_IP_START}  ${DISCOVER_IP_END}  ${DISCOVER_PROFILE}  auto_add=true  trap=false  syslog=false  archive=false
    Wait For Operations Panel Operation To Complete     Device License Check
    Wait For Operations Panel Operation To Complete     Discover Site Actions

    # Confirm device automatically added to Devices table
    Navigate to Site Devices and Confirm Success        ${TEST_SITE}
    Confirm IP Address Present in Devices Table         ${DUT_IP}

    # Confirm discovery event exists
    Navigate and Confirm Site Discovery Event

    # Delete device from Site Devices table
    Navigate to Site Devices and Confirm Success        ${TEST_SITE}
    Delete Device and Confirm Success                   ${DUT_IP}

Test 2: Perform Site Discovery with Auto Add Devices False
    [Documentation]     Sets Site Actions Automatically Add Devices to False and confirms device is in Discovered panel
    [Tags]              nightly1    xiqse_tc_949    xmc_5451    development    xiqse    acceptance    sites    discovery    add_actions    test2

    Clear Operations Panel and Confirm Success
    Navigate to Site Tab and Confirm Success            ${TEST_SITE}
    Perform IP Range Discovery and Confirm Success      ${DISCOVER_IP_START}  ${DISCOVER_IP_END}  ${DISCOVER_PROFILE}  auto_add=false  trap=false  syslog=false  archive=false
    Wait For Operations Panel Operation To Complete     Discover Site

    # Confirm device not automatically added to Devices table
    Navigate to Site Devices and Confirm Success        ${TEST_SITE}
    Confirm IP Address Not Present in Devices Table     ${DUT_IP}

    # Confirm device added to Discovered table
    Confirm IP Address Present in Discovered Table      ${DUT_IP}

    # Clear Device from Discovered table
    Navigate to Discovered and Confirm Success
    Clear IP From Discovered and Confirm Success        ${DUT_IP}

Test 3: Perform Site Discovery with Add to Archive True
    [Documentation]     Sets Site Actions Add to Archive to True and confirms archive exists in the Archives panel tree
    [Tags]              nightly1    xiqse_tc_949    xmc_5451    development    xiqse    acceptance    sites    discovery    add_actions    test3

    Clear Operations Panel and Confirm Success
    Navigate to Site Tab and Confirm Success            ${TEST_SITE}
    Perform IP Range Discovery and Confirm Success      ${DISCOVER_IP_START}  ${DISCOVER_IP_END}  ${DISCOVER_PROFILE}  auto_add=true  trap=false  syslog=false  archive=true
    Wait For Operations Panel Operation To Complete     Device License Check
    Wait For Operations Panel Operation To Complete     Discover Site Actions

    # Confirm device automatically added to Devices table
    Navigate to Site Devices and Confirm Success        ${TEST_SITE}
    Confirm IP Address Present in Devices Table         ${DUT_IP}

    # Confirm archive created in archives tree
    Navigate and Confirm Archive Exists In Tree         ${TEST_ARCHIVE}

    # Delete archive
    Delete Archive and Confirm Success                  ${TEST_ARCHIVE}

    # Delete device from Site Devices table
    Navigate to Site Devices and Confirm Success        ${TEST_SITE}
    Delete Device and Confirm Success                   ${DUT_IP}

Test 4: Perform Site Discovery with Add to Archive False
    [Documentation]     Sets Site Actions Add to Archive to False and confirms archive does not exist in the Archives panel tree
    [Tags]              nightly1    xiqse_tc_949    xmc_5451    development    xiqse    acceptance    sites    discovery    add_actions    test4

    Clear Operations Panel and Confirm Success
    Navigate to Site Tab and Confirm Success                ${TEST_SITE}
    Perform IP Range Discovery and Confirm Success          ${DISCOVER_IP_START}  ${DISCOVER_IP_END}  ${DISCOVER_PROFILE}  auto_add=true  trap=false  syslog=false  archive=false
    Wait For Operations Panel Operation To Complete         Device License Check
    Wait For Operations Panel Operation To Complete         Discover Site Actions

    # Confirm device automatically added to Devices table
    Navigate to Site Devices and Confirm Success            ${TEST_SITE}
    Confirm IP Address Present in Devices Table             ${DUT_IP}

    # Confirm archive was not created in Archives tree
    Navigate and Confirm Archive Does Not Exist In Tree     ${TEST_ARCHIVE}

    # Delete device from Site Devices table
    Navigate to Site Devices and Confirm Success            ${TEST_SITE}
    Delete Device and Confirm Success                       ${DUT_IP}

Test 5: Perform Site Discovery with Add Trap Receiver True
    [Documentation]     Sets Site Actions Add Trap Receiver to True and confirms the device is registered as a trap receiver
    [Tags]              nightly1    xiqse_tc_949    xmc_5451    development    xiqse    acceptance    sites    discovery    add_actions    test5

    Clear Operations Panel and Confirm Success
    Navigate to Site Tab and Confirm Success                ${TEST_SITE}
    Perform IP Range Discovery and Confirm Success          ${DISCOVER_IP_START}  ${DISCOVER_IP_END}  ${DISCOVER_PROFILE}  auto_add=true  trap=true  syslog=false  archive=false
    Wait For Operations Panel Operation To Complete         Device License Check
    Wait For Operations Panel Operation To Complete         Discover Site Actions
    Wait For Operations Panel Operation To Complete         Trap Configuration

    # Confirm device automatically added to Devices table
    Navigate to Site Devices and Confirm Success            ${TEST_SITE}
    Confirm IP Address Present in Devices Table             ${DUT_IP}

    # Confirm trap status column shows registered
    Navigate and Confirm Trap Status                        ${DUT_IP}    ${TRAP_REGISTERED}

    # Unregister trap receiver on device
    Clear Operations Panel and Confirm Success
    Navigate and Unregister Trap Receiver                   ${DUT_IP}

    # Confirm trap status column shows unregistered
    Navigate and Confirm Trap Status                        ${DUT_IP}    ${TRAP_UNREGISTERED}

    # Delete device from Site Devices table
    Navigate to Site Devices and Confirm Success            ${TEST_SITE}
    Delete Device and Confirm Success                       ${DUT_IP}

Test 6: Perform Site Discovery with Add Trap Receiver False
    [Documentation]     Sets Site Actions Add Trap Receiver to False and confirms the device is not registered as a trap receiver
    [Tags]              nightly1    xiqse_tc_949    xmc_5451    development    xiqse    acceptance    sites    discovery    add_actions    test6

    Clear Operations Panel and Confirm Success
    Navigate to Site Tab and Confirm Success                ${TEST_SITE}
    Perform IP Range Discovery and Confirm Success          ${DISCOVER_IP_START}  ${DISCOVER_IP_END}  ${DISCOVER_PROFILE}  auto_add=true  trap=false  syslog=false  archive=false
    Wait For Operations Panel Operation To Complete         Device License Check
    Wait For Operations Panel Operation To Complete         Discover Site Actions

    # Confirm device automatically added to Devices table
    Navigate to Site Devices and Confirm Success            ${TEST_SITE}
    Confirm IP Address Present in Devices Table             ${DUT_IP}

    # Confirm trap status column shows unregistered
    Navigate and Confirm Trap Status                        ${DUT_IP}    ${TRAP_UNREGISTERED}

    # Delete device from Site Devices table
    Navigate to Site Devices and Confirm Success            ${TEST_SITE}
    Delete Device and Confirm Success                       ${DUT_IP}

Test 7: Perform Site Discovery with Add Syslog Receiver True
    [Documentation]     Sets Site Actions Add Syslog Receiver to True and confirms the device is registered as a syslog receiver
    [Tags]              nightly1    xiqse_tc_949    xmc_5451    development    xiqse    acceptance    sites    discovery    add_actions    test7

    Clear Operations Panel and Confirm Success
    Navigate to Site Tab and Confirm Success                ${TEST_SITE}
    Perform IP Range Discovery and Confirm Success          ${DISCOVER_IP_START}  ${DISCOVER_IP_END}  ${DISCOVER_PROFILE}  auto_add=true  trap=false  syslog=true  archive=false
    Wait For Operations Panel Operation To Complete         Device License Check
    Wait For Operations Panel Operation To Complete         Discover Site Actions
    Wait For Operations Panel Operation To Complete         Syslog Configuration

    # Confirm device automatically added to Devices table
    Navigate to Site Devices and Confirm Success            ${TEST_SITE}
    Confirm IP Address Present in Devices Table             ${DUT_IP}

    # Confirm syslog status column shows registered
    Navigate and Confirm Syslog Status                      ${DUT_IP}    ${SYSLOG_REGISTERED}

    # Unregister syslog receiver on device
    Clear Operations Panel and Confirm Success
    Navigate and Unregister Syslog Receiver                 ${DUT_IP}

    # Confirm syslog status column shows unregistered
    Navigate and Confirm Syslog Status                      ${DUT_IP}    ${SYSLOG_UNREGISTERED}

    # Delete device from Site Devices table
    Navigate to Site Devices and Confirm Success            ${TEST_SITE}
    Delete Device and Confirm Success                       ${DUT_IP}

Test 8: Perform Site Discovery with Add Syslog Receiver False
    [Documentation]     Sets Site Actions Add Syslog Receiver to False and confirms the device is not registered as a syslog receiver
    [Tags]              nightly1    xiqse_tc_949    xmc_5451    development    xiqse    acceptance    sites    discovery    add_actions    test8

    Clear Operations Panel and Confirm Success
    Navigate to Site Tab and Confirm Success                ${TEST_SITE}
    Perform IP Range Discovery and Confirm Success          ${DISCOVER_IP_START}  ${DISCOVER_IP_END}  ${DISCOVER_PROFILE}  auto_add=true  trap=false  syslog=false  archive=false
    Wait For Operations Panel Operation To Complete         Device License Check
    Wait For Operations Panel Operation To Complete         Discover Site Actions

    # Confirm device automatically added to Devices table
    Navigate to Site Devices and Confirm Success            ${TEST_SITE}
    Confirm IP Address Present in Devices Table             ${DUT_IP}

    # Confirm syslog status column shows unregistered
    Navigate and Confirm Syslog Status                      ${DUT_IP}    ${SYSLOG_UNREGISTERED}

    # Delete device from Site Devices table
    Navigate to Site Devices and Confirm Success            ${TEST_SITE}
    Delete Device and Confirm Success                       ${DUT_IP}


*** Keywords ***
Log In and Set Up Test
    [Documentation]     Logs in and configures everything that is required for the test to run

    Log Into XIQSE and Confirm Success                 ${XIQSE_USERNAME}    ${XIQSE_PASSWORD}    url=${XIQSE_URL}
    Handle License Agreement If Displayed              ${XIQ_EMAIL}  ${XIQ_PASSWORD}
    Close Panels on Login If Displayed
    Set Option Web Server Session Timeout and Confirm Success  7  day(s)
    Set Option Device Tree Name Format and Confirm Success     IP Address
    Navigate and Create Site                         ${TEST_SITE}
    Select Site and Confirm Success                  ${TEST_SITE}
    Onboard XIQSE To XIQ If In Connected Mode        ${INSTALL_MODE}  ${XIQSE_IP_ADDRESS}  ${XIQ_EMAIL}  ${XIQ_PASSWORD}

Tear Down Test and Close Session
    [Documentation]     Logs in and cleans up all items that were set up for the test

    Restore Web Server Options to Default and Confirm Success
    Restore Site Engine General Options to Default and Confirm Success
    Navigate to Site Devices and Confirm Success                ${TEST_SITE}
    Navigate and Delete Site                                    ${TEST_SITE}
    Log Out of XIQSE and Quit Browser
    Remove XIQSE From XIQ If In Connected Mode                  ${INSTALL_MODE}  ${XIQ_EMAIL}  ${XIQ_PASSWORD}  ${XIQ_URL}  ${XIQSE_MAC}

Navigate and Confirm Site Discovery Event
    [Documentation]     Confirms the events view contains the expected discovery event

    Navigate to Events and Confirm Success
    Set Event Time Range and Confirm Success        Last 30 Minutes
    Set Event Type and Confirm Success              Console View,Inventory
    Set Event Search String and Confirm Success     ${DUT_IP}
    Confirm Event Row Contains Text                 Device Discovery ${DUT_IP} - Operation Complete
