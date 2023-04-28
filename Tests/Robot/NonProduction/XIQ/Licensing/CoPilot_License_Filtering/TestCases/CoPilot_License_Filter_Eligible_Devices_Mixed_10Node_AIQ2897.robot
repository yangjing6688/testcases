#----------------------------------------------------------------------
# Copyright (C) 2023... 2023 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : David W. Truesdell
# Description   : Test Suite for testing CoPilot license filtering for All CoPilot Eligible Devices - 10 Mixed Devices
#               : This is qTest test case TCCS-15118 in the CSIT project.


*** Settings ***
Resource         ../../CoPilot_License_Filtering/Resources/AllResources.robot

Force Tags       testbed_10_node

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

${DUT3_SERIAL}              ${netelem3.serial}
${DUT3_MAKE}                ${netelem3.make}
${DUT3_MAC}                 ${netelem3.mac}
${DUT3_CLI_TYPE}            ${netelem3.cli_type}
${DUT3_IP}                  ${netelem3.ip}
${DUT3_PORT}                ${netelem3.port}
${DUT3_USERNAME}            ${netelem3.username}
${DUT3_PASSWORD}            ${netelem3.password}
${DUT3_VR}                  ${netelem3.vr}

${DUT4_SERIAL}              ${netelem4.serial}
${DUT4_MAKE}                ${netelem4.make}
${DUT4_MAC}                 ${netelem4.mac}
${DUT4_CLI_TYPE}            ${netelem4.cli_type}
${DUT4_IP}                  ${netelem4.ip}
${DUT4_PORT}                ${netelem4.port}
${DUT4_USERNAME}            ${netelem4.username}
${DUT4_PASSWORD}            ${netelem4.password}
${DUT4_VR}                  ${netelem4.vr}

${DUT5_SERIAL}              ${netelem5.serial}
${DUT5_MAKE}                ${netelem5.make}
${DUT5_MAC}                 ${netelem5.mac}
${DUT5_CLI_TYPE}            ${netelem5.cli_type}
${DUT5_IP}                  ${netelem5.ip}
${DUT5_PORT}                ${netelem5.port}
${DUT5_USERNAME}            ${netelem5.username}
${DUT5_PASSWORD}            ${netelem5.password}
${DUT5_VR}                  ${netelem5.vr}

${DUT6_SERIAL}              ${netelem6.serial}
${DUT6_MAKE}                ${netelem6.make}
${DUT6_MAC}                 ${netelem6.mac}
${DUT6_CLI_TYPE}            ${netelem6.cli_type}
${DUT6_IP}                  ${netelem6.ip}
${DUT6_PORT}                ${netelem6.port}
${DUT6_USERNAME}            ${netelem6.username}
${DUT6_PASSWORD}            ${netelem6.password}
${DUT6_VR}                  ${netelem6.vr}

${DUT7_SERIAL}              ${netelem7.serial}
${DUT7_MAKE}                ${netelem7.make}
${DUT7_MAC}                 ${netelem7.mac}
${DUT7_CLI_TYPE}            ${netelem7.cli_type}
${DUT7_IP}                  ${netelem7.ip}
${DUT7_PORT}                ${netelem7.port}
${DUT7_USERNAME}            ${netelem7.username}
${DUT7_PASSWORD}            ${netelem7.password}
${DUT7_VR}                  ${netelem7.vr}

${DUT8_SERIAL}              ${netelem8.serial}
${DUT8_MAKE}                ${netelem8.make}
${DUT8_MAC}                 ${netelem8.mac}
${DUT8_CLI_TYPE}            ${netelem8.cli_type}
${DUT8_IP}                  ${netelem8.ip}
${DUT8_PORT}                ${netelem8.port}
${DUT8_USERNAME}            ${netelem8.username}
${DUT8_PASSWORD}            ${netelem8.password}
${DUT8_VR}                  ${netelem8.vr}

