# Author        : Subramani R
# Date          : 31 May 2022
# Description   : NG-XAPI - Test Suite for testing the new xapi for Aerohive AP models. 

# Topology:
# ---------
#    ScriptHost
#      |________
#      |        |
#     Cloud     AP
# Pre-config:
# -----------
#
#

# Execution Command:
# ------------------
# robot -v TOPO:topo.xapi-g2.yaml -v TESTBED:BANGALORE/testbed_all_SubramaniVR.yaml -L DEBUG XAPI-Production-Sanity.robot
#
#


*** Variables ***

${AP_DEVICE_ID}                 0
${SWITCH_DEVICE_ID}             0
${ERROR_CODE}                   error_code
${API_RESPONSE}                 200 OK
${NETWORK_POLICY_ID}=           -1
${location}                     Bangalore, EcoSpace-Bellandur, Floor-1
${nw_policy}                    test_nw_01
${location_name}                BLR1
${building_name}                EcoSpace1
${building_address}             ORR
${floor_name}                   floor2

*** Settings ***
Force Tags  testbed_3_node

Library     common/Xapi.py
Library     common/Cli.py
Library     xiq/flows/common/Login.py
Library     xiq/flows/configure/CommonObjects.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/common/Navigator.py
Library     xiq/flows/extreme_location/ExtremeLocation.py
Library     xiq/flows/globalsettings/GlobalSetting.py
Library     xiq/flows/configure/AdditionalSettings.py

Library     common/TestFlow.py
Library     common/Utils.py

Library     xiq/flows/manage/Devices.py
Library     Collections


Resource    Tests/Robot/Libraries/XAPI/XAPI-Authentication-Keywords.robot
Resource    Tests/Robot/Libraries/XAPI/XAPI-Configuration-Deployment-Keywords.robot
Resource    Tests/Robot/Libraries/XAPI/XAPI-Network-Policy-Keywords.robot
Resource    Tests/Robot/Libraries/XAPI/XAPI-Device-Keywords.robot
Resource    Tests/Robot/Libraries/XAPI/XAPI-Location-Keywords.robot

Variables   Environments/Config/waits.yaml
Variables   TestBeds/${TESTBED}
Variables   Environments/${TOPO}


Suite Setup     Pre Condition
Suite Teardown  Test Suite Clean Up

*** Keywords ***
Pre Condition
    [Documentation]   Generate Access Token

    # generate the key once per suite

    ${ACCESS_TOKEN}=        generate_access_token    ${tenant_username}      ${tenant_password}      login
    set suite variable     ${ACCESS_TOKEN}
    Should Not Be Equal As Strings     '${ACCESS_TOKEN}'     '-1'

Test Suite Clean Up
    [Documentation]    delete devices, topologies, created network policies

    [Tags]           tccs_7267	production  cleanup

#Delete Device

    ${AP_DEVICE_ID_NEW}=            xapi list and get device id     ${ap1.serial}
    skip if   ${AP_DEVICE_ID_NEW}==0
    set suite variable         ${AP_DEVICE_ID_NEW}

    ${DELETE_RESP}=              xapi delete device        ${AP_DEVICE_ID_NEW}
    Should Be Equal As Strings      '${DELETE_RESP}'       '1'

#Delete Floor
    skip if   ${FLOOR_ID}==0
    xapi delete floor     ${FLOOR_ID}
    ${LOCATIONS_TREE_STRING}=         xapi get locations tree string
    should not contain                ${LOCATIONS_TREE_STRING}            ${floor_name}

#Delete Building
    skip if   ${BUILDING_ID}==0
    xapi delete building     ${BUILDING_ID}
    ${LOCATIONS_TREE_STRING}=         xapi get locations tree string
    should not contain                ${LOCATIONS_TREE_STRING}            ${building_name}

#Delete Location
    skip if   ${LOCATION_ID}==0
    xapi delete location    ${LOCATION_ID}
    ${LOCATIONS_TREE_STRING}=         xapi get locations tree string
    should not contain                ${LOCATIONS_TREE_STRING}            ${location_name}

#Delete Network Policy
    skip if   ${NETWORK_POLICY_ID}==0
    ${NW_POLICY_DELETE_RESP}=            xapi delete network policy  ${NETWORK_POLICY_ID}
    log                     ${NW_POLICY_DELETE_RESP}
    Should Be Equal As Strings      '${NW_POLICY_DELETE_RESP}'       '1'

    ${NW_POLICY_LIST_RESP}=  xapi list network policies
    ${NEW_COUNT}=  get json values  ${NW_POLICY_LIST_RESP}  key=total_count

    ${new_count}=           evaluate                  ${NETWORK_POLICY_COUNT} - 1
    should be equal as integers     ${NEW_COUNT}        ${new_count}

    [Teardown]
    ${REVOKE_TOKEN}=         xapi logout
    Should Be Equal As Strings      '${REVOKE_TOKEN}'       '1'

*** Test Cases ***

TCCS-7267: XAPI Onboard Extreme-Aerohive AP , Assign Location and Assign Network Policy and Push Config
    [Documentation]         XAPI Production Sanity Automation - NG XAPI - Onboard Extreme-Aerohive AP , Assign Location and Assign Network Policy and Push Config

    [Tags]                  tccs_7267     production

#Device Onboard

    ${DEVICE_ONBOARD}=               xapi device onboard      ${ap1.serial}
    Should Be Equal As Strings          '${DEVICE_ONBOARD}'       '1'
    sleep    ${device_onboarding_wait}

    ${AP_SPAWN}=                Open Spawn          ${ap1.ip}   ${ap1.port}      ${ap1.username}       ${ap1.password}        ${ap1.platform}
    Set Suite Variable          ${AP_SPAWN}
    Send Commands               ${AP_SPAWN}         no capwap client enable, no capwap client server, no capwap client server name, no capwap client server backup name, no capwap client default-server-name, capwap client server name ${capwap_url}, capwap client server backup name ${capwap_url}, capwap client default-server-name ${capwap_url}, capwap client enable, save config
    sleep    ${device_onboarding_wait}


