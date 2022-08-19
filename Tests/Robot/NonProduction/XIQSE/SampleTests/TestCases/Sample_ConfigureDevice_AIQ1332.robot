#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Heidi S. White
# Description   : Test Suite for sanity testing of basic XIQ-SE device configuration functionality.
#                 This is qTest TC-890 in the XIQ-SE project.

*** Settings ***
Library         Collections
Library         xiqse/flows/network/common/XIQSE_NetworkCommonConfigureDevice.py
Library         xiqse/flows/network/common/configure_device/XIQSE_NetworkCommonConfigureDeviceDevice.py

Resource        ../../SampleTests/Resources/AllResources.robot

Force Tags      testbed_1_node

Suite Setup     Log In and Set Up Test
Suite Teardown  Tear Down Test and Close Session


*** Variables ***
${ENV}                   environment.remote.chrome.windows.xiqse1.yaml
${TOPO}                  topo.test.xiqse1.connected.yaml
${TESTBED}               SALEM/Dev/devices-salem-acceptance.yaml

${XIQSE_URL}             ${xiqse.url}
${XIQSE_USER}            ${xiqse.user}
${XIQSE_PASSWORD}        ${xiqse.password}

${DUT1_IP}               ${netelem1.ip}
${DUT1_PROFILE}          ${netelem1.profile}
${DUT1_SERIAL}           ${netelem1.serial}

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
${TEST_WEBVIEW_URL}      http://%DUT1_IP
${TEST_POLL_GROUP}       Less Frequent
${TEST_POLL_TYPE}        Ping
${TEST_TIMEOUT}          10
${TEST_RETRIES}          5
${TEST_TOPO}             Appliance
${TEST_COLL_MODE}        Threshold Alarms
${TEST_COLL_INTERVAL}    12


*** Test Cases ***
Test 1: Configure Device Annotations
    [Documentation]     Confirms a device's annotations can be configured and saved
    [Tags]              tcxe_890    aiq_1332    development    sample    xiqse    configure_device    test1

    # Make sure the necessary columns are displayed
    XIQSE Devices Show Columns    Asset Tag  User Data 1  User Data 2  User Data 3  User Data 4  Notes

    # Get the current values so we can reset them after the test
    &{before_info}=     XIQSE Get Device Row Values
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
    &{after_info}=     XIQSE Get Device Row Values
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

Test 2: Configure Device
    [Documentation]     Confirms a device's device tab values can be configured and saved
    [Tags]              tcxe_890    aiq_1332    development    sample    xiqse    configure_device    test2

    # Make sure the necessary columns are displayed
    XIQSE Devices Show Columns    System Name  Contact  Location

    # Get the current values so we can reset them after the test
    &{before_info}=     XIQSE Get Device Row Values  ${DUT1_IP}  System Name,Contact,Location

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

