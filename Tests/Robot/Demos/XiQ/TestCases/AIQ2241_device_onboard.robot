# Author        : Cserbu
# Date          : Sept 2022
# Description   : These tests are related to AIQ-2241 and are used to onboard a device several times in different ways (quick, advanced onboarding)
#                 and also switching between these 2 types of onboarding.
#                 The goal of this test is to consistently cause the device to not onboard.
#
#                 step1: Quick Onboard Device on XIQ
#                 step2: Advanced Onboard Device on XIQ
#                 step3: Switching Between Advanced Onboard And Quick Onboard

*** Variables ***
${LOCATION}                 auto_location_01, Santa Clara, building_02, floor_04
${CONFIG_PUSH_SSID_01}              SSID_01
${CONFIG_PUSH_SSID_02}              SSID_02
${POLICY_01}                        dummy
${SSID_01}                          dummy
${NEW_SSID_NAME_1}                  dummy



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
Library     extauto/xiq/flows/common/Navigator.py

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

    ${LOGIN_STATUS}=              Login User          ${tenant_username}      ${tenant_password}     check_warning_msg=True
    should be equal as integers             ${LOGIN_STATUS}               1

Test Suite Teardown
    Clean Up Device
    Logout User
    Quit Browser

Clean Up Device
    Navigate To Devices
    Refresh Devices Page
    delete device   device_serial=${device1.serial}

    ${SPAWN_CONNECTION}=     Open Spawn      ${device1.ip}    ${device1.port}   ${device1.username}    ${device1.password}   ${device1.cli_type}
    ${DISC_STATUS}=          disconnect device from cloud           ${device1.cli_type}       ${SPAWN_CONNECTION}
    Should Be Equal As Strings                  ${DISC_STATUS}       1
    Close Spawn         ${SPAWN_CONNECTION}


*** Test Cases ***
step1: Quick Onboard Device on XIQ
    [Documentation]         Checks for Quick Device onboarding on XIQ

    [Tags]                  onboard      development


    FOR  ${index}   IN RANGE   5
        Log    ${index}

        Clean Up Device

        ${ONBOARD_RESULT}=          onboard device      ${device1.serial}       ${device1.make}   device_mac=${device1.mac}  location=${LOCATION}
        Should Be Equal As Strings                  ${ONBOARD_RESULT}       1

        ${SPAWN_CONNECTION}=     Open Spawn      ${device1.ip}    ${device1.port}   ${device1.username}    ${device1.password}   ${device1.cli_type}
        ${CONF_STATUS_RESULT}=      configure device to connect to cloud    ${device1.cli_type}     ${generic_capwap_url}        ${SPAWN_CONNECTION}
        Should Be Equal As Strings                  ${CONF_STATUS_RESULT}       1
        Close Spawn         ${SPAWN_CONNECTION}

        ${ONLINE_STATUS_RESULT}=    wait until device online     ${device1.serial}
        Should Be Equal As Strings                  ${ONLINE_STATUS_RESULT}       1

        ${MANAGED_STATUS_RESULT}=   wait until device managed   ${device1.serial}
        Should Be Equal As Strings                  ${MANAGED_STATUS_RESULT}      1

        ${DEVICE_STATUS_RESULT}=    get device status      ${device1.serial}
        Should Be Equal As Strings                  ${DEVICE_STATUS_RESULT}      green
    END
