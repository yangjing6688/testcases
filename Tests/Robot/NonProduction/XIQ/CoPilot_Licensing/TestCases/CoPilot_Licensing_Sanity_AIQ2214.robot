#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : David W. Truesdell
# Description   : Test Suite for testing CoPilot licensing
#               : This is qTest test case TCCS-13439 in the CSIT project.


*** Settings ***
Library          OperatingSystem
Library          common/Utils.py

Resource         ../../CoPilot_Licensing/Resources/AllResources.robot

Force Tags       testbed_3_node

Suite Setup      Log Into XIQ and Set Up Test
Suite Teardown   Tear Down Test and Close Session


*** Variables ***
${XIQ_URL}                  ${xiq.test_url}
${XIQ_USER}                 ${xiq.tenant_username}
${XIQ_PASSWORD}             ${xiq.tenant_password}
${IQAGENT}                  ${xiq.sw_connection_host}

${DUT1_SERIAL}              ${netelem2.serial}
${DUT1_MAKE}                ${netelem2.make}
${DUT1_CLI_TYPE}            ${netelem2.cli_type}
${DUT1_IP}                  ${netelem2.ip}
${DUT1_PORT}                ${netelem2.port}
${DUT1_USERNAME}            ${netelem2.username}
${DUT1_PASSWORD}            ${netelem2.password}
${DUT1_VR}                  ${netelem2.vr}

${DUT2_SERIAL}              ${netelem3.serial}
${DUT2_MAKE}                ${netelem3.make}
${DUT2_CLI_TYPE}            ${netelem3.cli_type}
${DUT2_IP}                  ${netelem3.ip}
${DUT2_PORT}                ${netelem3.port}
${DUT2_USERNAME}            ${netelem3.username}
${DUT2_PASSWORD}            ${netelem3.password}
${DUT2_VR}                  ${netelem3.vr}

${DUT3_SERIAL}              ${netelem5.serial}
${DUT3_MAKE}                ${netelem5.make}
${DUT3_CLI_TYPE}            ${netelem5.cli_type}
${DUT3_IP}                  ${netelem5.ip}
${DUT3_PORT}                ${netelem5.port}
${DUT3_USERNAME}            ${netelem5.username}
${DUT3_PASSWORD}            ${netelem5.password}
${DUT3_VR}                  ${netelem5.vr}

${PILOT_ENTITLEMENT}        ${xiq.pilot_entitlements}
${COPILOT_ENTITLEMENT}      ${xiq.copilot_entitlements}

${PILOT_LICENSE}            PRD-XIQ-PIL-S-C
${COPILOT_LICENSE}          PRD-XIQ-COPILOT-S-C

${LOCATION}                 San Jose, building_01, floor_02
${ACTIVE}                   Active
${NO_COPILOT}               None
${MANAGED}                  MANAGED

# The following columns are unselected by default
${COLUMN_1}                 CoPilot
${COLUMN_2}                 Managed

# The following columns are selected by default
${COLUMN_3}                 Device License


*** Test Cases ***
Test 1: Check Baseline License Counts
    [Documentation]     Confirms license counts are at expected values in XIQ to begin with (nothing consumed)
    [Tags]              tccs-13439    copilot_license_testing    aiq-2214    development    xiq    copilot    test1

    Confirm Entitlement Counts for Feature Matches Expected         PRD-XIQ-PIL-S-C             10    0    0
    Confirm Entitlement Counts for Feature Matches Expected         PRD-XIQ-COPILOT-S-C          2    0    0

