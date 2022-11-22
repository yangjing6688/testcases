
*** Variables ***

*** Settings ***
Library     Collections
Library     extauto/common/Utils.py
Library     extauto/common/Cli.py
Library     extauto/xiq/flows/common/Login.py
Library     extauto/xiq/flows/manage/Devices.py
Library     extauto/xiq/flows/manage/Device360.py
Library     extauto/xiq/flows/manage/Switch.py
Library     extauto/xiq/flows/manage/Tools.py
Library     extauto/xiq/flows/configure/NetworkPolicy.py
Library     extauto/xiq/flows/globalsettings/GlobalSetting.py
Library     extauto/common/TestFlow.py
Library     ExtremeAutomation/Imports/CommonObjectUtils.py
Library     extauto/xiq/flows/manage/AdvanceOnboarding.py
Library     extauto/xiq/flows/manage/Alarms.py
Library     extauto/xiq/flows/manage/DeviceCliAccess.py
Library     ExtremeAutomation/Keywords/UserDefinedKeywords/NetworkElements/SetupTeardown/SetupTeardownUdks.py

Library     extauto/xiq/flows/common/Navigator.py
Library     extauto/xiq/flows/configure/AutoProvisioning.py
Library     extauto/xiq/flows/configure/CommonObjects.py
Library     extauto/xiq/flows/configure/ExpressNetworkPolicies.py
Library     extauto/xiq/flows/configure/RouterTemplate.py
Variables   Resources/voss_config.py
Resource    Resources/device_sanity_XIQ_config.robot

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml

Force Tags   testbed_1_node
Suite Setup     Test Suite Setup
Suite Teardown     Test Suite Teardown


*** Keywords ***
Test Suite Setup
    # Use this method to convert the ap, wing, netelem to a generic device object
    # ap1       => device1
    # wing1     => device1
    # netelem1  => device1 (EXOS / VOSS)
    convert to generic device object   device  index=1

    # Create a random string with a known string, so we track if things are not cleaned up
    ${random_string}=               Get Random String
    ${PUSH_CONFIG_SSID_01}=     Catenate    PUSH_CONFIG_SSID_${random_string}
    ${PUSH_CONFIG_POLICY_01}=   Catenate    PUSH_CONFIG_POLICY_${random_string}
    ${NEW_SSID_NAME_1}=         Catenate    PUSH_CONFIG_NEW_${random_string}

    Set Global Variable          ${NEW_SSID_NAME_1}
    Set Global Variable          ${PUSH_CONFIG_SSID_01}
    Set Global Variable          ${PUSH_CONFIG_POLICY_01}

    &{CONFIG_PUSH_OPEN_NW_01}=   Create Dictionary   ssid_name=${PUSH_CONFIG_SSID_01}         network_type=standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}   auth_profile=&{OPEN_AUTHENTICATION_PROFILE0}
    &{CONFIG_PUSH_OPEN_NW_02}=   Create Dictionary   ssid_name=${PUSH_CONFIG_POLICY_01}         network_type=standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}   auth_profile=&{OPEN_AUTHENTICATION_PROFILE0}

    Set Global Variable          &{CONFIG_PUSH_OPEN_NW_01}
    Set Global Variable          &{CONFIG_PUSH_OPEN_NW_02}

    # Create the connection to the device(s)
    Base Test Suite Setup
    Set Global Variable    ${MAIN_DEVICE_SPAWN}    ${device1.name}

    # downgrade the device if needed
    downgrade iqagent      ${device1.cli_type}  ${MAIN_DEVICE_SPAWN}

    # log in the user
    Login User      ${tenant_username}      ${tenant_password}

Test Suite Teardown
    Clean Up Device
    ${DLT_NW_POLICIES}=             Delete Network Polices      ${PUSH_CONFIG_POLICY_01}        ${VOSS_POLICY_NAME}    ignore_cli_feedback=true
    should be equal as integers     ${DLT_NW_POLICIES}          1

    ${DELETE_SSIDS}=                Delete SSIDs                ${PUSH_CONFIG_SSID_01}        ${NEW_SSID_NAME_1}  ${VOSS_SSID_NAME}     ignore_cli_feedback=true
    should be equal as integers     ${DELETE_SSIDS}             1

    Logout User
    Quit Browser
    Base Test Suite Cleanup

Clean Up Device
    ${search_result}=   Search Device       device_serial=${device1.serial}    ignore_cli_feedback=true
    # Disconnect from Extreme Cloud IQ
    Run Keyword If  '${search_result}' == '1'       Delete and Disconnect Device From Cloud

