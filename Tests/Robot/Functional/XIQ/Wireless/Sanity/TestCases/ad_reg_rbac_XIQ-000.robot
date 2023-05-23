# Author        : Karthik Venkatesamoorthy
# Date          : July 8 2022
# Description   : This contains RBAC related TCs
#check if Location,Building and floor are deleted before starting the test case
#check if ADESS is subscribed before starting the test case
# Topology      :
# Host ----- Cloud
*** Variables ***
#Defaults
${ENV}                  environment.ad_rt_reg.remote.win10.chrome.yaml
${TOPO}                 topo.ad_rt_reg.g2r1.yaml
${TESTBED}              BANGALORE/Prod/wireless/ad_rt_reg.yaml

${AP1_SERIAL}                   04102003240819
${AP1_NETWORK_POLICY}           Test_np
${AP1_WLAN}                     AP410C_02
${AP1_SSID}                     AP410C_02
${AP1_SITE}                     AP410C_02
${SSID_NAME}                    test_automation_adess_reg
${ALARM_TYPE}                   MAJOR
${AP1_TEMPLATE_NAME}            AP410C-ADESS_REG

${CAPWAP_URL}                     g2r1-cwpm-01.qa.xcloudiq.com
${CMD_CAPWAP_CLIENT_STATE}          show capwap client | include state
${CMD_CAPWAP_HM_PRIMARY_NAME}       show capwap client | include "HiveManager Primary Name"
${CMD_CAPWAP_SERVER_IP}             show capwap client | include "CAPWAP server IP"
${CMD_CAPWAP_PRIMARY_NAME}          show capwap client | include "HiveManager Primary Name"
${OUTPUT_CAPWAP_STATUS}             Connected securely to the CAPWAP server

${NW_POLICY_NAME}           adessreg_auto
${BUILDING_NAME}            building_01
${FLOOR_NAME}               floor_02
${MAP_FILE_NAME}            auto_location_f01_1654845780826.tar.gz
${Initial_ap_pass}          aerohive
${WIPS_POLICY_NAME}         WIPS_ADESSREG
${STATUS}                    ON
${TEST_ESS_URL}             https://g2r1.qa.xcloudiq.com/airdefense/essentials
${SEARCH_STRING}             ON
${MSG}                      Welcome to ExtremeCloud IQ
${user}                       monitor
${MAIL_ID}                      xiqextremeqa@gmail.com
${PASSWORD}                     Extreme@123
#robot -L INFO -v TEST_URL:https://g2.qa.xcloudiq.com/ -v TESTBED:kar_topo -v DEVICE1:AP410C -v DEVICE2:AP305C -v TOPO:topo1  ad_reg_rbac_XIQ-000.robot
#robot -L INFO -v TEST_URL:https://g2.qa.xcloudiq.com/ -v TESTBED:kar_topo -v DEVICE1:AP410C -v DEVICE2:AP305C -v TOPO:topo1 -i test1  ad_reg_rbac_XIQ-000.robot

*** Settings ***
Force Tags   testbed_adsp

Library     Collections
Library     String
Library     common/Utils.py
Library     common/Cli.py
Library     common/Mu.py
Library     common/TestFlow.py

# The keywords in Login.py have been moved to the keywords directory.
# If the moved keyword is not working correctly import the original library and remove the keywords/gui/login/KeywordsLogin.py version.
#Library     xiq/flows/common/Login.py
Library     keywords/gui/login/KeywordsLogin.py
Library     xiq/flows/common/Navigator.py
Library     xiq/flows/extreme_location/ExtremeLocation.py
Library     xiq/flows/manage/Client.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/Location.py

Library     xiq/flows/configure/Wips.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/configure/CommonObjects.py
Library     xiq/flows/configure/DeviceTemplate.py

Library     xiq/flows/globalsettings/GlobalSetting.py
Library     xiq/flows/globalsettings/AccountManagement.py
Library     xiq/flows/mlinsights/Network360Plan.py
Library     xiq/flows/AirDefence/AirDefenceAlarms.py
Library     common/CloudDriver.py
Library     common/GmailHandler.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml
Variables    TestBeds/BANGALORE/Prod/wireless/ad_rt_reg.yaml

