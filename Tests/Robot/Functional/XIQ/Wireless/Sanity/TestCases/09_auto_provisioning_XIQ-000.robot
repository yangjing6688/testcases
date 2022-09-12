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
Library     extauto/common/Cli.py

Library     xiq/flows/common/Login.py
Library     xiq/flows/common/Navigator.py
Library     xiq/flows/manage/Devices.py

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
    ${LOGIN_STATUS}=                    Login User      ${tenant_username}      ${tenant_password}      check_warning_msg=True
    should be equal as integers         ${LOGIN_STATUS}               1

    ${DLT_ALL_AUTOPROV_POLICIES}=       Delete All Auto Provision Policies
    should be equal as integers         ${DLT_ALL_AUTOPROV_POLICIES}               1

    Navigate To Devices
    Refresh Devices Page

    ${DELETE_DEVICE_STATUS1}=       Delete Device                  device_serial=${SERIAL1}
    should be equal as integers     ${DELETE_DEVICE_STATUS1}    1

    ${DELETE_DEVICE_STATUS2}=       Delete Device                  device_serial=${SERIAL2}
    should be equal as integers     ${DELETE_DEVICE_STATUS2}    1

    ${DLT_NW_POLICIES}=             Delete Network Polices                  ${POLICY_NAME_01}           ${POLICY_NAME_02}
    should be equal as integers     ${DLT_NW_POLICIES}          1

    ${DELETE_SSIDS}=                Delete SSIDs                            ${SSID_NAME_01}             ${SSID_NAME_02}
    should be equal as integers     ${DELETE_SSIDS}             1

Clean-up
    [Arguments]                             ${SERIAL1}                  ${SERIAL2}

    Navigate To Devices
    Refresh Devices Page

    ${DELETE_DEVICE_STATUS1}=       Delete Device       device_serial=${SERIAL1}
    should be equal as integers     ${DELETE_DEVICE_STATUS1}    1

    ${DELETE_DEVICE_STATUS2}=       Delete Device       device_serial=${SERIAL2}
    should be equal as integers     ${DELETE_DEVICE_STATUS2}    1

    ${DLT_ALL_AUTOPROV_POLICIES}=       Delete All Auto Provision Policies
    should be equal as integers         ${DLT_ALL_AUTOPROV_POLICIES}               1

    ${DLT_NW_POLICIES}=             Delete Network Polices                  ${POLICY_NAME_01}           ${POLICY_NAME_02}
    should be equal as integers     ${DLT_NW_POLICIES}          1

    ${DELETE_SSIDS}=                Delete SSIDs                            ${SSID_NAME_01}             ${SSID_NAME_02}
    should be equal as integers     ${DELETE_SSIDS}             1

    [Teardown]   run keywords               logout user
    ...                                     quit browser

*** Test Cases ***
TCCS-7632: Configure AP Auto Provision Profile
    [Documentation]         Configure AP Autoporvision Profile

    [Tags]                  production      tccs_7632

    ${POLICY_STATUS}=           Create Open Auth Express Network Policy     ${POLICY_NAME_01}      ${SSID_NAME_01}
    should be equal as integers             ${POLICY_STATUS}                1

    ${APP_BASIC_STGS_STATUS}=   Auto Provision Basic Settings                   ${APP_POLICY_NAME_AP_01}        ${ap1.country}          &{APP_AP_01}
    should be equal as integers             ${APP_BASIC_STGS_STATUS}        1

    Auto Provision Advanced Settings                &{AP_ADVANCED_SETTINGS_04}

    Auto Provision Device Credential                &{DEVICE_CREDENTIAL_01}

    Auto Provision Capwap Configurations            &{CAPWAP_CONFIGURATION_01}

    Save and Enable Auto Provision Policy           ${APP_POLICY_NAME_AP_01}

    ${ONBOARD_RESULT}=      Onboard Device          ${ap1.serial}           ${ap1.make}       location=${LOCATION}      device_os=${ap1.cli_type}
    Should Be Equal As Integers                     ${ONBOARD_RESULT}          1

    ${SPAWN_CONNECTION}=      Open Spawn    ${ap1.ip}     ${ap1.port}   ${ap1.username}   ${ap1.password}    ${ap1.cli_type}

    ${CONF_STATUS_RESULT}=    Configure Device To Connect To Cloud             ${ap1.cli_type}       ${capwap_url}       ${SPAWN_CONNECTION}
    Should Be Equal As Strings                  ${CONF_STATUS_RESULT}       1

    Close Spawn       ${SPAWN_CONNECTION}

    Log to Console      Waiting until the AP is online

    ${CONNECTED_STATUS}=    Wait Until Device Online                ${ap1.serial}   retry_count=15
    Should Be Equal as Integers             ${CONNECTED_STATUS}          1

    ${verify_result}=   Verify Auto Provision Policy Update     ${ap1.serial}     ${ap1.country}     &{APP_AP_01}
    Should Be Equal As Integers                     ${verify_result}        1

    Sleep       ${max_config_push_time}


