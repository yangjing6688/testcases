# Author        : Ramkumar
# Date          : Nov17,2020
# Description   : ADSP Integration on XIQ testacses
#
# Topology      :
# AP1(AP460C or AP410C)----- Cloud-----AP2(Any AP)-----Windows10 Client---Kali Laptop

# Pre-Condtion
# 1. Should Upgrade AP with Q3R3 – 10.2r2 or Q3R5 -10.2r3
# 2. AP2 Should Present Near to Kali Laptop

# Execution Command:
# ------------------
#  robot -L INFO -v TEST_URL:https://extremecloudiq.com/ TESTBED:blr_tb_2 -v DEVICE1:AP410C DEVICE2:AP630 -v TOPO:production adsp_integration.robot

*** Variables ***
${WIPS_POLICY_NAME}         test_automation_adsp
${NW_POLICY_NAME}           test_automation_adsp
${SSID_NAME}                test_automation_adsp
${LOCATION}                 auto_location_01, San Jose, building_01, floor_01
${LOCATION_DISPLAY}         auto_location_01 >> San Jose >> building_01 >> floor_01
${BUILDING_NAME}            building_01
${NW_POLICY_NAME2}          alarm_generation_policy
${SSID_NAME2}               alarm_generation_ssid
${EXPECTED_ALARM}           Soft AP

${MAP_FILE_NAME}            auto_location_01_1595321828282.tar.gz

*** Settings ***

Force Tags   testbed_adsp

Library     Collections
Library     String
Library     common/Utils.py
Library     common/Cli.py
Library     common/TestFlow.py
Library     common/WebElementHandler.py
Library     xiq/flows/common/Login.py
Library     xiq/flows/common/Navigator.py
Library     xiq/flows/AirDefence/AirDefenceAlarms.py
Library     xiq/flows/manage/Client.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/Location.py
Library     xiq/flows/configure/Wips.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/configure/CommonObjects.py
Library     xiq/flows/configure/DeviceTemplate.py
Library     xiq/flows/mlinsights/Network360Plan.py
Library     xiq/flows/globalsettings/GlobalSetting.py
Library     ExtremeAutomation/Imports/CommonObjectUtils.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml

Resource    Tests/Robot/Functional/XIQ/Wireless/Sanity/Resources/adsp_integration_config.robot


Suite Setup      Pre Condition
Suite Teardown   Test Suite Clean Up

*** Keywords ***
Pre Condition
    [Documentation]   AP Should be onboarded  and it is online

    # Use this method to convert the ap, wing, netelem to a generic device object
    # device1       => device1
    # wing1     => device1
    # netelem1  => device1 (EXOS / VOSS)
    convert to generic device object            device  index=1

    ${result}=                      Login User          ${tenant_username}     ${tenant_password}    map_override=${MAP_FILE_NAME}

    Logout User
    Quit Browser

Test Suite Clean Up
    [Documentation]         Test Suite Clean Up: Reset Customer Account Data
    [Tags]                  sanity  aerohive  P1   production   regression
    ${LOGIN_XIQ}=                   Login User          ${tenant_username}     ${tenant_password}
    ${RESET_VIQ_DATA}=               Reset VIQ Data
    Should Be Equal As Strings      '${RESET_VIQ_DATA}'              '1'
    sleep  60s
    [Teardown]                      Quit Browser

*** Test Cases ***

Test1: Onboard Sensor AP
    [Documentation]         Onboard Sensor AP
    [Tags]                  tccs_12494      adsp        development
    ${LOGIN_XIQ}=               Login User          ${tenant_username}     ${tenant_password}

    ${ONBOARD_RESULT}=          onboard device quick     ${device1}
    should be equal as integers       ${ONBOARD_RESULT}       1

    ${AP_SPAWN}=                open spawn       ${device1.ip}      ${device1.port}   ${device1.username}     ${device1.password}        ${device1.cli_type}

    Set Suite Variable          ${AP_SPAWN}

    ${OUTPUT0}=                 send Commands  ${AP_SPAWN}   capwap client server name ${capwap_url}, capwap client default-server-name ${capwap_url}, capwap client server backup name ${capwap_url}, no capwap client enable, capwap client enable, save config
    sleep  240s
    Wait Until Device Online    ${device1.serial}

    ${AP1_STATUS}=              get device status       device_mac=${device1.mac}

    Should Be Equal As Strings  '${AP1_STATUS}'     'green'

    [Teardown]         run keywords    logout user
     ...                               quit browser

