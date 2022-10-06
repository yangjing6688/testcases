#----------------------------------------------------------------------
# Copyright (C) 2021... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Dan McCarthy
# Description   : Test Suite for testing XIQSE-XIQ Integration for the Single Sign On functionality
#                  from the Manage > Devices view.  This is Jira story APC-44688.
#                 These qTest test cases are part of the CSIT project:
#                   TC-11879: XIQ-SE SSO - Role: Administrator - ACTIONS > Open Site Engine
#                   TC-11880: XIQ-SE SSO - UI: Limit "Open Site Engine" when multiple devices selected
#                   TC-11881: XIQ-SE SSO - UI: Open XIQ-SE for multiple devices


*** Settings ***
Library         xiq/flows/common/DeviceCommon.py
Library         xiqse/flows/admin/users/XIQSE_AdminAuthorizedUsers.py

Resource        ../../DeviceTable/Resources/AllResources.robot

Force Tags      testbed_6_node

Suite Setup     Log In and Set Up Test
Suite Teardown  Tear Down Test and Close Session


*** Variables ***
${ENV}                  environment.remote.chrome.windows.xiqse1.yaml
${TOPO}                 topo.test.xiqse1.connected.yaml
${TESTBED}              SALEM/Dev/devices-salem-acceptance.yaml

${XIQSE_URL}            ${xiqse.url}
${XIQSE_USER}           ${xiqse.user}
${XIQSE_PASSWORD}       ${xiqse.password}
${XIQSE_SERIAL}         ${xiqse.serial}
${XIQSE_MAC}            ${xiqse.mac}

${XIQ_URL}              ${xiq.test_url}
${XIQ_USER}             ${xiq.tenant_username}
${XIQ_PASSWORD}         ${xiq.tenant_password}

${DUT1_IP}              ${netelem1.ip}
${DUT1_PROFILE}         ${netelem1.profile}
${DUT1_MAC}             ${netelem1.mac}
${DUT1_SERIAL}          ${netelem1.serial}

${DUT2_IP}              ${netelem2.ip}
${DUT2_PROFILE}         ${netelem2.profile}
${DUT2_MAC}             ${netelem2.mac}
${DUT2_SERIAL}          ${netelem2.serial}

${DUT3_IP}              ${netelem3.ip}
${DUT3_PROFILE}         ${netelem3.profile}
${DUT3_MAC}             ${netelem3.mac}
${DUT3_SERIAL}          ${netelem3.serial}

${DUT4_IP}              ${netelem4.ip}
${DUT4_PROFILE}         ${netelem4.profile}
${DUT4_MAC}             ${netelem4.mac}
${DUT4_SERIAL}          ${netelem4.serial}

${DUT5_IP}              ${netelem5.ip}
${DUT5_PROFILE}         ${netelem5.profile}
${DUT5_MAC}             ${netelem5.mac}
${DUT5_SERIAL}          ${netelem5.serial}

${DUT6_IP}              ${netelem6.ip}
${DUT6_PROFILE}         ${netelem6.profile}
${DUT6_MAC}             ${netelem6.mac}
${DUT6_SERIAL}          ${netelem6.serial}

${XIQ_WINDOW_INDEX}             0
${XIQSE_WINDOW_INDEX}           0
@{XIQSE_OSE_WINDOW_INDEXES}     []

${WORLD_SITE}           World


*** Test Cases ***
Test 1: XIQ-SE SSO - Role: Administrator - ACTIONS > Open Site Engine
    [Documentation]     Selects the Open Site Engine link within the ACTIONS menu for a device managed by an 21.9.10.x XIQ-SE.
    [Tags]              nightly2    release_testing    tccs_11879    apc_44688    development    xiqse    xiq_integration    sso    test1

    XIQ Navigate to Devices and Confirm Success
    Select Device                                   ${DUT1_MAC}
    XIQ Actions Open Site Engine Link
    Confirm XIQ User Logged in to XIQ Site Engine

    [Teardown]  Clean Up Open Site Engine Windows

Test 2: XIQ-SE SSO - UI: Limit "Open Site Engine" when multiple devices selected
    [Documentation]     Verify that a maximum of five windows are opened when the Open Site Engine action is run for multiple devices.
    [Tags]              nightly2    release_testing    tccs_11880    apc_44688    development    xiqse    xiq_integration    sso    test2

    XIQ Navigate to Devices and Confirm Success
    Select Device Rows                              device_macs=${DUT1_MAC},${DUT2_MAC},${DUT3_MAC},${DUT4_MAC},${DUT5_MAC},${DUT6_MAC}
    XIQ Actions Open Site Engine Link
    Confirm XIQ Maximum Site Engine Message
    Confirm XIQ User Logged in to XIQ Site Engine

    [Teardown]  Clean Up Open Site Engine Windows

