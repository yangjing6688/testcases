#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Heidi S. White
# Description   : Test Suite for testing licensing functionality when devices are deleted.
#                 This test encompasses the Jira story APC-46353 (Testing: XIQSE to XIQ with Licensing)
#                 and the following qTest test cases in the CSIT project, located in the folder
#                 System Testing> Gemalto Licensing> APC-46353 - Testing: XIQ-SE to XIQ with licensing>
#                 Delete (return license):
#                   TC-11461: Delete Navigator Devices from XIQSE
#                   TC-11458: Delete Pilot Devices form XIQSE
#                   TC-11476: Delete Navigator Device Taking Pilot License from XIQSE
#                   TC-11474: Delete Device Not Using a License from XIQSE
#                   TC-11475: Delete XIQSE with Navigator and Pilot Devices from XIQ

*** Settings ***
Library         xiq/flows/manage/FilterManageDevices.py
Library         xiqse/flows/network/devices/tree_panel/XIQSE_NetworkDevicesTreePanel.py

Resource        ../../License/Resources/AllResources.robot

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
${XIQSE_MAC}              ${xiqse.mac}

${XIQ_URL}                ${xiq.test_url}
${XIQ_USER}               ${xiq.tenant_username}
${XIQ_PASSWORD}           ${xiq.tenant_password}

${PILOT_IP_START}         ${netelem7.ip}
${PILOT_IP_END}           ${netelem8.ip}
${PILOT_PROFILE}          ${netelem7.profile}

${PIL1_IP}                ${netelem1.ip}
${PIL1_PROFILE}           ${netelem1.profile}

${PIL2_IP}                ${netelem2.ip}
${PIL2_PROFILE}           ${netelem2.profile}

${PIL3_IP}                ${netelem3.ip}
${PIL3_PROFILE}           ${netelem3.profile}

${NAV1_IP}                ${netelem4.ip}
${NAV1_PROFILE}           ${netelem4.profile}

${NAV2_IP}                ${netelem5.ip}
${NAV2_PROFILE}           ${netelem5.profile}

${NAV3_IP}                ${netelem6.ip}
${NAV3_PROFILE}           ${netelem6.profile}

${PILOT_ENTITLEMENT}      ${xiq.pilot_entitlements}
${NAVIGATOR_ENTITLEMENT}  ${xiq.navigator_entitlements}

${PILOT_LICENSE}          XIQ-PIL-S-C
${NAVIGATOR_LICENSE}      XIQ-NAV-S-C

${NAV_SITE}               AutoSiteNavigators
${PILOT_SITE}             AutoSitePilots
${WORLD_SITE}             World


*** Test Cases ***
Test 1: TC-11461 - Delete Navigator Devices from XIQSE
    [Documentation]     Confirms Navigator licenses are returned when devices are deleted.
    [Tags]              nightly3    staging_testing    release_testing    license_testing    known_issue    tccs_11461    apc_46353    development    xiqse    xiq_integration    delete    test1

    Log To Console  KNOWN ISSUE: XMC-5262 (banner says no licenses available even though there are)

    # Create devices to consume all Navigator licenses and confirm the entitlements are used up
    Consume All Navigator Licenses and Confirm Success

    # Delete all the devices consuming Navigator licenses
    XIQSE Delete All Site Devices and Confirm Success  ${NAV_SITE}

    # Confirm the Navigator entitlements are no longer consumed
    XIQ Confirm Expected Navigator Licenses Consumed  0

Test 2: TC-11458 - Delete Pilot Devices form XIQSE
    [Documentation]     Confirms Pilot licenses are returned when devices are deleted
    [Tags]              nightly3    staging_testing    release_testing    license_testing    tccs_11458    apc_46353    development    xiqse    xiq_integration    delete    test2

    # Create devices to consume all Pilot licenses and confirm the entitlements are used up
    Consume All Pilot Licenses and Confirm Success

    # Delete all the devices consuming Pilot licenses
    XIQSE Delete All Site Devices and Confirm Success   ${PILOT_SITE}

    # Confirm the Pilot entitlements are no longer consumed (there should only be 1 used for XIQSE)
    XIQ Confirm Expected Pilot Licenses Consumed  1

