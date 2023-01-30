# Author        : Shilpa Hiremath
# Date          : Jun 6th 2022
# Description   : Manage Device Test Cases

# Topology      :
#Host ----- Cloud
#
#  To run using topo and environment:
#  ----------------------------------
#   robot -v TESTBED:/BANGALORE/Prod/wireless/xiq_blr_tb_sh_AP5010.yaml -v TOPO:topo.prod.g2r1.shilpa.yaml  -v ENV:environment.remote.win10.sh.chrome.yaml XIQ-999_AP5010_manage_device.robo
#
#
#  ---------------------
#  This file contains test cases.
#
#  Test Cases:
#  TC1 : TCXM-19404 : Verify filter option for AP5010U/AP5010
#              Left filter panel verification for AP5010U/AP5010
#  TCXM-19407 : verify location assign for AP5010U/AP5010 from manage device - hyperlink and from actions
#                 verify location assign for AP5010U/AP5010 from manage device - hyperlink and from actions
#TCXM-19408 : verify upgrade device - single and multiple AP5010U/AP5010
#            verify upgrade device - single and multiple AP5010U/AP5010 from manage device
#TCXM-19416 : verify actions - advanced - cli access for AP5010U/AP5010 from manage device
#            verify actions - advanced - cli access for AP5010U/AP5010 from manage device
#TCXM-19418 : verify actions - reboot for AP5010U/AP5010 from manage device
#             verify actions - reboot for AP5010U/AP5010 from manage device
#TCXM-19418 : Verify connection status with AP5010U/AP5010
#            AP5010U/AP5010 online and offline connection status check.
#TCXM-19418 : Check if all columns populate data in manage-device page grid
#            Check all columns populate data in manage-device page grid
########################################################################################################################
*** Variables ***
${EXIT_LEVEL}                  test_suite
${RECORD}                      True
${NTP_STATE_COLUMN}            NTP STATE
${AP1_NETWORK_POLICY}          Test_Policy
${POWER_VALUE}                 1
${CHANNEL_INPUT}               39
${RADIO_PROFILE_NAME}          radio_ng_11ax-6g
${model1}                      AP5010U
${model2}                      AP460C
${cmd}                         show version
${BUILD_ID}                    HiveOS 10.5r1 build-272113
${NETWORK1}                         AP5010_TemplateCaseStarts
${NETWORK2}                         AP5010_TemplateCaseEnds
${SSID_01}                          AP5010_TemplateCaseStarts
${SSID_02}                          AP5010_TeplateCaseEnds
${OPEN_SSID_01}                     AP5010_Openssid
${OPEN_SSID_02}                     OpenTestSsid
${OPEN_SSID_03}                     OpenNewTestSsid
${OPEN_SSID_04}                     DeleteSsid
${OPEN_SSID_05}                     CFD-4347-SSID
${NW_POLICY_NAME}                   AP5010_OpenssidNW
### AP1#####
${AP1_NAME}                     ${ap1.name}
${AP1_MODEL}                    ${ap1.model}
${AP1_DEVICE_TEMPLATE}          ${ap1.template}
${AP1_SERIAL}                   ${ap1.serial}
${AP1_OS}                       Cloud IQ Engine
${AP1_MAC}                      ${ap1.mac}
${AP1_BSSID}
${AP1_NETWORK_POLICY}           Test_np
${AP1_USERNAME}                 ${ap1.username}
${AP1_PASSWORD}                 ${ap1.password}
${AP1_PLATFORM}                 ${ap1.platform}
${AP1_CONSOLE_IP}               ${ap1.console_ip}
${AP1_CONSOLE_PORT}             ${ap1.console_port}
${PORT_NUM}                     ${ap1.console_port}
${IP_ADDR}                      ${ap1.console_ip}
${AP1_IP}                       ${ap1.ip}
${AP1_NETWORK_POLICY}           test_np_ap_01
${AP1_COUNTRY}                  ${ap1.country}
${AP1_SSID}                     test_ssid_ap_01
${AP1_MAKE}                     ${ap1.make}
${VERSION}                      10.5r1
${AP1_Cli_Type}                 ${ap1.cli_type}

