#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Heidi S. White
# Description   : Test Suite for testing sorting functionality:
#                   - all devices real, filter by device type "Real", sort, clear filter, sort
#                   - all devices up, update, sort on "Updated" column
#                   - all devices up, update, one device down, sort on "Updated" column
#                   - one device down, update devices which are up, sort on "Updated" column
#                 This is qTest test cases TC-6857, TC-6808, TC-6923, and TC-6941 in the CSIT project.

*** Settings ***
Library          Collections
Library          common/Cli.py
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
${DUT1_CONSOLE_IP}      ${ap1.ip}
${DUT1_CONSOLE_PORT}    ${ap1.port}
${DUT1_USERNAME}        ${ap1.username}
${DUT1_PASSWORD}        ${ap1.password}
${DUT1_CLI_TYPE}        ${ap1.cli_type}
${DUT1_MAKE}            ${ap1.make}

${DUT2_SERIAL}          ${ap2.serial}
${DUT2_MAC}             ${ap2.mac}
${DUT2_CONSOLE_IP}      ${ap2.ip}
${DUT2_CONSOLE_PORT}    ${ap2.port}
${DUT2_USERNAME}        ${ap2.username}
${DUT2_PASSWORD}        ${ap2.password}
${DUT2_CLI_TYPE}        ${ap2.cli_type}
${DUT2_MAKE}            ${ap2.make}

${DUT3_SERIAL}          ${ap3.serial}
${DUT3_MAC}             ${ap3.mac}
${DUT3_CONSOLE_IP}      ${ap3.ip}
${DUT3_CONSOLE_PORT}    ${ap3.port}
${DUT3_USERNAME}        ${ap3.username}
${DUT3_PASSWORD}        ${ap3.password}
${DUT3_CLI_TYPE}        ${ap3.cli_type}
${DUT3_MAKE}            ${ap3.make}

${DUT4_SERIAL}          ${ap4.serial}
${DUT4_MAC}             ${ap4.mac}
${DUT4_CONSOLE_IP}      ${ap4.ip}
${DUT4_CONSOLE_PORT}    ${ap4.port}
${DUT4_USERNAME}        ${ap4.username}
${DUT4_PASSWORD}        ${ap4.password}
${DUT4_CLI_TYPE}        ${ap4.cli_type}
${DUT4_MAKE}            ${ap4.make}

${DEFAULT_DEVICE_PWD}   Aerohive123
${POLICY_NAME}          Auto_Policy_Sorting
${SSID_NAME}            Auto_SSID_Sorting
${LOCATION}             San Jose, building_01, floor_02


*** Test Cases ***
Test 1: Confirm Sorting On Management IP Address Column When Filter Changed (CFD-4243)
    [Documentation]     Confirms the devices are correctly sorted on the Management IP Address column when a filter is changed
    [Tags]              tccs_6857   cfd_4243    development    xiq    manage_devices    sorting    test1

    Refresh Devices Page

    # Filter to only show Real devices
    Open Filter Panel
    ${filtered_status}=  Set Device Type Filter  Real Devices  true
    Should Be Equal As Integers  ${filtered_status}  1
    Close Filter Panel

    # Perform the sort
    ${filtered_sort_items}=  Sort Device Grid With Mgmt IP Address   ascending
    Log List                 ${filtered_sort_items}

    # Remove the filter for Real Devices
    Refresh Devices Page
    Open Filter Panel
    ${unfiltered_status}=  Set Device Type Filter  Real Devices  false
    Should Be Equal As Integers  ${unfiltered_status}  1
    Close Filter Panel

    # Perform the sort
    Refresh Devices Page
    ${unfiltered_sort_items}=  Sort Device Grid With Mgmt IP Address   ascending
    Log List                   ${unfiltered_sort_items}

    # Since all devices are Real in this test, the sort on filtered vs unfiltered devices should be the same
    Lists Should Be Equal      ${filtered_sort_items}  ${unfiltered_sort_items}

