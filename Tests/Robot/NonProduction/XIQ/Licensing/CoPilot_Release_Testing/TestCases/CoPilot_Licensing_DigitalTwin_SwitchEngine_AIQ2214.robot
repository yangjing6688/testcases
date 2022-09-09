#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : David W. Truesdell
# Description   : Test Suite for testing CoPilot licensing on Digital Twin SwitchEngine
#               : This is qTest test case TCCS-13504 in the CSIT project.


*** Settings ***
Resource         ../../CoPilot_Release_Testing/Resources/AllResources.robot

Force Tags       testbed_none

Suite Setup      Log Into XIQ and Set Up Test
Suite Teardown   Tear Down Test and Close Session


*** Variables ***
${XIQ_URL}                  ${test_url}
${XIQ_USER}                 ${tenant_username}
${XIQ_PASSWORD}             ${tenant_password}
${IQAGENT}                  ${sw_connection_host}

${DT_SE_PERSONA}            SwitchEngine
${DT_SE_MODEL}              5520-24T
${DT_SE_VERSION}            32.1.1.6
${DT_SE_POLICY}
${DT_SE_SERIAL}
${DT_SE_MAC}

${PILOT_ENTITLEMENT}        PRD-XIQ-PIL-S-C
${COPILOT_ENTITLEMENT}      PRD-XIQ-COPILOT-S-C
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
    [Tags]              tccs-13504    copilot_release_testing    copilot_license_testing    aiq-2214    development    xiq    copilot    digital_twin    test1

    Confirm Entitlement Counts for Feature Matches Expected     ${PILOT_ENTITLEMENT}       10   0    0
    Confirm Entitlement Counts for Feature Matches Expected     ${COPILOT_ENTITLEMENT}     2    0    0

Test 2: Onboard Digital Twin Switch Engine Device
    [Documentation]     Onboard "Digital Twin" Switch Engine device
    [Tags]              tccs-13504    copilot_release_testing    copilot_license_testing    aiq-2214     development    xiq    copilot    digital_twin    test2

    Navigate to Devices and Confirm Success

    ${selected}=    Column Picker Select                    ${COLUMN_1}     ${COLUMN_2}    ${COLUMN_3}
    Should Be Equal As Integers                             ${selected}     1

    ${dt_se_serial}=  Onboard Device DT                     device_type=Digital_Twin        os_persona=${DT_SE_PERSONA}
    ...                                                     device_model=${DT_SE_MODEL}     os_version=${DT_SE_VERSION}
    ...                                                     policy=${DT_SE_POLICY}
    Set Suite Variable                                      ${DT_SE_SERIAL}     ${dt_se_serial}

    Confirm Digital Twin Serial Number                      ${DT_SE_SERIAL}
    Confirm Device Status Icon                              ${DT_SE_SERIAL}     expected_icon=digital_twin
    Confirm Device Serial Online                            ${DT_SE_SERIAL}     retry_duration=10    retry_count=60
    Confirm Device Serial Managed                           ${DT_SE_SERIAL}     retry_duration=10    retry_count=60
    Confirm Device Serial Has Expected Status               ${DT_SE_SERIAL}     green

    ${dt_se_mac}=   Get Device Details                      ${DT_SE_SERIAL}     MAC
    Set Suite Variable                                      ${DT_SE_MAC}        ${dt_se_mac}

    Confirm Digital Twin MAC Address                        ${DT_SE_MAC}

    [Teardown]    Refresh Page

Test 3: Verify Device Does Not Consume Pilot or CoPilot License Within Global Settings License Management
    [Documentation]     Confirms the license counts for Pilot and CoPilot within Global Settings->License Management
    [Tags]              tccs-13504    copilot_release_testing    copilot_license_testing    aiq-2214    development    xiq    copilot    digital_twin    test3

    Depends On          Test 1

    Log To Console  Sleeping for 10 minutes to wait for the maximum 10 minute license update to come in
    Count Down in Minutes  10

    Confirm Entitlement Counts for Feature Matches Expected     ${PILOT_ENTITLEMENT}       10   0    0
    Confirm Entitlement Counts for Feature Matches Expected     ${COPILOT_ENTITLEMENT}     2    0    0

Test 4: Verify Device License and CoPilot Column Values On Device
    [Documentation]     Confirms the Device License and CoPilot column values to verify device did not consume the appropriate licenses
    [Tags]              tccs-13504    copilot_release_testing    copilot_license_testing    aiq-2214    development    xiq    copilot    digital_twin    test4

    Depends On          Test 1

    # Confirm the device row shows the correct pilot license status
    ${pilot1_result}=      Get Device Details    ${DT_SE_SERIAL}    DEVICE LICENSE
    Should Contain         ${pilot1_result}      ${NO_PILOT_LICENSE}

    # Confirm the device row shows the correct copilot license status
    ${copilot1_result}=    Get Device Details    ${DT_SE_SERIAL}    COPILOT
    Should Contain         ${copilot1_result}    ${COPILOT_NONE}


*** Keywords ***
Log Into XIQ and Set Up Test
    [Documentation]     Logs into XIQ and sets up the elements necessary to complete this test suite

    Log Into XIQ and Confirm Success            ${XIQ_USER}  ${XIQ_PASSWORD}  ${XIQ_URL}
    Enable CoPilot Feature and Confirm Success

Tear Down Test and Close Session
    [Documentation]     Cleans up test data, logs out of XIQ, and closes the browser

    Delete Device and Confirm Success                       ${DT_SE_SERIAL}
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

Confirm Required Columns Selected
    [Documentation]     Confirms the Device License and CoPilot columns are selected
    [Arguments]         ${column1}    ${column2}

    ${selected}=    Confirm Column Picker Column Selected     ${COLUMN_1}  ${COLUMN_2}
    Should Be Equal As Integers     ${selected}    1
