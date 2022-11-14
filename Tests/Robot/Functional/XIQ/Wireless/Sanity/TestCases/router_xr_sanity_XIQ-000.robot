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
${NW_POLICY_NAME}               test_automation_network_policy
${DEF_POLICY_NAME}              default_network_policy
${SSID_NAME}                    Router_XR_template
${INTERFACE_NAME}               eth2
${CMD_SHOW_TRUNK_VLANS}         show interface ${INTERFACE_NAME} allowed-vlan
${DEF_VAL_SHOW_TRUNK_VLANS}     1-4094
${DEF_VAL_SHOW_RUN_VLANS}       1 - 4094
${CUS_VAL_SHOW_TRUNK_VLANS}     10-20
${CUS_VAL_SHOW_RUN_VLANS}       10 - 20
${CMD_SHOW_CONFIG}              show running-config
${PORT_TYPE_NAME}               test_trunk_xr
${SUB_NETWORK_NAME}             test_subnetwork
${VLAN_NAME}                    test_router_vlan
${LOCATION}                     auto_location_01, Santa Clara, building_02, floor_04
${CLEANUP_TAG}                  production

*** Settings ***
Library     extauto/common/Cli.py
Library     extauto/common/Utils.py
Library     extauto/common/TestFlow.py

Library     extauto/xiq/flows/common/Login.py
Library     extauto/xiq/flows/common/Navigator.py

Library     extauto/xiq/flows/manage/Devices.py
Library     extauto/xiq/flows/manage/AdvanceOnboarding.py

Library     extauto/xiq/flows/configure/NetworkPolicy.py
Library     extauto/xiq/flows/configure/CommonObjects.py
Library     extauto/xiq/flows/configure/RouterTemplate.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml

Resource     Tests/Robot/Functional/XIQ/Wireless/Sanity/Resources/router_xr_sanity_config.robot

Force Tags   testbed_1_node

Suite Setup     Suite Setup   ${router1.serial}
Suite Teardown  Suite Teardown

*** Keywords ***
Suite Setup
    [Arguments]         ${SERIAL}

    ${LOGIN_STATUS}=    Login User  ${tenant_username}      ${tenant_password}      check_warning_msg=True
    Should Be Equal As Integers     ${LOGIN_STATUS}         1

    Navigate To Devices
    Refresh Devices Page

    ${DELETE_DEVICE}=               Delete Device                   device_serial=${router1.serial}
    Should Be Equal As Integers     ${DELETE_DEVICE}                1

    ${DLT_NW_POLICY}=               Delete Network Policy           ${NW_POLICY_NAME}
    Should Be Equal As Integers     ${DLT_NW_POLICY}                1

    ${DLT_DEF_POLICY}=              Delete Network Policy           default_network_policy
    Should Be Equal As Integers     ${DLT_DEF_POLICY}               1

    ${CREATE_DEF_POLICY_STATUS}=    Create Network Policy           default_network_policy      &{CONFIG_PUSH_OPEN_NW_01}
    Should Be Equal As Integers     ${CREATE_DEF_POLICY_STATUS}     1

    ${DELETE_SSID}=                 Delete SSIDs                    ${SSID_NAME}
    Should Be Equal As Integers     ${DELETE_SSID}                  1

    ${DELETE_ROUTER_TEMPLATE}=      Delete Router Template          default_network_policy      ${router1.device_template}
    Should Be True                  ${DELETE_ROUTER_TEMPLATE}

    ${DELETE_SUBNW_SPACE}=          Delete Sub Network Profile      ${SUB_NETWORK_NAME}
    Should Be Equal As Integers     ${DELETE_SUBNW_SPACE}           1

    ${DELETE_PORT_TYPE}=            Delete Port Type Profile        ${PORT_TYPE_NAME}
    Should Be Equal As Integers     ${DELETE_PORT_TYPE}             1

    ${DELETE_VLAN_PROFILE}=         Delete Vlan Profile             ${VLAN_NAME}
    Should Be Equal As Integers     ${DELETE_VLAN_PROFILE}          1

Suite Teardown
    [Documentation]             delete created network policies, SSID, Device etc
    [Tags]                      production      cleanup

    Navigate To Devices
    Refresh Devices Page

    ${DELETE_DEVICE}=               Delete Device                   device_serial=${router1.serial}
    Should Be Equal As Integers     ${DELETE_DEVICE}                1

    ${DLT_NW_POLICY}=               Delete Network Policy           ${NW_POLICY_NAME}
    Should Be Equal As Integers     ${DLT_NW_POLICY}                1

    ${DELETE_SSID}=                 Delete SSIDs                    ${SSID_NAME}
    Should Be Equal As Integers     ${DELETE_SSID}                  1

    ${DELETE_ROUTER_TEMPLATE}=      Delete Router Template          default_network_policy      ${router1.device_template}
    Should Be True                  ${DELETE_ROUTER_TEMPLATE}

    ${DELETE_SUBNW_SPACE}=          Delete Sub Network Profile      ${SUB_NETWORK_NAME}
    Should Be Equal As Integers     ${DELETE_SUBNW_SPACE}           1

    ${DELETE_PORT_TYPE}=            Delete Port Type Profile        ${PORT_TYPE_NAME}
    Should Be Equal As Integers     ${DELETE_PORT_TYPE}             1

    ${DELETE_VLAN_PROFILE}=         Delete Vlan Profile             ${VLAN_NAME}
    Should Be Equal As Integers     ${DELETE_VLAN_PROFILE}          1

    ${DLT_DEF_POLICY}=              Delete Network Policy           default_network_policy
    Should Be Equal As Integers     ${DLT_DEF_POLICY}               1

    [Teardown]   run keywords       logout user
    ...                             quit browser

