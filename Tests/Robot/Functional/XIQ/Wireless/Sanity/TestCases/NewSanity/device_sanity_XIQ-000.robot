
*** Variables ***
${LOCATION}                 auto_location_01, Santa Clara, building_02, floor_04
${CONFIG_PUSH_SSID_01}              SSID_01
${CONFIG_PUSH_SSID_02}              SSID_02
${POLICY_01}                        dummy
${SSID_01}                          dummy
${NEW_SSID_NAME_1}                  dummy


#Update this time because we have an ap that is taking a bit longer
${MAX_CONFIG_PUSH_TIME}             600

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

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml
Resource     Tests/Robot/Functional/XIQ/Wireless/Sanity/Resources/wireless_networks_config.robot

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

    ${SW_SPAWN}=     Open Spawn          ${device1.ip}   ${device1.port}   ${device1.username}   ${device1.password}   ${device1.cli_type}
    # downgrade the device if needed
    ${DOWNGRADE_IQAGENT}=        downgrade iqagent      ${device1.cli_type}       ${SW_SPAWN}
    Should Be Equal As Integers         ${DOWNGRADE_IQAGENT}       1

    Close Spawn     ${SW_SPAWN}

    # log in the user
    Login User      ${tenant_username}      ${tenant_password}

Test Suite Teardown
    Clean Up Device
    Logout User
    Quit Browser

Clean Up Device
    ${search_result}=   Search Device       device_serial=${device1.serial}    ignore_cli_feedback=true
    # Disconnect from Extreme Cloud IQ
    Run Keyword If  '${search_result}' == '1'       Delete and Disconnect Device From Cloud

Delete and Disconnect Device From Cloud
    delete device   device_serial=${device1.serial}
    ${SPAWN_CONNECTION}=      Open Spawn    ${device1.ip}     ${device1.port}   ${device1.username}   ${device1.password}    ${device1.cli_type}

    ${DISC_STATUS_RESULT}=     disconnect device from cloud     ${device1.cli_type}     ${SPAWN_CONNECTION}
    Should Be Equal As Strings                  ${DISC_STATUS_RESULT}       1

    Close Spawn       ${SPAWN_CONNECTION}


Disable SSH and Close Device360 Window
    ${DISABLE_SSH}=                     Device360 Disable SSH Connectivity
    Should Be Equal As Integers         ${DISABLE_SSH}     1

    ${CLOSE_DEVICE360_WINDOW}=          Close Device360 Window
    Should Be Equal As Integers         ${CLOSE_DEVICE360_WINDOW}     1

Validate Device Information
    @{column_list}=    Create List    MGT IP ADDRESS    MAC
    ${DEVICE_INFOMATION}=   get_device_column_information  ${device1.serial}    ${column_list}
    Run Keyword If  '${device1.cli_type}' != 'WING-AP'    Validate Device Managment IP Information   ${DEVICE_INFOMATION}
    ${DEVICE_MAC}=                 Get From Dictionary      ${DEVICE_INFOMATION}    MAC
    Should Be Equal As Strings    '${DEVICE_MAC}'           '${device1.mac}'

Validate Device Managment IP Information
    [Arguments]    ${DEVICE_INFOMATION}
    ${DEVICE_IP}=                  Get From Dictionary      ${DEVICE_INFOMATION}    MGT_IP_ADDRESS
    Should Be Equal As Strings    '${DEVICE_IP}'           '${device1.ip}'

clean up policy and ssid
    [Arguments]    ${POLICY_01}     ${SSID_01}      ${NEW_SSID_NAME_1}
    ${DELETE_NW_POLICY_STATUS}=     Delete network policy      ${POLICY_01}
    should be equal as integers     ${DELETE_NW_POLICY_STATUS}               1

    ${SSID_DLT_STATUS}=             Delete SSIDs        ${SSID_01}      ${NEW_SSID_NAME_1}
    should be equal as strings      '1'                 '${SSID_DLT_STATUS}'

*** Test Cases ***
step1: ssh_test
    [Documentation]     Log into Device

    [Tags]              onboard        development

    ${SPAWN}=        Open Spawn          ${device1.ip}   ${device1.port}      ${device1.username}       ${device1.password}        ${device1.cli_type}
    Close Spawn      ${SPAWN}

