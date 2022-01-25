#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : ??? NAME ???
# Description   : Test Suite for sanity testing of basic XIQ-SE ??? AREA ??? functionality.
#                 This is qTest TC-### in the XIQ-SE project.

*** Settings ***
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

${DUT1_IP}              ${netelem1.ip}
${DUT1_PROFILE}         ${netelem1.profile}


*** Test Cases ***
Test 1: This is the First Test
    [Documentation]     This is the first test
    [Tags]              xiqse_tc_###    aiq_1332    development    sample    xiqse    skeleton    test1

    [Setup]  Log To Console  This is a setup step which will always run at the beginning of this test case

    Log To Console  This is test 1 - add steps to do something useful

    [Teardown]  Log To Console  This is a teardown step which will always run at the end of this test case


*** Keywords ***
Log In and Set Up Test
    [Documentation]     Logs in and sets up the components for the test

    # Log into XIQSE and close any banner messages and help panel, if displayed
    Log Into XIQSE and Confirm Success  ${XIQSE_USER}  ${XIQSE_PASSWORD}  url=${XIQSE_URL}
    Close Panels on Login If Displayed

    # Create the test device
    Navigate and Create Device  ${DUT1_IP}  ${DUT1_PROFILE}

Tear Down Test and Close Session
    [Documentation]     Cleans up XIQSE test components and closes the browser

    # Clean up the test device
    Navigate and Delete Device  ${DUT1_IP}

    # Log out and close the browser
    Log Out of XIQSE and Quit Browser
