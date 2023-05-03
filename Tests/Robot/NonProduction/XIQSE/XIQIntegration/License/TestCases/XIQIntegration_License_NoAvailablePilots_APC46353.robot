#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Heidi S. White
# Description   : Test Suite for testing licensing when no pilot licenses are available.
#                 This test encompasses the Jira story APC-46353 (Testing: XIQSE to XIQ with Licensing)
#                 and the following qTest test cases in the CSIT project, located in the folder
#                 System Testing> Gemalto Licensing> APC-46353 - Testing: XIQ-SE to XIQ with licensing>
#                 With No Available Pilots:
#                   TC-11450 - With No Pilots> Add Device
#                   TC-11449 - With No Pilots> Discover Device
#                   TC-11448 - With No Pilots> Discover Multiple Devices
#                   TC-11447 - With No Pilots> Add from Discovered
#                   TC-11454 - With No Pilots> Add "Status Only" Device
#                   TC-11455 - With No Pilots> Add Device with "Ping Only" Profile

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

${PIL1_IP}                ${netelem1.ip}
${PIL1_PROFILE}           ${netelem1.profile}
${PIL1_SERIAL}            ${netelem1.serial}

${PIL2_IP}                ${netelem2.ip}
${PIL2_PROFILE}           ${netelem2.profile}
${PIL2_SERIAL}            ${netelem2.serial}

${PIL3_IP}                ${netelem3.ip}
${PIL3_PROFILE}           ${netelem3.profile}
${PIL3_SERIAL}            ${netelem3.serial}

${NAV1_IP}                ${netelem4.ip}
${NAV1_PROFILE}           ${netelem4.profile}

${NAV2_IP}                ${netelem5.ip}
${NAV2_PROFILE}           ${netelem5.profile}

${NAV3_IP}                ${netelem6.ip}
${NAV3_PROFILE}           ${netelem6.profile}
${NAV3_SERIAL}            ${netelem6.serial}

${PILOT_ENTITLEMENT}      ${xiq.pilot_entitlements}
${NAVIGATOR_ENTITLEMENT}  ${xiq.navigator_entitlements}

${PILOT_LICENSE}          XIQ-PIL-S-C
${NAVIGATOR_LICENSE}      XIQ-NAV-S-C

${MAIN_SITE}              AutoMainSite
${TEST_SITE}              AutoTestSite
${WORLD_SITE}             World


*** Test Cases ***
Test 1: TC-11450 - With No Pilots> Add Device
    [Documentation]     Confirms functionality surrounding adding a device in XIQSE when no pilot licenses are available
    [Tags]              nightly3    staging_testing    release_testing    license_testing    tccs_11450    apc_46353    development    xiqse    xiq_integration    no_pilots    test1

    [Setup]  XIQSE Close All Banner Messages and Confirm Success

    # Navigate to the Devices tab for the main test site
    XIQSE Navigate to Site Devices and Confirm Success  ${MAIN_SITE}

    # Confirm the device is not added to XIQSE
    XIQSE Add Device and Confirm Not Added  ${NAV3_IP}  ${NAV3_PROFILE}

    # Check that the user is notified about the add failure
    Run Keyword If  '21.4' in '${XIQSE_OS_VERSION}'
    ...  XIQSE Confirm License Device Limit Exceeded Event Generated For Devices    ${NAV3_IP}
    ...  ELSE
    ...  XIQSE Confirm User Informed License Limit Exceeded

    # Confirm the device is not onboarded to XIQ
    XIQ Confirm Devices Not Onboarded  ${NAV3_SERIAL}

