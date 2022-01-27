# Author        : Heidi S. White
# Description   : Verifies the "NTP State" column on the Manage> Devices page works as expected.
#                 This is qTest test case TC-8328 in the CSIT project.

*** Settings ***
Library          common/Cli.py
Library          common/Utils.py
Library          xiq/flows/manage/Location.py

Resource         ../../ManageDevices/Resources/AllResources.robot

Force Tags       testbed_1_node

Suite Setup      Log In and Set Up Test
Suite Teardown   Tear Down Test and Close Session


*** Variables ***
${XIQ_URL}                  ${xiq.test_url}
${XIQ_USER}                 ${xiq.tenant_username}
${XIQ_PASSWORD}             ${xiq.tenant_password}
${XIQ_CAPWAP_URL}           ${xiq.capwap_url}

${DUT_SERIAL}               ${ap1.serial}
${DUT_CONSOLE_IP}           ${ap1.console_ip}
${DUT_CONSOLE_PORT}         ${ap1.console_port}
${DUT_USERNAME}             ${ap1.username}
${DUT_PASSWORD}             ${ap1.password}
${DUT_PLATFORM}             ${ap1.platform}
${DUT_MAKE}                 ${ap1.make}

${LOCATION}                 San Jose, building_01, floor_02

${DEFAULT_DEVICE_PWD}       Aerohive123
${POLICY_NAME}              Automation_Policy
${SSID_NAME}                Auto_SSID


*** Test Cases ***
Confirm NTP State Immediately After Onboarding
    [Documentation]     Confirms the default value of the NTP State column
    [Tags]              csit_tc_8328   aiq_1332    development    xiq    manage_devices    ntp_state_enabled    test1

    Onboard New Test Device       ${DUT_SERIAL}  ${DUT_MAKE}  ${LOCATION}

    Configure CAPWAP              ${DUT_CONSOLE_IP}  ${DUT_CONSOLE_PORT}  ${DUT_USERNAME}  ${DUT_PASSWORD}
    ...                           ${DUT_PLATFORM}  ${XIQ_CAPWAP_URL}
    Confirm Device Serial Online  ${DUT_SERIAL}  retry_count=20

    Refresh Devices Page
    Confirm Device Details        ${DUT_SERIAL}  NTP STATE  N/A

Confirm NTP State Ten Minutes After Onboarding
    [Documentation]     Confirms the default value of the NTP State column
    [Tags]      csit_tc_8328   aiq_1332    development    xiq    manage_devices    ntp_state_enabled    test2

    Count Down in Minutes  10

    Refresh Devices Page
    Confirm Device Details  ${DUT_SERIAL}  NTP STATE  Enabled

Confirm NTP State is Unchanged After Policy Assigned
    [Documentation]     Confirms the value of the NTP State column is unchanged after policy is assigned
    [Tags]      csit_tc_8328   aiq_1332    development    xiq    manage_devices    ntp_state_enabled    test3

    Assign Policy to Device and Confirm Success  ${POLICY_NAME}  ${DUT_SERIAL}
    sleep  ${CONFIG_PUSH_WAIT}

    Refresh Devices Page
    Confirm Device Details  ${DUT_SERIAL}  NTP STATE  Enabled


*** Keywords ***
Log In and Set Up Test
    [Documentation]     Logs into XIQ and configures pre-requisites for the test

    Log Into XIQ and Confirm Success  ${XIQ_USER}  ${XIQ_PASSWORD}  ${XIQ_URL}

    Change Device Password and Confirm Success      ${DEFAULT_DEVICE_PWD}
    Create Open Express Policy and Confirm Success  ${POLICY_NAME}  ${SSID_NAME}

Tear Down Test and Close Session
    [Documentation]     Cleans up the components created during the test and ends the test

    Navigate to Devices and Confirm Success
    Delete Device and Confirm Success  ${DUT_SERIAL}

    Delete Policy and Confirm Success  ${POLICY_NAME}
    Delete SSID and Confirm Success    ${SSID_NAME}

    Log Out of XIQ and Quit Browser

Onboard New Test Device
    [Documentation]     Onboards the specified test device, deleting it first if it already exists
    [Arguments]         ${serial}  ${make}  ${location}

    Navigate to Devices and Confirm Success

    # If the device has already been onboarded, delete it first
    Delete Device and Confirm Success  ${serial}

    # Onboard the device
    Onboard Device  ${serial}  ${make}  location=${location}

    # Confirm the device was added successfully
    Confirm Device Serial Present  ${serial}

Configure CAPWAP
    [Documentation]     Configures the CAPWAP client
    [Arguments]         ${ip}  ${port}  ${user}  ${pwd}  ${platform}  ${capwap_server}

    ${spawn}=    Open Spawn  ${ip}  ${port}  ${user}  ${pwd}  ${platform}

    Send         ${spawn}   capwap client server name ${capwap_server}
    Send         ${spawn}   capwap client default-server-name ${capwap_server}
    Send         ${spawn}   capwap client server backup name ${capwap_server}
    Send         ${spawn}   no capwap client enable
    Send         ${spawn}   capwap client enable
    Send         ${spawn}   save config

    Close Spawn  ${spawn}

Confirm Device Details
    [Documentation]     Checks the specified value of the specified device and confirms it matches the expected value
    [Arguments]         ${serial}  ${column_name}  ${expected_value}

    ${result}=          Get Device Details  ${serial}   ${column_name}
    Should Contain      ${result}   ${expected_value}