${DUT9_SERIAL}              ${netelem9.serial}
${DUT9_MAKE}                ${netelem9.make}
${DUT9_MAC}                 ${netelem9.mac}
${DUT9_CLI_TYPE}            ${netelem9.cli_type}
${DUT9_IP}                  ${netelem9.ip}
${DUT9_PORT}                ${netelem9.port}
${DUT9_USERNAME}            ${netelem9.username}
${DUT9_PASSWORD}            ${netelem9.password}
${DUT9_VR}                  ${netelem9.vr}

${DT_PERSONA}               ${netelem10.digital_twin_persona}
${DT_MODEL}                 ${netelem10.model}
${DT_VERSION}               ${netelem10.digital_twin_version}

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
    [Tags]              tccs-15118    copilot_filter_testing    copilot_license_testing    xiq-16248   development    xiq    copilot    test1

    Confirm Entitlement Counts for Feature Matches Expected     ${PILOT_ENTITLEMENT}       10    0    10
    Confirm Entitlement Counts for Feature Matches Expected     ${COPILOT_ENTITLEMENT}      2    0     2

Test 2: Onboard EXOS CoPilot Eligible Device and Verify Success
    [Documentation]     Onboards an EXOS CoPilot eligible device and verifies success
    [Tags]              tccs-15118    copilot_filter_testing    copilot_license_testing    xiq-16248   development    xiq    copilot    test2

    Depends On Test     Test 1: Verify Pilot and CoPilot Baseline License Counts

    # Downgrade the device's iqagent if needed
    ${SPAWN_CONNECTION}=      Open Spawn        ${DUT1_IP}   ${DUT1_PORT}   ${DUT1_USERNAME}   ${DUT1_PASSWORD}   ${DUT1_CLI_TYPE}
    ${DOWNGRADE_IQAGENT}=     Downgrade Iqagent              ${DUT1_CLI_TYPE}        ${SPAWN_CONNECTION}
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

Test 3: Onboard VOSS CoPilot Eligible Device and Verify Success
    [Documentation]     Onboards a VOSS CoPilot eligible device and verifies success
    [Tags]              tccs-15118    copilot_filter_testing    copilot_license_testing    xiq-16248   development    xiq    copilot    test3

    Depends On Test     Test 1: Verify Pilot and CoPilot Baseline License Counts

    # Downgrade the device's iqagent if needed
    ${SPAWN_CONNECTION}=      Open Spawn        ${DUT2_IP}   ${DUT2_PORT}   ${DUT2_USERNAME}   ${DUT2_PASSWORD}   ${DUT2_CLI_TYPE}
    ${DOWNGRADE_IQAGENT}=     Downgrade Iqagent              ${DUT2_CLI_TYPE}        ${SPAWN_CONNECTION}
    Should Be Equal As Integers      ${DOWNGRADE_IQAGENT}     1

    ${CONF_STATUS_RESULT}=    Configure Device To Connect To Cloud        ${DUT2_CLI_TYPE}    ${IQAGENT}   ${SPAWN_CONNECTION}    vr=${DUT2_VR}
    Should Be Equal As Strings       ${CONF_STATUS_RESULT}    1
    Close Spawn         ${SPAWN_CONNECTION}

    Onboard New Test Device                     ${DUT2_SERIAL}  ${netelem2}

    ${selected}=    Column Picker Select        ${COLUMN_1}     ${COLUMN_2}    ${COLUMN_3}
    Should Be Equal As Integers                 ${selected}     1

    Refresh Devices Page
    Verify and Wait Until Device Online         ${DUT2_SERIAL}
    Verify and Wait Until Device Managed        ${DUT2_SERIAL}
    Verify Device Status Green                  ${DUT2_SERIAL}

