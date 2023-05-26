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

# The keywords in Login.py have been moved to the keywords directory.
# If the moved keyword is not working correctly import the original library and remove the keywords/gui/login/KeywordsLogin.py version.
#Library     extauto/xiq/flows/common/Login.py
Library     keywords/gui/login/KeywordsLogin.py
Library     extauto/xiq/flows/common/Navigator.py
Library     extauto/xiq/flows/manage/Devices.py

Library     extauto/xiq/flows/configure/AutoProvisioning.py
Library     extauto/xiq/flows/configure/NetworkPolicy.py
Library     extauto/xiq/flows/configure/CommonObjects.py
Library     extauto/xiq/flows/configure/ExpressNetworkPolicies.py
Library     ExtremeAutomation/Imports/CommonObjectUtils.py
Library     ExtremeAutomation/Keywords/UserDefinedKeywords/NetworkElements/SetupTeardown/SetupTeardownUdks.py
Library     keywords/gui/manage/KeywordsDevices.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config//waits.yaml
Variables    Environments/Config/device_commands.yaml

Resource     Tests/Robot/Functional/XIQ/Wireless/Sanity/Resources/sr_auto_provisioning_config.robot
Force Tags   testbed_1_node


Suite Setup     Test Suite Setup
Suite Teardown    Run Keyword And Warn On Failure    Test Suite Teardown
*** Keywords ***
Test Suite Setup
    # Use this method to convert the ap, wing, netelem to a generic device object
    # ap1       => device1
    # wing1     => device1
    # netelem1  => device1 (EXOS / VOSS)
    convert to generic device object   device  index=1

    # Create the connection to the device(s)
    Base Test Suite Setup
    Set Global Variable    ${MAIN_DEVICE_SPAWN}    ${device1.name}

    # log in the user
    ${LOGIN_STATUS}=                Login User          ${tenant_username}      ${tenant_password}     check_warning_msg=True
    should be equal as integers     ${LOGIN_STATUS}               1

    ${search_result}=   keywordsdevices.search device       ${device1}    ignore_failure=True
    # Disconnect from Extreme Cloud IQ
    Run Keyword If  '${search_result}' == '1'       Delete and Disconnect Device From Cloud  ${device1}  ${MAIN_DEVICE_SPAWN}

     # Clean up
    ${DLT_ALL_AUTOPROV_POLICIES}=       Delete All Auto Provision Policies
    should be equal as integers         ${DLT_ALL_AUTOPROV_POLICIES}               1

    ${DELETE_POLICIES_RESULT}=      Delete Network Polices          ${POLICY_NAME_02}   ignore_cli_feedback=true
    Should Be Equal As Integers     ${DELETE_POLICIES_RESULT}           1

    ${DELETE_SSID_RESULT}=          Delete SSIDs                    ${SSID_NAME_02}             ignore_cli_feedback=true
    Should Be Equal As Integers     ${DELETE_SSID_RESULT}               1

Test Suite Teardown
    ${NAVIGATE_STATUS}=     Navigate To Devices
    Should Be Equal As Integers     ${NAVIGATE_STATUS}               1

    ${REFRESH_PAGE_STATUS}=     Refresh Devices Page
    Should Be Equal As Integers     ${REFRESH_PAGE_STATUS}               1

    ${search_result}=   keywordsdevices.search device       ${device1}    ignore_failure=True
    # Disconnect from Extreme Cloud IQ
    Run Keyword If  '${search_result}' == '1'       Delete and Disconnect Device From Cloud  ${device1}  ${MAIN_DEVICE_SPAWN}

    ${DLT_ALL_AUTOPROV_POLICIES}=       Delete All Auto Provision Policies
    should be equal as integers         ${DLT_ALL_AUTOPROV_POLICIES}               1

    ${DELETE_POLICIES_RESULT}=      Delete Network Polices          ${POLICY_NAME_02}   ignore_cli_feedback=true
    Should Be Equal As Integers     ${DELETE_POLICIES_RESULT}           1

    ${DELETE_SSID_RESULT}=          Delete SSIDs                    ${SSID_NAME_02}             ignore_cli_feedback=true
    Should Be Equal As Integers     ${DELETE_SSID_RESULT}               1

    [Teardown]   run keywords               logout user
    ...                                     quit browser

