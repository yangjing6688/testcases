# Author        : Ramkumar
# Date          : Aug 19th 2020
# Description   : Exos Switch Onboard Testcases
#
# Topology      :
# Exos Switch ----- Cloud

*** Variables ***
${SSH_TIMEOUT}              5
${SSH_ACTIVE}               SSH Active
${LOCATION}                 auto_location_01, Santa Clara, building_02, floor_04

*** Settings ***
Library     Collections
Library     common/Utils.py
Library     common/Cli.py
Library     xiq/flows/common/Login.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/Device360.py
Library     xiq/flows/manage/Switch.py
Library     xiq/flows/manage/Tools.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/globalsettings/GlobalSetting.py
Library     common/TestFlow.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml

Force Tags   testbed_1_node

Suite Setup     Cleanup-Delete Switch   ${netelem1.serial}
Suite Teardown  Test Suite Clean Up

*** Keywords ***
Cleanup-Delete Switch
    [Arguments]     ${SERIAL}

    ${LOGIN_STATUS}=                    Login User          ${tenant_username}      ${tenant_password}     check_warning_msg=True
    should be equal as integers         ${LOGIN_STATUS}               1

    ${DELETE_DEVICE_STATUS}=            Delete Device                  device_serial=${SERIAL}
    should be equal as integers        ${DELETE_DEVICE_STATUS}               1

Test Suite Clean Up
    [Documentation]    delete Exos Switch

    [Tags]              production   cleanup

    ${DELETE_DEVICE_STATUS}=            Delete Device       device_serial=${netelem1.serial}
    Should Be Equal As Integers         ${DELETE_DEVICE_STATUS}     1

    [Teardown]   run keywords           Logout User
    ...                                 Quit Browser
    
*** Test Cases ***
TCCS-7292_Step1: Onboard EXOS Switch on XIQ
    [Documentation]         Checks for Exos switch onboarding on XIQ

    [Tags]                  production      tccs_7292       tccs_7292_step1

    ${ONBOARD_RESULT}=                  Onboard Switch      ${netelem1.serial}       ${netelem1.make}    location=${LOCATION}
    Should Be Equal As Strings          ${ONBOARD_RESULT}       1

    ${SEARCH_SWITCH}=       Search Device       device_serial=${netelem1.serial}
    Should Be Equal As Strings             ${SEARCH_SWITCH}       1

    ${SWITCH_CONNECTION_HOST}=      Capture XIQ Switch Connection Host
    Should Not Be Equal As Strings             ${SWITCH_CONNECTION_HOST}       ${EMPTY}

    ${SW_SPAWN}=            Open Spawn          ${netelem1.ip}       ${netelem1.port}      ${netelem1.username}       ${netelem1.password}        ${netelem1.cli_type}
    ${CONF_SWITCH_HOST}=    Send                ${SW_SPAWN}         configure iqagent server ipaddress ${SWITCH_CONNECTION_HOST}
    ${CONF_VR}=             Send                ${SW_SPAWN}         configure iqagent server vr VR-Default
    ${CONF_VR}=             Send                ${SW_SPAWN}         save config
    ${SHOW_PROCESS}=        Send                ${SW_SPAWN}         show process iqagent
    Should Contain                              ${SHOW_PROCESS}     Ready

    Close Spawn             ${SW_SPAWN}

    ${CONNECTED_STATUS}=                Wait Until Device Online                ${netelem1.serial}
    Should Be Equal as Integers         ${CONNECTED_STATUS}          1

    ${DEVICE_STATUS}=                   Get Device Status       device_mac=${netelem1.mac}
    Should contain any                  ${DEVICE_STATUS}    green     config audit mismatch

TCCS-7292_Step2: Verify EXOS Switch Information on Device 360 page
    [Documentation]         Verify EXOS Switch Information on Device 360 page

    [Tags]                  production      tccs_7292       tccs_7292_step2

    Depends On              TCCS-7292_Step1

    ${SYS_INFO_360_PAGE}=          Get ExOS Switch 360 Information  device_mac=${netelem1.mac}
    ${HOST_NAME}=                  Get From Dictionary      ${SYS_INFO_360_PAGE}    host_name
    Should Be Equal As Strings    '${HOST_NAME}'            '${netelem1.name}'
    ${DEVICE_MODEL}=               Get From Dictionary      ${SYS_INFO_360_PAGE}    device_model
    Should Be Equal As Strings    '${DEVICE_MODEL}'         '${netelem1.model}'
    ${DEVICE_IP}=                  Get From Dictionary      ${SYS_INFO_360_PAGE}    ip_address
    Should Be Equal As Strings    '${DEVICE_IP}'            '${netelem1.ip}'
    ${DEVICE_MAC}=                  Get From Dictionary     ${SYS_INFO_360_PAGE}    mac_address
    Should Be Equal As Strings    '${DEVICE_MAC}'           '${netelem1.mac}'
    ${DEVICE_SERIAL}=              Get From Dictionary      ${SYS_INFO_360_PAGE}    serial_number
    Should Be Equal As Strings    '${DEVICE_SERIAL}'        '${netelem1.serial}'

TCCS-7292_Step3: Verify ExOS SSH connectivity
  [Documentation]       Verify ExOS SSH connectivity

    [Tags]              production      tccs_7292       tccs_7292_step3

    Depends On          TCCS-7292_Step2

    ${ENABLE_SSH}=                      Enable SSH Availability
    should be equal as integers         ${ENABLE_SSH}               1

    &{ip_port_info}=                    Device360 Enable SSH CLI Connectivity     device_mac=${netelem1.mac}    run_time=${SSH_TIMEOUT}

    ${IP_ADDR}=            Get From Dictionary  ${ip_port_info}  ip
    ${PORT_NUM}=           Get From Dictionary  ${ip_port_info}  port

    Should not be Empty     ${IP_ADDR}
    Should not be Empty     ${PORT_NUM}

    ${SPAWN1}=          Open Paramiko SSH Spawn    ${IP_ADDR}   ${netelem1.username}    ${netelem1.password}  ${PORT_NUM}
    should not be equal as strings          ${SPAWN1}       -1

    ${OUTPUT1}=         Send Paramiko CMD           ${SPAWN1}           show version
    Should Contain      ${OUTPUT1}          ExtremeXOS version
    Should Contain      ${OUTPUT1}          ${netelem1.serial}

    ${SSH STATUS}=     UI SSH Status Check
    should be equal as strings              ${SSH STATUS}   ${SSH_ACTIVE}

    Sleep    5 minutes

    ${SPAWN2}=          Open Paramiko SSH Spawn    ${IP_ADDR}   ${netelem1.username}    ${netelem1.password}  ${PORT_NUM}
    should be equal as strings          ${SPAWN2}     -1