Test 2: TC-11449 - With No Pilots> Discover Device
    [Documentation]     Confirms functionality surrounding discovering a single device in XIQSE when no pilot licenses are available
    [Tags]              nightly3    staging_testing    release_testing    license_testing    tccs_11449    apc_46353    development    xiqse    xiq_integration    no_pilots    test2

    [Setup]  XIQSE Close All Banner Messages and Confirm Success

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    # Navigate to the Devices tab for the test site
    XIQSE Create Site and Confirm Success  ${TEST_SITE}
    XIQSE Navigate to Site Tab and Confirm Success  ${TEST_SITE}

    # Perform a discovery of one device
    XIQSE Clear Operations Panel and Confirm Success
    Perform IP Range Discovery and Ignore License Limit Error  ${PIL1_IP}  ${PIL1_IP}  ${PIL1_PROFILE}  auto_add=true

    # Confirm the discovered device count is what we expect (1)
    Confirm Discovered Device Count From Operations Panel  1

    # Confirm the device is not added to XIQSE
    XIQSE Confirm Devices Not Added  ${PIL1_IP}

    # Check that the user is notified about the add failure
    Run Keyword If  '21.4' in '${XIQSE_OS_VERSION}'
    ...  XIQSE Confirm License Device Limit Exceeded Event Generated For Devices    ${PIL1_IP}
    ...  ELSE
    ...  XIQSE Confirm Banner Message Reports License Limit Exceeded

    # Confirm the device is not onboarded to XIQ
    XIQ Confirm Devices Not Onboarded  ${PIL1_SERIAL}

    [Teardown]  XIQSE Delete Site and Confirm Success  ${TEST_SITE}

Test 3: TC-11448 - With No Pilots> Discover Multiple Devices
    [Documentation]     Confirms functionality surrounding discovering multiple devices in XIQSE when no pilot licenses are available
    [Tags]              nightly3    staging_testing    release_testing    license_testing    tccs_11448    apc_46353    development    xiqse    xiq_integration    no_pilots    test3

    [Setup]  XIQSE Close All Banner Messages and Confirm Success

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    # Navigate to the Devices tab for the test site
    XIQSE Create Site and Confirm Success  ${TEST_SITE}
    XIQSE Navigate to Site Tab and Confirm Success  ${TEST_SITE}

    # Perform a discovery of three devices
    XIQSE Clear Operations Panel and Confirm Success
    Perform IP Range Discovery and Ignore License Limit Error  ${PIL1_IP}  ${PIL3_IP}  ${PILOT_PROFILE}  auto_add=true

    # Confirm the discovered device count is what we expect (3)
    Confirm Discovered Device Count From Operations Panel  3

    # Confirm the devices are not added to XIQSE
    XIQSE Confirm Devices Not Added  ${PIL1_IP}  ${PIL2_IP}  ${PIL3_IP}

    # Check that the user is notified about the add failures
    Run Keyword If  '21.4' in '${XIQSE_OS_VERSION}'
    ...  XIQSE Confirm License Device Limit Exceeded Event Generated For Devices  ${PIL1_IP}  ${PIL2_IP}  ${PIL3_IP}
    ...  ELSE
    ...  XIQSE Confirm Banner Message Reports License Limit Exceeded

    # Confirm the devices are not onboarded to XIQ
    XIQ Confirm Devices Not Onboarded  ${PIL1_SERIAL}  ${PIL2_SERIAL}  ${PIL3_SERIAL}

    [Teardown]  XIQSE Delete Site and Confirm Success  ${TEST_SITE}

Test 4: TC-11447 - With No Pilots> Add From Discovered
    [Documentation]     Confirms functionality surrounding adding a device from the discovered tab in XIQSE when no pilot licenses are available
    [Tags]              nightly3    staging_testing    release_testing    license_testing    tccs_11447    apc_46353    development    xiqse    xiq_integration    no_pilots    test4

    [Setup]  XIQSE Close All Banner Messages and Confirm Success

    Run Keyword If  '21.4' in '${XIQSE_OS_VERSION}'
    ...  Log To Console  This test is not supported for 21.4.x XIQSE
    ...  ELSE
    ...  Confirm Add From Discovered Functionality

