# Author        : Karthik Venkatesamoorthy
# Description   : Testcases related to network policy config push when ADESS and XLOC are subscribed.
# Topology      :
# AP1----- Cloud-----Ubuntu

# Pre-Condtion
#1. AP and Client should Present Inside RF Box Environment
#2. Client MAC should be configured in APXX.robot file in topology folder.
#3. Need one  Customer Account to run this Feature (ADESS + XLOC ==> Subscribed)

# Execution Command:
# ------------------
#robot -L INFO -v TEST_URL:https://extremecloudiq.com/ -v TESTBED:blr_tb_2 -v DEVICE1:AP460C  -v TOPO:production ad_reg_configpush_XIQ-000.robot

*** Variables ***
#Defaults
${ENV}                  environment.ad_rt_reg.remote.win10.chrome.yaml
${TOPO}                 topo.ad_rt_reg.g2r1.yaml
${TESTBED}              BANGALORE/Prod/wireless/ad_rt_reg.yaml

${BEACON_SERVICE_NAME}          location_coex_test
${LOCATION}                     auto_location_01, San Jose, building_01, floor_01
${MAP_FILE_NAME}                 auto_location_f01_1654845780826.tar.gz

${NW_POLICY_NAME}               adess_coex_nwp
${SSID_NAME}                    adess_coex_ssid
${WIPS_POLICY_NAME}             adess-coex-wips

${BUILDING_NAME}                building_01
${UUID}                     123e4567-e89b-12d3-a456-426655440000
${CLIENT_MAC_FORMAT}               54:8d:5a:69:3c:5a
*** Settings ***
Force Tags   testbed_adsp

Library     Collections
Library     String
Library     robot.libraries.DateTime
Library     common/Utils.py
Library     common/Cli.py
Library     common/TestFlow.py
Library     common/Screen.py
Library     xiq/flows/common/Login.py
Library     xiq/flows/common/Navigator.py
Library     xiq/flows/manage/Client.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/Location.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/configure/Wips.py
Library     xiq/flows/configure/DeviceTemplate.py
Library     xiq/flows/configure/CommonObjects.py
Library     xiq/flows/globalsettings/GlobalSetting.py
Library     xiq/flows/AirDefence/AirDefenceAlarms.py
Library     xiq/flows/extreme_location/ExtremeLocation.py
Library     xiq/flows/mlinsights/Network360Plan.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml
Variables    TestBeds/BANGALORE/Prod/wireless/ad_rt_reg.yaml
Resource    testsuites/xiq/config/waits.robot
Resource    Tests/Robot/Functional/XIQ/Wireless/Sanity/Resources/ad_rt_reg_config.robot

Suite Setup      Pre Condition
Suite Teardown   Test Suite Clean Up


*** Keywords ***
Pre Condition
    [Documentation]   All the existing configuration clean up
    ${result}=                      Login User          ${TENANT_USERNAME1}     ${TENANT_PASSWORD1}
    click advanced onboard popup
    import map in network360plan     ${MAP_FILE_NAME}
    Logout User
    Quit Browser
Test Suite Clean Up
    [Documentation]    Delete Devices / cleanup scripts
    ${result}=    Login User        ${tenant_username1}     ${tenant_password1}
    navigate to devices
    Delete Device                   device_serial=${ap2.serial}
    logout user
    quit browser

