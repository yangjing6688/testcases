# Author        : Barbara Sochor
# Date          : April 8th 2022
# Description   : XIQ-1128 AP5010 Basic Device Support - Network 360
# Only Devices onboarded by this automamation script can be in the location under test.
#
# Topology:
# Host ----- AIO
#
#  To run using topo and environment:
#  ----------------------------------
#  robot -v TOPO:topology.yaml -v ENV:environment.yaml -v TESTBED:SJ/FT_testbed1.yaml -i xim_tc_18725 XIQ-1128.robot
#
#
#  ---------------------
#  This file contains test cases.
#
#  Test Cases:
#  Test1 - TCXM-18636: N360M_DeviceScoring_DeviceAvailabilityScore_100_1
#              Verifies that N360M_DEVICES_DeviceAvailabilityScore is 100.
#  Test2 - TCXM-18674 - N360M_DeviceScoring_DeviceHardwareHealthScore_100_1
#              Verifies that N360M_DEVICES_DeviceHardwareHealthScore is 100.
# Test3 - TCXM-18644 - N360M_DeviceScoring_Config&FirmwareScore_80_1
#              Verifies that N360M_DEVICES_Config&FirmwareScore is 80.
# Test4 - TCXM-18725: N360M_Client_Count_1_1
#              Verifies that N360M_CLIENTS_CLIENTS count is 1 5GHz client.
########################################################################################################################

*** Variables ***
${AVAILABILITY_SCORE}       100
${EXPECTED_HW_HEALTH}       100
${EXPECTED_FW_HEALTH}       80
${FLOOR_NAME}               floor_04
${CONFIG_PUSH_SSID_01}      SSID_01
${CONFIG_PUSH_SSID_02}      SSID_02
${SSID_01}                  ylbyukugfz

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
Library     common/ImageAnalysis.py
Library     xiq/flows/globalsettings/GlobalSetting.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/configure/ExpressNetworkPolicies.py
Library     xiq/flows/configure/CommonObjects.py
Library     extauto/common/Cli.py
Library     extauto/common/TestFlow.py
Library     extauto/xiq/flows/common/Login.py
Library     extauto/xiq/flows/common/Navigator.py
Library     extauto/xiq/flows/manage/Client.py
Library     extauto/common/tools/remote/WinMuConnect.py

Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    TestBeds/${TESTBED}
Variables    Environments/Config/device_commands.yaml
Variables    Environments/Config/waits.yaml
Variables    Tests/Robot/Functional/XIQ/Wireless/Network360Monitor/Resources/n360waits.yaml

Resource     Tests/Robot/Functional/XIQ/Wireless/Network360Monitor/Resources/wireless_networks_config.robot

Library	        Remote 	http://${mu1.ip}:${mu1.port}   WITH NAME   Remote_Server

Force Tags   testbed_1_node
Suite Setup    Cleanup

*** Test Cases ***
Test1 - TCXM-18636 - N360M_DeviceScoring_DeviceAvailabilityScore_100_1
    [Documentation]   Correctness of N360M Device Availability Score is verified.
#                     Assumption is that there is only 1 Device (added by this script) listed in XIQ, in this location.
    [Tags]            xim_tc_18636    development
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${result1}=             Login User          ${tenant_username}    ${tenant_password}
    should be equal as integers                 ${result1}            1
    ${onboard_result}=      Onboard Device      ${ap1.serial}         ${ap1.make}       location=${ap1.location}      device_os=${ap1.os}
    ${search_result}=       Search AP Serial    ${ap1.serial}
    should be equal as integers                 ${onboard_result}     1
    should be equal as integers                 ${search_result}      1
    ${AP_SPAWN}=            Open Spawn          ${ap1.ip}     ${ap1.port}     ${ap1.username}     ${ap1.password}     ${ap1.platform}
    ${OUTPUT0}=             Send Commands       ${AP_SPAWN}           capwap client server name ${CAPWAP_URL}, capwap client default-server-name ${CAPWAP_URL}, capwap client server backup name ${CAPWAP_URL}, no capwap client enable, capwap client enable, save config
    ${OUTPUT0}=             Send                ${AP_SPAWN}           ${CMD_CONSOLE_PAGE_0}
    ${OUTPUT0}=             Send                ${AP_SPAWN}           ${CMD_SHOW_VERSION_DETAIL}
    ${OUTPUT0}=             Send                ${AP_SPAWN}           ${CMD_SHOW_CAPWAP_CLIENT}
    ${OUTPUT1}=             Send                ${AP_SPAWN}           ${CMD_CAPWAP_HM_PRIMARY_NAME}
    ${OUTPUT2}=             Send                ${AP_SPAWN}           ${CMD_CAPWAP_SERVER_IP}
    ${OUTPUT3}=             Wait For CLI Output                       ${AP_SPAWN}         ${CMD_CAPWAP_CLIENT_STATE}          ${OUTPUT_CAPWAP_STATUS}
    Close Spawn             ${AP_SPAWN}
    Should Be Equal as Integers                 ${OUTPUT3}            1
    sleep     ${ap_reporting_time}
    ${availability}     ${hw_health}     ${fw_health}=                Get Network360monitor Device Health Overall Score     ${FLOOR_NAME}
    Log to Console          DeviceAvailabilityScore ${availability}
    Should Be Equal As Integers                 ${availability}       ${AVAILABILITY_SCORE}

Test2 - TCXM-18674 - N360M_DeviceScoring_DeviceHardwareHealthScore_100_1
    [Documentation]   Correctness of N360M Device Hardware Health Score is verified.