Test2: Onboard AP to Generate DoS Deauthentication
    [Documentation]         Pre-config-Onboard AP to Generate DoS Deauthentication
    [Tags]                  tccs_12495      adsp        development
    Depends On              Test1
    ${LOGIN_XIQ}=               Login User          ${tenant_username}     ${tenant_password}


    ${ONBOARD_RESULT}=          onboard device quick     ${ap2}
    should be equal as integers        ${ONBOARD_RESULT}       1
     ${AP2_SPAWN}=               open spawn       ${ap2.ip}      ${ap2.port}   ${ap2.username}     ${ap2.password}        ${ap2.cli_type}
     
    Set Suite Variable          ${AP2_SPAWN}
    ${OUTPUT0}=                 send commands      ${AP2_SPAWN}         capwap client server name ${capwap_url}, capwap client default-server-name ${capwap_url}, capwap client server backup name ${capwap_url}, no capwap client enable, capwap client enable, save config
    sleep  240s
    Wait Until Device Online    ${ap2.serial}

    ${AP2_STATUS}=               get device status      device_mac=${ap2.mac}
    Should Be Equal As Strings  '${AP2_STATUS}'     'green'

    [Teardown]         run keywords    logout user
     ...                               quit browser

Test3: Connect Client to Generate DoS Deauthentication
    [Documentation]         Pre-config-Connect Client to Generate DoS Deauthentication
    [Tags]                  tccs_12496      adsp        development
    Depends On              Test1  Test2
    ${LOGIN_XIQ}=                   Login User          ${tenant_username}     ${tenant_password}

    ${CREATE_POLICY1}=              Create Network Policy   ${NW_POLICY_NAME2}      ${OPEN_NW_02}
    Should Be Equal As Strings      '${CREATE_POLICY1}'   '1'

    ${AP2_UPDATE_CONFIG}=           Deploy Network Policy with Complete Update      ${NW_POLICY_NAME2}          ${ap2.serial}
    Should Be Equal As Strings      '${AP2_UPDATE_CONFIG}'       '1'

    ${DEVICE_STATUS}=             Wait Until Device Online       ${ap2.serial}
    Should Be Equal As Strings      '${DEVICE_STATUS}'     '1'

    Log to Console      Sleep for ${config_push_wait}
    sleep                         ${config_push_wait}

    [Teardown]         run keywords    logout user
     ...                               quit browser

Test4: Configure ADSP on AP
    [Documentation]         Configure ADSP on AP
    [Tags]                  tccs_12497      adsp        development
    Depends On              Test1
    ${LOGIN_XIQ}=              Login User          ${tenant_username}      ${tenant_password}

    ${CREATE_POLICY1}=         Create Network Policy   ${NW_POLICY_NAME}       ${ADSP_OPEN_NW}
    Should Be Equal As Strings   '${CREATE_POLICY1}'   '1'

    ${CREATE_AP_TEMPLATE}=     Add AP Template     ${device1.model}     AP410C-ADSP_Prod       ${AP_TEMPLATE_CONFIG}
    Should Be Equal As Strings   '${CREATE_AP_TEMPLATE}'   '1'

    ${CONFIG_WIPS_POLICY}      Configure WIPS Policy On Common Objects   ${WIPS_POLICY_NAME}
    Should Be Equal As Strings   '${CONFIG_WIPS_POLICY}'   '1'

    ${NP_REUSE_WIPS}           Configure Reuse Wips Policy On Network Policy  ${NW_POLICY_NAME}  ${WIPS_POLICY_NAME}
    Should Be Equal As Strings   '${NP_REUSE_WIPS}'   '1'

    ${AP1_UPDATE_CONFIG}=           Deploy Network Policy with Complete Update      ${NW_POLICY_NAME}          ${device1.serial}
    Should Be Equal As Strings      '${AP1_UPDATE_CONFIG}'       '1'

    ${DEVICE_STATUS}=             Wait Until Device Online       ${ap2.serial}
    Should Be Equal As Strings      '${DEVICE_STATUS}'     '1'

    ${AP_SPAWN}=               open spawn       ${device1.ip}      ${device1.port}   ${device1.username}     ${device1.password}        ${device1.cli_type}
    ${SENSOR_WIFI_CONFIG}=     send commands                ${AP_SPAWN}         show running-config | include "interface wifi2"
    Should Contain             ${SENSOR_WIFI_CONFIG}      interface wifi2 mode adsp-sensor

    ${SUBSCRIBE_ESSENTIALS} =  subscribe adess essentials
    Should Be Equal As Strings      '${SUBSCRIBE_ESSENTIALS}'   '1'

    close spawn   ${AP_SPAWN}

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

Test5: Generate DoS Deauthentication Alarm on Kali Linux
    [Documentation]         Generate DoS Deauthentication Alarm on Kali Linux
    [Tags]                  tccs_12498      adsp        development

    Depends On               Test3   Test4

    FOR    ${i}    IN RANGE  2
          ${KALI_SPAWN}=               open spawn        ${Kali_server1.ip}   ${Kali_server1.port}    ${Kali_server1.username}       ${Kali_server1.password}   ${Kali_server1.platform}
          ${DOS_ALARM_CMD}=            send commands               ${KALI_SPAWN}        cd auto && python autotest-2x.py -r 10 -c 165 -a 21, yes
          Should Contain               ${DOS_ALARM_CMD}   Running SoftAP
          close spawn   ${KALI_SPAWN}
    END
    Log to Console      Sleep for 3 Minutes to Validate Alarm Active Time
    Sleep               180s