*** Test Cases ***
Test1: Verify Network policy with wireless and routing mode enabled
    [Documentation]         Network policy with wireless and routing mode enabled , Alarms state validation in AD Essentials- ADESS and XLOC coexistence.
    [Tags]                  tccs_13250        testbed_adsp        development
     Login User                      ${TENANT_USERNAME1}     ${TENANT_PASSWORD1}
     ${ADV_cONBOARD}=                click advanced onboard popup

    ${CREATE_POLICY1} =              Create Network Policy               ${NW_POLICY_NAME}        ${ADESS_NWP}
    Should Be Equal As Strings      '${CREATE_POLICY1}'   '1'

    ${CREATE_AP_TEMPLATE}=           Add AP Template     ${ap2.model}     ${ap2.template_name}    ${AP_TEMPLATE_CONFIG}
    Should Be Equal As Strings       '${CREATE_AP_TEMPLATE}'   '1'

    ${CONFIG_WIPS_POLICY}            Create Wips Policy Adess Status On Common Objects  ${WIPS_POLICY_NAME}    Enable
    Should Be Equal As Strings       '${CONFIG_WIPS_POLICY}'   '1'

    ${NP_REUSE_WIPS} =               Configure Reuse Wips Policy On Network Policy  ${NW_POLICY_NAME}  ${WIPS_POLICY_NAME}
    Should Be Equal As Strings       '${NP_REUSE_WIPS}'   '1'

    ${EDIT_POLICY_AP_STATUS} =       Edit Network Policy Type  ${NW_POLICY_NAME}  wireless=enable,switches=disable,routing=enable
    Should Be Equal As Strings       '${EDIT_POLICY_AP_STATUS}'   '1'

    Enable Nw Presence Analytics     ${NW_POLICY_NAME}

    ${IBEACON_STATUS}=               Enable IBeacon Service In Network Policy  ${NW_POLICY_NAME}  ${BEACON_SERVICE_NAME}  ${UUID}   monitoring=enable
    Should Be Equal As Strings       '${IBEACON_STATUS}'   '1'

    ${ONBOARD_RESULT}=             Onboard AP                       ${ap2.serial}       aerohive       ${LOCATION}
    should be equal as integers        ${ONBOARD_RESULT}       1

    ${AP_SPAWN}=                     open spawn       ${ap2.ip}      ${ap2.port}   ${ap2.username}     ${ap2.password}        ${ap2.platform}
    Set Suite Variable               ${AP_SPAWN}
    ${OUTPUT0}=                      Send Commands       ${AP_SPAWN}         capwap client server name ${CAPWAP_URL}, capwap client default-server-name ${CAPWAP_URL}, capwap client server backup name ${CAPWAP_URL}, no capwap client enable, capwap client enable, save config
    sleep    240s
    Wait Until Device Online         ${ap2.serial}

    Refresh Devices Page

    ${AP2_UPDATE_CONFIG}=            Update Network Policy To AP   ${NW_POLICY_NAME}     ap_serial=${ap2.serial}   update_method=Complete
    Should Be Equal As Strings      '${AP2_UPDATE_CONFIG}'       '1'
    Wait Until Device Online         ${ap2.serial}

    sleep   2 minutes
    Refresh Devices Page

    subscribe adess essentials
    subscribe extreme location essentials
    sleep   4 minutes

    [Teardown]   run keywords        Logout User
    ...                              Quit Browser

Test2: validate alarms details in AD essentials - ADESS and XLOC coexistence
    [Documentation]         validate alarms details in AD essentials - ADESS and XLOC coexistence.
    [Tags]                  tccs_13251        testbed_adsp        development
    Depends On              Test1
    Login User                      ${TENANT_USERNAME1}     ${TENANT_PASSWORD1}
    ${ALARM_DETAILS_ON_GRID}=        Get ADSP Alarm Details    ${ap2.mac}
    ${ALARM_STATE_GRID}=             Get From Dictionary       ${ALARM_DETAILS_ON_GRID}    alarmState
    ${ALARM_STATE_LIST}=             Split String              ${ALARM_STATE_GRID}         separator=notifications_active\n
    ${ALARM_STATE}=                  Set Variable              ${ALARM_STATE_LIST}[1]
    Should Contain                   '${ALARM_STATE}'          'ACTIVE'
    Should Not Contain               '${ALARM_STATE}'          'INACTIVE'

    ${SENSOR_MAC}=                   Get From Dictionary       ${ALARM_DETAILS_ON_GRID}    sensorMac
    Should Be Equal As Strings       '${SENSOR_MAC}'          '${ap2.mac}'

    ${SITE_ID}=                      Get From Dictionary       ${ALARM_DETAILS_ON_GRID}    siteId
    Should Be Equal As Strings       '${SITE_ID}'              '${BUILDING_NAME}'

    [Teardown]   run keywords        Logout User
    ...                              Quit Browser

Test3: validate alarms count in AD essentials - ADESS and XLOC coexistence
    [Documentation]         validate alarms count in AD essentials - ADESS and XLOC coexistence.
    [Tags]                  tccs_13252       testbed_adsp        development
    Depends On              Test1
    Login User                       ${TENANT_USERNAME1}     ${TENANT_PASSWORD1}
    ${ALARM_COUNT_ON_GRID}=          Get Total ADSP Alarm Count

    ${ALARM_OVERVIEW_COUNT}=         Check ADSP Alarms Overview Widget Count

    Should Be Equal As Strings       '${ALARM_OVERVIEW_COUNT}'  '${ALARM_COUNT_ON_GRID}'
    [Teardown]   run keywords        Logout User
    ...                              Quit Browser

