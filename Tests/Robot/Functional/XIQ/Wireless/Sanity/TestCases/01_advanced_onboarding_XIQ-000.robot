*** Variables ***
# Arguments passed from the command line
${ADVANCE_NW_POLICY1}        AUTO_ADVANCE_TEST
${INTERNAL_SSID_NAME1}       AUTO_INTERNAL_SSID
${GUEST_SSID_NAME1}          AUTO_GUEST_SSID
${LOCATION}                  auto_location_01, Santa Clara, building_02, floor_04
${DEVICE_MAKE_AEROHIVE}      Extreme - Aerohive

*** Settings ***
Library     common/Cli.py
Library     common/TestFlow.py

Library     xiq/flows/common/Login.py
Library     xiq/flows/manage/AdvanceOnboarding.py
Library     xiq/flows/manage/AdvOnboard.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/DeviceCliAccess.py

Library     xiq/flows/globalsettings/GlobalSetting.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/configure/CommonObjects.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml

Resource     Tests/Robot/Functional/XIQ/Wireless/Sanity/Resources/advanced_onboarding_config.robot

Force Tags   flow3   flow7

Suite Setup     Cleanup-Delete AP   ${ap1.serial}

*** Keywords ***
Cleanup-Delete AP
    [Arguments]     ${SERIAL}
    Login User      ${tenant_username}      ${tenant_password}
    Delete AP       ap_serial=${SERIAL}
    Change Device Password                  Aerohive123
    Logout User
    Quit Browser

*** Test Cases ***
Test1: Advance Onboard Extreme-Aerohive Access Point
    [Documentation]
    [Tags]             sanity     adv-onboard   Test1       production

    ${LOGIN_STATUS}=                  Login User                     ${tenant_username}     ${tenant_password}
    should be equal as strings       '${LOGIN_STATUS}'     '1'

    ${ONBOARD_STATUS}=               Advance Onboard Device         ${ap1.serial}    device_make=${DEVICE_MAKE_AEROHIVE}   dev_location=${LOCATION}
    should be equal as integers      ${ONBOARD_STATUS}       1

    [Teardown]         run keywords    logout user
     ...                               quit browser

Test2: Config AP to Report AIO
    [Documentation]     Configure Capwap client server
    [Tags]              production          ap-config       P1                Test2
    Depends On          Test1
    ${AP_SPAWN}=        Open Spawn          ${ap1.console_ip}   ${ap1.console_port}      ${ap1.username}       ${ap1.password}        ${ap1.platform}
    Set Suite Variable  ${AP_SPAWN}
    ${OUTPUT0}=         Send Commands       ${AP_SPAWN}         capwap client server name ${capwap_url}, capwap client default-server-name ${capwap_url}, capwap client server backup name ${capwap_url}, no capwap client enable, capwap client enable, save config

    ${OUTPUT0}=         Send                ${AP_SPAWN}         console page 0
    ${OUTPUT0}=         Send                ${AP_SPAWN}         show version detail
    ${OUTPUT0}=         Send                ${AP_SPAWN}         show capwap client
    ${OUTPUT2}=         Send                ${AP_SPAWN}         ${cmd_capwap_hm_primary_name}
    ${OUTPUT3}=         Send                ${AP_SPAWN}         ${cmd_capwap_server_ip}
    ${OUTPUT1}=         Wait For CLI Output                     ${AP_SPAWN}         ${cmd_capwap_client_state}          ${output_capwap_status}

    Should Be Equal as Integers             ${OUTPUT1}          1

Test3: Check AP Status On UI
    [Documentation]     Checks for ap status
    [Tags]              sanity              status-check        P1          production      Test3
    Depends On          test2
    ${result}=          Login User          ${tenant_username}     ${tenant_password}
    Wait Until Device Online                ${ap1.serial}

    Wait Until Device Reboots               ${ap1.serial}

    Wait Until Device Online                ${ap1.serial}
    ${AP_STATUS}=                           Get AP Status       ap_mac=${ap1.mac}
    Should Be Equal As Strings             '${AP_STATUS}'       'green'

    [Teardown]         run keywords    logout user
     ...                               quit browser

Test Suite Clean Up
    [Documentation]    Test suite clean up
    [Tags]             production   adv-onboard

    ${result}=    Login User       ${tenant_username}        ${tenant_password}
    Create Network Policy          OPEN_AUTO                 &{CONFIG_PUSH_OPEN_NW_01}
    Update Network Policy To Ap    policy_name=OPEN_AUTO     ap_serial=${ap1.serial}

    delete network policy      ${ADVANCE_NW_POLICY1}
    delete ssids     ${INTERNAL_SSID_NAME1}     ${GUEST_SSID_NAME1}

    [Teardown]         run keywords    logout user
     ...                               quit browser
