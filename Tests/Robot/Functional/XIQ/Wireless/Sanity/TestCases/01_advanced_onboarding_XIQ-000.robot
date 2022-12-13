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

Force Tags   testbed_1_node

Suite Setup     Cleanup-Delete AP   ${ap1.serial}
Suite Teardown  Test Suite Clean Up

*** Keywords ***
Cleanup-Delete AP
    [Arguments]     ${SERIAL}
    ${LOGIN_STATUS}=                    Login User      ${tenant_username}      ${tenant_password}      check_warning_msg=True
    should be equal as integers         ${LOGIN_STATUS}               1

    ${DELETE_DEVICE_STATUS}=                Delete Device       device_serial=${SERIAL}
    should be equal as integers         ${DELETE_DEVICE_STATUS}               1

    ${CHANGE_PASSWORD_STATUS}=          Change Device Password                  Aerohive123
    should be equal as integers         ${CHANGE_PASSWORD_STATUS}               1

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

Test Suite Clean Up
    [Documentation]    Test suite clean up

    [Tags]             production   cleanup

    ${LOGIN_STATUS}=                        Login User       ${tenant_username}        ${tenant_password}
    should be equal as integers             ${LOGIN_STATUS}               1

    ${CREATE_NW_POLICY_STATUS}=             Create Network Policy          OPEN_AUTO                 ${CONFIG_PUSH_OPEN_NW_01}
    should be equal as integers             ${CREATE_NW_POLICY_STATUS}               1

    ${UPDATE_NW_POLICY_STATUS}=             Update Network Policy To Ap    policy_name=OPEN_AUTO     ap_serial=${ap1.serial}
    should be equal as integers             ${UPDATE_NW_POLICY_STATUS}               1

    ${DELETE_NW_POLICY_STATUS}=             Delete network policy      ${ADVANCE_NW_POLICY1}
    should be equal as integers             ${DELETE_NW_POLICY_STATUS}               1

    ${DELETE_SSID_STATUS}=                  Delete ssids     ${INTERNAL_SSID_NAME1}     ${GUEST_SSID_NAME1}
    should be equal as integers             ${DELETE_SSID_STATUS}               1

    [Teardown]         run keywords    logout user
     ...                               quit browser

*** Test Cases ***
TCCS-7709_Step1: Advance Onboard Extreme-Aerohive Access Point
    [Documentation]

    [Tags]             production   tccs_7709       tccs_7709_step1

    ${LOGIN_STATUS}=                    Login User                     ${tenant_username}     ${tenant_password}
    should be equal as integers         ${LOGIN_STATUS}               1

    ${ONBOARD_STATUS}=                  Advance Onboard Device         ${ap1.serial}    device_make=${DEVICE_MAKE_AEROHIVE}   dev_location=${LOCATION}
    should be equal as integers         ${ONBOARD_STATUS}       1

    [Teardown]         run keywords    logout user
     ...                               quit browser

TCCS-7709_Step2: Config AP to Report AIO
    [Documentation]     Configure Capwap client server

    [Tags]              production          tccs_7709       tccs_7709_step2

    Depends On          TCCS-7709_Step1
    ${AP_SPAWN}=        Open Spawn          ${ap1.ip}   ${ap1.port}      ${ap1.username}       ${ap1.password}        ${ap1.cli_type}

    Should not be equal as Strings          '${AP_SPAWN}'        '-1'

    Set Suite Variable  ${AP_SPAWN}

    ${OUTPUT0}=         Send Commands       ${AP_SPAWN}         capwap client server name ${capwap_url}, capwap client default-server-name ${capwap_url}, capwap client server backup name ${capwap_url}, no capwap client enable, capwap client enable, save config

    ${OUTPUT0}=         Send                ${AP_SPAWN}         console page 0
    ${OUTPUT0}=         Send                ${AP_SPAWN}         show version detail
    ${OUTPUT0}=         Send                ${AP_SPAWN}         show capwap client
    ${OUTPUT2}=         Send                ${AP_SPAWN}         ${cmd_capwap_hm_primary_name}
    ${OUTPUT3}=         Send                ${AP_SPAWN}         ${cmd_capwap_server_ip}
    ${OUTPUT1}=         Wait For CLI Output                     ${AP_SPAWN}         ${cmd_capwap_client_state}          ${output_capwap_status}

    Should Be Equal as Integers             ${OUTPUT1}          1

    [Teardown]    Close Spawn    ${AP_SPAWN}

TCCS-7709_Step3: Check AP Status On UI
    [Documentation]     Checks for ap status

    [Tags]              production      tccs_7709       tccs_7709_step3

    Depends On          TCCS-7709_Step2
    ${LOGIN_STATUS}=          Login User          ${tenant_username}     ${tenant_password}
    should be equal as integers             ${LOGIN_STATUS}               1

    ${CONNECTED_STATUS}=    Wait Until Device Online                ${ap1.serial}
    Should Be Equal as Integers             ${CONNECTED_STATUS}          1

    ${DEVICE_STATUS}=       Get Device Status       device_mac=${ap1.serial}
    Should contain any  ${DEVICE_STATUS}    green     config audit mismatch

    [Teardown]         run keywords    logout user
     ...                               quit browser

