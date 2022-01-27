#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Heidi S. White
# Description   : Test Suite for sanity testing of basic XIQ-SE discovery functionality.
#                 This is qTest TC-138 in the XIQ-SE project.

*** Settings ***
Resource        ../../SampleTests/Resources/AllResources.robot

Force Tags      testbed_license_node

Suite Setup     Log In and Set Up Test
Suite Teardown  Tear Down Test and Close Session


*** Variables ***
${ENV}                  environment.remote.chrome.windows.xiqse1.yaml
${TOPO}                 topo.test.xiqse1.connected.yaml
${TESTBED}              SALEM/Dev/devices-salem-acceptance.yaml

${XIQSE_URL}            ${xiqse.url}
${XIQSE_USER}           ${xiqse.user}
${XIQSE_PASSWORD}       ${xiqse.password}

${DISCOVER_IP_START}    ${pilot1.ip}
${DISCOVER_IP_END}      ${pilot3.ip}
${DISCOVER_SUBNET}      ${pilot1.ip}/24
${DISCOVER_PROFILE}     ${pilot1.profile}

${DUT_IP}               ${pilot1.ip}
${DUT_SERIAL}           ${pilot1.serial}

${TEST_SITE}            AutomationSite


*** Test Cases ***
Test 1: Discover IP Range
    [Documentation]     Confirms an IP range discovery can be performed
    [Tags]              xiqse_tc_138    aiq_1332    development    sample    xiqse    discovery    test1

    Navigate to Site Tab and Confirm Success                        ${TEST_SITE}
    Perform IP Range Discovery and Obtain Discovered Device Count   ${DISCOVER_IP_START}  ${DISCOVER_IP_END}  ${DISCOVER_PROFILE}
    Clean Up IP Range Discovery Settings and Confirm Success        ${DISCOVER_IP_START}  ${DISCOVER_IP_END}  ${DISCOVER_PROFILE}
    Confirm Discovered Row Count                                    ${RANGE_COUNT}

Test 2: Discovery Check Column Value
    [Documentation]     Checks the column value for a device in the Discovered tab
    [Tags]              xiqse_tc_138    aiq_1332    development    sample    xiqse    discovery    test2

    Navigate to Discovered and Confirm Success
    XIQSE Discovered Do Not Show In Groups

    Confirm IP Address Present in Discovered Table              ${DUT_IP}

    ${column_check}=  XIQSE Discovered Get Device Column Value  ${DUT_SERIAL}  IP Address
    Should Be Equal As Strings                                  ${column_check}  ${DUT_IP}

Test 3: Add Selected Device from Discovered Tab
    [Documentation]     Confirms a specific device can be removed from the Discovered tab
    [Tags]              xiqse_tc_138    aiq_1332    development    sample    xiqse    discovery    test3

    Navigate to Discovered and Confirm Success
    XIQSE Discovered Do Not Show In Groups

    # Add a device from the Discovered table
    Confirm IP Address Present in Discovered Table              ${DISCOVER_IP_START}
    ${add_result}=  XIQSE Discovered Add Device                 ${DISCOVER_IP_START}
    Should Be Equal As Integers                                 ${add_result}     1

    # Confirm the device was removed from the Discovered table
    Confirm IP Address Not Present in Discovered Table          ${DISCOVER_IP_START}

    # Confirm the device is present in the Devices table
    Navigate to Devices and Confirm Success
    Confirm IP Address Present in Devices Table                 ${DISCOVER_IP_START}

    [Teardown]  Navigate and Delete Device                      ${DISCOVER_IP_START}

Test 4: Clear Selected Device from Discovered Tab
    [Documentation]     Confirms a specific device can be removed from the Discovered tab
    [Tags]              xiqse_tc_138    aiq_1332    development    sample    xiqse    discovery    test4

    Navigate to Discovered and Confirm Success
    XIQSE Discovered Do Not Show In Groups

    Confirm IP Address Present in Discovered Table      ${DISCOVER_IP_END}
    Clear IP From Discovered and Confirm Success        ${DISCOVER_IP_END}

Test 5: Clear All from Discovered Tab - Small Number of Devices
    [Documentation]     Confirms clear all removes all devices from the Discovered tab
    [Tags]              xiqse_tc_138    aiq_1332    development    sample    xiqse    discovery    test5

    Navigate to Discovered and Confirm Success
    Clear All From Discovered and Confirm Success

Test 6: Discover Subnet
    [Documentation]     Confirms a subnet discovery can be performed
    [Tags]              xiqse_tc_138    aiq_1332    development    sample    xiqse    discovery    test6

    Navigate to Site Tab and Confirm Success                        ${TEST_SITE}
    Perform Subnet Discovery and Obtain Discovered Device Count     ${DISCOVER_SUBNET}  ${DISCOVER_PROFILE}
    Clean Up Subnet Discovery Settings and Confirm Success          ${DISCOVER_SUBNET}  ${DISCOVER_PROFILE}
    Confirm Discovered Row Count                                    ${SUBNET_COUNT}