Test 4: Onboard Universal Switch Engine CoPilot Eligible Device and Verify Success
    [Documentation]     Onboards a Universal Switch Engine CoPilot eligible device and verifies success
    [Tags]              tccs-15118    copilot_filter_testing    copilot_license_testing    xiq-16248   development    xiq    copilot    test4

    Depends On Test     Test 1: Verify Pilot and CoPilot Baseline License Counts

    # Downgrade the device's iqagent if needed
    ${SPAWN_CONNECTION}=      Open Spawn        ${DUT3_IP}   ${DUT3_PORT}   ${DUT3_USERNAME}   ${DUT3_PASSWORD}   ${DUT3_CLI_TYPE}
    ${DOWNGRADE_IQAGENT}=     Downgrade Iqagent              ${DUT3_CLI_TYPE}        ${SPAWN_CONNECTION}
    Should Be Equal As Integers      ${DOWNGRADE_IQAGENT}     1

    ${CONF_STATUS_RESULT}=    Configure Device To Connect To Cloud        ${DUT3_CLI_TYPE}    ${IQAGENT}   ${SPAWN_CONNECTION}    vr=${DUT3_VR}
    Should Be Equal As Strings       ${CONF_STATUS_RESULT}    1
    Close Spawn         ${SPAWN_CONNECTION}

    Onboard New Test Device                     ${DUT3_SERIAL}  ${netelem3}

    ${selected}=    Column Picker Select        ${COLUMN_1}     ${COLUMN_2}    ${COLUMN_3}
    Should Be Equal As Integers                 ${selected}     1

    Refresh Devices Page
    Verify and Wait Until Device Online         ${DUT3_SERIAL}
    Verify and Wait Until Device Managed        ${DUT3_SERIAL}
    Verify Device Status Green                  ${DUT3_SERIAL}

Test 5: Onboard Universal Fabric Engine CoPilot Eligible Device and Verify Success
    [Documentation]     Onboards a Univeral Fabric Engine CoPilot eligible device and verifies success
    [Tags]              tccs-15118    copilot_filter_testing    copilot_license_testing    xiq-16248   development    xiq    copilot    test5

    Depends On Test     Test 1: Verify Pilot and CoPilot Baseline License Counts

    # Downgrade the device's iqagent if needed
    ${SPAWN_CONNECTION}=      Open Spawn        ${DUT4_IP}   ${DUT4_PORT}   ${DUT4_USERNAME}   ${DUT4_PASSWORD}   ${DUT4_CLI_TYPE}
    ${DOWNGRADE_IQAGENT}=     Downgrade Iqagent              ${DUT4_CLI_TYPE}        ${SPAWN_CONNECTION}
    Should Be Equal As Integers      ${DOWNGRADE_IQAGENT}     1

    ${CONF_STATUS_RESULT}=    Configure Device To Connect To Cloud        ${DUT4_CLI_TYPE}    ${IQAGENT}   ${SPAWN_CONNECTION}    vr=${DUT4_VR}
    Should Be Equal As Strings       ${CONF_STATUS_RESULT}    1
    Close Spawn         ${SPAWN_CONNECTION}

    Onboard New Test Device                     ${DUT4_SERIAL}  ${netelem4}

    ${selected}=    Column Picker Select        ${COLUMN_1}     ${COLUMN_2}    ${COLUMN_3}
    Should Be Equal As Integers                 ${selected}     1

    Refresh Devices Page
    Verify and Wait Until Device Online         ${DUT4_SERIAL}
    Verify and Wait Until Device Managed        ${DUT4_SERIAL}
    Verify Device Status Green                  ${DUT4_SERIAL}

