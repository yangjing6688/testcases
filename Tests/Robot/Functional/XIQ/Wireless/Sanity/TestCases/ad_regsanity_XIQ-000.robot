# Author        : Kiran
# Date          : June27,2022
# Description   : ADSP Regression Cases

*** Variables ***
${WIPS_POLICY_NAME}             adsp_reg_wips_policy
${NW_POLICY_NAME}               adsp_reg_nw_policy
${SSID_NAME}                    adsp_reg_ssid
${NEW_LOCATION}                 auto_location_01,San Jose,building_01,floor_01
${LOCATION}                     auto_location_01, San Jose, building_01, floor_02

${NW_ONPREM_POLICY_NAME}        policy_onprem_reg_adsp
${SSID_NAME_ONPREM}             ssid_onprem_reg_adsp
${WIPS_ONPREM_POLICY_NAME}      wips_onprem_reg_adsp

${NW_DUAL_POLICY_NAME}          policy_dual_reg_adsp
${SSID_NAME_DUAL}               ssid_dual_reg_adsp
${WIPS_DUAL_POLICY_NAME}        wips_dual_reg_adsp

${NW_WIFI6_POLICY_NAME}         policy_wifi6_reg_adsp
${SSID_NAME_WIFI6}              ssid_wifi6_reg_adsp
${WIPS_WIFI6_POLICY_NAME}       wips_wifi6_reg_adsp

${NEWLOCATIONXLOC}              auto_location_01,San Jose,building_01,floor_02

${BUILDING_NAME}                building_01
${NW_POLICY_NAME2}              alarm_generation_policy
${SSID_NAME2}                   alarm_generation_ssid
${EXPECTED_NON_ROGUE_ALARM}     DoS Deauthentication
${MAP_FILE_NAME}                auto_location_01_1595321828282.tar.gz
*** Settings ***

Force Tags   testbed_adsp

Library     Collections
Library     String
Library     common/Utils.py
Library     common/Cli.py
Library     common/TestFlow.py

Library     xiq/flows/common/Login.py
Library     xiq/flows/common/Navigator.py
Library     xiq/flows/mlinsights/Network360Plan.py

Library     xiq/flows/AirDefence/AirDefenceAlarms.py
Library     xiq/flows/extreme_location/ExtremeLocation.py
Library     xiq/flows/extreme_guest/ExtremeGuest.py
Library     xiq/flows/globalsettings/GlobalSetting.py

Library     xiq/flows/manage/Client.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/Location.py

Library     xiq/flows/configure/Wips.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/configure/CommonObjects.py
Library     xiq/flows/configure/DeviceTemplate.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml

Resource    Tests/Robot/Functional/XIQ/Wireless/Sanity/Resources/ad_rt_reg_config.robot

Suite Setup      Pre Condition
Suite Teardown   Test Suite Clean Up

*** Keywords ***
Pre Condition
    [Documentation]   Onboard Tri Radio AP410C, Assign policy, template with WIPS ON as ADEss Enabled
    Pre Condition
    [Documentation]   All the existing configuration clean up
    ${result}=                      Login User          ${tenant_username}     ${tenant_password}
    click advanced onboard popup
    import map in network360plan     ${MAP_FILE_NAME}
    Logout User
    Quit Browser

Test Suite Clean Up
    [Documentation]    Reset Customer Account Data
    Sleep    2 minutes
    ${LOGIN_XIQ}=                   Login User          ${tenant_username}     ${tenant_password}

    ${RESET_VIQ_DATA}=               Reset VIQ Data
    Should Be Equal As Strings      '${RESET_VIQ_DATA}'              '1'

    logout user
    quit browser

*** Test Cases ***

