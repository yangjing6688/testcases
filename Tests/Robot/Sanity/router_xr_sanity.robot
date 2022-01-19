# Author        : Ramkumar
# Date          : June 04th 2020
# Description   : XR Router Sanity Cases
#
# Topology      :
# XR Router ----- XIQ Cloud

# Execution Command:
# ------------------
# robot -L INFO -v DEVICE:XR200P -v TOPO:production  -v TEST_URL:https://extremecloudiq.com/ router_xr_sanity.robot
# robot -L INFO -v DEVICE:XR200P -v TOPO:production  -v TEST_URL:https://extremecloudiq.com/ -v CLEANUP_TAG:production router_xr_sanity.robot

*** Variables ***
${NW_POLICY_NAME}           test_automation_network_policy
${SSID_NAME}                Router_XR_template
${INTERFACE_NAME}           eth2
${CMD_SHOW_TRUNK_VLANS}     show interface ${INTERFACE_NAME} allowed-vlan
${EXPECTED_TRUNK_VLANS}     10-20
${CMD_SHOW_CONFIG}          show running-config
${PORT_TYPE_NAME}           test_trunk_xr
${SUB_NETWORK_NAME}         test_subnetwork
${VLAN_NAME}                test_router_vlan
${LOCATION}                  auto_location_01, Santa Clara, building_02, floor_04
${CLEANUP_TAG}              production

*** Settings ***
Library     common/Cli.py
Library     common/Utils.py
Library     common/TestFlow.py

Library     xiq/flows/common/Login.py

Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/AdvanceOnboarding.py

Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/configure/CommonObjects.py
Library     xiq/flows/configure/RouterTemplate.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml

Resource     router_xr_sanity_config.robot

Suite Setup     Cleanup-Delete Router   ${router1.serial}

*** Keywords ***
Cleanup-Delete Router
    [Arguments]             ${SERIAL}
    Login User              ${tenant_username}      ${tenant_password}
    Run Keyword If   '${CLEANUP_TAG}'=='production'  run keywords   Create Network Policy    default_network_policy     &{CONFIG_PUSH_OPEN_NW_01}
    ...     AND       Update Network Policy To Router   default_network_policy    router_serial=${router1.serial}
    ...     AND       Delete Device  device_serial=${router1.serial}
    ...     AND       Delete Network Policy  ${NW_POLICY_NAME}
    ...     AND       Delete SSID  ${SSID_NAME}
    ...     AND       Delete Router Template  default_network_policy  ${router1.device_template}
    ...     AND       Delete Sub Network Profile  ${SUB_NETWORK_NAME}
    ...     AND       Delete Port Type Profile    ${PORT_TYPE_NAME}
    ...     AND       Delete Vlan Profile   ${VLAN_NAME}
    Logout User
    Quit Browser

*** Test Cases ***
Test1: Onboard Aerohive XR Router Using Quick Add Method
    [Documentation]         Onboard Aerohive XR Router Using Quick Add Method
    [Tags]                  sanity   onboard  router  XR  P2  P3  P4  production  regression    Test1

    ${LOGIN_XIQ}=           Login User              ${tenant_username}      ${tenant_password}   capture_version=True
    Should Be Equal As Integers             ${LOGIN_XIQ}            1

    Delete Device  device_serial=${router1.serial}

    ${ONBOARD_RESULT}=      Onboard Device          ${router1.serial}         ${router1.make}       location=${LOCATION}
    Should Be Equal As Integers                     ${ONBOARD_RESULT}           1

    ${SEARCH_ROUTER}=       Search Device Serial    ${router1.serial}
    Should Be Equal As Integers             ${SEARCH_ROUTER}        1

    ${ROUTER_SPAWN}=        Open Spawn          ${router1.console_ip}   ${router1.console_port}      ${router1.username}       ${router1.password}        ${router1.platform}
    Set Suite Variable      ${ROUTER_SPAWN}
    ${CONFIG_CAPWAP}=       Send Commands           ${ROUTER_SPAWN}         capwap client server name ${capwap_url}, no capwap client enable, capwap client enable, save config

    ${OUTPUT}=              Send                ${ROUTER_SPAWN}         console page 0
    ${SHOW_VERSION}=        Send                ${ROUTER_SPAWN}         show version detail
    ${CAPWAP_CLIENT}=       Send                ${ROUTER_SPAWN}         show capwap client
    ${CHECK_CAPWAP}=        Send                ${ROUTER_SPAWN}         ${cmd_capwap_hm_primary_name}
    Should Contain                              ${CHECK_CAPWAP}         HiveManager Primary Name:
    ${CAPWAP_SERVER}=       Send                ${ROUTER_SPAWN}         ${cmd_capwap_server_ip}


    Wait Until Device Online    ${router1.serial}
    ${ROUTER_STATUS}=       Get Device Status       device_serial=${router1.serial}
    Should Be Equal As Strings             '${ROUTER_STATUS}'      'green'

    ${CAPWAP_STATUS}=       Send            ${ROUTER_SPAWN}         ${cmd_capwap_client_state}
    Should Contain                          ${CAPWAP_STATUS}        ${output_capwap_status}


    [Teardown]   run keywords       Logout User
    ...                             Quit Browser
                 Close Spawn        ${ROUTER_SPAWN}

