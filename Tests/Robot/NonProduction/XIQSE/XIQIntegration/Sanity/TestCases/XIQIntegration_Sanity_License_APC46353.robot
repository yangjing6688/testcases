#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Heidi S. White
# Description   : Test Suite for sanity testing of license-related XIQ Integration functionality.
#                 Checks license counts within XIQ after performing various activities in XIQSE,
#                 like onboarding XIQSE to XIQ, creating pilot and navigator devices in XIQSE,
#                 deleting pilot and navigator devices from XIQSE, and removing XIQSE from XIQ.
#                 This is qTest test case TC-11877 in the CSIT project, and Jira story APC-46353.

*** Settings ***
Resource        ../../Sanity/Resources/AllResources.robot

Force Tags      testbed_license_node

Suite Setup     Log In and Set Up Test
Suite Teardown  Tear Down Test and Close Session


*** Variables ***
# Defaults
${ENV}                    environment.remote.chrome.windows.xiqse1.yaml
${TOPO}                   topo.test.xiqse1.connected.yaml
${TESTBED}                RDU/Prod/rdu_xiqse_license1.yaml

${XIQSE_URL}              ${xiqse.url}
${XIQSE_USER}             ${xiqse.user}
${XIQSE_PASSWORD}         ${xiqse.password}
${XIQSE_SERIAL}           ${xiqse.serial}
${XIQSE_IP}               ${xiqse.ip}
${XIQSE_MAC}              ${xiqse.mac}

${XIQ_URL}                ${xiq.test_url}
${XIQ_USER}               ${xiq.tenant_username}
${XIQ_PASSWORD}           ${xiq.tenant_password}

${PIL1_IP}                ${pilot1.ip}
${PIL1_PROFILE}           ${pilot1.profile}
${PIL1_SERIAL}            ${pilot1.serial}

${NAV1_IP}                ${nav1.ip}
${NAV1_PROFILE}           ${nav1.profile}
${NAV1_SERIAL}            ${nav1.serial}

${PILOT_ENTITLEMENT}      ${xiq.pilot_entitlements}
${NAVIGATOR_ENTITLEMENT}  ${xiq.navigator_entitlements}

${PILOT_LICENSE}          PRD-XIQ-PIL-S-C
${NAVIGATOR_LICENSE}      PRD-XIQ-NAV-S-C
${WORLD_SITE}             World


*** Test Cases ***
Test 1: Check Baseline License Counts
    [Documentation]     Confirms license counts are at expected values in XIQ to begin with (nothing consumed)
    [Tags]              release_testing    license_testing    staging_testing    tccs_11877    apc_46353    development    xiqse    xiq_integration    license_sanity    test1

    Switch To Window  ${XIQ_WINDOW_INDEX}

    XIQ Confirm Expected Pilot Licenses Consumed        0
    XIQ Confirm Expected Navigator Licenses Consumed    0

Test 2: Onboard XIQSE to XIQ and Check License Counts
    [Documentation]     Onboards XIQSE to XIQ and confirms the license counts
    [Tags]              release_testing    license_testing    staging_testing    tccs_11877    apc_46353    development    xiqse    xiq_integration    license_sanity    test2

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Navigate to XIQ Device Message Details and Confirm Success
    Onboard XIQSE if Not Onboarded          ${XIQSE_IP}  ${XIQ_USER}  ${XIQ_PASSWORD}
    Confirm XIQSE Onboarded Successfully    ${XIQSE_IP}

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Navigate Filter and Confirm Device MAC Present  ${XIQSE_MAC}

    # Confirm license counts
    XIQ Confirm Expected Pilot Licenses Consumed        1
    XIQ Confirm Expected Navigator Licenses Consumed    0

Test 3: Create Pilot Device and Check License Counts
    [Documentation]     Creates a pilot type device in XIQSE and confirms the license counts
    [Tags]              release_testing    license_testing    staging_testing    tccs_11877    apc_46353    development    xiqse    xiq_integration    license_sanity    test3

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    XIQSE Add Device and Confirm Success    ${PIL1_IP}  ${PIL1_PROFILE}
    Confirm XIQSE Device Onboarded to XIQ   ${PIL1_IP}

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Navigate Filter and Confirm Device Serial Present   ${PIL1_SERIAL}

    # Confirm license counts
    XIQ Confirm Expected Pilot Licenses Consumed        2
    XIQ Confirm Expected Navigator Licenses Consumed    0

Test 4: Create Navigator Device and Check License Counts
    [Documentation]     Creates a navigator type device in XIQSE and confirms the license counts
    [Tags]              release_testing    license_testing    staging_testing    tccs_11877    apc_46353    development    xiqse    xiq_integration    license_sanity    test4

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    XIQSE Add Device and Confirm Success    ${NAV1_IP}  ${NAV1_PROFILE}
    Confirm XIQSE Device Onboarded to XIQ   ${NAV1_IP}

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Navigate Filter and Confirm Device Serial Present   ${NAV1_SERIAL}

    # Confirm license counts
    XIQ Confirm Expected Pilot Licenses Consumed        2
    XIQ Confirm Expected Navigator Licenses Consumed    1

Test 5: Delete Pilot Device and Check License Counts
    [Documentation]     Deletes a pilot type device in XIQSE and confirms the license counts
    [Tags]              release_testing    license_testing    staging_testing    tccs_11877    apc_46353    development    xiqse    xiq_integration    license_sanity    test5

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Delete Device and Confirm Success                       ${PIL1_IP}

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Navigate Filter and Confirm Device Serial Not Present   ${PIL1_SERIAL}

    # Confirm license counts
    XIQ Confirm Expected Pilot Licenses Consumed        1
    XIQ Confirm Expected Navigator Licenses Consumed    1

