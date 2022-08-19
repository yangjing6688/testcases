#----------------------------------------------------------------------
# Copyright (C) 2021... 2021 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Heidi S. White
# Description   : Test Suite for testing that the device archived state is sent to XIQ.
#                 This is qTest test case TC-134 (XIQ-SE project) and TC-10317 (CSIT project),
#                 and Jira story APC-44684 (XIQSE Device Notes to XIQ).

*** Settings ***
Library         Collections
Library         String
Library         xiq/flows/common/Login.py
Library         xiq/flows/common/Navigator.py
Library         xiq/flows/globalsettings/GlobalSetting.py
Library         xiq/flows/manage/Device360.py
Library         xiq/flows/manage/Devices.py

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

${DUT_SERIAL}           ${netelem1.serial}
${DUT_MAC}              ${netelem1.mac}
${DUT_IP}               ${netelem1.ip}
${DUT_PROFILE}          ${netelem1.profile}

${TEST_ARCHIVE}         D360_AUTO_ARCHIVE
${WORLD_SITE}           World

*** Test Cases ***
Test 1: Confirm Initial Archived Status in XIQSE is Reflected in XIQ
    [Documentation]     Confirms the initial unarchived status of a device is reflected correclty in XIQ
    [Tags]              nightly2    release_testing    tccs_10317   apc_44684    development    xiqse    xiq_integration    d360    archived    test1

    Switch To Window  ${XIQSE_WINDOW_INDEX}
    XIQSE Navigate to Devices and Confirm Success

    # Confirm the current Archived value in XIQ matches XIQSE
    ${se_before}=  XIQSE Get Device Column Value    ${DUT_IP}       Archived
    Should Be Equal as Strings                      ${se_before}    False
    XIQ Confirm Device Archived Value               ${DUT_MAC}      ${se_before}

Test 2: Confirm Archived Status in XIQSE is Reflected in XIQ When Device is Archived
    [Documentation]     Creates an archive for the device and confirms XIQ displays the correct Archived value
    [Tags]              nightly2    release_testing    tccs_10317   apc_44684    development    xiqse    xiq_integration    d360    archived    test2

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    # Create a backup so the device is marked as archived
    Navigate and Create Archive                     ${TEST_ARCHIVE}  ${DUT_IP}

    # Wait until the device becomes archived
    XIQSE Navigate to Devices and Confirm Success
    Confirm Device Archived                         ${DUT_IP}

    # Confirm the new Archived value in XIQ matches XIQSE
    ${se_after}=  XIQSE Get Device Column Value     ${DUT_IP}       Archived
    Should Be Equal as Strings                      ${se_after}     True
    XIQ Confirm Device Archived Value               ${DUT_MAC}      ${se_after}

Test 3: Confirm Archived Status in XIQSE is Reflected in XIQ When Device No Longer Archived
    [Documentation]     Deletes the archive for the device and confirms XIQ displays the correct Archived value
    [Tags]              nightly2    release_testing    tccs_10317   apc_44684    development    xiqse    xiq_integration    d360    archived    test3

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    # Delete the archive
    Navigate and Delete Archive                     ${TEST_ARCHIVE}

    # Wait until the device becomes unarchived
    XIQSE Navigate to Devices and Confirm Success
    Confirm Device Not Archived                     ${DUT_IP}

    # Confirm the new Archived value in XIQ matches XIQSE
    ${se_reset}=  XIQSE Get Device Column Value     ${DUT_IP}       Archived
    Should Be Equal as Strings                      ${se_reset}     False
    XIQ Confirm Device Archived Value               ${DUT_MAC}      ${se_reset}


*** Keywords ***
Log In and Set Up Test
    [Documentation]     Logs in and sets up the components for the test

    XIQSE Log In and Set Window Index
    Set Up XIQSE Components

    XIQ Log In and Set Window Index
    Set Up XIQ Components

    # Onboard the XIQ Site Engine
    Onboard XIQ Site Engine and Confirm Success

    # Wait until the device added in XIQSE is onboarded to XIQ
    Switch To Window  ${XIQ_WINDOW_INDEX}
    ${search_result}=  Wait Until Device Added      ${DUT_SERIAL}
    Should Be Equal As Integers                     ${search_result}    1

Tear Down Test and Close Session
    [Documentation]     Cleans up XIQ and XIQSE test components and closes the browser

    Clean Up XIQ Components
    Clean Up XIQSE Components
    Quit Browser and Confirm Success

XIQSE Log In and Set Window Index
    [Documentation]     Logs into XIQSE and obtains the window index

    Log Into XIQSE and Confirm Success              ${XIQSE_USER}  ${XIQSE_PASSWORD}  url=${XIQSE_URL}
    Handle License Agreement If Displayed           ${XIQ_USER}  ${XIQ_PASSWORD}

    # Close any banner messages (Connection Lost with XIQ, License Expiration, etc.) and the Help panel, if displayed
    Close Panels on Login If Displayed

    # Store the window index so we can switch between XIQSE and XIQ
    ${xiqse_win}=  XIQSE Get Window Index
    Log To Console  Setting XIQSE Window Index to ${xiqse_win}
    Set Suite Variable  ${XIQSE_WINDOW_INDEX}  ${xiqse_win}

XIQ Log In and Set Window Index
    [Documentation]     Logs into XIQ and obtains the window index

    ${result}=  Login User          ${XIQ_USER}  ${XIQ_PASSWORD}  url=${XIQ_URL}
    Should Be Equal As Integers     ${result}     1

    ${xiq_win}=  Get Window Index
    Log To Console  Setting XIQ Window Index to ${xiq_win}
    Set Suite Variable  ${XIQ_WINDOW_INDEX}  ${xiq_win}

