#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : David W. Truesdell
# Description   : Test Suite for testing Navigator licensing using 3 nodes
#               : This is qTest test case TCCS-13550 in the CSIT project.


*** Settings ***
Resource         ../../Pilot_Navigator/Resources/AllResources.robot

Force Tags       testbed_3_node

Suite Setup      Log Into XIQ and Set Up Test
Suite Teardown   Tear Down Test and Close Session


*** Variables ***
${XIQ_URL}                   ${test_url}
${XIQ_USER}                  ${tenant_username}
${XIQ_PASSWORD}              ${tenant_password}
${IQAGENT}                   ${wing_sw_connection_host}

${DUT1_SERIAL}               ${netelem1.serial}
${DUT1_MAKE}                 ${netelem1.make}
${DUT1_MAC}                  ${netelem1.mac}
${DUT1_CLI_TYPE}             ${netelem1.cli_type}
${DUT1_MAKE}                 ${netelem1.make}
${DUT1_MAC}                  ${netelem1.mac}
${DUT1_IP}                   ${netelem1.ip}
${DUT1_PORT}                 ${netelem1.port}
${DUT1_USERNAME}             ${netelem1.username}
${DUT1_PASSWORD}             ${netelem1.password}
${DUT1_VR}                   ${netelem1.vr}

${DUT2_SERIAL}               ${netelem2.serial}
${DUT2_MAKE}                 ${netelem2.make}
${DUT2_MAC}                  ${netelem2.mac}
${DUT2_CLI_TYPE}             ${netelem2.cli_type}
${DUT2_MAKE}                 ${netelem2.make}
${DUT2_MAC}                  ${netelem2.mac}
${DUT2_IP}                   ${netelem2.ip}
${DUT2_PORT}                 ${netelem2.port}
${DUT2_USERNAME}             ${netelem2.username}
${DUT2_PASSWORD}             ${netelem2.password}
${DUT2_VR}                   ${netelem2.vr}

${DUT3_SERIAL}               ${netelem3.serial}
${DUT3_MAKE}                 ${netelem3.make}
${DUT3_MAC}                  ${netelem3.mac}
${DUT3_CLI_TYPE}             ${netelem3.cli_type}
${DUT3_MAKE}                 ${netelem3.make}
${DUT3_MAC}                  ${netelem3.mac}
${DUT3_IP}                   ${netelem3.ip}
${DUT3_PORT}                 ${netelem3.port}
${DUT_3USERNAME}             ${netelem3.username}
${DUT3_PASSWORD}             ${netelem3.password}
${DUT_3VR}                   ${netelem3.vr}

${NAV_ENTITLEMENT}           XIQ-NAV-S-C
${NAV_LICENSE}               Navigator
${PILOT_ENTITLEMENT}         XIQ-PIL-S-C
${PILOT_LICENSE}             Pilot

${COLUMN_1}                  Managed
${COLUMN_2}                  Device License

${LOCATION}                  San Jose, building_01, floor_02


*** Test Cases ***
Test 1: Verify Navigator and Pilot Baseline License Counts
    [Documentation]     Confirms Pilot and Navigator license counts are at expected value in XIQ to begin with (nothing consumed)
    [Tags]              tccs-13550    navigator_release_testing    navigator_license_testing    aiq-2214    development    xiq    navigator    test1

    Confirm Entitlement Counts for Feature Matches Expected     ${NAV_ENTITLEMENT}       2    0    2
    Confirm Entitlement Counts for Feature Matches Expected     ${PILOT_ENTITLEMENT}     3    0    3

Test 2: Onboard First Device and Verify Success
    [Documentation]     Onboards first test device and verifies success
    [Tags]              tccs-13550    navigator_release_testing    navigator_license_testing    aiq-2214    development    xiq    navigator    test2

    Depends On          Test 1

    # Downgrade the device's iqagent if needed
    ${SPAWN_CONNECTION}=      Open Spawn        ${DUT1_IP}   ${DUT1_PORT}   ${DUT1_USERNAME}   ${DUT1_PASSWORD}   ${DUT1_CLI_TYPE}
    ${DOWNGRADE_IQAGENT}=     Downgrade Iqagent              ${DUT1_CLI_TYPE}        ${SPAWN_CONNECTION}
    Should Be Equal As Integers      ${DOWNGRADE_IQAGENT}     1

    ${CONF_STATUS_RESULT}=    Configure Device To Connect To Cloud        ${DUT1_CLI_TYPE}    ${IQAGENT}   ${SPAWN_CONNECTION}    vr=${DUT1_VR}
    Should Be Equal As Strings       ${CONF_STATUS_RESULT}    1
    Close Spawn         ${SPAWN_CONNECTION}

    Onboard New Test Device                     ${DUT1_SERIAL}  ${netelem1}

    ${selected}=    Column Picker Select        ${COLUMN_1}     ${COLUMN_2}
    Should Be Equal As Integers                 ${selected}     1

    Refresh Devices Page
    Verify and Wait Until Device Online         ${DUT1_SERIAL}
    Verify and Wait Until Device Managed        ${DUT1_SERIAL}
    Verify Device Status Green                  ${DUT1_SERIAL}

