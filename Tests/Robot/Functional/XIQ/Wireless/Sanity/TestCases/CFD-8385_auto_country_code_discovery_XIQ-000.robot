#########################################################################################################
# Author        : Binh Nguyen
# Date          : April 20th 2023
# Description   : TCCS-15117 - CFD-8385: Auto Country Code Discovery Failure
#########################################################################################################

*** Settings ***
Library     String
Library     Collections
Library     DependencyLibrary

Library     common/Cli.py
Library     common/Utils.py

# The keywords in Login.py have been moved to the keywords directory.
# If the moved keyword is not working correctly import the original library and remove the keywords/gui/login/KeywordsLogin.py version.
#Library     xiq/flows/common/Login.py
Library     keywords/gui/login/KeywordsLogin.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/DevicesActions.py
Library     xiq/flows/manage/DeviceConfig.py
Library     xiq/flows/manage/DeviceCliAccess.py

Library     xiq/flows/globalsettings/GlobalSetting.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml

Force Tags       testbed_none
Suite Setup      Pre_condition
Suite Teardown   Post_condition

*** Test Cases ***
Step1: Configure and Verify country code as default 998
    [Documentation]     Configure and Verify country code as default 998
    [Tags]              tccs-15117   development   step1   steps

    ${SPAWN}     Open Spawn    ${ap1.ip}   ${ap1.port}   ${ap1.username}   ${ap1.password}   ${ap1.cli_type}
    ${OUTPUT}    Send          ${SPAWN}    mfg-set-region-code #G6L@*Sv^&<W>Cp/ 1 998
    ${OUTPUT}    Send          ${SPAWN}    show boot-param | inc country
    should contain   ${OUTPUT}   998
    [Teardown]   Close Spawn   ${SPAWN}

Step2: Make capwap disconnection and reconnection
    [Documentation]     Make capwap disconnection and reconnection
    [Tags]              tccs-15117   development   step2   steps

    Depends On Test     Step1: Configure and Verify country code as default 998
    ${SPAWN}     Open Spawn      ${ap1.ip}   ${ap1.port}   ${ap1.username}   ${ap1.password}   ${ap1.cli_type}
    ${OUTPUT}    Send            ${SPAWN}    no capwap client enable
    ${OUTPUT}    Send            ${SPAWN}    capwap client enable
    ${STATUS}                    Wait for Configure Device to Connect to Cloud   ${ap1.cli_type}   ${capwap_url}     ${SPAWN}
    Should Be Equal As Strings   '${STATUS}'                            '1'
    Close Spawn                  ${SPAWN}

Step3: Wait for country code discover
    [Documentation]     Wait for country code discover
    [Tags]              tccs-15117   development   step3   steps

    Depends On Test     Step2: Make capwap disconnection and reconnection
    ${OUTPUT}    Wait Until Country Discovered   ${ap1.serial}

Step4: Verfiy the expected country code in the output 840
    [Documentation]     Verfiy the expected country code in the output 840
    [Tags]              tccs-15117   development   step4   steps

    Depends On Test     Step3: Wait for country code discover
    ${SPAWN}     Open Spawn     ${ap1.ip}   ${ap1.port}   ${ap1.username}   ${ap1.password}   ${ap1.cli_type}
    FOR   ${i}    IN RANGE    20
        ${OUTPUT}    Send   ${SPAWN}   show boot-param | inc country
        ${STATUS}    Run Keyword And Return Status    should contain   ${OUTPUT}   840
        exit for loop if   '${STATUS}'=='True'
        sleep        15s
    END
    [Teardown]   Close Spawn   ${SPAWN}

*** Keywords ***
Pre_condition
    ${STATUS}                     Login User    ${tenant_username}   ${tenant_password}
    should be equal as strings    '${STATUS}'   '1'
    reset devices to default
    log to console                Wait for 2 minutes for completing reboot....
    sleep                         2m
    delete all devices
    Onboard_AP

Post_condition
    Logout User
    Quit Browser

Onboard_AP
    ${STATUS}       onboard device quick                            ${ap1}
    Should Be Equal As Strings                                      '${STATUS}'       '1'
    ${AP_SPAWN}     Open Spawn                                      ${ap1.ip}         ${ap1.port}      ${ap1.username}   ${ap1.password}   ${ap1.cli_type}
    ${STATUS}       Configure Device To Connect To Cloud            ${ap1.cli_type}   ${capwap_url}    ${AP_SPAWN}
    Should Be Equal As Strings                                      '${STATUS}'       '1'

    ${STATUS}       Wait for Configure Device to Connect to Cloud   ${ap1.cli_type}   ${capwap_url}    ${AP_SPAWN}
    Should Be Equal As Strings                                      '${STATUS}'       '1'
    Wait_device_online                                              ${ap1}
    [Teardown]      Close Spawn                                     ${AP_SPAWN}

Wait_device_online
    [Arguments]    ${ap}
    ${STATUS}                       Wait Until Device Online    ${ap}[serial]
    Should Be Equal As Strings      '${STATUS}'    '1'
    ${STATUS}                       Get Device Status           ${ap}[serial]
    ${STATUS}                       Run Keyword And Return Status    Should contain any    ${STATUS}    green    config audit mismatch
    IF    not ${STATUS}
        Wait Until Device Reboots       ${ap}[serial]
        ${STATUS}                       Wait Until Device Online    ${ap}[serial]    retry_count=60
        Should Be Equal As Strings      '${STATUS}'    '1'
        ${STATUS}                       Get Device Status           ${ap}[serial]
        Should contain any              ${STATUS}      green        config audit mismatch
    END