##### AP2 deatials ####
${AP2_NAME}                     bui-flo-0620
${AP2_MODEL}                    AP460C
${AP2_DEVICE_TEMPLATE}          AP_460C-default-template
${AP2_SERIAL}                   24602005230620
${AP2_OS}                       Cloud IQ Engine
${AP2_MAC}                      bcf31065a100
${AP2_BSSID}
${AP2_NETWORK_POLICY}           Test_np_01
${AP2_USERNAME}                 admin
${AP2_PASSWORD}                 Aerohive123
${AP2_PLATFORM}                 aerohive
${AP2_CONSOLE_IP}               10.234.107.230
${AP2_CONSOLE_PORT}             7016
${PORT_NUM}                     22
${IP_ADDR}                      10.234.107.186
${AP2_IP}                       14.14.14.187
${AP2_NETWORK_POLICY}           test_np_ap_02
${AP2_COUNTRY}                  United Kingdom
${AP2_SSID}                     test_ssid_ap_02
${AP2_MAKE}                     Extreme - Aerohive
${ap2_model}                    AP_460C
${AP2_NAME}                     ${ap2.name}
${AP2_MODEL}                    ${ap2.model}
${AP2_DEVICE_TEMPLATE}          ${ap2.template}
${AP2_SERIAL}                   ${ap2.serial}
${AP2_OS}                       Cloud IQ Engine
${AP2_MAC}                      ${ap2.mac}
${AP2_BSSID}
${AP2_NETWORK_POLICY}           Test_np
${AP2_USERNAME}                 ${ap2.username}
${AP2_PASSWORD}                 ${ap2.password}
${AP2_PLATFORM}                 ${ap2.platform}
${AP2_CONSOLE_IP}               ${ap2.console_ip}
${AP2_CONSOLE_PORT}             ${ap2.console_port}
${PORT_NUM}                     ${ap2.console_port}
${IP_ADDR}                      ${ap2.console_ip}
${AP2_IP}                       ${ap2.ip}
${AP2_NETWORK_POLICY}           test_np_ap_01
${AP2_COUNTRY}                  ${ap2.country}
${AP2_SSID}                     test_ssid_ap_01
${AP2_MAKE}                     ${ap2.make}
${AP2_Cli_Type}                 ${ap2.cli_type}
${LOCATION}             Extreme Networks,  Eco space, 3B,  floor-1
${LOCATION_HYPER}       Extreme Networks,  Bangalore, Eco space tower, F-1
${LOCATION_HYPER1}      Extreme Networks, Symbol Tower, 3B building, Floor-1

*** Settings ***
Library     Collections
Library     extauto/common/Cli.py
Library     common/Utils.py
Library     common/TestFlow.py
Library     xiq/flows/common/Login.py
Library     xiq/flows/common/Navigator.py
Library     xiq/flows/manage/Client.py
Library     xiq/flows/configure/CommonObjects.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/Device360.py
Library     xiq/flows/manage/DeviceCliAccess.py
Library     xiq/flows/manage/DeviceConfig.py
Library     xiq/flows/globalsettings/GlobalSetting.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/configure/ExpressNetworkPolicies.py
Library     xiq/elements/NetworkPolicyWebElements.py
Library     xiq/flows/manage/Location.py
Library     xiq/flows/manage/FilterManageDevices.py
Library     xiq/flows/a3/A3Inventory.py
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    TestBeds/${TESTBED}
Variables    Environments/Config/device_commands.yaml
Variables    Environments/Config/waits.yaml
Force Tags       testbed_2_node
Resource    testsuites/xiq/config/waits.robot
Resource    testsuites/xiq/config/device_commands.robot
Resource    testsuites/xiq/functional/device_template_config.robot
Resource    testsuites/xiq/functional/WPA3_secuirty_config.robot
Suite Setup     pre condition
#Suite Teardown   Test Suite Clean Up

*** Keywords ***
Pre Condition
    [Documentation]   AP Should be onboarded  without assigining the Network polciy  and it is online
    ${RESSULT}=                      Login User               ${TENANT_USERNAME}     ${TENANT_PASSWORD}
    ${AP_STATUS}=                   Get AP Status            ap_serial=${AP1_SERIAL}
    Should Be Equal As Strings     '${AP_STATUS}'           'green'

    [Teardown]   run keywords      logout user
    ...                            quit browser

Test Suite Clean Up
    [Documentation]         delete created network policies, SSID, Device etc
    [Tags]                  sanity    p2   p3  p4  production  regression
    Login User              ${TENANT_USERNAME}      ${TENANT_PASSWORD}
    Delete device           device_serial=${AP1_SERIAL}
#    Delete AP     ${AP2_SERIAL}
    Delete Network Policy      ${NW_POLICY_NAME}
    Logout User
    Quit Browser

*** Test Cases ***
TCXM-19406: verify policy assign for AP5010U/AP5010 from manage device from actions
    [Documentation]     verify policy assign for AP5010U/AP5010 from manage device -  from actions
    [Tags]              development         tcxm-19406      p-1
    ${RESULT}=          Login User       ${TENANT_USERNAME}      ${TENANT_PASSWORD}
    Should be Equal as integers     ${RESULT}       1

    ${POLICY_RESULT}=                Create Network Policy          ${NW_POLICY_NAME}       ${SSID_1}
    Should Be Equal As Strings      '${POLICY_RESULT}'   '1'

    ${AP1_UPDATE_CONFIG}=           Update Network Policy To AP     ${NW_POLICY_NAME}     ap_serial=${AP1_SERIAL}   update_method=Complete
    Should Be Equal As Strings      '${AP1_UPDATE_CONFIG}'       '1'

    Log to Console      Sleep for ${CONFIG_PUSH_WAIT}
    Sleep       ${CONFIG_PUSH_WAIT}
    [Teardown]   run keywords      logout user
    ...                            quit browser


