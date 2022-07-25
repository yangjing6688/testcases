# Author        : Ramkumar
# Date          : March 06th 2020
# Description   : Aerohive Switch Onboard Testcases
#
# Topology      :
# Host ----- Cloud

*** Variables ***
${LOCATION}                 auto_location_01, Santa Clara, building_02, floor_04
${DEVICE_MAKE_AEROHIVE}     Extreme - Aerohive

*** Settings ***
Library     common/Utils.py
Library     extauto/common/Cli.py
Library     xiq/flows/common/Login.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/Switch.py
Library     xiq/flows/manage/AdvOnboard.py
Library     xiq/flows/manage/AdvanceOnboarding.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml

Force Tags   testbed_1_node
Suite Setup     Suite Setup
Suite Teardown  Suite Teardown

*** Keywords ***
Suite Setup
    ${LOGIN_RESULT}=    Login User      ${tenant_username}      ${tenant_password}
    Should Be Equal as Integers         ${LOGIN_RESULT}         1
    Delete Device                       ${aerohive_sw1.serial}

Suite Teardown
    Run Keywords        logout user
    ...                 quit browser

*** Test Cases ***
TCCS-7748_Step1: Onboard Aerohive Switch
    [Documentation]         Checks for Aerohive switch onboarding is success in case of valid scenario

    [Tags]                  production      tccs_7748   tccs_7748_step1
    ${ONBOARD_RESULT}=  Onboard Device  ${aerohive_sw1.serial}  ${aerohive_sw1.cli_type}    location=${LOCATION}
    Should Be Equal as Integers         ${ONBOARD_RESULT}       1


TCCS-7748_Step2: Config Aerohive/Fastpath Switch to Report AIO
    [Documentation]     Config Aerohive Switch to Report AIO

    [Tags]              production         tccs_7748    tccs_7748_step2
    IF          '${aerohive_sw1.cli_type}'=='AH-FASTPATH'
                    Set Test Variable   ${CAPWAP_URL}   ${sw_capwap_url}
    ELSE IF     '${aerohive_sw1.cli_type}'=='AH-AP'
                    Set Test Variable   ${CAPWAP_URL}   ${capwap_url}
    END
    ${CONFIG_RESULT}=   Configure Device to Connect to Cloud    ${aerohive_sw1.cli_type}    ${aerohive_sw1.ip}  ${aerohive_sw1.port}  ${aerohive_sw1.username}  ${aerohive_sw1.password}  ${CAPWAP_URL}
    Should Be Equal as Integers         ${CONFIG_RESULT}        1


TCCS-7748_Step3: Check Aerohive Switch Status On UI
    [Documentation]     Checks for switch status

    [Tags]              production          tccs_7748   tccs_7748_step3
    ${ONLINE_STATUS}=   Wait Until Device Online    device_serial=${aerohive_sw1.serial}
    Should Be Equal as Integers         ${ONLINE_STATUS}        1
    ${SW_STATUS}=       Get Device Status           device_serial=${aerohive_sw1.serial}
    Should Be Equal as Strings          ${SW_STATUS}            green

    ${DELETE_STATUS}=   Delete Device   ${aerohive_sw1.serial}
    Should Be Equal as Integers         ${DELETE_STATUS}        1


TCCS-7748_Step4: Onboard Aerohive Switch via advanced Onboarding
    [Documentation]         Checks for Aerohive switch(SR23XX) onboarding via advanced onboard

    [Tags]                  production  tccs_7748   tccs_7748_step4
    ${ONBOARD_RESULT}=      Advance Onboard Device              ${aerohive_sw1.serial}  device_make=${aerohive_sw1.cli_type}    dev_location=${LOCATION}
    Should Be Equal as Integers         ${ONBOARD_RESULT}       1
    ${SEARCH_RESULT}=       Search Device                       ${aerohive_sw1.serial}
    Should Be Equal as Integers         ${SEARCH_RESULT}        1
    ${ONLINE_STATUS}=       Wait Until Device Online            device_serial=${aerohive_sw1.serial}
    Should Be Equal as Integers         ${ONLINE_STATUS}        1
    ${SW_STATUS}=           Get Device Status                   device_serial=${aerohive_sw1.serial}
    Should Be Equal As Strings          ${SW_STATUS}            green

    ${DELETE_STATUS}=   Delete Device   ${aerohive_sw1.serial}
    Should Be Equal as Integers         ${DELETE_STATUS}        1