step2: Advanced Onboard Device on XIQ
    [Documentation]         Checks for Advanced Device onboarding on XIQ

    [Tags]                  onboard      development

    Depends On              step1

    Clean Up Device

    ${ONBOARD_RESULT}=      Advance Onboard Device         ${device1.serial}    device_make=${device1.make}   dev_location=${LOCATION}  device_mac=${device1.mac}
    Should Be Equal As Strings                  ${ONBOARD_RESULT}       1

    ${SPAWN_CONNECTION}=      Open Spawn    ${device1.ip}    ${device1.port}   ${device1.username}    ${device1.password}    ${device1.cli_type}

    ${CONF_STATUS_RESULT}=      Configure Device To Connect To Cloud    ${device1.cli_type}       ${generic_capwap_url}     ${SPAWN_CONNECTION}
    Should Be Equal As Strings                  ${CONF_STATUS_RESULT}       1

    Close Spawn       ${SPAWN_CONNECTION}

    ${ONLINE_STATUS_RESULT}=    wait until device online     ${device1.serial}
    Should Be Equal As Strings                  ${ONLINE_STATUS_RESULT}       1

    ${MANAGED_STATUS_RESULT}=   wait until device managed   ${device1.serial}
    Should Be Equal As Strings                  ${MANAGED_STATUS_RESULT}      1

    ${DEVICE_STATUS_RESULT}=    get device status      ${device1.serial}
    Should Be Equal As Strings                  ${DEVICE_STATUS_RESULT}      green


step3: Verify Information on Device page (Advanced onboarding)
    [Documentation]         Verify Information on Device page

    [Tags]                  onboard     development

    Depends On              step2
    Validate Device Information

Step4: Simple Onboard Device on XIQ
    [Documentation]         Checks for Device onboarding on XIQ

    [Tags]                  onboard      development

    Depends On              step3

    Clean Up Device

    ${ONBOARD_RESULT}=          onboard device      ${device1.serial}       ${device1.make}   device_mac=${device1.mac}  location=${LOCATION}
    Should Be Equal As Strings                  ${ONBOARD_RESULT}       1

    ${SPAWN_CONNECTION}=      Open Spawn    ${device1.ip}    ${device1.port}   ${device1.username}    ${device1.password}    ${device1.cli_type}

    ${CONF_STATUS_RESULT}=      Configure Device To Connect To Cloud     ${device1.cli_type}       ${generic_capwap_url}     ${SPAWN_CONNECTION}
    Should Be Equal As Strings                  ${CONF_STATUS_RESULT}       1

    Close Spawn       ${SPAWN_CONNECTION}

    ${ONLINE_STATUS_RESULT}=    wait until device online     ${device1.serial}
    Should Be Equal As Strings                  ${ONLINE_STATUS_RESULT}       1

    ${MANAGED_STATUS_RESULT}=   wait until device managed   ${device1.serial}
    Should Be Equal As Strings                  ${MANAGED_STATUS_RESULT}      1

    ${DEVICE_STATUS_RESULT}=    get device status      ${device1.serial}
    Should Be Equal As Strings                  ${DEVICE_STATUS_RESULT}      green

step5: Verify Information on Device page (Simple onboaring)
    [Documentation]         Verify Information on Device page

    [Tags]                  onboard      development

    Depends On              step4
    Validate Device Information

