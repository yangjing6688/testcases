#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : David W. Truesdell
# Description   : Test Suite for testing CoPilot License Filtering - Set Filter and Onboard Device
#               : This is qTest test case TCCS-15103 in the CSIT project.


*** Settings ***
Resource         ../../CoPilot_Release_Testing/Resources/AllResources.robot

Force Tags       testbed_3_node

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
    [Tags]              tccs-15103    copilot_release_testing    copilot_license_testing    xiq-16250    development    xiq    copilot    test1

    Confirm Entitlement Counts for Feature Matches Expected     ${PILOT_ENTITLEMENT}       3    0    3
    Confirm Entitlement Counts for Feature Matches Expected     ${COPILOT_ENTITLEMENT}     2    0    2

Test 2: Set Filter to CoPilot None
    [Documentation]     Filters by the CoPilot License 'CoPilot None' to show devices that have a None CoPilot license
    [Tags]              tccs-15103    copilot_release_testing    copilot_license_testing    xiq-16250    development    xiq    copilot    test2

    Depends On Test     Test 1: Verify Pilot and CoPilot Baseline License Counts

    Clear All Filters
    Set Filter For CoPilot License None

Test 3: Onboard Device
    [Documentation]     Onboards test device
    [Tags]              tccs-15103    copilot_release_testing    copilot_license_testing    xiq-16250    development    xiq    copilot    test3

    Depends On Test     Test 1: Verify Pilot and CoPilot Baseline License Counts

    # Downgrade the device's iqagent if needed
    ${SPAWN_CONNECTION}=      Open Spawn        ${DUT1_IP}   ${DUT1_PORT}   ${DUT1_USERNAME}   ${DUT1_PASSWORD}   ${DUT1_CLI_TYPE}
    ${DOWNGRADE_IQAGENT}=     Downgrade Iqagent              ${DUT1_CLI_TYPE}         ${SPAWN_CONNECTION}
    Should Be Equal As Integers      ${DOWNGRADE_IQAGENT}     1

    ${CONF_STATUS_RESULT}=    Configure Device To Connect To Cloud        ${DUT1_CLI_TYPE}    ${IQAGENT}   ${SPAWN_CONNECTION}    vr=${DUT1_VR}
    Should Be Equal As Strings       ${CONF_STATUS_RESULT}    1
    Close Spawn         ${SPAWN_CONNECTION}

    ${selected}=    Column Picker Select        ${COLUMN_1}     ${COLUMN_2}    ${COLUMN_3}
    Should Be Equal As Integers                 ${selected}     1

    Onboard New Test Device                     ${DUT1_SERIAL}  ${netelem1}

Test 4: Verify Device Is Present In CoPilot None Filterered Devices Panel
    [Documentation]     Verifies device is present in Devices panel when filtering on "CoPilot None"
    [Tags]              tccs-15103    copilot_release_testing    copilot_license_testing    xiq-16250    development    xiq    copilot    test4

    Confirm Device Serial Present in Filtered Devices Panel             ${DUT1_SERIAL}

    #Verify COPILOT column value of None
    ${copilot1_result}=    Get Device Details    ${DUT1_SERIAL}    COPILOT
    Should Contain         ${copilot1_result}    ${COPILOT_NONE}

Test 5: Verify Device Consumes Pilot and CoPilot License Within Global Settings License Management
    [Documentation]     Confirms the license counts for Pilot and CoPilot within Global Settings->License Management
    [Tags]              tccs-15103    copilot_sanity_testing    copilot_license_testing    xiq-16250    development    xiq    copilot    test5

    Depends On Test     Test 1: Verify Pilot and CoPilot Baseline License Counts

    Confirm Entitlement Counts for Feature Matches Expected     ${PILOT_ENTITLEMENT}       2    1    3
    Confirm Entitlement Counts for Feature Matches Expected     ${COPILOT_ENTITLEMENT}     1    1    2