Test 6: Onboard Second EXOS CoPilot Eligible Device and Verify Success
    [Documentation]     Onboards a second EXOS CoPilot eligible device and verifies success
    [Tags]              tccs-15118    copilot_filter_testing    copilot_license_testing    xiq-16248   development    xiq    copilot    test6

    Depends On Test     Test 1: Verify Pilot and CoPilot Baseline License Counts

    # Downgrade the device's iqagent if needed
    ${SPAWN_CONNECTION}=      Open Spawn        ${DUT5_IP}   ${DUT5_PORT}   ${DUT5_USERNAME}   ${DUT5_PASSWORD}   ${DUT5_CLI_TYPE}
    ${DOWNGRADE_IQAGENT}=     Downgrade Iqagent              ${DUT5_CLI_TYPE}        ${SPAWN_CONNECTION}
    Should Be Equal As Integers      ${DOWNGRADE_IQAGENT}     1

    ${CONF_STATUS_RESULT}=    Configure Device To Connect To Cloud        ${DUT5_CLI_TYPE}    ${IQAGENT}   ${SPAWN_CONNECTION}    vr=${DUT5_VR}
    Should Be Equal As Strings       ${CONF_STATUS_RESULT}    1
    Close Spawn         ${SPAWN_CONNECTION}

    Onboard New Test Device                     ${DUT5_SERIAL}  ${netelem5}

    ${selected}=    Column Picker Select        ${COLUMN_1}     ${COLUMN_2}    ${COLUMN_3}
    Should Be Equal As Integers                 ${selected}     1

    Refresh Devices Page
    Verify and Wait Until Device Online         ${DUT5_SERIAL}
    Verify and Wait Until Device Managed        ${DUT5_SERIAL}
    Verify Device Status Green                  ${DUT5_SERIAL}

Test 7: Onboard Third EXOS CoPilot Eligible Device and Verify Success
    [Documentation]     Onboards a third EXOS CoPilot eligible device and verifies success
    [Tags]              tccs-15118    copilot_filter_testing    copilot_license_testing    xiq-16248   development    xiq    copilot    test7

    Depends On Test     Test 1: Verify Pilot and CoPilot Baseline License Counts

    # Downgrade the device's iqagent if needed
    ${SPAWN_CONNECTION}=      Open Spawn        ${DUT6_IP}   ${DUT6_PORT}   ${DUT6_USERNAME}   ${DUT6_PASSWORD}   ${DUT6_CLI_TYPE}
    ${DOWNGRADE_IQAGENT}=     Downgrade Iqagent              ${DUT6_CLI_TYPE}        ${SPAWN_CONNECTION}
    Should Be Equal As Integers      ${DOWNGRADE_IQAGENT}     1

    ${CONF_STATUS_RESULT}=    Configure Device To Connect To Cloud        ${DUT6_CLI_TYPE}    ${IQAGENT}   ${SPAWN_CONNECTION}    vr=${DUT6_VR}
    Should Be Equal As Strings       ${CONF_STATUS_RESULT}    1
    Close Spawn         ${SPAWN_CONNECTION}

    Onboard New Test Device                     ${DUT6_SERIAL}  ${netelem6}

    ${selected}=    Column Picker Select        ${COLUMN_1}     ${COLUMN_2}    ${COLUMN_3}
    Should Be Equal As Integers                 ${selected}     1

    Refresh Devices Page
    Verify and Wait Until Device Online         ${DUT6_SERIAL}
    Verify and Wait Until Device Managed        ${DUT6_SERIAL}
    Verify Device Status Green                  ${DUT6_SERIAL}

Test 8: Onboard Fourth EXOS CoPilot Eligible Device and Verify Success
    [Documentation]     Onboards a fourth EXOS CoPilot eligible device and verifies success
    [Tags]              tccs-15118    copilot_filter_testing    copilot_license_testing    xiq-16248   development    xiq    copilot    test8

    Depends On Test     Test 1: Verify Pilot and CoPilot Baseline License Counts

    # Downgrade the device's iqagent if needed
    ${SPAWN_CONNECTION}=      Open Spawn        ${DUT7_IP}   ${DUT7_PORT}   ${DUT7_USERNAME}   ${DUT7_PASSWORD}   ${DUT7_CLI_TYPE}
    ${DOWNGRADE_IQAGENT}=     Downgrade Iqagent              ${DUT7_CLI_TYPE}        ${SPAWN_CONNECTION}
    Should Be Equal As Integers      ${DOWNGRADE_IQAGENT}     1

    ${CONF_STATUS_RESULT}=    Configure Device To Connect To Cloud        ${DUT7_CLI_TYPE}    ${IQAGENT}   ${SPAWN_CONNECTION}    vr=${DUT7_VR}
    Should Be Equal As Strings       ${CONF_STATUS_RESULT}    1
    Close Spawn         ${SPAWN_CONNECTION}

    Onboard New Test Device                     ${DUT7_SERIAL}  ${netelem7}

    ${selected}=    Column Picker Select        ${COLUMN_1}     ${COLUMN_2}    ${COLUMN_3}
    Should Be Equal As Integers                 ${selected}     1

    Refresh Devices Page
    Verify and Wait Until Device Online         ${DUT7_SERIAL}
    Verify and Wait Until Device Managed        ${DUT7_SERIAL}
    Verify Device Status Green                  ${DUT7_SERIAL}

