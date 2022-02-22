#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : David Truesdell
# Description   : Test Suite for sanity testing of basic XIQSE device functionality.
#                 This is qTest TC-869 in the XIQ-SE project.

*** Settings ***
Library     xiqse/flows/network/devices/site/actions/XIQSE_NetworkDevicesSiteActions.py

Resource    ../../Inventory/Resources/AllResources.robot

Force Tags      testbed_1_node

Suite Setup      Log In and Set Up Test
Suite Teardown   Tear Down Test and Close Session

*** Variables ***
${XIQSE_URL}                ${xiqse.url}
${XIQSE_USERNAME}           ${xiqse.user}
${XIQSE_PASSWORD}           ${xiqse.password}
${XIQSE_IP_ADDRESS}         ${xiqse.ip}
${XIQSE_MAC}                ${xiqse.mac}
${INSTALL_MODE}             ${upgrades.install_mode}

${XIQ_URL}                  ${xiq.test_url}
${XIQ_EMAIL}                ${xiq.tenant_username}
${XIQ_PASSWORD}             ${xiq.tenant_password}

${DUT_IP}                   ${netelem1.ip}
${DUT_PROFILE}              ${netelem1.profile}

${WORLD_SITE}               World
${TEST_PROFILE}             AUTO_PROFILE
${TEST_PROFILE_VERSION}     SNMPv2
${TEST_PROFILE_READ}        public_v2
${TEST_PROFILE_WRITE}       private_v2
${TEST_PROFILE_MAX}         private_v2
${TEST_PROFILE_CLI}         Default
${TEST_NICKNAME}            AUTO NICKNAME
${TEST_ASSET_TAG}           AUTO ASSET TAG
${TEST_USER_DATA_1}         AUTO DATA 1
${TEST_USER_DATA_2}         AUTO DATA 2
${TEST_USER_DATA_3}         AUTO DATA 3
${TEST_USER_DATA_4}         AUTO DATA 4
${TEST_NOTE}                AUTO NOTE


*** Test Cases ***
Test 1: Set Device Profile
    [Documentation]     Confirms the profile can be changed on a device
    [Tags]              xiqse_tc_869    xmc_5451    development    xiqse    acceptance    inventory    configure    test1

    Navigate and Create Profile      ${TEST_PROFILE}  ${TEST_PROFILE_VERSION}  ${TEST_PROFILE_READ}  ${TEST_PROFILE_WRITE}  ${TEST_PROFILE_MAX}  ${TEST_PROFILE_CLI}

    Navigate to Devices and Confirm Success

    # Make sure the Admin Profile column is being displayed
    ${col}=  XIQSE Devices Show Columns     Admin Profile
    Should Be Equal As Integers             ${col}     1

    # Confirm the value before the update
    ${before_result}=  XIQSE Confirm Device Profile     ${DUT_IP}  ${DUT_PROFILE}
    Should Be Equal As Integers                         ${before_result}     1

    # Set the profile
    Set Profile and Confirm Success                     ${DUT_IP}  ${TEST_PROFILE}

    # Reset the profile
    Set Profile and Confirm Success                     ${DUT_IP}  ${DUT_PROFILE}

    # Delete the test profile
    Navigate and Delete Profile                         ${TEST_PROFILE}

    # Navigate to the Network> Devices> Devices page
    Navigate to Devices and Confirm Success

