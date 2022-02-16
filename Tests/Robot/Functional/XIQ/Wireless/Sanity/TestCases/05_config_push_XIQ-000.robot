# Author        : Rameswar
# Date          : March 30th 2020
# Description   :
#
# Topology      :
# Host ----- Cloud

*** Variables ***
${CONFIG_PUSH_SSID_01}              SSID_01
${CONFIG_PUSH_SSID_02}              SSID_02

*** Settings ***
Library     Collections
Library     common/Utils.py
Library     common/Cli.py
Library     common/Mu.py
Library     common/TestFlow.py
Library     common/ImageHandler.py
Library     common/ImageAnalysis.py

Library     xiq/flows/common/Login.py
Library     xiq/flows/manage/Client.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/configure/ExpressNetworkPolicies.py
Library     xiq/flows/configure/CommonObjects.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}

Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml
Resource     router_xr_sanity_config.robot
Resource     wireless_networks_config.robot

Force Tags   flow1   flow4   flow5
*** Keywords ***

*** Test Cases ***
Test1: Verification of config push complete config update
    [Documentation]             Add Policy
    [Tags]                      sanity                  policy          P1      production      test1

    ${POLICY_01}=               Get Random String
    ${SSID_01}=                 Get Random String

    Set Suite Variable          ${POLICY_01}
    Set Suite Variable          ${SSID_01}
    Set To Dictionary           ${CONFIG_PUSH_OPEN_NW_01}    ssid_name=${SSID_01}
    Log to Console              ${CONFIG_PUSH_OPEN_NW_01}

    ${result}=                  Login User              ${tenant_username}      ${tenant_password}
    ${POLICY_STATUS}=           Create Network Policy   policy=config_push_${POLICY_01}      &{CONFIG_PUSH_OPEN_NW_01}
    ${DEPLOY_STATUS}=           Deploy Network Policy with Complete Update      config_push_${POLICY_01}          ${ap1.serial}

    Wait Until Device Online    ${ap1.serial}  None   30   20

    ${SPAWN}=               Open Spawn      ${ap1.console_ip}   ${ap1.console_port}      ${ap1.username}       ${ap1.password}        ${ap1.platform}
    ${OUTPUT1}=             Send            ${SPAWN}                show ssid

    should be equal as integers             ${POLICY_STATUS}            1
    should be equal as integers             ${DEPLOY_STATUS}            1
    Should Contain                          ${OUTPUT1}                  ${SSID_01}

    [Teardown]    Run Keywords    Close Spawn      ${SPAWN}
    ...           AND    Logout User
    ...           AND    Quit Browser

Test2: Verification of config push delta update
    [Documentation]         Add Policy
    [Tags]                  sanity              test2       policy      P1      production
    Depends On              Test1
    ${result}=              Login User      ${tenant_username}          ${tenant_password}
    ${NEW_SSID_NAME_1}=     Get Random String

    ${EDIT_STATUS}=         Edit Network Policy SSID                    config_push_${POLICY_01}          ${SSID_01}     ${NEW_SSID_NAME_1}
    ${DEPLOY_STATUS}=       Deploy Network Policy with Delta Update     config_push_${POLICY_01}          ${ap1.serial}
    Wait Until Device Online    ${ap1.serial}

    ${SPAWN}=               Open Spawn      ${ap1.console_ip}   ${ap1.console_port}      ${ap1.username}       ${ap1.password}        ${ap1.platform}
    ${OUTPUT1}=             Send            ${SPAWN}                show ssid

    should be equal as integers             ${EDIT_STATUS}              1
    should be equal as integers             ${DEPLOY_STATUS}            1
    Should Contain                          ${OUTPUT1}                  ${NEW_SSID_NAME_1}

    [Teardown]    Run Keywords    Close Spawn      ${SPAWN}
    ...           AND    Logout User
    ...           AND    Quit Browser

Tes3: Verification of the functionality "Upgrade on the next reboot"
    [Tags]			        sanity              next-reboot             update      P1      test3
    ${POLICY_05}=               Get Random String
    ${SSID_05}=                 Get Random String

    Set To Dictionary           ${CONFIG_PUSH_OPEN_NW_01}    ssid_name=${SSID_05}
    Log to Console              ${CONFIG_PUSH_OPEN_NW_01}

    ${result}=              Login User      ${tenant_username}          ${tenant_password}

    ${POLICY_STATUS}=       Create Network Policy                       policy=test5_${POLICY_05}   &{CONFIG_PUSH_OPEN_NW_01}
    ${DEPLOY_STATUS}=       Deploy Network Policy with Next Reboot      test5_${POLICY_05}          ${ap1.serial}

    should be equal as integers             ${DEPLOY_STATUS}            1

    Wait Until Device Online                ${ap1.serial}

    ${SPAWN}=               Open Spawn      ${ap1.console_ip}   ${ap1.console_port}      ${ap1.username}       ${ap1.password}        ${ap1.platform}
    ${SSID_OUTPUT1}=        Send            ${SPAWN}     show ssid
    Should Not Contain      ${SSID_OUTPUT1}      ${SSID_05}
    Close Spawn             ${SPAWN}

    Reboot Device           ${ap1.serial}
    Sleep                   30

    Wait Until Device Reboots        ${ap1.serial}
    Sleep                   ${ap_reboot_wait}
    ${SPAWN}=               Open Spawn      ${ap1.console_ip}   ${ap1.console_port}      ${ap1.username}       ${ap1.password}        ${ap1.platform}
    ${SSID_OUTPUT2}=        Send            ${SPAWN1}    show ssid
    Should Contain          ${SSID_OUTPUT2}      ${SSID_05}

    [Teardown]    Run Keywords    Close Spawn     ${SPAWN1}
    ...           AND    Logout User
    ...           AND    Quit Browser

