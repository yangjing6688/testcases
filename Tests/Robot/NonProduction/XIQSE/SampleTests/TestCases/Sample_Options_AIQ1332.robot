#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Heidi S. White
# Description   : Test Suite for sanity testing of basic XIQ-SE Options functionality.
#                 This is qTest TC-135 in the XIQ-SE project.

*** Settings ***
Resource        ../../SampleTests/Resources/AllResources.robot

Force Tags      testbed_0_node

Suite Setup     Log Into XIQSE and Close Panels    ${XIQSE_USER}  ${XIQSE_PASSWORD}  url=${XIQSE_URL}
Suite Teardown  Log Out of XIQSE and Quit Browser


*** Variables ***
${ENV}                  environment.remote.chrome.windows.xiqse1.yaml
${TOPO}                 topo.test.xiqse1.connected.yaml
${TESTBED}              SALEM/Dev/devices-salem-acceptance.yaml

${XIQSE_URL}            ${xiqse.url}
${XIQSE_USER}           ${xiqse.user}
${XIQSE_PASSWORD}       ${xiqse.password}


*** Test Cases ***
Test 1: Web Server - HTTP Session Timeout
    [Documentation]     Confirms the HTTP Session Timeout option can be configured
    [Tags]              tcxe_135    aiq_1332    development    sample    xiqse    options    test1

    Set Option Web Server Session Timeout and Confirm Success  16  hr(s)
    Set Option Web Server Session Timeout and Confirm Success  45  min(s)
    Set Option Web Server Session Timeout and Confirm Success  7   day(s)

Test 2: Site Engine - General - Device Tree Name Format
    [Documentation]     Confirms the Device Tree Name Format option can be configured
    [Tags]              tcxe_135    aiq_1332    development    sample    xiqse    options    test2

    Set Option Device Tree Name Format and Confirm Success  System Name
    Set Option Device Tree Name Format and Confirm Success  Nickname
    Set Option Device Tree Name Format and Confirm Success  IP Address

Test 3: Restore Defaults
    [Documentation]     Confirms the options can be restored to the defaults
    [Tags]              tcxe_135    aiq_1332    development    sample    xiqse    options    test3

    ${result_ws}=  XIQSE Restore Default Web Server Options and Save
    Should Be Equal As Integers    ${result_ws}     1

    ${result_seg}=  XIQSE Restore Default Site Engine General Options and Save
    Should Be Equal As Integers    ${result_seg}     1
