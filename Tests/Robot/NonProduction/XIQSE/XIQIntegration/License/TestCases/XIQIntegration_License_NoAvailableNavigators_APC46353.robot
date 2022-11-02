#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Heidi S. White
# Description   : Test Suite for testing licensing when no navigator licenses are available.
#                 This test encompasses the Jira story APC-46353 (Testing: XIQSE to XIQ with Licensing)
#                 and the following qTest test cases in the CSIT project, located in the folder
#                 System Testing> Gemalto Licensing> APC-46353 - Testing: XIQ-SE to XIQ with licensing>
#                 With No Available Navigators:
#                   TC-11468: With No Navigator> Add non-Extreme device
#                   TC-11465: With No Navigator, No Pilots> Add non-Extreme
#                   TC-11462: With Not Enough Navigator> Add non-Extreme

*** Settings ***
Library         xiq/flows/manage/FilterManageDevices.py
Library         xiqse/flows/common/XIQSE_CommonTable.py
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

${NAV1_IP}                ${netelem4.ip}
${NAV1_PROFILE}           ${netelem4.profile}

${NAV2_IP}                ${netelem5.ip}
${NAV2_PROFILE}           ${netelem5.profile}
${NAV2_SERIAL}            ${netelem5.serial}

${NAV3_IP}                ${netelem6.ip}
${NAV3_PROFILE}           ${netelem6.profile}
${NAV3_SERIAL}            ${netelem6.serial}

${PILOT_ENTITLEMENT}      ${xiq.pilot_entitlements}
${NAVIGATOR_ENTITLEMENT}  ${xiq.navigator_entitlements}

${PILOT_LICENSE}          PRD-XIQ-PIL-S-C
${NAVIGATOR_LICENSE}      PRD-XIQ-NAV-S-C

${NAV_SITE}               AutoSiteNavigators
${PILOT_SITE}             AutoSitePilots
${WORLD_SITE}             World


*** Test Cases ***
Test 1: TC-11468 - With No Navigator> Add non-Extreme device
    [Documentation]     Confirms functionality surrounding adding a non-Extreme device when no navigator licenses are available
    [Tags]              staging_testing    release_testing    license_testing    tccs_11468    apc_46353    development    xiqse    xiq_integration    no_navigators    test1

    # Navigate to the Devices tab for the test site
    XIQSE Navigate to Site Devices and Confirm Success  ${NAV_SITE}

    # Create a navigator device and confirm the device is added to XIQSE
    XIQSE Add Device and Confirm Success  ${NAV3_IP}  ${NAV3_PROFILE}

    # Confirm the device is onboarded to XIQ
    XIQSE Confirm Devices Onboarded  ${NAV3_IP}
    XIQ Confirm Devices Onboarded    ${NAV3_SERIAL}

    # Confirm the device is shown to be using a pilot license in the Devices table
    XIQ Confirm Device License       ${NAV3_SERIAL}  Pilot

    # Confirm a Pilot entitlement is used for this device (1 for XIQSE, and 1 for the device, so a total of 2),
    # and all Navigator licenses are consumed
    XIQ Confirm Expected Pilot Licenses Consumed        2
    XIQ Confirm Expected Navigator Licenses Consumed    ${NAVIGATOR_ENTITLEMENT}

    [Teardown]  Delete Device and Confirm Expected License Counts  ${NAV3_IP}  1  ${NAVIGATOR_ENTITLEMENT}

Test 2: TC-11465 - With No Navigator, No Pilots> Add non-Extreme
    [Documentation]     Confirms functionality surrounding adding a non-Extreme device when no licenses (navigator or pilot) are available
    [Tags]              staging_testing    release_testing    license_testing    tccs_11465    apc_46353    development    xiqse    xiq_integration    no_navigators    test2

    [Setup]    Consume All Pilot Licenses and Confirm Success

    # Navigate to the Devices tab for the test site
    XIQSE Navigate to Site Devices and Confirm Success  ${NAV_SITE}

    # Confirm the device is not added to XIQSE
    XIQSE Add Device and Confirm Not Added  ${NAV3_IP}  ${NAV3_PROFILE}

    # Check that the user is notified about the add failure
    Run Keyword If  '21.4' in '${XIQSE_OS_VERSION}'
    ...  XIQSE Confirm License Device Limit Exceeded Event Generated For Device    ${NAV3_IP}
    ...  ELSE
    ...  XIQSE Confirm User Informed License Limit Exceeded

    # Confirm the device is not onboarded to XIQ
    XIQ Confirm Devices Not Onboarded  ${NAV3_SERIAL}

    [Teardown]    Delete All Pilot Devices and Confirm Success

