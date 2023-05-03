#----------------------------------------------------------------------
# Copyright (C) 2023... 2023 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : David W. Truesdell
# Description   : Test Suite for testing CoPilot license filter for All CoPilot Eligible Devices - UNIVERSAL Access Point
#               : This is qTest test case TCCS-15108 in the CSIT project.


*** Settings ***
Resource         ../../CoPilot_License_Filtering/Resources/AllResources.robot

Force Tags       testbed_1_node

Suite Setup      Log Into XIQ and Set Up Test
Suite Teardown   Tear Down Test and Close Session


*** Variables ***
${XIQ_URL}                  ${test_url}
${XIQ_USER}                 ${tenant_username}
${XIQ_PASSWORD}             ${tenant_password}
#${CAPWAP_URL}               ${capwap_url}
${IQAGENT}                  ${capwap_url}

${DUT1_SERIAL}              ${netelem1.serial}
${DUT1_MAKE}                ${netelem1.make}
${DUT1_MAC}                 ${netelem1.mac}
${DUT1_CLI_TYPE}            ${netelem1.cli_type}
${DUT1_IP}                  ${netelem1.ip}
${DUT1_PORT}                ${netelem1.port}
${DUT1_USERNAME}            ${netelem1.username}
${DUT1_PASSWORD}            ${netelem1.password}
${DUT1_VR}                  ${netelem1.vr}

${DT_PERSONA}               ${netelem2.digital_twin_persona}
${DT_MODEL}                 ${netelem2.model}
${DT_VERSION}               ${netelem2.digital_twin_version}

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
    [Tags]              tccs-15107    copilot_filter_testing    copilot_license_testing    xiq-16248   development    xiq    copilot    test1

    Confirm Entitlement Counts for Feature Matches Expected     ${PILOT_ENTITLEMENT}       3    0    3
    Confirm Entitlement Counts for Feature Matches Expected     ${COPILOT_ENTITLEMENT}     2    0    2

Test 2: Onboard Universal Access Point CoPilot Eligible Device and Verify Success
    [Documentation]     Onboards an EXOS CoPilot eligible device and verifies success
    [Tags]              tccs-15107    copilot_filter_testing    copilot_license_testing    xiq-16248   development    xiq    copilot    test2

    Depends On Test     Test 1: Verify Pilot and CoPilot Baseline License Counts

    Onboard New Test Device                     ${DUT1_SERIAL}  ${netelem1}

    # Downgrade the device's iqagent if needed
    ${SPAWN_CONNECTION}=      Open Spawn        ${DUT1_IP}   ${DUT1_PORT}   ${DUT1_USERNAME}   ${DUT1_PASSWORD}   ${DUT1_CLI_TYPE}
    ${DOWNGRADE_IQAGENT}=     Downgrade Iqagent              ${DUT1_CLI_TYPE}        ${SPAWN_CONNECTION}
    Should Be Equal As Integers      ${DOWNGRADE_IQAGENT}     1

    ${CONF_STATUS_RESULT}=    Configure Device To Connect To Cloud        ${DUT1_CLI_TYPE}    ${IQAGENT}   ${SPAWN_CONNECTION}    vr=${DUT1_VR}
    Should Be Equal As Strings       ${CONF_STATUS_RESULT}    1
    Close Spawn         ${SPAWN_CONNECTION}

    ${selected}=    Column Picker Select        ${COLUMN_1}     ${COLUMN_2}    ${COLUMN_3}
    Should Be Equal As Integers                 ${selected}     1

    Refresh Devices Page
    Verify and Wait Until Device Online         ${DUT1_SERIAL}
    Verify and Wait Until Device Managed        ${DUT1_SERIAL}
    Verify Device Status Green                  ${DUT1_SERIAL}

Test 3: Onboard Non-CoPilot Eligible Digital Twin Device and Verify Success
    [Documentation]     Onboards a non-CoPilot Digital Twin eligible device and verifies success
    [Tags]              tccs-15107    copilot_filter_testing    copilot_license_testing    xiq-16248   development    xiq    copilot    test3

    Depends On Test     Test 1: Verify Pilot and CoPilot Baseline License Counts

    ${ONBOARD_RESULT}=      onboard device quick            ${netelem2}
    Should Be Equal As Strings                              ${ONBOARD_RESULT}     1

    ${dt_serial}=           set variable                    ${${netelem2.name}.serial}
    Set Suite Variable                                      ${DT_SERIAL}    ${dt_serial}

    Verify and Wait Until Device Online                     ${DT_SERIAL}
    Verify and Wait Until Device Managed                    ${DT_SERIAL}
    Verify Device Status Green                              ${DT_SERIAL}

