# Author        : Rameswar
# Date          : March 30th 2020
# Description   :
#
# Topology      :
# Host ----- Cloud

*** Variables ***
${CONFIG_PUSH_SSID_01}              SSID_01
${CONFIG_PUSH_SSID_02}              SSID_02
${POLICY_01}                        dummy
${SSID_01}                          dummy
${NEW_SSID_NAME_1}                  dummy



*** Settings ***
Library     Collections
Library     common/Utils.py
Library     common/Cli.py
Library     common/Mu.py
Library     common/TestFlow.py
Library     common/ImageHandler.py
Library     common/ImageAnalysis.py

Library     xiq/flows/common/Login.py
Library     xiq/flows/manage/Client.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/configure/ExpressNetworkPolicies.py
Library     xiq/flows/configure/CommonObjects.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}

Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml
Resource     Tests/Robot/Functional/XIQ/Wireless/Sanity/Resources/wireless_networks_config.robot

Force Tags   testbed_1_node

Suite Teardown  Test Suite Clean Up

*** Keywords ***

Test Suite Clean Up
    [Tags]			        cleanup         test7	production
    ${LOGIN_STATUS}=                Login User              ${tenant_username}      ${tenant_password}
    should be equal as integers     ${LOGIN_STATUS}               1

    ${DELETE_DEVICE_STATUS}=        Delete Device                  device_serial=${ap1.serial}
    should be equal as integers     ${DELETE_DEVICE_STATUS}               1

    ${DELETE_NW_POLICY_STATUS}=     Delete network policy      ${POLICY_01}
    should be equal as integers     ${DELETE_NW_POLICY_STATUS}               1

    ${SSID_DLT_STATUS}=             Delete SSIDs        ${SSID_01}      ${NEW_SSID_NAME_1}
    should be equal as strings      '1'                 '${SSID_DLT_STATUS}'

    [Teardown]   run keywords               logout user
    ...                                     quit browser

*** Test Cases ***
TCCS-11310: Verification of config push complete config update
    [Documentation]             Verification of config push complete config update
    [Tags]                      production      tccs_11310
    ${POLICY_01}=               Get Random String
    ${SSID_01}=                 Get Random String

    Set Global Variable          ${POLICY_01}
    Set Global Variable          ${SSID_01}
    Set To Dictionary           ${CONFIG_PUSH_OPEN_NW_01}    ssid_name=${SSID_01}
    Log to Console              ${CONFIG_PUSH_OPEN_NW_01}

    ${LOGIN_STATUS}=                Login User              ${tenant_username}      ${tenant_password}
    should be equal as integers     ${LOGIN_STATUS}               1

    ${CREATE_NW_POLICY_STATUS}=     Create Network Policy   ${POLICY_01}      ${CONFIG_PUSH_OPEN_NW_01}
    should be equal as integers     ${CREATE_NW_POLICY_STATUS}               1

    ${DEPLOY_STATUS}=               Deploy Network Policy with Complete Update      ${POLICY_01}          ${ap1.serial}
    should be equal as integers     ${DEPLOY_STATUS}               1

    ${CONNECTED_STATUS}=            Wait Until Device Online                ${ap1.serial}   None   30   20
    Should Be Equal as Integers     ${CONNECTED_STATUS}          1

    ${SPAWN}=               Open Spawn      ${ap1.ip}   ${ap1.port}      ${ap1.username}       ${ap1.password}        ${ap1.cli_type}
    ${OUTPUT1}=             Send            ${SPAWN}                show ssid

    Should Contain                          ${OUTPUT1}                  ${SSID_01}

    [Teardown]   run keywords       logout user
    ...          AND                quit browser
    ...          AND                Close Spawn        ${SPAWN}