Test 2: Onboard First Test Device and Verify Device Consumes Pilot and CoPilot License
    [Documentation]     Onboards test device and confirms the license counts
    [Tags]              tccs-13439    copilot_license_testing    aiq-2214    development    xiq    copilot    test2

    # Downgrade the device's iqagent if needed
    Downgrade Iqagent                           ${DUT1_IP}   ${DUT1_PORT}   ${DUT1_USERNAME}   ${DUT1_PASSWORD}   ${DUT1_CLI_TYPE}

    Configure Device To Connect To Cloud        ${DUT1_CLI_TYPE}  ${DUT1_IP}  ${DUT1_PORT}  ${DUT1_USERNAME}  ${DUT1_PASSWORD}  ${IQAGENT}  vr=${DUT1_VR}
    Onboard New Test Device                     ${DUT1_SERIAL}  ${DUT1_MAKE}  ${LOCATION}

    Column Picker Select                                        ${COLUMN_1}     ${COLUMN_2}
    ${selected}=    Confirm Column Picker Column Selected       ${COLUMN_1}     ${COLUMN_2}    ${COLUMN_3}
    Should Be Equal As Integers                 ${selected}     1

    Refresh Devices Page
    Verify Device Online                        ${DUT1_SERIAL}
    Verify Device Managed                       ${DUT1_SERIAL}    ${MANAGED}
    Verify Device Status Green                  ${DUT1_SERIAL}

    # Confirm license counts
    Confirm Entitlement Counts for Feature Matches Expected         PRD-XIQ-PIL-S-C             9    1    1
    Confirm Entitlement Counts for Feature Matches Expected         PRD-XIQ-COPILOT-S-C         1    1    1

Test 3: Onboard Second Test Device and Verify Device Consumes Pilot and CoPilot License
    [Documentation]     Onboards a second test device and confirms the license counts
    [Tags]              tccs-13439    copilot_license_testing    aiq-2214    development    xiq    copilot    test3

    # Downgrade the device's iqagent if needed
    Downgrade Iqagent                           ${DUT2_IP}   ${DUT2_PORT}   ${DUT2_USERNAME}   ${DUT2_PASSWORD}   ${DUT2_CLI_TYPE}

    Configure Device To Connect To Cloud        ${DUT2_CLI_TYPE}  ${DUT2_IP}  ${DUT2_PORT}  ${DUT2_USERNAME}  ${DUT2_PASSWORD}  ${IQAGENT}    vr=${DUT2_VR}
    Onboard New Test Device                     ${DUT2_SERIAL}  ${DUT2_MAKE}  ${LOCATION}

    Refresh Devices Page
    Verify Device Online                        ${DUT2_SERIAL}
    Verify Device Managed                       ${DUT2_SERIAL}    ${MANAGED}
    Verify Device Status Green                  ${DUT2_SERIAL}

    # Confirm license counts
    Confirm Entitlement Counts for Feature Matches Expected         PRD-XIQ-PIL-S-C             8    2    2
    Confirm Entitlement Counts for Feature Matches Expected         PRD-XIQ-COPILOT-S-C         0    2    2

Test 4: Onboard Third Test Device and Verify Device Consumes Pilot but not CoPilot License
    [Documentation]     Onboards a third test device and confirms the license counts
    [Tags]              tccs-13439    copilot_license_testing    aiq-2214    development    xiq    copilot    test4

    # Downgrade the device's iqagent if needed
    Downgrade Iqagent                           ${DUT3_IP}   ${DUT3_PORT}   ${DUT3_USERNAME}   ${DUT3_PASSWORD}   ${DUT3_CLI_TYPE}

    Configure Device To Connect To Cloud        ${DUT3_CLI_TYPE}  ${DUT3_IP}  ${DUT3_PORT}  ${DUT3_USERNAME}  ${DUT3_PASSWORD}  ${IQAGENT}  vr=${DUT3_VR}
    Onboard New Test Device                     ${DUT3_SERIAL}  ${DUT3_MAKE}  ${LOCATION}

    Refresh Devices Page
    Verify Device Online                        ${DUT3_SERIAL}
    Verify Device Managed                       ${DUT3_SERIAL}    ${MANAGED}
    Verify Device Status Green                  ${DUT3_SERIAL}

    # Confirm license counts
    Confirm Entitlement Counts for Feature Matches Expected         PRD-XIQ-PIL-S-C             7    3    3
    Confirm Entitlement Counts for Feature Matches Expected         PRD-XIQ-COPILOT-S-C         0    2    2