Test 3: TC-11462 - With Not Enough Navigator> Add non-Extreme
    [Documentation]     Confirms functionality surrounding adding a non-Extreme device when not enough navigator licenses are available
    [Tags]              staging_testing    release_testing    license_testing    tccs_11462    apc_46353    development    xiqse    xiq_integration    no_navigators    test3

    # Delete one of the navigator devices to get back one navigator license entitlement
    XIQSE Navigate to Site Devices and Confirm Success  ${NAV_SITE}
    Delete XIQSE Test Device and Confirm Success  ${NAV2_IP}

    # Confirm the expected entitlements are available (only 1 Navigator license and 1 Pilot license should be consumed)
    XIQ Confirm Expected Pilot Licenses Consumed        1
    XIQ Confirm Expected Navigator Licenses Consumed    1

    # Perform a discovery for 2 Navigator devices
    XIQSE Navigate to Site Tab and Confirm Success  ${NAV_SITE}
    Clear Operations Panel and Confirm Success
    Perform IP Range Discovery and Confirm Success  ${NAV2_IP}  ${NAV3_IP}  ${NAV2_PROFILE}  auto_add=true

    # Obtain the discovered device count and confirm it is what we expect (2)
    ${device_count}=  XIQSE Operations Get Discovered Device Count
    Should Be Equal As Integers  ${device_count}  2

    # Confirm both devices were added to XIQSE
    XIQSE Confirm Devices Added  ${NAV2_IP}  ${NAV3_IP}

    # Confirm both devices were onboarded to XIQ
    XIQSE Confirm Devices Onboarded  ${NAV2_IP}  ${NAV3_IP}
    XIQ Confirm Devices Onboarded    ${NAV2_SERIAL}  ${NAV3_SERIAL}

    # Confirm a Pilot entitlement is used for the extra device (1 for XIQSE, and 1 for the device, so a total of 2),
    # and confirm all Navigator entitlements are used.
    XIQ Confirm Expected Pilot Licenses Consumed        2
    XIQ Confirm Expected Navigator Licenses Consumed    ${NAVIGATOR_ENTITLEMENT}


*** Keywords ***
Log In and Set Up Test
    [Documentation]     Logs in and sets up the components for the test

    XIQSE Log In and Set Window Index
    Set Up XIQSE Components

    XIQ Log In and Set Window Index
    Set Up XIQ Components

    Onboard XIQ Site Engine and Confirm Success

    Consume All Navigator Licenses and Confirm Success

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

    # Confirm we have the expected number of available entitlements
    XIQ Confirm Expected Pilot Licenses Consumed        0
    XIQ Confirm Expected Navigator Licenses Consumed    0

Consume All Navigator Licenses and Confirm Success
    [Documentation]     Creates enough devices to consume all available navigator licenses

    XIQSE Navigate to Site Devices and Confirm Success  ${NAV_SITE}

    # Since there is a known issue where sometimes the license limit exceeded message is displayed when a device
    # is added when it shouldn't be (that is, licenses are in fact available - XMC-5262), repeat the first call
    # to Add Device twice with a minute between each call.  Typically, just retrying this one time will work the
    # second time.  This known issue can't be handled with the "known_issue" tag since this step is done during the
    # Suite Setup step.
    Wait Until Keyword Succeeds  2x  60s  Run Keywords
    ...  XIQSE Close License Limit Warning Message
    ...  AND
    ...  XIQSE Add Device and Confirm Success           ${NAV1_IP}  ${NAV1_PROFILE}
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

XIQ Confirm Device License
    [Documentation]  Confirms the specified device has the expected license in the Devices table's DEVICE LICENSE colunm
    [Arguments]      ${serial}  ${license}

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Navigate to XIQ Devices and Confirm Success

    ${result}=  Get Device Details  ${serial}  DEVICE LICENSE
    Should Be Equal                 ${result}  ${license}

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