TCCS-11309: Verification of config push delta update
    [Documentation]         Verification of config push delta update
    [Tags]                  production      tccs_11309
    Depends On              TCCS-11310
    ${LOGIN_STATUS}=                Login User              ${tenant_username}      ${tenant_password}
    should be equal as integers     ${LOGIN_STATUS}               1

    ${NEW_SSID_NAME_1}=             Get Random String
    Set Global Variable             ${NEW_SSID_NAME_1}

    ${EDIT_STATUS}=                 Edit Network Policy SSID                    ${POLICY_01}          ${SSID_01}     ${NEW_SSID_NAME_1}
    should be equal as integers             ${EDIT_STATUS}              1

    ${DEPLOY_STATUS}=       Deploy Network Policy with Delta Update     ${POLICY_01}          ${ap1.serial}
    should be equal as integers             ${DEPLOY_STATUS}            1

    ${CONNECTED_STATUS}=    Wait Until Device Online                ${ap1.serial}
    Should Be Equal as Integers             ${CONNECTED_STATUS}          1

    ${SPAWN}=               Open Spawn      ${ap1.ip}   ${ap1.port}      ${ap1.username}       ${ap1.password}        ${ap1.cli_type}
    ${OUTPUT1}=             Send            ${SPAWN}                show ssid

    Should Contain                          ${OUTPUT1}                  ${NEW_SSID_NAME_1}

    [Teardown]   run keywords               logout user
    ...             AND                     quit browser
    ...             AND                     Close Spawn        ${SPAWN}

TCCS-7373: IQ engine upgrade to lastest version
    [Documentation]         Verify IQ engine upgrade to lastest version
    [Tags]			        production      tccs_7373
    ${SPAWN1}=              Open Spawn      ${ap1.ip}   ${ap1.port}      ${ap1.username}       ${ap1.password}        ${ap1.cli_type}
    Should not be equal as Strings          '${SPAWN1}'        '-1'

    ${CLOCK_OUPUT1}=        Send            ${SPAWN1}         show clock
    ${REBOOT_OUPUT1}=       Send            ${SPAWN1}         show reboot schedule
    Should Not Contain      ${REBOOT_OUPUT1}     Next reboot Scheduled

    ${VERSION_DETAIL1}=     Send            ${SPAWN1}         show version detail

    Should Contain          ${VERSION_DETAIL1}   Running image:      Current version
    Should Contain          ${VERSION_DETAIL1}   Backup version:     HiveOS 10.0r3
    Should Contain          ${VERSION_DETAIL1}   Load after reboot:  Current version

    ${AP_BUILD_VERSION1}=   Get AP Version              ${SPAWN1}

    ${LOGIN_STATUS}=        Login User      ${tenant_username}      ${tenant_password}
    should be equal as integers     ${LOGIN_STATUS}               1

    ${LATEST_VERSION}=      Upgrade Device To Latest Version            ${ap1.serial}
    Should Not be Empty     ${LATEST_VERSION}

    Sleep                   ${ap_reboot_wait}

    ${CONNECTED_STATUS}=    Wait Until Device Online                ${ap1.serial}       retry_count=15
    Should Be Equal as Integers             ${CONNECTED_STATUS}          1

    ${REBOOT_STATUS}=    Wait Until Device Reboots               ${ap1.serial}
    Should Be Equal as Integers             ${REBOOT_STATUS}          1

    Close Spawn             ${SPAWN1}

    ${SPAWN2}=              Open Spawn      ${ap1.ip}   ${ap1.port}      ${ap1.username}       ${ap1.password}        ${ap1.cli_type}
    Should not be equal as Strings          '${SPAWN2}'        '-1'

    ${CLOCK_OUPUT2}=        Send            ${SPAWN2}         show clock

    ${REBOOT_OUPUT2}=       Send            ${SPAWN2}         show reboot schedule
    Should Not Contain      ${REBOOT_OUPUT2}     Next reboot Scheduled

    ${VERSION_DETAIL2}=     Send            ${SPAWN2}         show version detail

    Should Contain          ${VERSION_DETAIL2}   Running image:      Current version
    Should Contain          ${VERSION_DETAIL2}   Backup version:     HiveOS 10.0r3
    Should Contain          ${VERSION_DETAIL2}   Load after reboot:  Current version
    Should Contain          ${VERSION_DETAIL2}   Uptime:             0 weeks, 0 days, 0 hours

    ${AP_BUILD_VERSION2}=   Get AP Version              ${SPAWN2}
    Should Be Equal As Strings  ${LATEST_VERSION}           ${AP_BUILD_VERSION2}

    Close Spawn        ${SPAWN2}

    [Teardown]   run keywords               logout user
    ...             AND                     quit browser
