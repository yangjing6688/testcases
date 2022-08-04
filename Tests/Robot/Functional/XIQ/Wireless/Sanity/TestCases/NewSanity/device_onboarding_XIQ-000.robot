
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

*** Test Cases ***
simple_onboard_step1: Onboard Device on XIQ
    [Documentation]         Checks for Device onboarding on XIQ

    [Tags]                  simple_onboard      development

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

#verify_info_on_devices_page_step2: Verify Information on Device page
#    [Documentation]         Verify Information on Device page
#
#    [Tags]                  verify_device_info
#
#    Depends On              simple_onboard_step1
#    ${DEVICE_ROW}=          get_device_row  device_mac=${device1.mac}
#    log to console      ${DEVICE_ROW}
#    ${SYS_INFO_360_PAGE}=          get_device_360_information   ${device1.cli_type}   device_mac=${device1.mac}
#    ${DEVICE_IP}=                  Get From Dictionary      ${SYS_INFO_360_PAGE}    ip_address
#    Should Be Equal As Strings    '${DEVICE_IP}'            '${device1.ip}'
#    ${DEVICE_MAC}=                 Get From Dictionary      ${SYS_INFO_360_PAGE}    mac_address
#    Should Be Equal As Strings    '${DEVICE_MAC}'           '${device1.mac}'
#    ${DEVICE_SERIAL}=              Get From Dictionary      ${SYS_INFO_360_PAGE}    serial_number
#    Should Be Equal As Strings    '${DEVICE_SERIAL}'        '${device1.serial}'




