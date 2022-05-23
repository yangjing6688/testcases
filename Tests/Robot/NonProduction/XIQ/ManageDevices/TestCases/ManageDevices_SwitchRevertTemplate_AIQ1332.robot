#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Heidi S. White
# Description   : Verifies the "Revert Device Template Defaults" functionality works as expected.
#                 This is qTest test case TC-7032 in the CSIT project.

*** Settings ***
Library          common/Cli.py
Library          xiq/flows/manage/Device360.py

Resource         ../../ManageDevices/Resources/AllResources.robot

Force Tags       testbed_1_node

Suite Setup      Log In and Set Up Test
Suite Teardown   Tear Down Test and Close Session


*** Variables ***
${XIQ_URL}              ${xiq.test_url}
${XIQ_USER}             ${xiq.tenant_username}
${XIQ_PASSWORD}         ${xiq.tenant_password}
${IQAGENT}              ${xiq.sw_connection_host}

${DUT_SERIAL}           ${aerohive_sw1.serial}
${DUT_MAC}              ${aerohive_sw1.mac}
${DUT_CONSOLE_IP}       ${aerohive_sw1.console_ip}
${DUT_CONSOLE_PORT}     ${aerohive_sw1.console_port}
${DUT_USERNAME}         ${aerohive_sw1.username}
${DUT_PASSWORD}         ${aerohive_sw1.password}
${DUT_PLATFORM}         ${aerohive_sw1.platform}
${DUT_MAKE}             ${aerohive_sw1.make}
${DUT_TEST_TEMPLATE}    ${aerohive_sw1.device_template}
${DUT_TEST_PORT}        ${aerohive_sw1.test_port}

${POLICY_NAME}          Automation_Policy
${SSID_NAME}            Auto_SSID
${DEFAULT_DEVICE_PWD}   Aerohive123
${LOCATION}             San Jose, building_01, floor_02


*** Test Cases ***
Test 1: Change Port Configuration
    [Documentation]     Changes the port configuration on the switch
    [Tags]              csit_tc_7032   aiq_1332    development    xiq    manage_devices    switch_revert    test1

    Navigate to Device360 Port Configuration and Confirm Success  ${DUT_MAC}

    ${port_enabled}=  Device360 Confirm Port Enabled              ${DUT_TEST_PORT}
    Should Be Equal As Integers                                   ${port_enabled}  1

    ${disable_result}=  Device360 Disable Port                    ${DUT_TEST_PORT}
    Should Be Equal As Integers                                   ${disable_result}  1

    Close Device360 Window
    Navigate to Device360 Port Configuration and Confirm Success  ${DUT_MAC}
    ${port_disabled}=  Device360 Confirm Port Disabled            ${DUT_TEST_PORT}
    Should Be Equal As Integers                                   ${port_disabled}  1

    [Teardown]  Close Device360 Window

Test 2: Revert Device to Template Defaults
    [Documentation]     Performs the 'Revert Device to Template Defaults' action
    [Tags]              csit_tc_7032   aiq_1332    development    xiq    manage_devices    switch_revert    test2

    ${result}=  Revert Device to Template  ${DUT_SERIAL}
    Should Be Equal As Integers            ${result}  1

Test 3: Confirm Port Configuration Was Reverted
    [Documentation]     Confirms the port configuration changes were reverted to template defaults
    [Tags]              csit_tc_7032   aiq_1332    development    xiq    manage_devices    switch_revert    test3

    Navigate to Device360 Port Configuration and Confirm Success  ${DUT_MAC}

    ${port_enabled}=  Device360 Confirm Port Enabled              ${DUT_TEST_PORT}
    Should Be Equal As Integers                                   ${port_enabled}  1

    [Teardown]  Close Device360 Window


*** Keywords ***
Log In and Set Up Test
    [Documentation]     Logs into XIQ and configures pre-requisites for the test

    Log Into XIQ and Confirm Success  ${XIQ_USER}  ${XIQ_PASSWORD}  ${XIQ_URL}

    Change Device Password and Confirm Success  ${DEFAULT_DEVICE_PWD}

    Configure iqagent for Aerohive Switch  ${DUT_CONSOLE_IP}  ${DUT_CONSOLE_PORT}  ${DUT_USERNAME}
    ...                                    ${DUT_PASSWORD}  ${IQAGENT}

    Create Open Express Policy With Switch Template and Confirm Success  ${POLICY_NAME}  ${SSID_NAME}  ${DUT_TEST_TEMPLATE}

    Onboard New Test Device       ${DUT_SERIAL}  ${DUT_MAKE}  ${LOCATION}
    Column Picker Select          MAC Address
    Confirm Device Serial Online  ${DUT_SERIAL}

    Assign Policy to Switch and Confirm Success  ${POLICY_NAME}  ${DUT_SERIAL}

Tear Down Test and Close Session
    [Documentation]     Cleans up the components created during the test and ends the test

    Navigate to Devices and Confirm Success
    Delete Device and Confirm Success  ${DUT_SERIAL}

    Delete Policy and Confirm Success  ${POLICY_NAME}
    Delete SSID and Confirm Success    ${SSID_NAME}

    Log Out of XIQ and Quit Browser

Navigate to Device360 Port Configuration and Confirm Success
    [Documentation]     Navigates to the Device360 view for the specified device and selects the Port Configuration tab
    [Arguments]         ${mac}

    Navigate to Device360 and Confirm Success  ${mac}
    Navigate to Port Configuration and Confirm Success

Navigate to Device360 and Confirm Success
    [Documentation]     Navigates to the Device360 view for the specified device and confirms the action was successful
    [Arguments]         ${mac}

    ${nav_result}=  Navigate to Device360 Page with MAC  ${mac}
    Should Be Equal As Integers  ${nav_result}  1

Navigate to Port Configuration and Confirm Success
    [Documentation]     Navigates to the Port Configuration tab of the Device360 view and confirms the action was successful

    ${nav_result}=  Device360 Navigate to Port Configuration
    Should Be Equal As Integers  ${nav_result}  1

Onboard New Test Device
    [Documentation]     Onboards the specified test device, deleting it first if it already exists
    [Arguments]         ${serial}  ${make}  ${location}

    Navigate to Devices and Confirm Success

    # If the device has already been onboarded, delete it first (this will return success if device does not exist)
    Delete Device and Confirm Success  ${serial}

    # Onboard the device and confirm it was onboarded successfully
    Onboard Device  ${serial}  ${make}  location=${location}
    Confirm Device Serial Present  ${serial}

Configure iqagent for Aerohive Switch
    [Documentation]     Configures the iqagent for the Aerohive switch
    [Arguments]         ${ip}  ${port}  ${user}  ${pwd}  ${iqagent}

    ${spawn}=  Open Spawn  ${ip}  ${port}  ${user}  ${pwd}  aerohive-switch

    ${conf_results}=  Send Commands  ${spawn}
    ...  enable, no hivemanager address, hivemanager address ${iqagent}, application stop hiveagent, application start hiveagent, exit
    Log To Console    Command results are ${conf_results}

    [Teardown]  Close Spawn  ${spawn}
