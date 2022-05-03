#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : John Borges
# Description   : Test Suite for testing the Global Setting VIQ Management SSH Availability
# Topology      : One AP


*** Settings ***
Library               xiq/flows/manage/Device360.py
Library               common/Cli.py

Resource              ../../GlobalSettings/Resources/AllResources.robot

Force Tags            testbed_1_node

Suite Setup           Log Into XIQ and Set Up Test
Suite Teardown        Tear Down Test and Close Session


*** Variables ***
${XIQ_URL}            ${test_url}
${XIQ_USER}           ${tenant_username}
${XIQ_PASSWORD}       ${tenant_password}
${XIQ_CAPWAP_URL}     ${capwap_url}

${AP_NAME}            ${ap1.name}
${AP_SERIAL}          ${ap1.serial}
${AP_MAKE}            ${ap1.make}
${AP_LOCATION}        ${ap1.location}
${AP_MAC}             ${ap1.mac}
${AP_CONSOLE_IP}      ${ap1.console_ip}
${AP_CONSOLE_PORT}    ${ap1.console_port}
${AP_USERNAME}        ${ap1.username}
${AP_PASSWORD}        ${ap1.password}
${AP_PLATFORM}        ${ap1.platform}


*** Test Cases ***
TCXM-15253: Disable SSH Availability
    [Documentation]     Confirms the disabling of SSH Availability
    [Tags]              xim_tc_15253   development

    ${dis_result}=      Disable SSH Availability
    Should Be Equal As Integers   ${dis_result}   1
    ${d360_result}=     Device360 Is SSH Disabled   device_mac=${AP_MAC}
    Should Be Equal As Integers   ${d360_result}   1
    ${close_results}=   Close Device360 Window
    Should Be Equal As Integers   ${close_results}   1

TCXM-15252: Enable SSH Availability
    [Documentation]     Confirms the enabling of SSH Availability
    [Tags]              xim_tc_15252   development

    ${en_result}=       Enable SSH Availability
    Should Be Equal As Integers   ${en_result}   1
    ${d360_result}=     Device360 Is SSH Enabled   device_mac=${AP_MAC}
    Should Be Equal As Integers   ${d360_result}   1
    ${close_results}=   Close Device360 Window
    Should Be Equal As Integers   ${close_results}   1


*** Keywords ***
Log Into XIQ and Set Up Test
    [Documentation]     Logs into XIQ and sets up the elements necessary to complete this test suite

    Log Into XIQ and Confirm Success  ${XIQ_USER}  ${XIQ_PASSWORD}  ${XIQ_URL}
    Onboard Test Devices

Onboard Test Devices
    [Documentation]     Onboards the test devices

    Navigate to Devices and Confirm Success

    # Onboard the devices for the test
    ${dut1_result}=     Search Device Serial   ${AP_SERIAL}
    Run Keyword If      '${dut1_result}' != '1'  Onboard Device   ${AP_SERIAL}  ${AP_MAKE}  location=${AP_LOCATION}

    Configure CAPWAP               ${AP_CONSOLE_IP}  ${AP_CONSOLE_PORT}  ${AP_USERNAME}
    ...                            ${AP_PASSWORD}  ${AP_PLATFORM}  ${XIQ_CAPWAP_URL}

    # Confirm the devices were onboarded
    Confirm Device Serial Present  ${AP_SERIAL}
    Wait Until Device Online       ${AP_SERIAL}

Configure CAPWAP
    [Documentation]     Configures the CAPWAP client
    [Arguments]         ${ip}  ${port}  ${user}  ${pwd}  ${platform}  ${capwap_server}

    ${spawn}=           Open Spawn  ${ip}  ${port}  ${user}  ${pwd}  ${platform}

    Send                ${spawn}   capwap client server name ${capwap_server}
    Send                ${spawn}   capwap client default-server-name ${capwap_server}
    Send                ${spawn}   capwap client server backup name ${capwap_server}
    Send                ${spawn}   no capwap client enable
    Send                ${spawn}   capwap client enable
    Send                ${spawn}   save config

    Close Spawn         ${spawn}

Tear Down Test and Close Session
    [Documentation]     Cleans up test data, logs out of XIQ, and closes the browser

    Clean Up Test Device and Confirm Success  ${AP_SERIAL}
    Log Out of XIQ and Quit Browser

Clean Up Test Device and Confirm Success
    [Documentation]     Deletes the specified device and confirms the action was successful
    [Arguments]         ${serial}

    Navigate to Devices and Confirm Success
    Delete Device and Confirm Success  ${serial}
    Confirm Device Serial Not Present  ${serial}
