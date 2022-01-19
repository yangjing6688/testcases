# Author        : Rameswar
# Date          : January 15th 2020
# Description   : Basic Login Test Cases
#
# Topology      :
# Host ----- Cloud

*** Variables ***
${LOCATION}                 auto_location_01, Santa Clara, building_02, floor_04

*** Settings ***
Library     common/Cli.py
Library     common/TestFlow.py
Library     xiq/flows/common/Login.py
Library     xiq/flows/common/Navigator.py
Library     xiq/flows/manage/Client.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/globalsettings/GlobalSetting.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/device_commands.yaml

Library	    Remote 	http://${mu1.ip}:${mu1.port}   WITH NAME   MU1

*** Keywords ***

*** Test Cases ***
Test1 - TC-49861 - Onboard Aerohive AP
    [Documentation]         Checks for ap onboarding is success in case of valid scenario
    [Tags]                  production      test1           TC-49861
    ${result}=              Login User          ${tenant_username}      ${tenant_password}
    Delete AP               ap_serial=${ap1.serial}
    Change Device Password                      Aerohive123
    ${ONBOARD_RESULT}=      Onboard Device      ${ap1.serial}           ${ap1.make}       location=${LOCATION}      device_os=${ap1.os}
    ${search_result}=       Search AP Serial    ${ap1.serial}
    should be equal as integers             ${result}               1
    should be equal as integers             ${ONBOARD_RESULT}       1
    should be equal as integers             ${search_result}        1
    [Teardown]  Run Keywords   Logout User   Quit Browser



Test2 - TC-49861 - Config AP to Report AIO
    [Documentation]     Configure Capwap client server
    [Tags]              production      test2           TC-49861
    Depends On          test1
    ${AP_SPAWN}=        Open Spawn          ${ap1.console_ip}   ${ap1.console_port}      ${ap1.username}       ${ap1.password}        ${ap1.platform}
    ${OUTPUT0}=         Send Commands       ${AP_SPAWN}         capwap client server name ${capwap_url}, capwap client default-server-name ${capwap_url}, capwap client server backup name ${capwap_url}, no capwap client enable, capwap client enable, save config

    ${OUTPUT0}=         Send                ${AP_SPAWN}         console page 0
    ${OUTPUT0}=         Send                ${AP_SPAWN}         show version detail
    ${OUTPUT0}=         Send                ${AP_SPAWN}         show capwap client
    ${OUTPUT2}=         Send                ${AP_SPAWN}         ${cmd_capwap_hm_primary_name}
    ${OUTPUT3}=         Send                ${AP_SPAWN}         ${cmd_capwap_server_ip}
    ${OUTPUT1}=         Wait For CLI Output                     ${AP_SPAWN}         ${cmd_capwap_client_state}          ${output_capwap_status}

    Should Be Equal as Integers             ${OUTPUT1}          1

    [Teardown]    Close Spawn    ${AP_SPAWN}


Test3 - TC-49861 - Check AP Status On UI
    [Documentation]     Checks for ap status
    [Tags]              production      test3           TC-49861
    Depends On          test2
    ${result}=          Login User          ${tenant_username}     ${tenant_password}
    Wait Until Device Online                ${ap1.serial}
    ${AP_STATUS}=       Get AP Status       ap_mac=${ap1.mac}
    Should Be Equal As Strings  '${AP_STATUS}'     'green'
    [Teardown]    Run Keywords    Logout User   Quit Browser

TC-52856 - Quick Onboard Simulated Device
    [Documentation]         Quick Onboarding - Add Simulated Devices
    [Tags]                  production      test1           TC-49861          simulated
    ${result}=              Login User          ${tenant_username}          ${tenant_password}
    ${SIM_SERIAL}=          Onboard Simulated Device                AP460C             location=${LOCATION}

    [Teardown]  Run Keywords   Delete APs              ${SIM_SERIAL}
    ...         AND            Quit Browser

