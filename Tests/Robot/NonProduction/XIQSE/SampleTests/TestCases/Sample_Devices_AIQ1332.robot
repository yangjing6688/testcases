#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Heidi S. White
# Description   : Test Suite for sanity testing of basic XIQ-SE device functionality.
#                 This is qTest TC-129 in the XIQ-SE project.

*** Settings ***
Library         Collections

Resource        ../../SampleTests/Resources/AllResources.robot

Force Tags      testbed_1_node

Suite Setup     Log In and Set Up Test
Suite Teardown  Log Out of XIQSE and Quit Browser


*** Variables ***
${ENV}                   environment.remote.chrome.windows.xiqse1.yaml
${TOPO}                  topo.test.xiqse1.connected.yaml
${TESTBED}               SALEM/Dev/devices-salem-acceptance.yaml

${XIQSE_URL}             ${xiqse.url}
${XIQSE_USER}            ${xiqse.user}
${XIQSE_PASSWORD}        ${xiqse.password}

${DUT1_IP}               ${netelem1.ip}
${DUT1_PROFILE}          ${netelem1.profile}

${TEST_SITE}             AUTO_SITE
${TEST_PROFILE}          AUTO_PROFILE
${TEST_PROFILE_VERSION}  SNMPv2
${TEST_NICKNAME}         AUTO NICKNAME
${TEST_ASSET_TAG}        AUTO ASSET TAG
${TEST_USER_DATA_1}      AUTO DATA 1
${TEST_USER_DATA_2}      AUTO DATA 2
${TEST_USER_DATA_3}      AUTO DATA 3
${TEST_USER_DATA_4}      AUTO DATA 4
${TEST_NOTE}             AUTO NOTE
${TEST_SYSTEMNAME}       AUTO NAME
${TEST_CONTACT}          AUTO CONTACT
${TEST_LOCATION}         AUTO LOCATION


*** Test Cases ***
Test 1: Add Device
    [Documentation]     Confirms a device can be added
    [Tags]              tcxe_129    aiq_1332    development    sample    xiqse    devices    test1

    Navigate and Create Device  ${DUT1_IP}  ${DUT1_PROFILE}
    Confirm Device Status Up    ${DUT1_IP}

Test 2: Create Site
    [Documentation]     Confirms a site can be created
    [Tags]              tcxe_129    aiq_1332    development    sample    xiqse    devices    test2

    Navigate and Create Site  ${TEST_SITE}

    [Teardown]  Select Site and Confirm Success     World

Test 3: Select Site
    [Documentation]     Confirms a site can be selected
    [Tags]              tcxe_129    aiq_1332    development    sample    xiqse    devices    test3

    # Select the site in the devices tree
    Navigate to Site Tree Node and Confirm Success  ${TEST_SITE}

    # Select the test site tab
    Navigate to Site Tab and Confirm Success  ${TEST_SITE}

    [Teardown]  Navigate to Site Devices and Confirm Success    World

Test 4: Set Device Profile
    [Documentation]     Confirms the profile can be changed on a device
    [Tags]              tcxe_129    aiq_1332    development    sample    xiqse    devices    test4

    # Create the profile to use in the test
    Navigate and Create Profile  ${TEST_PROFILE}  ${TEST_PROFILE_VERSION}

    # Navigate to the Network> Devices> Devices page
    Navigate to Devices and Confirm Success

    # Make sure the Admin Profile column is being displayed
    ${col}=  XIQSE Devices Show Columns  Admin Profile
    Should Be Equal As Integers          ${col}     1

    # Confirm the value before the update
    ${before_result}=  XIQSE Confirm Device Profile  ${DUT1_IP}  ${DUT1_PROFILE}
    Should Be Equal As Integers                      ${before_result}     1

    # Set the profile
    Set Profile and Confirm Success  ${DUT1_IP}  ${TEST_PROFILE}

    # Reset the profile
    Set Profile and Confirm Success  ${DUT1_IP}  ${DUT1_PROFILE}

    # Delete the test profile
    Navigate and Delete Profile  ${TEST_PROFILE}

    # Navigate to the Network> Devices> Devices page
    Navigate to Devices and Confirm Success

Test 5: Configure Device Annotations
    [Documentation]     Confirms a device's annotations can be configured
    [Tags]              tcxe_129    aiq_1332    development    sample    xiqse    devices    test5

    Navigate to Devices and Confirm Success

    # Make sure the necessary columns are displayed
    XIQSE Devices Show Columns    Asset Tag  User Data 1  User Data 2  User Data 3  User Data 4  Notes

    # Get the current values so we can reset them after the test
    &{before_info}=  XIQSE Get Device Row Values
    ...  ${DUT1_IP}  Nickname,Asset Tag,User Data 1,User Data 2,User Data 3,User Data 4,Notes

    ${before_nn}=       Get From Dictionary  ${before_info}  Nickname
    ${before_asset}=    Get From Dictionary  ${before_info}  Asset Tag
    ${before_ud1}=      Get From Dictionary  ${before_info}  User Data 1
    ${before_ud2}=      Get From Dictionary  ${before_info}  User Data 2
    ${before_ud3}=      Get From Dictionary  ${before_info}  User Data 3
    ${before_ud4}=      Get From Dictionary  ${before_info}  User Data 4
    ${before_note}=     Get From Dictionary  ${before_info}  Notes

    # Update Device Annotations
    Set Device Annotations  ${DUT1_IP}  ${TEST_NICKNAME}  ${TEST_ASSET_TAG}  ${TEST_USER_DATA_1}  ${TEST_USER_DATA_2}
    ...  ${TEST_USER_DATA_3}  ${TEST_USER_DATA_4}  ${TEST_NOTE}

    # Confirm new values were set
    &{after_info}=  XIQSE Get Device Row Values
    ...  ${DUT1_IP}  Nickname,Asset Tag,User Data 1,User Data 2,User Data 3,User Data 4,Notes

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

    [Teardown]  Set Device Annotations  ${DUT1_IP}
    ...         ${before_nn}  ${before_asset}  ${before_ud1}  ${before_ud2}  ${before_ud3}  ${before_ud4}  ${before_note}