Test 2: Configure Device
    [Documentation]     Confirms a device can be configured
    [Tags]              xiqse_tc_869    xmc_5451    development    xiqse    acceptance    inventory    configure    test2

    Navigate to Devices and Confirm Success

    # Make sure the necessary colunns are displayed
    XIQSE Devices Show Columns    Asset Tag  User Data 1  User Data 2  User Data 3  User Data 4  Notes

    # Get the current values so we can reset them after the test
    &{before_info}=     XIQSE Get Device Row Values
    ...  ${DUT_IP}  Nickname,Asset Tag,User Data 1,User Data 2,User Data 3,User Data 4,Notes

    ${before_nn}=       Get From Dictionary  ${before_info}  Nickname
    ${before_asset}=    Get From Dictionary  ${before_info}  Asset Tag
    ${before_ud1}=      Get From Dictionary  ${before_info}  User Data 1
    ${before_ud2}=      Get From Dictionary  ${before_info}  User Data 2
    ${before_ud3}=      Get From Dictionary  ${before_info}  User Data 3
    ${before_ud4}=      Get From Dictionary  ${before_info}  User Data 4
    ${before_note}=     Get From Dictionary  ${before_info}  Notes

    # Update Device Annotations
    Set Device Annotations  ${DUT_IP}  ${TEST_NICKNAME}  ${TEST_ASSET_TAG}  ${TEST_USER_DATA_1}  ${TEST_USER_DATA_2}
    ...  ${TEST_USER_DATA_3}  ${TEST_USER_DATA_4}  ${TEST_NOTE}

    # Confirm new values were set
    &{after_info}=     XIQSE Get Device Row Values
    ...  ${DUT_IP}  Nickname,Asset Tag,User Data 1,User Data 2,User Data 3,User Data 4,Notes

    ${after_nn}=        Get From Dictionary  ${after_info}  Nickname
    ${after_asset}=     Get From Dictionary  ${after_info}  Asset Tag
    ${after_ud1}=       Get From Dictionary  ${after_info}  User Data 1
    ${after_ud2}=       Get From Dictionary  ${after_info}  User Data 2
    ${after_ud3}=       Get From Dictionary  ${after_info}  User Data 3
    ${after_ud4}=       Get From Dictionary  ${after_info}  User Data 4
    ${after_note}=      Get From Dictionary  ${after_info}  Notes
  
    Should Be Equal As Strings  ${after_nn}     ${TEST_NICKNAME}
    Should Be Equal As Strings  ${after_asset}  ${TEST_ASSET_TAG}
    Should Be Equal As Strings  ${after_ud1}    ${TEST_USER_DATA_1}
    Should Be Equal As Strings  ${after_ud2}    ${TEST_USER_DATA_2}
    Should Be Equal As Strings  ${after_ud3}    ${TEST_USER_DATA_3}
    Should Be Equal As Strings  ${after_ud4}    ${TEST_USER_DATA_4}
    Should Be Equal As Strings  ${after_note}   ${TEST_NOTE}
    
    [Teardown]  Set Device Annotations  ${DUT_IP}
    ...         ${before_nn}  ${before_asset}  ${before_ud1}  ${before_ud2}  ${before_ud3}  ${before_ud4}  ${before_note}

*** Keywords ***
Log In and Set Up Test
    [Documentation]     Logs in and configures everything that is required for the test to run

    Log Into XIQSE and Close Panels                  ${XIQSE_USERNAME}    ${XIQSE_PASSWORD}    url=${XIQSE_URL}
    Set Option Web Server Session Timeout and Confirm Success  7  day(s)
    Set Option Device Tree Name Format and Confirm Success   IP Address
    Disable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver    ${WORLD_SITE}
    Onboard XIQSE To XIQ If In Connected Mode        ${INSTALL_MODE}  ${XIQSE_IP_ADDRESS}  ${XIQ_EMAIL}  ${XIQ_PASSWORD}
    Navigate and Create Device                       ${DUT_IP}  ${DUT_PROFILE}
    Clear Operations Panel and Confirm Success

Tear Down Test and Close Session
    [Documentation]     Logs in and cleans up all items that were set up for the test

    Navigate to Devices and Confirm Success
    Delete Device and Confirm Success             ${DUT_IP}
    Restore Web Server Options to Default and Confirm Success
    Restore Site Engine General Options to Default and Confirm Success
    Enable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver    ${WORLD_SITE}
    Log Out of XIQSE and Quit Browser
    Remove XIQSE From XIQ If In Connected Mode    ${INSTALL_MODE}  ${XIQ_EMAIL}  ${XIQ_PASSWORD}  ${XIQ_URL}  ${XIQSE_MAC}

Set Profile and Confirm Success
    [Documentation]     Sets the profile to the specified value and confirms the action was successful
    [Arguments]         ${ip}    ${profile}

    # Update the profile
    ${set_result}=  XIQSE Device Set Profile            ${ip}  ${profile}
    Should Be Equal As Integers                         ${set_result}     1

    # Confirm the value after the update
    ${after_result}=  XIQSE Confirm Device Profile      ${ip}  ${profile}
    Should Be Equal As Integers                         ${after_result}     1

Set Device Annotations
    [Documentation]     Sets the device annotations on the specified device.
    [Arguments]         ${ip}    ${nn}  ${asset}  ${ud1}  ${ud2}  ${ud3}  ${ud4}  ${note}

    ${result}=  XIQSE Configure Device Annotations and Save    ${ip}  nickname=${nn}  asset_tag=${asset}
    ...    ud1=${ud1}  ud2=${ud2}  ud3=${ud3}  ud4=${ud4}  note=${note}
    Should Be Equal As Integers     ${result}  1
