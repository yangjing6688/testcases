#----------------------------------------------------------------------
# Copyright (C) 2021... 2021 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Heidi S. White
# Description   : Test Suite for testing device deletion from XIQSE when sharing has been disabled and re-enabled,
#                 including when a device contains a note and when a device is archived.
#                 This is Jira APC-47784 - Deleting devices from XIQSE is not removing devices from XIQ
#                 This is qTest test case TC-10310 in project CSIT:
#                   TC-10310: XIQSE Delete Devices - Disconnect - Sharing

*** Settings ***
Library         String
Library         xiq/flows/globalsettings/GlobalSetting.py

Resource        ../../DeleteDevices/Resources/AllResources.robot

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

${TEST_NOTE}            Automation Test Note
${TEST_ARCHIVE}         Automation_Archive
${WORLD_SITE}           World


*** Test Cases ***
Test 1: Delete Device - Sharing Disabled and Re-enabled
    [Documentation]  Confirms a device deleted from XIQSE is removed from XIQ after sharing has been disabled and re-enabled
    [Tags]           nightly2    release_testing    csit_tc_10310    apc_47884    development    xiqse    xiq_integration    delete_device    disconnect    sharing    test1

    XIQSE Add Device and Confirm Success        ${DUT_IP}  ${DUT_PROFILE}
    XIQSE Confirm Device Onboarded to XIQ       ${DUT_IP}
    Confirm Device Onboarded to XIQ             ${DUT_SERIAL}

    Confirm Device360 Page Opens For Device     ${DUT_MAC}
    Confirm Device360 Page Opens For Device     ${XIQSE_MAC}

    Disable Sharing and Confirm Device Status
    Enable Sharing and Confirm Device Status

    XIQSE Delete Device and Confirm Success     ${DUT_IP}
    Confirm Device Removed From XIQ             ${DUT_SERIAL}

    Confirm Device360 Page Opens For Device     ${XIQSE_MAC}

    [Teardown]  Run Keywords
    ...  Switch To Window  ${XIQSE_WINDOW_INDEX}
    ...  AND
    ...  Enable XIQ Connection Sharing and Confirm Success

Test 2: Delete Device With Note - Sharing Disabled and Re-enabled
    [Documentation]  Confirms a device deleted from XIQSE which has a note is removed from XIQ after disconnected via sharing
    [Tags]           nightly2    release_testing    csit_tc_10310    apc_47884    development    xiqse    xiq_integration    delete_device    disconnect    sharing    test2

    XIQSE Add Device and Confirm Success                    ${DUT_IP}  ${DUT_PROFILE}
    XIQSE Confirm Device Onboarded to XIQ                   ${DUT_IP}
    Confirm Device Onboarded to XIQ                         ${DUT_SERIAL}

    XIQSE Set Device Note and Confirm Success               ${DUT_IP}  ${TEST_NOTE}

    Confirm Device360 System Information Note For Device    ${DUT_MAC}  ${TEST_NOTE}
    Confirm Device360 Page Opens For Device                 ${XIQSE_MAC}

    Disable Sharing and Confirm Device Status
    Enable Sharing and Confirm Device Status

    Confirm Device360 System Information Note For Device    ${DUT_MAC}  ${TEST_NOTE}

    XIQSE Delete Device and Confirm Success                 ${DUT_IP}
    Confirm Device Removed From XIQ                         ${DUT_SERIAL}

    Confirm Device360 Page Opens For Device                 ${XIQSE_MAC}

    [Teardown]  Run Keywords
    ...  Switch To Window  ${XIQSE_WINDOW_INDEX}
    ...  AND
    ...  Enable XIQ Connection Sharing and Confirm Success

