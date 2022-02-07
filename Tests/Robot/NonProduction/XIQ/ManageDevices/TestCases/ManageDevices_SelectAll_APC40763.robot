#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Heidi S. White
# Description   : Test Suite for testing select all functionality:
#                   -- all devices are selected when Select All button is clicked
#                   -- Device360 link works when all devices are selected
#                 This is qTest test case TC-7587 in the CSIT project.

*** Settings ***
Library          Collections
Library          common/Cli.py
Library          xiq/flows/common/DeviceCommon.py
Library          xiq/flows/manage/Device360.py
Library          xiq/flows/manage/FilterManageDevices.py

Resource         ../../ManageDevices/Resources/AllResources.robot

Force Tags       testbed_4_node

Suite Setup      Log Into XIQ and Set Up Test
Suite Teardown   Tear Down Test and Close Session


*** Variables ***
${XIQ_URL}              ${xiq.test_url}
${XIQ_USER}             ${xiq.tenant_username}
${XIQ_PASSWORD}         ${xiq.tenant_password}
${XIQ_CAPWAP_URL}       ${xiq.capwap_url}

${DUT1_SERIAL}          ${ap1.serial}
${DUT1_MAC}             ${ap1.mac}
${DUT1_CONSOLE_IP}      ${ap1.console_ip}
${DUT1_CONSOLE_PORT}    ${ap1.console_port}
${DUT1_USERNAME}        ${ap1.username}
${DUT1_PASSWORD}        ${ap1.password}
${DUT1_PLATFORM}        ${ap1.platform}
${DUT1_MAKE}            ${ap1.make}

${DUT2_SERIAL}          ${ap2.serial}
${DUT2_MAC}             ${ap2.mac}
${DUT2_CONSOLE_IP}      ${ap2.console_ip}
${DUT2_CONSOLE_PORT}    ${ap2.console_port}
${DUT2_USERNAME}        ${ap2.username}
${DUT2_PASSWORD}        ${ap2.password}
${DUT2_PLATFORM}        ${ap2.platform}
${DUT2_MAKE}            ${ap2.make}

${DUT3_SERIAL}          ${ap3.serial}
${DUT3_MAC}             ${ap3.mac}
${DUT3_CONSOLE_IP}      ${ap3.console_ip}
${DUT3_CONSOLE_PORT}    ${ap3.console_port}
${DUT3_USERNAME}        ${ap3.username}
${DUT3_PASSWORD}        ${ap3.password}
${DUT3_PLATFORM}        ${ap3.platform}
${DUT3_MAKE}            ${ap3.make}

${DUT4_SERIAL}          ${ap4.serial}
${DUT4_MAC}             ${ap4.mac}
${DUT4_CONSOLE_IP}      ${ap4.console_ip}
${DUT4_CONSOLE_PORT}    ${ap4.console_port}
${DUT4_USERNAME}        ${ap4.username}
${DUT4_PASSWORD}        ${ap4.password}
${DUT4_PLATFORM}        ${ap4.platform}
${DUT4_MAKE}            ${ap4.make}

${DEFAULT_DEVICE_PWD}   Aerohive123
${POLICY_NAME}          Auto_Policy_SelectAll
${SSID_NAME}            Auto_SSID_SelectAll
${LOCATION}             San Jose, building_01, floor_02


*** Test Cases ***
Test 1: Confirm Select All Action Works As Expected
    [Documentation]     Confirms the select all action selects all devices, and deselect all action deselects all devices
    [Tags]              csit_tc_7587   apc_40763    development    xiq    manage_devices    select_all    test1

    # Perform the select all action
    ${action}=  Select All Devices
    Should Be Equal As Integers  ${action}  1

    # Confirm all devices are selected
    sleep  2 seconds
    ${sel_result1}=  Confirm Devices Selected  ${DUT1_SERIAL}  ${DUT2_SERIAL}  ${DUT3_SERIAL}  ${DUT4_SERIAL}
    Should Be Equal As Integers  ${sel_result1}  1
    ${sel_result2}=  Confirm All Devices Selected
    Should Be Equal As Integers  ${sel_result2}  1

    # Confirm all devices can be deselected
    ${desel_result1}=  Deselect All Devices
    Should Be Equal As Integers  ${desel_result1}  1
    sleep  2 seconds
    ${desel_result}=  Confirm All Devices Deselected
    Should Be Equal As Integers  ${desel_result}  1

Test 2: Confirm Device360 Link Works When All Devices Selected
    [Documentation]     Confirms the Device360 view is accessible when all devices are selected
    [Tags]              csit_tc_7587   apc_40763    development    xiq    manage_devices    select_all    test2

    # Confirm the Device360 view is accessible for each of the devices when all devices are selected
    Refresh Devices Page
    Select All Devices
    sleep  2 seconds
    ${nav_1}=  Go To Device360 Window  device_mac=${DUT1_MAC}
    Close Device360 Window

    Refresh Devices Page
    Select All Devices
    sleep  1 second
    ${nav_2}=  Go To Device360 Window  device_mac=${DUT2_MAC}
    Close Device360 Window

    Refresh Devices Page
    Select All Devices
    sleep  1 second
    ${nav_3}=  Go To Device360 Window  device_mac=${DUT3_MAC}
    Close Device360 Window

    Refresh Devices Page
    Select All Devices
    sleep  1 second
    ${nav_4}=  Go To Device360 Window  device_mac=${DUT4_MAC}
    Close Device360 Window

    Should Be Equal As Integers  ${nav_1}  1
    Should Be Equal As Integers  ${nav_2}  1
    Should Be Equal As Integers  ${nav_3}  1
    Should Be Equal As Integers  ${nav_4}  1


