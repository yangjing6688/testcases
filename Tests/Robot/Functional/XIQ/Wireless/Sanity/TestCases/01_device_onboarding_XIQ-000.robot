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
Library     extauto/xiq/flows/common/Navigator.py
Library     extauto/xiq/flows/manage/Client.py
Library     extauto/xiq/flows/manage/Devices.py
Library     extauto/xiq/flows/globalsettings/GlobalSetting.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/device_commands.yaml

Force Tags   testbed_1_node

*** Keywords ***

*** Test Cases ***
TCCS-7651_Step1: Onboard Aerohive AP
    [Documentation]         Checks for ap onboarding is success in case of valid scenario
    [Tags]                  production      tccs_7651       tccs_7651_step_1
    ${LOGIN_STATUS}=                Login User          ${tenant_username}      ${tenant_password}     check_warning_msg=True
    should be equal as integers     ${LOGIN_STATUS}               1

    # Clean up the device if something happened
    ${DELETE_DEVICE_STATUS}=            Delete Device       device_serial=${ap1.serial}
    should be equal as integers     ${DELETE_DEVICE_STATUS}               1

    ${CHANGE_PASSWORD_STATUS}=      Change Device Password                  Aerohive123
    should be equal as integers     ${CHANGE_PASSWORD_STATUS}               1

    ${ONBOARD_RESULT}=              Onboard Device      ${ap1.serial}           ${ap1.make}       location=${LOCATION}
    should be equal as integers     ${ONBOARD_RESULT}       1

    ${search_result}=               Search AP Serial    ${ap1.serial}
    should be equal as integers     ${search_result}        1

    [Teardown]  Run Keywords   Logout User   Quit Browser


TCCS-7651_Step2: Config AP to Report AIO
    [Documentation]     Configure Capwap client server
    [Tags]              production      tccs_7651       tccs_7651_step_2
    Depends On          TCCS-7651_Step1
    ${AP_SPAWN}=        Open Spawn          ${ap1.ip}   ${ap1.port}      ${ap1.username}       ${ap1.password}        ${ap1.cli_type}
    Should not be equal as Strings      '${AP_SPAWN}'        '-1'

    ${OUTPUT0}=         Send Commands       ${AP_SPAWN}         capwap client server name ${capwap_url}, capwap client default-server-name ${capwap_url}, capwap client server backup name ${capwap_url}, no capwap client enable, capwap client enable, save config

    ${OUTPUT0}=         Send                ${AP_SPAWN}         console page 0
    ${OUTPUT0}=         Send                ${AP_SPAWN}         show version detail
    ${OUTPUT0}=         Send                ${AP_SPAWN}         show capwap client
    ${OUTPUT2}=         Send                ${AP_SPAWN}         ${cmd_capwap_hm_primary_name}
    ${OUTPUT3}=         Send                ${AP_SPAWN}         ${cmd_capwap_server_ip}
    ${OUTPUT1}=         Wait For CLI Output                     ${AP_SPAWN}         ${cmd_capwap_client_state}          ${output_capwap_status}

    Should Be Equal as Integers             ${OUTPUT1}          1

    [Teardown]    Close Spawn    ${AP_SPAWN}


TCCS-7651_Step3: Check AP Status On UI
    [Documentation]     Checks for ap status
    [Tags]              production      tccs_7651       tccs_7651_step_3 
    Depends On          TCCS-7651_Step2

    ${LOGIN_STATUS}=          Login User          ${tenant_username}     ${tenant_password}
    should be equal as integers             ${LOGIN_STATUS}               1

    ${CONNECTED_STATUS}=    Wait Until Device Online                ${ap1.serial}
    Should Be Equal as Integers             ${CONNECTED_STATUS}          1

    ${DEVICE_STATUS}=       Get Device Status       device_mac=${ap1.mac}
    Should contain any  ${DEVICE_STATUS}    green     config audit mismatch

    [Teardown]    Run Keywords    Logout User   Quit Browser

TCCS-7651_Step4: Quick Onboard Simulated Device
    [Documentation]         Quick Onboarding - Add Simulated Devices
    [Tags]                  production      tccs_7651       tccs_7651_step_4
    ${LOGIN_STATUS}=                Login User          ${tenant_username}          ${tenant_password}
    should be equal as integers     ${LOGIN_STATUS}               1

    ${SIM_SERIAL}=                  Onboard Simulated Device                AP460C             location=${LOCATION}
    Should not be Empty             ${SIM_SERIAL}

    ${DELETE_AP}=                   Delete Devices              ${SIM_SERIAL}
    should be equal as integers     ${DELETE_AP}               1

    [Teardown]  Run Keywords    Logout User   Quit Browser

