#----------------------------------------------------------------------
# Copyright (C) 2021... 2021 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Heidi S. White
# Description   : Test Suite for testing that device annotations from XIQSE are sent to XIQ:
#                   - Asset Tag
#                   - User Data 1
#                   - User Data 2
#                   - User Data 3
#                   - User Data 4
#                   - Notes
#                 This is qTest test case TC-133 (XIQ-SE project) and TC-10318 (CSIT project),
#                 and Jira story APC-44684 (XIQSE Device Notes to XIQ).

*** Settings ***
Library         Collections
Library         xiq/flows/common/Login.py
Library         xiq/flows/common/Navigator.py
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

${TEST_ASSET_TAG}       AUTO ASSET TAG
${TEST_USER_DATA_1}     AUTO DATA 1
${TEST_USER_DATA_2}     AUTO DATA 2
${TEST_USER_DATA_3}     AUTO DATA 3
${TEST_USER_DATA_4}     AUTO DATA 4
${TEST_NOTE}            AUTO NOTE
${WORLD_SITE}           World

*** Test Cases ***
Test 1: Confirm Initial Device Annotation Values in XIQSE are Reflected in XIQ
    [Documentation]     Confirms the initial device annotations in XIQSE are reflected in XIQ
    [Tags]              nightly2    release_testing    csit_tc_10318   apc_44684    development    xiqse    xiq_integration    d360    annotations    test1

    Switch To Window  ${XIQSE_WINDOW_INDEX}
    XIQSE Navigate to Devices and Confirm Success

    # Confirm current device annotation values in XIQSE
    XIQSE Confirm Device Annotation Values  ${DUT_IP}  ${BEFORE_ASSET}  ${BEFORE_UD1}
    ...  ${BEFORE_UD2}  ${BEFORE_UD3}  ${BEFORE_UD4}  ${BEFORE_NOTE}

    # Confirm current values are displayed in XIQ correctly
    XIQ Confirm Device Annotation Values  ${DUT_MAC}  ${BEFORE_ASSET}  ${BEFORE_UD1}
    ...  ${BEFORE_UD2}  ${BEFORE_UD3}  ${BEFORE_UD4}  ${BEFORE_NOTE}

Test 2: Confirm Device Annotations Configured in XIQSE are Reflected in XIQ
    [Documentation]     Configures the device annotations in XIQSE and confirms XIQ displays them correctly
    [Tags]              nightly2    release_testing    known_issue    csit_tc_10318   apc_44684    development    xiqse    xiq_integration    d360    annotations    test2

    Switch To Window  ${XIQSE_WINDOW_INDEX}
    XIQSE Navigate to Devices and Confirm Success

    # Update Device Annotations in XIQSE
    Set Device Annotations  ${DUT_IP}  ${TEST_ASSET_TAG}  ${TEST_USER_DATA_1}  ${TEST_USER_DATA_2}
    ...  ${TEST_USER_DATA_3}  ${TEST_USER_DATA_4}  ${TEST_NOTE}

    # Confirm new values were set correctly in XIQSE
    XIQSE Confirm Device Annotation Values  ${DUT_IP}  ${TEST_ASSET_TAG}  ${TEST_USER_DATA_1}
    ...  ${TEST_USER_DATA_2}  ${TEST_USER_DATA_3}  ${TEST_USER_DATA_4}  ${TEST_NOTE}

    # Confirm new values are displayed in XIQ
    XIQ Confirm Device Annotation Values  ${DUT_MAC}  ${TEST_ASSET_TAG}  ${TEST_USER_DATA_1}
    ...  ${TEST_USER_DATA_2}  ${TEST_USER_DATA_3}  ${TEST_USER_DATA_4}  ${TEST_NOTE}

Test 3: Confirm Device Annotations Updated in XIQSE are Reflected in XIQ
    [Documentation]     Resets the device annotations in XIQSE and confirms XIQ displays them correctly
    [Tags]              nightly2    release_testing    known_issue    csit_tc_10318   apc_44684    development    xiqse    xiq_integration    d360    annotations    test3

    Switch To Window  ${XIQSE_WINDOW_INDEX}
    XIQSE Navigate to Devices and Confirm Success

    # Reset the device annotations
    Set Device Annotations  ${DUT_IP}
    ...  ${BEFORE_ASSET}  ${BEFORE_UD1}  ${BEFORE_UD2}  ${BEFORE_UD3}  ${BEFORE_UD4}  ${BEFORE_NOTE}

    # Confirm new values were set in XIQSE
    XIQSE Confirm Device Annotation Values  ${DUT_IP}  ${BEFORE_ASSET}  ${BEFORE_UD1}
    ...  ${BEFORE_UD2}  ${BEFORE_UD3}  ${BEFORE_UD4}  ${BEFORE_NOTE}

    # Confirm values are displayed in XIQ
    XIQ Confirm Device Annotation Values  ${DUT_MAC}  ${BEFORE_ASSET}  ${BEFORE_UD1}
    ...  ${BEFORE_UD2}  ${BEFORE_UD3}  ${BEFORE_UD4}  ${BEFORE_NOTE}


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

    ${result}=  Logout User
    Should Be Equal As Integers  ${result}  1