Test 5: TC-11454 - With No Pilots> Add "Status Only" Device
    [Documentation]     Confirms functionality surrounding adding a status only device in XIQSE when no pilot licenses are available
    [Tags]              nightly3    staging_testing    release_testing    license_testing    tccs_11454    apc_46353    development    xiqse    xiq_integration    no_pilots    test5

    [Setup]  XIQSE Close All Banner Messages and Confirm Success

    # Navigate to the Devices tab for the test site
    XIQSE Navigate to Site Devices and Confirm Success  ${MAIN_SITE}

    # Confirm a status-only device is added successfully to XIQSE
    Create Status Only Device and Confirm Success       ${NAV3_IP}  ${NAV3_PROFILE}

    # Confirm the status-only device is not onboarded to XIQ
    XIQ Confirm Devices Not Onboarded  ${NAV3_SERIAL}

    [Teardown]  Delete XIQSE Test Device and Confirm Success  ${NAV3_IP}

Test 6: TC-11455 - With No Pilots> Add "Ping Only" Device
    [Documentation]     Confirms functionality surrounding adding a ping only device in XIQSE when no pilot licenses are available
    ...                 NOTE: this test will not work against 21.4.x XIQSE
    [Tags]              nightly3    staging_testing    release_testing    license_testing    tccs_11455    apc_46353    development    xiqse    xiq_integration    no_pilots    test6

    [Setup]  XIQSE Close All Banner Messages and Confirm Success

    Run Keyword If  '21.4' in '${XIQSE_OS_VERSION}'
    ...  Log To Console  This test is not supported for 21.4.x XIQSE
    ...  ELSE
    ...  Confirm Ping Only Device Functionality


*** Keywords ***
Log In and Set Up Test
    [Documentation]     Logs in and sets up the components for the test

    XIQSE Log In and Set Window Index
    Set Up XIQSE Components

    XIQ Log In and Set Window Index
    Set Up XIQ Components

    Onboard XIQ Site Engine and Confirm Success

    Consume All Licenses and Confirm Success

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

    # Create the test site
    XIQSE Create Site and Confirm Success  ${MAIN_SITE}

Set Up XIQ Components
    [Documentation]     Sets up the XIQ components for the test

    # Remove XIQSE if it is already present
    Navigate and Remove Device by MAC From XIQ  ${XIQSE_MAC}

    # Confirm we have the expected number of available entitlements
    XIQ Confirm Expected Pilot Licenses Consumed        0
    XIQ Confirm Expected Navigator Licenses Consumed    0

Consume All Licenses and Confirm Success
    [Documentation]     Creates enough devices to consume all available licenses

    # Perform a discovery to use up the available pilot licenses (minus 1 to leave room for XIQSE to be onboarded)
    XIQSE Navigate to Site Tab and Confirm Success          ${MAIN_SITE}
    XIQSE Clear Operations Panel and Confirm Success
    Perform IP Range Discovery and Confirm Success          ${PILOT_IP_START}  ${PILOT_IP_END}  ${PILOT_PROFILE}  auto_add=true

    # NOTE: for the current release, the available Navigator licenses also must be consumed, as XIQ sends the total
    # number allowed, without separating PIL and NAV.  In the future, the PIL and NAV numbers will be sent separately,
    # so the Navigator consumption can be removed at that point.
    XIQSE Navigate to Site Devices and Confirm Success      ${MAIN_SITE}
    Create Device and Confirm Success                       ${NAV1_IP}  ${NAV1_PROFILE}
    Create Device and Confirm Success                       ${NAV2_IP}  ${NAV2_PROFILE}

    # Confirm all licenses are reported as consumed within XIQ
    XIQ Confirm All Licenses Consumed

XIQSE Navigate to Site Context and Confirm Success
    [Documentation]     Navigates to the specified site in XIQSE and confirms the action was successful
    [Arguments]         ${site}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    # Select the site in the tree
    Navigate to Site Tree Node and Confirm Success  ${site}

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