Test 3: Configure Device Tab Settings
    [Documentation]     Confirms a device's device tab values can be configured - these changes are not saved
    [Tags]              tcxe_890    aiq_1332    development    sample    xiqse    configure_device    test3

    XIQSE Devices Refresh Table

    # Open the Configure Device dialog
    ${open_result}=  XIQSE Open Configure Device Dialog    ${DUT1_IP}
    Should Be Equal As Integers     ${open_result}  1

    # Select the Device tab
    ${tab_result}=  XIQSE Configure Device Dialog Select Tab    Device
    Should Be Equal As Integers     ${tab_result}  1


    # Confirm the various fields of the Device tab can be set
    ${field_result}=  XIQSE Configure Device Dialog Set System Name                     ${TEST_SYSTEMNAME}
    Should Be Equal As Integers     ${field_result}  1

    ${field_result}=  XIQSE Configure Device Dialog Set Contact                         ${TEST_CONTACT}
    Should Be Equal As Integers     ${field_result}  1

    ${field_result}=  XIQSE Configure Device Dialog Set Location                        ${TEST_LOCATION}
    Should Be Equal As Integers     ${field_result}  1

    ${field_result}=  XIQSE Configure Device Dialog Set Admin Profile                   ${TEST_PROFILE}
    Should Be Equal As Integers     ${field_result}  1

    ${field_result}=  XIQSE Configure Device Dialog Set Replacement Serial              ${DUT1_SERIAL}
    Should Be Equal As Integers     ${field_result}  1

    ${field_result}=  XIQSE Configure Device Dialog Enable Remove From Service
    Should Be Equal As Integers     ${field_result}  1

    ${field_result}=  XIQSE Configure Device Dialog Disable Remove From Service
    Should Be Equal As Integers     ${field_result}  1

    ${field_result}=  XIQSE Configure Device Dialog Disable Use Default WebView URL
    Should Be Equal As Integers     ${field_result}  1

    ${field_result}=  XIQSE Configure Device Dialog Set WebView URL                     ${TEST_WEBVIEW_URL}
    Should Be Equal As Integers     ${field_result}  1

    ${field_result}=  XIQSE Configure Device Dialog Enable Use Default WebView URL
    Should Be Equal As Integers     ${field_result}  1

    ${field_result}=  XIQSE Configure Device Dialog Set Default Site                    ${TEST_SITE}
    Should Be Equal As Integers     ${field_result}  1

    ${field_result}=  XIQSE Configure Device Dialog Set Default Site                    World  import_site=Yes
    Should Be Equal As Integers     ${field_result}  1

    ${field_result}=  XIQSE Configure Device Dialog Set Default Site                    ${TEST_SITE}  import_site=No
    Should Be Equal As Integers     ${field_result}  1

    ${field_result}=  XIQSE Configure Device Dialog Set Poll Group                      ${TEST_POLL_GROUP}
    Should Be Equal As Integers     ${field_result}  1

    ${field_result}=  XIQSE Configure Device Dialog Set Poll Type                       ${TEST_POLL_TYPE}
    Should Be Equal As Integers     ${field_result}  1

    ${field_result}=  XIQSE Configure Device Dialog Set SNMP Timeout                    ${TEST_TIMEOUT}
    Should Be Equal As Integers     ${field_result}  1

    ${field_result}=  XIQSE Configure Device Dialog Set SNMP Retries                    ${TEST_RETRIES}
    Should Be Equal As Integers     ${field_result}  1

    ${field_result}=  XIQSE Configure Device Dialog Set Topology Layer                  ${TEST_TOPO}
    Should Be Equal As Integers     ${field_result}  1

    ${field_result}=  XIQSE Configure Device Dialog Set Collection Mode                 ${TEST_COLL_MODE}
    Should Be Equal As Integers     ${field_result}  1

    ${field_result}=  XIQSE Configure Device Dialog Set Collection Interval             ${TEST_COLL_INTERVAL}
    Should Be Equal As Integers     ${field_result}  1

    [Teardown]  Close Configure Device Dialog and Confirm Success


*** Keywords ***
Log In and Set Up Test
    [Documentation]     Logs in and sets up the components for the test

    # Log into XIQSE and close the banner messages and help panel
    Log Into XIQSE and Close Panels     ${XIQSE_USER}  ${XIQSE_PASSWORD}  url=${XIQSE_URL}

    # Add the test device
    Navigate and Create Device          ${DUT1_IP}  ${DUT1_PROFILE}
    Confirm Device Status Up            ${DUT1_IP}

    # Add a test site
    Navigate and Create Site            ${TEST_SITE}

    # Add a test profile
    Navigate and Create Profile         ${TEST_PROFILE}  ${TEST_PROFILE_VERSION}

    # Navigate to the Devices tab for the World site
    Navigate to Site Devices and Confirm Success    World

Tear Down Test and Close Session
    [Documentation]     Cleans up XIQSE test components and closes the browser

    # Delete the test device
    Navigate and Delete Device      ${DUT1_IP}

    # Delete the test site
    Navigate and Delete Site        ${TEST_SITE}

    # Delete the test profile
    Navigate and Delete Profile     ${TEST_PROFILE}

    # Log out of XIQSE and close the browser
    Log Out of XIQSE and Quit Browser

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

Close Configure Device Dialog and Confirm Success
    [Documentation]     Clicks Cancel in the Configure Device dialog.

    ${close_result}=  XIQSE Configure Device Dialog Click Cancel
    Should Be Equal As Integers     ${close_result}  1