Test 7: Clear All from Discovered Tab - Large Number of Devices
    [Documentation]     Confirms clear all removes all devices from the Discovered tab
    [Tags]              xiqse_tc_138    aiq_1332    development    sample    xiqse    discovery    test7

    Navigate to Discovered and Confirm Success
    Clear All From Discovered and Confirm Success

Test 8: Confirm Duplicate Addresses Handled Gracefully
    [Documentation]     Confirms attempting to add a duplicate address entry is handled gracefully (no error)
    [Tags]              xiqse_tc_138    aiq_1332    development    sample    xiqse    discovery    test8

    Navigate to Site Tab and Confirm Success    ${TEST_SITE}

    ${nav_result}=   XIQSE Site Select Discover Tab
    Should Be Equal As Integers      ${nav_result}     1

    # ADDRESS RANGE
    ${add1_result}=  XIQSE Discover Addresses Add Address Range     ${DISCOVER_IP_START}  ${DISCOVER_IP_END}
    Should Be Equal As Integers      ${add1_result}    1
    ${add2_result}=  XIQSE Discover Addresses Add Address Range     ${DISCOVER_IP_START}  ${DISCOVER_IP_END}
    Should Be Equal As Integers      ${add2_result}    1
    ${del_result}=   XIQSE Discover Addresses Delete Address Range  ${DISCOVER_IP_START}  ${DISCOVER_IP_END}
    Should Be Equal As Integers      ${del_result}     1

    # SUBNET
    ${add1_result}=  XIQSE Discover Addresses Add Subnet            ${DISCOVER_SUBNET}
    Should Be Equal As Integers      ${add1_result}    1
    ${add2_result}=  XIQSE Discover Addresses Add Subnet            ${DISCOVER_SUBNET}
    Should Be Equal As Integers      ${add2_result}    1
    ${del_result}=   XIQSE Discover Addresses Delete Subnet         ${DISCOVER_SUBNET}
    Should Be Equal As Integers      ${del_result}     1

    # SEED ADDRESS
    ${add1_result}=  XIQSE Discover Addresses Add Seed Address      ${DISCOVER_IP_START}
    Should Be Equal As Integers      ${add1_result}    1
    ${add2_result}=  XIQSE Discover Addresses Add Seed Address      ${DISCOVER_IP_START}
    Should Be Equal As Integers      ${add2_result}    1
    ${del_result}=   XIQSE Discover Addresses Delete Seed Address   ${DISCOVER_IP_START}
    Should Be Equal As Integers      ${del_result}     1

    [Teardown]  Save Site Changes and Confirm Success


*** Keywords ***
Log In and Set Up Test
    [Documentation]     Logs in and sets up the components for the test

   # Log into XIQSE and close the banner messages and help panel
    Log Into XIQSE and Close Panels     ${XIQSE_USER}    ${XIQSE_PASSWORD}    url=${XIQSE_URL}

    # Create the test site
    Navigate and Create Site     ${TEST_SITE}

    # Confirm the Discovered tab is currently empty
    Confirm Discovered Row Count        0

Tear Down Test and Close Session
    [Documentation]     Cleans up XIQ and XIQSE test components and closes the browser

    # Delete the Site
    Navigate and Delete Site     ${TEST_SITE}
    sleep  2 seconds

    # Log out of XIQSE and close the browser
    Log Out of XIQSE and Quit Browser

Perform IP Range Discovery and Obtain Discovered Device Count
    [Documentation]     Performs an IP Range discovery in XIQ-SE and confirms the action was successful
    [Arguments]         ${ip_start}  ${ip_end}  ${profile}

    # Clear the contents of the Operations panel
    Clear Operations Panel and Confirm Success

    # Perform the discovery
    Perform IP Range Discovery and Confirm Success  ${ip_start}  ${ip_end}  ${profile}

    # Get the number of devices which were discovered and store them in a variable
    ${device_count}=  Get Discovered Device Count From Operations Panel
    Set Suite Variable   ${RANGE_COUNT}  ${device_count}

Perform Subnet Discovery and Obtain Discovered Device Count
    [Documentation]     Performs a subnet discovery in XIQ-SE and confirms the action was successful
    [Arguments]         ${subnet_mask}  ${profile}

    # Clear the contents of the Operations panel
    Clear Operations Panel and Confirm Success

    # Perform the discovery
    Perform Subnet Discovery and Confirm Success  ${subnet_mask}  ${profile}

    # Get the number of devices which were discovered and store them in a variable
    ${device_count}=  Get Discovered Device Count From Operations Panel
    Set Suite Variable   ${SUBNET_COUNT}  ${device_count}
