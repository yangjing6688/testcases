#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Heidi S. White
# Description   : Test Suite for sanity testing of basic XIQ-SE SNMP Credentials functionality.
#                 This is qTest TC-897 in the XIQ-SE project.

*** Settings ***
Resource        ../../SampleTests/Resources/AllResources.robot

Force Tags      testbed_0_node

Suite Setup     Log In and Set Up Test
Suite Teardown  Tear Down Test and Close Session


*** Variables ***
${ENV}                  environment.remote.chrome.windows.xiqse1.yaml
${TOPO}                 topo.test.xiqse1.connected.yaml
${TESTBED}              SALEM/Dev/devices-salem-acceptance.yaml

${XIQSE_URL}            ${xiqse.url}
${XIQSE_USER}           ${xiqse.user}
${XIQSE_PASSWORD}       ${xiqse.password}

${V1_CRED_NAME}         AUTO_v1
${V2_CRED_NAME}         AUTO_v2
${V3_CRED_NAME}         AUTO_v3
${CRED_COMM}            automation
${CRED_USER}            admin
${AUTH_PWD}             Abcd1234
${PRIV_PWD}             6789wxyZ


*** Test Cases ***
Test 1: Add SNMPv1 Credential
    [Documentation]     Confirms an SNMPv1 credential can be added
    [Tags]              xiqse_tc_897    aiq_1332    development    sample    xiqse    snmp_creds    test1

    ${add_result}=  XIQSE Create SNMPv1 Credential  ${V1_CRED_NAME}  ${CRED_COMM}
    Should Be Equal As Integers                     ${add_result}     1

    ${find_result}=  XIQSE Find SNMP Credential     ${V1_CRED_NAME}
    Should Be Equal As Integers                     ${find_result}     1

    [Teardown]  Delete SNMP Credential  ${V1_CRED_NAME}

Test 2: Add SNMPv2 Credential
    [Documentation]     Confirms an SNMPv2 credential can be added
    [Tags]              xiqse_tc_897    aiq_1332    development    sample    xiqse    snmp_creds    test2

    ${add_result}=  XIQSE Create SNMPv2 Credential  ${V2_CRED_NAME}  ${CRED_COMM}
    Should Be Equal As Integers                     ${add_result}     1

    ${find_result}=  XIQSE Find SNMP Credential     ${V2_CRED_NAME}
    Should Be Equal As Integers                     ${find_result}     1

    [Teardown]  Delete SNMP Credential  ${V2_CRED_NAME}

Test 3: Add SNMPv3 Credential - No Authentication
    [Documentation]     Confirms an SNMPv3 credential can be added with No Authentication Type
    [Tags]              xiqse_tc_897    aiq_1332    development    sample    xiqse    snmp_creds    test3

    ${add_result}=  XIQSE Create SNMPv3 Credential  ${V3_CRED_NAME}  ${CRED_USER}
    Should Be Equal As Integers                     ${add_result}     1

    ${find_result}=  XIQSE Find SNMP Credential     ${V3_CRED_NAME}
    Should Be Equal As Integers                     ${find_result}     1

    [Teardown]  Delete SNMP Credential  ${V3_CRED_NAME}

Test 4: Add SNMPv3 Credential - MD5 Authentication
    [Documentation]     Confirms an SNMPv3 credential can be added with MD5 Authentication Type
    [Tags]              xiqse_tc_897    aiq_1332    development    sample    xiqse    snmp_creds    test4

    ${add_result}=  XIQSE Create SNMPv3 Credential  ${V3_CRED_NAME}  ${CRED_USER}  auth_type=MD5  auth_pwd=${AUTH_PWD}
    Should Be Equal As Integers                     ${add_result}     1

    ${find_result}=  XIQSE Find SNMP Credential     ${V3_CRED_NAME}
    Should Be Equal As Integers                     ${find_result}     1

    [Teardown]  Delete SNMP Credential  ${V3_CRED_NAME}

