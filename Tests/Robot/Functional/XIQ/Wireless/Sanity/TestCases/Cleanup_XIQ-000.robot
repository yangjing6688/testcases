# Author        : Rmeswar
# Date          : July 2020
# Description   : Remove all APs, Network Policies & Common Objects

# Execution Command:
# robot -L DEBUG -i ALL -v TOPO:g7r2 cleanup.robot

*** Variables ***

*** Settings ***
Library     xiq/flows/common/Login.py
Library     xiq/flows/common/Navigator.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/configure/CommonObjects.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/configure/AutoProvisioning.py
Library     common/Cli.py

Variables   Environments/Config/device_commands.yaml
Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}

*** Keywords ***

Force Tags   testbed_1_node

*** Test Cases ***
TCCS-7436_Step1: Remove all APs, Network-Policies, SSIDs & Auto-Provision-Policies
    [Documentation]    Remove All APs

    [Tags]             production       tccs_7436_step1
    ${LOGIN_STATUS}=                 Login User              ${TENANT_USERNAME}     ${TENANT_PASSWORD}

    Navigate To Network Policies List View Page

    ${NP}=              Delete All Network Policies
    ${SSID}=            Delete All SSIDs                    exclude_list=ssid0
    ${APP}=             Delete All Auto Provision Policies

    run keyword and ignore error      Should Be Equal As Integers       ${NP}     1           Unable to delete all the Network Policies
    run keyword and ignore error      Should Be Equal As Integers       ${SSID}   1           Unable to delete all the SSIDs
    run keyword and ignore error      Should Be Equal As Integers       ${APP}    1           Unable to delete all the Auto Provision Policies
    run keywords                      quit browser

TCCS-7436_Step2: Clear capwap config
   [Documentation]     Clear capwap config

    [Tags]              production  tccs_7436_step2

    ${AP_SPAWN}=        Open Spawn          ${ap1.console_ip}   ${ap1.console_port}      ${ap1.username}       ${ap1.password}        ${ap1.platform}
    ${OUTPUT0}=         Send Commands       ${AP_SPAWN}         no capwap client server name, no capwap client default-server-name, no capwap client server backup name , no capwap client enable, capwap client enable, save config
    ${OUTPUT0}=         Send                ${AP_SPAWN}         console page 0
    ${OUTPUT0}=         Send                ${AP_SPAWN}         show version detail
    ${OUTPUT0}=         Send                ${AP_SPAWN}         show capwap client