Test 5: Verify CoPilot License Status
    [Documentation]     Confirms the CoPilot License Status column to verify it consumed a license or not
    [Tags]              tccs-13439    copilot_license_testing    aiq-2214    development    xiq    copilot    test5

    # Confirm the device row shows the correct copilot license status
    ${copilot1_result}=    Get Device Details    ${DUT1_SERIAL}    COPILOT
    Should Contain         ${copilot1_result}    ${ACTIVE}

    ${copilot2_result}=    Get Device Details    ${DUT2_SERIAL}    COPILOT
    Should Contain         ${copilot2_result}    ${ACTIVE}

    ${copilot3_result}=    Get Device Details    ${DUT3_SERIAL}    COPILOT
    Should Contain         ${copilot3_result}    ${NO_COPILOT}

Test 6: Delete Third Test Device and Verify Pilot License Revoked But Not CoPilot License
    [Documentation]     Deletes a test device and confirms the license counts
    [Tags]              tccs-13439    copilot_license_testing    aiq-2214    development    xiq    copilot    test6

    Delete Test Device and Confirm Success          ${DUT3_SERIAL}

    # Confirm license counts
    Confirm Entitlement Counts for Feature Matches Expected         PRD-XIQ-PIL-S-C             8    2    2
    Confirm Entitlement Counts for Feature Matches Expected         PRD-XIQ-COPILOT-S-C         0    2    2

Test 7: Delete Second Test Device and Verify Both Pilot and CoPilot Licenses Revoked
    [Documentation]     Deletes a test device and confirms the license counts
    [Tags]              tccs-13439    copilot_license_testing    aiq-2214    development    xiq    copilot    test7

    Delete Test Device and Confirm Success          ${DUT2_SERIAL}

    # Confirm license counts
    Confirm Entitlement Counts for Feature Matches Expected         PRD-XIQ-PIL-S-C             9    1    1
    Confirm Entitlement Counts for Feature Matches Expected         PRD-XIQ-COPILOT-S-C         1    1    1

Test 8: Delete First Test Device and Verify Both Pilot and CoPilot Licenses Revoked
    [Documentation]     Deletes a test device and confirms the license counts
    [Tags]              tccs-13439    copilot_license_testing    aiq-2214    development    xiq    copilot    test8

    Delete Test Device and Confirm Success          ${DUT1_SERIAL}

    # Confirm license counts
    Confirm Entitlement Counts for Feature Matches Expected         PRD-XIQ-PIL-S-C             10    0    0
    Confirm Entitlement Counts for Feature Matches Expected         PRD-XIQ-COPILOT-S-C          2    0    0


*** Keywords ***
Log Into XIQ and Set Up Test
    [Documentation]     Logs into XIQ and sets up the elements necessary to complete this test suite

    Log Into XIQ and Confirm Success            ${XIQ_USER}  ${XIQ_PASSWORD}  ${XIQ_URL}

    # Enable CoPilot Feature
    Enable CoPilot Feature For This VIQ

Tear Down Test and Close Session
    [Documentation]     Cleans up test data, logs out of XIQ, and closes the browser

    # Disable CoPilot Feature
    Disable CoPilot Feature For This VIQ

    Log Out of XIQ and Quit Browser

Onboard New Test Device
    [Documentation]     Onboards the specified test device, deleting it first if it already exists
    [Arguments]         ${serial}  ${make}  ${location}

    Navigate to Devices and Confirm Success

    # If the device has already been onboarded, delete it first
    Delete Device and Confirm Success  ${serial}
    Confirm Device Serial Not Present  ${serial}

    # Onboard the device
    Onboard Device    ${serial}  ${make}  location=${location}
    sleep   ${DEVICE_ONBOARDING_WAIT}
    Confirm Device Serial Present  ${serial}

Verify Device Online
    [Documentation]     Confirms that the device is online in XIQ
    [Arguments]         ${serial}

    ${online}=    Wait Until Device Online          ${serial}
    Should Be Equal As Integers                     ${online}     1

Verify Device Managed
    [Documentation]     Confirms that the device is managed by XIQ
    [Arguments]         ${serial}    ${column}

    ${managed}=    wait_until_device_managed        ${serial}
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