Test 6: Delete Navigator Device and Check License Counts
    [Documentation]     Deletes a navigator type device in XIQSE and confirms the license counts
    [Tags]              release_testing    license_testing    staging_testing    known_issue    tccs_11877    apc_46353    development    xiqse    xiq_integration    license_sanity    test6

    Log To Console  KNOWN ISSUE: XIQ-639

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Delete Device and Confirm Success                       ${NAV1_IP}

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Navigate Filter and Confirm Device Serial Not Present   ${NAV1_SERIAL}

    # Confirm license counts
    XIQ Confirm Expected Pilot Licenses Consumed        1
    XIQ Confirm Expected Navigator Licenses Consumed    0

Test 7: Remove XIQSE from XIQ and Check License Counts
    [Documentation]     Removes XIQSE from XIQ and confirms the license counts (nothing consumed)
    [Tags]              release_testing    license_testing    staging_testing    tccs_11877    apc_46353    development    xiqse    xiq_integration    license_sanity    test7

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Navigate and Remove Device by MAC From XIQ          ${XIQSE_MAC}

    Navigate Filter and Confirm Device MAC Not Present  ${XIQSE_MAC}

    # Confirm license counts
    XIQ Confirm Expected Pilot Licenses Consumed        0
    XIQ Confirm Expected Navigator Licenses Consumed    0


*** Keywords ***
Log In and Set Up Test
    [Documentation]     Sets up the components for the test

    XIQSE Log In and Set Window Index
    Set Up XIQSE Components

    XIQ Log In and Set Window Index
    Set Up XIQ Components

Tear Down Test and Close Session
    [Documentation]     Cleans up XIQ and XIQ-SE test components

    Clean Up XIQ Components
    Clean Up XIQSE Components
    XIQSE Quit Browser

XIQSE Log In and Set Window Index
    [Documentation]     Logs into XIQ-SE and confirms the login was successful

    Log Into XIQSE and Confirm Success              ${XIQSE_USER}  ${XIQSE_PASSWORD}  url=${XIQSE_URL}
    Handle License Agreement If Displayed           ${XIQ_USER}  ${XIQ_PASSWORD}

    # Close any banner messages (Connection Lost with XIQ, License Expiration, etc.) and the Help panel, if displayed
    Close Panels on Login If Displayed

    # Store the window index so we can switch between XIQSE and XIQ
    ${xiqse_win}=  XIQSE Get Window Index
    Log To Console  Setting XIQSE Window Index to ${xiqse_win}
    Set Suite Variable  ${XIQSE_WINDOW_INDEX}  ${xiqse_win}

XIQ Log In and Set Window Index
    [Documentation]     Logs into XIQ and confirms the login was successful

    Log Into XIQ and Confirm Success    ${XIQ_USER}  ${XIQ_PASSWORD}  ${XIQ_URL}

    ${xiq_win}=  Get Window Index
    Log To Console  Setting XIQ Window Index to ${xiq_win}
    Set Suite Variable  ${XIQ_WINDOW_INDEX}  ${xiq_win}

Set Up XIQSE Components
    [Documentation]     Sets up the XIQ-SE components for the test

    Disable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver    ${WORLD_SITE}

    # Enable all columns for event searches
    Set Alarm Event Search Scope    true

    Confirm Serial Number and Set Common Options  ${XIQSE_SERIAL}

Set Up XIQ Components
    [Documentation]     Sets up the XIQ components for the test

    # Remove XIQSE if it is already present
    Navigate and Remove Device by MAC From XIQ  ${XIQSE_MAC}

    # Enable CoPilot Feature
    Enable CoPilot Feature

    # Confirm we have the expected number of available entitlements - wait until this keyword succeeds, up to 5 minutes
    Wait Until Keyword Succeeds  10x  30s
    ...  Confirm Number of Licenses Available From CoPilot Dashboard  ${PILOT_ENTITLEMENT}  ${NAVIGATOR_ENTITLEMENT}

Clean Up XIQ Components
    [Documentation]     Cleans up components used in XIQ during the test and logs out

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Navigate and Remove Device by MAC From XIQ   ${XIQSE_MAC}

    # Disable CoPilot Feature
    Disable CoPilot Feature

    Log Out of XIQ and Confirm Success

Clean Up XIQSE Components
    [Documentation]     Cleans up components used in XIQ-SE during the test and logs out

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Enable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver    ${WORLD_SITE}

    # Disable all columns for event searches
    Set Alarm Event Search Scope    false

    Log Out of XIQSE and Confirm Success

XIQSE Add Device and Confirm Success
    [Documentation]     Adds a device to XIQSE and confirms it was added successfully
    [Arguments]    ${ip}  ${profile}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Navigate and Create Device   ${ip}  ${profile}

XIQ Confirm Expected Pilot Licenses Consumed
    [Documentation]  Confirms the expected number of pilot licenses are consumed based on entitlements
    [Arguments]      ${consumed}

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Confirm Expected Pilot Licenses Consumed  ${PILOT_ENTITLEMENT}  ${consumed}  ${PILOT_LICENSE}

XIQ Confirm Expected Navigator Licenses Consumed
    [Documentation]  Confirms the expected number of navigator licenses are consumed based on entitlements
    [Arguments]      ${consumed}

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Confirm Expected Navigator Licenses Consumed  ${NAVIGATOR_ENTITLEMENT}  ${consumed}  ${NAVIGATOR_LICENSE}