Delete and Disconnect Device From Cloud
    [Arguments]                             ${device}  ${SPAWN}
    ${DELETE_DEVICE}=          keywordsdevices.delete device        ${device}
    Should Be Equal As Integers     ${DELETE_DEVICE}               1
    ${DISCONNECT_RESULT}=          disconnect device from cloud     ${device.cli_type}     ${SPAWN}
    Should Be Equal As Integers     ${DISCONNECT_RESULT}               1

Clean Up Device
    [Arguments]                             ${device}  ${SPAWN}
    ${search_result}=   keywordsdevices.search device       ${device}    ignore_failure=True
    # Disconnect from Extreme Cloud IQ
    Run Keyword If  '${search_result}' == '1'       Delete and Disconnect Device From Cloud  ${device}     ${SPAWN}

Device Onboard
    [Arguments]                             ${device}  ${SPAWN}  ${generic_capwap_url}
    # onboard the device
    Clean Up Device     ${device}  ${SPAWN}

    ${CONF_RESULT}=         Configure Device To Connect To Cloud            ${device.cli_type}     ${generic_capwap_url}   ${MAIN_DEVICE_SPAWN}
    Should Be Equal As Integers     ${CONF_RESULT}          1

    ${ONBOARD_RESULT}=          onboard device quick     ${device}
    Should Be Equal As Strings                  ${ONBOARD_RESULT}       1

    ${WAIT_CONF_RESULT}=    Wait For Configure Device To Connect To Cloud   ${device.cli_type}     ${generic_capwap_url}   ${MAIN_DEVICE_SPAWN}
    Should Be Equal As Integers     ${WAIT_CONF_RESULT}     1

    ${ONLINE_STATUS_RESULT}=    wait until device online     ${device.serial}
    Should Be Equal As Strings                  ${ONLINE_STATUS_RESULT}       1

    ${REBOOT_STATUS_RESULT}=    Wait Until Device Reboots               ${device.serial}
    Should Be Equal as Integers             ${REBOOT_STATUS_RESULT}          1

    ${MANAGED_STATUS_RESULT}=   wait until device managed   ${device.serial}
    Should Be Equal As Strings                  ${MANAGED_STATUS_RESULT}      1

    ${DEVICE_STATUS_RESULT}=    get device status      ${device.serial}
    Should contain any                  ${DEVICE_STATUS_RESULT}    green     config audit mismatch

*** Test Cases ***
TCCS-7571: Configure Switch Auto Provision Profile
    [Documentation]         Configure Switch  Autoporvision Profile

    [Tags]                  production      tccs_7571

    ${POLICY_STATUS}=           Create Open Auth Express Network Policy     ${POLICY_NAME_02}      ${SSID_NAME_02}
    should be equal as integers             ${POLICY_STATUS}                1

    IF  '${device1.cli_type}'=='AH-FASTPATH'
        &{SW_SR22_SR23_01}=    Create Dictionary      device_function=Extreme Networks SR22xx / SR23xx Switches       device_model=${device1.model}     service_tags=Disable   ip_subnetworks=Disable      network_policy=${POLICY_NAME_02}
        ${APP_BASIC_STGS_STATUS}=     Auto Provision Basic Settings                   ${APP_POLICY_NAME_SW_01}        ${SW_SR22_SR23_01}
        should be equal as integers             ${APP_BASIC_STGS_STATUS}        1
    ELSE IF     '${device1.cli_type}'=='AH-AP'
        ${APP_BASIC_STGS_STATUS}=   Auto Provision Basic Settings                   ${APP_POLICY_NAME_SW_01}        ${SW_SR20_SR21_01}
        should be equal as integers             ${APP_BASIC_STGS_STATUS}        1
    END

    Auto Provision Advanced Settings                &{SW_ADVANCED_SETTINGS_03}

    Auto Provision Device Credential                &{DEVICE_CREDENTIAL_01}

    Auto Provision Capwap Configurations            &{CAPWAP_CONFIGURATION_01}

    Save and Enable Auto Provision Policy           ${APP_POLICY_NAME_SW_01}

    Device Onboard   ${device1}  ${MAIN_DEVICE_SPAWN}  ${sw_capwap_url}

    Sleep       1min

    ${verify_result}=   Verify Auto Provision Policy Update     ${device1.serial}      ${SW_SR22_SR23_01}
    Should Be Equal As Integers                     ${verify_result}        1

    ${update_result}=   Wait Until device update done   device_serial=${device1.serial}
    Should Be Equal As Integers                     ${update_result}        1
