# Author        : hshivanagi
# Date          : Sep 2020
# Description   : XAPI Presence

# Topology      :
# Client -----> AP --->XIQ Instance
################## PRE-CONDITION ########################
# 1. AP should be onboarded and it is online
# 2. start the remote srevre in MU. Starting remote server on MU refer testsuite/xiq/config/remote_server_config.txt
# 3. Start the stand alone selenium server on MU refer:testsuite/xiq/config/remote_server_config.txt
# 4. Required Device: 1 AP, 1 Windows10 MU

# Execution Command:
# robot -L INFO -v DEVICE:AP630 -v TOPO:g7r2  xapi_presence.robot
# Select the "TOPO" and "DEVICE" variable based on Test bed


*** Variables ***
# client secret, client id and redirect url are fixed *** variables ***
# Follow the https://aerohive.qtestnet.com/p/81669/portal/project#tab=testdesign&object=1&id=44426991 steps for more info
${CLIENT_SECRET}        612bc06113b40581b499d0ee296b536a
${CLIENT_ID}            f3c507e5
${XAPI_NW}              XAPI_NW
${XAPI_SSID}            XAPI_AUTO_SSID
${LOCATION}             Santa Clara, building_02, floor_03
${PAGE_TITLE}           End-to-End Cloud Driven Networking Solutions - Extreme Networks

*** Settings ***
Library     common/Rest.py
Library     common/Utils.py
Library     common/TestFlow.py

# The keywords in Login.py have been moved to the keywords directory.
# If the moved keyword is not working correctly import the original library and remove the keywords/gui/login/KeywordsLogin.py version.
#Library     xiq/flows/common/Login.py
Library     keywords/gui/login/KeywordsLogin.py
Library     xiq/flows/common/MuCaptivePortal.py
Library     xiq/flows/configure/CommonObjects.py

Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/Location.py
Library     xiq/flows/globalsettings/GlobalSetting.py
Library     xiq/flows/configure/NetworkPolicy.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml

Resource     Tests/Robot/Functional/XIQ/Wireless/Sanity/Resources/xapi_presence_config.robot

Force Tags   testbed_1_node

Library	         Remote 	http://${mu1.ip}:${mu1.port}   WITH NAME   MU1
Suite Setup      Pre Condition
Suite Teardown   Test Suite Clean Up

*** Keywords ***
Connect Open Wireless Network
    [Arguments]    ${NETWORK}
    ${CONNECT_STATUS}=           MU1.connect_open_network    ${NETWORK}
    should be equal as strings  '${CONNECT_STATUS}'              '1'
    sleep                        ${client_connect_wait}

    ${URL_TITLE}=                 Check Internet Connectivity    ${mu1.ip}
    should be equal as strings   '${URL_TITLE}'                 '${PAGE_TITLE}'

    ${START_TIME}=                get_utc_iso_time_format
    set global variable           ${START_TIME}

Pre Condition
    [Documentation]   AP Should be onboarded  and it is online
    ${result}=                      Login User        ${tenant_username}     ${tenant_password}

    ${base_url}=                    Get Base Url Of Current Page
    set global variable             ${base_url}

    ${AP_STATUS}=                   get device status     device_mac=${ap1.mac}
    Should Be Equal As Strings     '${AP_STATUS}'     'green'

    ${ASSIGN_LOC}=                  Assign Location With Device Actions    ${ap1.serial}    ${LOCATION}
    ${OWNER_ID}=                    Get Viq Id
    set global variable             ${OWNER_ID}

    Create Network Policy           OPEN_AUTO               ${DEFAULT_NETWORK}

    Create Network Policy           ${XAPI_NW}              ${XAPI_NETWORK}
    Enable Nw Presence Analytics    ${XAPI_NW}

    Update Network Policy To Ap     policy_name=XAPI_NW      ap_serial=${ap1.serial}
    Sleep                           ${config_push_wait}
    Sleep                           180
    Connect Open Wireless Network   ${XAPI_SSID}

    [Teardown]  run keywords        logout user
     ...                            quit browser

Test Suite Clean Up
    [Documentation]    cleaning the createst SSID

    ${result}=    Login User       ${tenant_username}        ${tenant_password}
    Update Network Policy To Ap     policy_name=OPEN_AUTO      ap_serial=${ap1.serial}
	Delete Device                 device_serial=${ap1.serial}

    delete network policy         ${XAPI_NW}
    delete ssid                   ${XAPI_SSID}
    Delete Api Access Tokens

    [Teardown]   run keywords     logout user
    ...                           quit browser
    
