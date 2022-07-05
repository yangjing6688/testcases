# Author        : sagarika
# Date          : May 2020
# Description   : Configure  Autoporvision Profile

# Topology      :
# Host ----- Cloud

# Topology
# Client -----> AP --->XIQ Instance

# Pre-Condtion
# 1. AP and switch should be onboarded\
# 2. Should have Network Policies: policy1 & policy2

# Execution Command:
# robot -L INFO -v DEVICE:AP630 -v TOPO:g7r2 autoprovision_configuration.robot
# Select the Topology file based on Test bed
# Time taken to run is "17 mins"

*** Variables ***
${POLICY_NAME_01}       app_np_01
${SSID_NAME_01}         app_ssid_01

${POLICY_NAME_02}       app_np_02
${SSID_NAME_02}         app_ssid_02
${DEFAULT_POLICY_NAME}              default_network_policy

${DEFAULT_POLICY_NAME}              default_network_policy
${DEFAULT_SSID_NAME}                default_ssid
${APP_POLICY_NAME_AP_01}            app_policy_01
${APP_POLICY_NAME_SW_01}            app_policy_02
${LOCATION}                         auto_location_01, Santa Clara, building_02, floor_04

*** Settings ***
Library     common/Cli.py

Library     xiq/flows/common/Login.py
Library     xiq/flows/common/Navigator.py
Library     xiq/flows/manage/Devices.py
Library     extauto/app/common/TestFlow.py

Library     xiq/flows/configure/AutoProvisioning.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/configure/CommonObjects.py
Library     xiq/flows/configure/ExpressNetworkPolicies.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config//waits.yaml
Variables    Environments/Config/device_commands.yaml

Resource     Tests/Robot/Functional/XIQ/Wireless/Sanity/Resources/auto_provisioning_config.robot
Force Tags   testbed_1_node


Suite Setup     Cleanup-Delete AP   ${ap1.serial}       ${aerohive_sw1.serial}
Suite Teardown    Clean-up          ${ap1.serial}       ${aerohive_sw1.serial}
*** Keywords ***
Cleanup-Delete AP
    [Arguments]                             ${SERIAL1}                  ${SERIAL2}
    Login User                              ${tenant_username}          ${tenant_password}
    Delete All Auto Provision Policies

    Navigate To Devices
    Refresh Devices Page
    Delete Device                           device_serial=${SERIAL1}
    Delete Device                           device_serial=${SERIAL2}
    Delete Network Polices                  ${POLICY_NAME_01}           ${POLICY_NAME_02}
    Delete SSIDs                            ${SSID_NAME_01}             ${SSID_NAME_02}

Clean-up
    [Arguments]                             ${SERIAL1}                  ${SERIAL2}

    Delete All Auto Provision Policies
    Navigate To Devices
    Delete Device                           device_serial=${SERIAL1}
    Delete Device                           device_serial=${SERIAL2}
    Delete Network Polices                  ${POLICY_NAME_01}           ${POLICY_NAME_02}
    Delete SSIDs                            ${SSID_NAME_01}             ${SSID_NAME_02}

    [Teardown]   run keywords               logout user
    ...                                     quit browser

Configure XIQ on Fastpath Switch
    [Arguments]         ${SPAWN}            ${sw_capwap_url}
    ${OUTPUT0}=         Send                ${SPAWN}         Hivemanager address ${sw_capwap_url}
    ${OUTPUT0}=         Send                ${SPAWN}         Application stop hiveagent
    ${OUTPUT0}=         Send                ${SPAWN}         Application start hiveagent


Configure XIQ on Aerohive Switch
    [Arguments]         ${SPAWN}            ${capwap_url}
    ${OUTPUT0}=         Send                ${SPAWN}            capwap client server name ${capwap_url}
    ${OUTPUT0}=         Send                ${SPAWN}            capwap client default-server-name ${capwap_url}
    ${OUTPUT0}=         Send                ${SPAWN}            no capwap client enable
    ${OUTPUT0}=         Send                ${SPAWN}            capwap client enable
    ${OUTPUT0}=         Send                ${SPAWN}            save config