Test 3: TC-11476 - Delete Navigator Device Taking Pilot License from XIQSE
    [Documentation]     Confirms the correct license is returned when a Navigator device consuming a Pilot is deleted.
    [Tags]              nightly3    staging_testing    release_testing    license_testing    known_issue    tccs_11476    apc_46353    development    xiqse    xiq_integration    delete    test3

    [Setup]  Consume All Navigator Licenses and Confirm Success

    # The known issue is XMC-5262 (banner says no licenses available even though there are)

    # Create a Navigator device which will end up consuming a Pilot license since no Navigator licenses are left
    XIQSE Navigate to Site Devices and Confirm Success  ${NAV_SITE}
    XIQSE Add Device and Confirm Success                ${NAV3_IP}  ${NAV3_PROFILE}

    # Confirm the Pilot entitlements are at the expected value (2, one for XIQSE and one for the additional device)
    XIQ Confirm Expected Pilot Licenses Consumed  2

    # Delete the Navigator device consuming the Pilot license
    Delete XIQSE Test Device and Confirm Success  ${NAV3_IP}

    # Confirm the Navigator entitlements are at the expected value (still all consumed)
    XIQ Confirm Expected Navigator Licenses Consumed    ${NAVIGATOR_ENTITLEMENT}

    # Confirm the Pilot entitlements are at the expected value (there should only be 1 used for XIQSE)
    XIQ Confirm Expected Pilot Licenses Consumed  1

    [Teardown]  XIQSE Delete All Site Devices and Confirm Success   ${NAV_SITE}

Test 4: TC-11474 - Delete Device Not Using a License from XIQSE
    [Documentation]     Confirms deleting devices not consuming a license does not affect the license counts.
    [Tags]              nightly3    staging_testing    release_testing    license_testing    tccs_11474    apc_46353    development    xiqse    xiq_integration    delete    test4

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    # Create a device which will use a Pilot license
    Navigate to Site Devices and Confirm Success        ${PILOT_SITE}
    Create Device and Confirm Success                   ${PIL1_IP}  ${PIL1_PROFILE}

    # Create a device which will use a Navigator license
    Navigate to Site Devices and Confirm Success        ${NAV_SITE}
    Create Device and Confirm Success                   ${NAV1_IP}  ${NAV1_PROFILE}

    # Confirm the expected license entitlements were used for the devices (2 pilot, 1 navigator)
    XIQ Confirm Expected Pilot Licenses Consumed        2
    XIQ Confirm Expected Navigator Licenses Consumed    1

    # Create some status-only devices
    Switch To Window  ${XIQSE_WINDOW_INDEX}
    Navigate to Site Devices and Confirm Success        World
    Create Status Only Device and Confirm Success       ${PIL2_IP}  ${PIL2_PROFILE}
    Create Status Only Device and Confirm Success       ${PIL3_IP}  ${PIL3_PROFILE}
    Create Status Only Device and Confirm Success       ${NAV2_IP}  ${NAV2_PROFILE}
    Create Status Only Device and Confirm Success       ${NAV3_IP}  ${NAV3_PROFILE}

    # Confirm no license entitlements were used for the status-only devices (should be same values as before)
    XIQ Confirm Expected Pilot Licenses Consumed        2
    XIQ Confirm Expected Navigator Licenses Consumed    1

    # Delete all of the status-only devices
    Switch To Window  ${XIQSE_WINDOW_INDEX}
    Navigate to Site Devices and Confirm Success        World
    Delete Device and Confirm Success                   ${PIL2_IP}
    Delete Device and Confirm Success                   ${PIL3_IP}
    Delete Device and Confirm Success                   ${NAV2_IP}
    Delete Device and Confirm Success                   ${NAV3_IP}

    # Confirm the license entitlements are at the expected values (should be same values as before)
    XIQ Confirm Expected Pilot Licenses Consumed        2
    XIQ Confirm Expected Navigator Licenses Consumed    1

    # Delete all the devices
    XIQSE Delete All Site Devices and Confirm Success   ${PILOT_SITE}
    XIQSE Delete All Site Devices and Confirm Success   ${NAV_SITE}

    # Confirm the license entitlements are at the expected values (should be just one Pilot for XIQSE)
    XIQ Confirm Expected Pilot Licenses Consumed        1
    XIQ Confirm Expected Navigator Licenses Consumed    0

