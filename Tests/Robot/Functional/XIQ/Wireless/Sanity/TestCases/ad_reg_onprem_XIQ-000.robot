# Author        : Karthik Venkatesamoorthy
# Description   : Testcases related to ONPREM ADSP when ADESS and XLOC are not subscribed.
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
${BEACON_SERVICE_NAME}          adonprem_coex_test
${LOCATION}                     auto_location_01, San Jose, building_01, floor_01
${MAP_FILE_NAME}                 auto_location_f01_1654845780826.tar.gz
${NW_POLICY_NAME}               ad_onprem_nwp
${SSID_NAME}                    ad_onprem_ssid
${WIPS_POLICY_NAME}             ad_onprem_wips
${BUILDING_NAME}                building_01
${UUID}                     123e4567-e89b-12d3-a456-426655440020
${CLIENT_MAC_FORMAT}               54:8d:5a:69:3c:5a
${AP2_SERIAL}                       24602001170028
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
    [Documentation]         Test Suite Clean Up: Reset Customer Account Data

    ${LOGIN_XIQ}=                   Login User          ${TENANT_USERNAME1}     ${TENANT_PASSWORD1}
    ${RESET_VIQ_DATA}=               Reset VIQ Data
    Should Be Equal As Strings      '${RESET_VIQ_DATA}'              '1'
    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

*** Test Cases ***
Test1: Configure on-prem ADSP ip address in WIPS profile
    [Documentation]         Configure on-prem ADSP ip address in WIPS profile - when ADEss is not subscribed
    [Tags]                  tccs_13263        testbed_adsp        development
     Login User                      ${TENANT_USERNAME1}     ${TENANT_PASSWORD1}
    ${CREATE_POLICY1} =              Create Network Policy               ${NW_POLICY_NAME}        ${ADESS_NWP}
    Should Be Equal As Strings      '${CREATE_POLICY1}'   '1'
    ${CREATE_AP_TEMPLATE}=           Add AP Template     ${ap2.model}     ${ap2.template_onprem}    ${AP_TEMPLATE_CONFIG}
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
    ${ONPREM_CONFIG}=       Wips onprem adsp serverip configuration on Network Policy  ${NW_POLICY_NAME}  ${WIPS_POLICY_NAME}  enable  &{ON_PREM_ADSP_SERVER_IP_CONFIG}
    Should Be Equal As Strings       '${ONPREM_CONFIG}'   '1'
    Onboard AP                       ${ap2.serial}       aerohive       ${LOCATION}
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
    [Teardown]   run keywords        Logout User
    ...                              Quit Browser

Test2: validate on-prem adsp command in ap cli -the sensor reports to ADSP as online
    [Documentation]         validate on-prem adsp command in ap cli -the sensor reports to ADSP as online - when ADESS is NOT subscribed
    [Tags]                  tccs_13264     testbed_adsp             development
    Depends On              Test1
    ${AP_SPAWN}=                     open spawn       ${ap2.ip}      ${ap2.port}   ${ap2.username}     ${ap2.password}        ${ap2.platform}
    Set Suite Variable               ${AP_SPAWN}
    ${SENSOR_WIFI_CONFIG}=           send commands             ${AP_SPAWN}         show running-config | include "interface wifi2"
    Should Contain                   ${SENSOR_WIFI_CONFIG}      interface wifi2 mode adsp-sensor
    ${CONFIG1}=                      send commands               ${AP_SPAWN}         show adsp-server status
    Should Contain                   ${CONFIG1}          Server 1: ${ONPREM_ADSP_SERVER_IP}  Port: ${ONPREM_ADSP_SERVER_SENSOR_PORT}
    Should Contain                   ${CONFIG1}          status: online
    log to report                    Config of adsp server ${CONFIG1}
    Close Spawn                      ${AP_SPAWN}

