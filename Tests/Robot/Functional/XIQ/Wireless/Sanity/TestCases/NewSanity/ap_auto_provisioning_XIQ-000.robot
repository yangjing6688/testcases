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
${POLICY_NAME_01}       auto_provisioning_app_np_01
${SSID_NAME_01}         auto_provisioning_app_ssid_01

${DEFAULT_POLICY_NAME}              auto_provisioning_default_network_policy

${DEFAULT_POLICY_NAME}              auto_provisioning_default_network_policy
${DEFAULT_SSID_NAME}                auto_provisioning_default_ssid
${APP_POLICY_NAME_AP_01}            auto_provisioning_app_policy_01
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

Resource     Tests/Robot/Functional/XIQ/Wireless/Sanity/Resources/ap_auto_provisioning_config.robot
Force Tags   testbed_1_node


Suite Setup     Test Suite Setup
Suite Teardown    Run Keyword And Warn On Failure    Test Suite Teardown
*** Keywords ***
Test Suite Setup

    # Log into the device
    ${SPAWN_AP}=  open spawn  ${ap1.ip}  ${ap1.port}  ${ap1.username}  ${ap1.password}  ${ap1.cli_type}
    Set Global Variable    ${MAIN_DEVICE_SPAWN_AP}    ${SPAWN_AP}

    # log in the user
    Login User      ${tenant_username}      ${tenant_password}

    ${search_result}=   Search Device       device_serial=${ap1.serial}    ignore_failure=True
    # Disconnect from Extreme Cloud IQ
    Run Keyword If  '${search_result}' == '1'       Delete and Disconnect Device From Cloud  ${ap1}  ${MAIN_DEVICE_SPAWN_AP}

     # Clean up
    ${DLT_ALL_AUTOPROV_POLICIES}=       Delete All Auto Provision Policies
    should be equal as integers         ${DLT_ALL_AUTOPROV_POLICIES}               1

    Delete Network Polices                  ${POLICY_NAME_01}           ignore_cli_feedback=true
    Delete SSIDs                            ${SSID_NAME_01}             ignore_cli_feedback=true

Test Suite Teardown
    Navigate To Devices
    Refresh Devices Page

    ${search_result}=   Search Device       device_serial=${ap1.serial}    ignore_failure=True
    # Disconnect from Extreme Cloud IQ
    Run Keyword If  '${search_result}' == '1'       Delete and Disconnect Device From Cloud  ${ap1}  ${MAIN_DEVICE_SPAWN_AP}

    ${DLT_ALL_AUTOPROV_POLICIES}=       Delete All Auto Provision Policies
    should be equal as integers         ${DLT_ALL_AUTOPROV_POLICIES}               1

    Delete Network Polices                  ${POLICY_NAME_01}           ignore_cli_feedback=true
    Delete SSIDs                            ${SSID_NAME_01}             ignore_cli_feedback=true

    close spawn  ${MAIN_DEVICE_SPAWN_AP}

    [Teardown]   run keywords               logout user
    ...                                     quit browser

Delete and Disconnect Device From Cloud
    [Arguments]                             ${device}  ${SPAWN}
    delete device   device_serial=${device.serial}
    disconnect device from cloud     ${device.cli_type}     ${SPAWN}

Clean Up Device
    [Arguments]                             ${device}  ${SPAWN}
    ${search_result}=   Search Device       device_serial=${device.serial}    ignore_failure=True
    # Disconnect from Extreme Cloud IQ
    Run Keyword If  '${search_result}' == '1'       Delete and Disconnect Device From Cloud  ${device.cli_type}     ${SPAWN}

Device Onboard
    [Arguments]                             ${device}  ${SPAWN}  ${generic_capwap_url}
    # onboard the device
    Clean Up Device     ${device}  ${SPAWN}

    ${ONBOARD_RESULT}=          onboard device quick      ${device}
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
TCCS-7632: Configure AP Auto Provision Profile
    [Documentation]         Configure AP Autoporvision Profile

    [Tags]                  production      tccs_7632

    ${POLICY_STATUS}=           Create Open Auth Express Network Policy     ${POLICY_NAME_01}      ${SSID_NAME_01}
    should be equal as integers             ${POLICY_STATUS}                1

    ${APP_BASIC_STGS_STATUS}=   Auto Provision Basic Settings                   ${APP_POLICY_NAME_AP_01}    ${APP_AP_01}    ${ap1.country}
    should be equal as integers             ${APP_BASIC_STGS_STATUS}        1

    Auto Provision Advanced Settings                &{AP_ADVANCED_SETTINGS_04}

    Auto Provision Device Credential                &{DEVICE_CREDENTIAL_01}

    Auto Provision Capwap Configurations            &{CAPWAP_CONFIGURATION_01}

    Save and Enable Auto Provision Policy           ${APP_POLICY_NAME_AP_01}

    Device Onboard   ${ap1}  ${MAIN_DEVICE_SPAWN_AP}  ${capwap_url}

    ${verify_result}=   Verify Auto Provision Policy Update     ${ap1.serial}   ${APP_AP_01}    ${ap1.country}
    Should Be Equal As Integers                     ${verify_result}        1

    ${update_result}=   Wait Until device update done   device_serial=${ap1.serial}
    Should Be Equal As Integers                     ${update_result}        1

    Sleep       ${max_config_push_time}