Test 5: TC-11475 - Delete XIQSE with Navigator and Pilot Devices from XIQ
    [Documentation]     Confirms deleting XIQSE from XIQ will return all used licenses, including the license used by XIQSE.
    [Tags]              nightly3    staging_testing    release_testing    license_testing    known_issue    tccs_11475    apc_46353    development    xiqse    xiq_integration    delete    test5

    Log To Console  KNOWN ISSUE: XMC-5262 (banner says no licenses available even though there are)

    # Create devices to consume all Navigator licenses and confirm the entitlements are used up
    Consume All Navigator Licenses and Confirm Success

    # Create devices to consume all Pilot licenses and confirm the entitlements are used up
    Consume All Pilot Licenses and Confirm Success

    # Perform a search for the XIQSE model
    Navigate to XIQ Devices and Confirm Success
    Search XIQ Devices Table and Confirm Success  ${XIQSE_MAC}

    # Remove XIQSE from XIQ
    Remove Device By MAC From XIQ and Confirm Success  ${XIQSE_MAC}

    # Clear the search on the Devices table
    Clear Search on XIQ Devices Table and Confirm Success

    # Confirm all entitlements have been returned
    XIQ Confirm Expected Pilot Licenses Consumed        0
    XIQ Confirm Expected Navigator Licenses Consumed    0


*** Keywords ***
Log In and Set Up Test
    [Documentation]     Logs in and sets up the components for the test

    XIQSE Log In and Set Window Index
    Set Up XIQSE Components

    XIQ Log In and Set Window Index
    Set Up XIQ Components

    Onboard XIQ Site Engine and Confirm Success

Tear Down Test and Close Session
    [Documentation]     Cleans up XIQ and XIQSE test components and closes the browser

    Clean Up XIQSE Components
    Clean Up XIQ Components

    Quit Browser and Confirm Success

XIQSE Log In and Set Window Index
    [Documentation]     Logs into XIQSE and sets the window index

    Log Into XIQSE and Confirm Success              ${XIQSE_USER}  ${XIQSE_PASSWORD}  url=${XIQSE_URL}
    Handle License Agreement If Displayed           ${XIQ_USER}  ${XIQ_PASSWORD}

    # Close any banner messages (Connection Lost with XIQ, License Expiration, etc.) and the Help panel, if displayed
    Close Panels on Login If Displayed

    # Store the window index so we can switch between XIQSE and XIQ
    ${xiqse_win}=  XIQSE Get Window Index
    Log To Console  Setting XIQSE Window Index to ${xiqse_win}
    Set Suite Variable  ${XIQSE_WINDOW_INDEX}  ${xiqse_win}

XIQ Log In and Set Window Index
    [Documentation]     Logs into XIQ and sets the window index

    Log Into XIQ and Confirm Success    ${XIQ_USER}  ${XIQ_PASSWORD}  url=${XIQ_URL}

    ${xiq_win}=  Get Window Index
    Log To Console  Setting XIQ Window Index to ${xiq_win}
    Set Suite Variable  ${XIQ_WINDOW_INDEX}  ${xiq_win}