Test4: validate essentials command in ap cli - ADESS and XLOC coexistence
    [Documentation]         validate essentials command in ap cli - ADESS and XLOC coexistence.
    [Tags]                  tccs_13253       testbed_adsp        development
    Depends On              Test1

    ${AP_SPAWN}=                     open spawn       ${ap2.ip}      ${ap2.port}   ${ap2.username}     ${ap2.password}        ${ap2.platform}
    ${SENSOR_WIFI_CONFIG}=           send commands               ${AP_SPAWN}         show running-config | include "interface wifi2"
    Should Contain                   ${SENSOR_WIFI_CONFIG}      interface wifi2 mode adsp-sensor

    ${IBEACON_CONFIG}=               send commands                ${AP_SPAWN}         show running-config | include ble0
    Should Contain                   ${IBEACON_CONFIG}      interface ble0 ibeacon enable
    Should Contain                   ${IBEACON_CONFIG}      interface ble0 ibeacon-monitor enable

    ${CONFIG1}=                      send commands              ${AP_SPAWN}         show application-essentials info
    Should Contain                   ${CONFIG1}          wifi2:  status:on  profile:default-xiq-profile

    ${CONFIG2}=                      send commands              ${AP_SPAWN}         show application-essentials profile
    Should Contain                   ${CONFIG2}          Name:   default-xiq-profile

    ${ESSENTIALS_CONFIG}=            send commands                ${AP_SPAWN}         show running-config | include essentials
    Should Contain                   ${ESSENTIALS_CONFIG}      wips-essentials enable
    Should Contain                   ${ESSENTIALS_CONFIG}      location-essentials enable

Test5: Verify Network policy with wireless and switching mode enabled
    [Documentation]         Network policy with wireless and switching mode enabled, Alarms state validation in AD Essentials - ADESS and XLOC coexistence.
    [Tags]                  tccs_13254   testbed_adsp       development
     Depends On              Test1

     Login User          ${TENANT_USERNAME1}     ${TENANT_PASSWORD1}

    ${EDIT_POLICY_AP_TEMPLATE_STATUS} =     Edit Network Policy Type  ${NW_POLICY_NAME}  wireless=enable,switches=enable,routing=disable
    Should Be Equal As Strings      '${EDIT_POLICY_AP_TEMPLATE_STATUS}'   '1'

    ${AP2_UPDATE_CONFIG}=           Update Network Policy To AP   policy_name=${NW_POLICY_NAME}     ap_serial=${ap2.serial}   update_method=Delta
    Should Be Equal As Strings      '${AP2_UPDATE_CONFIG}'       '1'

    Refresh Devices Page

    ${ALARM_DETAILS_ON_GRID}=        Get ADSP Alarm Details    ${ap2.mac}
    ${ALARM_STATE_GRID}=             Get From Dictionary       ${ALARM_DETAILS_ON_GRID}    alarmState
    ${ALARM_STATE_LIST}=             Split String              ${ALARM_STATE_GRID}         separator=notifications_active\n
    ${ALARM_STATE}=                  Set Variable              ${ALARM_STATE_LIST}[1]
    Should Contain                   '${ALARM_STATE}'          'ACTIVE'
    Should Not Contain               '${ALARM_STATE}'          'INACTIVE'

    ${SENSOR_MAC}=                   Get From Dictionary       ${ALARM_DETAILS_ON_GRID}    sensorMac
    Should Be Equal As Strings       '${SENSOR_MAC}'          '${ap2.mac}'

    ${SITE_ID}=                      Get From Dictionary       ${ALARM_DETAILS_ON_GRID}    siteId
    Should Be Equal As Strings       '${SITE_ID}'              '${BUILDING_NAME}'

    [Teardown]   run keywords        Logout User
    ...                              Quit Browser

