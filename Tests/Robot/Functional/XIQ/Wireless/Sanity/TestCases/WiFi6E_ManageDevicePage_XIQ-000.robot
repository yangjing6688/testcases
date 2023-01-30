# Date          : 4th October 2021
# Description   : APC-45642: WiFi 6E - manage device page: Verify the 3 new columns of WiFi2 Power/WiFi2 Channel/WiFi2 Radio Profile values for AP 4000/Ap4000U.
# Precondition  : AP4000 or AP4000U Should be onboarded with a network policy having WiFi2 SSID.
# Initial version by kunal Babbar, modified by Jay Moorkoth
#****************************************************************************************************************************************************************
# Execution Commands: The testcases in this script can be run either independently or together depending on the tags.
# robot -L INFO -i p2 WiFi6E_ManageDevicePage_XIQ-000.robot
# robot -L INFO -i TCCS-12167 WiFi6E_ManageDevicePage_XIQ-000.robot
# robot -L INFO -i TCCS-12185 WiFi6E_ManageDevicePage_XIQ-000.robot
# robot -L INFO -i TCCS-12179 WiFi6E_ManageDevicePage_XIQ-000.robot
# robot -L INFO -i TCCS-12153 WiFi6E_ManageDevicePage_XIQ-000.robot
# robot -L INFO -i TCCS-12155 WiFi6E_ManageDevicePage_XIQ-000.robot
# robot -L INFO -i TCCS-12148 WiFi6E_ManageDevicePage_XIQ-000.robot
# Select the "TOPO" and "DEVICE" variable based on Test bed to run the following execution
# robot -L INFO -v DEVICE:AP4000U -v TOPO:g2r1  WiFi6E_ManageDevicePage_XIQ-000.robot
#****************************************************************************************************************************************************************
*** Variables ***
${DEVICE}
${TOPO}
${EXIT_LEVEL}                  test_suite
${RECORD}                      True
${NTP_STATE_COLUMN}            NTP STATE
${AP1_NETWORK_POLICY}          Test_Policy
${POWER_VALUE}                 1
${CHANNEL_INPUT}               39
${RADIO_PROFILE_NAME}          jay-radio_ng_11ax-6g
*** Settings ***
Library     Collections
Library     common/Cli.py
Library     common/Utils.py
Library     common/TestFlow.py
Library     xiq/flows/common/Login.py
Library     xiq/flows/common/Navigator.py
Library     xiq/flows/manage/Client.py
Library     xiq/flows/configure/CommonObjects.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/Device360.py
Library     xiq/flows/manage/DeviceCliAccess.py
Library     xiq/flows/manage/DeviceConfig.py
Library     xiq/flows/globalsettings/GlobalSetting.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/configure/ExpressNetworkPolicies.py
Library     xiq/elements/NetworkPolicyWebElements.py
Library     xiq/flows/configure/RadioProfile.py
Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml

Force Tags   testbed_1_node

Suite Teardown  Clean-up

*** Keywords ***

Clean-up
    [Documentation]         Cleanup script

    [Tags]                  cleanup    development 

    ${LOGIN_STATUS}=                Login User              ${tenant_username}     ${tenant_password}
    should be equal as integers     ${LOGIN_STATUS}               1

    ${DELETE_DEVICE_STATUS1}=            Delete Device                  device_serial=${ap1.serial}
    should be equal as integers     ${DELETE_DEVICE_STATUS1}               1

    ${DELETE_DEVICE_STATUS2}=            Delete Device                  device_serial=${ap2.serial}
    should be equal as integers     ${DELETE_DEVICE_STATUS2}               1

    [Teardown]   run keywords        Logout User
    ...                              quit browser

*** Test Cases ***
TCCS-12167: Verify Column Wifi2 Radio Profile Default
    [Documentation]    Verify the new column values of WiFi2 Radio Profile for AP4000/AP4000U.
    [Tags]             tccs-12167  development  
    ${result}            Login User      ${tenant_username}     ${tenant_password}
    navigate_to_radio_profile
    update_override_configuration_to_device  device_serial=${ap1.serial}
    Sleep   1mins
    Refresh Devices Page
    ${RADIO_PROFILE}=        Get Ap WIFI2 Radio Profile        ${ap1.serial}
    Log to Console      RADIO_PROFILE=${RADIO_PROFILE}
    should contain     radio_ng_11ax-6g            ${RADIO_PROFILE} 
    [Teardown]   run keywords       Logout User
    ...                             Quit Browser
TCCS-12185: Verify Column Wifi2 Channel Default
    [Documentation]    Verify the new column values of WiFi2 Channel for AP 4000/Ap4000U.
    [Tags]             tccs-12185    development   
    [Setup]            Login User      ${TENANT_USERNAME}     ${TENANT_PASSWORD}
    navigate_to_radio_profile
    add_radio_profile   ${RADIO_PROFILE_NAME}
    ${WIFI2_RADIO_STATUS}=     enable_radio_status         ON      interface=wifi2
    Log to Console       ${WIFI2_RADIO_STATUS} 
    ${CHANNEL_STATUS}=         config_radio_profile_radio_channel     channel_selection=Auto
    Log to Console      *** Channel Status *** 
    Log to Console      ${CHANNEL_STATUS} 
    save_radio_profile  ${RADIO_PROFILE_NAME}
    update_override_configuration_to_device  device_serial=${ap1.serial}
    Log to Console      *** Updated config radio***
    Sleep   1mins
    ${SPAWN2}=      Open Spawn         ${ap1.ip}    ${ap1.port}     ${ap1.username}     ${ap1.password}     ${ap1.cli_type}
    ${OUTPUT2}=            Send Commands       ${SPAWN2}         show acsp | in wifi2
    ${CHANNEL}=      Get Ap Wifi2 Channel      ${ap1.serial}
    Log to Console      *** Channel is   ***
    Log to Console      ${CHANNEL} 
    Log to Console      *** OUTPUT2 is   ***
    Log to Console      ${OUTPUT2}
    Sleep   1mins
    Close Spawn         ${SPAWN2}
    Sleep   1mins
    Refresh Devices Page
    Sleep   1mins
    should contain       ${OUTPUT2}     ${CHANNEL}            
    [Teardown]   run keywords       Logout User
    ...                             Quit Browser
