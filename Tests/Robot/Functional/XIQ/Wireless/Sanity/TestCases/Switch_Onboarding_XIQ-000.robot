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
Library     common/Cli.py
Library     xiq/flows/common/Login.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/Switch.py
Library     xiq/flows/manage/AdvOnboard.py
Library     xiq/flows/manage/AdvanceOnboarding.py

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

Get XIQ Status on Fastpath Switch
    [Arguments]         ${SPAWN}            ${capwap_url}
    ${SW_VERSION}=      Send                ${SPAWN}         show version
    ${HM_FULL_STATUS}=  Send                ${SPAWN}         show hivemanager status
    ${HM_STATUS}=       Send                ${SPAWN}         show hivemanager status | include Status
    ${HM_ADDRESS}=      Send                ${SPAWN}         show hivemanager address
    Should Contain      ${HM_ADDRESS}       ${capwap_url}
    Should Contain      ${HM_STATUS}        CONNECTED TO HIVEMANAGER

Configure XIQ on Aerohive Switch
    [Arguments]         ${SPAWN}            ${capwap_url}
    ${OUTPUT0}=         Send                ${SPAWN}         capwap client default-server-name ${capwap_url}
    ${OUTPUT0}=         Send                ${SPAWN}         save config

Get XIQ Status on Aerohive Switch
    [Arguments]         ${SPAWN}            ${capwap_url}
    ${SW_VERSION}=      Send                ${SPAWN}         show version
    ${HM_ADDRESS}=      Send                ${SPAWN}         show hivemanager
    Should Contain      ${HM_ADDRESS}       ${capwap_url}

*** Test Cases ***
TCCS-7748_Step1: Onboard Aerohive Switch
    [Documentation]         Checks for Aerohive switch onboarding is success in case of valid scenario

    [Tags]                  production      tccs_7748_step1
    ${result}=              Login User          ${tenant_username}      ${tenant_password}
    Delete Device           device_serial=${aerohive_sw1.serial}
    ${ONBOARD_RESULT}=      Onboard Device      ${aerohive_sw1.serial}           ${aerohive_sw1.make}       location=${LOCATION}
    should be equal as integers                 ${ONBOARD_RESULT}       1
    [Teardown]         run keywords    logout user
     ...                               quit browser

TCCS-7748_Step2: Config Aerohive/Fastpath Switch to Report AIO
    [Documentation]     Config Aerohive Switch to Report AIO

    [Tags]              production         tccs_7748_step2
    ${SW_SPAWN}=        Open Spawn          ${aerohive_sw1.ip}   ${aerohive_sw1.port}      ${aerohive_sw1.username}       ${aerohive_sw1.password}        ${aerohive_sw1.cli_type}
    Run Keyword If     '${aerohive_sw1.platform}'=='aerohive-fastpath'   Configure XIQ on Fastpath Switch        ${SW_SPAWN}         ${sw_capwap_url}
    Run Keyword If     '${aerohive_sw1.platform}'=='aerohive-switch'     Configure XIQ on Aerohive Switch        ${SW_SPAWN}         ${capwap_url}

    [Teardown]          Close Spawn         ${SW_SPAWN}

TCCS-7748_Step3: Check Aerohive Switch Status On UI
    [Documentation]     Checks for switch status

    [Tags]              production          tccs_7748_step3
    ${result}=          Login User          ${tenant_username}     ${tenant_password}
    wait until device online                device_serial=${aerohive_sw1.serial}
    ${SW_STATUS}=       Get Device Status           device_serial=${aerohive_sw1.serial}

    Delete Device		${aerohive_sw1.serial}

    [Teardown]   run keywords       logout user
    ...                             quit browser


TCCS-7748_Step4: Onboard Aerohive Switch via advanced Onboarding
    [Documentation]         Checks for Aerohive switch(SR23XX) onboarding via advanced onboard

    [Tags]                  production  tccs_7748_step4
    ${result}=              Login User          ${tenant_username}      ${tenant_password}
    ${onboard_result}=      Advance Onboard Device          ${aerohive_sw1.serial}          device_make=${aerohive_sw1.make}   dev_location=${LOCATION}
    Sleep                   ${device_onboarding_wait}
    ${search_result}=       Search Device Serial    ${aerohive_sw1.serial}
    ${SW_SPAWN}=        Open Spawn          ${aerohive_sw1.ip}   ${aerohive_sw1.port}      ${aerohive_sw1.username}       ${aerohive_sw1.password}        ${aerohive_sw1.cli_type}
    Run Keyword If     '${aerohive_sw1.platform}'=='aerohive-fastpath'   Configure XIQ on Fastpath Switch        ${SW_SPAWN}         ${sw_capwap_url}
    Run Keyword If     '${aerohive_sw1.platform}'=='aerohive-switch'     Configure XIQ on Aerohive Switch        ${SW_SPAWN}         ${capwap_url}
    wait until device online                        device_serial=${aerohive_sw1.serial}
    ${SW_STATUS}=           Get Device Status       device_serial=${aerohive_sw1.serial}
    should be equal as integers             ${result}               1
    should be equal as integers             ${onboard_result}       1
    should be equal as integers             ${search_result}        1
    Should Be Equal As Strings              '${SW_STATUS}'     'green'
    Delete Device           				device_serial=${aerohive_sw1.serial}

    [Teardown]   run keywords       logout user
    ...                             quit browser