Test 6: Verify Device Is Removed From Filtered Devices Panel Once It Activates a CoPilot License
    [Documentation]     Verify once device changes from CoPilot None to CoPilot Active it is removed from Devices panel where it's filtering on CoPilot None
    [Tags]              tccs-15103    copilot_release_testing    copilot_license_testing    xiq-16250    development    xiq    copilot    test6

    Depends On Test     Test 1: Verify Pilot and CoPilot Baseline License Counts

    Navigate to Devices and Confirm Success
    Confirm Device Serial Not Present in Filtered Devices Panel             ${DUT1_SERIAL}

Test 7: Filter For CoPilot License Active and Verify Device Present In Devices panel
    [Documentation]     Filters by the CoPilot License 'CoPilot Active' to show device(s) that have an Active CoPilot license
    [Tags]              tccs-15103    copilot_release_testing    copilot_license_testing    xiq-16250    development    xiq    copilot    test7

    Depends On Test     Test 1: Verify Pilot and CoPilot Baseline License Counts

    Set Filter For CoPilot License Active
    Confirm Device Serial Present in Filtered Devices Panel             ${DUT1_SERIAL}

Test 8: Verify Device CoPilot Column Value Of Active
    [Documentation]     Confirms the CoPilot column value is Active
    [Tags]              tccs-15103    copilot_release_testing    copilot_license_testing    xiq-16250    development    xiq    copilot    test8

    Depends On Test     Test 1: Verify Pilot and CoPilot Baseline License Counts

    ${copilot1_result}=    Get Device Details    ${DUT1_SERIAL}    COPILOT
    Should Contain         ${copilot1_result}    ${COPILOT_ACTIVE}

Test 9: Delete Device and Verify Success
    [Documentation]     Deletes all devices and verifies success
    [Tags]              tccs-15103    copilot_sanity_testing    copilot_license_testing    xiq-16250    development    xiq    copilot    test9

    Depends On Test     Test 1: Verify Pilot and CoPilot Baseline License Counts

    Delete Test Device and Confirm Success          ${DUT1_SERIAL}

Test 10: Verify First Device's Pilot and CoPilot Licenses Revoked Within Global Settings License Management
    [Documentation]     Confirms the license counts for Pilot and CoPilot within Global Settings->License Management
    [Tags]              tccs-15103    copilot_release_testing    copilot_license_testing    xiq-16250    development    xiq    copilot    test10

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

    Clear All Filters
    Delete All devices and Confirm Success
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

Delete All Devices and Confirm Success
    [Documentation]     Deletes the specified device and confirms the action was successful

    Navigate to Devices and Confirm Success

    ${del_result}=  Delete All Devices
    Should Be Equal As Integers  ${del_result}  1

Set Filter For CoPilot License Active
    [Documentation]     Filters by the CoPilot License group

    Clear All Filters
    ${filter_result}=  Set CoPilot License Filter    CoPilot Active    true
    Should Be Equal As Integers                      ${filter_result}  1
    Apply Filters

Set Filter For CoPilot License None
    [Documentation]     Filters by the CoPilot License group

    Clear All Filters
    ${filter_result}=  Set CoPilot License Filter    CoPilot None    true
    Should Be Equal As Integers                      ${filter_result}  1
    Apply Filters

Confirm Device Serial Present in Filtered Devices Panel
    [Documentation]     Confirms the specified device by SERIAL NUMBER is present in Devices panel filtered list
    [Arguments]         ${serial}

    Refresh Devices Page

    ${search_result}=  Search Device        device_serial=${serial}
    Should Be Equal As Integers             ${search_result}    1

Confirm Device Serial Not Present In Filtered Devices Panel
    [Documentation]     Confirms the specified device by SERIAL NUMBER is not present in Devices panel filtered list
    [Arguments]         ${serial}

    Refresh Devices Page

    ${search_result}=  Search Device        device_serial=${serial}      expect_error=True
    Should Be Equal As Integers             ${search_result}    -1