Test6: validate alarms count in AD essentials - ADESS and XLOC coexistence-wireless and switching mode enabled
    [Documentation]         validate alarms count in AD essentials - wireless and switching mode enabled - ADESS and XLOC coexistence.
    [Tags]                  tccs_13255      testbed_adsp       development
    Depends On              Test1
    Login User                       ${TENANT_USERNAME1}     ${TENANT_PASSWORD1}

    ${ALARM_COUNT_ON_GRID}=          Get Total ADSP Alarm Count

    ${ALARM_OVERVIEW_COUNT}=         Check ADSP Alarms Overview Widget Count

    Should Be Equal As Strings       '${ALARM_OVERVIEW_COUNT}'  '${ALARM_COUNT_ON_GRID}'
    [Teardown]   run keywords        Logout User
    ...                              Quit Browser

Test7: validate essentials command in ap cli - ADESS and XLOC coexistence--wireless and switching mode enabled
    [Documentation]         validate essentials command in ap cli - wireless and switching mode enabled - ADESS and XLOC coexistence.
    [Tags]                  tccs_13256      testbed_adsp       development
    Depends On              Test1

    ${AP_SPAWN}=                     open spawn       ${ap2.ip}      ${ap2.port}   ${ap2.username}     ${ap2.password}        ${ap2.platform}
    ${SENSOR_WIFI_CONFIG}=           send commands               ${AP_SPAWN}         show running-config | include "interface wifi2"
    Should Contain                   ${SENSOR_WIFI_CONFIG}      interface wifi2 mode adsp-sensor

    ${IBEACON_CONFIG}=               send commands                ${AP_SPAWN}         show running-config | include ble0
    Should Contain                   ${IBEACON_CONFIG}      interface ble0 ibeacon enable
    Should Contain                   ${IBEACON_CONFIG}      interface ble0 ibeacon-monitor enable

    ${CONFIG1}=                      send commands               ${AP_SPAWN}         show application-essentials info
    Should Contain                   ${CONFIG1}          wifi2:  status:on  profile:default-xiq-profile

    ${CONFIG2}=                      send commands               ${AP_SPAWN}         show application-essentials profile
    Should Contain                   ${CONFIG2}          Name:   default-xiq-profile

    ${ESSENTIALS_CONFIG}=            send commands               ${AP_SPAWN}         show running-config | include essentials
    Should Contain                   ${ESSENTIALS_CONFIG}      wips-essentials enable
    Should Contain                   ${ESSENTIALS_CONFIG}      location-essentials enable

Test8: Verify Network policy with ONLY wireless mode enabled
    [Documentation]         Network policy with ONLY wireless mode enabled, Alarms state validation in AD Essentials - ADESS and XLOC coexistence.
    [Tags]                  tccs_13257      testbed_adsp        development
    Depends On              Test1

    Login User          ${TENANT_USERNAME1}     ${TENANT_PASSWORD1}

    ${EDIT_POLICY_AP_TEMPLATE_STATUS} =     Edit Network Policy Type  ${NW_POLICY_NAME}  wireless=enable,switches=disable,routing=disable
    Should Be Equal As Strings      '${EDIT_POLICY_AP_TEMPLATE_STATUS}'   '1'

    ${AP2_UPDATE_CONFIG}=           Update Network Policy To AP   policy_name=${NW_POLICY_NAME}     ap_serial=${ap2.serial}   update_method=Delta
    Should Be Equal As Strings      '${AP2_UPDATE_CONFIG}'       '1'

    Refresh Devices Page

    ${ALARM_DETAILS_ON_GRID}=        Get ADSP Alarm Details    ${ap2.mac}
    ${ALARM_STATE_GRID}=             Get From Dictionary       ${ALARM_DETAILS_ON_GRID}    alarmState
    ${ALARM_STATE_LIST}=             Split String              ${ALARM_STATE_GRID}         separator=notifications_active\n
    ${ALARM_STATE}=                  Set Variable              ${ALARM_STATE_LIST}[1]
    Should Contain                   '${ALARM_STATE}'          'ACTIVE'
    Should Not Contain               '${ALARM_STATE}'          'INACTIVE'

    ${SENSOR_MAC}=                   Get From Dictionary       ${ALARM_DETAILS_ON_GRID}    sensorMac
    Should Be Equal As Strings       '${SENSOR_MAC}'          '${ap2.mac}'

    ${SITE_ID}=                      Get From Dictionary       ${ALARM_DETAILS_ON_GRID}    siteId
    Should Be Equal As Strings       '${SITE_ID}'              '${BUILDING_NAME}'

    [Teardown]   run keywords        Logout User
    ...                              Quit Browser