Delete and Disconnect Device From Cloud
    delete device   device_serial=${device1.serial}
    disconnect device from cloud     ${device1.cli_type}     ${MAIN_DEVICE_SPAWN}

Disable SSH and Close Device360 Window
    ${DISABLE_SSH}=                     Device360 Disable SSH Connectivity   ${device1.mac}
    Should Be Equal As Integers         ${DISABLE_SSH}     1

    ${CLOSE_DEVICE360_WINDOW}=          Close Device360 Window
    Should Be Equal As Integers         ${CLOSE_DEVICE360_WINDOW}     1

Validate Device Information
    @{column_list}=    Create List    MGT IP ADDRESS    MAC
    ${DEVICE_INFOMATION}=   get_device_column_information  ${device1.serial}    ${column_list}
    Run Keyword If  '${device1.cli_type}' != 'WING-AP' and '${device1.cli_type}' != 'AH-XR'  Validate Device Managment IP Information   ${DEVICE_INFOMATION}
    ${DEVICE_MAC}=                 Get From Dictionary      ${DEVICE_INFOMATION}    MAC
    Should Be Equal As Strings    '${DEVICE_MAC}'           '${device1.mac}'

Validate Device Managment IP Information
    [Arguments]    ${DEVICE_INFOMATION}
    ${DEVICE_IP}=                  Get From Dictionary      ${DEVICE_INFOMATION}    MGT_IP_ADDRESS
    Should Be Equal As Strings    '${DEVICE_IP}'           '${device1.ip}'

Confirm Device Status
    [Documentation]     Checks the status of the specified device and confirms it matches the expected value
    [Arguments]         ${serial}  ${expected_status}

    ${device_status}=       Get Device Status       device_serial=${serial}
    Should Contain          ${device_status}   ${expected_status}

Clean Up Test Device and Confirm Success
    [Documentation]     Deletes the specified device and confirms the action was successful
    [Arguments]         ${serial}

    Navigate to Devices and Confirm Success
    ${del_result}=  Delete Device   ${serial}
    Should Be Equal As Integers     ${del_result}  1

*** Test Cases ***
TCCS-13684: Advanced Onboard Device on XIQ
    [Documentation]         Checks for Advanced Device onboarding on XIQ

    [Tags]                  advanced_onboard      development   tccs_13684

    Clean Up Device

    ${ONBOARD_RESULT}=      Advance Onboard Device         ${device1.serial}    device_make=${device1.make}   dev_location=${LOCATION}  device_mac=${device1.mac}
    Should Be Equal As Strings                  ${ONBOARD_RESULT}       1

    configure device to connect to cloud    ${device1.cli_type}    ${generic_capwap_url}  ${MAIN_DEVICE_SPAWN}

    ${ONLINE_STATUS_RESULT}=    wait until device online     ${device1.serial}
    Should Be Equal As Strings                  ${ONLINE_STATUS_RESULT}       1

    ${MANAGED_STATUS_RESULT}=   wait until device managed   ${device1.serial}
    Should Be Equal As Strings                  ${MANAGED_STATUS_RESULT}      1

    ${DEVICE_STATUS_RESULT}=    get device status      ${device1.serial}
    Should Be Equal As Strings                  ${DEVICE_STATUS_RESULT}      green

    Validate Device Information

TCCS-13685: Simple Onboard Device on XIQ
    [Documentation]         Checks for Device onboarding on XIQ

    [Tags]                  onboard      development   onboard-fast     tccs_13685      tccs_13686      tccs_13687      tccs_13688      tccs_13689

    Clean Up Device

    ${ONBOARD_RESULT}=          onboard device quick      ${device1}
    Should Be Equal As Strings                  ${ONBOARD_RESULT}       1

    configure device to connect to cloud    ${device1.cli_type}   ${generic_capwap_url}   ${MAIN_DEVICE_SPAWN}

    ${ONLINE_STATUS_RESULT}=    wait until device online     ${device1.serial}
    Should Be Equal As Strings                  ${ONLINE_STATUS_RESULT}       1

    ${MANAGED_STATUS_RESULT}=   wait until device managed   ${device1.serial}
    Should Be Equal As Strings                  ${MANAGED_STATUS_RESULT}      1

    ${DEVICE_STATUS_RESULT}=    get device status      ${device1.serial}
    Should Be Equal As Strings                  ${DEVICE_STATUS_RESULT}      green

    Validate Device Information

