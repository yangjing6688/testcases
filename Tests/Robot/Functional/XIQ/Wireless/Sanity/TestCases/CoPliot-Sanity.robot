# Author        : Shrisha
# Date          : Aug24,2022
# Description   : Co-Pilot Wireless client Experience
#
# Topology      :
# AP1----- Cloud-----Ubuntu(MU1) or Windows MU

# Execution Command:
# ------------------
#  robot -v TESTBED:BANGALORE/Prod/wireless/adsptestbed1.yaml -v TOPO:topo.test.g2r1.xim.automation.yaml -v ENV:environment.adsp.remote.win10.chrome.yaml CoPilot-Sanity.robot

*** Variables ***
${LOCATION}                 auto_location_01, San Jose, building_01, floor_01
${NW_POLICY_NAME}           copilot_gf_policy
${SSID_NAME}                copilot_gf_sanity_ssid
${BUILDING_NAME}            building_01
${FLOOR_NAME}               floor_01
${MAP_FILE_NAME}            auto_location_01_1595321828282.tar.gz
${DURATION_OPTION}          Last 1 Hour
${VIEW_BY_LOCATION}         Location
${VIEW_BY_SSID}             SSID
${QUALITY_INDEX}            10
@{Quality_index_list}=                    5    6    7    8    9    10

${LOCATION_2}       Sant Clara
${BUILDING_NAME_2}            building_02
${BULDING_FLOOR_NAME_2_1}               floor_03
${BULDING_FLOOR_NAME_2_2}               floor_04


*** Settings ***
Library     Collections
Library     String
Library     Dialogs
Library     common/Utils.py
Library     common/Cli.py
Library     common/Mu.py
Library     common/TestFlow.py

Library     xiq/flows/common/Login.py
Library     xiq/flows/common/Navigator.py

Library     xiq/flows/extreme_location/ExtremeLocation.py
Library     xiq/flows/copilot/Copilot.py

Library     xiq/flows/manage/Client.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/Location.py

Library     xiq/flows/configure/Wips.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/configure/CommonObjects.py
Library     xiq/flows/configure/DeviceTemplate.py

Library     xiq/flows/globalsettings/GlobalSetting.py
Library     xiq/flows/mlinsights/Network360Plan.py
Library     xiq/flows/common/MuCaptivePortal.py

Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml
Resource     Tests/Robot/Functional/XIQ/Wireless/Sanity/Resources/extreme_copilot_sanity_config.robot
Library	     Remote   http://${mu1.ip}:${mu1.port}  WITH NAME   Remote_Server

Force Tags   testbed_1_node

#Suite Setup     Pre Condition
Suite Teardown  Test Suite Clean Up

*** Keywords ***
Test Suite Clean Up
    [Documentation]    delete created network policies,ssid

    [Tags]      sanity      cleanup
    ${result}=    Login User       ${tenant_username}     ${tenant_password}
    Remote_Server.Disconnect WiFi
    Delete Device  device_serial=${ap1.serial}
    Delete Network Polices         ${NW_POLICY_NAME}
    delete ap template profile     ${ap1.template_name}
    Delete ssids                   ${SSID_NAME}
    #delete_location_building_floor      ${LOCATION_2}    ${BUILDING_NAME_2}    ${BULDING_FLOOR_NAME_2_1}
    #delete_location_building_floor      ${LOCATION_2}    ${BUILDING_NAME_2}    ${BULDING_FLOOR_NAME_2_2}
    Logout User
    Quit Browser

