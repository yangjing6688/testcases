#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Heidi S. White
# Description   : Test Suite for testing the device 360 view of the VOSS switch in terms of the graphs and charts.
#                 This is qTest test case TC-8492 in the CSIT project.

*** Settings ***
Library          xiq/flows/manage/Device360.py

Resource         ../../VOSS/Resources/AllResources.robot

Force Tags       testbed_voss_node

Suite Setup      Log Into XIQ and Set Up Test
Suite Teardown   Tear Down Test and Close Session


*** Variables ***
${XIQ_URL}                  ${xiq.test_url}
${XIQ_USER}                 ${xiq.tenant_username}
${XIQ_PASSWORD}             ${xiq.tenant_password}
${IQAGENT}                  ${xiq.sw_connection_host}

${DUT_SERIAL}               ${netelem3.serial}
${DUT_MAC}                  ${netelem3.mac}
${DUT_NAME}                 ${netelem3.name}
${DUT_IP}                   ${netelem3.ip}
${DUT_PORT}                 ${netelem3.port}
${DUT_USERNAME}             ${netelem3.username}
${DUT_PASSWORD}             ${netelem3.password}
${DUT_PLATFORM}             ${netelem3.platform}
${DUT_TEST_PORT}            ${netelem3.test_port_num}
${DUT_MAKE}                 ${netelem3.make}
${DUT_CLI_TYPE}             ${netelem3.cli_type}

${LOCATION}                 San Jose, building_01, floor_02

@{OVERVIEW_DAY_HOURS}       1  2  4  8  24
@{OVERVIEW_WEEK_DAYS}       1  2  7
@{OVERVIEW_MONTH_DAYS}      7  14  30  90

@{CLIENTS_DAY_HOURS}        1  2  4  8  24
@{CLIENTS_WEEK_DAYS}        1  2  7
@{CLIENTS_MONTH_DAYS}       7  14  30  90

@{DIAGNOSTICS_DAY_HOURS}    1  2  4  8  24
@{DIAGNOSTICS_WEEK_DAYS}    1  2  7
@{DIAGNOSTICS_MONTH_DAYS}   7  14  30


*** Test Cases ***
Test 1: Confirm Monitor Overview Page Functionality
    [Documentation]     Confirms functionality of graphs on the Monitor> Overview page of the Device360 view
    [Tags]              csit_tc_8492    aiq_1332    development    xiq    voss    d360    test1

    [Setup]  Navigate To Device360 Page With MAC     ${DUT_MAC}

    Device360 Navigate to Monitor Overview
    Confirm Overview Chart Displayed
    Confirm Time Range Selections Can Be Made    ${OVERVIEW_DAY_HOURS}  ${OVERVIEW_WEEK_DAYS}  ${OVERVIEW_MONTH_DAYS}

    [Teardown]  Close Device360 Window

Test 2: Confirm Monitor Clients Page Functionality
    [Documentation]     Confirms functionality of graphs on the Monitor> Clients page of the Device360 view
    [Tags]              csit_tc_8492    aiq_1332    development    xiq    voss    d360    test2

    [Setup]  Navigate To Device360 Page With MAC     ${DUT_MAC}

    Device360 Navigate to Monitor Clients
    Confirm Clients Chart Displayed
    Confirm Time Range Selections Can Be Made    ${CLIENTS_DAY_HOURS}  ${CLIENTS_WEEK_DAYS}  ${CLIENTS_MONTH_DAYS}

    [Teardown]  Close Device360 Window

Test 3: Confirm Monitor Diagnostics Page Functionality
    [Documentation]     Confirms functionality of graphs on the Monitor> Diagnostics page of the Device360 view
    [Tags]              known_issue    csit_tc_8492    aiq_1332    development    xiq    voss    d360    test3

    [Setup]  Navigate To Device360 Page With MAC     ${DUT_MAC}

    Log To Console  KNOWN ISSUE: XIQ-273

    Device360 Navigate to Monitor Diagnostics
    Confirm Diagnostics Chart Displayed
    Confirm Time Range Selections Can Be Made    ${DIAGNOSTICS_DAY_HOURS}  ${DIAGNOSTICS_WEEK_DAYS}  ${DIAGNOSTICS_MONTH_DAYS}
    Confirm Port Selections

    [Teardown]  Close Device360 Window


*** Keywords ***
Log Into XIQ and Set Up Test
    [Documentation]     Logs into XIQ and sets up the elements necessary to complete this test suite

    Log Into XIQ and Confirm Success            ${XIQ_USER}  ${XIQ_PASSWORD}  ${XIQ_URL}
    Configure Test Device                       ${DUT_IP}  ${DUT_PORT}  ${DUT_USERNAME}  ${DUT_PASSWORD}  ${DUT_CLI_TYPE}  ${IQAGENT}
    Onboard New Test Device                     ${DUT_SERIAL}  ${DUT_MAKE}  ${LOCATION}
    Confirm Device Serial Online                ${DUT_SERIAL}

Tear Down Test and Close Session
    [Documentation]     Cleans up test data, logs out of XIQ, and closes the browser

    Clean Up Test Device and Confirm Success    ${DUT_SERIAL}
    Log Out of XIQ and Quit Browser