TCCS-7571: Configure Switch Auto Provision Profile
    [Documentation]         Configure Switch  Autoporvision Profile

    [Tags]                  production      tccs_7571

    ${POLICY_STATUS}=           Create Open Auth Express Network Policy     ${POLICY_NAME_02}      ${SSID_NAME_02}
    should be equal as integers             ${POLICY_STATUS}                1

    IF  '${aerohive_sw1.cli_type}'=='AH-FASTPATH'
        ${APP_BASIC_STGS_STATUS}=     Auto Provision Basic Settings                   ${APP_POLICY_NAME_SW_01}        &{SW_SR22_SR23_01}
        should be equal as integers             ${APP_BASIC_STGS_STATUS}        1
    ELSE IF     '${aerohive_sw1.cli_type}'=='AH-AP'
        ${APP_BASIC_STGS_STATUS}=   Auto Provision Basic Settings                   ${APP_POLICY_NAME_SW_01}        &{SW_SR20_SR21_01}
        should be equal as integers             ${APP_BASIC_STGS_STATUS}        1
    END

    Auto Provision Advanced Settings                &{SW_ADVANCED_SETTINGS_03}

    Auto Provision Device Credential                &{DEVICE_CREDENTIAL_01}

    Auto Provision Capwap Configurations            &{CAPWAP_CONFIGURATION_01}

    Save and Enable Auto Provision Policy           ${APP_POLICY_NAME_SW_01}

    ${ONBOARD_RESULT}=      Onboard Device          ${aerohive_sw1.serial}           ${aerohive_sw1.make}       location=${LOCATION}
    Should Be Equal As Integers                     ${ONBOARD_RESULT}          1

    ${SPAWN_CONNECTION}=      Open Spawn    ${aerohive_sw1.ip}     ${aerohive_sw1.port}   ${aerohive_sw1.username}   ${aerohive_sw1.password}    ${aerohive_sw1.cli_type}

    ${CONF_STATUS_RESULT}=    Configure Device To Connect To Cloud             ${aerohive_sw1.cli_type}       ${sw_capwap_url}       ${SPAWN_CONNECTION}
    Should Be Equal As Strings                  ${CONF_STATUS_RESULT}       1

    Close Spawn        ${SPAWN_CONNECTION}

    Log to Console      Waiting until the switch is online
    Sleep               ${config_push_wait}

    ${CONNECTED_STATUS}=    Wait Until Device Online                ${aerohive_sw1.serial}   retry_count=15
    Should Be Equal as Integers             ${CONNECTED_STATUS}          1

    ${verify_result}=   Verify Auto Provision Policy Update     serial=${aerohive_sw1.serial}       country_code=NA    &{SW_SR22_SR23_01}
    Should Be Equal As Integers                     ${verify_result}        1

    ${update_result}=   Wait Until device update done   device_serial=${aerohive_sw1.serial}
    Should Be Equal As Integers                     ${update_result}        1

    Sleep       ${max_config_push_time}