XIQSE Navigate to Discovered and Confirm Success
    [Documentation]     Navigates to the Network> Discovered view in XIQSE and confirms the action was successful

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Navigate to Discovered and Confirm Success

XIQ Confirm All Licenses Consumed
    [Documentation]     Confirms all pilot and navigator licenses are consumed based on entitlements

    Switch To Window  ${XIQ_WINDOW_INDEX}

    XIQ Confirm Expected Pilot Licenses Consumed        ${PILOT_ENTITLEMENT}
    XIQ Confirm Expected Navigator Licenses Consumed    ${NAVIGATOR_ENTITLEMENT}

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

XIQSE Clear Operations Panel and Confirm Success
    [Documentation]     Clears the operations panel and confirms the action was successful

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Clear Operations Panel and Confirm Success

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
    Confirm Discovered Device Count From Operations Panel  ${expected_device_count}

    XIQSE Devices Select Devices Tab
    ${result}=  XIQSE Wait Until Devices Present  ${expected_device_count}
    Should Be Equal As Integers  ${result}  1

XIQSE Add Device and Confirm Not Added
    [Documentation]     Adds a device to XIQSE and confirms it is NOT added to the Devices table
    [Arguments]         ${ip}  ${profile}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    XIQSE Clear Operations Panel and Confirm Success

    Add Device and Wait for Device Add Operation to Complete  ${ip}  ${profile}

    XIQSE Confirm Devices Not Added     ${ip}

XIQSE Confirm Devices Not Added
    [Documentation]     Confirms the specified devices are not present in XIQSE
    [Arguments]         @{ip_list}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Navigate to Devices and Confirm Success
    FOR  ${ip}  IN  @{ip_list}
        Confirm IP Address Not Present in Devices Table  ${ip}
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

XIQSE Confirm Devices Present in Discovered Table
    [Documentation]     Confirms the specified IP addresses are present in the Discovered table
    [Arguments]         @{ip_list}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    FOR  ${ip}  IN  @{ip_list}
        Confirm IP Address Present in Discovered Table  ${ip}
    END

XIQSE Confirm Devices Not Present in Discovered Table
    [Documentation]     Confirms the specified IP addresses are not present in the Discovered table
    [Arguments]         @{ip_list}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    FOR  ${ip}  IN  @{ip_list}
        Confirm IP Address Not Present in Discovered Table  ${ip}
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

XIQSE Confirm Banner Message Reports License Limit Exceeded
    [Documentation]     Confirms a banner message is displayed stating the license limit has been exceeded and closes it

    Confirm License Limit Warning Message Displayed
    Close License Limit Warning Message

XIQSE Confirm License Device Limit Exceeded Event Generated For Devices
    [Documentation]     Confirms the License Device Limit Exceeded event exists for the specified devices
    [Arguments]         @{ip_list}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Navigate to Events and Confirm Success
    Set Event Time Range and Confirm Success        Last 30 Minutes
    Set Event Type and Confirm Success              Console
    Set Event Search String and Confirm Success     Device Add Failure

    FOR  ${ip}  IN  @{ip_list}
        ${col_result}=  XIQSE Table Set Column Filter   Source  ${ip}
        Should Be Equal As Integers                     ${col_result}  1
        Confirm Event Row Contains Text                 License Device Limit Exceeded
    END

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

    # Log out and close the window
    [Teardown]  XIQ Log Out and Close Window

Clean Up XIQSE Components
    [Documentation]     Cleans up components used in XIQSE during the test and logs out

    Switch To Window    ${XIQSE_WINDOW_INDEX}

    Enable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver    ${WORLD_SITE}

    # Disable all columns for event searches
    Set Alarm Event Search Scope    false

    # Delete all the discovered devices from the site
    XIQSE Delete All Site Devices and Confirm Success   ${MAIN_SITE}

    # Delete the test site
    XIQSE Delete Site and Confirm Success  ${MAIN_SITE}

    # Clear out the operations panel
    XIQSE Clear Operations Panel and Confirm Success

    # Log out
    Log Out of XIQSE and Confirm Success

