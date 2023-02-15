#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : David W. Truesdell
# Description   : Test Suite for testing CoPilot licensing using 1 node VOSS
#               : This is qTest test case tcxm-20887 in the CSIT project.


*** Settings ***
Resource         ../../CoPilot_Sanity_Testing/Resources/AllResources.robot

Force Tags       testbed_1_node

Suite Setup      Log Into XIQ and Set Up Test
Suite Teardown   Tear Down Test and Close Session


*** Variables ***
${XIQ_URL}                  ${test_url}
${XIQ_USER}                 ${tenant_username}
${XIQ_PASSWORD}             ${tenant_password}
${IQAGENT}                  ${sw_connection_host}

${DUT_SERIAL}               ${netelem1.serial}
${DUT_MAKE}                 ${netelem1.make}
${DUT_MAC}                  ${netelem1.mac}
${DUT_CLI_TYPE}             ${netelem1.cli_type}
${DUT_IP}                   ${netelem1.ip}
${DUT_PORT}                 ${netelem1.port}
${DUT_USERNAME}             ${netelem1.username}
${DUT_PASSWORD}             ${netelem1.password}
${DUT_VR}                   ${netelem1.vr}

${PILOT_ENTITLEMENT}        XIQ-PIL-S-C
${COPILOT_ENTITLEMENT}      XIQ-COPILOT-S-C
${COPILOT_ACTIVE}           Active
${COPILOT_NONE}             None
${PILOT_LICENSE}            Pilot
${NO_PILOT_LICENSE}         Not Required

${COLUMN_1}                 CoPilot
${COLUMN_2}                 Managed
${COLUMN_3}                 Device License


*** Test Cases ***
Test 1: Verify Pilot and CoPilot Baseline License Counts
    [Documentation]     Confirms license counts are at expected values in XIQ to begin with (nothing consumed)
    [Tags]              tcxm-20887    copilot_sanity_testing    copilot_license_testing    aiq-2214    development    xiq    copilot    test1

    Confirm Entitlement Counts for Feature Matches Expected     ${PILOT_ENTITLEMENT}       3    0    3
    Confirm Entitlement Counts for Feature Matches Expected     ${COPILOT_ENTITLEMENT}     2    0    2

Test 2: Onboard Device and Verify Success
    [Documentation]     Onboards test device and verifies success
    [Tags]              tcxm-20887    copilot_sanity_testing    copilot_license_testing    aiq-2214    development    xiq    copilot    test2

    Depends On          Test 1

    # Downgrade the device's iqagent if needed
    ${SPAWN_CONNECTION}=      Open Spawn        ${DUT_IP}   ${DUT_PORT}   ${DUT_USERNAME}   ${DUT_PASSWORD}   ${DUT_CLI_TYPE}
    ${DOWNGRADE_IQAGENT}=     Downgrade Iqagent              ${DUT_CLI_TYPE}        ${SPAWN_CONNECTION}
    Should Be Equal As Integers      ${DOWNGRADE_IQAGENT}     1

    ${CONF_STATUS_RESULT}=    Configure Device To Connect To Cloud        ${DUT_CLI_TYPE}    ${IQAGENT}   ${SPAWN_CONNECTION}    vr=${DUT_VR}
    Should Be Equal As Strings       ${CONF_STATUS_RESULT}    1
    Close Spawn         ${SPAWN_CONNECTION}

    Onboard New Test Device                     ${DUT_SERIAL}  ${netelem1}

    ${selected}=    Column Picker Select        ${COLUMN_1}     ${COLUMN_2}    ${COLUMN_3}
    Should Be Equal As Integers                 ${selected}     1

    Refresh Devices Page
    Verify and Wait Until Device Online         ${DUT_SERIAL}
    Verify and Wait Until Device Managed        ${DUT_SERIAL}
    Verify Device Status Green                  ${DUT_SERIAL}

Test 3: Verify Device Consumes Pilot and CoPilot License Within Global Settings License Management
    [Documentation]     Confirms the license counts for Pilot and CoPilot within Global Settings->License Management
    [Tags]              tcxm-20887    copilot_sanity_testing    copilot_license_testing    aiq-2214    development    xiq    copilot    test3

    Depends On          Test 1

    Confirm Entitlement Counts for Feature Matches Expected     ${PILOT_ENTITLEMENT}       2    1    3
    Confirm Entitlement Counts for Feature Matches Expected     ${COPILOT_ENTITLEMENT}     1    1    2

Test 4: Verify Device License and CoPilot Column Values
    [Documentation]     Confirms the Device License and CoPilot columns to verify device consumed the appropriate license or not
    [Tags]              tcxm-20887    copilot_sanity_testing    copilot_license_testing    aiq-2214    development    xiq    copilot    test4

    Depends On          Test 1

    # Confirm the device row shows the correct pilot license status
    ${pilot1_result}=      Get Device Details    ${DUT_SERIAL}    DEVICE LICENSE
    Should Contain         ${pilot1_result}      ${PILOT_LICENSE}

    # Confirm the device row shows the correct copilot license status
    ${copilot1_result}=    Get Device Details    ${DUT_SERIAL}    COPILOT
    Should Contain         ${copilot1_result}    ${COPILOT_ACTIVE}