Set Up XIQSE Components
    [Documentation]     Sets up the XIQSE components for the test

    Disable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver    ${WORLD_SITE}

    # Make sure the correct Serial Number is being used
    Confirm XIQSE Serial Number     ${XIQSE_SERIAL}

    # Set the HTTP session timeout
    Set Option Web Server Session Timeout and Confirm Success  7  day(s)
    # Enable all columns for event searches
    Set Alarm Event Search Scope    true
    # Create the test sites
    XIQSE Create Site and Confirm Success  ${NAV_SITE}
    XIQSE Create Site and Confirm Success  ${PILOT_SITE}

Set Up XIQ Components
    [Documentation]     Sets up the XIQ components for the test

    # Remove XIQSE if it is already present
    Navigate and Remove Device by MAC From XIQ  ${XIQSE_MAC}

    # Enable CoPilot Feature
    Enable CoPilot Feature

    # Confirm we are starting with no licenses consumed
    XIQ Confirm Expected Pilot Licenses Consumed        0
    XIQ Confirm Expected Navigator Licenses Consumed    0

Consume All Navigator Licenses and Confirm Success
    [Documentation]     Creates enough devices to consume all available navigator licenses

    XIQSE Navigate to Site Devices and Confirm Success  ${NAV_SITE}
    XIQSE Add Device and Confirm Success                ${NAV1_IP}  ${NAV1_PROFILE}
    XIQSE Add Device and Confirm Success                ${NAV2_IP}  ${NAV2_PROFILE}

    XIQ Confirm Expected Navigator Licenses Consumed    ${NAVIGATOR_ENTITLEMENT}

Consume All Pilot Licenses and Confirm Success
    [Documentation]     Creates enough devices to consume all available pilot licenses

    # Perform a discovery to use up the available pilot licenses (minus 1 to leave room for XIQSE to be onboarded)
    XIQSE Navigate to Site Tab and Confirm Success                  ${PILOT_SITE}
    Clear Operations Panel and Confirm Success
    XIQSE Perform IP Range Discovery and Confirm Expected Counts    ${PILOT_IP_START}  ${PILOT_IP_END}  ${PILOT_PROFILE}

    XIQ Confirm Expected Pilot Licenses Consumed                    ${PILOT_ENTITLEMENT}

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

XIQSE Navigate to Site Tab and Confirm Success
    [Documentation]     Navigates to the specified site tab in XIQSE and confirms the action was successful
    [Arguments]         ${site}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    # Navigate to the site context
    Navigate to Site Tab and Confirm Success  ${site}

XIQSE Navigate to Site Devices and Confirm Success
    [Documentation]     Navigates to the Devices tab for the specified site in XIQSE and confirms the action was successful
    [Arguments]         ${site}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    # Navigate to the site context
    Navigate to Site Devices and Confirm Success  ${site}

XIQSE Create Site and Confirm Success
    [Documentation]     Creates the specified site under the World node
    [Arguments]  ${site}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    # Navigate to the Devices tab for the World node
    XIQSE Navigate to Site Devices and Confirm Success  World

    # Create the specified site
    Create Site and Confirm Success  ${site}

XIQSE Delete Site and Confirm Success
    [Documentation]     Deletes the specified site
    [Arguments]  ${site}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    # Navigate to the Devices tab for the World node
    XIQSE Navigate to Site Devices and Confirm Success  World

    # Delete the specified site
    Delete Site and Confirm Success  ${site}

Onboard XIQ Site Engine and Confirm Success
    [Documentation]     Confirms the XIQ Site Engine can be onboarded successfully

    Auto Onboard XIQ Site Engine
    Confirm XIQ Site Engine Onboarded to XIQ

Auto Onboard XIQ Site Engine
    [Documentation]     Onboards the specified XIQ Site Engine, deleting it first if it already exists

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Enter XIQ Credentials to Auto Onboard XIQSE  ${XIQ_USER}  ${XIQ_PASSWORD}

Confirm XIQ Site Engine Onboarded to XIQ
    [Documentation]     Confirms the XIQ Site Engine has been onboarded to XIQ successfully

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Confirm Device Serial Present   ${XIQSE_SERIAL}
    Confirm Device Serial Online    ${XIQSE_SERIAL}