TCCS-13686: Enable SSH on Device and Confirm Only a Single SSH Session Can Be Established
    [Documentation]     Enable SSH on Switch and Confirm Only a Single SSH Session Can Be Established

    [Tags]              ssh      development    tccs_13686

    Depends On           TCCS-13685

    # make sure the feature is enabled
    enable ssh availability

    # Create the SSH connection
    &{ip_port_info}=                    Device360 Enable SSH CLI Connectivity   ${device1.mac}  run_time=30
    ${ip}=                              Get From Dictionary  ${ip_port_info}  ip
    ${port}=                            Get From Dictionary  ${ip_port_info}  port

    Should not be Empty     ${ip}
    Should not be Empty     ${port}
    # SSH to the connection
    ${ssh_spawn}=                       Open Spawn    ${ip}  ${port}  ${device1.username}  ${device1.password}  ${device1.cli_type}  pxssh=True
    # Close the connection
    ${close_result}=                    Close Spawn   ${ssh_spawn}  pxssh=True
    # Try to ssh again ( this should fail )
    ${ssh_spawn}=                       Open Spawn    ${ip}  ${port}  ${device1.username}  ${device1.password}  ${device1.cli_type}  pxssh=True  expect_error=true

    [Teardown]  Disable SSH and Close Device360 Window

TCCS-13687: Firmware upgrade to lastest version (AH-AP Only)
    [Documentation]         Verify IQ engine upgrade to lastest version ( we should just make sure it was upgraded )

    [Tags]			        push_config     development     tccs_13687

    Depends On              TCCS-13685

    @{supported_cli_types}=    Create List   AH-AP
    check_cli_type_and_skip     ${supported_cli_types}     ${device1.cli_type}

    ${SPAWN1}=              Open Spawn      ${device1.ip}   ${device1.port}      ${device1.username}       ${device1.password}        ${device1.cli_type}

    ${VERSION_DETAIL1}=     Send            ${SPAWN1}         show version detail

    ${AP_BUILD_VERSION1}=   Get AP Version              ${SPAWN1}

    ${LATEST_VERSION}=      Upgrade Device To Latest Version            ${device1.serial}
    Should Not be Empty     ${LATEST_VERSION}

    Sleep                   ${ap_reboot_wait}

    ${CONNECTED_STATUS}=    Wait Until Device Online                ${device1.serial}       retry_count=15
    Should Be Equal as Integers             ${CONNECTED_STATUS}          1

    ${REBOOT_STATUS}=    Wait Until Device Reboots               ${device1.serial}
    Should Be Equal as Integers             ${REBOOT_STATUS}          1

    Close Spawn             ${SPAWN1}

    ${SPAWN2}=              Open Spawn      ${device1.ip}   ${device1.port}      ${device1.username}       ${device1.password}        ${device1.cli_type}
    Should not be equal as Strings          '${SPAWN2}'        '-1'

    ${CLOCK_OUPUT2}=        Send            ${SPAWN2}         show clock

    ${REBOOT_OUPUT2}=       Send            ${SPAWN2}         show reboot schedule
    Should Not Contain      ${REBOOT_OUPUT2}     Next reboot Scheduled

    ${VERSION_DETAIL2}=     Send            ${SPAWN2}         show version detail

    ${AP_BUILD_VERSION2}=   Get AP Version              ${SPAWN2}
    Should Be Equal As Strings  ${LATEST_VERSION}           ${AP_BUILD_VERSION2}

    Close Spawn        ${SPAWN2}

TCCS-13688: Verification of config push complete config update (AH-AP Only)
    [Documentation]             Verification of config push complete config update

    [Tags]                      push_config     development     tccs_13688      tccs_13689

    Depends On                  TCCS-13685

    @{supported_cli_types}=    Create List   AH-AP
    check_cli_type_and_skip     ${supported_cli_types}     ${device1.cli_type}

    Set To Dictionary           ${CONFIG_PUSH_OPEN_NW_01}    ssid_name=${PUSH_CONFIG_SSID_01}
    Log to Console              ${CONFIG_PUSH_OPEN_NW_01}

    ${CREATE_NW_POLICY_STATUS}=     Create Network Policy   policy=${PUSH_CONFIG_POLICY_01}      &{CONFIG_PUSH_OPEN_NW_01}
    should be equal as integers     ${CREATE_NW_POLICY_STATUS}               1

    ${DEPLOY_STATUS}=               Deploy Network Policy with Complete Update      ${PUSH_CONFIG_POLICY_01}          ${device1.serial}
    should be equal as integers     ${DEPLOY_STATUS}               1

    ${CONNECTED_STATUS}=            Wait Until Device Online                ${device1.serial}   None   30   20
    Should Be Equal as Integers     ${CONNECTED_STATUS}          1

    ${OUTPUT1}=             Send           ${MAIN_DEVICE_SPAWN}                show ssid
    Should Contain                          ${OUTPUT1}                  ${PUSH_CONFIG_SSID_01}


