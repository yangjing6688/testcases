#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Heidi S. White
# Description   : Test Suite for sanity testing of basic XIQ-SE analytics functionality.
#                 This is qTest TC-888 in the XIQ-SE project.

*** Settings ***
Resource        ../../SampleTests/Resources/AllResources.robot

Force Tags      testbed_0_node

Suite Setup     Log Into XIQSE and Close Panels  ${XIQSE_USER}  ${XIQSE_PASSWORD}  url=${XIQSE_URL}
Suite Teardown  Log Out of XIQSE and Quit Browser


*** Variables ***
${ENV}                  environment.remote.chrome.windows.xiqse1.yaml
${TOPO}                 topo.test.xiqse1.connected.yaml
${TESTBED}              SALEM/Dev/devices-salem-acceptance.yaml

${XIQSE_URL}            ${xiqse.url}
${XIQSE_USER}           ${xiqse.user}
${XIQSE_PASSWORD}       ${xiqse.password}

${NEXTGEN_IP}           ${nextgen.ip}
${NEXTGEN_NAME}         ${nextgen.name}
${APPLIANCE_PROFILE}    snmp_v3_profile


*** Test Cases ***
Test 1: Create Analytics Engine and Confirm Success
    [Documentation]     Creates an analytics engine and confirms the action was successful
    [Tags]              tcxe_888    aiq_1332    development    sample    xiqse    analytics    test1

    Navigate and Add Analytics Engine  ${NEXTGEN_IP}  ${NEXTGEN_NAME}  ${APPLIANCE_PROFILE}

Test 2: Confirm Adding Duplicate Analytics Engine Does Not Fail Test
    [Documentation]     Creates a duplicate analytics engine and confirms the test does not fail
    [Tags]              tcxe_888    aiq_1332    development    sample    xiqse    analytics    test2

    Navigate and Add Analytics Engine  ${NEXTGEN_IP}  ${NEXTGEN_NAME}  ${APPLIANCE_PROFILE}

Test 3: Delete Analytics Engine and Confirm Success
    [Documentation]     Confirms an engine can be deleted
    [Tags]              tcxe_888    aiq_1332    development    sample    xiqse    analytics    test3

    Navigate and Delete Analytics Engine  ${NEXTGEN_IP}
