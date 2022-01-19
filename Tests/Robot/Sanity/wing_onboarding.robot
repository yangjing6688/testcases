# Author        : Rameswar
# Date          : January 15th 2020
# Description   : Basic Login Test Cases
#
# Topology      :
# Host ----- Cloud

*** Variables ***

*** Settings ***
Library     common/Utils.py
Library     common/Cli.py
Library     common/Rest.py
Library     common/Screen.py
Library     common/TestFlow.py

Library     xiq/flows/common/Login.py
Library     xiq/flows/common/Navigator.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/Device360.py
Library     xiq/flows/globalsettings/GlobalSetting.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml

*** Keywords ***

*** Test Cases ***
test1: Onboard WiNG AP
    [Documentation]         Checks for ap onboarding is success in case of valid scenario
    [Tags]                  sanity              onboard         P1      production      test1
    ${result}=              Login User          ${tenant_username}      ${tenant_password}
    ${DELETE_RESULT}=       Delete AP           ap_serial=${wing1.serial}
    Log                     ${DELETE_RESULT}

    ${ONBOARD_RESULT}=      Onboard WiNG AP         ${wing1.serial}         ${wing1.mac}   ${wing1.make}
    Should Be Equal As Integers                     ${ONBOARD_RESULT}           1
    ${search_result}=       Search AP Serial    ${wing1.serial}
    should be equal as integers             ${result}               1
    should be equal as integers             ${search_result}        1

    [Teardown]
    Logout User
    Quit Browser

test2: Config AP to Report XIQ
    [Documentation]     Configure Capwap client server
    [Tags]              sanity              ap-config       P1          production      test2
    Depends On          test1
    ${AP_SPAWN}=        Open Spawn          ${wing1.console_ip}   ${wing1.console_port}      ${wing1.username}       ${wing1.password}        ${wing1.platform}

    Set Suite Variable  ${AP_SPAWN}
    ${OUTPUT0}=         Send Commands       ${AP_SPAWN}         en, end, en, configure, no nsight-policy xiq, commit write memory, commit write memory
    ${OUTPUT0}=         Send Commands       ${AP_SPAWN}         nsight-policy xiq, server host ${wing_capwap_url} https enforce-verification poll-work-queue, commit write memory
    ${OUTPUT0}=         Send Commands       ${AP_SPAWN}         rf-domain default, use nsight-policy xiq, commit write memory

    ${OUTPUT1}=         Send                ${AP_SPAWN}         show running-config nsight-policy xiq
    ${OUTPUT2}=         Send                ${AP_SPAWN}         show running-config rf-domain default
    ${OUTPUT3}=         Send                ${AP_SPAWN}         self, show context, end

    [Teardown]
    Close Spawn         ${AP_SPAWN}

test3: Check AP Status On UI
    [Documentation]     Checks for ap status
    [Tags]              sanity              status-check        P1          production      test3
    Depends On          test1               test2
    ${result}=          Login User          ${tenant_username}     ${tenant_password}

    Wait Until Device Online                ${wing1.serial}

    ${AP_STATUS}=       Get AP Status       ap_mac=${wing1.mac}

    ${HOST_NAME}=       Get Device Details  ${wing1.mac}          HOST NAME
    Log To Console      ${HOST_NAME}

    ${SERIAL}=          Get Device Details  ${wing1.mac}          SERIAL
    Log To Console      ${SERIAL}

    ${OS_VERSION}=      Get Device Details  ${wing1.mac}          OS VERSION
    Log To Console      ${OS_VERSION}

    ${MODEL}=           Get Device Details  ${wing1.mac}          MODEL
    Log To Console      ${MODEL}

    ${MGT_IP_ADDRESS}=  Get Device Details  ${wing1.mac}          MGT IP ADDRESS
    Log To Console      ${MGT_IP_ADDRESS}

    Should Be Equal As Strings  '${AP_STATUS}'     'green'

    Should Contain              ${OS_VERSION}       ${wing1.os_version}
    Should Be Equal As Strings  ${HOST_NAME}        ${wing1.name}
    Should Be Equal As Strings  ${SERIAL}           ${wing1.serial}
    Should Be Equal As Strings  ${MODEL}            ${wing1.model}        ignore_case=True

    [Teardown]
    Logout User
    Quit Browser

test4: Check for SSH CLI Reachability
    [Documentation]     Check for SSH CLI Reachability
    [Tags]              sanity              cli-ssh        P1              production      test4
    Depends On          test1               test2               test3
    ${result}=          Login User          ${tenant_username}     ${tenant_password}
    Enable SSH Availability
    Navigate To Devices
    ${IP_ADDR}   ${PORT_NUM}              Device360 Enable SSH CLI Connectivity   device_name=${wing1.name}         run_time=5

    ${SPAWN1}=          Open PXSSH Spawn    ${IP_ADDR}      ${wing1.username}    ${wing1.password}      ${PORT_NUM}
    ${OUTPUT1}=         Send Commands       ${SPAWN1}       en, show version
    Should Contain      ${OUTPUT1}          Extreme Networks, Inc.
    should not be equal as strings          ${SPAWN1}       -1
    close spawn         ${SPAWN1}

    Sleep               5min
    ${SPAWN2}=          Open PXSSH Spawn    ${IP_ADDR}      ${wing1.username}    ${wing1.password}      ${PORT_NUM}
    Should be Equal As Integers             ${SPAWN2}       -1

    [Teardown]
    Quit Browser

test5: Check for SSH WEB Reachability
    [Documentation]     Check for SSH WEB Reachability
    [Tags]              sanity              web-ssh        P1              production      test5
    Depends On          test1               test2               test3           test4
    ${result}=          Login User          ${tenant_username}     ${tenant_password}

    ${URL}=             Device360 Enable SSH WEB Connectivity   device_name=${wing1.name}         run_time=5
    Log                 ${URL}
    ${RESULT1}=           CURL COMMAND       ${URL}
    Should be Equal As Integers         ${RESULT1}      200
    Log To Console       ${RESULT1}

    ${RESULT2}=         Device360 Disable SSH WEB Connectivity   device_name=${wing1.name}
    Should be Equal As Integers         ${RESULT2}      1
    Sleep                   30

    ${RESULT2}=           CURL COMMAND       ${URL}
    Should be Equal As Integers         ${RESULT2}      0

    [Teardown]
    Quit Browser

test6: Cleanup
    [Documentation]     Check for SSH WEB Reachability
    [Tags]              sanity              web-ssh        P1              production      test5
    Depends On          test1               test2               test3           test4
    Login User          ${tenant_username}  ${tenant_password}

    ${DELETE_STATUS}=   Delete Device       device_serial=${wing1.serial}
    Should be Equal As Integers             ${DELETE_STATUS}      1

    [Teardown]
    Quit Browser