Test 9: Onboard Fifth EXOS CoPilot Eligible Device and Verify Success
    [Documentation]     Onboards a fifth EXOS CoPilot eligible device and verifies success
    [Tags]              tccs-15118    copilot_filter_testing    copilot_license_testing    xiq-16248   development    xiq    copilot    test9

    Depends On Test     Test 1: Verify Pilot and CoPilot Baseline License Counts

    # Downgrade the device's iqagent if needed
    ${SPAWN_CONNECTION}=      Open Spawn        ${DUT8_IP}   ${DUT8_PORT}   ${DUT8_USERNAME}   ${DUT8_PASSWORD}   ${DUT8_CLI_TYPE}
    ${DOWNGRADE_IQAGENT}=     Downgrade Iqagent              ${DUT8_CLI_TYPE}        ${SPAWN_CONNECTION}
    Should Be Equal As Integers      ${DOWNGRADE_IQAGENT}     1

    ${CONF_STATUS_RESULT}=    Configure Device To Connect To Cloud        ${DUT8_CLI_TYPE}    ${IQAGENT}   ${SPAWN_CONNECTION}    vr=${DUT8_VR}
    Should Be Equal As Strings       ${CONF_STATUS_RESULT}    1
    Close Spawn         ${SPAWN_CONNECTION}

    Onboard New Test Device                     ${DUT8_SERIAL}  ${netelem8}

    ${selected}=    Column Picker Select        ${COLUMN_1}     ${COLUMN_2}    ${COLUMN_3}
    Should Be Equal As Integers                 ${selected}     1

    Refresh Devices Page
    Verify and Wait Until Device Online         ${DUT8_SERIAL}
    Verify and Wait Until Device Managed        ${DUT8_SERIAL}
    Verify Device Status Green                  ${DUT8_SERIAL}

Test 10: Onboard Sixth EXOS CoPilot Eligible Device and Verify Success
    [Documentation]     Onboards a fifth EXOS CoPilot eligible device and verifies success
    [Tags]              tccs-15118    copilot_filter_testing    copilot_license_testing    xiq-16248   development    xiq    copilot    test10

    Depends On Test     Test 1: Verify Pilot and CoPilot Baseline License Counts

    # Downgrade the device's iqagent if needed
    ${SPAWN_CONNECTION}=      Open Spawn        ${DUT9_IP}   ${DUT9_PORT}   ${DUT9_USERNAME}   ${DUT9_PASSWORD}   ${DUT9_CLI_TYPE}
    ${DOWNGRADE_IQAGENT}=     Downgrade Iqagent              ${DUT9_CLI_TYPE}        ${SPAWN_CONNECTION}
    Should Be Equal As Integers      ${DOWNGRADE_IQAGENT}     1

    ${CONF_STATUS_RESULT}=    Configure Device To Connect To Cloud        ${DUT9_CLI_TYPE}    ${IQAGENT}   ${SPAWN_CONNECTION}    vr=${DUT9_VR}
    Should Be Equal As Strings       ${CONF_STATUS_RESULT}    1
    Close Spawn         ${SPAWN_CONNECTION}

    Onboard New Test Device                     ${DUT9_SERIAL}  ${netelem9}

    ${selected}=    Column Picker Select        ${COLUMN_1}     ${COLUMN_2}    ${COLUMN_3}
    Should Be Equal As Integers                 ${selected}     1

    Refresh Devices Page
    Verify and Wait Until Device Online         ${DUT9_SERIAL}
    Verify and Wait Until Device Managed        ${DUT9_SERIAL}
    Verify Device Status Green                  ${DUT9_SERIAL}

