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

Library     xiq/flows/common/Login.py
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

Resource     ../Resources/xapi_presence_config.robot

Force Tags   flow5

Library	         Remote 	http://${mu1.ip}:${mu1.port}   WITH NAME   MU1
Suite Setup      Pre Condition

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

    ${${base_url}}=                    Get Base Url Of Current Page
    set global variable             ${${base_url}}

    ${AP_STATUS}=                   Get AP Status     ap_mac=${ap1.mac}
    Should Be Equal As Strings     '${AP_STATUS}'     'green'

    ${ASSIGN_LOC}=                  Assign Location With Device Actions    ${ap1.serial}    ${LOCATION}
    ${OWNER_ID}=                    Get Viq Id
    set global variable             ${OWNER_ID}

    Create Network Policy           OPEN_AUTO               &{DEFAULT_NETWORK}

    Create Network Policy           ${XAPI_NW}              &{XAPI_NETWORK}
    Enable Nw Presence Analytics    ${XAPI_NW}

    Update Network Policy To Ap     policy_name=XAPI_NW      ap_serial=${ap1.serial}
    Sleep                           ${config_push_wait}
    Sleep                           180
    Connect Open Wireless Network   ${XAPI_SSID}

    [Teardown]  run keywords        logout user
     ...                            quit browser

*** Test Cases ***
Test1 Step1: Get The Autherization Code
     [Documentation]   generate auterization code
     [Tags]            XAPI    P1     production
     ${AUTH_CODE}=         Generate Auth Code    ${test_url}   ${CLIENT_ID}     ${tenant_username}      ${tenant_password}
     set global variable   ${AUTH_CODE}


Test1 Step2: Get Access Token And Refresh Token
     [Documentation]   generate the access and extract access token and refresh token from json data
     [Tags]            XAPI    P1     production

     depends on             Test1 Step1
     ${JSON_DATA}=          Generate Access Token                    ${AUTH_CODE}    ${CLIENT_SECRET}    ${CLIENT_ID}   ${test_url}

     ${ACCESS_TOKEN}=       Get Value From Gen Access Token Resp     ${JSON_DATA}    ${OWNER_ID}         accessToken
     set global variable    ${ACCESS_TOKEN}

     ${REFRESH_TOKEN}=      Get Value From Gen Access Token Resp     ${JSON_DATA}    ${OWNER_ID}        refreshToken
     set global variable    ${REFRESH_TOKEN}

Test1 Step3: Validate The Access Token In Xiq Global Settings
     [Documentation]   Validate the access token with automatically updated token in API Token Management
     [Tags]            XAPI    P1     production

     depends on                     Test1 Step2
     ${RESULT}=                     Login User        ${tenant_username}      ${tenant_password}
     should be equal as strings    '${RESULT}'             '1'

     ${TOKEN_DETAILS}=              Get Api Access Token Details    ${ACCESS_TOKEN}

     should be equal as strings     '${TOKEN_DETAILS}[Access Token]'     '${ACCESS_TOKEN}'
     should be equal as strings     '${TOKEN_DETAILS}[Refresh Token]'    '${REFRESH_TOKEN}'

     [Teardown]  run keywords    logout user
     ...                         quit browser


Test1 Step4: API Call To Get The Device IDs
     [Documentation]   API call to get the device id's
     [Tags]            XAPI    P1     production

     depends on             Test1 Step2
     ${API_RESP}=           xapi_get_method   ${${base_url}}/xapi/v1/monitor/devices?ownerId=${OWNER_ID}     ${CLIENT_SECRET}   ${CLIENT_ID}   ${ACCESS_TOKEN}

     ${DEVICE_ID}=          get_data_from_api_resp    ${API_RESP}    ${ap1.mac}  deviceId
     set global variable    ${DEVICE_ID}

Test1 Step5: Get The Locationid Of The Device
     [Documentation]   API call to get the device Location id
     [Tags]            XAPI    P1     production

     depends on            Test1 Step4
     ${API_RESP}=          xapi_get_method   ${${base_url}}/xapi/v1/monitor/devices/${DEVICE_ID}?ownerId=${OWNER_ID}     ${CLIENT_SECRET}   ${CLIENT_ID}   ${ACCESS_TOKEN}
     ${LOCATION_ID}=       get_location_id_from_api_resp      ${API_RESP}
     set global variable   ${LOCATION_ID}

Test1 Step6: Get The Presence Information Of Client
     [Documentation]   API call to get Presence of client
     [Tags]            XAPI    P1     production

     depends on            Test1 Step5
     sleep                 5 minutes
     ${END_TIME}=          get_utc_iso_time_format
     ${PRESENCE_RESP}=     xapi_get_method     ${${base_url}}/xapi/v2/clientlocation/clientpresence?ownerId=${OWNER_ID}&location=${LOCATION_ID}&startTime=${START_TIME}Z&endTime=${END_TIME}Z&timeUnit=FiveMinutes
     ...                   ${CLIENT_SECRET}   ${CLIENT_ID}   ${ACCESS_TOKEN}

     ${CLIENT_MAC}=        Get Presence Of Client From Api Response     ${PRESENCE_RESP}    ${mu1.wifi_mac}     clientMacAddress
     should be equal as strings     '${CLIENT_MAC}'     '${mu1.wifi_mac}'

     [Teardown]   run keywords     MU1.disconnect_wifi
     ...          AND              MU1.delete_wlan_profile   ${XAPI_SSID}

Test Suite Clean Up
    [Documentation]    cleaning the createst SSID
    [Tags]    XAPI    P1     production

    ${result}=    Login User       ${tenant_username}        ${tenant_password}
    Update Network Policy To Ap     policy_name=OPEN_AUTO      ap_serial=${ap1.serial}

    delete network policy         ${XAPI_NW}
    delete ssid                   ${XAPI_SSID}
    Delete Api Access Tokens

    [Teardown]   run keywords     logout user
    ...                           quit browser