TCCS-12179: Verify Column Wifi2 Power Default
    [Documentation]    Verify the new column values of WiFi2 Power for AP4000/Ap4000U.
    [Tags]             tccs-12179     development 
    [Setup]            Login User      ${TENANT_USERNAME}     ${TENANT_PASSWORD}
    navigate_to_radio_profile
    add_radio_profile   ${RADIO_PROFILE_NAME}
    ${WIFI2_RADIO_STATUS}=     enable_radio_status         ON      interface=wifi2
    ${POWER_STATUS}=    conf_transmission_power_auto    Auto
    save_radio_profile  ${RADIO_PROFILE_NAME}
    update_override_configuration_to_device  device_serial=${ap1.serial}
    ${SPAWN2}=      Open Spawn         ${ap1.ip}    ${ap1.port}     ${ap1.username}     ${ap1.password}     ${ap1.cli_type}
    ${OUTPUT2}=            Send Commands       ${SPAWN2}         show acsp | in wifi2
    ${POWER}=        Get Ap WIFI2 Power        ${ap1.serial}
    Close Spawn            ${SPAWN2}
    should be equal as integers             ${POWER_STATUS}     1
    [Teardown]   run keywords       Logout User
    ...                             Quit Browser
TCCS-12153: Verify Non Supported AP Model
    [Documentation]    Verify the 3 new columns names and values for non supported AP model
    [Tags]             tccs-12153     development 
    [Setup]            Login User      ${TENANT_USERNAME}     ${TENANT_PASSWORD}
    ${CHANNEL}=      Get Ap WIFI2 Channel      ${ap2.serial}
    ${POWER}=        Get Ap WIFI2 Power        ${ap2.serial}
    ${RADIO_PROFILE}=        Get Ap WIFI2 Radio Profile        ${ap2.serial}
    should contain    ${CHANNEL}      N/A
    should contain    ${RADIO_PROFILE}   N/A
    [Teardown]   run keywords       Logout User
    ...                             Quit Browser
TC-12155: Verify Column Wifi2 Radio Profile Manual
    [Documentation]    Verify the new column values of WiFi2 Radio Profile for AP4000/AP4000U.
    [Tags]             tccs-12155     development 
    [Setup]            Login User      ${TENANT_USERNAME}     ${TENANT_PASSWORD}
    navigate_to_radio_profile
    add_radio_profile   ${RADIO_PROFILE_NAME}
    save_radio_profile  ${RADIO_PROFILE_NAME}
    update_override_configuration_to_device  device_serial=${ap1.serial}
    sleep    2mins
    ${SPAWN2}=      Open Spawn         ${ap1.ip}    ${ap1.port}     ${ap1.username}     ${ap1.password}     ${ap1.cli_type}
    ${OUTPUT2}=            Send Commands       ${SPAWN2}         show run | in wifi2
    Log to Console    ${OUTPUT2} 
    sleep    1mins
    Close Spawn            ${SPAWN2}
    sleep    2mins
    Refresh Devices Page
    ${RADIO_PROFILE}=        Get Ap WIFI2 Radio Profile        ${ap1.serial}
    Log to Console    ${RADIO_PROFILE}
    should contain          ${OUTPUT2}      ${RADIO_PROFILE}
    [Teardown]   run keywords       Logout User
    ...                             Quit Browser
TC-12148: Verify Column Wifi2 Channel Manual
    [Documentation]    Verify the column values of WiFi2 Channel by user entry for AP4000/AP4000U.
    [Tags]             tccs-12148     development 
    [Setup]            Login User      ${TENANT_USERNAME}     ${TENANT_PASSWORD}
    navigate_to_radio_profile
    add_radio_profile   ${RADIO_PROFILE_NAME}
    ${WIFI2_RADIO_STATUS}=     enable_radio_status         ON      interface=wifi2
    Log to Console       ${WIFI2_RADIO_STATUS}
    ${CHANNEL_STATUS}=         config_radio_profile_radio_channel     channel_selection=${CHANNEL_INPUT}
    Log to Console      *** Channel Status ***
    Log to Console      ${CHANNEL_STATUS}
    save_radio_profile  ${RADIO_PROFILE_NAME}
    update_override_configuration_to_device  device_serial=${ap1.serial}
    sleep    1mins
    Refresh Devices Page
    sleep    1mins
    ${SPAWN2}=      Open Spawn         ${ap1.ip}    ${ap1.port}     ${ap1.username}     ${ap1.password}     ${ap1.cli_type}
    ${OUTPUT2}=            Send Commands       ${SPAWN2}         show acsp | in wifi2
    ${CHANNEL}=      Get Ap WIFI2 Channel      ${ap1.serial}
    sleep    1mins
    Close Spawn            ${SPAWN2}
    sleep    1mins
    should be equal as integers             ${WIFI2_RADIO_STATUS}     1
    should be equal as integers             ${CHANNEL_STATUS}   1
    [Teardown]   run keywords       Logout User
    ...                             Quit Browser