Test 11: Onboard Non-CoPilot Eligible Digital Twin Device and Verify Success
    [Documentation]     Onboards a non-CoPilot Digital Twin eligible device and verifies success
    [Tags]              tccs-15118    copilot_filter_testing    copilot_license_testing    xiq-16248   development    xiq    copilot    test11

    Depends On Test     Test 1: Verify Pilot and CoPilot Baseline License Counts

    ${ONBOARD_RESULT}=      onboard device quick            ${netelem10}
    Should Be Equal As Strings                              ${ONBOARD_RESULT}     1

    ${dt_serial}=           set variable                    ${${netelem10.name}.serial}
    Set Suite Variable                                      ${DT_SERIAL}    ${dt_serial}

    Verify and Wait Until Device Online                     ${DT_SERIAL}
    Verify and Wait Until Device Managed                    ${DT_SERIAL}
    Verify Device Status Green                              ${DT_SERIAL}

Test 12: Verify CoPilot Eligible Device Consumes Pilot And CoPilot Licenses Within Global Settings License Management
    [Documentation]     Confirms the license counts for Pilot and CoPilot within Global Settings->License Management
    [Tags]              tccs-15118    copilot_filter_testing    copilot_license_testing    xiq-16248   development    xiq    copilot    test12

    Depends On Test     Test 1: Verify Pilot and CoPilot Baseline License Counts

    Confirm Entitlement Counts for Feature Matches Expected     ${PILOT_ENTITLEMENT}       3     7    10
    Confirm Entitlement Counts for Feature Matches Expected     ${COPILOT_ENTITLEMENT}     0     2     2

Test 13: Verify Device License and CoPilot Column Values On All Devices
    [Documentation]     Confirms the Device License and CoPilot column values to verify devices consumed the appropriate license or not
    [Tags]              tccs-15118    copilot_filter_testing    copilot_license_testing    xiq-16248   development    xiq    copilot    test13

    Depends On Test     Test 1: Verify Pilot and CoPilot Baseline License Counts

    # Confirm the device row shows the correct pilot license status
    ${pilot1_result}=      Get Device Details    ${DUT1_SERIAL}    DEVICE LICENSE
    Should Contain         ${pilot1_result}      ${PILOT_LICENSE}

    # Confirm the device row shows the correct copilot license status
    Log To Console      CHECKING VALUES FOR DUT1
    ${copilot1_result}=    Get Device Details    ${DUT1_SERIAL}    COPILOT
    Should Contain         ${copilot1_result}    ${COPILOT_ACTIVE}

    Log To Console      CHECKING VALUES FOR DUT2
    ${pilot2_result}=      Get Device Details    ${DUT2_SERIAL}    DEVICE LICENSE
    Should Contain         ${pilot2_result}      ${PILOT_LICENSE}

    ${copilot2_result}=    Get Device Details    ${DUT2_SERIAL}    COPILOT
    Should Contain         ${copilot2_result}    ${COPILOT_ACTIVE}

    Log To Console      CHECKING VALUES FOR DUT3
    ${copilot3_result}=    Get Device Details    ${DUT3_SERIAL}    COPILOT
    Should Contain         ${copilot3_result}    ${COPILOT_NONE}

    Log To Console      CHECKING VALUES FOR DUT4
    ${copilot4_result}=    Get Device Details    ${DUT4_SERIAL}    COPILOT
    Should Contain         ${copilot4_result}    ${COPILOT_NONE}

    Log To Console      CHECKING VALUES FOR DUT5
    ${pilot5_result}=      Get Device Details    ${DUT5_SERIAL}    DEVICE LICENSE
    Should Contain         ${pilot5_result}      ${PILOT_LICENSE}

    ${copilot5_result}=    Get Device Details    ${DUT5_SERIAL}    COPILOT
    Should Contain         ${copilot5_result}    ${COPILOT_NONE}

    Log To Console      CHECKING VALUES FOR DUT6
    ${pilot6_result}=      Get Device Details    ${DUT6_SERIAL}    DEVICE LICENSE
    Should Contain         ${pilot6_result}      ${PILOT_LICENSE}

    ${copilot6_result}=    Get Device Details    ${DUT6_SERIAL}    COPILOT
    Should Contain         ${copilot6_result}    ${COPILOT_NONE}

    Log To Console      CHECKING VALUES FOR DUT7
    ${pilot7_result}=      Get Device Details    ${DUT7_SERIAL}    DEVICE LICENSE
    Should Contain         ${pilot7_result}      ${PILOT_LICENSE}

    ${copilot7_result}=    Get Device Details    ${DUT7_SERIAL}    COPILOT
    Should Contain         ${copilot7_result}    ${COPILOT_NONE}

    Log To Console      CHECKING VALUES FOR DUT8
    ${pilot8_result}=      Get Device Details    ${DUT8_SERIAL}    DEVICE LICENSE
    Should Contain         ${pilot8_result}      ${PILOT_LICENSE}

    ${copilot8_result}=    Get Device Details    ${DUT8_SERIAL}    COPILOT
    Should Contain         ${copilot8_result}    ${COPILOT_NONE}

    Log To Console      CHECKING VALUES FOR DUT9
    ${pilot9_result}=      Get Device Details    ${DUT9_SERIAL}    DEVICE LICENSE
    Should Contain         ${pilot9_result}      ${PILOT_LICENSE}

    ${copilot9_result}=    Get Device Details    ${DUT9_SERIAL}    COPILOT
    Should Contain         ${copilot9_result}    ${COPILOT_NONE}

    Log To Console      CHECKING VALUES FOR DUT10
    ${pilot10_result}=      Get Device Details    ${DT_SERIAL}    DEVICE LICENSE
    Should Contain         ${pilot10_result}      ${NO_PILOT_LICENSE}

    ${copilot10_result}=    Get Device Details    ${DT_SERIAL}    COPILOT
    Should Contain         ${copilot10_result}    ${COPILOT_NONE}