Test6: Validate Alarm Grid Information
    [Documentation]         Test3: Validate Alarm Grid Information
    [Tags]                  tccs_12499      adsp        development
    Depends On              Test4   Test5
    ${LOGIN_XIQ}=                   Login User                ${tenant_username}      ${tenant_password}

    ${ALARM_DETAILS_ON_GRID}=       Get ADSP Alarm Details    ${EXPECTED_ALARM}

    ${SENSOR_MAC}=                  Get From Dictionary       ${ALARM_DETAILS_ON_GRID}    sensorMac
    Should Be Equal As Strings      '${SENSOR_MAC}'          '${device1.mac}'

    ${SITE_ID}=                     Get From Dictionary       ${ALARM_DETAILS_ON_GRID}    siteId
    Should Be Equal As Strings      '${SITE_ID}'              '${BUILDING_NAME}'

    [Teardown]                      Quit Browser

Test7: Change Wireless Thread Detection Status
    [Documentation]         Change Wireless Thread Detection Status
    [Tags]                  tccs_12500      adsp        development
    Depends On              Test4
    ${LOGIN_XIQ}=                 Login User          ${tenant_username}      ${tenant_password}
    ${CHANGE_WTD_STATUS}=         Change Wireless Thread Detection Status   ${WIPS_POLICY_NAME}    OFF
    Should Be Equal As Strings   '${CHANGE_WTD_STATUS}'   '1'

    [Teardown]                      Quit Browser

Test8: Verify Alarms Overview Widget Count
    [Documentation]         Verify Alarms Overview Widget Count
    [Tags]                  tccs_12501      adsp        development
    Depends On              Test4
    ${LOGIN_XIQ}=                 Login User          ${tenant_username}      ${tenant_password}

    ${AP1_UPDATE_CONFIG}=         update device delta configuration     ${device1.serial}   update_method=Delta
    Should Be Equal As Strings   '${AP1_UPDATE_CONFIG}'       '1'

    Sleep                         ${config_push_wait}

    ${ALARM_COUNT_ON_GRID}=       Get Total ADSP Alarm Count

    ${ALARM_OVERVIEW_COUNT}=      Check ADSP Alarms Overview Widget Count
    Should Be Equal As Strings   '${ALARM_OVERVIEW_COUNT}'  '${ALARM_COUNT_ON_GRID}'

    [Teardown]                      Quit Browser

Test9: Verify Alarms By Severity Widget Count
    [Documentation]         Verify Alarms By Severity Widget Count
    [Tags]                  tccs_12502      adsp        development
    Depends On              Test4
    ${LOGIN_XIQ}=                 Login User          ${tenant_username}      ${tenant_password}

    ${ALARM_COUNT_ON_GRID}=       Get Total ADSP Alarm Count

    ${ALARM_SEVERITYCOUNT}=       Check ADSP Alarm By Severity Count
    Should Be Equal As Strings   '${ALARM_SEVERITYCOUNT}'  '${ALARM_COUNT_ON_GRID}'

    [Teardown]                      Quit Browser

Test10: Verify Alarm InActive Time
    [Documentation]         Verify Alarm InActive Time
    [Tags]                  tccs_12503      adsp        development
    Depends On              Test4

    Log to Console      Sleep for 30 Minutes to Validate Alarm InActive Time
    Sleep               30m

    ${LOGIN_XIQ}=                   Login User          ${tenant_username}      ${tenant_password}

    ${ALARM_DETAILS_ON_GRID}=       Get ADSP Alarm Details    ${EXPECTED_ALARM}
    ${ALARM_STATE_GRID}=            Get From Dictionary       ${ALARM_DETAILS_ON_GRID}    alarmState
    ${ALARM_STATE_LIST}=            Split String              ${ALARM_STATE_GRID}         separator=notifications\n
    ${ALARM_STATE}=                 Set Variable              ${ALARM_STATE_LIST}[1]
    Should Be Equal As Strings      '${ALARM_STATE}'          'INACTIVE'

    [Teardown]                      Quit Browser

Test11: Verify backup viq
    [Documentation]     Check the viq backup
    [Tags]      tccs_13260    adsp      development
    
    ${result1}=         login user  ${tenant_username}      ${tenant_password}
    Should Be Equal As Strings      '${result1}'     '1'
    ${BKUP_VIQ}=           backup viq data
    Should Be Equal As Strings      '${BKUP_VIQ}'              '1'
    sleep   60s

    [Teardown]                      Quit Browser