Test 5: Unmanage Device and Confirm Success
    [Documentation]     Sets MANAGED state to UNMANAGE and verifies success
    [Tags]              tcxm-20887    copilot_release_testing    copilot_license_testing    aiq-2214    development    xiq    copilot    test5

    Depends On          Test 1

    Navigate to Devices and Confirm Success
    Unmanage Device and Confirm Success         UNMANAGE    ${DUT_SERIAL}

    ${pilot1_result}=      Get Device Details    ${DUT_SERIAL}         MANAGED
    Should Contain         ${pilot1_result}      Unmanaged

Test 6: Verify Unmanaged Device Revokes CoPilot and Pilot Licenses in Global Settings License Management
    [Documentation]     Confirms the license counts for Pilot and CoPilot within Global Settings->License Management
    [Tags]              tcxm-20887    copilot_release_testing    copilot_license_testing    aiq-2214    development    xiq    copilot    test6

    Depends On          Test 1

    Confirm Entitlement Counts for Feature Matches Expected     ${PILOT_ENTITLEMENT}       3    0    3
    Confirm Entitlement Counts for Feature Matches Expected     ${COPILOT_ENTITLEMENT}     2    0    2

Test 7: Verify Device License and CoPilot Column Values
    [Documentation]     Confirms the Device License and CoPilot columns for unmanaged device to verify device revoked the copilot and pilot licenses
    [Tags]              tcxm-20887    copilot_release_testing    copilot_license_testing    aiq-2214    development    xiq    copilot    test7

    Depends On          Test 1

    # Confirm the device row shows the correct pilot license status
    ${pilot1_result}=      Get Device Details    ${DUT_SERIAL}    DEVICE LICENSE
    Should Contain         ${pilot1_result}      ${NO_PILOT_LICENSE}

    # Confirm the device row shows the correct copilot license status
    ${copilot1_result}=    Get Device Details    ${DUT_SERIAL}    COPILOT
    Should Contain         ${copilot1_result}    ${COPILOT_NONE}

Test 8: Manage Device and Confirm Success
    [Documentation]     Sets MANAGED state to MANAGE and verifies success
    [Tags]              tcxm-20887    copilot_release_testing    copilot_license_testing    aiq-2214    development    xiq    copilot    test8

    Depends On          Test 1

    Navigate to Devices and Confirm Success
    Change Management Status and Confirm Success        MANAGE       ${DUT_SERIAL}

    ${manage1_result}=      Get Device Details    ${DUT_SERIAL}         MANAGED
    Should Contain         ${manage1_result}      Managed

Test 9: Verify Managed Device Consumes Pilot and CoPilot License Within Global Settings License Management
    [Documentation]     Confirms the license counts for Pilot and CoPilot within Global Settings->License Management
    [Tags]              tcxm-2082088784    copilot_sanity_testing    copilot_license_testing    aiq-2214    development    xiq    copilot    test9

    Depends On          Test 1

    Confirm Entitlement Counts for Feature Matches Expected     ${PILOT_ENTITLEMENT}       2    1    3
    Confirm Entitlement Counts for Feature Matches Expected     ${COPILOT_ENTITLEMENT}     1    1    2

Test 10: Verify Managed Device License and CoPilot Column Values
    [Documentation]     Confirms the Device License and CoPilot columns to verify device consumed the appropriate license or not
    [Tags]              tcxm-20887    copilot_sanity_testing    copilot_license_testing    aiq-2214    development    xiq    copilot    test10

    Depends On          Test 1

    # Confirm the device row shows the correct pilot license status
    ${pilot1_result}=      Get Device Details    ${DUT_SERIAL}    DEVICE LICENSE
    Should Contain         ${pilot1_result}      ${PILOT_LICENSE}

    # Confirm the device row shows the correct copilot license status
    ${copilot1_result}=    Get Device Details    ${DUT_SERIAL}    COPILOT
    Should Contain         ${copilot1_result}    ${COPILOT_ACTIVE}

Test 11: Delete Device and Verify Success
    [Documentation]     Deletes the device and verifies success
    [Tags]              tcxm-20887    copilot_sanity_testing    copilot_license_testing    aiq-2214    development    xiq    copilot    test11

    Depends On          Test 1

    Delete Test Device and Confirm Success          ${DUT_SERIAL}

Test 12: Verify Pilot and CoPilot Licenses Revoked Within Global Settings License Management
    [Documentation]     Confirms the Pilot and CoPilot licenses are revoked
    [Tags]              tcxm-20887    copilot_sanity_testing    copilot_license_testing    aiq-2214    development    xiq    copilot    test12

    Depends On          Test 1

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
    Onboard Device Quick    ${netelem}
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

Unmanage Device and Confirm Success
    [Documentation]     Unmanages the specified device and confirms success
    [Arguments]         ${manage_type}    ${serial}

    Search Device              device_serial=${serial}

    ${set_unmanaged_state}=    Change Manage Device Status     ${manage_type}      device_serial=${serial}
    Should Be Equal As Integers                                ${set_unmanaged_state}  1

Change Management Status and Confirm Success
    [Documentation]     Changes the manage device status between Manage and Unmanage on specific device(s) and confirms success
    [Arguments]         ${manage_type}    ${serial}

    ${set_managed_state}=    Change Manage Device Status     ${manage_type}      device_serial=${serial}
    Should Be Equal As Integers                                ${set_managed_state}  1
