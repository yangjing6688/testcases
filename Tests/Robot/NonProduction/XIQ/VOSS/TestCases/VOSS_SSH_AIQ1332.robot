#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Heidi S. White
# Description   : Test Suite for testing SSH functionality of the VOSS switch.
#                 This is qTest test case TC-8553 in the CSIT project.

*** Settings ***
Library          Collections
Library          common/TestFlow.py
Library          common/Utils.py
Library          xiq/flows/manage/Device360.py
Library          xiq/flows/manage/Tools.py

Resource         ../../VOSS/Resources/AllResources.robot

Force Tags       testbed_voss_node

Suite Setup      Log Into XIQ and Set Up Test
Suite Teardown   Tear Down Test and Close Session


*** Variables ***
${XIQ_URL}                  ${xiq.test_url}
${XIQ_USER}                 ${xiq.tenant_username}
${XIQ_PASSWORD}             ${xiq.tenant_password}
${IQAGENT}                  ${xiq.sw_connection_host}

${DUT_SERIAL}               ${netelem3.serial}
${DUT_MAC}                  ${netelem3.mac}
${DUT_NAME}                 ${netelem3.name}
${DUT_TEMPLATE}             ${netelem3.template}
${DUT_CONSOLE_IP}           ${netelem3.console_ip}
${DUT_CONSOLE_PORT}         ${netelem3.console_port}
${DUT_USERNAME}             ${netelem3.username}
${DUT_PASSWORD}             ${netelem3.password}
${DUT_PLATFORM}             ${netelem3.platform}

${DEFAULT_DEVICE_PWD}       Aerohive123
${SSH_TIMER}                5
${STATUS_AFTER_UPDATE}      green
${LOCATION}                 auto_location_01, Santa Clara, building_02, floor_04
${POLICY_NAME}              VOSS_POLICY_AUTO
${SSID_NAME}                VOSS_SSID_AUTO


*** Test Cases ***
Test 1: Enable SSH on VOSS Switch and Confirm SSH Session Can Be Established
    [Documentation]     Enables SSH for the VOSS Switch
    [Tags]              csit_tc_8553    aiq_1332    development    xiq    voss    ssh    test1

    &{ip_port_info}=                    Device360 Enable SSH CLI Connectivity   device_mac=${DUT_MAC}  run_time=${SSH_TIMER}
    ${ip}=                              Get From Dictionary  ${ip_port_info}  ip
    ${port}=                            Get From Dictionary  ${ip_port_info}  port
    Set Suite Variable                  ${SSH_IP}     ${ip}
    Set Suite Variable                  ${SSH_PORT}   ${port}

    ${ssh_spawn}=                       Open pxssh Spawn    ${SSH_IP}  ${DUT_USERNAME}  ${DUT_PASSWORD}  ${SSH_PORT}
    ${cmd_result}=                      Send pxssh  ${ssh_spawn}  show sys-info | include Serial
    Log To Console                      SSH Command Result Is ${cmd_result}

    ${close_result}=                    Close pxssh Spawn  ${ssh_spawn}
    Should Not Be Equal As Integers     ${close_result}  -1

    [Teardown]  Close Device360 Window


Test 2: Confirm SSH Session Is Automatically Disabled When Timer Expires
    [Documentation]     Confirms SSH is disabled when the timer expires
    [Tags]              csit_tc_8553    aiq_1332    development    xiq    voss    ssh    test2

    Depends On  Test 1

    Count Down in Minutes  ${SSH_TIMER}

    Confirm SSH Disabled For Device     ${DUT_MAC}

    ${ssh_spawn}=                       Open pxssh Spawn    ${SSH_IP}  ${DUT_USERNAME}  ${DUT_PASSWORD}  ${SSH_PORT}
    Should Be Equal As Integers         ${ssh_spawn}  -1


*** Keywords ***
Log Into XIQ and Set Up Test
    [Documentation]     Logs into XIQ and sets up the elements necessary to complete this test suite

    Log Into XIQ and Confirm Success             ${XIQ_USER}  ${XIQ_PASSWORD}  ${XIQ_URL}

    Change Device Password and Confirm Success   ${DEFAULT_DEVICE_PWD}
    Enable SSH Availability

    Create Open Express Policy With Switch Template and Confirm Success  ${POLICY_NAME}  ${SSID_NAME}  ${DUT_TEMPLATE}

    Reset VOSS Switch to Factory Defaults        ${DUT_CONSOLE_IP}  ${DUT_CONSOLE_PORT}  ${DUT_USERNAME}  ${DUT_PASSWORD}
    Configure iqagent for VOSS Switch            ${DUT_CONSOLE_IP}  ${DUT_CONSOLE_PORT}  ${DUT_USERNAME}  ${DUT_PASSWORD}  ${IQAGENT}

    Onboard New Test Device                      ${DUT_SERIAL}  ${POLICY_NAME}  ${LOCATION}
    Assign Policy to Switch and Confirm Success  ${POLICY_NAME}  ${DUT_SERIAL}
    Confirm Device Serial Has Exected Status     ${DUT_SERIAL}  ${STATUS_AFTER_UPDATE}

Tear Down Test and Close Session
    [Documentation]     Cleans up test data, logs out of XIQ, and closes the browser

    Device360 Disable SSH Connectivity          device_mac=${DUT_MAC}
    Close Device360 Window
    Clean Up Test Device and Confirm Success    ${DUT_SERIAL}
    Delete Policy and Confirm Success           ${POLICY_NAME}
    Delete SSID and Confirm Success             ${SSID_NAME}

    Log Out of XIQ and Quit Browser

Onboard New Test Device
    [Documentation]     Onboards the specified test device, deleting it first if it already exists
    [Arguments]         ${serial}  ${policy}  ${location}

    Navigate to Devices and Confirm Success

    # If the device has already been onboarded, delete it first
    Delete Device and Confirm Success  ${serial}
    Confirm Device Serial Not Present  ${serial}

    # Onboard the device
    Onboard VOSS Device  ${serial}  loc_name=${location}
    sleep   ${DEVICE_ONBOARDING_WAIT}
    Confirm Device Serial Present  ${serial}

Confirm SSH Enabled For Device
    [Documentation]     Checks if SSH is enabled for the specified device
    [Arguments]         ${device_mac}

    Navigate to Devices and Confirm Success
    ${ssh_state}=  Device360 Confirm SSH Enabled   device_mac=${device_mac}
    Should Be Equal As Integers  ${ssh_state}  1
    Close Device360 Window

Confirm SSH Disabled For Device
    [Documentation]     Checks if SSH is disabled for the specified device
    [Arguments]         ${device_mac}

    Navigate to Devices and Confirm Success
    ${ssh_state}=  Device360 Confirm SSH Enabled   device_mac=${device_mac}
    Should Be Equal As Integers  ${ssh_state}  -1
    Close Device360 Window

Clean Up Test Device and Confirm Success
    [Documentation]     Deletes the specified device and confirms the action was successful
    [Arguments]         ${serial}

    Navigate to Devices and Confirm Success

    Delete Device and Confirm Success  ${serial}
    Confirm Device Serial Not Present  ${serial}