Test9: validate alarms count in AD essentials - ADESS and XLOC coexistence-Only wireless enabled
    [Documentation]         validate alarms count in AD essentials - Network policy with ONLY wireless mode enabled - ADESS and XLOC coexistence.
    [Tags]                  tccs_13258      testbed_adsp        development
    Depends On              Test1
    Login User                       ${TENANT_USERNAME1}     ${TENANT_PASSWORD1}

    ${ALARM_COUNT_ON_GRID}=          Get Total ADSP Alarm Count

    ${ALARM_OVERVIEW_COUNT}=         Check ADSP Alarms Overview Widget Count
    Should Be Equal As Strings       '${ALARM_OVERVIEW_COUNT}'  '${ALARM_COUNT_ON_GRID}'
    [Teardown]   run keywords        Logout User
    ...                              Quit Browser

Test10: validate essentials command in ap cli - ADESS and XLOC coexistence-Only wireless enabled
    [Documentation]         validate essentials command in ap cli - Network policy with ONLY wireless mode enabled - ADESS and XLOC coexistence.
    [Tags]                  tccs_13259      testbed_adsp        development
    Depends On              Test1

    ${AP_SPAWN}=                     open spawn       ${ap2.ip}      ${ap2.port}   ${ap2.username}     ${ap2.password}        ${ap2.platform}
    ${SENSOR_WIFI_CONFIG}=           send commands              ${AP_SPAWN}         show running-config | include "interface wifi2"
    Should Contain                   ${SENSOR_WIFI_CONFIG}      interface wifi2 mode adsp-sensor

    ${IBEACON_CONFIG}=               send commands               ${AP_SPAWN}         show running-config | include ble0
    Should Contain                   ${IBEACON_CONFIG}      interface ble0 ibeacon enable
    Should Contain                   ${IBEACON_CONFIG}      interface ble0 ibeacon-monitor enable

    ${CONFIG1}=                      send commands              ${AP_SPAWN}         show application-essentials info
    Should Contain                   ${CONFIG1}          wifi2:  status:on  profile:default-xiq-profile

    ${CONFIG2}=                      send commands              ${AP_SPAWN}         show application-essentials profile
    Should Contain                   ${CONFIG2}          Name:   default-xiq-profile

    ${ESSENTIALS_CONFIG}=            send commands              ${AP_SPAWN}         show running-config | include essentials
    Should Contain                   ${ESSENTIALS_CONFIG}      wips-essentials enable
    Should Contain                   ${ESSENTIALS_CONFIG}      location-essentials enable

Test11: Verify backup viq
    [Documentation]     Check the viq backup
    [Tags]      tccs_13260    testbed_adsp     development
      ${result1}=         login user  ${TENANT_USERNAME1}   ${TENANT_PASSWORD1}
     Should Be Equal As Strings      '${result1}'     '1'
       ${BKUP_VIQ}=           backup viq data
       Should Be Equal As Strings      '${BKUP_VIQ}'              '1'
                             sleep  60s
    [Teardown]        run keywords    logout user
     ...                               QUIT BROWSER

Test12: Verify reset viq
    [Documentation]     Check the reset viq
     [Tags]          tccs_13261   testbed_adsp      development
     depends on     Test11
    ${result1}=         login user  ${TENANT_USERNAME1}   ${TENANT_PASSWORD1}
     Should Be Equal As Strings      '${result1}'     '1'

     ${Reset_VIQ}=    reset viq data
                       Should Be Equal As Strings      '${Reset_VIQ}'     '1'
                        sleep  180s
     [Teardown]        run keywords    logout user
     ...                               QUIT BROWSER

Test13: Verify adess subscription after reset VIQ
      [Documentation]     Check the ADESS subscription after rest VIQ
      [Tags]        tccs_13262   testbed_adsp      development
             ${result1}=         login user  ${TENANT_USERNAME1}   ${TENANT_PASSWORD1}
                                 Should Be Equal As Strings      '${result1}'     '1'
                                 click advanced onboard popup
            ${Chk_ADESS_MENU}=     check subscription of ADEssentials page
            Should Be Equal As Strings       '${Chk_ADESS_MENU}'          '1'
      [Teardown]                   run keywords    logout user
     ...                                          QUIT BROWSER