#                     Assumption is that:
#                     there is only 1 Device listed in XIQ, in this location.
#                     "TCXM-18636: N360M_DeviceScoring_DeviceAvailabilityScore_100_1" was executed and Device was onboarded
    [Tags]            xim_tc_18674    development
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser
    Depends On          Test1
    ${result1}=         Login User    ${tenant_username}    ${tenant_password}
    should be equal as integers       ${result1}            1
    sleep     ${ap_reporting_time}
    ${availability}   ${hw_health}    ${fw_health}=         Get Network360monitor Device Health Overall Score     ${FLOOR_NAME}
    Log to Console                    DeviceHardwareHealthScore ${hw_health}
    Should Be Equal As Integers       ${hw_health}          ${EXPECTED_HW_HEALTH}


Test3 - TCXM-18644 - N360M_DeviceScoring_Config&FirmwareScore_80_1
    [Documentation]   Correctness of N360M Device Hardware Health Score is verified.
#                     Assumption is that:
#                     there is only 1 Device listed in XIQ, in this location.
#                     "TCXM-18636: N360M_DeviceScoring_DeviceAvailabilityScore_100_1" was executed and Device was onboarded
    [Tags]            xim_tc_18644    development
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser
    Depends On          Test2

    ${LOGIN_STATUS}=        Login User        ${tenant_username}      ${tenant_password}
    should be equal as integers               ${LOGIN_STATUS}         1
    ${LATEST_VERSION}=      Upgrade Device To Latest Version          ${ap1.serial}
    Sleep                   ${browser_load_wait}

    Wait Until Device Reboots                 ${ap1.serial}

    ${POLICY_01}=             Get Random String
    ${SSID_01}=               Get Random String
    ${NEW_SSID_NAME_1}=       Get Random String

    Set Suite Variable        ${POLICY_01}
    Set Suite Variable        ${SSID_01}
    Set To Dictionary         ${CONFIG_PUSH_OPEN_NW_01}    ssid_name=${SSID_01}
    Log to Console            ${CONFIG_PUSH_OPEN_NW_01}

    ${POLICY_STATUS}=         Create Network Policy   policy=config_push_${POLICY_01}      &{CONFIG_PUSH_OPEN_NW_01}
    ${DEPLOY_STATUS}=         Deploy Network Policy with Complete Update      config_push_${POLICY_01}          ${ap1.serial}
    Log to Console            POLICY_STATUS ${POLICY_STATUS}
    Log to Console            DeployStatus ${DEPLOY_STATUS}
    should be equal as integers   ${POLICY_STATUS}    1
    should be equal as integers   ${DEPLOY_STATUS}    1
    Wait Until Device Online  ${ap1.serial}  None  30  20

    Sleep                     ${browser_load_wait}
    ${AP_SPAWN1}=             Open Spawn        ${ap1.ip}   ${ap1.port}   ${ap1.username}   ${ap1.password}   ${ap1.platform}
    ${OUTPUT_SSID}=           Send              ${AP_SPAWN1}        show ssid
    ${AP_BUILD_VERSION}=      Get AP Version    ${AP_SPAWN1}
    Close Spawn               ${AP_SPAWN1}

    Log to Console            show_ssid ${OUTPUT_SSID}
    Should Contain            ${OUTPUT_SSID}    ${SSID_01}
    Log to Console            AP_BUILD_VERSN    ${AP_BUILD_VERSION}
    Should Be Equal As Strings  ${LATEST_VERSION}   ${AP_BUILD_VERSION}

    ${EDIT_STATUS}=           Edit Network Policy SSID    config_push_${POLICY_01}    ${SSID_01}    ${NEW_SSID_NAME_1}
    sleep                     ${ap_reporting_time}
    ${availability}     ${hw_health}     ${fw_health}=    Get Network360monitor Device Health Overall Score   ${FLOOR_NAME}
    Log to Console            DeviceHardwareHealthScore ${fw_health}
    Should Be Equal As Integers          ${fw_health}   ${EXPECTED_FW_HEALTH}


Test4 - TCXM-18725: N360M_Client_Count_1_1
    [Documentation]   Correctness of Client count (one 5GHz Client) is verified in N360M Client Health, CLIENTS widget.
#                     Assumption is that there is only one Client connected.
    [Tags]              xim_tc_18725    development
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser
    Depends On          Test3

    ${result1}=           Login User     ${tenant_username}    ${tenant_password}
    ${CONNECT_STATUS}=    Remote_Server.Connect Open Network    ${SSID_01}
    should be equal as strings          '${CONNECT_STATUS}'    '1'
    Log to Console        Sleep for ${client_connect_wait}
    sleep                 ${client_connect_wait}

    ${CLIENT_CONNECT}=    Get Client Status   client_mac=${mu1.wifi_mac}
    Should Be Equal As Strings          '${CLIENT_CONNECT}'      '1'
    sleep                 ${ap_reporting_time}
    ${client_count_2G}     ${client_count_5G}     ${client_count_6G}=       Get Network360monitor Clients Health Client Count   ${FLOOR_NAME}
    Log to Console        clientCount2G ${client_count_2G}
    Log to Console        clientCount5G ${client_count_5G}
    Log to Console        clientCount6G ${client_count_6G}
    Should Be Equal As Strings          '${client_count_2G}'     '0 (0%)'
    Should Be Equal As Strings          '${client_count_5G}'     '1 (100%)'
    Should Be Equal As Strings          '${client_count_6G}'     '0 (0%)'

*** Keywords ***
Cleanup
    Login User      ${tenant_username}      ${tenant_password}
    delete all aps
    delete_all_ssids
    delete all network policies
    Logout User
    Sleep   10
    Quit Browser