XIQSE Perform IP Range Discovery and Confirm Expected Counts
    [Documentation]     Performs an IP Range discovery in XIQSE and confirms the device count is what is expected
    [Arguments]         ${ip_start}  ${ip_end}  ${profile}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Perform IP Range Discovery and Confirm Success  ${ip_start}  ${ip_end}  ${profile}  auto_add=true

    # Make sure the discovery resulted in one less than the pilot license entitlement
    # (one less since XIQSE itself will consume one pilot license)
    ${pilot_int}=  Convert To Integer  ${PILOT_ENTITLEMENT}
    ${expected_device_count}=  Evaluate  $pilot_int - 1
    ${device_count}=  XIQSE Operations Get Discovered Device Count
    Should Be Equal As Integers  ${device_count}  ${expected_device_count}

    XIQSE Devices Select Devices Tab
    ${result}=  XIQSE Wait Until Devices Present  ${device_count}
    Should Be Equal As Integers  ${result}  1

XIQSE Add Device and Confirm Success
    [Documentation]     Adds a device to XIQSE and confirms it was added successfully
    [Arguments]    ${ip}  ${profile}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Create Device and Confirm Success   ${ip}  ${profile}

XIQSE Delete All Site Devices and Confirm Success
    [Documentation]     Deletes all devices in the specified site and confirms the action is successful
    [Arguments]         ${site}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    # Navigate to the Devices tab for the site
    XIQSE Navigate to Site Devices and Confirm Success  ${site}

    # Delete all devices within the site
    ${del_result}=  XIQSE Delete All Devices
    Should Be Equal As Integers  ${del_result}  1

    # Confirm the device count is zero
    ${count_result}=  XIQSE Get Device Total Count
    Should Be Equal As Integers  ${count_result}  0

Delete XIQSE Test Device and Confirm Success
    [Documentation]     Deletes the specified device from XIQSE and confirms the action was successful
    [Arguments]         ${ip}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Navigate and Delete Device  ${ip}

Clean Up XIQ Components
    [Documentation]     Cleans up components used in XIQ during the test and logs out

    Switch To Window    ${XIQ_WINDOW_INDEX}

    # Perform a search for the XIQSE model
    Navigate to XIQ Devices and Confirm Success
    Search XIQ Devices Table and Confirm Success  ${XIQSE_MAC}

    # Delete the Site Engine from XIQ if it is still onboarded (last test case removes it)
    Remove Device By MAC From XIQ and Confirm Success  ${XIQSE_MAC}

    # Clear the search on the Devices table
    Clear Search on XIQ Devices Table and Confirm Success

    # Confirm all entitlements have been returned
    XIQ Confirm Expected Pilot Licenses Consumed        0
    XIQ Confirm Expected Navigator Licenses Consumed    0

    # Disable CoPilot Feature
    Disable CoPilot Feature

    # Log out and close the window
    [Teardown]  XIQ Log Out and Close Window

Clean Up XIQSE Components
    [Documentation]     Cleans up components used in XIQSE during the test and logs out

    Switch To Window    ${XIQSE_WINDOW_INDEX}

    Enable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver    ${WORLD_SITE}

    # Disable all columns for event searches
    Set Alarm Event Search Scope    false

    # Delete all the discovered devices from the sites
    XIQSE Delete All Site Devices and Confirm Success   ${PILOT_SITE}
    XIQSE Delete All Site Devices and Confirm Success   ${NAV_SITE}

    # Delete the test site
    XIQSE Delete Site and Confirm Success  ${PILOT_SITE}
    XIQSE Delete Site and Confirm Success  ${NAV_SITE}

    # Clear out the operations panel
    Clear Operations Panel and Confirm Success

    # Log out
    Log Out of XIQSE and Confirm Success

XIQ Log Out and Close Window
    [Documentation]     Logs out of XIQ and closes the window

    Switch To Window    ${XIQ_WINDOW_INDEX}

    Log Out of XIQ and Confirm Success
    Close Window    ${XIQ_WINDOW_INDEX}
