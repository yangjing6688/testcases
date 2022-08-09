#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Heidi S. White
# Description   : Verifies the columns in the Manage Device columns are as expected and contain information:
#                   - MGT IP Address (CSIT: TC-7013)
#                   - Public IP Address (CSIT: TC-7071)

*** Settings ***
Library          common/Cli.py

Resource         ../../ManageDevices/Resources/AllResources.robot

Force Tags       testbed_1_node

Suite Setup      Log In and Set Up Test
Suite Teardown   Tear Down Test and Close Session


*** Variables ***
${XIQ_URL}              ${xiq.test_url}
${XIQ_USER}             ${xiq.tenant_username}
${XIQ_PASSWORD}         ${xiq.tenant_password}
${XIQ_CAPWAP_URL}       ${xiq.capwap_url}

${DUT_SERIAL}           ${ap1.serial}
${DUT_CONSOLE_IP}       ${ap1.ip}
${DUT_CONSOLE_PORT}     ${ap1.port}
${DUT_USERNAME}         ${ap1.username}
${DUT_PASSWORD}         ${ap1.password}
${DUT_CLI_TYPE}         ${ap1.cli_type}
${DUT_PLATFORM}         ${ap1.platform}
${DUT_MAKE}             ${ap1.make}

${LOCATION}             San Jose, building_01, floor_02


*** Test Cases ***
Test 1: Confirm MGT IP Address Column
    [Documentation]     Confirms the MGT IP Address column is present, contains information, and IPv4 is not present
    [Tags]              tccs_7013    aiq_1332    development    xiq    managed_devices    column_validation    mgt_ip    test1

    Navigate to Devices and Confirm Success
    ${yes_result}=  Confirm Column Picker Contains Column           MGT IP Address
    ${no_result}=   Confirm Column Picker Does Not Contain Column   IPv4
    Should Be Equal As Integers                                     ${yes_result}     1
    Should Be Equal As Integers                                     ${no_result}      1

    ${sel_result}=   Column Picker Select                           MGT IP Address
    Should Be Equal As Integers                                     ${sel_result}     1
    ${value}=  Get Device Details                                   ${DUT_SERIAL}  MGT IP ADDRESS
    Should Not Be Equal As Strings                                  '${value}'  ''

Test 2: Confirm Public IP Address Column
    [Documentation]     Confirms the Public IP Address column is present and contains information
    [Tags]              tccs_7071    aiq_1332    development    xiq    managed_devices    column_validation    public_ip    test2

    Navigate to Devices and Confirm Success
    ${yes_result}=  Confirm Column Picker Contains Column   Public IP Address
    Should Be Equal As Integers                             ${yes_result}     1

    ${sel_result}=   Column Picker Select                   Public IP Address
    Should Be Equal As Integers                             ${sel_result}     1
    ${value}=  Get Device Details                           ${DUT_SERIAL}  PUBLIC IP ADDRESS
    Should Not Be Equal As Strings                          '${value}'  ''


*** Keywords ***
Log In and Set Up Test
    [Documentation]     Logs into XIQ and configures pre-requisites for the test

    Log Into XIQ and Confirm Success  ${XIQ_USER}  ${XIQ_PASSWORD}  ${XIQ_URL}
    Navigate to Devices and Confirm Success

    Onboard Device                 ${DUT_SERIAL}  ${DUT_MAKE}  location=${LOCATION}
    Confirm Device Serial Present  ${DUT_SERIAL}

    Configure CAPWAP Device To Connect To Cloud     ${DUT_CLI_TYPE}  ${DUT_CONSOLE_IP}  ${DUT_CONSOLE_PORT}  ${DUT_USERNAME}
    ...                                             ${DUT_PASSWORD}  ${XIQ_CAPWAP_URL}

    Confirm Device Serial Online   ${DUT_SERIAL}  retry_count=20

Tear Down Test and Close Session
    [Documentation]     Cleans up the components created during the test and ends the test

    Navigate to Devices and Confirm Success
    Delete Device and Confirm Success  ${DUT_SERIAL}
    Log Out of XIQ and Quit Browser

Configure CAPWAP Device To Connect To Cloud
    [Documentation]     Configure the CAPWAP client with the necessary configuration on the Device to Connect to Cloud
    [Arguments]         ${cli_type}  ${ip}  ${port}  ${user}  ${pwd}  ${capwap_url}

    ${CONFIG_RESULT}=   Configure Device To Connect To Cloud     ${cli_type}  ${ip}  ${port}  ${user}  ${pwd}  ${capwap_url}
    Should Be Equal as Integers         ${CONFIG_RESULT}         1