Test 3: XIQ-SE SSO - UI: Open XIQ-SE for multiple devices
    [Documentation]     Verify separate windows are opened when the Open Site Engine action is run for multiple devices.
    [Tags]              nightly2    release_testing    tccs_11879    apc_44688    development    xiqse    xiq_integration    sso    test3

    XIQ Navigate to Devices and Confirm Success
    Select Device Rows                              device_macs=${DUT2_MAC},${DUT3_MAC}
    XIQ Actions Open Site Engine Link
    Confirm XIQ User Logged in to XIQ Site Engine

    [Teardown]  Clean Up Open Site Engine Windows


*** Keywords ***
Log In and Set Up Test
    [Documentation]     Logs in and sets up the components for the test

    XIQSE Log In and Set Window Index

    XIQ Log In and Set Window Index
    XIQ Navigate to Devices and Confirm Success
    Onboard XIQ Site Engine and Confirm Success

    # Set Up XIQSE Components and Log out of XIQSE
    Switch To Window                                ${XIQSE_WINDOW_INDEX}
    Set Up XIQSE Components
    Log Out of XIQSE and Confirm Success

    # Wait until the device added in XIQSE is onboarded to XIQ
    Switch To Window                                ${XIQ_WINDOW_INDEX}
    Confirm Device Serial Present                   ${DUT1_SERIAL}

Tear Down Test and Close Session
    [Documentation]     Cleans up XIQ and XIQ Site Engine test components and closes the browser

    Clean Up XIQ Components
    Clean Up XIQSE Components
    Quit Browser and Confirm Success

XIQ Log In and Set Window Index
    [Documentation]     Logs into XIQ and obtains the window index

    Log Into XIQ and Confirm Success                ${XIQ_USER}  ${XIQ_PASSWORD}  url=${XIQ_URL}

    ${xiq_win}=  Get Window Index
    Log To Console  Setting XIQ Window Index to ${xiq_win}
    Set Suite Variable                              ${XIQ_WINDOW_INDEX}  ${xiq_win}

XIQSE Log In and Set Window Index
    [Documentation]     Logs into XIQ Site Engine and obtains the window index

    Log Into XIQSE and Confirm Success              ${XIQSE_USER}  ${XIQSE_PASSWORD}  url=${XIQSE_URL}
    Handle License Agreement If Displayed           ${XIQ_USER}  ${XIQ_PASSWORD}

    # Close any banner messages (Connection Lost with XIQ, License Expiration, etc.) and the Help panel, if displayed
    Close Panels on Login If Displayed

    # Store the window index so we can switch between XIQSE and XIQ
    ${xiqse_win}=  XIQSE Get Window Index
    Log To Console  Setting XIQ Site Engine Window Index to ${xiqse_win}
    Set Suite Variable                              ${XIQSE_WINDOW_INDEX}  ${xiqse_win}

Set Up XIQSE Components
    [Documentation]     Sets up the XIQ Site Engine components for the test

    Disable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver    ${WORLD_SITE}

    # Enable all columns for event searches
    Set Alarm Event Search Scope    true

    # Confirm the serial number is correct and set the common options needed for automation
    Confirm Serial Number and Set Common Options    ${XIQSE_SERIAL}

    # Remove any devices that already exist
    Navigate And Delete All Devices

    # Create the test devices
    Navigate and Create Device                      ${DUT1_IP}  ${DUT1_PROFILE}
    Create Device and Confirm Success               ${DUT2_IP}  ${DUT2_PROFILE}
    Create Device and Confirm Success               ${DUT3_IP}  ${DUT3_PROFILE}
    Create Device and Confirm Success               ${DUT4_IP}  ${DUT4_PROFILE}
    Create Device and Confirm Success               ${DUT5_IP}  ${DUT5_PROFILE}
    Create Device and Confirm Success               ${DUT6_IP}  ${DUT6_PROFILE}

XIQ Navigate to Devices and Confirm Success
    [Documentation]     Navigates to the Manage> Devices view in XIQ and confirms the action was successful

    Switch To Window                                ${XIQ_WINDOW_INDEX}
    Navigate to XIQ Devices and Confirm Success
    Deselect All Devices

Onboard XIQ Site Engine and Confirm Success
    [Documentation]     Confirms the XIQ Site Engine can be onboarded successfully

    Remove Existing Site Engine from XIQ
    Auto Onboard XIQ Site Engine
    Confirm XIQ Site Engine Onboarded to XIQ

Remove Existing Site Engine from XIQ
    [Documentation]     Removes the XIQ Site Engine from XIQ if it exists

    Switch To Window                                ${XIQ_WINDOW_INDEX}
    Navigate and Remove Device By MAC From XIQ      ${XIQSE_MAC}

