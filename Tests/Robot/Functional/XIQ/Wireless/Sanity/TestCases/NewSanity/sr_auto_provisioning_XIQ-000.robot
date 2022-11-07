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
${POLICY_NAME_02}       auto_provisioning_app_np_02
${SSID_NAME_02}         auto_provisioning_app_ssid_02
${DEFAULT_POLICY_NAME}              auto_provisioning_default_network_policy

${DEFAULT_POLICY_NAME}              auto_provisioning_default_network_policy
${DEFAULT_SSID_NAME}                auto_provisioning_default_ssid
${APP_POLICY_NAME_SW_01}            auto_provisioning_app_policy_02
${LOCATION}                         auto_location_01, Santa Clara, building_02, floor_04

*** Settings ***
Library     extauto/common/Cli.py

Library     extauto/xiq/flows/common/Login.py
Library     extauto/xiq/flows/common/Navigator.py
Library     extauto/xiq/flows/manage/Devices.py

Library     extauto/xiq/flows/configure/AutoProvisioning.py
Library     extauto/xiq/flows/configure/NetworkPolicy.py
Library     extauto/xiq/flows/configure/CommonObjects.py
Library     extauto/xiq/flows/configure/ExpressNetworkPolicies.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config//waits.yaml
Variables    Environments/Config/device_commands.yaml

Resource     Resources/sr_auto_provisioning_config.robot
Force Tags   testbed_1_node


Suite Setup     Test Suite Setup
Suite Teardown    Test Suite Teardown
*** Keywords ***
Test Suite Setup

    # Log into the device
    ${SPAWN_SW}=  open spawn  ${aerohive_sw1.ip}  ${aerohive_sw1.port}  ${aerohive_sw1.username}  ${aerohive_sw1.password}  ${aerohive_sw1.cli_type}
    Set Global Variable    ${MAIN_DEVICE_SPAWN_SW}    ${SPAWN_SW}

    # log in the user
    Login User      ${tenant_username}      ${tenant_password}

    ${search_result}=   Search Device       device_serial=${aerohive_sw1.serial}    ignore_cli_feedback=true
    # Disconnect from Extreme Cloud IQ
    Run Keyword If  '${search_result}' == '1'       Delete and Disconnect Device From Cloud  ${aerohive_sw1}  ${MAIN_DEVICE_SPAWN_SW}

     # Clean up
    ${DLT_ALL_AUTOPROV_POLICIES}=       Delete All Auto Provision Policies
    should be equal as integers         ${DLT_ALL_AUTOPROV_POLICIES}               1

    Delete Network Polices              ${POLICY_NAME_02}   ignore_cli_feedback=true
    Delete SSIDs                        ${SSID_NAME_02}     ignore_cli_feedback=true

Test Suite Teardown
    Navigate To Devices
    Refresh Devices Page

    ${search_result}=   Search Device       device_serial=${aerohive_sw1.serial}    ignore_cli_feedback=true
    # Disconnect from Extreme Cloud IQ
    Run Keyword If  '${search_result}' == '1'       Delete and Disconnect Device From Cloud  ${aerohive_sw1}  ${MAIN_DEVICE_SPAWN_SW}

    ${DLT_ALL_AUTOPROV_POLICIES}=       Delete All Auto Provision Policies
    should be equal as integers         ${DLT_ALL_AUTOPROV_POLICIES}               1

    Delete Network Polices              ${POLICY_NAME_02}   ignore_cli_feedback=true
    Delete SSIDs                        ${SSID_NAME_02}     ignore_cli_feedback=true

    close spawn  ${MAIN_DEVICE_SPAWN_SW}

    [Teardown]   run keywords               logout user
    ...                                     quit browser

Delete and Disconnect Device From Cloud
    [Arguments]                             ${device}  ${SPAWN}
    delete device   device_serial=${device.serial}
    disconnect device from cloud     ${device.cli_type}     ${SPAWN}

Clean Up Device
    [Arguments]                             ${device}  ${SPAWN}
    ${search_result}=   Search Device       device_serial=${device.serial}    ignore_cli_feedback=true
    # Disconnect from Extreme Cloud IQ
    Run Keyword If  '${search_result}' == '1'       Delete and Disconnect Device From Cloud  ${device.cli_type}     ${SPAWN}

Device Onboard
    [Arguments]                             ${device}  ${SPAWN}  ${generic_capwap_url}
    # onboard the device
    Clean Up Device     ${device}  ${SPAWN}

    ${ONBOARD_RESULT}=          onboard device quick     ${device}
    Should Be Equal As Strings                  ${ONBOARD_RESULT}       1

    configure device to connect to cloud    ${device.cli_type}   ${generic_capwap_url}   ${SPAWN}

    ${ONLINE_STATUS_RESULT}=    wait until device online     ${device.serial}
    Should Be Equal As Strings                  ${ONLINE_STATUS_RESULT}       1

    ${REBOOT_STATUS_RESULT}=    Wait Until Device Reboots               ${device.serial}
    Should Be Equal as Integers             ${REBOOT_STATUS_RESULT}          1

    ${MANAGED_STATUS_RESULT}=   wait until device managed   ${device.serial}
    Should Be Equal As Strings                  ${MANAGED_STATUS_RESULT}      1

    ${DEVICE_STATUS_RESULT}=    get device status      ${device.serial}
    Should Be Equal As Strings                  ${DEVICE_STATUS_RESULT}      green


*** Test Cases ***
TCCS-7571: Configure Switch Auto Provision Profile
    [Documentation]         Configure Switch  Autoporvision Profile

    [Tags]                  production      tccs_7571

    ${POLICY_STATUS}=           Create Open Auth Express Network Policy     ${POLICY_NAME_02}      ${SSID_NAME_02}
    should be equal as integers             ${POLICY_STATUS}                1

    IF  '${aerohive_sw1.cli_type}'=='AH-FASTPATH'
        &{SW_SR22_SR23_01}=    Create Dictionary      device_function=Extreme Networks SR22xx / SR23xx Switches       device_model=${aerohive_sw1.model}     service_tags=Disable   ip_subnetworks=Disable      network_policy=${POLICY_NAME_02}
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

    Device Onboard   ${aerohive_sw1}  ${MAIN_DEVICE_SPAWN_SW}  ${sw_capwap_url}

    ${verify_result}=   Verify Auto Provision Policy Update     serial=${aerohive_sw1.serial}       country_code=NA    &{SW_SR22_SR23_01}
    Should Be Equal As Integers                     ${verify_result}        1

    ${update_result}=   Wait Until device update done   device_serial=${aerohive_sw1.serial}
    Should Be Equal As Integers                     ${update_result}        1

    Sleep       ${max_config_push_time}