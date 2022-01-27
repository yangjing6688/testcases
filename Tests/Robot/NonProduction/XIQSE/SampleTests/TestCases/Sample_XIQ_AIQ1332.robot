#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Heidi S. White
# Description   : Test Suite for sanity testing of basic XIQ functionality.
#                 Logs into XIQ, navigates to the Manage> Devices view, exercises various licensing keywords,
#                 and logs out of XIQ.  NOTE: "Test 4: Confirm License Counts" assumes no licenses are consumed.
#                 This is qTest TC-898 in the XIQ-SE project.

*** Settings ***
Resource        ../../SampleTests/Resources/AllResources.robot

Force Tags      testbed_0_node

Suite Setup      Start Test
Suite Teardown   End Test


*** Variables ***
${ENV}                    environment.remote.chrome.windows.xiqse1.yaml
${TOPO}                   topo.test.xiqse1.connected.yaml
${TESTBED}                SALEM/Dev/devices-salem-acceptance.yaml

${XIQ_URL}                ${xiq.test_url}
${XIQ_USER}               ${xiq.tenant_username}
${XIQ_PASSWORD}           ${xiq.tenant_password}

${PILOT_ENTITLEMENT}      ${xiq.pilot_entitlements}
${NAVIGATOR_ENTITLEMENT}  ${xiq.navigator_entitlements}

${PILOT_LICENSE}          PRD-XIQ-PIL-S-C
${NAVIGATOR_LICENSE}      PRD-XIQ-NAV-S-C


*** Test Cases ***
Test 1: Navigate to XIQ Manage> Devices
    [Documentation]     Confirms navigating to the Manage> Devices view of XIQ is successful
    [Tags]              xiqse_tc_898    aiq_1332    development    sample    xiqse    xiq    test1

    Navigate to XIQ Devices and Confirm Success

Test 2: Log License Information
    [Documentation]     Logs the license information from the Copilot Dashboard page
    [Tags]              xiqse_tc_898    aiq_1332    development    sample    xiqse    xiq    test2

    Log License Information From CoPilot Dashboard

Test 3: Get License Counts from CoPilot Dashboard
    [Documentation]     Obtains the license counts from the Copilot Dashboard page and prints the values
    [Tags]              xiqse_tc_898    aiq_1332    development    sample    xiqse    xiq    test3

    ${pilot_entitled}=  Get Total Pilot License Entitlements From CoPilot Dashboard
    Log To Console  Pilots Entitled: ${pilot_entitled}

    ${pilot_available}=  Get Pilot License Available Count From CoPilot Dashboard
    Log To Console  Pilots Available: ${pilot_available}

    ${pilot_consumed}=  Get Pilot License Consumed Count From CoPilot Dashboard
    Log To Console  Pilots Consumed: ${pilot_consumed}

    ${navigator_entitled}=  Get Total Navigator License Entitlements From CoPilot Dashboard
    Log To Console  Navigators Entitled: ${navigator_entitled}

    ${navigator_available}=  Get Navigator License Available Count From CoPilot Dashboard
    Log To Console  Navigators Available: ${navigator_available}

    ${navigator_consumed}=  Get Navigator License Consumed Count From CoPilot Dashboard
    Log To Console  Navigators Consumed: ${navigator_consumed}

Test 4: Confirm License Counts
    [Documentation]     Confirms the license counts match what is expected.
    ...                 This test assumes there are currently no licenses consumed.
    [Tags]              xiqse_tc_898    aiq_1332    development    sample    xiqse    xiq    test4

    Confirm Expected Pilot Licenses Consumed      ${PILOT_ENTITLEMENT}      0  ${PILOT_LICENSE}
    Confirm Expected Navigator Licenses Consumed  ${NAVIGATOR_ENTITLEMENT}  0  ${NAVIGATOR_LICENSE}


*** Keywords ***
Start Test
    [Documentation]     Starts the test session by logging into XIQ

    Log Into XIQ and Confirm Success    ${XIQ_USER}  ${XIQ_PASSWORD}  ${XIQ_URL}

End Test
    [Documentation]     Ends the test session by logging out of XIQ and closing the browser

    Log Out of XIQ and Confirm Success
    Quit XIQ Browser and Confirm Success