Resource     testsuites/xiq/config/waits.robot
Resource    Tests/Robot/Functional/XIQ/Wireless/Sanity/Resources/ad_rt_reg_config.robot


#Suite Setup      Pre Condition
#Suite Teardown   Test Suite Clean Up

*** Keywords ***
Pre Condition
    [Documentation]   AP Should be onboarded  and it is online
    ${result}=                      Login User          ${tenant_username}     ${tenant_password}
    click advanced onboard popup
    DELETE MANAGEMENT ACCOUNT       ${OPERATOR_EMAIL}
    DELETE MANAGEMENT ACCOUNT       ${MONITOR_EMAIL}
    DELETE MANAGEMENT ACCOUNT       ${HELPDESK_EMAIL}
    import map in network360plan     ${MAP_FILE_NAME}

    Logout User
    Quit Browser

Test Suite Clean Up
    [Documentation]         Test Suite Clean Up: Reset Customer Account Data
    ${LOGIN_XIQ}=                   Login User          ${TENANT_USERNAME}     ${TENANT_PASSWORD}
    ${RESET_VIQ_DATA}=               Reset VIQ Data
    Should Be Equal As Strings      '${RESET_VIQ_DATA}'              '1'
    [Teardown]   run keywords       Logout User
    ...                             Quit Browser
*** Test Cases ***
Test1: Onboard Sensor AP
    [Documentation]          Onboard Sensor AP
    [Tags]                    tccs_13236      testbed_adsp        development
    ${LOGIN_XIQ}=               Login User          ${tenant_username}     ${tenant_password}
    ${ONBOARD_RESULT}=          Onboard Device      ${ap1.serial}           ${ap1.make}       location=${ap1.location}      device_os=${ap1.cli_type}
    should be equal as integers        ${ONBOARD_RESULT}       1
    ${AP_SPAWN}=                open spawn       ${ap1.ip}      ${ap1.port}   ${ap1.username}     ${ap1.password}     ${ap1.cli_type}
    Set Suite Variable          ${AP_SPAWN}
    ${OUTPUT0}=                 send commands       ${AP_SPAWN}         capwap client server name ${capwap_url}, capwap client default-server-name ${capwap_url}, capwap client server backup name ${capwap_url}, no capwap client enable, capwap client enable, save config
    sleep  240s
    Wait Until Device Online    ${ap1.serial}
    Refresh Devices Page
    ${AP1_STATUS}=              get device status       device_mac=${ap1.mac}
    Should Be Equal As Strings  '${AP1_STATUS}'     'green'
    close Spawn  ${AP_SPAWN}
    [Teardown]         run keywords    logout user
     ...                               quit browser

Test 2: Verify Login till config push
    [Documentation]               Check the onboard AP
    [Tags]                       tccs_13237      testbed_adsp        development
          Login User                      ${TENANT_USERNAME}     ${TENANT_PASSWORD}
          ${CREATE_POLICY1}=              Create Network Policy   ${NW_POLICY_NAME}      ${ADSP_OPEN_NW}
         Should Be Equal As Strings      '${CREATE_POLICY1}'   '1'
         ${CREATE_AP_TEMPLATE}=            Add AP Template     ${ap1.model}     ${AP1_TEMPLATE_NAME}        ${AP_TEMPLATE_CONFIG}
         Should Be Equal As Strings      '${CREATE_AP_TEMPLATE}'   '1'
         ${CONFIG_WIPS_POLICY}           Configure WIPS Policy On Common Objects   ${WIPS_POLICY_NAME}
         Should Be Equal As Strings      '${CONFIG_WIPS_POLICY}'   '1'
         ${NP_REUSE_WIPS}           Configure Reuse Wips Policy On Network Policy  ${NW_POLICY_NAME}  ${WIPS_POLICY_NAME}
         Should Be Equal As Strings   '${NP_REUSE_WIPS}'   '1'
         ${AP1_UPDATE_CONFIG}=           Update Network Policy To AP   ${NW_POLICY_NAME}     ap_serial=${ap1.serial}   update_method=Complete
         Should Be Equal As Strings      '${AP1_UPDATE_CONFIG}'       '1'
         Log to Console      Sleep for ${config_push_wait}
         sleep                         ${config_push_wait}
    [Teardown]   run keywords        Logout User
    ...                              quit browser