# Waiting for the page to be refreshed in XIQ, this will only support AH-AP Only
# and will need to be expanded for all other device.
#Step6: Generate And Validate Fake Alarms (AH-AP Only)
#    [Documentation]    Chek the generation of alarms
#
#    [Tags]             verify_alarms    development
#
#    Depends On         step5
#
#    # FIXME Need to increase Support for all Devices
#    # Check to see if this test is supported on the device type
#    @{supported_cli_types}=    Create List   AH-AP
#    check_cli_type_and_skip     ${supported_cli_types}     ${device1.cli_type}
#
#    ${DEVICE_STATUS}=                   Get Device Status       device_mac=${device1.mac}
#    Should contain any                  ${DEVICE_STATUS}    green     config audit mismatch
#
#    ${CLEAR_ALARM_STATUS}=              Clear Alarm                       CRITICAL
#
#    ${SEND_CMD_STATUS}=                 Send Cmd On Device Advanced Cli    device_serial=${device1.serial}    cmd=_test trap-case alert failure
#    Should Not Be Equal As Strings      ${SEND_CMD_STATUS}          '-1'
#    sleep                               120s
#    ${ALARM_DETAILS}=                   Get Alarm Details                  CRITICAL
#    should be equal as strings          '${ALARM_DETAILS}[severity]'       'CRITICAL'
#    should be equal as strings          '${ALARM_DETAILS}[category]'       'System'
#    should be equal as strings          '${ALARM_DETAILS}[description]'    'fan failure.'
#    should be equal as strings          '${ALARM_DETAILS}[deviceMac]'      '${device1.mac}'


Step7: Enable SSH on Switch and Confirm SSH Session Can Be Established
    [Documentation]     Enables SSH for the Switch

    [Tags]              ssh     development

    Depends On          step5

    enable ssh availability

    &{ip_port_info}=                    Device360 Enable SSH CLI Connectivity   ${device1.mac}  run_time=30
    ${ip}=                              Get From Dictionary  ${ip_port_info}  ip
    ${port}=                            Get From Dictionary  ${ip_port_info}  port

    Should not be Empty     ${ip}
    Should not be Empty     ${port}
    ${ssh_spawn}=                       Open Spawn    ${ip}  ${port}  ${device1.username}  ${device1.password}  ${device1.cli_type}  pxssh=True
    ${close_result}=                    Close Spawn  ${ssh_spawn}  pxssh=True

    [Teardown]  Disable SSH and Close Device360 Window


Step8: Enable SSH on Switch and Confirm Only a Single SSH Session Can Be Established
    [Documentation]     Enable SSH on Switch and Confirm Only a Single SSH Session Can Be Established

    [Tags]              ssh      development

    Depends On           step5


    enable ssh availability

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


Step9: Verification of config push complete config update (AH-AP Only)
    [Documentation]             Verification of config push complete config update
    [Tags]                      push_config     development
    Depends On                  step5

    @{supported_cli_types}=    Create List   AH-AP
    check_cli_type_and_skip     ${supported_cli_types}     ${device1.cli_type}

    ${POLICY_01}=               Get Random String
    ${SSID_01}=                 Get Random String

    Set Global Variable          ${POLICY_01}
    Set Global Variable          ${SSID_01}
    Set To Dictionary           ${CONFIG_PUSH_OPEN_NW_01}    ssid_name=${SSID_01}
    Log to Console              ${CONFIG_PUSH_OPEN_NW_01}

    ${CREATE_NW_POLICY_STATUS}=     Create Network Policy   policy=${POLICY_01}      &{CONFIG_PUSH_OPEN_NW_01}
    should be equal as integers     ${CREATE_NW_POLICY_STATUS}               1

    ${DEPLOY_STATUS}=               Deploy Network Policy with Complete Update      ${POLICY_01}          ${ap1.serial}
    should be equal as integers     ${DEPLOY_STATUS}               1

    ${CONNECTED_STATUS}=            Wait Until Device Online                ${device1.serial}   None   30   20
    Should Be Equal as Integers     ${CONNECTED_STATUS}          1

    ${SPAWN}=               Open Spawn      ${device1.ip}   ${device1.port}      ${device1.username}       ${device1.password}        ${device1.cli_type}
    ${OUTPUT1}=             Send            ${SPAWN}                show ssid

    Should Contain                          ${OUTPUT1}                  ${SSID_01}
    Close Spawn        ${SPAWN}