Test 6: Configure Device Tab
    [Documentation]     Confirms a device's device tab values can be configured
    [Tags]              tcxe_129    aiq_1332    development    sample    xiqse    devices    test6

    Navigate to Devices and Confirm Success

    # Make sure the necessary columns are displayed
    XIQSE Devices Show Columns    System Name  Contact  Location

    # Get the current values so we can reset them after the test
    &{before_info}=  XIQSE Get Device Row Values  ${DUT1_IP}  System Name,Contact,Location

    ${before_name}=        Get From Dictionary  ${before_info}  System Name
    ${before_contact}=     Get From Dictionary  ${before_info}  Contact
    ${before_loc}=         Get From Dictionary  ${before_info}  Location

    # Update Device Tab Values
    Set Device Tab Values  ${DUT1_IP}  ${TEST_SYSTEMNAME}  ${TEST_CONTACT}  ${TEST_LOCATION}

    # Confirm new values were set
    &{after_info}=     XIQSE Get Device Row Values  ${DUT1_IP}  System Name,Contact,Location

    ${after_name}=        Get From Dictionary  ${after_info}  System Name
    ${after_contact}=     Get From Dictionary  ${after_info}  Contact
    ${after_loc}=         Get From Dictionary  ${after_info}  Location

    Should Be Equal As Strings  ${after_name}       ${TEST_SYSTEMNAME}
    Should Be Equal As Strings  ${after_contact}    ${TEST_CONTACT}
    Should Be Equal As Strings  ${after_loc}        ${TEST_LOCATION}

    [Teardown]  Set Device Tab Values  ${DUT1_IP}  ${before_name}  ${before_contact}  ${before_loc}

Test 7: Filter Devices Table
    [Documentation]     Filters the devices table
    [Tags]              tcxe_129    aiq_1332    development    sample    xiqse    devices    test7

    Navigate to Devices and Confirm Success

    Search Device and Confirm Success  ${DUT1_IP}
    sleep  1 second
    Clear Search and Confirm Success

Test 8: Delete Device
    [Documentation]     Confirms a device can be deleted
    [Tags]              tcxe_129    aiq_1332    development    sample    xiqse    devices    test8

    Navigate and Delete Device  ${DUT1_IP}

Test 9: Delete Site
    [Documentation]     Confirms a site can be deleted
    [Tags]              tcxe_129    aiq_1332    development    sample    xiqse    devices    test9

    Navigate and Delete Site    ${TEST_SITE}

    [Teardown]  Navigate to Site Devices and Confirm Success    World


*** Keywords ***
Log In and Set Up Test
    [Documentation]     Logs in and sets up the components for the test

    # Log into XIQSE and close the banner messages and help panel
    Log Into XIQSE and Close Panels     ${XIQSE_USER}    ${XIQSE_PASSWORD}    url=${XIQSE_URL}

    # Navigate to the Network> Devices> Devices page
    Navigate to Devices and Confirm Success

Set Profile and Confirm Success
    [Documentation]     Sets the profile to the specified value and confirms the action was successful
    [Arguments]         ${ip}    ${profile}

    # Update the profile
    Set Device Profile and Confirm Success              ${ip}  ${profile}

    # Confirm the value after the update
    ${after_result}=  XIQSE Confirm Device Profile      ${ip}  ${profile}
    Should Be Equal As Integers                         ${after_result}     1

Set Device Annotations
    [Documentation]     Sets the device annotations on the specified device.
    [Arguments]         ${ip}    ${nn}  ${asset}  ${ud1}  ${ud2}  ${ud3}  ${ud4}  ${note}

    ${result}=  XIQSE Configure Device Annotations and Save  ${ip}  nickname=${nn}  asset_tag=${asset}
    ...    ud1=${ud1}  ud2=${ud2}  ud3=${ud3}  ud4=${ud4}  note=${note}
    Should Be Equal As Integers     ${result}  1

Set Device Tab Values
    [Documentation]     Sets the device tab values on the specified device.
    [Arguments]         ${ip}    ${name}  ${contact}  ${loc}

    ${result}=  XIQSE Configure Device Device Tab and Save  ${ip}  system_name=${name}  contact=${contact}  location=${loc}
    Should Be Equal As Integers     ${result}  1
