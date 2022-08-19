#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Heidi S. White
# Description   : Test Suite for sanity testing of basic XIQ-SE profiles functionality.
#                 This is qTest TC-896 in the XIQ-SE project.

*** Settings ***
Resource        ../../SampleTests/Resources/AllResources.robot

Force Tags      testbed_0_node

Suite Setup     Log Into XIQSE and Close Panels    ${XIQSE_USER}   ${XIQSE_PASSWORD}   url=${XIQSE_URL}
Suite Teardown  Log Out of XIQSE and Quit Browser


*** Variables ***
${ENV}                   environment.remote.chrome.windows.xiqse1.yaml
${TOPO}                  topo.test.xiqse1.connected.yaml
${TESTBED}               SALEM/Dev/devices-salem-acceptance.yaml

${XIQSE_URL}             ${xiqse.url}
${XIQSE_USER}            ${xiqse.user}
${XIQSE_PASSWORD}        ${xiqse.password}

${TEST_PROFILE}          AUTO_PROFILE
${TEST_PROFILE_VERSION}  SNMPv2
${TEST_CRED_NAME}        AUTO_CRED
${TEST_CRED_VERSION}     SNMPv2
${TEST_CRED_COMM}        automation
${TEST_CLI_DESC}         AUTO_CLI
${TEST_CLI_USER}         AUTO_CLI_USER
${TEST_CLI_TYPE}         SSH
${TEST_CLI_LOGIN_PWD}    AUTO_LOGIN
${TEST_CLI_ENABLE_PWD}   AUTO_ENABLE
${TEST_CLI_CONFIG_PWD}   AUTO_CONFIG


*** Test Cases ***
Test 1: Add CLI Credential
    [Documentation]     Confirms a CLI credential can be added
    [Tags]              tcxe_896    aiq_1332    development    sample    xiqse    profiles    test1

    Navigate and Create CLI Credential  ${TEST_CLI_DESC}  ${TEST_CLI_USER}  ${TEST_CLI_TYPE}
    ...                                 ${TEST_CLI_LOGIN_PWD}  ${TEST_CLI_ENABLE_PWD}  ${TEST_CLI_CONFIG_PWD}

Test 2: Add Duplicate CLI Credential
    [Documentation]     Confirms creating a duplicate CLI credential is handled correctly (message printed, dialog closed)
    [Tags]              tcxe_896    aiq_1332    development    sample    xiqse    profiles    test2

    Navigate and Create CLI Credential          ${TEST_CLI_DESC}  ${TEST_CLI_USER}  ${TEST_CLI_TYPE}
    ...                                         ${TEST_CLI_LOGIN_PWD}  ${TEST_CLI_ENABLE_PWD}  ${TEST_CLI_CONFIG_PWD}
    Create CLI Credential and Confirm Success   ${TEST_CLI_DESC}  ${TEST_CLI_USER}  ${TEST_CLI_TYPE}
    ...                                         ${TEST_CLI_LOGIN_PWD}  ${TEST_CLI_ENABLE_PWD}  ${TEST_CLI_CONFIG_PWD}

Test 3: Add SNMP Credential
    [Documentation]     Confirms an SNMP credential can be added
    [Tags]              tcxe_896    aiq_1332    development    sample    xiqse    profiles    test3

    Navigate and Create SNMP Credential  ${TEST_CRED_NAME}  ${TEST_CRED_VERSION}  ${TEST_CRED_COMM}

Test 4: Add Duplicate SNMP Credential
    [Documentation]     Confirms creating a duplicate SNMP credential is handled correctly (message printed, dialog closed)
    [Tags]              tcxe_896    aiq_1332    development    sample    xiqse    profiles    test4

    Navigate and Create SNMP Credential         ${TEST_CRED_NAME}  ${TEST_CRED_VERSION}  ${TEST_CRED_COMM}
    Create SNMP Credential and Confirm Success  ${TEST_CRED_NAME}  ${TEST_CRED_VERSION}  ${TEST_CRED_COMM}