Test3: Sensor sends feeds to on-prem adsp even if it disconnects from XIQ
    [Documentation]         HOS sensor sends the feeds to on-prem ADSP, eventhough it lost connection to XIQ via unmanage action - When ADEss is not subscribed
    [Tags]                  tccs_13311          testbed_adsp            development
     Depends On              Test5

    Login User                      ${TENANT_USERNAME1}     ${TENANT_PASSWORD1}
    change manage device status       UNMANAGE                  ${ap2.serial}

    sleep   60s

    ${AP_SPAWN}=                     open spawn        ${ap2.ip}   ${ap2.port}   ${ap2.username}      ${ap2.password}       ${ap2.platform}
    ${SENSOR_WIFI_CONFIG}=           send commands             ${AP_SPAWN}         show running-config | include "interface wifi2"
    Should Contain                   ${SENSOR_WIFI_CONFIG}      interface wifi2 mode adsp-sensor


    ${CONFIG1}=                      send commands               ${AP_SPAWN}         show adsp-server status
    Should Contain                   ${CONFIG1}          Server 1: ${ONPREM_ADSP_SERVER_IP}  Port: ${ONPREM_ADSP_SERVER_SENSOR_PORT}
    Should Contain                   ${CONFIG1}          status: online

    log to report                    Config of adsp server ${CONFIG1}

    ${ONPREM_ADSP_SENSOR_MAC} =      convert mac to colon Format  ${ap2.mac}
    ${ADSP_SPAWN}=                   open spawn      ${ONPREM_ADSP_SERVER_IP}  ${ONPREM_ADSP_SERVER_SSH_PORT}  ${ONPREM_ADSP_CLI_USERNAME}  ${ONPREM_ADSP_CLI_PASSWORD}   ${ONPREM_ADSP_PLATFORM}
    ${TOT_RXMSGS_STRING}=             send commands with comma  ${ADSP_SPAWN}    eql "select mac(MAC),tot_txmsgs,tot_txmsgs_bits,tot_rxmsgs,tot_rxmsgs_bits from sensor where mac(MAC)='${ONPREM_ADSP_SENSOR_MAC}'" | grep ${ONPREM_ADSP_SENSOR_MAC} | awk '{ print $5 }'

     ${TEMP_LIST_TOT_RXMSGS_STRING}=  split string  ${TOT_RXMSGS_STRING}   \\n

     ${TOT_RXMSG_COUNT}=              set variable  ${TEMP_LIST_TOT_RXMSGS_STRING}[0]
      sleep  75s
     ${TOT_RXMSGS_STRING_1}=            send commands with comma     ${ADSP_SPAWN}    eql "select mac(MAC),tot_txmsgs,tot_txmsgs_bits,tot_rxmsgs,tot_rxmsgs_bits from sensor where mac(MAC)='${ONPREM_ADSP_SENSOR_MAC}'" | grep ${ONPREM_ADSP_SENSOR_MAC} | awk '{ print $5 }'

     ${TEMP_LIST_TOT_RXMSGS_STRING_1}=  split string   ${TOT_RXMSGS_STRING_1}   \\n

     ${TOT_RXMSG_COUNT_1}=              set variable  ${TEMP_LIST_TOT_RXMSGS_STRING_1}[0]
     Should Be True             $TOT_RXMSG_COUNT_1 > $TOT_RXMSG_COUNT

     close spawn     ${ADSP_SPAWN}
     NAVIGATE TO DEVICES
    change manage device status       MANAGE           ${ap2.serial}
    sleep  20s
    ${AP_SPAWN}=                     open spawn       ${ap2.ip}      ${ap2.port}   ${ap2.username}     ${ap2.password}        ${ap2.platform}
    ${OUTPUT0}=                      Send Commands       ${AP_SPAWN}    no capwap client enable, capwap client enable, save config
    sleep  60s
    Wait Until Device Online         ${ap2.serial}
    close spawn                      ${AP_SPAWN}
    [Teardown]   run keywords        Logout User
   ...                              Quit Browser

Test4: Verify backup viq
    [Documentation]      Check the viq backup
    [Tags]                 tccs_13260    testbed_adsp      development
      ${result1}=         login user  ${TENANT_USERNAME2}   ${TENANT_PASSWORD2}
                        Should Be Equal As Strings      '${result1}'     '1'
     ${BKUP_VIQ}=           backup viq data
     Should Be Equal As Strings      '${BKUP_VIQ}'              '1'
    [Teardown]        run keywords    logout user
     ...                               QUIT BROWSER