TCCS-13689: Verification of config push delta update (AH-AP Only)
    [Documentation]         Verification of config push delta update

    [Tags]                  push_config     development     tccs_13689

    Depends On              TCCS-13688

    @{supported_cli_types}=    Create List   AH-AP
    check_cli_type_and_skip     ${supported_cli_types}     ${device1.cli_type}

    ${EDIT_STATUS}=                 Edit Network Policy SSID                    ${PUSH_CONFIG_POLICY_01}          ${PUSH_CONFIG_SSID_01}     ${NEW_SSID_NAME_1}
    should be equal as integers             ${EDIT_STATUS}              1

    ${DEPLOY_STATUS}=       Deploy Network Policy with Delta Update     ${PUSH_CONFIG_POLICY_01}          ${device1.serial}
    should be equal as integers             ${DEPLOY_STATUS}            1

    ${CONNECTED_STATUS}=    Wait Until Device Online                ${device1.serial}
    Should Be Equal as Integers             ${CONNECTED_STATUS}          1

    ${OUTPUT1}=             Send            ${MAIN_DEVICE_SPAWN}              show ssid
    Should Contain                          ${OUTPUT1}                  ${NEW_SSID_NAME_1}

#Step10: Perform Device Update on VOSS Switch (VOSS ONLY)
#    [Documentation]     Performs a device update on the VOSS switch
#    [Tags]              production      tccs_7299       tccs_7299_step5   development
#
#    Depends On          onboard
#
#    @{supported_cli_types}=    Create List   VOSS-skipped
#    check_cli_type_and_skip     ${supported_cli_types}     ${device1.cli_type}
#
#    ${assign_policy_result}=        Assign network policy to switch  policy_name=${VOSS_POLICY_NAME}  serial=${device1.serial}
#    Should Be Equal As Integers     ${assign_policy_result}  1
#
#    ${result}=  Update Switch Policy and Configuration    ${device1.serial}
#    Should Be Equal As Integers     ${result}     1
#
#
#
#Step11: Confirm VOSS Device Values After Update (VOSS ONLY)
#    [Documentation]     Confirms the device table contains expected values for the VOSS switch after an update
#
#    [Tags]              production      tccs_7299       tccs_7299_step6    development
#
#    Depends On          onboard
#
#    @{supported_cli_types}=    Create List   VOSS-skipped
#    check_cli_type_and_skip     ${supported_cli_types}     ${device1.cli_type}
#
#    Refresh Devices Page
#    Confirm Device Status  ${device1.serial}  ${STATUS_AFTER_UPDATE}
#
#    &{device_info}=     Get Device Row Values  ${device1.serial}  POLICY,LOCATION,SERIAL,MODEL
#
#    ${policy_result}=   Get From Dictionary     ${device_info}  POLICY
#    Should Be Equal     ${policy_result}        ${VOSS_POLICY_NAME}
#
#    ${loc_result}=      Get From Dictionary     ${device_info}  LOCATION
#    Should Be Equal     ${loc_result}           ${LOCATION_DISPLAY}
#
#    ${serial_result}=   Get From Dictionary     ${device_info}  SERIAL
#    Should Be Equal     ${serial_result}        ${device1.serial}
#
#    ${model_result}=    Get From Dictionary     ${device_info}  MODEL
#    Should Be Equal     ${model_result}         ${device1.model}
#
#step12: Confirm Device360 View Values for VOSS Switch (VOSS ONLY)
#    [Documentation]     Confirms the Device360 view contains correct values for the VOSS Switch
#
#    [Tags]              production      tccs_7299       tccs_7299_step7    development
#
#    Depends On          onboard
#
#    @{supported_cli_types}=    Create List   VOSS-skipped
#    check_cli_type_and_skip     ${supported_cli_types}     ${device1.cli_type}
#
#    Refresh Devices Page
#    &{overview_info}=           Get VOSS Device360 Overview Information                 ${device1.mac}
#
#    Refresh Devices Page
#    &{device_config_info}=      Get VOSS Device360 Device Configuration Information     ${device1.mac}
#
#    ${overview_serial}=         Get From Dictionary  ${overview_info}  serial_number
#    Should Be Equal             ${overview_serial}  ${device1.serial}
#
#    ${overview_model}=          Get From Dictionary  ${overview_info}  device_model
#    Should Be Equal             ${overview_model}   ${device1.serial}
#
#    ${overview_policy}=         Get From Dictionary  ${overview_info}  network_policy
#    Should Be Equal             ${overview_policy}  ${VOSS_POLICY_NAME}
#
#    ${config_policy}=           Get From Dictionary  ${device_config_info}  network_policy
#    Should Be Equal             ${config_policy}  ${VOSS_POLICY_NAME}
#
#    ${config_template}=         Get From Dictionary  ${device_config_info}  device_template
#    Should Be Equal             ${config_template}  ${VOSS_TEMPLATE_NAME}
#
#
#step 13: Create Router XR Template (XR ONLY)
#    [Documentation]         Create Router XR Template
#
#    [Tags]                  production      tccs_12330    development
#
#    Depends On              onboard
#
#    @{supported_cli_types}=    Create List   AH-XR-skipped
#    check_cli_type_and_skip     ${supported_cli_types}     ${device1.cli_type}
#
#    # XR ONLY
#    &{ROUTER_TEMPLATE_CONFIG1}=  Create Dictionary   router_model=${device1.model}  template_name=${device1.device_template}  interface_name=ETH2    new_port_type_config=&{PORT_TYPE_CONFIG1}   network_allocation_config=&{NETWORK_ALLOCATION_CONFIG1}
#    Set Global Variable          &{ROUTER_TEMPLATE_CONFIG1}
#
#    ${CREATE_NW_POLICY}=    Create Network Policy   ${XR_NW_POLICY_NAME}       &{XR_ROUTER_NW_01}
#    Should Be Equal As Strings                      '${CREATE_NW_POLICY}'   '1'
#
#    ${CREATE_AP_TEMPLATE}=      Add Router Template     ${XR_NW_POLICY_NAME}     &{ROUTER_TEMPLATE_CONFIG1}
#
#    ${DEVICE_UPDATE_CONFIG}=    Update Network Policy To Router    policy_name=${XR_NW_POLICY_NAME}    router_serial=${router1.serial}
#    Should Be Equal As Strings                      '${DEVICE_UPDATE_CONFIG}'       '1'
#
#    Log to Console          Sleep for ${config_push_wait}
#    sleep                   ${config_push_wait}
#
#    ${DEVICE_UPDATE_STATUS}=    Wait Until Device Update Done   device_serial=${router1.serial}
#    Should Be Equal As Strings                      '${DEVICE_UPDATE_STATUS}'       '1'
#
#    ${SHOW_TRUNK_VLANS}=    Send                    ${MAIN_DEVICE_SPAWN}         ${XR_CMD_SHOW_TRUNK_VLANS}
#    Should Contain          ${SHOW_TRUNK_VLANS}     ${XR_EXPECTED_TRUNK_VLANS}
#
#    ${SHOW_RUN_CONFIG}=     Send                    ${MAIN_DEVICE_SPAWN}         ${XR_CMD_SHOW_CONFIG}
#    Should Contain          ${SHOW_RUN_CONFIG}      interface ${INTERFACE_NAME}  mode bridge-802.1q
#    Should Contain          ${SHOW_RUN_CONFIG}      interface ${INTERFACE_NAME}  allowed-vlan ${XR_EXPECTED_TRUNK_VLANS}
#
#
#step 14: Upgrade Latest IQ Engine Router Firmware (XR ONLY)
#    [Documentation]     Upgrate latest IQ Engine Router Firmware
#
#    [Tags]              production      tccs_7351    development
#
#    Depends On              onboard
#
#    @{supported_cli_types}=    Create List   AH-XR-skipped
#    check_cli_type_and_skip     ${supported_cli_types}     ${device1.cli_type}
#
#    ${LATEST_VERSION}=      Upgrade Device To Latest Version         ${router1.serial}
#
#    Sleep                   ${config_push_wait}
#    Sleep                   ${router_reboot_wait}
#    Sleep                   ${router_reboot_wait}
#
#    ${ROUTER_FM_VER}=       Send           ${MAIN_DEVICE_SPAWN}            show version | include Version
#    should contain          ${ROUTER_FM_VER}        ${LATEST_VERSION}
#
#    ${SHOW_RUN_CONFIG}=     Send           ${MAIN_DEVICE_SPAWN}            ${XR_CMD_SHOW_CONFIG}
#    Should Contain          ${SHOW_RUN_CONFIG}      interface ${INTERFACE_NAME}  mode bridge-802.1q
#    Should Contain          ${SHOW_RUN_CONFIG}      interface ${INTERFACE_NAME}  allowed-vlan ${XR_EXPECTED_TRUNK_VLANS}
#
#    [Teardown]
#
#    Close Spawn     ${ROUTER_SPAWN}