Test 3: Verify non-rogue-alarms generation
    [Documentation]     Check the onboard AP
    [Tags]              tccs_13238      adsp        development
      ${result1}=         login user  ${TENANT_USERNAME}   ${TENANT_PASSWORD}
                           sleep  180s
       ${result2}=         get adsp alarm details        ${ALARM_TYPE}

   [Teardown]              run keywords    logout user
     ...                                    QUIT BROWSER

Test 4: Verify creation of RBAC users--Operator

    [Documentation]     Check the creation of RBAC users
    [Tags]              tccs_13239   adsp        development

    ${result1}=             login user  ${TENANT_USERNAME}    ${TENANT_PASSWORD}

    ${create_account}=      Create Role Based Account        ${OPERATOR_ROLE}
                            logout user
                            sleep   4s
    ${URL}=                 get_url_to_set_password_for_new_user     automationadessreg@gmail.com    wbdofhkkleinjxkw
    ${DRIVER}=              load web page       url=${URL}
    ${result2}=             set_password      Aerohive123
    [Teardown]              run keywords    logout user
     ...                                    QUIT BROWSER

Test 5: Verify creation of RBAC users--Monitor

    [Documentation]            Check the creation of RBAC users--Monitor
    [Tags]                    tccs_13240   adsp        development
    ${result2}=              login user  ${TENANT_USERNAME}    ${TENANT_PASSWORD}

    ${create_account}=        Create Role Based Account        ${MONITOR_ROLE}
                                logout user
                            sleep   4s
    ${URL}=                 get_url_to_set_password_for_new_user     automationadessreg@gmail.com    wbdofhkkleinjxkw
    ${DRIVER}=              load web page       url=${URL}
    ${result2}=             set_password      Aerohive123
    [Teardown]                run keywords    logout user
     ...                                      QUIT BROWSER

Test 6: Verify creation of RBAC users--HD

    [Documentation]     Check the creation of RBAC users--HD
    [Tags]              tccs_13241  adsp        development
    ${result3}=             login user  ${TENANT_USERNAME}    ${TENANT_PASSWORD}

    ${create_account}=       Create Role Based Account        ${HELPDESK_ROLE}
                                logout user
                            sleep   4s
    ${URL}=                 get_url_to_set_password_for_new_user     automationadessreg@gmail.com    wbdofhkkleinjxkw
    ${DRIVER}=              load web page       url=${URL}
    ${result2}=             set_password      Aerohive123
    [Teardown]               run keywords    logout user
     ...                                     QUIT BROWSER

Test 7: Verify adsp alarm count with operator role
  [Documentation]             Check the operator login and ADESS access
    [Tags]                   tccs_13242    adsp        development
  ${oplogin}=                 login user    ${op_username}     ${op_password}
                              Should Be Equal As Strings      '${oplogin}'     '1'
    ${ALARM_COUNT_ON_GRID}=   get total adsp alarm count
    ${ALARM_OVERVIEW_COUNT}=   check adsp alarms overview widget count
    Should Be Equal As Strings   '${ALARM_OVERVIEW_COUNT}'  '${ALARM_COUNT_ON_GRID}'

    [Teardown]                  run keywords    logout user
     ...                                        QUIT BROWSER

Test 8: Verify wireless thread detection with operator role
  [Documentation]     Check the operator login and ADESS access
    [Tags]                    tccs_13243   adsp        development
  ${oplogin}=                  login user    ${op_username}     ${op_password}
                               Should Be Equal As Strings      '${oplogin}'     '1'
  ${THREAT_DETECTION_STATUS}=  change wireless thread detection status   ${WIPS_POLICY_NAME}   ${STATUS}
    [Teardown]                 run keywords    logout user
     ...                                       QUIT BROWSER

