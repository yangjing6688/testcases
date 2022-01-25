#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Heidi S. White
# Description   : Test Suite for sanity testing of basic XIQ-SE device tree context functionality.
#                 This is qTest TC-891 in the XIQ-SE project.

*** Settings ***
Library         xiqse/flows/network/devices/tree_panel/XIQSE_NetworkDevicesTreePanel.py

Resource        ../../SampleTests/Resources/AllResources.robot

Force Tags      testbed_0_node

Suite Setup     Log In and Set Up Test
Suite Teardown  Log Out of XIQSE and Quit Browser


*** Variables ***
${ENV}                  environment.remote.chrome.windows.xiqse1.yaml
${TOPO}                 topo.test.xiqse1.connected.yaml
${TESTBED}              SALEM/Dev/devices-salem-acceptance.yaml

${XIQSE_URL}            ${xiqse.url}
${XIQSE_USER}           ${xiqse.user}
${XIQSE_PASSWORD}       ${xiqse.password}


*** Test Cases ***
Test 1: Device Tree Context Selection - By Contact
    [Documentation]     Confirms the 'by Contact' device tree context can be selected
    [Tags]              xiqse_tc_891    aiq_1332    development    sample    xiqse    device_tree    test1

    ${result}=  XIQSE Devices Select Device Tree Context  by Contact
    Should Be Equal As Integers  ${result}     1
    sleep  1 second

Test 2: Device Tree Context Selection - By Device Type
    [Documentation]     Confirms the 'by Device Type' device tree context can be selected
    [Tags]              xiqse_tc_891    aiq_1332    development    sample    xiqse    device_tree    test2

    ${result}=  XIQSE Devices Select Device Tree Context  by Device Type
    Should Be Equal As Integers  ${result}     1
    sleep  1 second

Test 3: Device Tree Context Selection - By IP
    [Documentation]     Confirms the 'by IP' device tree context can be selected
    [Tags]              xiqse_tc_891    aiq_1332    development    sample    xiqse    device_tree    test3

    ${result}=  XIQSE Devices Select Device Tree Context  by IP
    Should Be Equal As Integers  ${result}     1
    sleep  1 second

Test 4: Device Tree Context Selection - By Location
    [Documentation]     Confirms the 'by Location' device tree context can be selected
    [Tags]              xiqse_tc_891    aiq_1332    development    sample    xiqse    device_tree    test4

    ${result}=  XIQSE Devices Select Device Tree Context  by Location
    Should Be Equal As Integers  ${result}     1
    sleep  1 second

Test 5: Device Tree Context Selection - Extended Bridges
    [Documentation]     Confirms the 'Extended Bridges' device tree context can be selected
    [Tags]              xiqse_tc_891    aiq_1332    development    sample    xiqse    device_tree    test5

    ${result}=  XIQSE Devices Select Device Tree Context  Extended Bridges
    Should Be Equal As Integers  ${result}     1
    sleep  1 second

Test 6: Device Tree Context Selection - Sites
    [Documentation]     Confirms the 'Sites' device tree context can be selected
    [Tags]              xiqse_tc_891    aiq_1332    development    sample    xiqse    device_tree    test6

    ${result}=  XIQSE Devices Select Device Tree Context  Sites
    Should Be Equal As Integers  ${result}     1
    sleep  1 second

Test 7: Device Tree Context Selection - User Device Groups
    [Documentation]     Confirms the 'User Device Groups' device tree context can be selected
    [Tags]              xiqse_tc_891    aiq_1332    development    sample    xiqse    device_tree    test7

    ${result}=  XIQSE Devices Select Device Tree Context  User Device Groups
    Should Be Equal As Integers  ${result}     1
    sleep  1 second

Test 8: Device Tree Context Selection - Wireless Controllers
    [Documentation]     Confirms the 'Wireless Controllers' device tree context can be selected
    [Tags]              xiqse_tc_891    aiq_1332    development    sample    xiqse    device_tree    test8

    ${result}=  XIQSE Devices Select Device Tree Context  Wireless Controllers
    Should Be Equal As Integers  ${result}     1
    sleep  1 second


*** Keywords ***
Log In and Set Up Test
    [Documentation]     Logs in and sets up the components for the test

    # Log into XIQSE and close the banner messages and help panel
    Log Into XIQSE and Close Panels     ${XIQSE_USER}    ${XIQSE_PASSWORD}    url=${XIQSE_URL}

    # Navigate to the Network> Devices> Devices page
    Navigate to Devices and Confirm Success