Test 14: Filter For All CoPilot Eligible Devices and Verify Devices Present
    [Documentation]     Filters by the Device Product Type group 'All CoPilot Eligible Devices' to show devices that are CoPilot eligible
    [Tags]              tccs-15118    copilot_filter_testing    copilot_license_testing    xiq-16248   development    xiq    copilot    test14

    Depends On Test     Test 1: Verify Pilot and CoPilot Baseline License Counts

    Set Filter For All CoPilot Eligible Devices

    Log To Console      VERIFYING DUT1 IS PRESENT IN FILTER PANEL
    Confirm Device Serial Present in Filtered Devices Panel             ${DUT1_SERIAL}
    Log To Console      VERIFYING DUT2 IS PRESENT IN FILTER PANEL
    Confirm Device Serial Present in Filtered Devices Panel             ${DUT2_SERIAL}
    Log To Console      VERIFYING DUT3 IS PRESENT IN FILTER PANEL
    Confirm Device Serial Present in Filtered Devices Panel             ${DUT3_SERIAL}
    Log To Console      VERIFYING DUT4 IS PRESENT IN FILTER PANEL
    Confirm Device Serial Present in Filtered Devices Panel             ${DUT4_SERIAL}
    Log To Console      VERIFYING DUT5 IS PRESENT IN FILTER PANEL
    Confirm Device Serial Present in Filtered Devices Panel             ${DUT5_SERIAL}
    Log To Console      VERIFYING DUT6 IS PRESENT IN FILTER PANEL
    Confirm Device Serial Present in Filtered Devices Panel             ${DUT6_SERIAL}
    Log To Console      VERIFYING DUT7 IS PRESENT IN FILTER PANEL
    Confirm Device Serial Present in Filtered Devices Panel             ${DUT7_SERIAL}
    Log To Console      VERIFYING DUT8 IS PRESENT IN FILTER PANEL
    Confirm Device Serial Present in Filtered Devices Panel             ${DUT8_SERIAL}
    Log To Console      VERIFYING DUT9 IS PRESENT IN FILTER PANEL
    Confirm Device Serial Present in Filtered Devices Panel             ${DUT9_SERIAL}
    Log To Console      VERIFYING DUT10 IS NOT PRESENT IN FILTER PANEL
    Confirm Device Serial Not Present in Filtered Devices Panel         ${DT_SERIAL}

