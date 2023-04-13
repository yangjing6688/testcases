#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : David W. Truesdell
# Description   : Test Suite for testing Connect user licensing using 1 node Simulation
#               : This is qTest test case tccs-13708 in the CSIT project.


*** Settings ***
Resource         ../../Connect_User/Resources/AllResources.robot

Force Tags       testbed_no_node

Suite Setup      Log Into XIQ and Set Up Test
Suite Teardown   Tear Down Test and Close Session


*** Variables ***
${XIQ_URL}                  ${test_url}
${XIQ_USER}                 ${tenant_username}
${XIQ_PASSWORD}             ${tenant_password}

${COPILOT_LICENSE}          None
${PILOT_LICENSE}            None

${COLUMN_1}                 CoPilot
${COLUMN_2}                 Managed
${COLUMN_3}                 Device License


*** Test Cases ***
Test 1: Onboard Device and Verify Success
    [Documentation]     Onboards test device and verifies success
    [Tags]              tccs-13708    connect_release_testing    connect_sanity_testing    aiq-2214    development    xiq    copilot    test1

    ${onboard_result}=       Onboard Device Quick       ${netelem1}
    Should Be Equal As Integers          ${onboard_result}    1

    ${sim_serial}=           set variable       ${${netelem1.name}.serial}
    Set Suite Variable                          ${SIM_SERIAL}    ${sim_serial}

    ${selected}=    Column Picker Select        ${COLUMN_1}     ${COLUMN_2}    ${COLUMN_3}
    Should Be Equal As Integers                 ${selected}     1

    Refresh Devices Page
    Verify and Wait Until Device Online         ${SIM_SERIAL}
    Verify and Wait Until Device Managed        ${SIM_SERIAL}
    Verify Device Status Green                  ${SIM_SERIAL}

Test 2: Verify Device License and CoPilot Column Values
    [Documentation]     Confirms the Device License and CoPilot columns to verify they are set to None
    [Tags]              tccs-13708    connect_release_testing    connect_sanity_testing    aiq-2214    development    xiq    copilot    test2

    Depends On          Test 1

    Navigate to Devices and Confirm Success
    Refresh Devices Page

    # Confirm the device row shows the correct pilot license status
    ${pilot1_result}=      Get Device Details    ${SIM_SERIAL}    DEVICE LICENSE
    Should Contain         ${pilot1_result}      ${PILOT_LICENSE}

    # Confirm the device row shows the correct copilot license status
    ${copilot1_result}=    Get Device Details    ${SIM_SERIAL}    COPILOT
    Should Contain         ${copilot1_result}    ${COPILOT_LICENSE}

Test 3: Delete Device and Verify Success
    [Documentation]     Deletes the device and verifies success
    [Tags]              tccs-13708    connect_release_testing    connect_sanity_testing    aiq-2214    development    xiq    copilot    test3

    Depends On          Test 1

    Delete Test Device and Confirm Success          ${SIM_SERIAL}


*** Keywords ***
Log Into XIQ and Set Up Test
    [Documentation]     Logs into XIQ and sets up the elements necessary to complete this test suite

    # Use this method to convert the ap, wing, netelem to a generic device object
    # ap1       => device1
    # wing1     => device1
    # netelem1  => device1 (EXOS / VOSS)
    convert to generic device object            device  index=1

    Log Into XIQ and Confirm Success            ${XIQ_USER}  ${XIQ_PASSWORD}  ${XIQ_URL}

Tear Down Test and Close Session
    [Documentation]     Cleans up test data, logs out of XIQ, and closes the browser

    Log Out of XIQ and Quit Browser

Verify and Wait Until Device Online
    [Documentation]     Confirms that the device is online in XIQ
    [Arguments]         ${serial}

    ${online}=    Wait Until Device Online          ${serial}
    Should Be Equal As Integers                     ${online}     1

Verify and Wait Until Device Managed
    [Documentation]     Confirms that the device is managed by XIQ
    [Arguments]         ${serial}

    ${managed}=    Wait Until Device Managed        ${serial}
    Should Be Equal As Integers                     ${managed}     1

Verify Device Status Green
    [Documentation]     Confirms that the device status in XIQ
    [Arguments]         ${serial}

    ${status }=    Verify Device Status   device_serial=${serial}    status=green
    Should Be Equal As Integers            ${status}     1

Confirm Required Columns Selected
    [Documentation]     Confirms the Device License and CoPilot columns are selected
    [Arguments]         ${column1}    ${column2}

    ${selected}=    Confirm Column Picker Column Selected     ${COLUMN_1}  ${COLUMN_2}
    Should Be Equal As Integers     ${selected}    1

Delete Test Device and Confirm Success
    [Documentation]     Deletes the specified device and confirms the action was successful
    [Arguments]         ${serial}

    Navigate to Devices and Confirm Success

    Delete Device and Confirm Success  ${serial}
    Confirm Device Serial Not Present  ${serial}

    Navigate to Devices and Confirm Success

Delete Device and Confirm Success
    [Documentation]     Deletes the specified device from XIQ and confirms it was removed successfully
    [Arguments]         ${serial}

    ${del_result}=  Delete Device                     device_serial=${serial}
    Should Be Equal As Integers                       ${del_result}      1
