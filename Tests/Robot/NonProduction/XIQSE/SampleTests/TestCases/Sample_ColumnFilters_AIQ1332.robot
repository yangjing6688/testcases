#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Heidi S. White
# Description   : Test Suite for sanity testing of basic XIQ-SE column filters functionality.
#                 This is qTest TC-889 in the XIQ-SE project.

*** Settings ***
Library         xiqse/flows/common/XIQSE_CommonTable.py

Resource        ../../SampleTests/Resources/AllResources.robot

Force Tags      testbed_0_node

Suite Setup     Log In and Set Up Test
Suite Teardown  Tear Down Test and Close Session


*** Variables ***
${ENV}                  environment.remote.chrome.windows.xiqse1.yaml
${TOPO}                 topo.test.xiqse1.connected.yaml
${TESTBED}              SALEM/Dev/devices-salem-acceptance.yaml

${XIQSE_URL}            ${xiqse.url}
${XIQSE_USER}           ${xiqse.user}
${XIQSE_PASSWORD}       ${xiqse.password}


*** Test Cases ***
Test 1: Set a Single Text Column Filter
    [Documentation]     Confirms a column filter which uses a text field can be applied
    [Tags]              xiqse_tc_889    aiq_1332    development    sample    xiqse    column_filters    test1

    ${set_result}=  XIQSE Table Set Column Filter  Admin Profile    public_v1_Profile
    Should Be Equal As Integers  ${set_result}      1
    sleep  2 seconds

Test 2: Remove a Single Column Filter
    [Documentation]     Confirms a column filter can be removed (depends on test 1)
    [Tags]              xiqse_tc_889    aiq_1332    development    sample    xiqse    column_filters    test2

    ${remove_result}=  XIQSE Table Remove Column Filter  Admin Profile
    Should Be Equal As Integers  ${remove_result}      1

Test 3: Set a Radio Button Column Filter
    [Documentation]     Confirms a column filter which uses a radio button can be applied
    [Tags]              xiqse_tc_889    aiq_1332    development    sample    xiqse    column_filters    test3

    ${set_result}=  XIQSE Table Set Column Filter  Archived    Yes    filter_type=Radio
    Should Be Equal As Integers  ${set_result}      1
    sleep  2 seconds

    [Teardown]  XIQSE Table Remove Column Filter  Archived

Test 4: Set a Checkbox Column Filter
    [Documentation]     Confirms a column filter which uses a checkbox can be applied
    [Tags]              xiqse_tc_889    aiq_1332    development    sample    xiqse    column_filters    test4

    ${set_result}=  XIQSE Table Set Column Filter  Status    Critical Alarms,Error Alarms    filter_type=Checkbox
    Should Be Equal As Integers  ${set_result}      1
    sleep  2 seconds

    [Teardown]  XIQSE Table Remove Column Filter  Status

Test 5: Set Multiple Column Filters
    [Documentation]     Confirms multiple column filters can be applied
    [Tags]              xiqse_tc_889    aiq_1332    development    sample    xiqse    column_filters    test5

    ${open_result}=  XIQSE Table Open Column Filters Dialog
    Should Be Equal As Integers  ${open_result}      1

    ${add1_result}=  XIQSE Table Add Column Filter  Admin Profile    public_v1_Profile
    Should Be Equal As Integers  ${add1_result}      1

    ${add2_result}=  XIQSE Table Add Column Filter  Archived    No        filter_type=Radio
    Should Be Equal As Integers  ${add2_result}      1

    ${add3_result}=  XIQSE Table Add Column Filter  Status    Device Down,Device Up    filter_type=Checkbox
    Should Be Equal As Integers  ${add3_result}      1

    ${close_result}=  XIQSE Table Close Column Filters Dialog
    Should Be Equal As Integers  ${close_result}      1
    sleep  2 seconds

Test 6: Remove Multiple Column Filters
    [Documentation]     Confirms a column filter can be removed (depends on test 5)
    [Tags]              xiqse_tc_889    aiq_1332    development    sample    xiqse    column_filters    test6

    ${remove_result}=  XIQSE Table Remove Column Filters  Status,Archived,Admin Profile
    Should Be Equal As Integers  ${remove_result}      1


*** Keywords ***
Log In and Set Up Test
    [Documentation]     Logs in and sets up the components for the test

    # Log into XIQSE
    ${login}=  XIQSE Load Page and Log In   ${XIQSE_USER}    ${XIQSE_PASSWORD}    url=${XIQSE_URL}
    Should Be Equal As Integers             ${login}     1

    # Close any banner messages (Connection Lost with XIQ, License Expiration, etc.)
    XIQSE Close Login Banner Messages

    # Close the Help panel if it is open
    XIQSE Close Help Panel

    # We will work with the Devices table
    Navigate to Devices and Confirm Success

Tear Down Test and Close Session
    [Documentation]     Cleans up XIQ and XIQSE test components and closes the browser

    # Reset the table
    ${reset_result}=  XIQSE Reset Table
    Should Be Equal As Integers     ${reset_result}     1

    # Log out of XIQSE
    ${result}=  XIQSE Logout User
    Should Be Equal As Integers     ${result}     1

    # Close the browser
    XIQSE Quit Browser

Navigate to Devices and Confirm Success
    [Documentation]     Navigates to the Network> Devices> Devices view in XIQ-SE and confirms the action was successful

    ${nav_result}=  XIQSE Navigate to Network Devices Tab
    Should Be Equal As Integers         ${nav_result}     1

    ${sel_result}=  XIQSE Devices Select Devices Tab
    Should Be Equal As Integers         ${sel_result}     1