Test1: Onboard Dual Radio AP305C, Assign policy, template with WIPS ON as ADEss Enabled
    [Documentation]         New ADEss subscription -Ensure async pushes all commands for AD Essentials and alarms are sent for AP410C
    [Tags]                  tccs_13266      adsp        development

    ${LOGIN_XIQ}=              Login User          ${tenant_username}      ${tenant_password}

    ${ONBOARD_RESULT}=          Onboard Device      ${ap3.serial}           ${ap3.make}       location=${ap3.location}

    ${AP3_SPAWN}=            Configure Device To Connect To Cloud    ${ap3.make}    ${ap3.ip}    ${ap3.port}    ${ap3.username}    ${ap3.password}    ${ap3.platform}    ${capwap_url}

    ${WAIT_ONLINE}=         Wait Until Device Online    ${ap3.serial}
    Should Be Equal As Strings   '${WAIT_ONLINE}'   '1'

    ${REFRESH_PAGE}=         Refresh Devices Page
    Should Be Equal As Strings      '${REFRESH_PAGE}'       '1'

    ${AP3_STATUS}=              Get AP Status       ap_mac=${ap3.mac}
    Should Be Equal As Strings  '${AP3_STATUS}'     'green'

    close Spawn  ${AP3_SPAWN}

    ${CREATE_POLICY2}=         Create Network Policy    ${NW_DUAL_POLICY_NAME}       ${ADSP_DUAL_OPEN_NW}
    Should Be Equal As Strings   '${CREATE_POLICY2}'   '1'

    ${CREATE_AP_TEMPLATE2}=     Add AP Template     ${ap3.model}     ${ap3.template_name}        &{AP_DUAL_TEMPLATE_CONFIG}
    Should Be Equal As Strings   '${CREATE_AP_TEMPLATE2}'   '1'

    ${CONFIG_WIPS_POLICY2}      Configure WIPS Policy On Common Objects   ${WIPS_DUAL_POLICY_NAME}
    Should Be Equal As Strings   '${CONFIG_WIPS_POLICY2}'   '1'

    ${NP_REUSE_WIPS2}           Configure Reuse Wips Policy On Network Policy    ${NW_DUAL_POLICY_NAME}    ${WIPS_DUAL_POLICY_NAME}
    Should Be Equal As Strings   '${NP_REUSE_WIPS2}'   '1'

    ${AP3_UPDATE_CONFIG2}=      Update Network Policy To AP   ${NW_DUAL_POLICY_NAME}     ap_serial=${ap3.serial}   update_method=Complete
    Should Be Equal As Strings              '${AP3_UPDATE_CONFIG2}'       '1'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

Test2: Onboard WiFi6 AP4000U, Assign policy, template with WIPS ON as ADEss Enabled
    [Documentation]         New ADEss subscription -Ensure async pushes all commands for AD Essentials and alarms are sent for AP410C
    [Tags]                  tccs_13267      adsp        development

    ${LOGIN_XIQ}=              Login User          ${tenant_username}      ${tenant_password}

    ${ONBOARD_RESULT}=          Onboard Device      ${ap4.serial}           ${ap4.make}       location=${ap4.location}

    ${AP4_SPAWN}=            Configure Device To Connect To Cloud    ${ap4.make}    ${ap4.ip}    ${ap4.port}    ${ap4.username}    ${ap4.password}    ${ap4.platform}    ${capwap_url}

    ${WAIT_ONLINE}=         Wait Until Device Online    ${ap4.serial}
    Should Be Equal As Strings   '${WAIT_ONLINE}'   '1'

    ${REFRESH_PAGE}=         Refresh Devices Page
    Should Be Equal As Strings      '${REFRESH_PAGE}'       '1'

    ${AP4_STATUS}=              Get AP Status       ap_mac=${ap4.mac}
    Should Be Equal As Strings  '${AP4_STATUS}'     'green'

    close Spawn  ${AP4_SPAWN}

    ${CREATE_POLICY3}=         Create Network Policy    ${NW_WIFI6_POLICY_NAME}       ${ADSP_WIFI6_OPEN_NW}
    Should Be Equal As Strings   '${CREATE_POLICY3}'   '1'

    ${CREATE_AP_TEMPLATE3}=     Add AP Template     ${ap4.model}     ${ap4.template_name}        &{AP_WIFI6_TEMPLATE_CONFIG}
    Should Be Equal As Strings   '${CREATE_AP_TEMPLATE3}'   '1'

    ${CONFIG_WIPS_POLICY3}      Configure WIPS Policy On Common Objects   ${WIPS_WIFI6_POLICY_NAME}
    Should Be Equal As Strings   '${CONFIG_WIPS_POLICY3}'   '1'

    ${NP_REUSE_WIPS3}           Configure Reuse Wips Policy On Network Policy    ${NW_WIFI6_POLICY_NAME}    ${WIPS_WIFI6_POLICY_NAME}
    Should Be Equal As Strings   '${NP_REUSE_WIPS3}'   '1'

    ${AP3_UPDATE_CONFIG3}=      Update Network Policy To AP   ${NW_WIFI6_POLICY_NAME}     ap_serial=${ap4.serial}   update_method=Complete
    Should Be Equal As Strings              '${AP3_UPDATE_CONFIG3}'       '1'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