Onboard New Test Device
    [Documentation]     Onboards the specified test device, deleting it first if it already exists
    [Arguments]         ${serial}  ${make}  ${location}

    Navigate to Devices and Confirm Success

    # If the device has already been onboarded, delete it first
    Delete Device and Confirm Success  ${serial}
    Confirm Device Serial Not Present  ${serial}

    # Onboard the device
    Onboard Device    ${serial}  ${make}  location=${location}
    sleep   ${DEVICE_ONBOARDING_WAIT}
    Confirm Device Serial Present  ${serial}

Configure Test Device
    [Documentation]     Configures the specified test device by rebooting a known good configuration file and then configuring the iqagent
    [Arguments]         ${ip}  ${port}  ${user}  ${pwd}  ${cli_type}  ${agent}

    Boot Switch To Known Good Configuration     ${ip}  ${port}  ${user}  ${pwd}  ${cli_type}
    Configure Device To Connect To Cloud        ${cli_type}  ${ip}  ${port}  ${user}  ${pwd}  ${agent}

Clean Up Test Device and Confirm Success
    [Documentation]     Deletes the specified device and confirms the action was successful
    [Arguments]         ${serial}

    Navigate to Devices and Confirm Success

    Delete Device and Confirm Success  ${serial}
    Confirm Device Serial Not Present  ${serial}

Confirm Overview Chart Displayed
    [Documentation]     Confirms the chart is displayed for the Monitor> Overview page

    ${chart_result}=  Confirm Device360 Monitor Overview Chart Displayed
    Should Be Equal As Integers  ${chart_result}     1

Confirm Clients Chart Displayed
    [Documentation]     Confirms the chart is displayed for the Monitor> Clients page

    ${chart_result}=  Confirm Device360 Monitor Clients Chart Displayed
    Should Be Equal As Integers  ${chart_result}     1

Confirm Diagnostics Chart Displayed
    [Documentation]     Confirms the chart is displayed for the Monitor> Diagnostics page

    ${chart_result}=  Confirm Device360 Monitor Diagnostics Chart Displayed
    Should Be Equal As Integers  ${chart_result}     1

Confirm Time Range Selections Can Be Made
    [Documentation]     Confirms each of the time range selections can be made
    [Arguments]   ${day_values}  ${week_values}  ${month_values}

    Confirm Month Time Range Selections Can Be Made     ${month_values}
    Device360 Refresh Page
    Confirm Week Time Range Selections Can Be Made      ${week_values}
    Device360 Refresh Page
    Confirm Day Time Range Selections Can Be Made       ${day_values}

Confirm Day Time Range Selections Can Be Made
    [Documentation]     Confirms each of the Day time range selections can be made
    [Arguments]   ${hour_list}

    ${time_range_select}=  Device360 Select Day Time Range
    Should Be Equal As Integers  ${time_range_select}     1
    sleep  2 seconds

    FOR  ${hour}  IN  @{hour_list}
        ${result}=  Device360 Select Day Time Range Hours Button  ${hour}
        Should Be Equal As Integers  ${result}     1
    END

Confirm Week Time Range Selections Can Be Made
    [Documentation]     Confirms each of the Week time range selections can be made
    [Arguments]   ${day_list}

    ${time_range_select}=  Device360 Select Week Time Range
    Should Be Equal As Integers  ${time_range_select}     1
    sleep  2 seconds

    FOR  ${day}  IN  @{day_list}
        ${result}=  Device360 Select Week Time Range Days Button  ${day}
        Should Be Equal As Integers  ${result}     1
    END

Confirm Month Time Range Selections Can Be Made
    [Documentation]     Confirms each of the Month time range selections can be made
    [Arguments]   ${day_list}

    ${time_range_select}=  Device360 Select Month Time Range
    Should Be Equal As Integers  ${time_range_select}     1
    sleep  2 seconds

    FOR  ${day}  IN  @{day_list}
        ${result}=  Device360 Select Month Time Range Days Button  ${day}
        Should Be Equal As Integers  ${result}     1
    END

Confirm Port Selections
    [Documentation]     Confirms the Select All Ports and Deselect All Ports actions work correctly, as well as selecting/deselecting an individual port

    # Deselect All Ports
    ${deselect_action}=  Device360 Port Diagnostics Deselect All Ports
    Should Be Equal As Integers  ${deselect_action}     1
    ${deselect_check}=  Confirm Device360 Port Diagnostics All Ports Deselected
    Should Be Equal As Integers  ${deselect_check}     1

    # Manually Select Specific Port
    ${port_check}=  Confirm Device360 Port Diagnostics Port Deselected  ${DUT_TEST_PORT}
    Should Be Equal As Integers  ${port_check}     1
    Device360 Port Diagnostics Select Port  ${DUT_TEST_PORT}
    ${port_check}=  Confirm Device360 Port Diagnostics Port Selected  ${DUT_TEST_PORT}
    Should Be Equal As Integers  ${port_check}     1

    # Select All Ports
    ${select_action}=  Device360 Port Diagnostics Select All Ports
    Should Be Equal As Integers  ${select_action}     1
    ${select_check}=  Confirm Device360 Port Diagnostics All Ports Selected
    Should Be Equal As Integers  ${select_check}     1

    # Manually Deselect Specific Port
    ${port_check}=  Confirm Device360 Port Diagnostics Port Selected  ${DUT_TEST_PORT}
    Should Be Equal As Integers  ${port_check}     1
    Device360 Port Diagnostics Deselect Port  ${DUT_TEST_PORT}
    ${port_check}=  Confirm Device360 Port Diagnostics Port Deselected  ${DUT_TEST_PORT}
    Should Be Equal As Integers  ${port_check}     1