TCXM-19404 : Verify filter option for AP5010U/AP5010
    [Documentation]     Left filter panel verification for AP5010U/AP5010
    [Tags]              development         tcxm-19404   p-2
    ${RESULT}=          Login User       ${TENANT_USERNAME}      ${TENANT_PASSWORD}
    Should be Equal as integers     ${RESULT}       1
    ${OUT_PUT1}=         filter hardware model          ${ap1.model}
    Should Contain     ${OUT_PUT1}          1
    Sleep       5

    [Teardown]   run keywords      logout user
    ...                            quit browser

TCXM-19408 : verify upgrade device - single and multiple AP5010U/AP5010
    [Documentation]         verify upgrade device - single and multiple AP5010U/AP5010 from manage device
    [Tags]              development         tcxm-19408
    ${RESULT}=          Login User       ${TENANT_USERNAME}      ${TENANT_PASSWORD}
    ${fw_version}=      upgrade device      ${ap1}
    Sleep               180s
    #${AP_SPAWN}=	Open Spawn  ${AP1_IP}  ${AP1_CONSOLE_PORT}   ${AP1_USERNAME}     ${AP1_PASSWORD}     ${AP1_PLATFORM}
    ${AP_SPAWN}=	Open Spawn      ${AP1_IP}   ${AP1_CONSOLE_PORT}   ${AP1_USERNAME}     ${AP1_PASSWORD}      ${AP1_Cli_Type}
    Set Suite Variable  ${AP_SPAWN}
    ${version_info}=    Send Commands       ${AP_SPAWN}      ${cmd}
    Close Spawn         ${AP_SPAWN}
    Should contain       ${version_info}       ${ap1.image}

      [Teardown]   run keywords      logout user
      ...                            quit browser

#TCXM-19407 : verify location assign for AP5010U/AP5010 from manage device - hyperlink and from actions
#    [Documentation]     verify location assign for AP5010U/AP5010 from manage device - hyperlink and from actions
#    [Tags]              TC         P1          Regression
#    ${RESULT}=          Login User       ${TENANT_USERNAME}      ${TENANT_PASSWORD}
#
#    ${ASSIGNED_LOC}=        assign_location_with_device_actions      ${AP1_SERIAL}       ${LOCATION_HYPER1}
#    Log to Console  ${ASSIGNED_LOC}
#    Should be Equal As Integers      ${ASSIGNED_LOC}     1
#
#    ${ASSIGNED_LOC}=     assign_location_with_hyperlink      ${AP1_SERIAL}        ${LOCATION_HYPER}
#    #${delta}=       update_network_policy_to_ap         ${NW_POLICY_NAME}     ap_serial=${AP1_SERIAL}        update_method="Delta"
#    ${delta}=       push_delta_config       ${AP1_SERIAL}       config_update_option=delta
##    deploy_network_policy_with_delta_update          ${NW_POLICY_NAME}           ${AP1_SERIAL}
#    Log to Console  ${ASSIGNED_LOC}
#    Should be Equal As Integers      ${ASSIGNED_LOC}     1
#    Should Be Equal As Strings      '${delta}'       '1'
#
#
#
#    [Teardown]      run keywords        Logout user
#    ...                                  quit browser


TCXM-19416 : verify actions - advanced - cli access for AP5010U/AP5010 from manage device
    [Documentation]         verify actions - advanced - cli access for AP5010U/AP5010 from manage device
    [Tags]              development         tcxm-19416      p-1
    ${RESULT}=          Login User       ${TENANT_USERNAME}      ${TENANT_PASSWORD}
    ${CMD_OUT}=         send_cmd_on_device_advanced_cli        ${AP1_SERIAL}         ${cmd}
    should contain      ${CMD_OUT}      Version
    #${CMD_OUT}=         send_cmd_on_device_advanced_cli        ${AP1_SERIAL}         ${cmd}
    #Should Contain      ${CMD_OUT}         Version:    ${BUILD_ID}
      [Teardown]   run keywords      logout user
      ...                            quit browser

TCXM-19418 : verify actions - reboot for AP5010U/AP5010 from manage device
    [Documentation]         verify actions - reboot for AP5010U/AP5010 from manage device
    [Tags]              development       tcxm-18636        p-1
    ${RESULT}=          Login User       ${TENANT_USERNAME}      ${TENANT_PASSWORD}
    ${reboot}=        reboot_ap        ${AP1_SERIAL}
    sleep         ${ap_reboot_wait}
    Should be Equal As Integers      ${reboot}      1
      [Teardown]   run keywords      logout user
      ...                            quit browser

TCXM-19411 : Verify connection status with AP5010U/AP5010
    [Documentation]         AP5010U/AP5010 online and offline connection status check.
    [Tags]             development    tcxm-19411            p-1
    ${RESULT}=          Login User       ${TENANT_USERNAME}      ${TENANT_PASSWORD}
    ${AP_STATUS}=                           Get AP Status       ap_serial=${AP1_SERIAL}
    should be equal as strings             '${AP_STATUS}'       'green'
      [Teardown]   run keywords      logout user
      ...                            quit browser