Test 2: Confirm Sorting on Updated Column - All Devices Connected (CFD-4149 Case 1)
    [Documentation]     Confirms the devices are correctly sorted on the Updated column when all devices are connected
    [Tags]              tccs_6808   cfd_4149    development    xiq    manage_devices    sorting       test2

    # Update each of the devices
    Assign Policy to Device and Confirm Success     ${POLICY_NAME}  ${DUT1_SERIAL}
    Assign Policy to Device and Confirm Success     ${POLICY_NAME}  ${DUT2_SERIAL}
    Assign Policy to Device and Confirm Success     ${POLICY_NAME}  ${DUT3_SERIAL}
    Assign Policy to Device and Confirm Success     ${POLICY_NAME}  ${DUT4_SERIAL}

    # Perform the sort
    Refresh Devices Page
    ${sort_items}=  Sort Device Grid With Updated   ascending
    Log List        ${sort_items}

Test 3: Confirm Sorting on Updated Column - One Device Disconnected After Update (CFD-4149 Case 2)
    [Documentation]     Confirms the devices are correctly sorted on the Updated column even when one device is disconnected
    [Tags]              tccs_6923   cfd_4149    development    xiq    manage_devices    sorting       test3

    # Disconnect one of the devices
    Disconnect Device               ${DUT3_CONSOLE_IP}  ${DUT3_CONSOLE_PORT}  ${DUT3_USERNAME}
    ...                             ${DUT3_PASSWORD}  ${DUT3_CLI_TYPE}
    Confirm Device Serial Offline   ${DUT3_SERIAL}
    Confirm Device Serial Has Expected Status  ${DUT3_SERIAL}  disconnected

    # Perform the sort
    Refresh Devices Page
    ${sort_items}=  Sort Device Grid With Updated   ascending
    Log List        ${sort_items}

Test 4: Confirm Sorting on Updated Column - One Device Disconnected Before Update (CFD-4149 Case 3)
    [Documentation]     Confirms the devices are correctly sorted on the Updated column when the sort is applied while one device is diconnected
    [Tags]              tccs_6941   cfd_4149    development    xiq    manage_devices    sorting       test4

    Refresh Devices Page

    # The device should still be disconnected
    ${device_status}=  Get Device Status   device_serial=${DUT3_SERIAL}
    Run Keyword If   '${device_status}' != 'disconnected'  Log To Console  >>> DEVICE NOT DISCONNECTED <<<
    Run Keyword If   '${device_status}' != 'disconnected'
    ...               Disconnect Device  ${DUT3_CONSOLE_IP}  ${DUT3_CONSOLE_PORT}  ${DUT3_USERNAME}
    ...                                  ${DUT3_PASSWORD}  ${DUT3_CLI_TYPE}
    Run Keyword If   '${device_status}' != 'disconnected'  Confirm Device Serial Offline   ${DUT3_SERIAL}
    Confirm Device Serial Has Expected Status  ${DUT3_SERIAL}  disconnected

    # Perform an update on the devices which are still connected
    Assign Policy to Device and Confirm Success  ${POLICY_NAME}  ${DUT1_SERIAL}
    Assign Policy to Device and Confirm Success  ${POLICY_NAME}  ${DUT2_SERIAL}
    Assign Policy to Device and Confirm Success  ${POLICY_NAME}  ${DUT4_SERIAL}

    # Perform the sort
    Refresh Devices Page
    ${sort_items}=  Sort Device Grid With Updated   ascending
    Log List        ${sort_items}


*** Keywords ***
Log Into XIQ and Set Up Test
    [Documentation]     Logs into XIQ and sets up the elements necessary to complete this test suite

    Log Into XIQ and Confirm Success                ${XIQ_USER}  ${XIQ_PASSWORD}  ${XIQ_URL}
    Change Device Password and Confirm Success      ${DEFAULT_DEVICE_PWD}
    Onboard and Configure Test Devices
    Column Picker Select                            MGT IP Address  Updated On
    Create Open Express Policy and Confirm Success  ${POLICY_NAME}  ${SSID_NAME}
    Wait Until Test Devices Online

Tear Down Test and Close Session
    [Documentation]     Cleans up test data, logs out of XIQ, and closes the browser

    Clean Up Test Devices and Confirm Success

    # Clean up the Policy information
    Delete Policy and Confirm Success  ${POLICY_NAME}
    Delete SSID and Confirm Success    ${SSID_NAME}

    Log Out of XIQ and Quit Browser

