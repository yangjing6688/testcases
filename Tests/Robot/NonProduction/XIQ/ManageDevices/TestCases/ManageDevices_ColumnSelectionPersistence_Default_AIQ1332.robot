#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Heidi S. White
# Description   : Verifies the column selection persistence functionality works as expected in the Default view
#                 of Manage> Devices.
#                 This is qTest test case TC-7073 in the CSIT project.
#
#                 Note this test used to be generic and based off the VIEW_TYPE variable passed in.
#                 With the switch to AutoIQ, I have converted this into four separate tests so they can
#                 more easily be run and the tags would be more easily manageable;  however, I left
#                 the test code using variables so in the future this could be easily converted back
#                 to one generic test based on the VIEW_TYPE variable.
#
#                 Also note this test assumes two remote windows sessions will be used, as it sets and
#                 utilizes the WINDOWS10 and WINDOWS10_2 variables.

*** Settings ***
Library          Collections

Resource         ../../ManageDevices/Resources/AllResources.robot

Force Tags       testbed_0_node

Suite Teardown   Tear Down Test and Close Session


*** Variables ***
# Defaults
${ENV}                      environment.remote.chrome.windows.xiqse1.yaml
${TOPO}                     topo.test.xiqse1.connected.yaml

${XIQ_URL}                  ${xiq.test_url}
${XIQ_USER}                 ${xiq.tenant_username}
${XIQ_PASSWORD}             ${xiq.tenant_password}

${XIQ_USER_2}               ${xiq2.tenant_username}
${XIQ_PASSWORD_2}           ${xiq2.tenant_password}

${WIN_1}                    ${WINDOWS10}
${WIN_2}                    ${WINDOWS10_2}

${VIEW_TYPE}                Default View

# The following columns are unselected by default
${COLUMN_1}                 Zone
${COLUMN_2}                 Branch ID
# The following columns are selected by default
${COLUMN_3}                 Uptime
${COLUMN_4}                 Connected Clients


*** Test Cases ***
Make Changes to the Column Picker Selections
    [Documentation]     Updates the column picker selections in the Manage> Devices table
    [Tags]              csit_tc_7073   aiq_1332    development    xiq    manage_devices    column_persistence_default    test1

    [Setup]     Log In and Navigate to Devices  ${WIN_1}  ${XIQ_USER}  ${XIQ_PASSWORD}  ${XIQ_URL}

    # Confirm we are starting with expected values
    Confirm Column Selections At Default Values

    # Make changes to column picker selection state
    Column Picker Select    ${COLUMN_1}  ${COLUMN_2}
    Column Picker Unselect  ${COLUMN_3}  ${COLUMN_4}

    # Confirm changes to column selections
    Confirm Column Selections At Updated Values

    [Teardown]    Log Out of XIQ and Quit Browser

Confirm Column Picker Selections Persist For User in New Browser Session
    [Documentation]     Confirms the column picker selections have persisted in a new browser session
    [Tags]              csit_tc_7073   aiq_1332    development    xiq    manage_devices    column_persistence_default    test2

    [Setup]     Log In and Navigate to Devices      ${WIN_1}  ${XIQ_USER}  ${XIQ_PASSWORD}  ${XIQ_URL}

    Confirm Column Selections At Updated Values

    [Teardown]    Log Out of XIQ and Quit Browser

Confirm Column Picker Selections Do Not Apply To Other View Types
    [Documentation]     Confirms the column picker selections only apply to the current view type
    [Tags]              known_issue    csit_tc_7073   aiq_1332    development    xiq    manage_devices    column_persistence_default    test3

    [Setup]     Log In and Navigate to Devices      ${WIN_1}  ${XIQ_USER}  ${XIQ_PASSWORD}  ${XIQ_URL}

    Log to Console  KNOWN ISSUE: XIQ-595

    # Confirm column selections are at defaults for view types other than what is being tested
    Run Keyword If  '${VIEW_TYPE}'.startswith('Default')
    ...  Confirm Non Default View At Default Column Selections

    [Teardown]    Log Out of XIQ and Quit Browser

Confirm Column Picker Selections Persist For Same User on Different PC
    [Documentation]     Confirms the column picker selections have persisted for the same user on a different PC
    [Tags]              csit_tc_7073   aiq_1332    development    xiq    manage_devices    column_persistence_default    test4

    [Setup]     Log In and Navigate to Devices      ${WIN_2}  ${XIQ_USER}  ${XIQ_PASSWORD}  ${XIQ_URL}

    Confirm Column Selections At Updated Values

    [Teardown]    Log Out of XIQ and Quit Browser

Confirm Column Picker Selections Do Not Persist For Different User
    [Documentation]     Confirms the column picker selections made by one user have not persisted for a different user
    [Tags]              csit_tc_7073   aiq_1332    development    xiq    manage_devices    column_persistence_default    test5

    [Setup]     Log In and Navigate to Devices      ${WIN_2}  ${XIQ_USER_2}  ${XIQ_PASSWORD_2}  ${XIQ_URL}

    Confirm Column Selections At Default Values

    [Teardown]    Log Out of XIQ and Quit Browser


*** Keywords ***
Tear Down Test and Close Session
    [Documentation]     Resets the column picker selections and closes the session

    Log In and Navigate to Devices      ${WIN_1}  ${XIQ_USER}  ${XIQ_PASSWORD}  ${XIQ_URL}

    Column Picker Select                ${COLUMN_3}  ${COLUMN_4}
    Column Picker Unselect              ${COLUMN_1}  ${COLUMN_2}

    Log Out of XIQ and Quit Browser

Log In and Navigate to Devices
    [Documentation]     Logs into XIQ on the specified Windows system with incognito mode, navigates to the Manage> Devices view, and selects the view type
    [Arguments]         ${win_ip}  ${user}  ${pwd}  ${url}

    Set Suite Variable  ${WINDOWS10}  ${win_ip}
    Log To Console      Windows 10 is set to ${WINDOWS10}

    Log Into XIQ with Incognito Mode and Confirm Success    ${user}  ${pwd}  ${url}
    Navigate to Devices and Confirm Success

    Select Table View Type and Confirm Success              ${VIEW_TYPE}

Confirm Column Selections At Default Values
    [Documentation]     Confirms the columns are at their default selection values

    ${unselected}=  Confirm Column Picker Column Unselected   ${COLUMN_1}  ${COLUMN_2}
    ${selected}=    Confirm Column Picker Column Selected     ${COLUMN_3}  ${COLUMN_4}
    Should Be Equal As Integers     ${unselected}  1
    Should Be Equal As Integers     ${selected}    1

Confirm Column Selections At Updated Values
    [Documentation]     Confirms the columns are at their default selection values

    ${selected}=    Confirm Column Picker Column Selected       ${COLUMN_1}  ${COLUMN_2}
    ${unselected}=  Confirm Column Picker Column Unselected     ${COLUMN_3}  ${COLUMN_4}
    Should Be Equal As Integers     ${unselected}  1
    Should Be Equal As Integers     ${selected}    1

Confirm Non Default View At Default Column Selections
    Select Table View Type and Confirm Success      Wireless View
    Confirm Column Selections At Default Values
    Select Table View Type and Confirm Success      LAN View
    Confirm Column Selections At Default Values
    Select Table View Type and Confirm Success      WAN View
    Confirm Column Selections At Default Values