Test3: Async subscription on ADEss application with Dual, Tri radio as well as WIFI6 AP and check for necessary wips commands in all APs
    [Documentation]         New ADEss subscription -Ensure async pushes all commands for AD Essentials and alarms are sent for AP410C
    [Tags]                  tccs_13268      adsp        development

    ${LOGIN_XIQ}=              Login User          ${tenant_username}      ${tenant_password}

    ${SUBSCRIBE_ADEss}=          Subscribe ADESS Essentials
    Should Be Equal As Strings      '${SUBSCRIBE_ADEss}'   '1'

    Sleep   30s

    ${AP1_SPAWN}=               open PXSSH spawn         ${ap1.ip}        ${ap1.username}       ${ap1.password}        ${ap1.port}
    ${SENSOR_WIFI_CONFIG1}=     Send                ${AP1_SPAWN}         show running-config | include "interface wifi2 mode"
    Should Contain             ${SENSOR_WIFI_CONFIG1}      interface wifi2 mode adsp-sensor

    ${CONFIG1}=                Send                ${AP1_SPAWN}         show running-config | include "wips-essentials"
    Should Contain             ${CONFIG1}          wips-essentials enable

    close spawn   ${AP1_SPAWN}

    ${AP3_SPAWN}=               open PXSSH spawn         ${ap3.ip}        ${ap3.username}       ${ap3.password}        ${ap3.port}

    ${CONFIG2}=                Send                ${AP3_SPAWN}         show running-config | include "wips-essentials"
    Should Contain             ${CONFIG2}          wips-essentials enable

    close spawn   ${AP3_SPAWN}

    ${AP4_SPAWN}=               Open Spawn          ${ap4.ip}       ${ap4.port}      ${ap4.username}       ${ap4.password}        ${ap4.platform}
    ${SENSOR_WIFI_CONFIG3}=     Send                ${AP4_SPAWN}         show running-config | include "interface wifi2 mode"
    Should Contain             ${SENSOR_WIFI_CONFIG3}      interface wifi2 mode adsp-sensor

    ${CONFIG3}=                Send                ${AP4_SPAWN}         show running-config | include "wips-essentials"
    Should Contain             ${CONFIG3}          wips-essentials enable

    close spawn   ${AP4_SPAWN}

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

Test4: Verify non-rogue alarm generation in the ADEss application
    [Documentation]         Verify DDoS Dissasociation alarm in ADEss application for AP410C
    [Tags]                  tccs_13269      adsp        development

    ${LOGIN_XIQ}=              Login User          ${tenant_username}      ${tenant_password}

    ${ALARM_DETAILS_ON_GRID}=       Get ADSP Alarm Details    ${EXPECTED_NON_ROGUE_ALARM}

    ${ALARM_NAME}=                  Get From Dictionary       ${ALARM_DETAILS_ON_GRID}    alarmId
    Should Be Equal As Strings      '${ALARM_NAME}'          '${EXPECTED_NON_ROGUE_ALARM}'

    [Teardown]   run keywords     Logout User
    ...                           Quit Browser