Test 9: Verify adsp alarm count with monitor role
   [Documentation]        Check the monitor user login and ADESS access
      [Tags]                tccs_13244    adsp        development

     ${monlogin}=       login user         ${mon_username}     ${mon_password}
                        Should Be Equal As Strings         '${monlogin}'      '1'
     ${ALARM_COUNT}=    get total adsp alarm count
     ${ALARM_OVERVIEW_COUNT}=      check adsp alarms overview widget count
     Should Be Equal As Strings   '${ALARM_OVERVIEW_COUNT}'  '${ALARM_COUNT_ON_GRID}'
    [Teardown]           run keywords    logout user
     ...                                 QUIT BROWSER

Test 10: Verify ADESS(settings page) with monitor role
    [Documentation]             Check the status of ON/OFF button with monitor user
       [Tags]                   tccs_13245          testbed_adsp        development
         ${monlogin}=            login user   ${mon_username}     ${mon_password}
                                 should be equal as strings           '${monlogin}'        '1'
                                 Rbac user wips profile click status  ${user}  ${WIPS_POLICY_NAME}
      [Teardown]                 run keywords    logout user
     ...                                       QUIT BROWSER

Test 11: Verify device in location selected for monitor role
        [Documentation]        Check the location selected  with monitor user
       [Tags]                    tccs_13246    testbed_adsp       development
       ${monlogin}=               login user   ${mon_username}     ${mon_password}
                                 should be equal as strings           '${monlogin}'        '1'
       ${SEARCH_AP}=              Rbac user multiple location search AP serial      ${AP1_SERIAL}
    [Teardown]                  run keywords    logout user
     ...                                      QUIT BROWSER

Test 12: Verify ADESS menu with helpdesk role
     [Documentation]        Check the helpdesk user login and ADESS access
     [Tags]                  tccs_13247   adsp        development
     ${helplogin} =          login user        ${help_username}     ${help_password}
                             Should Be Equal As Strings        '${helplogin}'    '1'
     ${NAV_ADMENU}=          rbac user navigate to extreme airdefence helpdesk
    [Teardown]              run keywords    logout user
     ...                                    QUIT BROWSER

Test 13: Verify ADESS alarms page with helpdesk role
     [Documentation]        Check the helpdesk user login and ADESS access
     [Tags]                 tccs_13248      adsp        development
     ${helplogin1} =         login user        ${help_username}     ${help_password}
                             Should Be Equal As Strings         '${helplogin1}'    '1'
     ${status}  ${value}=     Run Keyword And Ignore Error            load web page                 ${TEST_ESS_URL}
     ${ADESS_PAGE_HELPUSER}=          adsp user role not supported page
    [Teardown]              run keywords    logout user
     ...                                    QUIT BROWSER

Test14: Verify alarm count after deleting location
    [Documentation]            Check the alarm count after deleting location
     [Tags]                     tccs_13249    adsp      development
      ${result1}=                login user  ${TENANT_USERNAME}   ${TENANT_PASSWORD}
                                 Should Be Equal As Strings      '${result1}'     '1'
      ${result2}=                delete location building floor    San Jose    building_01    floor_01
      ${CLIENT_INFO}=            get_total_adsp_alarm_count
                                 Should Be Equal As Strings      '${CLIENT_INFO}'     '0'
    [Teardown]                  run keywords    logout user
     ...                                          QUIT BROWSER

Test15: Verify backup viq
    [Documentation]         Check the viq backup
    [Tags]                   tccs_13260    adsp      development
      ${result1}=         login user  ${TENANT_USERNAME}   ${TENANT_PASSWORD}
                         Should Be Equal As Strings      '${result1}'     '1'
     ${result2}=           backup viq data
    [Teardown]        run keywords    logout user
     ...                               QUIT BROWSER
