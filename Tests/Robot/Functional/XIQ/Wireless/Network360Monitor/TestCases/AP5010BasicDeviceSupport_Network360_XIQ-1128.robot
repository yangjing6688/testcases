# Author        : Barbara Sochor
# Date          : April 8th 2022
# Description   : XIQ-1128 AP5010 Basic Device Support - Network 360
# Only Devices onboarded by this automamation script can be in the location under test.
#
# Topology      :
# Host ----- AIO
#
#  To run using topo and environment:
#  ----------------------------------
#  robot -v TOPO:topology.yaml -v ENV:environment.yaml -v TESTBED:testbed.yaml XIQ-1128.robot
#
#
#  ---------------------
#  This file contains test cases.
#
#  Test Cases:
#  TCXM-18636: N360M_DeviceScoring_DeviceAvailabilityScore_100_1
#              Verifies that N360M_DEVICES_DeviceAvailabilityScore is 100.
#  TCXM-18674 - N360M_DeviceScoring_DeviceHardwareHealthScore_100_1
#              Verifies that N360M_DEVICES_DeviceHardwareHealthScore is 100.
# TCXM-18644 - N360M_DeviceScoring_Config&FirmwareScore_80_1
#              Verifies that N360M_DEVICES_Config&FirmwareScore is 80.
########################################################################################################################

*** Variables ***
${AVAILABILITY_SCORE}       100
${EXPECTED_HW_HEALTH}       100
${EXPECTED_FW_HEALTH}       80
${SLEEP_TIME}               240s
${FLOOR_NAME}               Floor1
${CONFIG_PUSH_SSID_01}      SSID_01
${CONFIG_PUSH_SSID_02}      SSID_02
${RETRY_DURATION}           40
${RETRY_COUNT}              20
${MAX_CONFIG_PUSH_TIME}     100

*** Settings ***
# import libraries
Library     Collections
Library     xiq/flows/common/Login.py
Library     common/Utils.py
Library     common/Screen.py
Library     common/ImageHandler.py
Library     common/ScreenDiff.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/mlinsights/Network360Monitor.py
Library     common/Mu.py
Library     common/ImageAnalysis.py
Library     xiq/flows/globalsettings/GlobalSetting.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/configure/ExpressNetworkPolicies.py
Library     extauto/common/Cli.py
Library     extauto/common/TestFlow.py
Library     extauto/xiq/flows/common/Login.py
Library     extauto/xiq/flows/common/Navigator.py
Library     extauto/xiq/flows/manage/Client.py

Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    TestBeds/SJ/${TESTBED}
Variables    Environments/Config/device_commands.yaml
Resource     Tests/Robot/Functional/XIQ/Wireless/Network360Monitor/Resources/wireless_networks_config.robot

Force Tags   testbed_1_node

*** Test Cases ***
Test1 - TCXM-18636 - N360M_DeviceScoring_DeviceAvailabilityScore_100_1
    [Documentation]   Correctness of N360M Device Availability Score is verified.
#                     Assumption is that there is only 1 Device (added by this script) listed in XIQ, in this location.
    [Tags]            xiq_tc_18636    development
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${result1}=             Login User          ${tenant_username}      ${tenant_password}
    should be equal as integers                 ${result1}            1
    Delete AP               ap_serial=${ap1.serial}
    ${onboard_result}=      Onboard Device      ${ap1.serial}         ${ap1.make}       location=${ap1.location}      device_os=${ap1.os}
    ${search_result}=       Search AP Serial    ${ap1.serial}
    should be equal as integers                 ${onboard_result}     1
    should be equal as integers                 ${search_result}      1
    ${AP_SPAWN}=            Open Spawn          ${ap1.console_ip}     ${ap1.console_port}     ${ap1.username}     ${ap1.password}     ${ap1.platform}
    ${OUTPUT0}=             Send Commands       ${AP_SPAWN}           capwap client server name ${CAPWAP_URL}, capwap client default-server-name ${CAPWAP_URL}, capwap client server backup name ${CAPWAP_URL}, no capwap client enable, capwap client enable, save config
    ${OUTPUT0}=             Send                ${AP_SPAWN}           ${CMD_CONSOLE_PAGE_0}
    ${OUTPUT0}=             Send                ${AP_SPAWN}           ${CMD_SHOW_VERSION_DETAIL}
    ${OUTPUT0}=             Send                ${AP_SPAWN}           ${CMD_SHOW_CAPWAP_CLIENT}
    ${OUTPUT1}=             Send                ${AP_SPAWN}           ${CMD_CAPWAP_HM_PRIMARY_NAME}
    ${OUTPUT2}=             Send                ${AP_SPAWN}           ${CMD_CAPWAP_SERVER_IP}
    ${OUTPUT3}=             Wait For CLI Output                       ${AP_SPAWN}         ${CMD_CAPWAP_CLIENT_STATE}          ${OUTPUT_CAPWAP_STATUS}
    Close Spawn             ${AP_SPAWN}
    Should Be Equal as Integers                 ${OUTPUT3}            1
    sleep     ${SLEEP_TIME}
    ${availability}     ${hw_health}     ${fw_health}=                Get Network360monitor Device Health Overall Score     ${FLOOR_NAME}
    Log to Console          DeviceAvailabilityScore ${availability}
    Should Be Equal As Integers                 ${availability}       ${AVAILABILITY_SCORE}