*** Test Cases ***
TCCS-7472_Step1: Get The Autherization Code
     [Documentation]   generate auterization code

     [Tags]            production   tccs_7472_step1     tccs_7472
     ${AUTH_CODE}=         Generate Auth Code    ${test_url}   ${CLIENT_ID}     ${tenant_username}      ${tenant_password}
     set global variable   ${AUTH_CODE}


TCCS-7472_Step2: Get Access Token And Refresh Token
     [Documentation]   generate the access and extract access token and refresh token from json data

     [Tags]            production   tccs_7472_step2     tccs_7472

     depends on             tccs_7472_step1
     ${JSON_DATA}=          Generate Access Token                    ${AUTH_CODE}    ${CLIENT_SECRET}    ${CLIENT_ID}   ${test_rdc_url}

     ${ACCESS_TOKEN}=       Get Value From Gen Access Token Resp     ${JSON_DATA}    ${OWNER_ID}         accessToken
     set global variable    ${ACCESS_TOKEN}

     ${REFRESH_TOKEN}=      Get Value From Gen Access Token Resp     ${JSON_DATA}    ${OWNER_ID}        refreshToken
     set global variable    ${REFRESH_TOKEN}

TCCS-7472_Step3: Validate The Access Token In Xiq Global Settings
     [Documentation]   Validate the access token with automatically updated token in API Token Management

     [Tags]            production   tccs_7472_step3     tccs_7472

     depends on                     tccs_7472_step2
     ${RESULT}=                     Login User        ${tenant_username}      ${tenant_password}
     should be equal as strings    '${RESULT}'             '1'

     ${TOKEN_DETAILS}=              Get Api Access Token Details    ${ACCESS_TOKEN}

     should be equal as strings     '${TOKEN_DETAILS}[Access Token]'     '${ACCESS_TOKEN}'
     should be equal as strings     '${TOKEN_DETAILS}[Refresh Token]'    '${REFRESH_TOKEN}'

     [Teardown]  run keywords    logout user
     ...                         quit browser


TCCS-7472_Step4: API Call To Get The Device IDs
     [Documentation]   API call to get the device id's

     [Tags]            production   tccs_7472_step4     tccs_7472

     depends on             tccs_7472_step3
     ${API_RESP}=           xapi_get_method   ${base_url}/xapi/v1/monitor/devices?ownerId=${OWNER_ID}     ${CLIENT_SECRET}   ${CLIENT_ID}   ${ACCESS_TOKEN}

     ${DEVICE_ID}=          get_data_from_api_resp    ${API_RESP}    ${ap1.mac}  deviceId
     set global variable    ${DEVICE_ID}

TCCS-7472_Step5: Get The Locationid Of The Device
     [Documentation]   API call to get the device Location id

     [Tags]            production   tccs_7472_step5     tccs_7472

     depends on            tccs_7472_step4
     ${API_RESP}=          xapi_get_method   ${base_url}/xapi/v1/monitor/devices/${DEVICE_ID}?ownerId=${OWNER_ID}     ${CLIENT_SECRET}   ${CLIENT_ID}   ${ACCESS_TOKEN}
     ${LOCATION_ID}=       get_location_id_from_api_resp      ${API_RESP}
     set global variable   ${LOCATION_ID}

#   Commenting the test case based on AIQ-1601
#TCCS-7472_Step6: Get The Presence Information Of Client
#     [Documentation]   API call to get Presence of client
#
#     [Tags]            production   tccs_7472_step6
#
#     depends on            tccs_7472_step5
#     ${CURRENT_DATE}=      Get Current Date
#     ${START_HOUR}         Set Variable           T00:01:00.000
#     ${END_HOUR}           Set Variable           T23:59:00.000
#     LOG TO CONSOLE         ${CURRENT_DATE}${START_HOUR}
#     LOG TO CONSOLE         ${CURRENT_DATE}${END_HOUR}
#     sleep                 5 minutes
#     ${PRESENCE_RESP}=     xapi_get_method     ${base_url}/xapi/v2/clientlocation/clientpresence?ownerId=${OWNER_ID}&location=${LOCATION_ID}&startTime=${CURRENT_DATE}${START_HOUR}Z&endTime=${CURRENT_DATE}${END_HOUR}Z&timeUnit=FiveMinutes
#
#     ...                   ${CLIENT_SECRET}   ${CLIENT_ID}   ${ACCESS_TOKEN}
#
#     ${CLIENT_MAC}=        Get Presence Of Client From Api Response     ${PRESENCE_RESP}    ${mu1.wifi_mac}     clientMacAddress
#     should be equal as strings     '${CLIENT_MAC}'     '${mu1.wifi_mac}'
#
#     [Teardown]   run keywords     MU1.disconnect_wifi
#     ...          AND              MU1.delete_wlan_profile   ${XAPI_SSID} 