Test 5: Add SNMPv3 Credential - SHA Authentication
    [Documentation]     Confirms an SNMPv3 credential can be added with SHA Authentication Type
    [Tags]              xiqse_tc_897    aiq_1332    development    sample    xiqse    snmp_creds    test5

    ${add_result}=  XIQSE Create SNMPv3 Credential  ${V3_CRED_NAME}  ${CRED_USER}  auth_type=SHA  auth_pwd=${AUTH_PWD}
    Should Be Equal As Integers                     ${add_result}     1

    ${find_result}=  XIQSE Find SNMP Credential     ${V3_CRED_NAME}
    Should Be Equal As Integers                     ${find_result}     1

    [Teardown]  Delete SNMP Credential  ${V3_CRED_NAME}

Test 6: Add SNMPv3 Credential - AES Privacy
    [Documentation]     Confirms an SNMPv3 credential can be added with AES Privacy Type
    [Tags]              xiqse_tc_897    aiq_1332    development    sample    xiqse    snmp_creds    test6

    ${add_result}=  XIQSE Create SNMPv3 Credential  ${V3_CRED_NAME}  ${CRED_USER}  auth_type=MD5  auth_pwd=${AUTH_PWD}
    ...    priv_type=AES    priv_pwd=${PRIV_PWD}
    Should Be Equal As Integers                     ${add_result}     1

    ${find_result}=  XIQSE Find SNMP Credential     ${V3_CRED_NAME}
    Should Be Equal As Integers                     ${find_result}     1

    [Teardown]  Delete SNMP Credential  ${V3_CRED_NAME}

Test 7: Add SNMPv3 Credential - DES Privacy
    [Documentation]     Confirms an SNMPv3 credential can be added with AES Privacy Type
    [Tags]              xiqse_tc_897    aiq_1332    development    sample    xiqse    snmp_creds    test7

    ${add_result}=  XIQSE Create SNMPv3 Credential  ${V3_CRED_NAME}  ${CRED_USER}  auth_type=MD5  auth_pwd=${AUTH_PWD}
    ...    priv_type=DES    priv_pwd=${PRIV_PWD}
    Should Be Equal As Integers                     ${add_result}     1

    ${find_result}=  XIQSE Find SNMP Credential     ${V3_CRED_NAME}
    Should Be Equal As Integers                     ${find_result}     1

    [Teardown]  Delete SNMP Credential  ${V3_CRED_NAME}


*** Keywords ***
Log In and Set Up Test
    [Documentation]     Logs in and sets up the components for the test

    # Log into XIQSE
    ${login}=  XIQSE Load Page and Log In  ${XIQSE_USER}    ${XIQSE_PASSWORD}    url=${XIQSE_URL}
    Should Be Equal As Integers            ${login}     1

    # Close any banner messages (Connection Lost with XIQ, License Expiration, etc.)
    XIQSE Close Login Banner Messages

    # Close the Help panel if it is open
    XIQSE Close Help Panel

    # Navigate to the Administration> Profiles page
    ${nav_result}=  XIQSE Navigate to Admin Profiles Tab
    Should Be Equal As Integers  ${nav_result}     1

    # Select the SNMP Credentials tab
    ${tab_result}=  XIQSE Profiles Select SNMP Credentials Tab
    Should Be Equal As Integers                  ${tab_result}     1

Tear Down Test and Close Session
    [Documentation]     Cleans up XIQ and XIQSE test components and closes the browser

    # Log out of XIQSE
    ${result}=  XIQSE Logout User
    Should Be Equal As Integers    ${result}     1

    # Close the browser
    XIQSE Quit Browser

Delete SNMP Credential
    [Documentation]     Deletes the specified SNMP credential and confirms it was removed
    [Arguments]         ${cred_name}

    ${del_result}=  XIQSE Delete SNMP Credential   ${cred_name}
    Should Be Equal As Integers                    ${del_result}     1

    ${find_result}=  XIQSE Find SNMP Credential    ${cred_name}
    Should Be Equal As Integers                    ${find_result}    -1