Set Up XIQSE Components
    [Documentation]     Sets up the XIQSE components for the test

    Disable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver    ${WORLD_SITE}

    # Confirm the serial number is correct and set the common options needed for automation
    Confirm Serial Number and Set Common Options     ${XIQSE_SERIAL}

    # Create the test device
    Navigate and Create Device      ${DUT_IP}  ${DUT_PROFILE}

    # Make sure the necessary colunns are displayed
    XIQSE Devices Show Columns    Asset Tag  User Data 1  User Data 2  User Data 3  User Data 4  Notes

    # Get the current annotation values so we can reset them after the test
    XIQSE Get Current Device Annotation Values  ${DUT_IP}

Set Up XIQ Components
    [Documentation]     Sets up the XIQ components for the test

    XIQ Navigate to Devices and Confirm Success

XIQ Navigate to Devices and Confirm Success
    [Documentation]     Navigates to the Manage> Devices view in XIQ and confirms the action was successful

    Switch To Window  ${XIQ_WINDOW_INDEX}

    ${nav_result}=  Navigate to Devices
    Should Be Equal As Integers  ${nav_result}  1

XIQSE Navigate to Devices and Confirm Success
    [Documentation]     Navigates to the Network> Devices> Devices view in XIQSE and confirms the action was successful

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Navigate to Devices and Confirm Success

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
    [Documentation]     Onboards the specified XIQ Site Engine from the Diagnostics tab in XIQSE

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Enter XIQ Credentials to Auto Onboard XIQSE     ${XIQ_USER}  ${XIQ_PASSWORD}

Confirm XIQ Site Engine Onboarded to XIQ
    [Documentation]     Confirms the XIQ Site Engine has been onboarded to XIQ successfully

    Switch To Window  ${XIQ_WINDOW_INDEX}

    ${search_result}=  Wait Until Device Added      ${XIQSE_SERIAL}
    Should Be Equal As Integers                     ${search_result}    1

    ${device_status}=  Wait Until Device Online     ${XIQSE_SERIAL}
    Should Be Equal As Integers                     ${device_status}    1

XIQSE Get Current Device Annotation Values
    [Documentation]     Retrieves the current device annotation values and stores them in suite variables.
    [Arguments]         ${ip}

    &{current_info}=     XIQSE Get Device Row Values
    ...  ${ip}  Asset Tag,User Data 1,User Data 2,User Data 3,User Data 4,Notes

    ${current_asset}=   Get From Dictionary  ${current_info}  Asset Tag
    ${current_ud1}=     Get From Dictionary  ${current_info}  User Data 1
    ${current_ud2}=     Get From Dictionary  ${current_info}  User Data 2
    ${current_ud3}=     Get From Dictionary  ${current_info}  User Data 3
    ${current_ud4}=     Get From Dictionary  ${current_info}  User Data 4
    ${current_note}=    Get From Dictionary  ${current_info}  Notes

    Set Suite Variable   ${BEFORE_ASSET}    ${current_asset}
    Set Suite Variable   ${BEFORE_UD1}      ${current_ud1}
    Set Suite Variable   ${BEFORE_UD2}      ${current_ud2}
    Set Suite Variable   ${BEFORE_UD3}      ${current_ud3}
    Set Suite Variable   ${BEFORE_UD4}      ${current_ud4}
    Set Suite Variable   ${BEFORE_NOTE}     ${current_note}

Set Device Annotations
    [Documentation]     Sets the device annotations on the specified device.
    [Arguments]         ${ip}  ${asset}  ${ud1}  ${ud2}  ${ud3}  ${ud4}  ${note}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    ${result}=  XIQSE Configure Device Annotations and Save  ${ip}  asset_tag=${asset}
    ...    ud1=${ud1}  ud2=${ud2}  ud3=${ud3}  ud4=${ud4}  note=${note}
    Should Be Equal As Integers     ${result}  1