Onboard and Configure Test Devices
    [Documentation]     Onboards the test devices

    Navigate to Devices and Confirm Success

    # Onboard the devices for the test
    ${dut1_result}=     Search Device   ${DUT1_SERIAL}
    ${dut2_result}=     Search Device   ${DUT2_SERIAL}
    ${dut3_result}=     Search Device   ${DUT3_SERIAL}
    ${dut4_result}=     Search Device   ${DUT4_SERIAL}
    Run Keyword If      '${dut1_result}' != '1'  onboard device quick    ${ap1}
    Run Keyword If      '${dut2_result}' != '1'  onboard device quick    ${ap2}
    Run Keyword If      '${dut3_result}' != '1'  onboard device quick    ${ap3}
    Run Keyword If      '${dut4_result}' != '1'  onboard device quick    ${ap4}

    # Confirm the devices were onboarded
    Confirm Device Serial Present  ${DUT1_SERIAL}
    Confirm Device Serial Present  ${DUT2_SERIAL}
    Confirm Device Serial Present  ${DUT3_SERIAL}
    Confirm Device Serial Present  ${DUT4_SERIAL}

    # Configure the devices
    ${dut1_status}=       Get Device Status       device_serial=${DUT1_SERIAL}
    ${dut2_status}=       Get Device Status       device_serial=${DUT2_SERIAL}
    ${dut3_status}=       Get Device Status       device_serial=${DUT3_SERIAL}
    ${dut4_status}=       Get Device Status       device_serial=${DUT4_SERIAL}
    Run Keyword If      '${dut1_status}' != 'green'
    ...      Configure CAPWAP Device To Connect To Cloud    ${DUT1_CLI_TYPE}  ${DUT1_CONSOLE_IP}  ${DUT1_CONSOLE_PORT}  ${DUT1_USERNAME}
    ...                                                     ${DUT1_PASSWORD}  ${XIQ_CAPWAP_URL}
    Run Keyword If      '${dut2_status}' != 'green'
    ...      Configure CAPWAP Device To Connect To Cloud    ${DUT2_CLI_TYPE}  ${DUT2_CONSOLE_IP}  ${DUT2_CONSOLE_PORT}  ${DUT2_USERNAME}
    ...                                                     ${DUT2_PASSWORD}  ${XIQ_CAPWAP_URL}
    Run Keyword If      '${dut3_status}' != 'green'
    ...      Configure CAPWAP Device To Connect To Cloud    ${DUT3_CLI_TYPE}  ${DUT3_CONSOLE_IP}  ${DUT3_CONSOLE_PORT}  ${DUT3_USERNAME}
    ...                                                     ${DUT3_PASSWORD}  ${XIQ_CAPWAP_URL}
    Run Keyword If      '${dut4_status}' != 'green'
    ...      Configure CAPWAP Device To Connect To Cloud    ${DUT4_CLI_TYPE}  ${DUT4_CONSOLE_IP}  ${DUT4_CONSOLE_PORT}  ${DUT4_USERNAME}
    ...                                                     ${DUT4_PASSWORD}  ${XIQ_CAPWAP_URL}

Wait Until Test Devices Online
    [Documentation]     Waits until all test devices have a connected status

    Confirm Device Serial Online  ${DUT1_SERIAL}
    Confirm Device Serial Online  ${DUT2_SERIAL}
    Confirm Device Serial Online  ${DUT3_SERIAL}
    Confirm Device Serial Online  ${DUT4_SERIAL}

Configure CAPWAP Device To Connect To Cloud
    [Documentation]     Configure the CAPWAP client with the necessary configuration on the Device to Connect to Cloud
    [Arguments]         ${cli_type}  ${ip}  ${port}  ${user}  ${pwd}  ${capwap_url}

    ${SPAWN_CONNECTION}=      Open Spawn        ${ip}  ${port}  ${user}  ${pwd}   ${cli_type}

    ${CONF_STATUS_RESULT}=      Configure Device To Connect To Cloud    ${cli_type}      ${capwap_url}     ${SPAWN_CONNECTION}
    Should Be Equal As Strings                  ${CONF_STATUS_RESULT}       1

    Close Spawn       ${SPAWN_CONNECTION}

Disconnect Device
    [Documentation]     Disconnects the device
    [Arguments]         ${ip}  ${port}  ${user}  ${pwd}  ${cli_type}

    ${spawn}=           Open Spawn  ${ip}  ${port}  ${user}  ${pwd}  ${cli_type}

    Send                ${spawn}   no capwap client enable
    Send                ${spawn}   save config

    Close Spawn         ${spawn}

Clean Up Test Devices and Confirm Success
    [Documentation]     Deletes the test devices and confirms the actions were successful

    Navigate to Devices and Confirm Success

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