Test 4: Verify CoPilot Eligible Device Consumes Pilot And CoPilot Licenses Within Global Settings License Management
    [Documentation]     Confirms the license counts for Pilot and CoPilot within Global Settings->License Management
    [Tags]              tccs-15107    copilot_filter_testing    copilot_license_testing    xiq-16248   development    xiq    copilot    test4

    Depends On Test     Test 1: Verify Pilot and CoPilot Baseline License Counts

    Confirm Entitlement Counts for Feature Matches Expected     ${PILOT_ENTITLEMENT}       2    1    3
    Confirm Entitlement Counts for Feature Matches Expected     ${COPILOT_ENTITLEMENT}     1    1    2


Test 5: Verify Device License and CoPilot Column Values On Devices
    [Documentation]     Confirms the Device License and CoPilot column values to verify device consumed the appropriate license or not
    [Tags]              tccs-15107    copilot_filter_testing    copilot_license_testing    xiq-16248   development    xiq    copilot    test5

    Depends On Test     Test 1: Verify Pilot and CoPilot Baseline License Counts

    # Confirm the device row shows the correct pilot license status
    ${pilot1_result}=      Get Device Details    ${DUT1_SERIAL}    DEVICE LICENSE
    Should Contain         ${pilot1_result}      ${PILOT_LICENSE}

    # Confirm the device row shows the correct copilot license status
    ${copilot1_result}=    Get Device Details    ${DUT1_SERIAL}    COPILOT
    Should Contain         ${copilot1_result}    ${COPILOT_ACTIVE}

    # Confirm the device row shows the correct pilot license status
    ${pilot2_result}=      Get Device Details    ${DT_SERIAL}    DEVICE LICENSE
    Should Contain         ${pilot2_result}      ${NO_PILOT_LICENSE}

    # Confirm the device row shows the correct copilot license status
    ${copilot2_result}=    Get Device Details    ${DT_SERIAL}    COPILOT
    Should Contain         ${copilot2_result}    ${COPILOT_NONE}

Test 6: Filter For All CoPilot Eligible Devices and Verify Devices Present
    [Documentation]     Filters by the Device Product Type group 'All CoPilot Eligible Devices' to show devices that are CoPilot eligible
    [Tags]              tccs-15107    copilot_filter_testing    copilot_license_testing    xiq-16248   development    xiq    copilot    test6

    Depends On Test     Test 1: Verify Pilot and CoPilot Baseline License Counts
    
    Set Filter For All CoPilot Eligible Devices

    Confirm Device Serial Present in Filtered Devices Panel             ${DUT1_SERIAL}
    Confirm Device Serial Not Present in Filtered Devices Panel         ${DT_SERIAL}

Test 7: Clear Filter For All CoPilot Eligible Devices and Verify Devices Present
    [Documentation]     Clears filters by the Device Product Type group 'All CoPilot Eligible Devices' to show all onboarded devices
    [Tags]              tccs-15107    copilot_filter_testing    copilot_license_testing    xiq-16248   development    xiq    copilot    test7

    Depends On Test     Test 1: Verify Pilot and CoPilot Baseline License Counts

    Clear Filter For All CoPilot Eligible Devices

    Confirm Device Serial Present in Filtered Devices Panel         ${DUT1_SERIAL}
    Confirm Device Serial Present in Filtered Devices Panel         ${DT_SERIAL}

Test 8: Delete All Devices and Verify Success
    [Documentation]     Deletes all devices and verifies success
    [Tags]              tccs-15107    copilot_sanity_testing    copilot_license_testing    xiq-16248    development    xiq    copilot    test8

    Depends On Test     Test 1: Verify Pilot and CoPilot Baseline License Counts

    Delete All devices and Confirm Success

Test 9: Verify All Pilot and CoPilot Licenses Revoked Within Global Settings License Management
    [Documentation]     Confirms the license counts for Pilot and CoPilot within Global Settings->License Management
    [Tags]              tccs-15107    copilot_release_testing    copilot_license_testing    xiq-16248    development    xiq    copilot    test9

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

    Disable CoPilot Feature and Confirm Success
    Delete All devices and Confirm Success
    Clear All Filters
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

Delete All Devices and Confirm Success
    [Documentation]     Deletes the specified device and confirms the action was successful

    Navigate to Devices and Confirm Success

    ${del_result}=  Delete All Devices
    Should Be Equal As Integers  ${del_result}  1

Set Filter For All CoPilot Eligible Devices
    [Documentation]     Filters by the CoPilot License group - All CoPilot Eligible Devices

    Clear All Filters
    ${filter_result}=  Set CoPilot License Filter    All CoPilot Eligible Devices  true
    Should Be Equal As Integers                      ${filter_result}  1
    Apply Filters

Clear Filter For All CoPilot Eligible Devices
    [Documentation]     Clears the filter for Device Product Type group - All CoPilot Eligible Devices

    Clear All Filters
    ${filter_result}=  Set Device Product Type Filter    All CoPilot Eligible Devices    false
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