Test5: Change device location in XIQ and check in ADEss Sensor Page
    [Documentation]         Change device location in XIQ and check in Sensor page of ADEss application
    [Tags]                  tccs_13271      adsp        development

    ${LOGIN_XIQ}=              Login User          ${tenant_username}      ${tenant_password}

    ${ASSIGN_NEW_LOCATION_TO_AP}=      Assign Location With Device Actions    ${ap4.serial}       ${ap4.new_location}
    Should Be Equal As Strings    '${ASSIGN_NEW_LOCATION_TO_AP}'    '1'

    ${VERIFY_LOCATION_ADESS}=      Check Location Assigned to AP in ADESS     ${ap4.serial}       ${NEW_LOCATION}
    Should Be Equal As Strings     '${VERIFY_LOCATION_ADESS}'    '1'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

Test6: Check whether AP4000U appears on ADEss Sensor Page
    [Documentation]         Assign policy and location to AP4000 and check in ADEss Device View Page
    [Tags]                  tccs_13270      adsp        development

    ${LOGIN_XIQ}=              Login User          ${tenant_username}      ${tenant_password}

    ${CHECK_AP_IN_ADESS}=         Check AP in ADESS Device View Page    ${ap4.serial}
    Should Be Equal As Strings   '${CHECK_AP_IN_ADESS}'    '1'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

Test7: Verify AD on-prem, XLOC and Eguest works together with one AP and one XIQ account. Test with AP410C
    [Documentation]         Check whether AP410C when configured with open ssid, presence and ad on prem server details, works fine for respective applications
    [Tags]                  tccs_13273      adsp        development

    ${LOGIN_XIQ}=              Login User          ${tenant_username}      ${tenant_password}

    ${CREATE_POLICY1}=         Create Network Policy    ${NW_ONPREM_POLICY_NAME}       ${ADSP_ONPREM_OPEN_NW}
    Should Be Equal As Strings   '${CREATE_POLICY1}'   '1'

    ${CREATE_AP_TEMPLATE}=     Add AP Template     ${ap1.model}     ${ap1.template_onprem_name}        &{AP_TEMPLATE_CONFIG}
    Should Be Equal As Strings   '${CREATE_AP_TEMPLATE}'   '1'

    Enable Nw Presence Analytics    ${NW_ONPREM_POLICY_NAME}

    ${CONFIG_NEW_WIPS_POLICY}      Configure WIPS Policy On Common Objects   ${WIPS_ONPREM_POLICY_NAME}
    Should Be Equal As Strings   '${CONFIG_NEW_WIPS_POLICY}'   '1'

    ${ONPREM_CONFIG}=       Wips onprem adsp serverip configuration on Network Policy      ${NW_ONPREM_POLICY_NAME}    ${WIPS_ONPREM_POLICY_NAME}     enable      &{ON_PREM_ADSP_SERVER_IP_CONFIG}
    Should Be Equal As Strings       '${ONPREM_CONFIG}'   '1'

    ${AP1_UPDATE_CONFIG}=           Update Network Policy To AP     ${NW_ONPREM_POLICY_NAME}     ap_serial=${ap1.serial}   update_method=Complete
    Should Be Equal As Strings      '${AP1_UPDATE_CONFIG}'       '1'

    ${SUBSCRIBE_LOCATION}=          Subscribe Extreme Location Essentials
    Should Be Equal As Strings      '${SUBSCRIBE_LOCATION}'   '1'

    ${SUBSCRIBE_GUEST}=          Go to Extreme Guest Landing Page
    Should Be Equal As Strings      '${SUBSCRIBE_GUEST}'   '1'

    ${AP_SPAWN}=               open PXSSH spawn         ${ap1.ip}        ${ap1.username}       ${ap1.password}        ${ap1.port}
    ${SENSOR_WIFI_CONFIG}=           Send                ${AP_SPAWN}         show running-config | include "interface wifi2 mode"
    Should Contain                   ${SENSOR_WIFI_CONFIG}      interface wifi2 mode adsp-sensor

    ${SENSOR_XLOC_CONFIG}=     Send                ${AP_SPAWN}         show running-config | include "location-essentials"
    Should Contain             ${SENSOR_XLOC_CONFIG}      location-essentials enable

    ${SENSOR_AD_ONPREM_CONFIG}=     Send                ${AP_SPAWN}         show running-config | include "adsp-server index 1"
    Should Contain             ${SENSOR_AD_ONPREM_CONFIG}      adsp-server index 1 ip-address ${ONPREM_ADSP_SERVER_IP} port ${ONPREM_ADSP_SERVER_PORT}
    Close Spawn                      ${AP_SPAWN}

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