*** Test Cases ***
TCCS-7632: Configure AP Auto Provision Profile
    [Documentation]         Configure AP Autoporvision Profile

    [Tags]                  production      tccs_7632

    ${POLICY_STATUS}=       Create Open Auth Express Network Policy     ${POLICY_NAME_01}      ${SSID_NAME_01}

    Auto Provision Basic Settings                   ${APP_POLICY_NAME_AP_01}        ${ap1.country}          &{APP_AP_01}
    Auto Provision Advanced Settings                &{AP_ADVANCED_SETTINGS_04}
    Auto Provision Device Credential                &{DEVICE_CREDENTIAL_01}
    Auto Provision Capwap Configurations            &{CAPWAP_CONFIGURATION_01}
    Save and Enable Auto Provision Policy           ${APP_POLICY_NAME_AP_01}

    ${ONBOARD_RESULT}=      Onboard Device          ${ap1.serial}           ${ap1.make}       location=${LOCATION}

    ${AP_SPAWN}=        Open Spawn                  ${ap1.ip}   ${ap1.port}      ${ap1.username}       ${ap1.password}        ${ap1.platform}
    ${OUTPUT0}=         Send Commands               ${AP_SPAWN}         capwap client server name ${capwap_url}, capwap client default-server-name ${capwap_url}, no capwap client enable, capwap client enable, save config

    Log to Console      Waiting until the AP is online
    wait_until_device_online        ${ap1.serial}       retry_count=15

    ${verify_result}=   Verify Auto Provision Policy Update     ${ap1.serial}     ${ap1.country}     &{APP_AP_01}
    Should Be Equal As Integers                     ${verify_result}        1

TCCS-7571: Configure Switch Auto Provision Profile
    [Documentation]         Configure Switch  Autoporvision Profile

    [Tags]                  production      tccs_7571

    Depends On              TCCS-7632

    ${POLICY_STATUS}=       Create Open Auth Express Network Policy         ${POLICY_NAME_02}      ${SSID_NAME_02}

    Run Keyword If     '${aerohive_sw1.platform}'=='aerohive-fastpath'               Auto Provision Basic Settings                   ${APP_POLICY_NAME_SW_01}        &{SW_SR22_SR23_01}
    Run Keyword If     '${aerohive_sw1.platform}'=='aerohive-switch'                 Auto Provision Basic Settings                   ${APP_POLICY_NAME_SW_01}        &{SW_SR20_SR21_01}

    Auto Provision Advanced Settings                &{SW_ADVANCED_SETTINGS_03}
    Auto Provision Device Credential                &{DEVICE_CREDENTIAL_01}
    Auto Provision Capwap Configurations            &{CAPWAP_CONFIGURATION_01}
    Save and Enable Auto Provision Policy           ${APP_POLICY_NAME_SW_01}

    ${ONBOARD_RESULT}=      Onboard Device          ${aerohive_sw1.serial}           ${aerohive_sw1.make}       location=${LOCATION}

    Should Be Equal As Integers                     ${ONBOARD_RESULT}          1

    ${SW_SPAWN}=        Open Spawn                  ${aerohive_sw1.ip}   ${aerohive_sw1.port}      ${aerohive_sw1.username}       ${aerohive_sw1.password}        ${aerohive_sw1.platform}

    Run Keyword If     '${aerohive_sw1.platform}'=='aerohive-fastpath'   Configure XIQ on Fastpath Switch        ${SW_SPAWN}     ${sw_capwap_url}
    Run Keyword If     '${aerohive_sw1.platform}'=='aerohive-switch'     Configure XIQ on Aerohive Switch        ${SW_SPAWN}     ${capwap_url}

    Log to Console      Waiting until the switch is online
    Sleep               ${config_push_wait}
    wait_until_device_online        ${aerohive_sw1.serial}       retry_count=15

    ${verify_result}=   Verify Auto Provision Policy Update     serial=${aerohive_sw1.serial}       country_code=NA    &{SW_SR22_SR23_01}
    Should Be Equal As Integers                     ${verify_result}        1

