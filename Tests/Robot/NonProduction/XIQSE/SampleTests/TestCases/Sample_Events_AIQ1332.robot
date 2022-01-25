#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Heidi S. White
# Description   : Test Suite for sanity testing of basic XIQ-SE events functionality.
#                 This is qTest TC-137 in the XIQ-SE project.

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
Test 1: Set Time Range
    [Documentation]     Confirms the events time range can be specified
    [Tags]              xiqse_tc_137    aiq_1332    development    sample    xiqse    events    test1

    [Setup]  Navigate to Events and Confirm Success

    Set Event Time Range and Confirm Success  Last 4 Weeks
    Set Event Time Range and Confirm Success  Last 2 Weeks
    Set Event Time Range and Confirm Success  Last Week
    Set Event Time Range and Confirm Success  Last 3 Days
    Set Event Time Range and Confirm Success  Last 24 Hours
    Set Event Time Range and Confirm Success  Last 12 Hours
    Set Event Time Range and Confirm Success  Last 6 Hours
    Set Event Time Range and Confirm Success  Last 2 Hours
    Set Event Time Range and Confirm Success  Last Hour
    Set Event Time Range and Confirm Success  Last 30 Minutes
    Set Event Time Range and Confirm Success  Yesterday
    Set Event Time Range and Confirm Success  Today
    Set Event Time Range and Confirm Success  Custom
    sleep  1 second

    [Teardown]  Set Event Time Range and Confirm Success  All

Test 2: Set Type
    [Documentation]     Confirms the events type can be specified
    [Tags]              xiqse_tc_137    aiq_1332    development    sample    xiqse    events    test2

    [Setup]  Navigate to Events and Confirm Success

    Set Event Type and Confirm Success  Console,Console View,Admin
    Set Event Type and Confirm Success  Traps,Syslog

    [Teardown]  Set Event Type and Confirm Success  All

Test 3: Search Events
    [Documentation]     Confirms the events view can be searched
    [Tags]              xiqse_tc_137    aiq_1332    development    sample    xiqse    events    test3

    [Setup]  Navigate to Events and Confirm Success

    Set Event Search String and Confirm Success     User Connection
    Clear Event Search String and Confirm Success

Test 4: Confirm Events
    [Documentation]     Confirms the events view contains the expected event
    [Tags]              xiqse_tc_137    aiq_1332    development    sample    xiqse    events    test4

    [Setup]  Navigate to Events and Confirm Success

    Set Event Time Range and Confirm Success        Last 30 Minutes
    Set Event Type and Confirm Success              Admin
    Set Event Search String and Confirm Success     Authentication

    Confirm Event Row Contains Text                 Authentication successful

    [Teardown]  Reset Events Tab


*** Keywords ***
Reset Events Tab
    [Documentation]     Resets the event tabs to the default values

    Clear Event Search String and Confirm Success
    Set Event Type and Confirm Success              All
    Set Event Time Range and Confirm Success        All