XIQSE Add Device and Confirm Not Added
    [Documentation]     Adds a device to XIQSE and confirms it is NOT added to the Devices table
    [Arguments]         ${ip}  ${profile}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Clear Operations Panel and Confirm Success

    Add Device and Wait for Operation to Complete  ${ip}  ${profile}

    XIQSE Confirm Devices Not Added      ${ip}

XIQSE Confirm Devices Added
    [Documentation]     Confirms the specified devices are present in XIQSE
    [Arguments]         @{ip_list}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Navigate to Devices and Confirm Success
    FOR  ${ip}  IN  @{ip_list}
        Confirm IP Address Present in Devices Table  ${ip}
    END

XIQSE Confirm Devices Not Added
    [Documentation]     Confirms the specified devices are not present in XIQSE
    [Arguments]         @{ip_list}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Navigate to Devices and Confirm Success
    FOR  ${ip}  IN  @{ip_list}
        Confirm IP Address Not Present in Devices Table  ${ip}
    END

XIQSE Confirm Devices Onboarded
    [Documentation]     Confirms the specified devices are marked as onboarded to XIQ
    [Arguments]         @{ip_list}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Navigate to Devices and Confirm Success
    FOR  ${ip}  IN  @{ip_list}
        Confirm XIQSE Device Onboarded to XIQ  ${ip}
    END

XIQ Confirm Devices Onboarded
    [Documentation]     Confirms the specified devices are present in XIQ
    [Arguments]         @{serial_list}

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Navigate to XIQ Devices and Confirm Success
    FOR  ${serial}  IN  @{serial_list}
        Confirm Device Serial Present  ${serial}
    END

XIQ Confirm Devices Not Onboarded
    [Documentation]     Confirms the specified devices are not present in XIQ
    [Arguments]         @{serial_list}

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Navigate to XIQ Devices and Confirm Success
    FOR  ${serial}  IN  @{serial_list}
        Confirm Device Serial Not Present  ${serial}
    END

XIQSE Confirm User Informed License Limit Exceeded
    [Documentation]     Confirms the user is informed that the device license limit has been exceeded

    Run Keyword If  '21.' in '${XIQSE_OS_VERSION}'
    ...  Run Keywords
    ...      Confirm License Limit Warning Message Displayed
    ...      AND
    ...      Close License Limit Warning Message
    ...      ELSE
    ...      Confirm Operations Panel Message For Type  Device Added  No licenses available

XIQSE Confirm License Device Limit Exceeded Event Generated For Device
    [Documentation]     Confirms the License Device Limit Exceeded event exists for the specified device
    [Arguments]         ${ip}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Navigate to Events and Confirm Success
    Set Event Time Range and Confirm Success        Last 30 Minutes
    Set Event Type and Confirm Success              Console
    Set Event Search String and Confirm Success     Device Add Failure

    ${col_result}=  XIQSE Table Set Column Filter   Source  ${ip}
    Should Be Equal As Integers                     ${col_result}  1

    Confirm Event Row Contains Text                 License Device Limit Exceeded

    [Teardown]  XIQSE Reset Events Page

XIQSE Reset Events Page
    [Documentation]     Resets the Time Range, Type, Search, and Column Filters applied to the Events page

    ${col_result}=  XIQSE Table Remove Column Filter    Source
    Should Be Equal As Integers                         ${col_result}  1

    Clear Event Search String and Confirm Success
    Set Event Type and Confirm Success                  All
    Set Event Time Range and Confirm Success            All

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

Delete All Pilot Devices and Confirm Success
    [Documentation]     Deletes all the devices consuming Pilot licenses and confirms success

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    XIQSE Delete All Site Devices and Confirm Success   ${PILOT_SITE}
    XIQ Confirm Expected Pilot Licenses Consumed  1

Delete Device and Confirm Expected License Counts
    [Documentation]     Deletes the specified device and confirms the license counts are at expected values
    [Arguments]         ${ip}  ${pilots}  ${navs}

    Delete XIQSE Test Device and Confirm Success  ${ip}

    # Confirm expected license counts
    XIQ Confirm Expected Pilot Licenses Consumed        ${pilots}
    XIQ Confirm Expected Navigator Licenses Consumed    ${navs}

Clean Up XIQ Components
    [Documentation]     Cleans up components used in XIQ during the test and logs out

    Switch To Window    ${XIQ_WINDOW_INDEX}

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