*** Test Cases ***
TCCS-13495_Step1 : Login and Onboard AP on XIQ Account
    [Documentation]         Onboard AP to XIQ Account
    [Tags]                  tccs_13495    tccs_13495_step1    development

    ${LOGIN_XIQ}=               Login User          ${tenant_username}     ${tenant_password}

    #${IMPORT_MAP}=                Import Map In Network360Plan  ${MAP_FILE_NAME}
    #Should Be Equal As Strings    ${IMPORT_MAP}       1

    ${ONBOARD_RESULT}=      Onboard Device      ${ap1.serial}           ${ap1.cli_type}       location=${LOCATION}
    Should be equal as integers                 ${ONBOARD_RESULT}       1

    ${AP_SPAWN}=                Open Spawn          ${ap1.ip}       ${ap1.port}      ${ap1.username}       ${ap1.password}        ${ap1.cli_type}
    Set Suite Variable          ${AP_SPAWN}
    ${OUTPUT0}=                 Send Commands       ${AP_SPAWN}         capwap client server name ${capwap_url}, capwap client default-server-name ${capwap_url}, capwap client server backup name ${capwap_url}, no capwap client enable, capwap client enable, save config

    Wait Until Device Online    ${ap1.serial}

    Refresh Devices Page

    ${AP1_STATUS}=               Get AP Status       ap_mac=${ap1.mac}
    Should Be Equal As Strings  '${AP1_STATUS}'     'green'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

TCCS-13495_Step2 : Create Network policy and Attach Network policy to AP
    [Documentation]         Assign network policy to AP
    [Tags]                  tccs_13495    tccs_13495_step2    development
    Depends on      TCCS-13495_Step1
    ${LOGIN_XIQ}=                   Login User          ${tenant_username}     ${tenant_password}

    ${CREATE_POLICY1}=              Create Network Policy   ${NW_POLICY_NAME}      &{LOCATION_OPEN_NW}
    Should Be Equal As Strings      '${CREATE_POLICY1}'   '1'

    ${CREATE_AP_TEMPLATE}=          Add AP Template     ${ap1.model}    ${ap1.template_name}    &{AP_TEMPLATE_CONFIG}
    Should Be Equal As Strings      '${CREATE_AP_TEMPLATE}'   '1'

    ${AP1_UPDATE_CONFIG}=           Update Network Policy To AP   ${NW_POLICY_NAME}     ap_serial=${ap1.serial}   update_method=Complete
    Should Be Equal As Strings      '${AP1_UPDATE_CONFIG}'       '1'

    Wait Until Device Online    ${ap1.serial}

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

TCCS-13495_Step3 : Connect WIFI Client and sleep for 20 min
    [Documentation]         Connect wifi client
    [Tags]                  tccs_13495    tccs_13495_step3    development
    Depends on      TCCS-13495_Step2

    ${LOGIN_XIQ}=                  Login User          ${tenant_username}     ${tenant_password}

    Remote_Server.Connect Open Network    ${SSID_NAME}

    Log to Console      Sleep for ${client_connect_wait}
    sleep                         ${client_connect_wait}

    ${CLIENT_STATUS}=                Get Client Status   client_mac=${mu1.wifi_mac}
    Should Be Equal As Strings       '${CLIENT_STATUS}'      '1'

    Log to Console      Sleep for ${client_connect_wait}
    sleep                         ${client_connect_wait}

    ### It takes around 45 min to show up the first data
    Wait Until Device Online    ${ap1.serial}

    Refresh Devices Page
    sleep   600s

    Refresh Devices Page
    sleep   600s

    Refresh Devices Page
    sleep   600s

    Refresh Devices Page
    sleep   600s

    Refresh Devices Page
    sleep   600s

    Refresh Devices Page
    sleep   600s


    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

TCCS-13495_Step4: Verify wireless client experience quality index by location
    [Documentation]         Verify wireless client experience quality index by location
    [Tags]                  tccs_13495    tccs_13495_step4    development
    Depends on      TCCS-13495_Step3

    ${LOGIN_XIQ}=                  Login User          ${tenant_username}     ${tenant_password}

    ${return_Quality_Index_val}=     get wirless clientexp quality index by location    ${BUILDING_NAME}    ${VIEW_BY_LOCATION}    ${DURATION_OPTION}
    #${return_Quality_Index_val}=     get wirless clientexp quality index by ssid    ${SSID_NAME}    ${VIEW_BY_SSID}    ${DURATION_OPTION}
    #Should Be Equal As Strings      '${return_Quality_Index_val}'       '${QUALITY_INDEX}'
    should contain match    ${Quality_index_list}   ${return_Quality_Index_val}

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