Test8: Change device location in XIQ and check in XLOC AP Page
    [Documentation]         Verify changed location in Test6 in AP Page of XLOC application
    [Tags]                  tccs_13272      adsp        development

    ${LOGIN_XIQ}=              Login User          ${tenant_username}      ${tenant_password}

    ${VERIFY_LOCATION_XLOC}=      Check Location Assigned to AP in XLOC    ${ap3.name}       ${NEWLOCATIONXLOC}
    Should Be Equal As Strings    '${VERIFY_LOCATION_XLOC}'    '1'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

Test9: Verify that HOS sensor won't send any frames and get disconnected from ADSP if 3rd radio is disabled for AP410C
    [Documentation]         Configure ADSP on AP
    [Tags]                  tccs_13274      adsp        development

    ${LOGIN_XIQ}=              Login User          ${tenant_username}      ${tenant_password}

    ${EDIT_AP_TEMPLATE}=      Edit AP Net Policy Template Wifi2     ${NW_ONPREM_POLICY_NAME}
    Should Be Equal As Strings    '${EDIT_AP_TEMPLATE}'    '1'

    ${AP1_UPDATE_CONFIG}=      Update Network Policy To AP    ${NW_ONPREM_POLICY_NAME}     ap_serial=${ap1.serial}
    Should Be Equal As Strings              '${AP1_UPDATE_CONFIG}'       '1'

    Sleep    20s

    ${AP_SPAWN}=               open PXSSH spawn         ${ap1.ip}        ${ap1.username}       ${ap1.password}        ${ap1.port}
    ${CONFIG1}=                      Send                ${AP_SPAWN}         show adsp-server status
    Should Contain                   ${CONFIG1}          Server 1: ${ONPREM_ADSP_SERVER_IP}  Port: ${ONPREM_ADSP_SERVER_PORT}
    Should Contain                   ${CONFIG1}          status: offline

    close Spawn  ${AP_SPAWN}

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

Test10: Verify Subscription Not Found when AD Essentials service is not enabled
    [Documentation]         Verify Subscription Not Found when Essentials service is not enabled
    [Tags]                  tccs_13275      adsp        development

    ${LOGIN_XIQ}=              Login User          ${tenant1_username1}      ${tenant1_password1}

    ${CHECK_ADESS_ERR_NOT_ENABLED}=          Check Error Msg When ADESS Not Enabled         ${adess_url}
    Should Be Equal As Strings      '${CHECK_ADESS_ERR_NOT_ENABLED}'   '1'

    [Teardown]   run keywords     Logout User
    ...                           Quit Browser

Test11: Perform BackUp VIQ
    [Documentation]         BackUp Customer Account Data
    [Tags]                  tccs_13276      adsp        development

    ${LOGIN_XIQ}=                   Login User          ${tenant_username}     ${tenant_password}
    ${BACKUP_VIQ_DATA}=             Backup VIQ Data
    Should Be Equal As Strings      '${BACKUP_VIQ_DATA}'              '1'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