Push XR Router Template
    [Arguments]         ${POLICY_NAME}
    [Documentation]     Push template to the XR router device

    ${DEVICE_UPDATE_CONFIG}=    Update Network Policy To Router     ${POLICY_NAME}      router_serial=${router1.serial}     update_method=Complete
    Should Be Equal As Integers         ${DEVICE_UPDATE_CONFIG}     1

    ${WAIT_PUSH_RESULT}=        Wait For Policy Config Push To Complete     ${router1.serial}       boot_wait_time=180
    Should Be Equal As Integers         ${WAIT_PUSH_RESULT}         1

    ${ROUTER_SPAWN}=    Open Spawn      ${router1.console_ip}       ${router1.console_port}     ${router1.username}     ${router1.password}     ${router1.cli_type}     connection_method=console
    Should Not Be Equal As Strings      '${ROUTER_SPAWN}'           '-1'
    Send                    ${ROUTER_SPAWN}             console page 0

    ${SHOW_TRUNK_VLANS}=    Send                        ${ROUTER_SPAWN}             ${CMD_SHOW_TRUNK_VLANS}
    ${SHOW_RUN_CONFIG}=     Send                        ${ROUTER_SPAWN}             ${CMD_SHOW_CONFIG}
    IF  '${POLICY_NAME}' == '${DEF_POLICY_NAME}'
        Should Contain          ${SHOW_TRUNK_VLANS}     ${DEF_VAL_SHOW_TRUNK_VLANS}
        Should Contain          ${SHOW_RUN_CONFIG}      interface ${INTERFACE_NAME} mode bridge-access
        Should Not Contain      ${SHOW_RUN_CONFIG}      interface ${INTERFACE_NAME} allowed-vlan ${DEF_VAL_SHOW_RUN_VLANS}
    END
    IF  '${POLICY_NAME}' == '${NW_POLICY_NAME}'
        Should Contain          ${SHOW_TRUNK_VLANS}     ${CUS_VAL_SHOW_TRUNK_VLANS}
        Should Contain          ${SHOW_RUN_CONFIG}      interface ${INTERFACE_NAME} mode bridge-802.1q
        Should Contain          ${SHOW_RUN_CONFIG}      interface ${INTERFACE_NAME} allowed-vlan ${CUS_VAL_SHOW_RUN_VLANS}
    END

    [Teardown]
    Close Spawn     ${ROUTER_SPAWN}

*** Test Cases ***
TCCS-7766_Step1: Onboard Aerohive XR Router Using Quick Add Method
    [Documentation]         Onboard Aerohive XR Router Using Quick Add Method
    [Tags]                  production      tccs_7766       tccs_7766_step1

    Navigate To Devices
    Refresh Devices Page


    ${ONBOARD_RESULT}=      onboard device quick          ${router1}
    Should Be Equal As Integers                     ${ONBOARD_RESULT}           1


    ${SEARCH_ROUTER}=   Search Device   device_serial=${router1.serial}
    Should Be Equal As Integers         ${SEARCH_ROUTER}            1

    ${ROUTER_SPAWN}=    Open Spawn      ${router1.console_ip}       ${router1.console_port}     ${router1.username}     ${router1.password}     ${router1.cli_type}     connection_method=console
    Should Not Be Equal As Strings      '${ROUTER_SPAWN}'           '-1'

    ${CONF_STATUS_RESULT}=          Configure Device To Connect To Cloud            ${router1.cli_type}     ${capwap_url}       ${ROUTER_SPAWN}
    Should Be Equal As Integers     ${CONF_STATUS_RESULT}           1

    ${WAIT_CONF_STATUS_RESULT}=     Wait For Configure Device To Connect To Cloud   ${router1.cli_type}     ${capwap_url}       ${ROUTER_SPAWN}
    Should Be Equal As Integers     ${WAIT_CONF_STATUS_RESULT}      1

    ${CONNECTED_STATUS}=            Wait Until Device Online                        ${router1.serial}
    Should Be Equal As Integers     ${CONNECTED_STATUS}             1

    ${DEVICE_STATUS}=       Get Device Status       device_mac=${router1.mac}
    Should contain any  ${DEVICE_STATUS}    green     config audit mismatch

    ${CAPWAP_STATUS}=       Send            ${ROUTER_SPAWN}         ${cmd_capwap_client_state}
    Should Contain                          ${CAPWAP_STATUS}        ${output_capwap_status}

    [Teardown]
    Close Spawn     ${ROUTER_SPAWN}