Test 3: Verify First Device Consumes Navigator License Within Global Settings License Management
    [Documentation]     Confirms the license count for Navigator and Pilot within Global Settings->License Management
    [Tags]              tccs-13550    navigator_release_testing    navigator_license_testing    aiq-2214    development    xiq    navigator    test3

    Depends On          Test 1

    Confirm Entitlement Counts for Feature Matches Expected     ${NAV_ENTITLEMENT}       1    1    2
    Confirm Entitlement Counts for Feature Matches Expected     ${PILOT_ENTITLEMENT}     3    0    3

Test 4: Onboard Second Device and Verify Success
    [Documentation]     Onboards second test device and verifies success
    [Tags]              tccs-13550    navigator_release_testing    navigator_license_testing    aiq-2214    development    xiq    navigator    test4

    Depends On          Test 1

    # Downgrade the device's iqagent if needed
    ${SPAWN_CONNECTION}=      Open Spawn        ${DUT2_IP}   ${DUT2_PORT}   ${DUT2_USERNAME}   ${DUT2_PASSWORD}   ${DUT2_CLI_TYPE}
    ${DOWNGRADE_IQAGENT}=     Downgrade Iqagent              ${DUT2_CLI_TYPE}        ${SPAWN_CONNECTION}
    Should Be Equal As Integers      ${DOWNGRADE_IQAGENT}     1

    ${CONF_STATUS_RESULT}=    Configure Device To Connect To Cloud        ${DUT2_CLI_TYPE}    ${IQAGENT}   ${SPAWN_CONNECTION}    vr=${DUT2_VR}
    Should Be Equal As Strings       ${CONF_STATUS_RESULT}    1
    Close Spawn         ${SPAWN_CONNECTION}

    Onboard New Test Device                     ${DUT2_SERIAL}  ${netelem2}

    ${selected}=    Column Picker Select        ${COLUMN_1}     ${COLUMN_2}
    Should Be Equal As Integers                 ${selected}     1

    Refresh Devices Page
    Verify and Wait Until Device Online         ${DUT2_SERIAL}
    Verify and Wait Until Device Managed        ${DUT2_SERIAL}
    Verify Device Status Green                  ${DUT2_SERIAL}

Test 5: Verify Second Device Consumes Navigator License Within Global Settings License Management
    [Documentation]     Confirms the license count for Navigator and Pilot within Global Settings->License Management
    [Tags]              tccs-13550    navigator_release_testing    navigator_license_testing    aiq-2214    development    xiq    navigator    test5

    Depends On          Test 1

    Confirm Entitlement Counts for Feature Matches Expected     ${NAV_ENTITLEMENT}       0    2    2
    Confirm Entitlement Counts for Feature Matches Expected     ${PILOT_ENTITLEMENT}     3    0    3

Test 6: Verify Device License Column Value
    [Documentation]     Checks the Device License column to verify devices consumed the appropriate license or not
    [Tags]              tccs-13550    navigator_release_testing    navigator_license_testing    aiq-2214    development    xiq    navigator    test6

    Depends On          Test 1

    # Confirm the device row shows the correct navigator license status
    ${nav1_result}=      Get Device Details    ${DUT1_SERIAL}    DEVICE LICENSE
    Should Contain         ${nav1_result}      ${NAV_LICENSE}

    ${nav2_result}=      Get Device Details    ${DUT2_SERIAL}    DEVICE LICENSE
    Should Contain         ${nav2_result}      ${NAV_LICENSE}