Log Out of XIQ and Confirm Success
    [Documentation]     Logs out of XIQ and confirms the logout was successful

    ${result}=      Logout User
    Should Be Equal As Integers     ${result}     1

Set Up XIQSE Components
    [Documentation]     Sets up the XIQSE components for the test

    Disable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver    ${WORLD_SITE}

    # Confirm the serial number is correct and set the common options needed for automation
    Confirm Serial Number and Set Common Options     ${XIQSE_SERIAL}

    # Create the test device - deleting it first if it already exists
    Navigate and Delete Device          ${DUT_IP}
    Create Device and Confirm Success   ${DUT_IP}  ${DUT_PROFILE}

    # Make sure the necessary colunns are displayed
    XIQSE Devices Show Columns          Archived

    # Make sure the device starts out as not archived
    Navigate and Delete Archive         ${TEST_ARCHIVE}
    Navigate to Devices and Confirm Success
    Confirm Device Not Archived         ${DUT_IP}

Set Up XIQ Components
    [Documentation]     Sets up the XIQ components for the test

    XIQ Navigate to Devices and Confirm Success

    # Onboard the XIQ Site Engine
    Onboard XIQ Site Engine and Confirm Success

    # Wait until the device added in XIQSE is onboarded to XIQ
    ${search_result}=  Wait Until Device Added              ${DUT_SERIAL}
    Should Be Equal As Integers                             ${search_result}    1

XIQ Navigate to Devices and Confirm Success
    [Documentation]     Navigates to the Manage> Devices view in XIQ and confirms the action was successful

    ${nav_result}=  Navigate to Devices
    Should Be Equal As Integers  ${nav_result}  1

XIQSE Navigate to Devices and Confirm Success
    [Documentation]     Navigates to the Network> Devices> Devices view in XIQSE and confirms the action was successful

    ${nav_result}=  XIQSE Navigate to Network Devices Tab
    Should Be Equal As Integers         ${nav_result}     1

    ${sel_result}=  XIQSE Devices Select Devices Tab
    Should Be Equal As Integers         ${sel_result}     1

Onboard XIQ Site Engine and Confirm Success
    [Documentation]     Confirms the XIQ Site Engine can be onboarded successfully

    Remove Existing Site Engine from XIQ
    Auto Onboard XIQ Site Engine
    Confirm XIQ Site Engine Onboarded to XIQ

Remove Existing Site Engine from XIQ
    [Documentation]     Removes the XIQ Site Engine from XIQ if it exists

    Switch To Window  ${XIQ_WINDOW_INDEX}

    XIQ Navigate to Devices and Confirm Success

    # If the XIQ Site Engine has already been onboarded, delete it
    ${search_result}=  Search Device   ${XIQSE_MAC}
    Run Keyword If  '${search_result}' == '1'    Delete Device  device_mac=${XIQSE_MAC}

Auto Onboard XIQ Site Engine
    [Documentation]     Onboards the specified XIQ Site Engine, deleting it first if it already exists

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Enter XIQ Credentials to Auto Onboard XIQSE     ${XIQ_USER}  ${XIQ_PASSWORD}

Confirm XIQ Site Engine Onboarded to XIQ
    [Documentation]     Confirms the XIQ Site Engine has been onboarded to XIQ successfully

    Switch To Window  ${XIQ_WINDOW_INDEX}

    ${search_result}=  Wait Until Device Added      ${XIQSE_SERIAL}
    Should Be Equal As Integers                     ${search_result}    1

    ${device_status}=  Wait Until Device Online     ${XIQSE_SERIAL}
    Should Be Equal As Integers                     ${device_status}    1

XIQ Confirm Device Archived Value
    [Documentation]     Confirms the device archived value set in XIQSE shows up correctly in XIQ
    [Arguments]         ${mac}  ${archived}

    Switch To Window  ${XIQ_WINDOW_INDEX}

    # Confirm Values in D360 View
    ${nav_result}=  Navigate to Device360 Page with MAC  ${mac}
    Should Be Equal As Integers  ${nav_result}  1
    Confirm Device360 System Information Archived  ${archived}

    [Teardown]  Close Device360 Window

Confirm Device360 System Information Archived
    [Documentation]     Confirms the System Information tab of the Device360 view contains expected value for the device archived status
    [Arguments]         ${archived}

    # Get the data displayed in the System Information view
    Device360 Refresh Page
    Device360 Navigate to Switch System Information

    &{sys_info}=  Device360 Get Switch System Information

    ${info_archived}=   Get From Dictionary  ${sys_info}  archived
    ${archived_upper}=  Convert To Upper Case  ${archived}
    Should Be Equal     ${info_archived}    ${archived_upper}

Clean Up XIQ Components
    [Documentation]     Cleans up components used in XIQ during the test and logs out

    Switch To Window    ${XIQ_WINDOW_INDEX}

    XIQ Navigate to Devices and Confirm Success
    ${del_result}=  Delete Device   device_mac=${XIQSE_MAC}
    Should Be Equal As Integers     ${del_result}  1

    Log Out of XIQ and Confirm Success
    Close Window    ${XIQ_WINDOW_INDEX}

Clean Up XIQSE Components
    [Documentation]     Cleans up components used in XIQSE during the test and logs out

    Switch To Window                    ${XIQSE_WINDOW_INDEX}
    Enable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver    ${WORLD_SITE}

    # Delete the archive again during tear down in case it is still present
    Navigate and Delete Archive         ${TEST_ARCHIVE}

    # Delete the test device
    Navigate and Delete Device          ${DUT_IP}

    # Log out
    Log Out of XIQSE and Confirm Success