Test 15: Clear Filter For All CoPilot Eligible Devices and Verify Devices Present
    [Documentation]     Clears filters by the Device Product Type group 'All CoPilot Eligible Devices' to show all onboarded devices
    [Tags]              tccs-15118    copilot_filter_testing    copilot_license_testing    xiq-16248   development    xiq    copilot    test15

    Depends On Test     Test 1: Verify Pilot and CoPilot Baseline License Counts

    Clear Filter For All CoPilot Eligible Devices

    Log To Console      VERIFYING DUT1 IS PRESENT IN FILTER PANEL
    Confirm Device Serial Present in Filtered Devices Panel             ${DUT1_SERIAL}
    Log To Console      VERIFYING DUT2 IS PRESENT IN FILTER PANEL
    Confirm Device Serial Present in Filtered Devices Panel             ${DUT2_SERIAL}
    Log To Console      VERIFYING DUT3 IS PRESENT IN FILTER PANEL
    Confirm Device Serial Present in Filtered Devices Panel             ${DUT3_SERIAL}
    Log To Console      VERIFYING DUT4 IS PRESENT IN FILTER PANEL
    Confirm Device Serial Present in Filtered Devices Panel             ${DUT4_SERIAL}
    Log To Console      VERIFYING DUT5 IS PRESENT IN FILTER PANEL
    Confirm Device Serial Present in Filtered Devices Panel             ${DUT5_SERIAL}
    Log To Console      VERIFYING DUT6 IS PRESENT IN FILTER PANEL
    Confirm Device Serial Present in Filtered Devices Panel             ${DUT6_SERIAL}
    Log To Console      VERIFYING DUT7 IS PRESENT IN FILTER PANEL
    Confirm Device Serial Present in Filtered Devices Panel             ${DUT7_SERIAL}
    Log To Console      VERIFYING DUT8 IS PRESENT IN FILTER PANEL
    Confirm Device Serial Present in Filtered Devices Panel             ${DUT8_SERIAL}
    Log To Console      VERIFYING DUT9 IS PRESENT IN FILTER PANEL
    Confirm Device Serial Present in Filtered Devices Panel             ${DUT9_SERIAL}
    Log To Console      VERIFYING DUT10 IS PRESENT IN FILTER PANEL
    Confirm Device Serial Present in Filtered Devices Panel             ${DT_SERIAL}

Test 16: Delete All Devices and Verify Success
    [Documentation]     Deletes all devices and verifies success
    [Tags]              tccs-15118    copilot_sanity_testing    copilot_license_testing    xiq-16248    development    xiq    copilot    test16

    Depends On Test     Test 1: Verify Pilot and CoPilot Baseline License Counts

    Delete All devices and Confirm Success

Test 17: Verify All Pilot and CoPilot Licenses Revoked Within Global Settings License Management
    [Documentation]     Confirms the license counts for Pilot and CoPilot within Global Settings->License Management
    [Tags]              tccs-15118    copilot_release_testing    copilot_license_testing    xiq-16248    development    xiq    copilot    test17

    Depends On Test     Test 1: Verify Pilot and CoPilot Baseline License Counts

    Confirm Entitlement Counts for Feature Matches Expected     ${PILOT_ENTITLEMENT}      10    0   10
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
    Clear All Filters
    Delete All devices and Confirm Success
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
    [Documentation]     Filters by the Device Product Type group - All CoPilot Eligible Devices

    Clear All Filters
    ${filter_result}=  Set Device Product Type Filter    All CoPilot Eligible Devices    true
    Should Be Equal As Integers                      ${filter_result}  1
    Apply Filters

Clear Filter For All CoPilot Eligible Devices
    [Documentation]     Clears the filter for Device Product Type group - All CoPilot Eligible Devices

    Clear All Filters
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
