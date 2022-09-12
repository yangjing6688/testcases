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
${DUT_IP}                   ${netelem3.ip}
${DUT_PORT}                 ${netelem3.port}
${DUT_USERNAME}             ${netelem3.username}
${DUT_PASSWORD}             ${netelem3.password}
${DUT_PLATFORM}             ${netelem3.platform}
${DUT_MAKE}                 ${netelem3.make}
${DUT_CLI_TYPE}             ${netelem3.cli_type}

${DEFAULT_DEVICE_PWD}       Aerohive123
${SSH_TIMER}                5
${STATUS_AFTER_UPDATE}      green
${LOCATION}                 auto_location_01, Santa Clara, building_02, floor_04
${POLICY_NAME}              VOSS_POLICY_AUTO
${SSID_NAME}                VOSS_SSID_AUTO


*** Test Cases ***
Test 1: Enable SSH on Teste Device and Confirm SSH Session Can Be Established
    [Documentation]     Enables SSH for the VOSS Switch
    [Tags]              tccs_8553    aiq_1332    development    xiq    voss    ssh    test1

    &{ip_port_info}=                    Device360 Enable SSH CLI Connectivity   device_mac=${DUT_MAC}  run_time=${SSH_TIMER}
    ${ip}=                              Get From Dictionary  ${ip_port_info}  ip
    ${port}=                            Get From Dictionary  ${ip_port_info}  port
    Set Suite Variable                  ${SSH_IP}     ${ip}
    Set Suite Variable                  ${SSH_PORT}   ${port}

    ${spawn}=                           Open Spawn    ${DUT_IP}  ${DUT_PORT}  ${DUT_USERNAME}  ${DUT_PASSWORD}  ${DUT_CLI_TYPE}
    ${cmd_result}=                      Send  ${spawn}  show sys-info | include Serial
    Log To Console                      SSH Command Result Is ${cmd_result}
    ${close_result}=                    Close Spawn and Confirm Success  ${spawn}

    [Teardown]  Close Device360 Window


Test 2: Confirm SSH Session Is Automatically Disabled When Timer Expires
    [Documentation]     Confirms SSH is disabled when the timer expires
    [Tags]              tccs_8553    aiq_1332    development    xiq    voss    ssh    test2

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

    Configure Test Device                        ${DUT_IP}  ${DUT_PORT}  ${DUT_USERNAME}  ${DUT_PASSWORD}  ${DUT_CLI_TYPE}  ${IQAGENT}

    Onboard New Test Device                      ${DUT_SERIAL}  ${DUT_MAKE}  ${POLICY_NAME}  ${LOCATION}
    Assign Policy to Switch and Confirm Success  ${POLICY_NAME}  ${DUT_SERIAL}
    Confirm Device Serial Has Expected Status    ${DUT_SERIAL}  ${STATUS_AFTER_UPDATE}

Tear Down Test and Close Session
    [Documentation]     Cleans up test data, logs out of XIQ, and closes the browser

    Device360 Disable SSH Connectivity          device_mac=${DUT_MAC}
    Close Device360 Window
    Clean Up Test Device and Confirm Success    ${DUT_SERIAL}
    Delete Policy and Confirm Success           ${POLICY_NAME}
    Delete SSID and Confirm Success             ${SSID_NAME}

    Log Out of XIQ and Quit Browser

Configure Test Device
    [Documentation]     Configures the specified test device by rebooting a known good configuration file and then configuring the iqagent
    [Arguments]         ${ip}  ${port}  ${user}  ${pwd}  ${cli_type}  ${agent}

    Boot Switch To Known Good Configuration     ${ip}  ${port}  ${user}  ${pwd}  ${cli_type}

    # Downgrade the device's iqagent if needed
    Downgrade Iqagent                           ${ip}  ${port}  ${user}  ${pwd}  ${cli_type}

    ${SPAWN_CONNECTION}=      Open Spawn       ${ip}  ${port}  ${user}  ${pwd}  ${cli_type}

    ${CONF_STATUS_RESULT}=      Configure Device To Connect To Cloud    ${cli_type}      ${agent}     ${SPAWN_CONNECTION}
    Should Be Equal As Strings                  ${CONF_STATUS_RESULT}       1

    Close Spawn       ${SPAWN_CONNECTION}

Onboard New Test Device
    [Documentation]     Onboards the specified test device, deleting it first if it already exists
    [Arguments]         ${serial}  ${make}  ${policy}  ${location}

    Navigate to Devices and Confirm Success

    # If the device has already been onboarded, delete it first
    Delete Device and Confirm Success  ${serial}
    Confirm Device Serial Not Present  ${serial}

    # Onboard the device
    Onboard Device    ${serial}  ${make}  ${policy}  location=${location}
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