test2: Onboard Aerohive XR Router Using Advance Onboarding Method
    [Documentation]         Onboard Aerohive XR Router Using Advance Onboarding Method
    [Tags]                  sanity   onboard  router  XR  P2  P3  P4  production   regression   test2

    ${LOGIN_XIQ}=           Login User          ${tenant_username}      ${tenant_password}
    Should Be Equal As Integers             ${LOGIN_XIQ}            1

    Delete Device  device_serial=${router1.serial}

    ${ONBOARD_ROUTER}=          Advance Onboard Device         ${router1.serial}    device_make=${router1.make}   dev_location=${LOCATION}
    Should Be Equal As Integers             ${ONBOARD_ROUTER}           1

    ${ROUTER_SPAWN}=        Open Spawn          ${router1.console_ip}   ${router1.console_port}      ${router1.username}       ${router1.password}        ${router1.platform}
    Set Suite Variable      ${ROUTER_SPAWN}
    ${CONFIG_CAPWAP}=       Send Commands       ${ROUTER_SPAWN}         capwap client server name ${capwap_url}, no capwap client enable, capwap client enable, save config

    ${OUTPUT}=              Send                ${ROUTER_SPAWN}         console page 0
    ${SHOW_VERSION}=        Send                ${ROUTER_SPAWN}         show version detail
    ${CAPWAP_CLIENT}=       Send                ${ROUTER_SPAWN}         show capwap client
    ${CHECK_CAPWAP}=        Send                ${ROUTER_SPAWN}         ${cmd_capwap_hm_primary_name}
    Should Contain                              ${CHECK_CAPWAP}         HiveManager Primary Name:
    ${CAPWAP_SERVER}=       Send                ${ROUTER_SPAWN}         ${cmd_capwap_server_ip}


    Wait Until Device Online    ${router1.serial}

    ${DEVICE_UPDATE_CONFIG}=    Update Network Policy To Router    policy_name=default_network_policy    router_serial=${router1.serial}
    Should Be Equal As Strings                      '${DEVICE_UPDATE_CONFIG}'       '1'
    Log to Console          Sleep for ${config_push_wait}
    sleep                   ${config_push_wait}

    ${ROUTER_STATUS}=       Get Device Status       device_serial=${router1.serial}
    Should Be Equal As Strings             '${ROUTER_STATUS}'      'green'

    ${CAPWAP_STATUS}=       Send            ${ROUTER_SPAWN}         ${cmd_capwap_client_state}
    Should Contain                          ${CAPWAP_STATUS}        ${output_capwap_status}


    [Teardown]   run keywords       Logout User
    ...                             Quit Browser
                 Close Spawn        ${ROUTER_SPAWN}

