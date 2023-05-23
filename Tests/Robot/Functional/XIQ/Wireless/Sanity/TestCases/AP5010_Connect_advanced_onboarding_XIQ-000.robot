# Author        : Pranav Chauhan
# Date          : April 2022
# Description   : AP5010 onboarding support at CONNECT level account

# Pre-Condtion


*** Settings ***

Library     extauto/common/Cli.py
Library     extauto/common/TestFlow.py
# The keywords in Login.py have been moved to the keywords directory.
# If the moved keyword is not working correctly import the original library and remove the keywords/gui/login/KeywordsLogin.py version.
#Library     extauto/xiq/flows/common/Login.py
Library     keywords/gui/login/KeywordsLogin.py
Library     extauto/xiq/flows/manage/AdvanceOnboarding.py
Library     extauto/xiq/flows/manage/AdvOnboard.py
Library     extauto/xiq/flows/common/Navigator.py
Library     extauto/xiq/flows/manage/Client.py
Library     extauto/xiq/flows/manage/Devices.py
Library     extauto/xiq/flows/manage/DeviceCliAccess.py
Library     extauto/xiq/flows/globalsettings/GlobalSetting.py
Library     extauto/xiq/flows/configure/NetworkPolicy.py
Library     extauto/xiq/flows/configure/CommonObjects.py
Library     ExtremeAutomation/Imports/CommonObjectUtils.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/device_commands.yaml

Force Tags   testbed_none

*** Variables ***

${DEVICE_MAKE_AEROHIVE}      Extreme - Aerohive
${DEVICE_TYPE}          Real
${ENTRY_TYPE}           Manual
${LOCATION}                 auto_location_01, Santa Clara, building_02, floor_04

*** Test Cases ***

TCXM-19754 - XIQ-4593 - Advanced onboard: Onboard AP5010/AP5010U cloud managed - step1
    [Documentation]         Checks for AP advanced onboarding is success
    [Tags]                  tcxm_19754    development     ap5010      step1     tcxm-19754    advanced
        # Use this method to convert the ap, wing, netelem to a generic device object
    # ap1       => device1
    # wing1     => device1
    # netelem1  => device1 (EXOS / VOSS)
    convert to generic device object   device  index=1

    ${result}=              Login User          ${tenant_username}      ${tenant_password}
    Delete device               device_serial=${device1.serial}
    Change Device Password                      Aerohive123
    ${ONBOARD_STATUS}=               Advance Onboard Device         ${device1.serial}    device_make=${DEVICE_MAKE_AEROHIVE}   dev_location=${LOCATION}
    should be equal as integers      ${ONBOARD_STATUS}       1

    [Teardown]   run keywords               logout user
    ...                                     quit browser


TCXM-19754 - XIQ-4593 - Advanced onboard: Onboard AP5010/AP5010U cloud managed - step2
    [Documentation]     Configure Capwap client server
    [Tags]              tcxm_19754    development     ap5010      step2      tcxm-19754   advanced
    Depends On          step1
    ${AP_SPAWN}=        Open Spawn          ${device1.ip}   ${device1.port}      ${device1.username}       ${device1.password}        ${device1.cli_type}
    ${OUTPUT0}=         Send Commands       ${AP_SPAWN}         capwap client server name ${capwap_url}, capwap client default-server-name ${capwap_url}, capwap client server backup name ${capwap_url}, no capwap client enable, capwap client enable, save config

    ${OUTPUT0}=         Send                ${AP_SPAWN}         console page 0
    ${OUTPUT0}=         Send                ${AP_SPAWN}         show version detail
    ${OUTPUT0}=         Send                ${AP_SPAWN}         show capwap client
    ${OUTPUT2}=         Send                ${AP_SPAWN}         ${cmd_capwap_hm_primary_name}
    ${OUTPUT3}=         Send                ${AP_SPAWN}         ${cmd_capwap_server_ip}
    ${OUTPUT1}=         Wait For CLI Output                     ${AP_SPAWN}         ${cmd_capwap_client_state}          ${output_capwap_status}

    Should Be Equal as Integers             ${OUTPUT1}          1

    [Teardown]    Close Spawn    ${AP_SPAWN}


TCXM-19754 - XIQ-4593 - Advanced onboard: Onboard AP5010/AP5010U cloud managed - step3
    [Documentation]     Checks for ap status
    [Tags]              tcxm_19754    development     ap5010      step3     tcxm-19754    advanced
    Depends On          step2
    ${result}=          Login User          ${tenant_username}     ${tenant_password}
    Wait Until Device Online                ${device1.serial}
    ${AP_STATUS}=       get device status       device_mac=${device1.mac}
    Should Be Equal As Strings  '${AP_STATUS}'     'green'

    [Teardown]   run keywords               logout user
    ...                                     quit browser