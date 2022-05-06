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

*** Keywords ***
Cleanup-Delete Switch
    [Arguments]     ${SERIAL}
    Login User      ${tenant_username}      ${tenant_password}
    Delete Device        device_serial=${netelem1.serial}
    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

*** Test Cases ***
TCCS-7292_Step1: Onboard EXOS Switch on XIQ
    [Documentation]         Checks for Exos switch onboarding on XIQ

    [Tags]                  production      tccs_7292_step1

    ${LOGIN_XIQ}=              Login User          ${tenant_username}      ${tenant_password}
    ${ONBOARD_RESULT}=      Onboard Switch      ${netelem1.serial}       ${netelem1.make}    location=${LOCATION}
    Should Be Equal As Strings                  ${ONBOARD_RESULT}       1

    ${SEARCH_SWITCH}=       Search Device Serial    ${netelem1.serial}
    Should Be Equal As Strings             ${SEARCH_SWITCH}       1
    ${SWITCH_CONNECTION_HOST}=      Capture XIQ Switch Connection Host
    Should Not Be Equal As Strings             ${SWITCH_CONNECTION_HOST}       ${EMPTY}

    ${SW_SPAWN}=            Open Spawn          ${netelem1.console_ip}   ${netelem1.console_port}      ${netelem1.username}       ${netelem1.password}        ${netelem1.platform}
    ${CONF_SWITCH_HOST}=    Send                ${SW_SPAWN}         configure iqagent server ipaddress ${SWITCH_CONNECTION_HOST}
    ${CONF_VR}=             Send                ${SW_SPAWN}         configure iqagent server vr VR-Default
    ${CONF_VR}=             Send                ${SW_SPAWN}         save config
    ${SHOW_PROCESS}=        Send                ${SW_SPAWN}         show process iqagent
    Should Contain                              ${SHOW_PROCESS}     Ready

    Close Spawn             ${SW_SPAWN}

    Wait Until Device Online    ${netelem1.serial}
    ${SWITCH_STATUS}=       Get Device Status       device_serial=${netelem1.serial}

    [Teardown]         run keywords    logout user
     ...                               quit browser

TCCS-7292_Step2: Verify EXOS Switch Information on Device 360 page
    [Documentation]         Verify EXOS Switch Information on Device 360 page

    [Tags]                  production      tccs_7292_step2

    Depends On              tccs_7292_step1
    ${LOGIN_XIQ} =                 Login User               ${tenant_username}      ${tenant_password}
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

    [Teardown]         run keywords    logout user
     ...                               quit browser

TCCS-7292_Step3: Verify ExOS SSH connectivity
  [Documentation]       Verify ExOS SSH connectivity

    [Tags]              production      tccs_7292_step3

    Depends On          tccs_7292_step2
    ${LOGIN_XIQ}=         Login User          ${tenant_username}      ${tenant_password}
    ${ENABLE_SSH}=         Enable SSH Availability

    &{ip_port_info}=       Device360 Enable SSH CLI Connectivity     device_mac=${netelem1.mac}    run_time=${SSH_TIMEOUT}
    ${IP ADDR}=            Get From Dictionary  ${ip_port_info}  ip
    ${PORT NUM}=           Get From Dictionary  ${ip_port_info}  port

    ${SPAWN1}=          Open Paramiko SSH Spawn    ${IP ADDR}   ${netelem1.username}    ${netelem1.password}  ${PORT NUM}
    ${OUTPUT1}=         Send Paramiko CMD           ${SPAWN1}           show version
    Should Contain      ${OUTPUT1}          ExtremeXOS version
    Should Contain      ${OUTPUT1}          ${netelem1.serial}
    should not be equal as strings          ${SPAWN1}       -1

    ${SSH STATUS}=     UI SSH Status Check
    should be equal as strings              ${SSH STATUS}   ${SSH_ACTIVE}

    Sleep    5 minutes

    ${SPAWN2}=          Open Paramiko SSH Spawn    ${IP ADDR}   ${netelem1.username}    ${netelem1.password}  ${PORT NUM}
    should be equal as strings          ${SPAWN2}     -1

    [Teardown]         run keywords    logout user
     ...                               quit browser

Test Suite Clean Up
    [Documentation]    delete Exos Switch

    [Tags]              production   cleanup
     ${result}=    Login User        ${tenant_username}     ${tenant_password}
     ${DELETE_RESULT}=      Delete Device       device_serial=${netelem1.serial}
     Should Be Equal As Integers                ${DELETE_RESULT}     1
     [Teardown]   run keywords       Logout User
    ...                             Quit Browser