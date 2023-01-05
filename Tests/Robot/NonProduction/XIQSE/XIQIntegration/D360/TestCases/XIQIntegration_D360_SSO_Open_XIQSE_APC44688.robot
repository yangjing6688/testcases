#----------------------------------------------------------------------
# Copyright (C) 2021... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Dan McCarthy
# Description   : Test Suite for testing XIQSE-XIQ Integration for the Single Sign On functionality
#                 from the Device 360 view.  This is Jira story APC-44688.
#                 This is qTest test case in the CSIT project:
#                   TC-11878: XIQ-SE SSO - Role: Administrator - D360 view > Open Site Engine


*** Settings ***
Library         xiqse/flows/admin/users/XIQSE_AdminAuthorizedUsers.py

Resource        ../../D360/Resources/AllResources.robot

Force Tags      testbed_1_node

Suite Setup     Log In and Set Up Test
Suite Teardown  Tear Down Test and Close Session


*** Variables ***
# Defaults
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

${DUT_IP}               ${netelem1.ip}
${DUT_PROFILE}          ${netelem1.profile}
${DUT_MAC}              ${netelem1.mac}
${DUT_SERIAL}           ${netelem1.serial}

${XIQ_WINDOW_INDEX}             0
${XIQSE_WINDOW_INDEX}           0
@{XIQSE_OSE_WINDOW_INDEXES}     []

${WORLD_SITE}           World

*** Test Cases ***
Test 1: Open Site Engine Link: XIQ-SE Managed Device
    [Documentation]     Confirms that the D360 "Open Site Engine" link works for a device managed by XIQ Site Engine
    [Tags]              nightly2    release_testing    staging_testing    tccs_11878    apc_44688    development    xiqse    xiq_integration    d360     sso    test1

    XIQ Navigate to Devices and Confirm Success
    XIQ Device360 Click Open Site Engine Link       ${DUT_MAC}
    Confirm XIQ User Logged in to XIQ Site Engine
    Navigate to Devices and Confirm Success

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
    Confirm Device Serial Present                   ${DUT_SERIAL}

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

    # Remove the test device if it already exists and then create the device we will be using in the test
    Navigate and Delete Device                      ${DUT_IP}
    Create Device and Confirm Success               ${DUT_IP}  ${DUT_PROFILE}

XIQ Navigate to Devices and Confirm Success
    [Documentation]     Navigates to the Manage> Devices view in XIQ and confirms the action was successful

    Switch To Window                                ${XIQ_WINDOW_INDEX}
    Navigate to XIQ Devices and Confirm Success
    Deselect All Devices

XIQSE Navigate to Devices and Confirm Success
    [Documentation]     Navigates to the Network> Devices> Devices view in XIQ Site Engine and confirms the action was successful

    Switch To Window                                ${XIQSE_WINDOW_INDEX}
    Navigate to Devices and Confirm Success

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

    Navigate to Devices and Confirm Success

    # Delete the test device
    Delete Device and Confirm Success               ${DUT_IP}

    # Delete the XIQ User from the Administration > Users > Authorized Users table
    XIQSE Delete the Authorized User                ${XIQ_USER}

    # Log out
    Log Out of XIQSE and Confirm Success

XIQ Device360 Click Open Site Engine Link
    [Documentation]     Clicks the "Open Site Engine" Link within the Device D360 view
    [Arguments]         ${mac}

    Switch To Window                                ${XIQ_WINDOW_INDEX}
    XIQ Navigate to Devices and Confirm Success

    ${result}    Set Variable    0
    ${nav_result}=    Navigate to Device360 Page with MAC  ${mac}
    IF    '${nav_result}' == '1'
        ${result}=  Device360 Click Open Site Engine Link
    END

    Should Be Equal As Integers     ${result}   1

    # Allow the XIQ Site Engine "OneView > Network > DeviceView" page to open and load.
    sleep  30s
    XIQSE Obtain Child Window Indexes

    [Teardown]  Close XIQ Device360 Window and Confirm Success

Confirm XIQ User Logged in to XIQ Site Engine
    [Documentation]     Confirm that the XIQ User is successfully logged in to XIQ Site Engine

    FOR   ${xiqse_window}  IN  @{XIQSE_OSE_WINDOW_INDEXES}
        Switch To Window  ${xiqse_window}
        Confirm User Is Logged Into XIQSE

        ${result}=  XIQSE Get Username
        Should Be Equal As Strings      ${result}   ${XIQ_USER}    ignore_case=True

        ${authgroup}=  XIQSE Get Authorization Group
        Log To Console  XIQ-SE User is assigned to Authorization Group ${authgroup}

        Navigate to Devices and Confirm Success
    END

XIQSE Delete the Authorized User
    [Documentation]     Delete the Authorized User from XIQ Site Engine Administration > Users
    [Arguments]         ${username}

    ${result}=  XIQSE Navigate And Delete Authorized User       ${username}     ignore_case=True
    Should Be Equal As Integers     ${result}   1

XIQSE Obtain Child Window Indexes
    [Documentation]     Obtains the window index for any child windows.

    @{xiqse_windows}=  XIQSE Child Window Indexes   ${XIQ_WINDOW_INDEX}
    Log To Console  Setting XIQ-SE Open Site Window Indexes to @{xiqse_windows}
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
