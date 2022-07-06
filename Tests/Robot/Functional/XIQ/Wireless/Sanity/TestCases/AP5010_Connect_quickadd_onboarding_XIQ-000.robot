# Author        : Pranav Chauhan
# Date          : April 2022
# Description   : AP5010 onboarding support at CONNECT level account

# Pre-Condtion


*** Settings ***

Library     extauto/common/Cli.py
Library     extauto/common/TestFlow.py
Library     extauto/xiq/flows/common/Login.py
Library     extauto/xiq/flows/common/Navigator.py
Library     extauto/xiq/flows/manage/Client.py
Library     extauto/xiq/flows/manage/Devices.py
Library     extauto/xiq/flows/manage/DeviceCliAccess.py
Library     extauto/xiq/flows/globalsettings/GlobalSetting.py
Library     extauto/xiq/flows/configure/NetworkPolicy.py
Library     extauto/xiq/flows/configure/CommonObjects.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/device_commands.yaml

Force Tags   testbed_none

*** Variables ***

${DEVICE_TYPE}          Real
${ENTRY_TYPE}           Manual
${LOCATION}                 auto_location_01, Santa Clara, building_02, floor_04

*** Test Cases ***

TCXM-19753 - XIQ-4593 - QuickAdd: Onboard AP5010/AP5010U cloud managed - step1
    [Documentation]         Checks for ap onboarding is success in case of valid scenario
    [Tags]                  xim_tc_19753    development     ap5010      step1      tcxm-19753      quickadd
    ${result}=              Login User          ${tenant_username}      ${tenant_password}
    Delete AP               ap_serial=${ap5010.serial}
    Change Device Password                      Aerohive123
    ${ONBOARD_RESULT}=      Onboard Device      ${ap5010.serial}           ${ap5010.make}       location=${LOCATION}
    ${search_result}=       Search AP Serial    ${ap5010.serial}
    should be equal as integers             ${result}               1
    should be equal as integers             ${ONBOARD_RESULT}       1
    should be equal as integers             ${search_result}        1

    [Teardown]   run keywords               logout user
    ...                                     quit browser


TCXM-19753 - XIQ-4593 - QuickAdd: Onboard AP5010/AP5010U cloud managed - step2
    [Documentation]     Configure Capwap client server on AP
    [Tags]              xim_tc_19753    development     ap5010      step2     tcxm-19753      quickadd
    Depends On          step1
    ${AP_SPAWN}=        Open Spawn          ${ap5010.ip}   ${ap5010.port}      ${ap5010.username}       ${ap5010.password}        ${ap5010.cli_type}

    ${OUTPUT0}=         Send Commands       ${AP_SPAWN}         capwap client server name ${capwap_url}, capwap client default-server-name ${capwap_url}, capwap client server backup name ${capwap_url}, no capwap client enable, capwap client enable, save config

    ${OUTPUT0}=         Send                ${AP_SPAWN}         console page 0
    ${OUTPUT0}=         Send                ${AP_SPAWN}         show version detail
    ${OUTPUT0}=         Send                ${AP_SPAWN}         show capwap client
    ${OUTPUT2}=         Send                ${AP_SPAWN}         ${cmd_capwap_hm_primary_name}
    ${OUTPUT3}=         Send                ${AP_SPAWN}         ${cmd_capwap_server_ip}
    ${OUTPUT1}=         Wait For CLI Output                     ${AP_SPAWN}         ${cmd_capwap_client_state}          ${output_capwap_status}

    Should Be Equal as Integers             ${OUTPUT1}          1

    [Teardown]    Close Spawn    ${AP_SPAWN}


TCXM-19753 - XIQ-4593 - QuickAdd: Onboard AP5010/AP5010U cloud managed - step3
    [Documentation]     Check AP Status On UI
    [Tags]              xim_tc_19753    development     ap5010      step3      tcxm-19753      quickadd
    Depends On          step2
    ${result}=          Login User          ${tenant_username}     ${tenant_password}
    Wait Until Device Online                ${ap5010.serial}
    ${AP_STATUS}=       Get AP Status       ap_mac=${ap5010.mac}
    Should Be Equal As Strings  '${AP_STATUS}'     'green'

    [Teardown]   run keywords               logout user
    ...                                     quit browser