Auto Onboard XIQ Site Engine
    [Documentation]     Onboards the specified XIQ Site Engine from the Diagnostics tab in XIQSE

    Switch To Window                                ${XIQSE_WINDOW_INDEX}
    Enter XIQ Credentials to Auto Onboard XIQSE     ${XIQ_USER}  ${XIQ_PASSWORD}

Confirm XIQ Site Engine Onboarded to XIQ
    [Documentation]     Confirms the XIQ Site Engine has been onboarded to XIQ successfully

    Switch To Window                                ${XIQ_WINDOW_INDEX}
    Confirm Device Serial Present                   ${XIQSE_SERIAL}
    Confirm Device Serial Online                    ${XIQSE_SERIAL}
    Confirm Device OS Version Present               ${XIQSE_SERIAL}

Clean Up XIQ Components
    [Documentation]     Cleans up components used in XIQ during the test and logs out

    Switch To Window                                ${XIQ_WINDOW_INDEX}
    Navigate and Remove Device by MAC From XIQ      ${XIQSE_MAC}
    Log Out of XIQ and Confirm Success
    Close Window                                    ${XIQ_WINDOW_INDEX}

Clean Up XIQSE Components
    [Documentation]     Cleans up components used in XIQ Site Engine during the test and logs out

    Switch To Window                                ${XIQSE_WINDOW_INDEX}
    XIQSE Login User                                ${XIQSE_USER}    ${XIQSE_PASSWORD}

    Enable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver    ${WORLD_SITE}

    # Disable all columns for event searches
    Set Alarm Event Search Scope    false

    # Delete all the devices
    Navigate and Delete All Devices

    # Delete the XIQ User from the Administration > Users > Authorized Users table
    XIQSE Delete the Authorized User                ${XIQ_USER}

    # Log out
    Log Out of XIQSE and Confirm Success

XIQ Actions Open Site Engine Link
    [Documentation]     Clicks the "Open Site Engine" Link within the Manage > Device > Actions menu

    ${result}=  Actions XIQSE Open Site Engine
    Should Be Equal As Integers     ${result}   1

    # Allow the XIQ Site Engine "OneView > Network > DeviceView" page to open and load.
    Sleep  30s
    XIQSE Obtain Child Window Indexes

Confirm XIQ User Logged in to XIQ Site Engine
    [Documentation]     Confirm that the XIQ User is successfully logged in to XIQ Site Engine

    FOR     ${xiqse_window}  IN  @{XIQSE_OSE_WINDOW_INDEXES}
        Switch To Window                            ${xiqse_window}
        Confirm User Is Logged Into XIQSE

        ${result}=  XIQSE Get Username
        Should Be Equal As Strings      ${result}   ${XIQ_USER}     ignore_case=True

        ${authgroup}=  XIQSE Get Authorization Group
        Log To Console  XIQ-SE User ${XIQ_USER} is assigned to Authorization Group ${authgroup}

        Navigate to Devices and Confirm Success
    END

Confirm XIQ Maximum Site Engine Message
    [Documentation]     Confirm the 'Maximum 5 Site Engine > Device Views...' message is displayed

    Switch To Window                                ${XIQ_WINDOW_INDEX}
    ${displayed}=  Is XIQSE Maximum Site Engine Message Displayed
    Should Be Equal As Strings          ${displayed}    True

XIQSE Delete the Authorized User
    [Documentation]     Delete the Authorized User from XIQ Site Engine Administration > Users
    [Arguments]         ${username}

    ${result}=  XIQSE Navigate And Delete Authorized User       ${username}     ignore_case=True
    Should Be Equal As Integers     ${result}   1

XIQSE Obtain Child Window Indexes
    [Documentation]     Obtains the window index for any child windows.

    @{xiqse_windows}=  XIQSE Child Window Indexes   ${XIQ_WINDOW_INDEX}
    log to console  Setting XIQ-SE Open Site Window Indexes to @{xiqse_windows}
    Set Suite Variable                              @{XIQSE_OSE_WINDOW_INDEXES}     @{xiqse_windows}

Clean Up Open Site Engine Windows
    [Documentation]     Logout and Close the XIQ Site Engine windows

    Log Out of XIQSE and Confirm Success
    Close XIQSE Child Window Indexes

Close XIQSE Child Window Indexes
    [Documentation]     Closes the XIQ Site Engine Child Windows

    FOR     ${xiqse_window}     IN      @{XIQSE_OSE_WINDOW_INDEXES}
        Switch To Window                ${xiqse_window}
        Close Window                    ${xiqse_window}
    END