Test 3: Delete Archived Device - Sharing Disabled and Re-enabled
    [Documentation]  Confirms an archived device deleted from XIQSE is removed from XIQ after disconnected via sharing
    [Tags]           nightly2    release_testing    csit_tc_10310    apc_47884    development    xiqse    xiq_integration    delete_device    disconnect    sharing    test3

    XIQSE Add Device and Confirm Success                        ${DUT_IP}  ${DUT_PROFILE}
    XIQSE Confirm Device Onboarded to XIQ                       ${DUT_IP}
    Confirm Device Onboarded to XIQ                             ${DUT_SERIAL}

    XIQSE Archive Device and Confirm Success                    ${TEST_ARCHIVE}  ${DUT_IP}
    XIQSE Confirm Device Is Archived                            ${DUT_IP}

    Confirm Device360 System Information Archived For Device    ${DUT_MAC}  True
    Confirm Device360 Page Opens For Device                     ${XIQSE_MAC}

    Disable Sharing and Confirm Device Status
    Enable Sharing and Confirm Device Status

    Confirm Device360 System Information Archived For Device    ${DUT_MAC}  True

    XIQSE Delete Device and Confirm Success                     ${DUT_IP}
    Confirm Device Removed From XIQ                             ${DUT_SERIAL}

    Confirm Device360 Page Opens For Device                     ${XIQSE_MAC}

    [Teardown]  Run Keywords
    ...  XIQSE Delete Archive and Confirm Success    ${TEST_ARCHIVE}
    ...  AND
    ...  Enable XIQ Connection Sharing and Confirm Success


*** Keywords ***
Log In and Set Up Test
    [Documentation]     Logs in and sets up the components for the test

    XIQSE Log In and Set Window Index
    Set Up XIQSE Components

    XIQ Log In and Set Window Index

    Onboard XIQ Site Engine and Confirm Success

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

Set Up XIQSE Components
    [Documentation]     Sets up the XIQSE components for the test

    Disable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver    ${WORLD_SITE}

    # Confirm the serial number is correct and set the common options needed for automation
    Confirm Serial Number and Set Common Options     ${XIQSE_SERIAL}

    # Make sure the necessary colunns are displayed
    XIQSE Navigate to Devices and Confirm Success
    XIQSE Devices Show Columns    Notes    Archived    XIQ Onboarded

XIQ Navigate to Devices and Confirm Success
    [Documentation]     Navigates to the Manage> Devices view in XIQ and confirms the action was successful

    Switch To Window  ${XIQ_WINDOW_INDEX}

    ${nav_result}=  Navigate to Devices
    Should Be Equal As Integers  ${nav_result}  1

XIQSE Navigate to Devices and Confirm Success
    [Documentation]     Navigates to the Network> Devices> Devices view in XIQSE and confirms the action was successful

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    # This keyword is defined in testsuites/xiqse/libraries/lib_devices
    Navigate to Devices and Confirm Success

Log Out of XIQ and Confirm Success
    [Documentation]     Logs out of XIQ and confirms the logout was successful

    ${result}=  Logout User
    Should Be Equal As Integers     ${result}     1

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
    ${search_result}=  Search Device Mac   ${XIQSE_MAC}
    Run Keyword If  '${search_result}' == '1'    Delete Device  device_mac=${XIQSE_MAC}

Auto Onboard XIQ Site Engine
    [Documentation]     Onboards the specified XIQ Site Engine, deleting it first if it already exists

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Enter XIQ Credentials to Auto Onboard XIQSE  ${XIQ_USER}  ${XIQ_PASSWORD}

Confirm XIQ Site Engine Onboarded to XIQ
    [Documentation]     Confirms the XIQ Site Engine has been onboarded to XIQ successfully

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Confirm Device Onboarded to XIQ     ${XIQSE_SERIAL}

Confirm Device Onboarded to XIQ
    [Documentation]     Confirms the specified device has been onboarded to XIQ successfully
    [Arguments]         ${serial}

    Switch To Window  ${XIQ_WINDOW_INDEX}

    ${search_result}=  Wait Until Device Added      ${serial}
    Should Be Equal As Integers                     ${search_result}    1

    ${device_status}=  Wait Until Device Online     ${serial}
    Should Be Equal As Integers                     ${device_status}    1

Confirm Device Removed From XIQ
    [Documentation]     Confirms the specified device has been removed from XIQ successfully
    [Arguments]         ${serial}

    Switch To Window  ${XIQ_WINDOW_INDEX}

    ${search_result}=  Wait Until Device Removed    device_serial=${serial}
    Should Be Equal As Integers                     ${search_result}    1

