#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : David W. Truesdell
# Description   : Test Suite for testing CoPilot licensing when user does not have CoPilot entitlements
#               : This test assumes the XIQ user has NO CoPilot entitlements
#               : This verifies a user without CoPilot entitlements can't enable the feature and when a
#               : device is onboarded it consumes a Pilot entitlement
#               : This is qTest test case TCCS-13534 in the CSIT project.


*** Settings ***
Resource         ../../CoPilot_Release_Testing/Resources/AllResources.robot

Force Tags       testbed_1_node

Suite Setup      Log Into XIQ and Set Up Test
Suite Teardown   Tear Down Test and Close Session


*** Variables ***
${XIQ_URL}                      ${test_url}
${XIQ_USER}                     ${tenant_username}
${XIQ_PASSWORD}                 ${tenant_password}
${IQAGENT}                      ${sw_connection_host}

${DUT1_SERIAL}                  ${netelem1.serial}
${DUT1_MAKE}                    ${netelem1.make}
${DUT1_MAC}                     ${netelem1.mac}
${DUT1_CLI_TYPE}                ${netelem1.cli_type}
${DUT1_IP}                      ${netelem1.ip}
${DUT1_PORT}                    ${netelem1.port}
${DUT1_USERNAME}                ${netelem1.username}
${DUT1_PASSWORD}                ${netelem1.password}
${DUT1_VR}                      ${netelem1.vr}

${PILOT_ENTITLEMENT}            PRD-XIQ-PIL-S-C
${COPILOT_ENTITLEMENT}          PRD-XIQ-COPILOT-S-C
${COPILOT_NONE}                 None
${PILOT_LICENSE}                Pilot

${COLUMN_1}                     CoPilot
${COLUMN_2}                     Managed
${COLUMN_3}                     Device License

${LOCATION}                     San Jose, building_01, floor_02


*** Test Cases ***
Test 1: Verify CoPilot Entitlement Not Present in License Management
    [Documentation]     Confirms CoPilot entitlement is not present in Licemse Management table
    [Tags]              tccs-13534    copilot_release_testing    copilot_license_testing    aiq-2214    development    xiq    copilot    test1

    Confirm Entitlements Table Does Not Contain Feature         PRD-XIQ-COPILOT-S-C

Test 2: Verify User Unable to "Enable CoPilot" Within CoPilot Menu Page and Alert Warning Present
    [Documentation]     Verifies the "Enable CoPilot" feature from CoPilot Menu page in not available to select and alert warning present
    [Tags]              tccs-13534    copilot_release_testing    copilot_license_testing    aiq-2214    development    xiq    copilot    test2

    Depends On          Test 1

    Enable CoPilot Menu Feature and Confirm No CoPilot Entitlements

Test 3: Verify User Unable to "Enable CoPilot" Within Global Settings->VIQ Management and Warning Banner Displayed
    [Documentation]     Enables CoPilot feature from Global Settings->VIQ Management page and verifies a warning banner is displayed
    [Tags]              tccs-13534    copilot_release_testing    copilot_license_testing    aiq-2214    development    xiq    copilot    test3

    Depends On          Test 1

    Enable CoPilot Feature For This VIQ and Confirm User Unable To Enable

Test 4: Verify Pilot Baseline License Counts
    [Documentation]     Confirms Pilot license count is at expected value in XIQ to begin with (nothing consumed)
    [Tags]              tccs-13534    copilot_release_testing    copilot_license_testing    aiq-2214    development    xiq    copilot    test4

    Depends On          Test 1

    Confirm Entitlement Counts for Feature Matches Expected     ${PILOT_ENTITLEMENT}       3    0    0

Test 5: Onboard Device and Verify Success
    [Documentation]     Onboards first test device and verifies success
    [Tags]              tccs-13534    copilot_release_testing    copilot_license_testing    aiq-2214    development    xiq    copilot    test5

    Depends On          Test 1

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

Test 6: Verify Device Consumes Pilot License Within Global Settings License Management
    [Documentation]     Confirms the license counts for Pilot within Global Settings->License Management
    [Tags]              tccs-13534    copilot_release_testing    copilot_license_testing    aiq-2214    development    xiq    copilot    test6

    Depends On          Test 1

    Confirm Entitlement Counts for Feature Matches Expected     ${PILOT_ENTITLEMENT}       2    1    1

Test 7: Verify Device License and CoPilot Column Values
    [Documentation]     Confirms the Device License and CoPilot columns to verify device consumed the pilot license and not a copilot license
    [Tags]              tccs-13534    copilot_release_testing    copilot_license_testing    aiq-2214    development    xiq    copilot    test7

    Depends On          Test 1

    # Confirm the device row shows the correct pilot license status
    ${pilot1_result}=      Get Device Details    ${DUT1_SERIAL}    DEVICE LICENSE
    Should Contain         ${pilot1_result}      ${PILOT_LICENSE}

    # Confirm the device row shows the correct copilot license status
    ${copilot1_result}=    Get Device Details    ${DUT1_SERIAL}    COPILOT
    Should Contain         ${copilot1_result}    ${COPILOT_NONE}

Test 8: Delete Device and Verify Success
    [Documentation]     Deletes a test device and verifies success
    [Tags]              tccs-13534    copilot_release_testing    copilot_license_testing    aiq-2214    development    xiq    copilot    test8

    Depends On          Test 1

    Delete Test Device and Confirm Success          ${DUT1_SERIAL}

Test 9: Verify Pilot and License Revoked
    [Documentation]     Confirms license counts are revoked in XIQ after devices were deleted
    [Tags]              tccs-13534    copilot_release_testing    copilot_license_testing    aiq-2214    development    xiq    copilot    test9

    Depends On          Test 1

    Confirm Entitlement Counts for Feature Matches Expected     ${PILOT_ENTITLEMENT}       3    0    0

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

Enable CoPilot Menu Feature and Confirm No CoPilot Entitlements
    [Documentation]     Verifies user is not able to click on "Enable CoPilot" feature in main CoPilot web page since user has no copilot entitlements

    ${result_enable}=               Enable CoPilot Menu Feature
    Should Be Equal As Strings      ${result_enable}     False

Confirm Entitlements Table Does Not Contain Feature
    [Documentation]     Checks to see if feature is in License Management table
    [Arguments]         ${feature}

    ${result_feature}=   Confirm Entitlements Table Contains Feature             ${feature}
    Should Be Equal As Integers                       ${result_feature}      -1

Confirm Entitlements Table Does Contain Feature
    [Documentation]     Checks to see if feature is in License Management table
    [Arguments]         ${feature}

    ${result_feature}=   Confirm Entitlements Table Contains Feature             ${feature}
    Should Be Equal As Integers                       ${result_feature}      1

Enable CoPilot Feature For This VIQ and Confirm User Unable To Enable
    [Documentation]     Verifies user is unable to Enables CoPilot feature in Global Settings -> VIQ Management, warning banner is displayed and verifies success

    ${result_enable}=    Enable CoPilot Feature For This VIQ
    Should Be Equal As Integers     ${result_enable}     1

    Verify CoPilot Deactivate Banner Message Displayed

Verify CoPilot Deactivate Banner Message Displayed
    [Documentation]     Verifies the "CoPilot deactivated due to lack of licenses" banner is displayed

    ${banner_result}=  Confirm CoPilot Deactivated Due To Lack Of Licenses Banner Displayed
    Should Be Equal As Strings                       ${banner_result}      True
