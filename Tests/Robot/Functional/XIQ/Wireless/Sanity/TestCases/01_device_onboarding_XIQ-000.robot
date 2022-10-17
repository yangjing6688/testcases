# Author        : Rameswar
# Date          : January 15th 2020
# Description   : Basic Login Test Cases
#
# Topology      :
# Host ----- Cloud

*** Variables ***
${LOCATION}                 auto_location_01, Santa Clara, building_02, floor_04

*** Settings ***
Library     extauto/common/Cli.py
Library     extauto/common/TestFlow.py
Library     extauto/xiq/flows/common/Login.py
Library     extauto/xiq/flows/manage/Devices.py
Library     extauto/xiq/flows/globalsettings/GlobalSetting.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/device_commands.yaml
Variables    Environments/Config/waits.yaml

Force Tags   testbed_1_node
Suite Setup     Suite Setup
Suite Teardown  Suite Teardown

*** Keywords ***
Suite Setup
    ${LOGIN_STATUS}=                Login User          ${tenant_username}      ${tenant_password}     check_warning_msg=True
    should be equal as integers     ${LOGIN_STATUS}               1

    ${DELETE_DEVICE_STATUS}=            Delete Device       device_serial=${ap1.serial}
    should be equal as integers     ${DELETE_DEVICE_STATUS}               1

Suite Teardown
    Run Keywords        logout user
    ...                 quit browser

*** Test Cases ***
TCCS-7651_Step1: Onboard Aerohive AP
    [Documentation]         Checks for ap onboarding is success in case of valid scenario
    [Tags]                  production      tccs_7651       tccs_7651_step_1

    ${CHANGE_PASSWORD_STATUS}=      Change Device Password                  Aerohive123
    should be equal as integers     ${CHANGE_PASSWORD_STATUS}               1

    ${ONBOARD_RESULT}=              Onboard Device      ${ap1.serial}           ${ap1.make}       location=${LOCATION}
    should be equal as integers     ${ONBOARD_RESULT}       1

    ${search_result}=               Search AP Serial    ${ap1.serial}
    should be equal as integers     ${search_result}        1

TCCS-7651_Step2: Config AP to Report AIO and Check status
    [Documentation]     Configure Capwap client server
    [Tags]              production      tccs_7651       tccs_7651_step_2
    Depends On          TCCS-7651_Step1
    ${AP_SPAWN}=        Open Spawn          ${ap1.ip}   ${ap1.port}      ${ap1.username}       ${ap1.password}        ${ap1.cli_type}
    Should not be equal as Strings      '${AP_SPAWN}'        '-1'

    ${CONF_STATUS_RESULT}=      Configure Device To Connect To Cloud      ${ap1.cli_type}         ${capwap_url}       ${AP_SPAWN}
    Should Be Equal As Strings                  ${CONF_STATUS_RESULT}       1

    ${WAIT_STATUS_RESULT}=      Wait for Configure Device to Connect to Cloud       ${ap1.cli_type}         ${capwap_url}       ${AP_SPAWN}
    Should Be Equal As Strings                  ${WAIT_STATUS_RESULT}       1

    ${DEVICE_STATUS}=       Get Device Status       device_mac=${ap1.serial}
    Should contain any  ${DEVICE_STATUS}    green     config audit mismatch

    [Teardown]    Close Spawn    ${AP_SPAWN}

TCCS-7651_Step3: AP upgrade to lastest version
    [Documentation]     AP upgrade to lastest version
    [Tags]              production      tccs_7651       tccs_7651_step_3

    Depends On          TCCS-7651_Step2

    ${LATEST_VERSION}=      Upgrade Device To Latest Version            ${ap1.serial}
    Should Not be Empty     ${LATEST_VERSION}

    Sleep                   ${ap_reboot_wait}

    ${REBOOT_STATUS}=    Wait Until Device Reboots               ${ap1.serial}
    Should Be Equal as Integers             ${REBOOT_STATUS}          1

    ${CONNECTED_STATUS}=    Wait Until Device Online                ${ap1.serial}       retry_count=15
    Should Be Equal as Integers             ${CONNECTED_STATUS}          1
