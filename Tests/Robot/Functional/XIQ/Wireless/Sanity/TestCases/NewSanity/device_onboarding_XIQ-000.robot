
*** Variables ***
${LOCATION}                 auto_location_01, Santa Clara, building_02, floor_04

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

    # downgrade the device if needed
    downgrade iqagent  ${device1.ip}   ${device1.port}   ${device1.username}   ${device1.password}   ${device1.cli_type}

    # log in the user
    Login User      ${tenant_username}      ${tenant_password}

Test Suite Teardown
    Clean Up Device
    Logout User
    Quit Browser

Clean Up Device
    ${search_result}=   Search Device       device_serial=${device1.serial}    ignore_cli_feedback=true
    Run Keyword If  '${search_result}' == '1'       delete device   device_serial=${device1.serial}

Disable SSH and Close Device360 Window
    ${DISABLE_SSH}=                     Device360 Disable SSH Connectivity
    Should Be Equal As Integers         ${DISABLE_SSH}     1

    ${CLOSE_DEVICE360_WINDOW}=          Close Device360 Window
    Should Be Equal As Integers         ${CLOSE_DEVICE360_WINDOW}     1

Validate Device Information
    @{column_list}=    Create List    MGT IP ADDRESS    MAC
    ${DEVICE_INFOMATION}=   get_device_column_information  ${device1.serial}    ${column_list}
    # This need to be removed for the WING until we write a new bug
    Run Keyword If      '${device1.cli_type}' != 'WING-AP'    Validate Device Managment IP Information   ${DEVICE_INFOMATION}
    ${DEVICE_MAC}=                 Get From Dictionary      ${DEVICE_INFOMATION}    MAC
    Should Be Equal As Strings    '${DEVICE_MAC}'           '${device1.mac}'

Validate Device Managment IP Information
    [Arguments]    ${DEVICE_INFOMATION}
    ${DEVICE_IP}=                  Get From Dictionary      ${DEVICE_INFOMATION}    MGT_IP_ADDRESS
    Should Be Equal As Strings    '${DEVICE_IP}'           '${device1.ip}'

*** Test Cases ***
ssh_test_step1: ssh_test
    [Documentation]     Log into Device

    [Tags]              simple_onboard      advanced_onboard    development

    ${SPAWN}=        Open Spawn          ${device1.ip}   ${device1.port}      ${device1.username}       ${device1.password}        ${device1.cli_type}
    Close Spawn      ${SPAWN}

simple_onboard_step2: Onboard Device on XIQ
    [Documentation]         Checks for Device onboarding on XIQ

    [Tags]                  simple_onboard      development

    Depends On              ssh_test_step1

    Clean Up Device

    ${ONBOARD_RESULT}=          onboard device      ${device1.serial}       ${device1.make}   device_mac=${device1.mac}  location=${LOCATION}
    Should Be Equal As Strings                  ${ONBOARD_RESULT}       1

    ${CONF_STATUS_RESULT}=      configure device to connect to cloud    ${device1.cli_type}   ${device1.ip}    ${device1.port}   ${device1.username}    ${device1.password}    ${generic_capwap_url}
    Should Be Equal As Strings                  ${CONF_STATUS_RESULT}       1

    ${ONLINE_STATUS_RESULT}=    wait until device online     ${device1.serial}
    Should Be Equal As Strings                  ${ONLINE_STATUS_RESULT}       1

    ${MANAGED_STATUS_RESULT}=   wait until device managed   ${device1.serial}
    Should Be Equal As Strings                  ${MANAGED_STATUS_RESULT}      1

    ${DEVICE_STATUS_RESULT}=    get device status      ${device1.serial}
    Should Be Equal As Strings                  ${DEVICE_STATUS_RESULT}      green

verify_info_on_devices_page_step3: Verify Information on Device page
    [Documentation]         Verify Information on Device page

    [Tags]                  simple_onboard      development

    Depends On              simple_onboard_step1
    Validate Device Information

adavnced_onboard_step4: Advanced Onboard Device on XIQ
    [Documentation]         Checks for Advanced Device onboarding on XIQ

    [Tags]                  advanced_onboard      development

    Depends On              ssh_test_step1

    Clean Up Device

    ${ONBOARD_RESULT}=      Advance Onboard Device         ${device1.serial}    device_make=${device1.make}   dev_location=${LOCATION}  device_mac=${device1.mac}
    Should Be Equal As Strings                  ${ONBOARD_RESULT}       1

    ${CONF_STATUS_RESULT}=      configure device to connect to cloud    ${device1.cli_type}   ${device1.ip}    ${device1.port}   ${device1.username}    ${device1.password}    ${generic_capwap_url}
    Should Be Equal As Strings                  ${CONF_STATUS_RESULT}       1

    ${ONLINE_STATUS_RESULT}=    wait until device online     ${device1.serial}
    Should Be Equal As Strings                  ${ONLINE_STATUS_RESULT}       1

    ${MANAGED_STATUS_RESULT}=   wait until device managed   ${device1.serial}
    Should Be Equal As Strings                  ${MANAGED_STATUS_RESULT}      1

    ${DEVICE_STATUS_RESULT}=    get device status      ${device1.serial}
    Should Be Equal As Strings                  ${DEVICE_STATUS_RESULT}      green


verify_info_on_devices_page_step5: Verify Information on Device page (Advanced onboarding)
    [Documentation]         Verify Information on Device page

    [Tags]                  advanced_onboard     development

    Depends On              adavnced_onboard_step4
    Validate Device Information

#Generate_And_Validate_Fake_Alarms_Step6: Generate And Validate Fake Alarms
#    [Documentation]    Chek the generation of alarms
#
#    [Tags]             verify_alarms    development
#
#    Depends On         simple_onboard_step1
#
#     # FIXME Need to increase Support for all Devices
#     # Check to see if this test is supported on the device type
#     @{supported_cli_types}=    Create List   AH-AP
#     check_cli_type_and_skip     ${supported_cli_types}     ${device1.cli_type}
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


Switch SSH Step6: Enable SSH on Switch and Confirm SSH Session Can Be Established
    [Documentation]     Enables SSH for the Switch

    [Tags]              ssh_switch      development

    Depends On           simple_onboard_step1

    &{ip_port_info}=                    Device360 Enable SSH CLI Connectivity   ${device1.mac}  run_time=30
    ${ip}=                              Get From Dictionary  ${ip_port_info}  ip
    ${port}=                            Get From Dictionary  ${ip_port_info}  port

    Should not be Empty     ${ip}
    Should not be Empty     ${port}
    ${ssh_spawn}=                       Open Spawn    ${ip}  ${port}  ${device1.username}  ${device1.password}  ${device1.cli_type}  pxssh=True
    ${close_result}=                    Close Spawn  ${ssh_spawn}  pxssh=True

    [Teardown]  Disable SSH and Close Device360 Window


Switch SSH Step7: Enable SSH on Switch and Confirm Only a Single SSH Session Can Be Established
    [Documentation]     Enable SSH on Switch and Confirm Only a Single SSH Session Can Be Established

    [Tags]              ssh_switch      development

    Depends On           simple_onboard_step1

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