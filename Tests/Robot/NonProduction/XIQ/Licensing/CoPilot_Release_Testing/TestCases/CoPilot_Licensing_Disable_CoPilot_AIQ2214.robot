#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : David W. Truesdell
# Description   : Test Suite for testing CoPilot licensing
#               : This is qTest test case TCCS-13494 in the CSIT project.


*** Settings ***
Resource         ../../CoPilot_Release_Testing/Resources/AllResources.robot

Force Tags       testbed_2_node

Suite Setup      Log Into XIQ and Set Up Test
Suite Teardown   Tear Down Test and Close Session


*** Variables ***
${XIQ_URL}                  ${test_url}
${XIQ_USER}                 ${tenant_username}
${XIQ_PASSWORD}             ${tenant_password}
${IQAGENT}                  ${sw_connection_host}

${DUT1_SERIAL}              ${netelem1.serial}
${DUT1_MAKE}                ${netelem1.make}
${DUT1_MAC}                 ${netelem1.mac}
${DUT1_CLI_TYPE}            ${netelem1.cli_type}
${DUT1_IP}                  ${netelem1.ip}
${DUT1_PORT}                ${netelem1.port}
${DUT1_USERNAME}            ${netelem1.username}
${DUT1_PASSWORD}            ${netelem1.password}
${DUT1_VR}                  ${netelem1.vr}

${DUT2_SERIAL}              ${netelem2.serial}
${DUT2_MAKE}                ${netelem2.make}
${DUT2_MAC}                 ${netelem2.mac}
${DUT2_CLI_TYPE}            ${netelem2.cli_type}
${DUT2_IP}                  ${netelem2.ip}
${DUT2_PORT}                ${netelem2.port}
${DUT2_USERNAME}            ${netelem2.username}
${DUT2_PASSWORD}            ${netelem2.password}
${DUT2_VR}                  ${netelem2.vr}

${PILOT_ENTITLEMENT}        XIQ-PIL-S-C
${COPILOT_ENTITLEMENT}      XIQ-COPILOT-S-C
${COPILOT_ACTIVE}           Active
${COPILOT_NONE}             None
${PILOT_LICENSE}            Pilot

${COLUMN_1}                 CoPilot
${COLUMN_2}                 Managed
${COLUMN_3}                 Device License

${LOCATION}                 San Jose, building_01, floor_02


*** Test Cases ***
Test 1: Verify Pilot and CoPilot Baseline License Counts
    [Documentation]     Confirms license counts are at expected values in XIQ to begin with (nothing consumed)
    [Tags]              tccs-13494    copilot_release_testing    copilot_license_testing    aiq-2214    development    xiq    copilot    test1

    Confirm Entitlement Counts for Feature Matches Expected     ${PILOT_ENTITLEMENT}       3    0    3
    Confirm Entitlement Counts for Feature Matches Expected     ${COPILOT_ENTITLEMENT}     2    0    2

Test 2: Onboard First Device and Verify Success
    [Documentation]     Onboards first test device and verifies success
    [Tags]              tccs-13494    copilot_release_testing    copilot_license_testing    aiq-2214    development    xiq    copilot    test2

    Depends On Test     Test 1: Verify Pilot and CoPilot Baseline License Counts

    # Downgrade the device's iqagent if needed
    ${SPAWN_CONNECTION}=      Open Spawn        ${DUT1_IP}   ${DUT1_PORT}   ${DUT1_USERNAME}   ${DUT1_PASSWORD}   ${DUT1_CLI_TYPE}
    ${DOWNGRADE_IQAGENT}=     Downgrade Iqagent              ${DUT1_CLI_TYPE}         ${SPAWN_CONNECTION}
    Should Be Equal As Integers      ${DOWNGRADE_IQAGENT}     1

    ${CONF_STATUS_RESULT}=    Configure Device To Connect To Cloud        ${DUT1_CLI_TYPE}    ${IQAGENT}   ${SPAWN_CONNECTION}    vr=${DUT1_VR}
    Should Be Equal As Strings       ${CONF_STATUS_RESULT}    1
    Close Spawn         ${SPAWN_CONNECTION}

    Onboard New Test Device                     ${DUT1_SERIAL}  ${netelem1}

    ${selected}=    Column Picker Select        ${COLUMN_1}     ${COLUMN_2}    ${COLUMN_3}
    Should Be Equal As Integers                 ${selected}     1

    Refresh Devices Page
    Verify and Wait Until Device Online         ${DUT1_SERIAL}
    Verify and Wait Until Device Managed        ${DUT1_SERIAL}
    Verify Device Status Green                  ${DUT1_SERIAL}

