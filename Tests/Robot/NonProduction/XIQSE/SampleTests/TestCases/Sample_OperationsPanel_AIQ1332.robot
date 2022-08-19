#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Heidi S. White
# Description   : Test Suite for sanity testing of basic XIQ-SE Operations Panel functionality.
#                 This is qTest TC-895 in the XIQ-SE project.

*** Settings ***
Library         common/Screen.py

Resource        ../../SampleTests/Resources/AllResources.robot

Force Tags      testbed_1_node

Suite Setup     Log In and Set Up Test
Suite Teardown  Tear Down Test and Close Session


*** Variables ***
${ENV}                  environment.remote.chrome.windows.xiqse1.yaml
${TOPO}                 topo.test.xiqse1.connected.yaml
${TESTBED}              SALEM/Dev/devices-salem-acceptance.yaml

${XIQSE_URL}            ${xiqse.url}
${XIQSE_USER}           ${xiqse.user}
${XIQSE_PASSWORD}       ${xiqse.password}

${DUT_IP}               ${netelem1.ip}
${DUT_PROFILE}          ${netelem1.profile}


*** Test Cases ***
Test 1: Open and Close Operations Panel
    [Documentation]     Confirms the Operations Panel can be opened and closed
    [Tags]              tcxe_895    aiq_1332    development    sample    xiqse    ops_panel    test1

    Open Operations Panel and Confirm Success
    Save Screen Shot
    Close Operations Panel and Confirm Success
    Save Screen Shot

Test 2: Confirm Operations Panel Message
    [Documentation]     Confirms the expected message is displayed in the Operations Panel
    [Tags]              tcxe_895    aiq_1332    development    sample    xiqse    ops_panel    test2

    [Setup]  Navigate and Create Device  ${DUT_IP}  ${DUT_PROFILE}

    Open Operations Panel and Confirm Success
    Save Screen Shot
    Wait For Operations Panel Operation To Complete  Device Added
    Confirm Operations Panel Message For Type  Device Added  Completed
    Save Screen Shot

    [Teardown]  Run Keywords
    ...  Navigate and Delete Device  ${DUT_IP}
    ...  AND
    ...  Wait For Operations Panel Operation To Complete  Device Removed
    ...  AND
    ...  Wait For Operations Panel Operation To Complete  Device License Check

Test 3: Clear Operations Panel
    [Documentation]     Confirms the Operations Panel can be cleared
    [Tags]              tcxe_895    aiq_1332    development    sample    xiqse    ops_panel    test3

    Clear Operations Panel and Confirm Success
    Confirm Operations Panel is Empty
    Save Screen Shot

    [Teardown]  Close Operations Panel and Confirm Success

Test 4: Clear Empty Operations Panel
    [Documentation]     Confirms clearing an empty Operations Panel does not result in a failure
    [Tags]              tcxe_895    aiq_1332    development    sample    xiqse    ops_panel    test4

    Clear Operations Panel and Confirm Success
    Save Screen Shot
    Confirm Operations Panel is Empty

    Clear Operations Panel and Confirm Success
    Save Screen Shot
    Confirm Operations Panel is Empty

    [Teardown]  Close Operations Panel and Confirm Success


*** Keywords ***
Log In and Set Up Test
    [Documentation]     Logs in and sets up the components for the test

    # Log into XIQSE and close any banner messages and help panel, if displayed
    Log Into XIQSE and Confirm Success  ${XIQSE_USER}  ${XIQSE_PASSWORD}  url=${XIQSE_URL}
    Close Panels on Login If Displayed

Tear Down Test and Close Session
    [Documentation]     Cleans up XIQSE test components and closes the browser

    # Log out and close the browser
    Log Out of XIQSE and Quit Browser
