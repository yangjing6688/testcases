#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : David Truesdell
# Description   : Test Suite for acceptance testing of basic XIQSE DUT analytics engine Configuration functionality.
#                 This is qTest TC-873 in the XIQ-SE project.

*** Settings ***
Library         xiqse/flows/network/devices/site/actions/XIQSE_NetworkDevicesSiteActions.py

Resource        ../../AcceptanceTest/Resources/AllResources.robot

Force Tags      testbed_1_node

Suite Setup      Log In and Set Up Test
Suite Teardown   Tear Down Test and Close Session

*** Variables ***
${XIQSE_URL}                        ${xiqse.url}
${XIQSE_USERNAME}                   ${xiqse.user}
${XIQSE_PASSWORD}                   ${xiqse.password}
${XIQSE_IP_ADDRESS}                 ${xiqse.ip}
${XIQSE_MAC}                        ${xiqse.mac}
${INSTALL_MODE}                     ${upgrades.install_mode}

${XIQ_URL}                          ${xiq.test_url}
${XIQ_EMAIL}                        ${xiq.tenant_username}
${XIQ_PASSWORD}                     ${xiq.tenant_password}

${DUT_IP}                           ${purview.ip}
${DUT_NAME}                         ${purview.name}
${DUT_PROFILE}                      ${appliance.profile}

${TEST_CLI_USER}                    ${appliance.user}
${TEST_CLI_LOGIN_PWD}               ${appliance.password}
${TEST_CLI_ENABLE_PWD}              ${appliance.password}
${TEST_CLI_CONFIG_PWD}              ${appliance.password}
${TEST_PROFILE_NAME}                ${appliance.profile}

${WORLD_SITE}                       World
${TEST_CLI_NAME}                    Analytics_Engine_CLI
${TEST_CLI_TYPE}                    SSH
${TEST_PROFILE_VERSION}             SNMPv3
${TEST_PROFILE_READ_COMM}           default_snmp_v3
${TEST_PROFILE_WRITE_COMM}          default_snmp_v3
${TEST_PROFILE_MAX_COMM}            default_snmp_v3
${TEST_PROFILE_READ_SECURITY}       AuthPriv
${TEST_PROFILE_WRITE_SECURITY}      AuthPriv
${TEST_PROFILE_MAX_SECURITY}        AuthPriv


*** Test Cases ***
TEST 1: Create DUT Analytics Engine and Confirm Success
    [Documentation]     Creates an analytics engine
    [Tags]              xiqse_tc_873    xmc_5451    development    xiqse    acceptance    analytics    test1

    Navigate and Add Analytics Engine       ${DUT_IP}  ${DUT_NAME}  ${TEST_PROFILE_NAME}

TEST 2: Confirm Events - DUT Engine Added
    [Documentation]     Confirms the events view contains the expected event
    [Tags]              xiqse_tc_873    xmc_5451    development    xiqse    acceptance    analytics    test2

    Navigate to Events and Confirm Success
    Set Event Time Range and Confirm Success        Last 30 Minutes
    Set Event Type and Confirm Success              Application Analytics
    Set Event Search String and Confirm Success     Application Analytics Engine Added

    Confirm Event Row Contains Text                 Application Analytics Engine ${DUT_IP} '${DUT_NAME}' added

TEST 3: Enforce DUT Engine and Confirm Success
    [Documentation]     Enforces an analytics engine
    [Tags]              xiqse_tc_873    xmc_5451    development    xiqse    acceptance    analytics    test3

    Navigate and Enforce Analytics Engine            ${DUT_IP}

TEST 4: Confirm Events - DUT Engine Enforced
    [Documentation]     Confirms the events view contains the expected event
    [Tags]              xiqse_tc_873    xmc_5451    development    xiqse    acceptance    analytics    test4

    Navigate to Events and Confirm Success
    Set Event Search String and Confirm Success     Application Analytics Engine Enforcement

    Confirm Event Row Contains Text                 Application Analytics Engine ${DUT_IP} '${DUT_NAME}' enforced successfully

TEST 5: Poll DUT Engine and Confirm Success
    [Documentation]     Polls an analytics engine
    [Tags]              xiqse_tc_873    xmc_5451    development    xiqse    acceptance    analytics    test5

    Navigate and Poll Analytics Engine          ${DUT_IP}

TEST 6: Restart Collector on DUT Engine and Confirm Success
    [Documentation]     Restarts collector on an analytics engine
    [Tags]              xiqse_tc_873    xmc_5451    development    xiqse    acceptance    analytics    test6

    Restart Collector and Confirm Success       ${DUT_IP}

TEST 7: Confirm Events - Restart Collector on DUT Engine
    [Documentation]     Confirms the events view contains the expected event
    [Tags]              xiqse_tc_873    xmc_5451    development    xiqse    acceptance    analytics    test7

    Navigate to Events and Confirm Success
    Set Event Search String and Confirm Success     Application Analytics Engine Collector Restart

    Confirm Event Row Contains Text             ${DUT_IP}

