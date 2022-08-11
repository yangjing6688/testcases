# Author        : Barbara Sochor
# Date          : August 10th 2022
# Description   : XIQ-6165 AP5010 Regulatory Support
#
# Topology:
# Host ----- XIQ
#
#  To run using topo and environment:
#  ----------------------------------
#  robot -v TOPO:topology.yaml -v ENV:environment.yaml -v TESTBED:SJ/Dev/xiq_sj_tb0.yaml -i xim_tc_20804 AP5010xxx.robot
#
#
#  ---------------------
#  This file contains test cases.
#
#  Test Cases:
#  Test1 - TCXM-20804 - Verify: AP Can Be Configured To Albania
#             Verifies that AP can be configured to Country Albania.
#  Test2 - TCXM-20816 - Verify: AP Can Be Configured To Austria
#             Verifies that AP can be configured to Country Austria.
########################################################################################################################

*** Variables ***

*** Settings ***
# import libraries
Library     Collections
Library     xiq/flows/common/Login.py
Library     common/Utils.py
Library     common/Screen.py
Library     common/ImageHandler.py
Library     common/ScreenDiff.py
Library     xiq/flows/manage/Devices.py
Library     common/ImageAnalysis.py
Library     xiq/flows/globalsettings/GlobalSetting.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/configure/ExpressNetworkPolicies.py
Library     xiq/flows/configure/CommonObjects.py
Library     extauto/common/Cli.py
Library     extauto/common/TestFlow.py
Library     extauto/xiq/flows/common/Login.py
Library     extauto/xiq/flows/common/Navigator.py

Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    TestBeds/${TESTBED}
Variables    Environments/Config/device_commands.yaml
Variables    Environments/Config/waits.yaml
Variables    Tests/Robot/Functional/XIQ/Wireless/Network360Monitor/Resources/n360waits.yaml

Force Tags   testbed_1_node
Suite Setup    InitialSetup

*** Test Cases ***
Test1 - TCXM-20804 - Verify: AP Can Be Configured To Albania
    [Documentation]         AP's country code is changed to Albania and result it verified on UI level
    [Tags]                  tcxm-20804    development
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Albania
    ${COUNTRY_CODE}     Set Variable    8
    Log                         ${COUNTRY}
    Log to Console              ${COUNTRY}
    ${result}=                  Login User          ${tenant_username}    ${tenant_password}
    ${COUNTRY_STATUS}=          Change Country      ${ap1.serial}         ${COUNTRY}
    Wait Until Device Reboots   ${ap1.serial}
    refresh devices page
    ${AP_STATUS2}=              Get AP Status       ${ap1.serial}
    refresh devices page
    ${AP_COUNTRY}=              Get AP Country      ${ap1.serial}
    refresh devices page
    ${GET_FLAG_STATUS}=         Get AP Flag         ${ap1.serial}
    Save Screen Shot
    ${AP_SPAWN}=                Open Spawn          ${ap1.ip}     ${ap1.port}     ${ap1.username}     ${ap1.password}     ${ap1.platform}
    ${OUTPUT0}=                 Send                ${AP_SPAWN}   ${CMD_BOOT_PARAM}
    Close Spawn                 ${AP_SPAWN}

    Log to Console                      RESTULTS====
    Log to Console                      BOOT_PARAM: ${OUTPUT0}
    Should Contain Any                  ${OUTPUT0}    World   ${COUNTRY_CODE}
    Log to Console                      AP_COUNTRY: ${AP_COUNTRY}
    Should Contain                      ${AP_COUNTRY}           ${COUNTRY}
    Log to Console                      GET_FLAG_STATUS: ${GET_FLAG_STATUS}
    Should Not Be Equal as Integers     ${GET_FLAG_STATUS}      -1
    Log to Console                      COUNTRY_STATUS: ${COUNTRY_STATUS}
    Should Be Equal as Integers         ${COUNTRY_STATUS}       1
    Log to Console                      AP_STATUS2: ${AP_STATUS2}
    Should Be Equal as Strings          '${AP_STATUS2}'         'green'
    Log to Console                      END_RESTULTS====