Step10: Verification of config push delta update (AH-AP Only)
    [Documentation]         Verification of config push delta update
    [Tags]                  push_config     development
    Depends On              step5

    @{supported_cli_types}=    Create List   AH-AP
    check_cli_type_and_skip     ${supported_cli_types}     ${device1.cli_type}

    ${NEW_SSID_NAME_1}=             Get Random String
    Set Global Variable             ${NEW_SSID_NAME_1}

    ${EDIT_STATUS}=                 Edit Network Policy SSID                    ${POLICY_01}          ${SSID_01}     ${NEW_SSID_NAME_1}
    should be equal as integers             ${EDIT_STATUS}              1

    ${DEPLOY_STATUS}=       Deploy Network Policy with Delta Update     ${POLICY_01}          ${ap1.serial}
    should be equal as integers             ${DEPLOY_STATUS}            1

    ${CONNECTED_STATUS}=    Wait Until Device Online                ${device1.serial}
    Should Be Equal as Integers             ${CONNECTED_STATUS}          1

    ${SPAWN}=               Open Spawn      ${device1.ip}   ${device1.port}      ${device1.username}       ${device1.password}        ${device1.cli_type}
    ${OUTPUT1}=             Send            ${SPAWN}                show ssid

    Should Contain                          ${OUTPUT1}                  ${NEW_SSID_NAME_1}
    Close Spawn        ${SPAWN}

# Not sure if this should be a part of Sanity
# yes, froce the upgrade
#
#Step11: Firmware upgrade to lastest version (AH-AP Only)
#    [Documentation]         Verify IQ engine upgrade to lastest version ( we should just make sure it was upgraded )
#    [Tags]			        push_config     development
#    Depends On             step1
#
#    @{supported_cli_types}=    Create List   AH-AP
#    check_cli_type_and_skip     ${supported_cli_types}     ${device1.cli_type}
#
#    ${SPAWN1}=              Open Spawn      ${device1.ip}   ${device1.port}      ${device1.username}       ${device1.password}        ${device1.cli_type}
#
#    ${CLOCK_OUPUT1}=        Send            ${SPAWN1}         show clock
#    ${REBOOT_OUPUT1}=       Send            ${SPAWN1}         show reboot schedule
#    Should Not Contain      ${REBOOT_OUPUT1}     Next reboot Scheduled
#
#    ${VERSION_DETAIL1}=     Send            ${SPAWN1}         show version detail
#
#    Should Contain          ${VERSION_DETAIL1}   Running image:      Current version
#    Should Contain          ${VERSION_DETAIL1}   Backup version:     HiveOS 10.0r3
#    Should Contain          ${VERSION_DETAIL1}   Load after reboot:  Current version
#
#    ${AP_BUILD_VERSION1}=   Get AP Version              ${SPAWN1}
#
#    ${LATEST_VERSION}=      Upgrade Device To Latest Version            ${ap1.serial}
#    Should Not be Empty     ${LATEST_VERSION}
#
#    Sleep                   ${ap_reboot_wait}
#
#    ${CONNECTED_STATUS}=    Wait Until Device Online                ${device1.serial}       retry_count=15
#    Should Be Equal as Integers             ${CONNECTED_STATUS}          1
#
#    ${REBOOT_STATUS}=    Wait Until Device Reboots               ${device1.serial}
#    Should Be Equal as Integers             ${REBOOT_STATUS}          1
#
#    Close Spawn             ${SPAWN1}
#
#    ${SPAWN2}=              Open Spawn      ${device1.ip}   ${device1.port}      ${device1.username}       ${device1.password}        ${device1.cli_type}
#    Should not be equal as Strings          '${SPAWN2}'        '-1'
#
#    ${CLOCK_OUPUT2}=        Send            ${SPAWN2}         show clock
#
#    ${REBOOT_OUPUT2}=       Send            ${SPAWN2}         show reboot schedule
#    Should Not Contain      ${REBOOT_OUPUT2}     Next reboot Scheduled
#
#    ${VERSION_DETAIL2}=     Send            ${SPAWN2}         show version detail
#
#    Should Contain          ${VERSION_DETAIL2}   Running image:      Current version
#    Should Contain          ${VERSION_DETAIL2}   Backup version:     HiveOS 10.0r3
#    Should Contain          ${VERSION_DETAIL2}   Load after reboot:  Current version
#    Should Contain          ${VERSION_DETAIL2}   Uptime:             0 weeks, 0 days, 0 hours
#
#    ${AP_BUILD_VERSION2}=   Get AP Version              ${SPAWN2}
#    Should Be Equal As Strings  ${LATEST_VERSION}           ${AP_BUILD_VERSION2}
#
#    Close Spawn        ${SPAWN2}