XIQ Log Out and Close Window
    [Documentation]     Logs out of XIQ and closes the window

    Switch To Window    ${XIQ_WINDOW_INDEX}

    Log Out of XIQ and Confirm Success
    Close Window    ${XIQ_WINDOW_INDEX}

Confirm Ping Only Device Functionality
    [Documentation]     Confirms adding a ping only device in XIQSE when no pilot licenses are available adds the device

    # Navigate to the Devices tab for the test site
    XIQSE Navigate to Site Devices and Confirm Success  ${MAIN_SITE}

    # Confirm a "Ping Only" device is added successfully to XIQSE
    Create Device and Confirm Success  ${NAV3_IP}  <Ping Only>

    # Confirm the "Ping Only" device is marked as onboarded to XIQ within XIQSE
    Confirm XIQSE Device Onboarded to XIQ  ${NAV3_IP}

    # Confirm the "Ping Only" device is preent in XIQ
    Switch To Window    ${XIQ_WINDOW_INDEX}
    Navigate to XIQ Devices and Confirm Success
    Search XIQ Devices Table and Confirm Success  ${NAV3_IP}
    Clear Search on XIQ Devices Table and Confirm Success

    # Confirm the license entitlement counts are still the same
    XIQ Confirm All Licenses Consumed

    [Teardown]  Delete XIQSE Test Device and Confirm Success  ${NAV3_IP}

Confirm Add From Discovered Functionality
    [Documentation]     Confirms adding devices from the discovered tab in XIQSE when no pilot licenses are available
    ...                 does not add the devices, and the user is notified that the devices were not added.

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    # Navigate to the Devices tab for the test site
    XIQSE Create Site and Confirm Success  ${TEST_SITE}
    XIQSE Navigate to Site Tab and Confirm Success  ${TEST_SITE}

    # Perform a discovery of three devices with "Automatically Add to Site" disabled
    XIQSE Clear Operations Panel and Confirm Success
    Perform IP Range Discovery and Ignore License Limit Error  ${PIL1_IP}  ${PIL3_IP}  ${PILOT_PROFILE}  auto_add=false

    # Confirm the discovered device count is what we expect (3)
    Confirm Discovered Device Count From Operations Panel  3

    # Confirm the devices are added to the Discovered tab
    XIQSE Navigate to Discovered and Confirm Success
    XIQSE Discovered Do Not Show In Groups
    XIQSE Confirm Devices Present in Discovered Table           ${PIL1_IP}  ${PIL2_IP}  ${PIL3_IP}

    # Select and add the three devices
    ${add_result}=  XIQSE Discovered Add Devices                ${PIL1_IP},${PIL2_IP},${PIL3_IP}
    Should Be Equal As Integers                                 ${add_result}     1

    # Check that the user is notified that the devices were not added
    XIQSE Confirm Banner Message Reports License Limit Exceeded

    # Confirm the devices remain in the Discovered tab
    XIQSE Confirm Devices Present in Discovered Table           ${PIL1_IP}  ${PIL2_IP}  ${PIL3_IP}

    # Clear the devices from the Discovered tab
    Clear All From Discovered and Confirm Success

    # Confirm the devices were not added to the Devices table
    XIQSE Navigate to Site Devices and Confirm Success  ${TEST_SITE}
    XIQSE Confirm Devices Not Added  ${PIL1_IP}  ${PIL2_IP}  ${PIL3_IP}

    # Confirm the devices were not onboarded to XIQ
    XIQ Confirm Devices Not Onboarded  ${PIL1_SERIAL}  ${PIL2_SERIAL}  ${PIL3_SERIAL}

    [Teardown]  XIQSE Delete Site and Confirm Success  ${TEST_SITE}

XIQSE Close All Banner Messages and Confirm Success
    [Documentation]     Switches to the XIQSE window and closes all banner messages, confirming action is successful.

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Close All Banner Messages and Confirm Success