Test2 - TCXM-20816 - Verify: AP Can Be Configured To Austria
    [Documentation]         AP's country code is changed to Austria and result it verified on UI level
    [Tags]                  tcxm-20816    development
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Austria
    ${COUNTRY_CODE}     Set Variable    40
    Log                         ${COUNTRY}
    Log to Console              ${COUNTRY}
    ${result}=                  Login User          ${tenant_username}    ${tenant_password}
    ${COUNTRY_STATUS}=          Change Country      ${ap1.serial}         ${COUNTRY}
    Wait Until Device Reboots   ${ap1.serial}
    refresh devices page
    ${AP_STATUS2}=              Get AP Status       ${ap1.serial}
    refresh devices page
    ${AP_COUNTRY}=              Get AP Country      ${ap1.serial}
    refresh devices page
    ${GET_FLAG_STATUS}=         Get AP Flag         ${ap1.serial}
    Save Screen Shot
    ${AP_SPAWN}=                Open Spawn          ${ap1.ip}     ${ap1.port}     ${ap1.username}     ${ap1.password}     ${ap1.platform}
    ${OUTPUT0}=                 Send                ${AP_SPAWN}   ${CMD_BOOT_PARAM}
    Close Spawn                 ${AP_SPAWN}

    Log to Console                      RESTULTS====
    Log to Console                      BOOT_PARAM: ${OUTPUT0}
    Should Contain                      ${OUTPUT0}              ${COUNTRY_CODE}
    Log to Console                      AP_COUNTRY: ${AP_COUNTRY}
    Should Contain                      ${AP_COUNTRY}           ${COUNTRY}
    Log to Console                      GET_FLAG_STATUS: ${GET_FLAG_STATUS}
    Should Not Be Equal as Integers     ${GET_FLAG_STATUS}      -1
    Log to Console                      COUNTRY_STATUS: ${COUNTRY_STATUS}
    Should Be Equal as Integers         ${COUNTRY_STATUS}       1
    Log to Console                      AP_STATUS2: ${AP_STATUS2}
    Should Be Equal as Strings          '${AP_STATUS2}'         'green'
    Log to Console                      END_RESTULTS====

*** Keywords ***
InitialSetup
    Login User      ${tenant_username}      ${tenant_password}
    delete all aps
    delete all network policies
    delete_all_ssids

    ${onboard_result}=      Onboard Device      ${ap1.serial}         ${ap1.make}       location=${ap1.location}      device_os=${ap1.os}
    ${search_result}=       Search AP Serial    ${ap1.serial}
    should be equal as integers                 ${onboard_result}     1
    should be equal as integers                 ${search_result}      1

    ${AP_SPAWN}=            Open Spawn          ${ap1.ip}     ${ap1.port}     ${ap1.username}     ${ap1.password}     ${ap1.platform}
    ${OUTPUT0}=             Send Commands       ${AP_SPAWN}           mfg-set-region-code #G6L@*Sv^&<W>Cp/ 1 40, capwap client server name ${CAPWAP_URL}, capwap client default-server-name ${CAPWAP_URL}, capwap client server backup name ${CAPWAP_URL}, no capwap client enable, capwap client enable, save config
    ${OUTPUT0}=             Send                ${AP_SPAWN}           ${CMD_CONSOLE_PAGE_0}
    ${OUTPUT0}=             Send                ${AP_SPAWN}           ${CMD_SHOW_VERSION_DETAIL}
    ${OUTPUT0}=             Send                ${AP_SPAWN}           ${CMD_SHOW_CAPWAP_CLIENT}
    ${OUTPUT1}=             Send                ${AP_SPAWN}           ${CMD_CAPWAP_HM_PRIMARY_NAME}
    ${OUTPUT2}=             Send                ${AP_SPAWN}           ${CMD_CAPWAP_SERVER_IP}
    ${OUTPUT3}=             Wait For CLI Output                       ${AP_SPAWN}         ${CMD_CAPWAP_CLIENT_STATE}          ${OUTPUT_CAPWAP_STATUS}
    Close Spawn             ${AP_SPAWN}
    Should Be Equal as Integers                 ${OUTPUT3}            1
    sleep    60
    Wait Until Device Reboots                   ${ap1.serial}
    Log to Console                              WaitUntilCountryDiscovered
    Wait Until Country Discovered               ${ap1.serial}   60    100
    Log to Console                              WaitUntilDeviceReboots
    Wait Until Device Reboots                   ${ap1.serial}
    Sleep   60
    Logout User
    Sleep   10
    Quit Browser
