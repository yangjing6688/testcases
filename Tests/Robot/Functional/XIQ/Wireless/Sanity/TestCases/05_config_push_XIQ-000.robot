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
*** Keywords ***

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

    ${result}=                  Login User              ${tenant_username}      ${tenant_password}
    ${POLICY_STATUS}=           Create Network Policy   policy=${POLICY_01}      &{CONFIG_PUSH_OPEN_NW_01}
    ${DEPLOY_STATUS}=           Deploy Network Policy with Complete Update      ${POLICY_01}          ${ap1.serial}

    Wait Until Device Online    ${ap1.serial}  None   30   20

    ${SPAWN}=               Open Spawn      ${ap1.ip}   ${ap1.port}      ${ap1.username}       ${ap1.password}        ${ap1.cli_type}
    ${OUTPUT1}=             Send            ${SPAWN}                show ssid

    should be equal as integers             ${POLICY_STATUS}            1
    should be equal as integers             ${DEPLOY_STATUS}            1
    Should Contain                          ${OUTPUT1}                  ${SSID_01}

    [Teardown]   run keywords       logout user
    ...          AND                quit browser
    ...          AND                Close Spawn        ${SPAWN}

TCCS-11309: Verification of config push delta update
    [Documentation]         Verification of config push delta update

    [Tags]                  production      tccs_11309

    Depends On              tccs_11310
    ${result}=              Login User      ${tenant_username}          ${tenant_password}
    ${NEW_SSID_NAME_1}=     Get Random String
    Set Global Variable    ${NEW_SSID_NAME_1}

    ${EDIT_STATUS}=         Edit Network Policy SSID                    ${POLICY_01}          ${SSID_01}     ${NEW_SSID_NAME_1}
    ${DEPLOY_STATUS}=       Deploy Network Policy with Delta Update     ${POLICY_01}          ${ap1.serial}
    Wait Until Device Online    ${ap1.serial}

    ${SPAWN}=               Open Spawn      ${ap1.ip}   ${ap1.port}      ${ap1.username}       ${ap1.password}        ${ap1.cli_type}
    ${OUTPUT1}=             Send            ${SPAWN}                show ssid

    should be equal as integers             ${EDIT_STATUS}              1
    should be equal as integers             ${DEPLOY_STATUS}            1
    Should Contain                          ${OUTPUT1}                  ${NEW_SSID_NAME_1}

    [Teardown]   run keywords               logout user
    ...             AND                     quit browser
    ...             AND                     Close Spawn        ${SPAWN}

TCCS-7373: IQ engine upgrade to lastest version
    [Documentation]         Verify IQ engine upgrade to lastest version

    [Tags]			        production      tccs_7373

    ${SPAWN1}=              Open Spawn      ${ap1.ip}   ${ap1.port}      ${ap1.username}       ${ap1.password}        ${ap1.cli_type}
    ${CLOCK_OUPUT1}=        Send            ${SPAWN1}         show clock
    ${REBOOT_OUPUT1}=       Send            ${SPAWN1}         show reboot schedule
    ${VERSION_DETAIL1}=     Send            ${SPAWN1}         show version detail
    ${AP_BUILD_VERSION1}=   Get AP Version              ${SPAWN1}

    Should Not Contain      ${REBOOT_OUPUT1}     Next reboot Scheduled
    Should Contain          ${VERSION_DETAIL1}   Running image:      Current version
    Should Contain          ${VERSION_DETAIL1}   Backup version:     HiveOS 10.0r3
    Should Contain          ${VERSION_DETAIL1}   Load after reboot:  Current version

    ${LOGIN_STATUS}=        Login User      ${tenant_username}      ${tenant_password}
    ${LATEST_VERSION}=      Upgrade Device To Latest Version            ${ap1.serial}
    Sleep                   30                          Sleep 30 Seconds

    Wait Until Device Reboots               ${ap1.serial}
    Close Spawn             ${SPAWN1}

    ${SPAWN2}=              Open Spawn      ${ap1.ip}   ${ap1.port}      ${ap1.username}       ${ap1.password}        ${ap1.cli_type}
    ${CLOCK_OUPUT2}=        Send            ${SPAWN2}         show clock
    ${REBOOT_OUPUT2}=       Send            ${SPAWN2}         show reboot schedule
    ${VERSION_DETAIL2}=     Send            ${SPAWN2}         show version detail
    ${AP_BUILD_VERSION2}=   Get AP Version              ${SPAWN2}

    Should Not Contain      ${REBOOT_OUPUT2}     Next reboot Scheduled
    Should Contain          ${VERSION_DETAIL2}   Running image:      Current version
    Should Contain          ${VERSION_DETAIL2}   Backup version:     HiveOS 10.0r3
    Should Contain          ${VERSION_DETAIL2}   Load after reboot:  Current version
    Should Contain          ${VERSION_DETAIL2}   Uptime:             0 weeks, 0 days, 0 hours

    Should Be Equal As Strings  ${LATEST_VERSION}           ${AP_BUILD_VERSION2}

    [Teardown]   run keywords               logout user
    ...             AND                     quit browser
    ...             AND                     Close Spawn        ${SPAWN2}

Tes7: Cleanup
    [Tags]			        cleanup         test7	production
    ${LOGIN_STATUS}=        Login User          ${tenant_username}      ${tenant_password}
    Delete Device           device_serial=${ap1.serial}
    Delete Network Policy   ${POLICY_01}
    Delete SSIDs            ${SSID_01}      ${NEW_SSID_NAME_1}
    [Teardown]   run keywords               logout user
    ...                                     quit browser