Test 3: Onboard Second Test Device and Verify Success
    [Documentation]     Onboards a second test device and verifies success
    [Tags]              tccs-13494    copilot_release_testing    copilot_license_testing    aiq-2214    development    xiq    copilot    test3

    Depends On Test     Test 1: Verify Pilot and CoPilot Baseline License Counts

    # Downgrade the device's iqagent if needed
    ${SPAWN_CONNECTION}=      Open Spawn        ${DUT2_IP}   ${DUT2_PORT}   ${DUT2_USERNAME}   ${DUT2_PASSWORD}   ${DUT2_CLI_TYPE}
    ${DOWNGRADE_IQAGENT}=     Downgrade Iqagent              ${DUT2_CLI_TYPE}         ${SPAWN_CONNECTION}
    Should Be Equal As Integers      ${DOWNGRADE_IQAGENT}     1

    ${CONF_STATUS_RESULT}=    Configure Device To Connect To Cloud        ${DUT2_CLI_TYPE}    ${IQAGENT}   ${SPAWN_CONNECTION}    vr=${DUT2_VR}
    Should Be Equal As Strings       ${CONF_STATUS_RESULT}    1
    Close Spawn         ${SPAWN_CONNECTION}

    Onboard New Test Device                     ${DUT2_SERIAL}  ${netelem2}

    Refresh Devices Page
    Verify and Wait Until Device Online         ${DUT2_SERIAL}
    Verify and Wait Until Device Managed        ${DUT2_SERIAL}
    Verify Device Status Green                  ${DUT2_SERIAL}

Test 4: Verify Devices Consumed Pilot and CoPilot License Within Global Settings License Management
    [Documentation]     Confirms the license counts for Pilot and CoPilot within Global Settings->License Management
    [Tags]              tccs-13494    copilot_release_testing    copilot_license_testing    aiq-2214    development    xiq    copilot    test4

    Depends On Test     Test 1: Verify Pilot and CoPilot Baseline License Counts

    Confirm Entitlement Counts for Feature Matches Expected     ${PILOT_ENTITLEMENT}       1    2    3
    Confirm Entitlement Counts for Feature Matches Expected     ${COPILOT_ENTITLEMENT}     0    2    2

Test 5: Verify Device License and CoPilot Column Values On All Devices
    [Documentation]     Confirms the Device License and CoPilot column values to verify device consumed the appropriate license or not
    [Tags]              tccs-13494    copilot_release_testing    copilot_license_testing    aiq-2214    development    xiq    copilot    test5

    Depends On Test     Test 1: Verify Pilot and CoPilot Baseline License Counts

    # Confirm the device row shows the correct pilot license status
    ${pilot1_result}=      Get Device Details    ${DUT1_SERIAL}    DEVICE LICENSE
    Should Contain         ${pilot1_result}      ${PILOT_LICENSE}

    # Confirm the device row shows the correct copilot license status
    ${copilot1_result}=    Get Device Details    ${DUT1_SERIAL}    COPILOT
    Should Contain         ${copilot1_result}    ${COPILOT_ACTIVE}

    # Confirm the device row shows the correct pilot license status
    ${pilot2_result}=      Get Device Details    ${DUT2_SERIAL}    DEVICE LICENSE
    Should Contain         ${pilot2_result}      ${PILOT_LICENSE}

    # Confirm the device row shows the correct copilot license status
    ${copilot2_result}=    Get Device Details    ${DUT2_SERIAL}    COPILOT
    Should Contain         ${copilot2_result}    ${COPILOT_ACTIVE}

Test 6: Diable CoPilot Feature and Verify Success
    [Documentation]     Disables CoPilot feature in Global Settings -> VIQ Management and verifies success
    [Tags]              tccs-13494    copilot_release_testing    copilot_license_testing    aiq-2214    development    xiq    copilot    test6
    
    Depends On Test     Test 1: Verify Pilot and CoPilot Baseline License Counts
    
    Disable CoPilot Feature and Confirm Success

Test 7: Verify Device CoPilot License Revoked Within Global Settings License Management
    [Documentation]     Confirms the license count for CoPilot within Global Settings->License Management
    [Tags]              tccs-13493    copilot_release_testing    copilot_license_testing    aiq-2214    development    xiq    copilot    test7

    Depends On Test     Test 1: Verify Pilot and CoPilot Baseline License Counts
    
    Confirm Entitlement Counts for Feature Matches Expected     ${COPILOT_ENTITLEMENT}     2    0    2

Test 8: Verify Device CoPilot Column Values On All Devices
    [Documentation]     Confirms the CoPilot column for device to verify copilot license is revoked
    [Tags]              tccs-13494    copilot_release_testing    copilot_license_testing    aiq-2214    development    xiq    copilot    test8

    Depends On Test     Test 1: Verify Pilot and CoPilot Baseline License Counts

    # Confirm the device row shows the correct copilot license status
    ${copilot1_result}=    Get Device Details    ${DUT1_SERIAL}    COPILOT
    Should Contain         ${copilot1_result}    ${COPILOT_NONE}

    ${copilot2_result}=    Get Device Details    ${DUT2_SERIAL}    COPILOT
    Should Contain         ${copilot2_result}    ${COPILOT_NONE}