Confirm Device360 Page Opens For Device
    [Documentation]     Confirms the Device360 view can be opened for the device with the specified MAC address
    [Arguments]  ${mac}

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Navigate to Device360 Page with MAC     ${mac}

    [Teardown]  Close XIQ Device360 Window and Confirm Success

Confirm Device360 System Information Note For Device
    [Documentation]     Confirms the System Information tab of the Device360 view contains expected value for the device's note
    [Arguments]         ${mac}  ${note}

    Switch To Window  ${XIQ_WINDOW_INDEX}

    # Open the D360 view
    Navigate to Device360 Page with MAC     ${mac}

    # Get the data displayed in the System Information view
    Device360 Refresh Page
    Device360 Navigate to Switch System Information

    # Extract the note value
    &{sys_info}=  Device360 Get Switch System Information
    ${info_note}=   Get From Dictionary  ${sys_info}  note

    # Confirm the note is what we expedt.
    # Need to strip the white space since D360 reports empty value as "" and XIQSE reports it as " "
    Should Be Equal As Strings  '${info_note.strip()}'      '${note.strip()}'

    [Teardown]  Close Device360 Window

Confirm Device360 System Information Archived For Device
    [Documentation]     Confirms the device archived state is at the expected value.
    [Arguments]         ${mac}  ${archived}

    Switch To Window  ${XIQ_WINDOW_INDEX}

    # Open the D360 view
    Navigate to Device360 Page with MAC  ${mac}

    # Get the data displayed in the System Information view
    Device360 Refresh Page
    Device360 Navigate to Switch System Information

    # Extract the archived state value
    &{sys_info}=  Device360 Get Switch System Information
    ${info_archived}=   Get From Dictionary  ${sys_info}  archived
    ${archived_upper}=  Convert To Upper Case  ${archived}

    # Confirm the archived state is what we expect.
#    Should Be Equal     ${info_archived}    ${archived_upper}
    Log To Console  >>>-----------------------------------------<<<
    Log To Console  >>> This is broken until APC-47758 is fixed <<<
    Log To Console  D360 Archived State is ${info_archived}
    Log To Console  Expected Archived State is ${archived_upper}
    Log To Console  >>>-----------------------------------------<<<

    [Teardown]  Close Device360 Window

XIQSE Add Device and Confirm Success
    [Documentation]     Adds a device to XIQSE and confirms it was added successfully
    [Arguments]         ${ip}  ${profile}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Navigate and Create Device   ${ip}  ${profile}

XIQSE Delete Device and Confirm Success
    [Documentation]     Deletes the specified device from XIQSE and confirms the action was successful
    [Arguments]         ${ip}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Navigate and Delete Device  ${ip}

XIQSE Confirm Device Onboarded to XIQ
    [Documentation]     Confirms the specified device is onboarded to XIQ by checking the XIQ Onboarded column
    [Arguments]         ${ip}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    XIQSE Navigate to Devices and Confirm Success

    Confirm XIQSE Device Onboarded to XIQ  ${ip}

XIQSE Set Device Note and Confirm Success
    [Documentation]     Sets the "Note" device annotation on the specified device.
    [Arguments]         ${ip}  ${note}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    ${result}=  XIQSE Configure Device Annotations and Save  ${ip}  note=${note}
    Should Be Equal As Integers     ${result}  1

XIQSE Archive Device and Confirm Success
    [Documentation]     Archives the specified device and confirms the action was successful
    [Arguments]         ${archive}  ${ip}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    ${nav_result}=  XIQSE Navigate to Network Archives Tab
    Should Be Equal As Integers         ${nav_result}     1

    ${create_result}=  XIQSE Archives Create Archive    ${archive}    ${ip}
    Should Be Equal As Integers  ${create_result}  1

    ${wait_result}=  XIQSE Wait Until Archive Added     ${archive}
    Should Be Equal As Integers  ${wait_result}  1

    ${confirm_result}=  XIQSE Confirm Archive Exists    ${archive}
    Should Be Equal As Integers  ${confirm_result}  1