Tes4: Update at specific time functionality
    [Tags]			        sanity              time-specific           update      P1      test4
    ${POLICY_06}=           Get Random String
    ${SSID_06}=             Get Random String

    Set To Dictionary       ${CONFIG_PUSH_OPEN_NW_01}    ssid_name=${SSID_06}
    Log                     ${CONFIG_PUSH_OPEN_NW_01}

    ${SPAWN}=               Open Spawn      ${ap1.console_ip}   ${ap1.console_port}      ${ap1.username}       ${ap1.password}        ${ap1.platform}
    ${REBOOT_OUPUT1}=       Send            ${SPAWN}     show reboot schedule
    Should Not Contain      ${REBOOT_OUPUT1}        Next reboot Scheduled

    ${CLOCK_OUPUT1}=        Send            ${SPAWN}     show clock
    ${SSID_OUPUT1}=         Send            ${SPAWN}     show ssid

    ${LOGIN_STATUS}=        Login User      ${tenant_username}      ${tenant_password}
    ${POLICY_STATUS}=       Create Network Policy       test6_${POLICY_06}      &{CONFIG_PUSH_OPEN_NW_01}

    ${CLOCK_OUPUT2}=        Send            ${SPAWN}     show clock
    ${REBOOT_OUPUT2}=       Send            ${SPAWN}     show reboot schedule
    ${SSID_OUPUT2}=         Send            ${SPAWN}     show ssid

    ${DUT_TIME}=            Get Device Time     ${CLOCK_OUPUT2}
    ${DUT_DATE}=            Get Device Date     ${CLOCK_OUPUT2}

    ${DEPLOY_TIME}=         Deploy Network Policy at Specific Time      test6_${POLICY_06}          ${ap1.serial}          ${DUT_DATE}     ${DUT_TIME}
    Sleep                   ${config_push_wait}

    ${CLOCK_OUPUT3}=        Send            ${SPAWN}     show clock
    ${REBOOT_OUPUT3}=       Send            ${SPAWN}     show reboot schedule
    ${SSID_OUPUT3}=         Send            ${SPAWN}     show ssid

    Close Spawn             ${SPAWN}

    Log to Console          Sleep for 15m. Specific time upgrade interval is 15 mins
    Sleep                   15m

    ${SPAWN2}=              Open Spawn      ${ap1.console_ip}   ${ap1.console_port}      ${ap1.username}       ${ap1.password}        ${ap1.platform}
    ${CLOCK_OUPUT4}=        Send            ${SPAWN2}     show clock
    ${REBOOT_OUPUT4}=       Send            ${SPAWN2}     show reboot schedule
    ${SSID_OUPUT4}=         Send            ${SPAWN2}     show ssid

    Should Not Contain      ${SSID_OUPUT3}      ${SSID_06}
    Should Contain          ${REBOOT_OUPUT3}    Next reboot Scheduled
    Should Contain          ${REBOOT_OUPUT3}    ${DEPLOY_TIME}
    Should Contain          ${SSID_OUPUT4}      ${SSID_06}

    [Teardown]    Run Keywords    Close Spawn             ${SPAWN2}
    ...           AND    Logout User
    ...           AND    Quit Browser


