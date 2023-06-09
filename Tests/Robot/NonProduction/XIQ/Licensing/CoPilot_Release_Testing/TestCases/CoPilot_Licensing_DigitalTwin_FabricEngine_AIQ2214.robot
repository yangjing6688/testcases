#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : David W. Truesdell
# Description   : Test Suite for testing CoPilot licensing on Digital Twin FabricEngine
#               : This is qTest test case TCCS-13505 in the CSIT project.


*** Settings ***
Resource         ../../CoPilot_Release_Testing/Resources/AllResources.robot

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}

Suite Setup      Log Into XIQ and Set Up Test
Suite Teardown   Tear Down Test and Close Session


*** Variables ***
${XIQ_URL}                  ${test_url}
${XIQ_USER}                 ${tenant_username}
${XIQ_PASSWORD}             ${tenant_password}
${IQAGENT}                  ${sw_connection_host}

${DT_FE_PERSONA}               ${netelem1.digital_twin_persona}
${DT_FE_MAKE}                  ${netelem1.make}
${DT_FE_MODEL}                 ${netelem1.model}
${DT_FE_VERSION}               ${netelem1.digital_twin_version}
${DT_FE_IP_ADDRESS}            ${netelem1.ip}


${PILOT_ENTITLEMENT}        XIQ-PIL-S-C
${COPILOT_ENTITLEMENT}      XIQ-COPILOT-S-C
${COPILOT_ACTIVE}           Active
${COPILOT_NONE}             None
${PILOT_LICENSE}            Pilot
${NO_PILOT_LICENSE}         Not Required

${COLUMN_1}                 CoPilot
${COLUMN_2}                 Managed
${COLUMN_3}                 Device License
${COLUMN_4}                 Model


*** Test Cases ***
Test 1: Verify Pilot and CoPilot Baseline License Counts
    [Documentation]     Confirms license counts are at expected values in XIQ to begin with (nothing consumed)
    [Tags]              tccs-13505    copilot_release_testing    copilot_license_testing    aiq-2214    development    xiq    copilot    digital_twin    test1

    Confirm Entitlement Counts for Feature Matches Expected     ${PILOT_ENTITLEMENT}       3    0    3
    Confirm Entitlement Counts for Feature Matches Expected     ${COPILOT_ENTITLEMENT}     2    0    2

Test 2: Onboard Digital Twin Fabric Engine Device
    [Documentation]     Onboard "Digital Twin" Fabric Engine device
    [Tags]              tccs-13505    copilot_release_testing    copilot_license_testing    aiq-2214     development    xiq    copilot    digital_twin    test2

    Depends On Test     Test 1: Verify Pilot and CoPilot Baseline License Counts

    Navigate to Devices and Confirm Success

    ${selected}=    Column Picker Select                    ${COLUMN_1}     ${COLUMN_2}    ${COLUMN_3}    ${COLUMN_4}
    Should Be Equal As Integers                             ${selected}     1

    ${ONBOARD_RESULT}=    onboard device quick              ${netelem1}
    Should Be Equal As Strings                              ${ONBOARD_RESULT}     1

    ${dt_fe_serial}=           set variable                    ${${netelem1.name}.serial}
    Set Suite Variable                                      ${DT_FE_SERIAL}     ${dt_fe_serial}

    Confirm Digital Twin Serial Number                      ${DT_FE_SERIAL}
    Confirm Device Status Icon                              ${DT_FE_SERIAL}     expected_icon=digital_twin
    Confirm Device Serial Online                            ${DT_FE_SERIAL}     retry_duration=10    retry_count=60
    Confirm Device Serial Managed                           ${DT_FE_SERIAL}     retry_duration=10    retry_count=60
    Confirm Device Serial Has Expected Status               ${DT_FE_SERIAL}     green

    ${dt_fe_mac}=   Get Device Details                      ${DT_FE_SERIAL}     MAC
    Set Suite Variable                                      ${DT_FE_MAC}        ${dt_fe_mac}

    Confirm Digital Twin MAC Address                        ${DT_FE_MAC}

    [Teardown]    Refresh Page

Test 3: Verify Device Does Not Consume Pilot or CoPilot License Within Global Settings License Management
    [Documentation]     Confirms the license counts for Pilot and CoPilot within Global Settings->License Management
    [Tags]              tccs-13505    copilot_release_testing    copilot_license_testing    aiq-2214    development    xiq    copilot    digital_twin    test3

    Depends On Test     Test 1: Verify Pilot and CoPilot Baseline License Counts

    Log To Console  Sleeping for 10 minutes to wait for the maximum 10 minute license update to come in
    Count Down in Minutes  10

    Confirm Entitlement Counts for Feature Matches Expected     ${PILOT_ENTITLEMENT}       3    0    3
    Confirm Entitlement Counts for Feature Matches Expected     ${COPILOT_ENTITLEMENT}     2    0    2

Test 4: Verify Device License and CoPilot Column Values On Device
    [Documentation]     Confirms the Device License and CoPilot column values to verify device did not consume the appropriate licenses
    [Tags]              tccs-13505    copilot_release_testing    copilot_license_testing    aiq-2214    development    xiq    copilot    digital_twin    test4

    Depends On Test     Test 1: Verify Pilot and CoPilot Baseline License Counts

    # Confirm the device row shows the correct pilot license status
    ${pilot1_result}=      Get Device Details    ${DT_FE_SERIAL}    DEVICE LICENSE
    Should Contain         ${pilot1_result}      ${NO_PILOT_LICENSE}

    # Confirm the device row shows the correct copilot license status
    ${copilot1_result}=    Get Device Details    ${DT_FE_SERIAL}    COPILOT
    Should Contain         ${copilot1_result}    ${COPILOT_NONE}


*** Keywords ***
Log Into XIQ and Set Up Test
    [Documentation]     Logs into XIQ and sets up the elements necessary to complete this test suite

    Log Into XIQ and Confirm Success            ${XIQ_USER}  ${XIQ_PASSWORD}  ${XIQ_URL}
    Enable CoPilot Feature and Confirm Success

Tear Down Test and Close Session
    [Documentation]     Cleans up test data, logs out of XIQ, and closes the browser

    Delete Device and Confirm Success                       ${DT_FE_SERIAL}
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
