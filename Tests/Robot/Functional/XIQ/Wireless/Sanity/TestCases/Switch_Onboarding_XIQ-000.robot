# Author        : Ramkumar
# Date          : March 06th 2020
# Description   : Aerohive Switch Onboard Testcases
#
# Topology      :
# Host ----- Cloud

*** Variables ***
${LOCATION}                 auto_location_01, Santa Clara, building_02, floor_04
${DEVICE_MAKE_AEROHIVE}     Extreme - Aerohive

*** Settings ***
Library     common/Utils.py
Library     extauto/common/Cli.py
Library     xiq/flows/common/Login.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/Switch.py
Library     xiq/flows/manage/AdvOnboard.py
Library     xiq/flows/manage/AdvanceOnboarding.py
Library     extauto/common/TestFlow.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml

Force Tags   testbed_1_node

*** Keywords ***
Configure XIQ on Fastpath Switch
    [Arguments]         ${SPAWN}            ${capwap_url}
    ${OUTPUT0}=         Send                ${SPAWN}         Hivemanager address ${capwap_url}
    ${OUTPUT0}=         Send                ${SPAWN}         Application stop hiveagent
    ${OUTPUT0}=         Send                ${SPAWN}         Application start hiveagent

Configure XIQ on Aerohive Switch
    [Arguments]         ${SPAWN}            ${capwap_url}
    ${OUTPUT0}=         Send                ${SPAWN}         capwap client default-server-name ${capwap_url}
    ${OUTPUT0}=         Send                ${SPAWN}         save config

*** Test Cases ***
TCCS-7748_Step1: Onboard Aerohive Switch
    [Documentation]         Checks for Aerohive switch onboarding is success in case of valid scenario

    [Tags]                  production      tccs_7748   tccs_7748_step1

    ${LOGIN_STATUS}=              Login User          ${tenant_username}      ${tenant_password}     check_warning_msg=True
    should be equal as integers             ${LOGIN_STATUS}               1

    ${DELETE_DEVICE_STATUS}=            Delete Device                  device_serial=${aerohive_sw1.serial}
    should be equal as integers     ${DELETE_DEVICE_STATUS}               1

    ${ONBOARD_RESULT}=      Onboard Device      ${aerohive_sw1.serial}           ${aerohive_sw1.make}       location=${LOCATION}
    should be equal as integers                 ${ONBOARD_RESULT}       1

    [Teardown]         run keywords    logout user
     ...                               quit browser

TCCS-7748_Step2: Config Aerohive/Fastpath Switch to Report AIO
    [Documentation]     Config Aerohive Switch to Report AIO

    [Tags]              production         tccs_7748    tccs_7748_step2

    Depends On          TCCS-7748_Step1

    ${SW_SPAWN}=        Open Spawn          ${aerohive_sw1.ip}   ${aerohive_sw1.port}      ${aerohive_sw1.username}       ${aerohive_sw1.password}        ${aerohive_sw1.cli_type}
    Should not be equal as Strings          '${SW_SPAWN}'        '-1'
    
    Run Keyword If     '${aerohive_sw1.platform}'=='aerohive-fastpath'   Configure XIQ on Fastpath Switch        ${SW_SPAWN}         ${sw_capwap_url}
    Run Keyword If     '${aerohive_sw1.platform}'=='aerohive-switch'     Configure XIQ on Aerohive Switch        ${SW_SPAWN}         ${capwap_url}

    [Teardown]          Close Spawn         ${SW_SPAWN}

TCCS-7748_Step3: Check Aerohive Switch Status On UI
    [Documentation]     Checks for switch status

    [Tags]              production          tccs_7748   tccs_7748_step3

    Depends On          TCCS-7748_Step2

    ${LOGIN_STATUS}=              Login User          ${tenant_username}      ${tenant_password}
    should be equal as integers             ${LOGIN_STATUS}               1

    ${CONNECTED_STATUS}=    Wait Until Device Online                ${aerohive_sw1.serial}
    Should Be Equal as Integers             ${CONNECTED_STATUS}          1

    ${DEVICE_STATUS}=       Get Device Status       device_mac=${aerohive_sw1.mac}
    Should contain any  ${DEVICE_STATUS}    green     config audit mismatch

    [Teardown]   run keywords       logout user
    ...                             quit browser

TCCS-7748_Step4: Onboard Aerohive Switch via advanced Onboarding
    [Documentation]         Checks for Aerohive switch(SR23XX) onboarding via advanced onboard

    [Tags]                  production      tccs_7748   tccs_7748_step4

    ${LOGIN_STATUS}=              Login User          ${tenant_username}      ${tenant_password}
    should be equal as integers             ${LOGIN_STATUS}               1

    ${DELETE_DEVICE_STATUS}=            Delete Device                  device_serial=${aerohive_sw1.serial}
    should be equal as integers     ${DELETE_DEVICE_STATUS}               1

    ${ONBOARD_RESULT}=      Advance Onboard Device          ${aerohive_sw1.serial}          device_make=${aerohive_sw1.make}   dev_location=${LOCATION}
    should be equal as integers             ${ONBOARD_RESULT}       1

    Sleep                   ${device_onboarding_wait}
    
    ${SW_SPAWN}=        Open Spawn          ${aerohive_sw1.ip}   ${aerohive_sw1.port}      ${aerohive_sw1.username}       ${aerohive_sw1.password}        ${aerohive_sw1.cli_type}
    Should not be equal as Strings          '${SW_SPAWN}'        '-1'

    Run Keyword If     '${aerohive_sw1.platform}'=='aerohive-fastpath'   Configure XIQ on Fastpath Switch        ${SW_SPAWN}         ${sw_capwap_url}
    Run Keyword If     '${aerohive_sw1.platform}'=='aerohive-switch'     Configure XIQ on Aerohive Switch        ${SW_SPAWN}         ${capwap_url}

    ${CONNECTED_STATUS}=    Wait Until Device Online                ${aerohive_sw1.serial}
    Should Be Equal as Integers             ${CONNECTED_STATUS}          1

    ${DEVICE_STATUS}=       Get Device Status       device_mac=${aerohive_sw1.mac}
    Should contain any  ${DEVICE_STATUS}    green     config audit mismatch

    ${DELETE_DEVICE_STATUS}=            Delete Device                  device_serial=${aerohive_sw1.serial}
    should be equal as integers     ${DELETE_DEVICE_STATUS}               1

    [Teardown]   run keywords       logout user
    ...          AND                quit browser
    ...          AND                Close Spawn        ${SW_SPAWN}