*** Keywords ***
Log Into XIQ and Set Up Test
    [Documentation]     Logs into XIQ and sets up the elements necessary to complete this test suite

    Log Into XIQ and Confirm Success                ${XIQ_USER}  ${XIQ_PASSWORD}  ${XIQ_URL}
    Change Device Password and Confirm Success      ${DEFAULT_DEVICE_PWD}
    Onboard and Configure Test Devices
    Create Open Express Policy and Confirm Success  ${POLICY_NAME}  ${SSID_NAME}
    Wait Until Test Devices Online

    # Assign a policy to and update each of the devices except one
    Assign Policy to Device and Confirm Success     ${POLICY_NAME}  ${DUT2_SERIAL}
    Assign Policy to Device and Confirm Success     ${POLICY_NAME}  ${DUT3_SERIAL}
    Assign Policy to Device and Confirm Success     ${POLICY_NAME}  ${DUT4_SERIAL}

Tear Down Test and Close Session
    [Documentation]     Cleans up test data, logs out of XIQ, and closes the browser

    # Clean up the devices
    Delete Device and Confirm Success  ${DUT1_SERIAL}
    Delete Device and Confirm Success  ${DUT2_SERIAL}
    Delete Device and Confirm Success  ${DUT3_SERIAL}
    Delete Device and Confirm Success  ${DUT4_SERIAL}

    # Confirm the devices were deleted
    Confirm Device Serial Not Present  ${DUT1_SERIAL}
    Confirm Device Serial Not Present  ${DUT2_SERIAL}
    Confirm Device Serial Not Present  ${DUT3_SERIAL}
    Confirm Device Serial Not Present  ${DUT4_SERIAL}

    # Clean up the Policy information
    Delete Policy and Confirm Success  ${POLICY_NAME}
    Delete SSID and Confirm Success    ${SSID_NAME}

    Log Out of XIQ and Quit Browser

Configure CAPWAP
    [Documentation]     Configures the CAPWAP client
    [Arguments]         ${ip}  ${port}  ${user}  ${pwd}  ${platform}

    ${spawn}=           Open Spawn  ${ip}  ${port}  ${user}  ${pwd}  ${platform}

    Send                ${spawn}   capwap client server name ${XIQ_CAPWAP_URL}
    Send                ${spawn}   capwap client default-server-name ${XIQ_CAPWAP_URL}
    Send                ${spawn}   capwap client server backup name ${XIQ_CAPWAP_URL}
    Send                ${spawn}   no capwap client enable
    Send                ${spawn}   capwap client enable
    Send                ${spawn}   save config
    Close Spawn         ${spawn}

Onboard and Configure Test Devices
    [Documentation]     Onboards the test devices

    Navigate to Devices and Confirm Success

    # Onboard the devices for the test
    Onboard Device      ${DUT1_SERIAL}  ${DUT1_MAKE}  location=${LOCATION}
    Onboard Device      ${DUT2_SERIAL}  ${DUT2_MAKE}  location=${LOCATION}
    Onboard Device      ${DUT3_SERIAL}  ${DUT3_MAKE}  location=${LOCATION}
    Onboard Device      ${DUT4_SERIAL}  ${DUT4_MAKE}  location=${LOCATION}

    # Confirm the devices were onboarded
    Confirm Device Serial Present  ${DUT1_SERIAL}
    Confirm Device Serial Present  ${DUT2_SERIAL}
    Confirm Device Serial Present  ${DUT3_SERIAL}
    Confirm Device Serial Present  ${DUT4_SERIAL}

    # Configure the devices
    Configure CAPWAP    ${DUT1_CONSOLE_IP}  ${DUT1_CONSOLE_PORT}  ${DUT1_USERNAME}
    ...                 ${DUT1_PASSWORD}  ${DUT1_PLATFORM}
    Configure CAPWAP    ${DUT2_CONSOLE_IP}  ${DUT2_CONSOLE_PORT}  ${DUT2_USERNAME}
    ...                 ${DUT2_PASSWORD}  ${DUT2_PLATFORM}
    Configure CAPWAP    ${DUT3_CONSOLE_IP}  ${DUT3_CONSOLE_PORT}  ${DUT3_USERNAME}
    ...                 ${DUT3_PASSWORD}  ${DUT3_PLATFORM}
    Configure CAPWAP    ${DUT4_CONSOLE_IP}  ${DUT4_CONSOLE_PORT}  ${DUT4_USERNAME}
    ...                 ${DUT4_PASSWORD}  ${DUT4_PLATFORM}

Wait Until Test Devices Online
    [Documentation]     Waits until all test devices have a connected status

    Confirm Device Serial Online  ${DUT1_SERIAL}
    Confirm Device Serial Online  ${DUT2_SERIAL}
    Confirm Device Serial Online  ${DUT3_SERIAL}
    Confirm Device Serial Online  ${DUT4_SERIAL}