#Get Device ID

    ${AP_DEVICE_ID}=            xapi list and get device id     ${ap1.serial}
    skip if   ${AP_DEVICE_ID}==0
    set suite variable         ${AP_DEVICE_ID}


#Get Root Location ID

    ${ROOT_LOCATION_ID}=    xapi get root location id
    set suite variable     ${ROOT_LOCATION_ID}


#Create Topoloy - Location

    skip if   ${ROOT_LOCATION_ID}=='None'
    ${LOCATION_ID}=         xapi create location    ${ROOT_LOCATION_ID}    ${location_name}
    ${RESPONSE}=            xapi get locations tree string
    should contain          ${RESPONSE}             ${location_name}
    set suite variable      ${LOCATION_ID}


#Create Topoloy - Building

    skip if   ${LOCATION_ID}==0
    ${BUILDING_ID}=         xapi create building    ${LOCATION_ID}    ${building_name}     ${building_address}
    ${RESPONSE}=            xapi get locations tree string
    should contain          ${RESPONSE}             ${building_name}
    set suite variable      ${BUILDING_ID}


#Create Topoloy - Floor

    skip if   ${BUILDING_ID}==0
    ${FLOOR_ID}=            xapi create floor    ${BUILDING_ID}    ${floor_name}
    ${RESPONSE}=            xapi get locations tree string
    should contain          ${RESPONSE}             ${floor_name}
    set suite variable      ${FLOOR_ID}

#Assign Location To Device

    FOR    ${i}    IN RANGE    30
        ${AP_CONNECTED_STATE}=                  xapi list device connected status         ${ap1.serial}
        Log      ${AP_CONNECTED_STATE}
        Exit For Loop If   '${AP_CONNECTED_STATE}'=='True'
        Log      ${i}
        sleep    ${device_onboarding_wait}

    END
    Log     ${AP_CONNECTED_STATE}
    Log    Exiting as Device is Conneceted

    skip if   ${AP_CONNECTED_STATE}=='false'
    skip if   ${FLOOR_ID}==0

    ${RESPONSE}=    xapi assign location to device         ${AP_DEVICE_ID}       ${FLOOR_ID}
    should be equal as integers             ${RESPONSE}         1


#Create Network-Policy

    ${RESP}=  xapi create network policy        '{"name" : "${nw_policy}", "type" : "NETWORK_ACCESS_AND_SWITCHING", "description" : "test network policy for network access and switch"}'
    ${NETWORK_POLICY_ID}=  get json values  ${RESP}  key=id
    set suite variable      ${NETWORK_POLICY_ID}

    ${RESP_LIST}=  xapi list network policies
    ${NETWORK_POLICY_COUNT}=  get json values  ${RESP_LIST}  key=total_count
    set suite variable      ${NETWORK_POLICY_COUNT}


#Assign network policy to device

    sleep       ${device_onboarding_wait}
    ${ASSIGN_NW_POLICY}=                xapi assign network policy to a device      ${AP_DEVICE_ID}     ${NETWORK_POLICY_ID}
    Should Be Equal As Strings          '${ASSIGN_NW_POLICY}'       '1'


#Push configuration and upgrade firmware

    FOR    ${i}    IN RANGE    30
        ${AP_CONNECTED_STATE}=                  xapi list device connected status         ${ap1.serial}
        Log      ${AP_CONNECTED_STATE}
        Exit For Loop If   '${AP_CONNECTED_STATE}'=='True'
        Log      ${i}
        sleep    ${device_onboarding_wait}

    END
    Log     ${AP_CONNECTED_STATE}
    Log    Exiting as Device is Conneceted


    skip if     ${AP_CONNECTED_STATE}=='false'

	${PUSH_CONFIG}=               xapi push config      ${AP_DEVICE_ID}
    Should Be Equal As Strings      '${PUSH_CONFIG}'       '1'


#Get Configuration Deployment Status

    sleep   30s
    ${CONFIG_DEPLOY_STATUS}=                xapi configuration push deployment status    ${AP_DEVICE_ID}
    Should Be Equal As Strings              '${CONFIG_DEPLOY_STATUS}'   'True'


# Reset Device - Run Device Factory Reset API request on AH-AP

    FOR    ${i}    IN RANGE    30
        ${AP_CONNECTED_STATE}=                  xapi list device connected status         ${ap1.serial}
        Log      ${AP_CONNECTED_STATE}
        Exit For Loop If   '${AP_CONNECTED_STATE}'=='True'
        Log      ${i}
        sleep    ${device_onboarding_wait}

    END
    Log     ${AP_CONNECTED_STATE}
    Log    Exiting as Device is Conneceted


    skip if     ${AP_CONNECTED_STATE}=='false'

    ${RESP}=  xapi reset device    ${AP_DEVICE_ID}
    should be equal as integers     ${RESP}     1


#Get AP Device Details Post Reset

    sleep       10s
    ${AP_DEVICE_ADMIN_STATE}=        xapi list device admin state    ${ap1.serial}
    Should Be Equal As Strings      '${AP_DEVICE_ADMIN_STATE}'   'NEW'

    ${AP_NW_POLICY_NAME}=            xapi list device network policy name    ${ap1.serial}
    Should Be Equal As Strings      '${AP_NW_POLICY_NAME}'   ''