XIQSE Confirm Device Annotation Values
    [Documentation]     Confirms the device annotations for the specified device are at the expected values.
    [Arguments]         ${ip}  ${asset}  ${ud1}  ${ud2}  ${ud3}  ${ud4}  ${note}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    &{row_info}=     XIQSE Get Device Row Values
    ...  ${ip}  Asset Tag,User Data 1,User Data 2,User Data 3,User Data 4,Notes

    ${row_asset}=     Get From Dictionary  ${row_info}  Asset Tag
    ${row_ud1}=       Get From Dictionary  ${row_info}  User Data 1
    ${row_ud2}=       Get From Dictionary  ${row_info}  User Data 2
    ${row_ud3}=       Get From Dictionary  ${row_info}  User Data 3
    ${row_ud4}=       Get From Dictionary  ${row_info}  User Data 4
    ${row_note}=      Get From Dictionary  ${row_info}  Notes

    Should Be Equal As Strings  '${row_asset.strip()}'  '${asset.strip()}'
    Should Be Equal As Strings  '${row_ud1.strip()}'    '${ud1.strip()}'
    Should Be Equal As Strings  '${row_ud2.strip()}'    '${ud2.strip()}'
    Should Be Equal As Strings  '${row_ud3.strip()}'    '${ud3.strip()}'
    Should Be Equal As Strings  '${row_ud4.strip()}'    '${ud4.strip()}'
    Should Be Equal As Strings  '${row_note.strip()}'   '${note.strip()}'

XIQ Confirm Device Annotation Values
    [Documentation]     Confirms the device annotations set in XIQSE show up correctly in XIQ
    [Arguments]         ${mac}  ${asset}  ${ud1}  ${ud2}  ${ud3}  ${ud4}  ${note}

    Switch To Window  ${XIQ_WINDOW_INDEX}
    XIQ Navigate to Devices and Confirm Success

    # Confirm Values in D360 View
    ${nav_result}=  Navigate to Device360 Page with MAC  ${mac}
    Should Be Equal As Integers  ${nav_result}  1
    Confirm Device360 System Information Annotations  ${asset}  ${ud1}  ${ud2}  ${ud3}  ${ud4}  ${note}

    [Teardown]  Close Device360 Window

Confirm Device360 System Information Annotations
    [Documentation]     Confirms the System Information tab of the Device360 view contains expected values for the device annotations
    [Arguments]         ${asset_tag}  ${ud1}  ${ud2}  ${ud3}  ${ud4}  ${note}

    # Get the data displayed in the System Information view
    Device360 Refresh Page
    Device360 Navigate to Switch System Information

    &{sys_info}=  Device360 Get Switch System Information

    ${info_asset}=  Get From Dictionary  ${sys_info}  asset_tag
    ${info_ud1}=    Get From Dictionary  ${sys_info}  user_data_1
    ${info_ud2}=    Get From Dictionary  ${sys_info}  user_data_2
    ${info_ud3}=    Get From Dictionary  ${sys_info}  user_data_3
    ${info_ud4}=    Get From Dictionary  ${sys_info}  user_data_4
    ${info_note}=   Get From Dictionary  ${sys_info}  note

    # Need to strip the white space since D360 reports empty value as "" and XIQSE reports it as " "
    Should Be Equal As Strings  '${info_asset.strip()}'     '${asset_tag.strip()}'
    Should Be Equal As Strings  '${info_ud1.strip()}'       '${ud1.strip()}'
    Should Be Equal As Strings  '${info_ud2.strip()}'       '${ud2.strip()}'
    Should Be Equal As Strings  '${info_ud3.strip()}'       '${ud3.strip()}'
    Should Be Equal As Strings  '${info_ud4.strip()}'       '${ud4.strip()}'
    Should Be Equal As Strings  '${info_note.strip()}'      '${note.strip()}'

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

    Switch To Window                                ${XIQSE_WINDOW_INDEX}
    Enable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver    ${WORLD_SITE}
    XIQSE Navigate to Devices and Confirm Success

    # Reset the device annotations - doing this again during tear down in case the test case failed
    # and this step didn't run
    Set Device Annotations  ${DUT_IP}
    ...  ${BEFORE_ASSET}  ${BEFORE_UD1}  ${BEFORE_UD2}  ${BEFORE_UD3}  ${BEFORE_UD4}  ${BEFORE_NOTE}

    # Delete the test device
    Delete Device and Confirm Success    ${DUT_IP}

    # Log out
    Log Out of XIQSE and Confirm Success