Test5: IQ engine upgrade to specific version
    [Tags]			        sanity              upgrade                 specific-version      P1        test5

    ${SPAWN}=               Open Spawn      ${ap1.console_ip}   ${ap1.console_port}      ${ap1.username}       ${ap1.password}        ${ap1.platform}
    ${CLOCK_OUPUT1}=        Send            ${SPAWN}     show clock
    ${REBOOT_OUPUT1}=       Send            ${SPAWN}     show reboot schedule
    ${VERSION_DETAIL1}=     Send            ${SPAWN}     show version detail
    ${AP_BUILD_VERSION1}=   Get AP Version          ${SPAWN}

    Should Not Contain      ${REBOOT_OUPUT1}     Next reboot Scheduled
    Should Contain          ${VERSION_DETAIL1}   Running image:      Current version
    Should Contain          ${VERSION_DETAIL1}   Backup version:     HiveOS 10.0r3
    Should Contain          ${VERSION_DETAIL1}   Load after reboot:  Current version

    ${LOGIN_STATUS}=        Login User      ${tenant_username}      ${tenant_password}
    ${SPECIFIC_VERSION}=    Upgrade Device To Specific Version            ${ap1.serial}

    ${VERSION_DETAIL3}=     Send            ${SPAWN}         show version detail
    Sleep                   30                          Sleep 30 Seconds
    ${VERSION_DETAIL3}=     Send            ${SPAWN}         show version detail

    Wait Until Device Reboots               ${ap1.serial}
    Close Spawn             ${SPAWN}

    ${SPAWN2}=              Open Spawn      ${ap1.console_ip}   ${ap1.console_port}      ${ap1.username}       ${ap1.password}        ${ap1.platform}
    ${CLOCK_OUPUT2}=        Send            ${SPAWN2}         show clock
    ${REBOOT_OUPUT2}=       Send            ${SPAWN2}         show reboot schedule
    ${VERSION_DETAIL2}=     Send            ${SPAWN2}         show version detail
    ${AP_BUILD_VERSION2}=   Get AP Version          ${SPAWN2}

    Should Not Contain      ${REBOOT_OUPUT2}     Next reboot Scheduled
    Should Contain          ${VERSION_DETAIL2}   Running image:      Current version
    Should Contain          ${VERSION_DETAIL2}   Backup version:     HiveOS 10.0r3
    Should Contain          ${VERSION_DETAIL2}   Load after reboot:  Current version
    Should Contain          ${VERSION_DETAIL2}   Uptime:             0 weeks, 0 days, 0 hours

    Should Be Equal As Strings  ${SPECIFIC_VERSION}           ${AP_BUILD_VERSION2}

    [Teardown]    Run Keywords    Close Spawn             ${SPAWN2}
    ...           AND    Logout User
    ...           AND    Quit Browser



Tes6: IQ engine upgrade to lastest version
    [Tags]			        sanity              upgrade                 latest-version      P1      test6  production

    ${SPAWN1}=              Open Spawn      ${ap1.console_ip}   ${ap1.console_port}      ${ap1.username}       ${ap1.password}        ${ap1.platform}
    ${CLOCK_OUPUT1}=        Send            ${SPAWN1}         show clock
    ${REBOOT_OUPUT1}=       Send            ${SPAWN1}         show reboot schedule
    ${VERSION_DETAIL1}=     Send            ${SPAWN1}         show version detail
    ${AP_BUILD_VERSION1}=   Get AP Version              ${SPAWN1}

    Should Not Contain      ${REBOOT_OUPUT1}     Next reboot Scheduled
    Should Contain          ${VERSION_DETAIL1}   Running image:      Current version
    Should Contain          ${VERSION_DETAIL1}   Backup version:     HiveOS 10.0r3
    Should Contain          ${VERSION_DETAIL1}   Load after reboot:  Current version

    ${LOGIN_STATUS}=        Login User      ${tenant_username}      ${tenant_password}
    ${LATEST_VERSION}=      Upgrade Device To Latest Version            ${ap1.serial}
    Sleep                   30                          Sleep 30 Seconds

    Wait Until Device Reboots               ${ap1.serial}
    Close Spawn             ${SPAWN1}

    ${SPAWN2}=              Open Spawn      ${ap1.console_ip}   ${ap1.console_port}      ${ap1.username}       ${ap1.password}        ${ap1.platform}
    ${CLOCK_OUPUT2}=        Send            ${SPAWN2}         show clock
    ${REBOOT_OUPUT2}=       Send            ${SPAWN2}         show reboot schedule
    ${VERSION_DETAIL2}=     Send            ${SPAWN2}         show version detail
    ${AP_BUILD_VERSION2}=   Get AP Version              ${SPAWN2}

    Should Not Contain      ${REBOOT_OUPUT2}     Next reboot Scheduled
    Should Contain          ${VERSION_DETAIL2}   Running image:      Current version
    Should Contain          ${VERSION_DETAIL2}   Backup version:     HiveOS 10.0r3
    Should Contain          ${VERSION_DETAIL2}   Load after reboot:  Current version
    Should Contain          ${VERSION_DETAIL2}   Uptime:             0 weeks, 0 days, 0 hours

    Should Be Equal As Strings  ${LATEST_VERSION}           ${AP_BUILD_VERSION2}

    [Teardown]    Run Keywords    Close Spawn    ${SPAWN2}
    ...           AND   Quit Browser

Tes7: Cleanup
    [Tags]			        cleanup         test7
    ${LOGIN_STATUS}=        Login User          ${tenant_username}      ${tenant_password}
    Delete Device           device_serial=${ap1.serial}
    [Teardown]    Quit Browser