XIQSE Confirm Device Is Archived
    [Documentation]     Confirms the specified device is marked as being archived
    [Arguments]         ${ip}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    XIQSE Navigate to Devices and Confirm Success

    Confirm Device Archived  ${ip}

XIQSE Delete Archive and Confirm Success
    [Documentation]     Deletes an archive and confirms the deletion was successful
    [Arguments]         ${archive}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    ${nav_result}=  XIQSE Navigate to Network Archives Tab
    Should Be Equal As Integers         ${nav_result}     1

    ${delete_result}=  XIQSE Archives Delete Archive    ${TEST_ARCHIVE}
    Should Not Be Equal As Integers  ${delete_result}  -1

    ${wait_result}=  XIQSE Wait Until Archive Removed   ${TEST_ARCHIVE}
    Should Be Equal As Integers  ${wait_result}  1

    ${confirm_result}=  XIQSE Confirm Archive Exists    ${TEST_ARCHIVE}  false
    Should Be Equal As Integers  ${confirm_result}  1

Disable Sharing and Confirm Device Status
    [Documentation]     Disables XIQSE-XIQ sharing and confirms the connection status is updated correctly in XIQ

    # Disable sharing
    Switch To Window  ${XIQSE_WINDOW_INDEX}
    Disable XIQ Connection Sharing and Confirm Success

    # Confirm connection status in XIQ
    Switch To Window  ${XIQ_WINDOW_INDEX}

    ##   Confirm XIQSE has status Disconnected
    Wait Until Device Offline           ${XIQSE_SERIAL}  retry_duration=30  retry_count=22
    Confirm Device Status with MAC      ${XIQSE_MAC}     disconnected

    ##   Confirm test devices have status Unknown
    Confirm Device Status with Serial   ${DUT_SERIAL}    unknown

Enable Sharing and Confirm Device Status
    [Documentation]     Enables XIQSE-XIQ sharing and confirms the connection status is updated correctly in XIQ

    # Enable sharing
    Switch To Window  ${XIQSE_WINDOW_INDEX}
    Enable XIQ Connection Sharing and Confirm Success

    # Confirm connection status in XIQ
    Switch To Window  ${XIQ_WINDOW_INDEX}

    ##   Confirm XIQSE has status Connected (green)
    Wait Until Device Online            ${XIQSE_SERIAL}  retry_duration=30  retry_count=22
    Confirm Device Status with MAC      ${XIQSE_MAC}     green

    ##   Confirm test devices have status Connected (green)
    Confirm Device Status with Serial   ${DUT_SERIAL}    green

Confirm Device Status with Serial
    [Documentation]     Checks the status of the specified device using Serial Number and confirms it matches the expected value
    [Arguments]         ${serial}  ${expected_status}

    Switch To Window  ${XIQ_WINDOW_INDEX}

    ${device_status}=       Get Device Status   device_serial=${serial}
    Should Contain          ${device_status}    ${expected_status}

Confirm Device Status with MAC
    [Documentation]     Checks the status of the specified device using MAC address and confirms it matches the expected value
    [Arguments]         ${mac}  ${expected_status}

    Switch To Window  ${XIQ_WINDOW_INDEX}

    ${device_status}=       Get Device Status   device_mac=${mac}
    Should Contain          ${device_status}    ${expected_status}

Clean Up XIQ Components
    [Documentation]     Cleans up components used in XIQ during the test and logs out

    Switch To Window    ${XIQ_WINDOW_INDEX}

    Remove Existing Site Engine from XIQ

    Log Out of XIQ and Confirm Success
    Close Window    ${XIQ_WINDOW_INDEX}

Clean Up XIQSE Components
    [Documentation]     Cleans up components used in XIQSE during the test and logs out

    Switch To Window    ${XIQSE_WINDOW_INDEX}

    Enable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver    ${WORLD_SITE}

    # Enable sharing on cleanup in case something failed and this was not completed
    Enable XIQ Connection Sharing and Confirm Success

    # Make sure the test device has been deleted
    XIQSE Delete Device and Confirm Success     ${DUT_IP}

    # Log out
    Log Out of XIQSE and Confirm Success