Test2 - TCXM-18674 - N360M_DeviceScoring_DeviceHardwareHealthScore_100_1
    [Documentation]   Correctness of N360M Device Hardware Health Score is verified.
#                     Assumption is that:
#                     there is only 1 Device listed in XIQ, in this location.
#                     "TCXM-18636: N360M_DeviceScoring_DeviceAvailabilityScore_100_1" was executed and Device was onboarded
    [Tags]            xiq_tc_18674    development
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser
    Depends On          Test1
    ${result1}=         Login User    ${tenant_username}    ${tenant_password}
    should be equal as integers       ${result1}            1
    ${availability}   ${hw_health}    ${fw_health}=         Get Network360monitor Device Health Overall Score     ${FLOOR_NAME}
    Log to Console                    DeviceHardwareHealthScore ${hw_health}
    Should Be Equal As Integers       ${hw_health}          ${EXPECTED_HW_HEALTH}


Test3 - TCXM-18644 - N360M_DeviceScoring_Config&FirmwareScore_80_1
    [Documentation]   Correctness of N360M Device Hardware Health Score is verified.
#                     Assumption is that:
#                     there is only 1 Device listed in XIQ, in this location.
#                     "TCXM-18636: N360M_DeviceScoring_DeviceAvailabilityScore_100_1" was executed and Device was onboarded
    [Tags]            xiq_tc_18644    development
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser
    Depends On          Test2

    ${LOGIN_STATUS}=        Login User        ${tenant_username}      ${tenant_password}
    should be equal as integers               ${LOGIN_STATUS}         1
    ${LATEST_VERSION}=      Upgrade Device To Latest Version          ${ap1.serial}
    Sleep                   30                          Sleep 30 Seconds

    Wait Until Device Reboots                 ${ap1.serial}

    ${SPAWN1}=             Open Spawn        ${ap1.console_ip}   ${ap1.console_port}      ${ap1.username}       ${ap1.password}        ${ap1.platform}
    ${CLOCK_OUTPUT}=       Send              ${SPAWN1}         show clock
    ${REBOOT_OUTPUT}=      Send              ${SPAWN1}         show reboot schedule
    ${VERSION_DETAIL}=     Send              ${SPAWN1}         show version detail
    ${AP_BUILD_VERSION}=   Get AP Version    ${SPAWN1}
    Log to Console         AP_BUILD_VERSN2   ${AP_BUILD_VERSION}

    Should Not Contain      ${REBOOT_OUTPUT}    Next reboot Scheduled
    Should Contain          ${VERSION_DETAIL}   Running image:      Current version
    Should Contain          ${VERSION_DETAIL}   Load after reboot:  Current version
    Should Contain          ${VERSION_DETAIL}   Uptime:             0 weeks, 0 days, 0 hours

    Should Be Equal As Strings  ${LATEST_VERSION}           ${AP_BUILD_VERSION}

    ${POLICY_01}=             Get Random String
    ${SSID_01}=               Get Random String
    ${NEW_SSID_NAME_1}=       Get Random String

    Set Suite Variable        ${POLICY_01}
    Set Suite Variable        ${SSID_01}
    Set To Dictionary         ${CONFIG_PUSH_OPEN_NW_01}    ssid_name=${SSID_01}
    Log to Console            ${CONFIG_PUSH_OPEN_NW_01}

    ${POLICY_STATUS}=         Create Network Policy   policy=config_push_${POLICY_01}      &{CONFIG_PUSH_OPEN_NW_01}

    ${DEPLOY_STATUS}=         Deploy Network Policy with Complete Update      config_push_${POLICY_01}          ${ap1.serial}
    Log to Console            DeployStatus ${DEPLOY_STATUS}
    Wait Until Device Online   ${ap1.serial}  None   30   20
    Close Spawn               ${SPAWN1}
    ${SPAWN}=                 Open Spawn      ${ap1.console_ip}   ${ap1.console_port}      ${ap1.username}       ${ap1.password}        ${ap1.platform}
    ${OUTPUT1}=               Send            ${SPAWN}            show ssid
    Close Spawn               ${SPAWN}
    Log to Console            POLICY_STATUS ${POLICY_STATUS}
    Log to Console            DEPLOY_STATUS ${DEPLOY_STATUS}
    should be equal as integers             ${POLICY_STATUS}            1
    should be equal as integers             ${DEPLOY_STATUS}            1
    Log to Console            show_ssid ${OUTPUT1}
    Should Contain            ${OUTPUT1}    ${SSID_01}
    ${EDIT_STATUS}=           Edit Network Policy SSID    config_push_${POLICY_01}    ${SSID_01}    ${NEW_SSID_NAME_1}
    sleep               ${SLEEP_TIME}
    ${availability}     ${hw_health}     ${fw_health}=    Get Network360monitor Device Health Overall Score   ${FLOOR_NAME}
    Log to Console      DeviceHardwareHealthScore ${fw_health}
    Should Be Equal As Integers           ${fw_health}       ${EXPECTED_FW_HEALTH}


Tes7: Cleanup
    [Tags]			        cleanup         test7
    ${LOGIN_STATUS}=    Login User    ${tenant_username}    ${tenant_password}
    Delete Device       device_serial=${ap1.serial}
    [Teardown]    Quit Browser