TCCS-7766_Step2: Onboard Aerohive XR Router Using Advance Onboarding Method
    [Documentation]         Onboard Aerohive XR Router Using Advance Onboarding Method
    [Tags]                  production      tccs_7766       tccs_7766_step2

    Navigate To Devices
    Refresh Devices Page

    ${DELETE_DEVICE}=               Delete Device                   device_serial=${router1.serial}
    Should Be Equal As Integers     ${DELETE_DEVICE}                1

    ${ONBOARD_ROUTER}=              Advance Onboard Device      ${router1.serial}       device_make=${router1.make}     dev_location=${LOCATION}
    Should Be Equal As Integers     ${ONBOARD_ROUTER}               1

    ${ROUTER_SPAWN}=    Open Spawn      ${router1.console_ip}       ${router1.console_port}     ${router1.username}     ${router1.password}     ${router1.cli_type}     connection_method=console
    Should Not Be Equal As Strings      '${ROUTER_SPAWN}'           '-1'

    ${CONF_STATUS_RESULT}=          Configure Device To Connect To Cloud            ${router1.cli_type}     ${capwap_url}       ${ROUTER_SPAWN}
    Should Be Equal As Integers     ${CONF_STATUS_RESULT}           1

    ${WAIT_CONF_STATUS_RESULT}=     Wait For Configure Device To Connect To Cloud   ${router1.cli_type}     ${capwap_url}       ${ROUTER_SPAWN}
    Should Be Equal As Integers     ${WAIT_CONF_STATUS_RESULT}      1

    ${CONNECTED_STATUS}=            Wait Until Device Online                        ${router1.serial}
    Should Be Equal As Integers     ${CONNECTED_STATUS}             1

    ${DEVICE_STATUS}=               Get Device Status       device_mac=${router1.mac}
    Should Contain Any              ${DEVICE_STATUS}        green       config audit mismatch

    [Teardown]
    Close Spawn     ${ROUTER_SPAWN}

TCCS-12330: Create Router XR Template
    [Documentation]         Create Router XR Template
    [Tags]                  production      tccs_12330

    Depends On              TCCS-7766_Step1

    Push XR Router Template     ${DEF_POLICY_NAME}

    ${CREATE_NW_POLICY}=        Create Network Policy   ${NW_POLICY_NAME}   &{XR_ROUTER_NW_01}
    Should Be Equal As Integers     ${CREATE_NW_POLICY}         1

    ${CREATE_ROUTER_TEMPLATE}=  Add Router Template     ${NW_POLICY_NAME}   &{ROUTER_TEMPLATE_CONFIG1}
    Should Be Equal As Integers     ${CREATE_ROUTER_TEMPLATE}   1

    Push XR Router Template     ${NW_POLICY_NAME}

TCCS-7351: Upgrade Latest IQ Engine Router Firmware
    [Documentation]     Upgrate latest IQ Engine Router Firmware
    [Tags]              production      tccs_7351

    Depends On              TCCS-7766_Step1

    ${LATEST_VERSION}=      Upgrade Device To Latest Version        ${router1.serial}
    Should Not Be Equal As Strings      '${LATEST_VERSION}'         '-1'

    Sleep                   ${config_push_wait}
    Sleep                   ${router_reboot_wait}
    Sleep                   ${router_reboot_wait}

    ${ROUTER_SPAWN}=        Open Spawn      ${router1.console_ip}       ${router1.console_port}     ${router1.username}     ${router1.password}     ${router1.cli_type}     connection_method=console
    Should Not Be Equal As Strings      '${ROUTER_SPAWN}'           '-1'
    Send                    ${ROUTER_SPAWN}         console page 0

    ${ROUTER_FM_VER}=       Send                    ${ROUTER_SPAWN}     show version | include Version
    Should Contain          ${ROUTER_FM_VER}        ${LATEST_VERSION}

    ${SHOW_TRUNK_VLANS}=    Send                    ${ROUTER_SPAWN}     ${CMD_SHOW_TRUNK_VLANS}
    ${SHOW_RUN_CONFIG}=     Send                    ${ROUTER_SPAWN}     ${CMD_SHOW_CONFIG}
    Should Contain          ${SHOW_TRUNK_VLANS}     ${CUS_VAL_SHOW_TRUNK_VLANS}
    Should Contain          ${SHOW_RUN_CONFIG}      interface ${INTERFACE_NAME} mode bridge-802.1q
    Should Contain          ${SHOW_RUN_CONFIG}      interface ${INTERFACE_NAME} allowed-vlan ${CUS_VAL_SHOW_RUN_VLANS}

    Close Spawn     ${ROUTER_SPAWN}

    Push XR Router Template     ${DEF_POLICY_NAME}