Test 7: Onboard Third Test Device and Verify Device Consumes Pilot License Since Navigator Licenses Exceeded
    [Documentation]     Onboard a third test device and verifies it was onboarded but consumed pilot license due to navigator license limit exceeded
    [Tags]              tccs-13492    navigator_release_testing    navigator_license_testing    aiq-2214    development    xiq    pilot    test7

    Depends On          Test 1

    # Downgrade the device's iqagent if needed
    ${SPAWN_CONNECTION}=      Open Spawn        ${DUT3_IP}   ${DUT3_PORT}   ${DUT3_USERNAME}   ${DUT3_PASSWORD}   ${DUT3_CLI_TYPE}
    ${DOWNGRADE_IQAGENT}=     Downgrade Iqagent              ${DUT3_CLI_TYPE}         ${SPAWN_CONNECTION}
    Should Be Equal As Integers      ${DOWNGRADE_IQAGENT}     1

    ${CONF_STATUS_RESULT}=    Configure Device To Connect To Cloud        ${DUT3_CLI_TYPE}    ${IQAGENT}   ${SPAWN_CONNECTION}    vr=${DUT3_VR}
    Should Be Equal As Strings       ${CONF_STATUS_RESULT}    1
    Close Spawn         ${SPAWN_CONNECTION}

    Onboard New Test Device                     ${DUT3_SERIAL}  ${netelem3}

    Refresh Devices Page
    Verify and Wait Until Device Online         ${DUT3_SERIAL}
    Verify and Wait Until Device Managed        ${DUT3_SERIAL}
    Verify Device Status Green                  ${DUT3_SERIAL}

Test 8: Verify Third Device Consumes Pilot License Within Global Settings License Management
    [Documentation]     Confirms the license count for Navigator and Pilot within Global Settings->License Management
    [Tags]              tccs-13550    navigator_release_testing    navigator_license_testing    aiq-2214    development    xiq    navigator    test8

    Depends On          Test 1

    Confirm Entitlement Counts for Feature Matches Expected     ${NAV_ENTITLEMENT}       0    2    2
    Confirm Entitlement Counts for Feature Matches Expected     ${PILOT_ENTITLEMENT}     2    1    3

Test 9: Verify Device License Column Value
    [Documentation]     Checks the Device License column to verify devices consumed the appropriate license or not
    [Tags]              tccs-13550    navigator_release_testing    navigator_license_testing    aiq-2214    development    xiq    navigator    test9

    Depends On          Test 1

    # Confirm the device row shows the correct navigator license status
    ${nav1_result}=      Get Device Details    ${DUT1_SERIAL}    DEVICE LICENSE
    Should Contain         ${nav1_result}      ${NAV_LICENSE}

    ${nav2_result}=      Get Device Details    ${DUT2_SERIAL}    DEVICE LICENSE
    Should Contain         ${nav2_result}      ${NAV_LICENSE}

    ${nav3_result}=      Get Device Details    ${DUT3_SERIAL}    DEVICE LICENSE
    Should Contain         ${nav3_result}      ${PILOT_LICENSE}

Test 10: Delete All Devices and Verify Success
    [Documentation]     Deletes all devices and verifies success
    [Tags]              tccs-13550    navigator_release_testing    navigator_license_testing    aiq-2214    development    xiq    navigator    test10

    Depends On          Test 1

    Delete All devices and Confirm Success

Test 11: Verify Navigator License Revoked Within Global Settings License Management
    [Documentation]     Confirms the Navigator and Pilot licenses was revoked
    [Tags]              tccs-13550    navigator_release_testing    navigator_license_testing    aiq-2214    development    xiq    navigator    test11

    Depends On          Test 1

    Confirm Entitlement Counts for Feature Matches Expected     ${NAV_ENTITLEMENT}        2    0    2
    Confirm Entitlement Counts for Feature Matches Expected     ${PILOT_ENTITLEMENT}      3    0    3


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

    Navigate to Devices and Confirm Success
    ${del_result}=  Delete All Devices
    Should Be Equal As Integers  ${del_result}  1

    Log Out of XIQ and Quit Browser

Onboard New Test Device
    [Documentation]     Onboards the specified test device, deleting it first if it already exists
    [Arguments]         ${serial}  ${netelem}

    Navigate to Devices and Confirm Success

    # If the device has already been onboarded, delete it first
    Delete Device and Confirm Success  ${serial}
    Confirm Device Serial Not Present  ${serial}

    # Onboard the device
    onboard device quick    ${netelem}
    sleep   ${DEVICE_ONBOARDING_WAIT}
    Confirm Device Serial Present  ${serial}


    Verify and Wait Until Device Online         ${serial}
    Verify and Wait Until Device Managed        ${serial}

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
    [Documentation]     Confirms the Device License and Managed columns are selected
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
    [Arguments]         ${ip}

    ${del_result}=  Delete Device                     ${ip}
    Should Be Equal As Integers                       ${del_result}      1

Delete All Devices and Confirm Success
    [Documentation]     Deletes the specified device and confirms the action was successful

    Navigate to Devices and Confirm Success

    ${del_result}=  Delete All Devices
    Should Be Equal As Integers  ${del_result}  1