step2: Advanced Onboard Device on XIQ
    [Documentation]         Checks for Advanced Device onboarding on XIQ

    [Tags]                  onboard      development
    Depends On              step1

    FOR     ${index}     IN RANGE   5
        Log    ${index}
        Clean Up Device

        ${ONBOARD_RESULT}=      Advance Onboard Device         ${device1.serial}    device_make=${device1.make}   dev_location=${LOCATION}  device_mac=${device1.mac}
        Should Be Equal As Strings                  ${ONBOARD_RESULT}       1

        ${SPAWN_CONNECTION}=     Open Spawn      ${device1.ip}    ${device1.port}   ${device1.username}    ${device1.password}   ${device1.cli_type}
        ${CONF_STATUS_RESULT}=      configure device to connect to cloud    ${device1.cli_type}     ${generic_capwap_url}        ${SPAWN_CONNECTION}
        Should Be Equal As Strings                  ${CONF_STATUS_RESULT}       1
        Close Spawn         ${SPAWN_CONNECTION}

        ${ONLINE_STATUS_RESULT}=    wait until device online     ${device1.serial}
        Should Be Equal As Strings                  ${ONLINE_STATUS_RESULT}       1

        ${MANAGED_STATUS_RESULT}=   wait until device managed   ${device1.serial}
        Should Be Equal As Strings                  ${MANAGED_STATUS_RESULT}      1

        ${DEVICE_STATUS_RESULT}=    get device status      ${device1.serial}
        Should Be Equal As Strings                  ${DEVICE_STATUS_RESULT}      green

    END


step3: Switching Between Advanced Onboard And Quick Onboard
    [Documentation]         Switching Between Advanced Onboard And Quick Onboard

    [Tags]                  onboard      development
    Depends On              step2

    FOR  ${index}   IN RANGE   5
        Log    ${index}
        Clean Up Device

        ${ONBOARD_RESULT}=          onboard device      ${device1.serial}       ${device1.make}   device_mac=${device1.mac}  location=${LOCATION}
        Should Be Equal As Strings                  ${ONBOARD_RESULT}       1

        ${SPAWN_CONNECTION}=     Open Spawn      ${device1.ip}    ${device1.port}   ${device1.username}    ${device1.password}   ${device1.cli_type}
        ${CONF_STATUS_RESULT}=      configure device to connect to cloud    ${device1.cli_type}     ${generic_capwap_url}        ${SPAWN_CONNECTION}
        Should Be Equal As Strings                  ${CONF_STATUS_RESULT}       1
        Close Spawn         ${SPAWN_CONNECTION}

        ${ONLINE_STATUS_RESULT}=    wait until device online     ${device1.serial}
        Should Be Equal As Strings                  ${ONLINE_STATUS_RESULT}       1

        ${MANAGED_STATUS_RESULT}=   wait until device managed   ${device1.serial}
        Should Be Equal As Strings                  ${MANAGED_STATUS_RESULT}      1

        ${DEVICE_STATUS_RESULT}=    get device status      ${device1.serial}
        Should Be Equal As Strings                  ${DEVICE_STATUS_RESULT}      green

        Clean Up Device

        ${ONBOARD_RESULT}=      Advance Onboard Device         ${device1.serial}    device_make=${device1.make}   dev_location=${LOCATION}  device_mac=${device1.mac}
        Should Be Equal As Strings                  ${ONBOARD_RESULT}       1

        ${SPAWN_CONNECTION}=     Open Spawn      ${device1.ip}    ${device1.port}   ${device1.username}    ${device1.password}   ${device1.cli_type}
        ${CONF_STATUS_RESULT}=      configure device to connect to cloud    ${device1.cli_type}     ${generic_capwap_url}        ${SPAWN_CONNECTION}
        Should Be Equal As Strings                  ${CONF_STATUS_RESULT}       1
        Close Spawn         ${SPAWN_CONNECTION}

        ${ONLINE_STATUS_RESULT}=    wait until device online     ${device1.serial}
        Should Be Equal As Strings                  ${ONLINE_STATUS_RESULT}       1

        ${MANAGED_STATUS_RESULT}=   wait until device managed   ${device1.serial}
        Should Be Equal As Strings                  ${MANAGED_STATUS_RESULT}      1

        ${DEVICE_STATUS_RESULT}=    get device status      ${device1.serial}
        Should Be Equal As Strings                  ${DEVICE_STATUS_RESULT}      green

    END