TEST 8: Delete DUT Analytics Engine and Confirm Success
    [Documentation]     Confirms a device can be deleted
    [Tags]              xiqse_tc_873    xmc_5451    development    xiqse    acceptance    analytics    test8

    Navigate and Delete Analytics Engine        ${DUT_IP}

TEST 9: Confirm Events - DUT Engine Deleted
    [Documentation]     Confirms the events view contains the expected event
    [Tags]              xiqse_tc_873    xmc_5451    development    xiqse    acceptance    analytics    test9

    Navigate to Events and Confirm Success
    Set Event Search String and Confirm Success     Application Analytics Engine Deleted
    Confirm Event Row Contains Text                 Application Analytics Engine ${DUT_IP} '${DUT_NAME}' deleted


*** Keywords ***
Log In and Set Up Test
    [Documentation]     Logs in and configures everything that is required for the test to run

    Log Into XIQSE and Close Panels                 ${XIQSE_USERNAME}    ${XIQSE_PASSWORD}    url=${XIQSE_URL}
    Set Option Web Server Session Timeout and Confirm Success  7  day(s)
    Set Option Device Tree Name Format and Confirm Success   IP Address
    Disable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver    ${WORLD_SITE}
    Create Analytics Engine CLI Credentials    ${TEST_CLI_NAME}  ${TEST_CLI_USER}  ${TEST_CLI_TYPE}
    ...                                        ${TEST_CLI_LOGIN_PWD}  ${TEST_CLI_ENABLE_PWD}  ${TEST_CLI_CONFIG_PWD}
    Create Analytics Engine SNMPv3 Profile and Confirm Success    ${TEST_PROFILE_NAME}  ${TEST_PROFILE_VERSION}  ${TEST_PROFILE_READ_COMM}   ${TEST_PROFILE_WRITE_COMM}  ${TEST_PROFILE_MAX_COMM}
    ...                                                           ${TEST_CLI_NAME}   ${TEST_PROFILE_READ_SECURITY}  ${TEST_PROFILE_WRITE_SECURITY}  ${TEST_PROFILE_MAX_SECURITY}
    Onboard XIQSE To XIQ If In Connected Mode        ${INSTALL_MODE}  ${XIQSE_IP_ADDRESS}  ${XIQ_EMAIL}  ${XIQ_PASSWORD}

Tear Down Test and Close Session
    [Documentation]     Logs in and cleans up all items that were set up for the test

    Restore Web Server Options to Default and Confirm Success
    Restore Site Engine General Options to Default and Confirm Success
    Enable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver    ${WORLD_SITE}
    Log Out of XIQSE and Quit Browser
    Remove XIQSE From XIQ If In Connected Mode        ${INSTALL_MODE}  ${XIQ_EMAIL}  ${XIQ_PASSWORD}  ${XIQ_URL}  ${XIQSE_MAC}

Create Analytics Engine CLI Credentials
    [Documentation]     Confirms a CLI credential can be added
    [Arguments]         ${cli_name}  ${cli_user}  ${cli_type}  ${cli_login_pwd}  ${cli_enable_pwd}  ${cli_config_pwd}

    Navigate and Create CLI Credential            ${TEST_CLI_NAME}  ${TEST_CLI_USER}  ${TEST_CLI_TYPE}
    ...                                           ${TEST_CLI_LOGIN_PWD}  ${TEST_CLI_ENABLE_PWD}  ${TEST_CLI_CONFIG_PWD}

Create Analytics Engine SNMPv3 Profile and Confirm Success
    [Documentation]     Confirms an SNMPv3 profile can be added
    [Arguments]         ${profile_name}  ${profile_version}  ${profile_read_comm}  ${profile_write_comm}  ${profile_max_comm}
    ...                 ${cli_name}  ${profile_read_sec}  ${profile_write_sec}  ${profile_max_sec}

    Navigate and Create Profile    ${TEST_PROFILE_NAME}  ${TEST_PROFILE_VERSION}  ${TEST_PROFILE_READ_COMM}   ${TEST_PROFILE_WRITE_COMM}  ${TEST_PROFILE_MAX_COMM}
    ...                            ${TEST_CLI_NAME}   ${TEST_PROFILE_READ_SECURITY}  ${TEST_PROFILE_WRITE_SECURITY}  ${TEST_PROFILE_MAX_SECURITY}

Delete Profile
    [Documentation]     Confirms a profile can be deleted

    Navigate and Delete Profile  ${TEST_PROFILE_NAME}

Delete CLI Credential
    [Documentation]     Confirms a CLI credential can be deleted

    Navigate and Delete CLI Credential  ${TEST_CLI_NAME}