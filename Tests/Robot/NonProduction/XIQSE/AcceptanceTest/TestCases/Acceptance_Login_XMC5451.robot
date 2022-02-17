#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Heidi S. White
# Description   : Testing of basic XIQSE login functionality.
#                 NOTE: this test assumes the License Agrrement has already been accepted.
#                 This is qTest TC-870 in the XIQ-SE project.

*** Settings ***
Resource        ../../AcceptanceTest/Resources/AllResources.robot

Force Tags      testbed_1_node

Suite Setup      Log In and Set Up Test
Suite Teardown   Tear Down Test and Close Session

*** Variables ***
${XIQSE_URL}            ${xiqse.url}
${XIQSE_USERNAME}       ${xiqse.user}
${XIQSE_PASSWORD}       ${xiqse.password}
${XIQSE_IP_ADDRESS}     ${xiqse.ip}
${XIQSE_MAC}            ${xiqse.mac}
${INSTALL_MODE}         ${upgrades.install_mode}

${XIQ_URL}              ${xiq.test_url}
${XIQ_EMAIL}            ${xiq.tenant_username}
${XIQ_PASSWORD}         ${xiq.tenant_password}


*** Test Cases ***
Test 1: Confirm Log In with Valid Credentials
    [Documentation]     Confirms successful log in with valid credentials
    [Tags]              xiqse_tc_870    xmc_5451    development    xiqse    acceptance    login    test1

    Log Into XIQSE and Confirm Success    ${XIQSE_USERNAME}  ${XIQSE_PASSWORD}  url=${XIQSE_URL}

    Log Out of XIQSE and Confirm Success
    [Teardown]  Quit Browser and Confirm Success

Test 2: Confirm Log In with Invalid User
    [Documentation]     Confirms log in with invalid user fails
    [Tags]              xiqse_tc_870    xmc_5451    development    xiqse    acceptance    login    test2

    ${result}=  XIQSE Load Page and Log In  BAD_USER  ${XIQSE_PASSWORD}  url=${XIQSE_URL}
    Should Be Equal As Integers             ${result}     -1

    [Teardown]  Quit Browser and Confirm Success

Test 3: Confirm Log In with Invalid Password
    [Documentation]     Confirms log in with invalid password fails
    [Tags]              xiqse_tc_870    xmc_5451    development    xiqse    acceptance    login    test3

    ${result}=  XIQSE Load Page and Log In  ${XIQSE_USERNAME}  BAD_PASSWORD  url=${XIQSE_URL}
    Should Be Equal As Integers             ${result}     -1

    [Teardown]  Quit Browser and Confirm Success

Test 4: Confirm Log In with Invalid User and Invalid Password
    [Documentation]     Confirms log in with invalid user and invalid password fails
    [Tags]              xiqse_tc_870    xmc_5451    development    xiqse    acceptance    login    test4

    ${result}=  XIQSE Load Page and Log In  BAD_USER  BAD_PASSWORD  url=${XIQSE_URL}
    Should Be Equal As Integers             ${result}     -1

    [Teardown]  Quit Browser and Confirm Success

Test 5: Confirm Log In with Valid Credentials after Invalid Credentials is Successful
    [Documentation]     Confirms log in with valid credentials works after failing with invalid credentials
    [Tags]              nxiqse_tc_870    xmc_5451    development    xiqse    acceptance    login    test5

    ${invalid_result}=  XIQSE Load Page and Log In  BAD_USER  BAD_PASSWORD  url=${XIQSE_URL}
    Should Be Equal As Integers                     ${invalid_result}     -1

    ${valid_result}=  XIQSE Login User              ${XIQSE_USERNAME}  ${XIQSE_PASSWORD}
    Should Be Equal As Integers                     ${valid_result}     1

    Log Out of XIQSE and Confirm Success
    [Teardown]  Quit Browser and Confirm Success


*** Keywords ***
Log In and Set Up Test
    [Documentation]     Logs in and configures everything that is required for the test to run

    Log Into XIQSE and Close Panels                 ${XIQSE_USERNAME}    ${XIQSE_PASSWORD}    url=${XIQSE_URL}
    Onboard XIQSE To XIQ If In Connected Mode        ${INSTALL_MODE}  ${XIQSE_IP_ADDRESS}  ${XIQ_EMAIL}  ${XIQ_PASSWORD}
    Log Out of XIQSE and Quit Browser

Tear Down Test and Close Session
    [Documentation]     Logs in and cleans up all items that were set up for the test

    Remove XIQSE From XIQ If In Connected Mode        ${INSTALL_MODE}  ${XIQ_EMAIL}  ${XIQ_PASSWORD}  ${XIQ_URL}  ${XIQSE_MAC}