Test 9: Enable CoPilot Feature and Verify Success
    [Documentation]     Enables CoPilot feature in Global Settings -> VIQ Management and verifies success
    [Tags]              tccs-13494    copilot_release_testing    copilot_license_testing    aiq-2214    development    xiq    copilot    test9

    Depends On Test     Test 1: Verify Pilot and CoPilot Baseline License Counts

    Enable CoPilot Feature and Confirm Success

Test 10: Verify Devices CoPilot License Consumed Within Global Settings License Management
    [Documentation]     Confirms the license count for CoPilot within Global Settings->License Management
    [Tags]              tccs-13494    copilot_release_testing    copilot_license_testing    aiq-2214    development    xiq    copilot    test10

    Depends On Test     Test 1: Verify Pilot and CoPilot Baseline License Counts

    Confirm Entitlement Counts for Feature Matches Expected     ${COPILOT_ENTITLEMENT}     0    2    2

Test 11: Verify CoPilot Column Values On All Devices
    [Documentation]     Confirms the CoPilot column for device to verify device copilot license is consumed again
    [Tags]              tccs-13494    copilot_release_testing    copilot_license_testing    aiq-2214    development    xiq    copilot    test11

    Depends On Test     Test 1: Verify Pilot and CoPilot Baseline License Counts

    # Confirm the device row shows the correct copilot license status
    ${copilot1_result}=    Get Device Details    ${DUT1_SERIAL}    COPILOT
    Should Contain         ${copilot1_result}    ${COPILOT_ACTIVE}

    ${copilot2_result}=    Get Device Details    ${DUT2_SERIAL}    COPILOT
    Should Contain         ${copilot2_result}    ${COPILOT_ACTIVE}

Test 12: Delete Second Test Device and Verify Success
    [Documentation]     Deletes the second test device and verifies success
    [Tags]              tccs-13494    copilot_release_testing    copilot_license_testing    aiq-2214    development    xiq    copilot    test12

    Depends On Test     Test 1: Verify Pilot and CoPilot Baseline License Counts

    Delete Test Device and Confirm Success          ${DUT2_SERIAL}

Test 13: Delete First Test Device and Verify Success
    [Documentation]     Deletes a test device and verifies success
    [Tags]              tccs-13494    copilot_release_testing    copilot_license_testing    aiq-2214    development    xiq    copilot    test13

    Depends On Test     Test 1: Verify Pilot and CoPilot Baseline License Counts

    Delete Test Device and Confirm Success          ${DUT1_SERIAL}

Test 14: Verify Pilot and CoPilot Licenses Revoked Within Global Settings License Management
    [Documentation]     Confirms the license counts for Pilot and CoPilot within Global Settings->License Management
    [Tags]              tccs-13494    copilot_release_testing    copilot_license_testing    aiq-2214    development    xiq    copilot    test14

    Depends On Test     Test 1: Verify Pilot and CoPilot Baseline License Counts

    Confirm Entitlement Counts for Feature Matches Expected     ${PILOT_ENTITLEMENT}       3    0    3
    Confirm Entitlement Counts for Feature Matches Expected     ${COPILOT_ENTITLEMENT}     2    0    2


*** Keywords ***
Log Into XIQ and Set Up Test
    [Documentation]     Logs into XIQ and sets up the elements necessary to complete this test suite

    # Use this method to convert the ap, wing, netelem to a generic device object
    # ap1       => device1
    # wing1     => device1
    # netelem1  => device1 (EXOS / VOSS)
    convert to generic device object            device  index=1

    Log Into XIQ and Confirm Success            ${XIQ_USER}  ${XIQ_PASSWORD}  ${XIQ_URL}
    Enable CoPilot Feature and Confirm Success

Tear Down Test and Close Session
    [Documentation]     Cleans up test data, logs out of XIQ, and closes the browser

    Navigate to Devices and Confirm Success
    ${del_result}=  Delete All Devices
    Should Be Equal As Integers  ${del_result}  1

    Disable CoPilot Feature and Confirm Success
    Log Out of XIQ and Quit Browser

Enable CoPilot Feature and Confirm Success
    [Documentation]     Enables CoPilot feature in Global Settings -> VIQ Management and verifies success

    ${result_enable}=    Enable CoPilot Feature For This VIQ
    Should Be Equal As Integers     ${result_enable}     1

Disable CoPilot Feature and Confirm Success
    [Documentation]     Disables CoPilot feature in Global Settings -> VIQ Management and verifies success

    ${result_disable}=    Disable CoPilot Feature For This VIQ
    Should Be Equal As Integers     ${result_disable}     1

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
    [Arguments]         ${ip}

    ${del_result}=  Delete Device                     ${ip}
    Should Be Equal As Integers                       ${del_result}      1