Test 5: Add Profile
    [Documentation]     Confirms a profile can be added (depends on tests 1 and 3, adding CLI and SNMP creds)
    [Tags]              tcxe_896    aiq_1332    development    sample    xiqse    profiles    test5

    Navigate and Create Profile  ${TEST_PROFILE}  ${TEST_PROFILE_VERSION}  read=${TEST_CRED_NAME}  cli=${TEST_CLI_DESC}

Test 6: Add Duplicate Profile
    [Documentation]     Confirms creating a duplicate profile is handled correctly (message printed, dialog closed)
    ...                 (depends on tests 1 and 3, adding CLI and SNMP creds)
    [Tags]              tcxe_896    aiq_1332    development    sample    xiqse    profiles    test6

    Navigate and Create Profile         ${TEST_PROFILE}  ${TEST_PROFILE_VERSION}  read=${TEST_CRED_NAME}  cli=${TEST_CLI_DESC}
    Create Profile and Confirm Success  ${TEST_PROFILE}  ${TEST_PROFILE_VERSION}  read=${TEST_CRED_NAME}  cli=${TEST_CLI_DESC}

Test 7: Edit Profile
    [Documentation]     Confirms a profile can be edited (depends on tests 1 and 3, adding CLI and SNMP creds)
    [Tags]              tcxe_896    aiq_1332    development    sample    xiqse    profiles    test7

    Edit Profile and Confirm Success  ${TEST_PROFILE}  write=${TEST_CRED_NAME}  max=${TEST_CRED_NAME}  cli=Default

Test 8: Edit Profile With No Changes
    [Documentation]     Confirms editing a profile with no changes is handled correctly (message printed, dialog closed)
    ...                 (depends on tests 1 and 3, adding CLI and SNMP creds)
    [Tags]              tcxe_896    aiq_1332    development    sample    xiqse    profiles    test8

    Edit Profile and Confirm Success    ${TEST_PROFILE}  write=${TEST_CRED_NAME}  max=${TEST_CRED_NAME}  cli=Default
    Edit Profile and Confirm Success    ${TEST_PROFILE}  write=${TEST_CRED_NAME}  max=${TEST_CRED_NAME}  cli=Default

Test 9: Delete Profile
    [Documentation]     Confirms a profile can be deleted (depends on test 5, adding a profile)
    [Tags]              tcxe_896    aiq_1332    development    sample    xiqse    profiles    test9

    Navigate and Delete Profile  ${TEST_PROFILE}

Test 10: Delete SNMP Credential (depends on test 3, adding an SNMP credential)
    [Documentation]     Confirms an SNMP credential can be deleted
    [Tags]              tcxe_896    aiq_1332    development    sample    xiqse    profiles    test10

    Navigate and Delete SNMP Credential  ${TEST_CRED_NAME}

Test 11: Delete CLI Credential
    [Documentation]     Confirms a CLI credential can be deleted (depends on test 1, adding a CLI credential)
    [Tags]              tcxe_896    aiq_1332    development    sample    xiqse    profiles    test11

    Navigate and Delete CLI Credential  ${TEST_CLI_DESC}

Test 12: Add SNMPv1 Profile
    [Documentation]     Confirms an SNMPv1 profile can be added
    [Tags]              tcxe_896    aiq_1332    development    sample    xiqse    profiles    test12

    Navigate and Create Profile  ${TEST_PROFILE}  SNMPv1

    Delete Profile and Confirm Success  ${TEST_PROFILE}

Test 13: Add SNMPv2 Profile
    [Documentation]     Confirms an SNMPv2 profile can be added
    [Tags]              tcxe_896    aiq_1332    development    sample    xiqse    profiles    test13

    Navigate and Create Profile  ${TEST_PROFILE}  SNMPv2

    Delete Profile and Confirm Success  ${TEST_PROFILE}

Test 14: Add SNMPv3 Profile
    [Documentation]     Confirms an SNMPv3 profile can be added
    [Tags]              tcxe_896    aiq_1332    development    sample    xiqse    profiles    test14

    Navigate and Create Profile  ${TEST_PROFILE}  SNMPv3  read_sec=AuthPriv  write_sec=AuthNoPriv  max_sec=NoAuthNoPriv

    Delete Profile and Confirm Success  ${TEST_PROFILE}