Test3: Create Router XR Template
    [Documentation]         Create Router XR Template
    [Tags]                  sanity    router-template  XR  P2  P3  P4   regression      Test3  production

    Depends On              Test2

    ${LOGIN_XIQ}=           Login User              ${tenant_username}      ${tenant_password}

    ${CREATE_NW_POLICY}=    Create Network Policy   ${NW_POLICY_NAME}       &{XR_ROUTER_NW_01}
    Should Be Equal As Strings                      '${CREATE_NW_POLICY}'   '1'

    ${CREATE_AP_TEMPLATE}=      Add Router Template     ${NW_POLICY_NAME}     &{ROUTER_TEMPLATE_CONFIG1}
    Should Be Equal As Strings   '${CREATE_AP_TEMPLATE}'   '1'

    ${DEVICE_UPDATE_CONFIG}=    Update Network Policy To Router    policy_name=${NW_POLICY_NAME}    router_serial=${router1.serial}
    Should Be Equal As Strings                      '${DEVICE_UPDATE_CONFIG}'       '1'
    Log to Console          Sleep for ${config_push_wait}
    sleep                   ${config_push_wait}

    ${ROUTER_SPAWN}=        Open Spawn          ${router1.console_ip}   ${router1.console_port}      ${router1.username}       ${router1.password}        ${router1.platform}
    Set Suite Variable      ${ROUTER_SPAWN}
    ${SHOW_TRUNK_VLANS}=    Send                    ${ROUTER_SPAWN}         ${CMD_SHOW_TRUNK_VLANS}
    Should Contain          ${SHOW_TRUNK_VLANS}     ${EXPECTED_TRUNK_VLANS}

    ${SHOW_RUN_CONFIG}=     Send                    ${ROUTER_SPAWN}         ${CMD_SHOW_CONFIG}
    Should Contain          ${SHOW_RUN_CONFIG}      interface ${INTERFACE_NAME}  mode bridge-802.1q
    Should Contain          ${SHOW_RUN_CONFIG}      interface ${INTERFACE_NAME}  allowed-vlan ${EXPECTED_TRUNK_VLANS}


    [Teardown]   run keywords       Logout User
    ...                             Quit Browser
                 Close Spawn        ${ROUTER_SPAWN}

Test4: Upgrade Latest IQ Engine Router Firmware
    [Documentation]     Upgrate latest IQ Engine Router Firmware
    [Tags]              sanity   upgrade  XR  P2  P3  P4  regression    Test4  production

    Depends On              Test3
    ${LOGIN_XIQ}=           Login User              ${tenant_username}      ${tenant_password}
    ${LATEST_VERSION}=      Upgrade Device To Latest Version         ${router1.serial}

    Sleep                   ${config_push_wait}
    Sleep                   ${router_reboot_wait}
    Sleep                   ${router_reboot_wait}

    ${ROUTER_SPAWN}=        Open Spawn          ${router1.console_ip}   ${router1.console_port}      ${router1.username}       ${router1.password}        ${router1.platform}
    ${ROUTER_FM_VER}=       Send          ${ROUTER_SPAWN}           show version | include Version
    ${SHOW_RUN_CONFIG}=     Send          ${ROUTER_SPAWN}           ${CMD_SHOW_CONFIG}
    Close Spawn             ${ROUTER_SPAWN}

    should contain          ${ROUTER_FM_VER}        ${LATEST_VERSION}
    Should Contain          ${SHOW_RUN_CONFIG}      interface ${INTERFACE_NAME}  mode bridge-802.1q
    Should Contain          ${SHOW_RUN_CONFIG}      interface ${INTERFACE_NAME}  allowed-vlan ${EXPECTED_TRUNK_VLANS}

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser
                 Close Spawn        ${ROUTER_SPAWN}

Test Suite Clean Up
    [Documentation]             delete created network policies, SSID, Device etc
    [Tags]                      sanity   router  P2   P3  P4  production  regression
    Login User              ${tenant_username}      ${tenant_password}
    Run Keyword If   '${CLEANUP_TAG}'=='production'  run keywords  Update Network Policy To Router   default_network_policy    router_serial=${router1.serial}
    ...     AND       Delete Device  device_serial=${router1.serial}
    ...     AND       Delete Network Policy  ${NW_POLICY_NAME}
    ...     AND       Delete SSID  ${SSID_NAME}
    ...     AND       Delete Router Template  default_network_policy  ${router1.device_template}
    ...     AND       Delete Sub Network Profile  ${SUB_NETWORK_NAME}
    ...     AND       Delete Port Type Profile    ${PORT_TYPE_NAME}
    ...     AND       Delete Vlan Profile   ${VLAN_NAME}
    Logout User
    Quit Browser
