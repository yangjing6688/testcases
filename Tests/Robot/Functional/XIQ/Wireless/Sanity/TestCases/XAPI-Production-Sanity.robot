# Author        : Subramani R
# Date          : 18 July 2022
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
${AP_DEVICE_ID_NEW}             0
${NETWORK_POLICY_ID}=           0
${nw_policy}                    test_nw_01
${location_name}                BLR1
${building_name}                EcoSpace1
${building_address}             ORR
${floor_name}                   floor2

*** Settings ***
Force Tags  testbed_3_node

Library     common/Xapi.py
Library     extauto/common/Cli.py
Library     common/TestFlow.py
Library     common/Utils.py


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
    Log    Checking the Access Token not equal to -1
    skip if     '${ACCESS_TOKEN}' == '-1'



Test Suite Clean Up
    [Documentation]    delete devices, topologies, created network policies

    [Tags]           tccs_7267	production  cleanup

#Delete Device

    #The below 2 lines will be uncommented, and AP_DEVICE_ID will be modified to AP_DEVICE_ID_NEW, once the device reset portion is uncommented (see Test Cases section), https://jira.extremenetworks.com/browse/AIQ-1997
    #skip if   ${AP_DEVICE_ID_NEW}==0
    #${DELETE_RESP}=              xapi delete device        ${AP_DEVICE_ID_NEW}
    ${DELETE_RESP}=              xapi delete device        ${AP_DEVICE_ID}
    Log    Validating the Successful Delete of Device
    Should Be Equal As Integers      ${DELETE_RESP}       1


#Delete Floor
    skip if   ${FLOOR_ID}==0
    xapi delete floor     ${FLOOR_ID}
    ${LOCATIONS_TREE_STRING}=         xapi get locations tree string
    Log    Validating the Floor has been deleted successfully
    should not contain                ${LOCATIONS_TREE_STRING}            ${floor_name}


#Delete Building
    skip if   ${BUILDING_ID}==0
    xapi delete building     ${BUILDING_ID}
    ${LOCATIONS_TREE_STRING}=         xapi get locations tree string
    Log    Validating the Building has been deleted successfully
    should not contain                ${LOCATIONS_TREE_STRING}            ${building_name}


#Delete Location
    skip if   ${LOCATION_ID}==0
    xapi delete location    ${LOCATION_ID}
    ${LOCATIONS_TREE_STRING}=         xapi get locations tree string
    Log    Validating the Location has been deleted successfully
    should not contain                ${LOCATIONS_TREE_STRING}            ${location_name}


#Delete Network Policy
    skip if   ${NETWORK_POLICY_ID}==0
    skip if   ${NETWORK_POLICY_ID}==-1
    skip if   ${NETWORK_POLICY_ID}==''
    skip if   ${NETWORK_POLICY_ID}=='None'
    ${NW_POLICY_DELETE_RESP}=            xapi delete network policy  ${NETWORK_POLICY_ID}
    log                     ${NW_POLICY_DELETE_RESP}

    Log    Validating the Network Policy Delete
    Should Be Equal As Integers      ${NW_POLICY_DELETE_RESP}       1

    ${NW_POLICY_LIST_RESP}=  xapi list network policies
    ${NEW_COUNT}=  get json values  ${NW_POLICY_LIST_RESP}  key=total_count

    ${new_count}=           evaluate                  ${NETWORK_POLICY_COUNT} - 1
    Log    Validating the count of network poicies to be reduced by one
    should be equal as integers     ${NEW_COUNT}        ${new_count}

    [Teardown]
    ${REVOKE_TOKEN}=         xapi logout        ${ACCESS_TOKEN}
    Log    Validating the Successful Access Token Logout
    Should Be Equal As Strings      ${REVOKE_TOKEN}       1

*** Test Cases ***

TCCS-7267: XAPI Onboard Extreme-Aerohive AP , Assign Location and Assign Network Policy and Push Config
    [Documentation]         XAPI Production Sanity Automation - NG XAPI - Onboard Extreme-Aerohive AP , Assign Location and Assign Network Policy and Push Config

    [Tags]                  tccs_7267     production

#Device Onboard

    ${DEVICE_ONBOARD}=               xapi ap device onboard      ${ap1.serial}
    Log    Validating the Successful Device Onboard
    Should Be Equal As Integers          ${DEVICE_ONBOARD}       1
    sleep    ${device_onboarding_wait}

    configure_device_to_connect_to_cloud    ${ap1.cli_type}  ${ap1.ip}  ${ap1.port}  ${ap1.username}   ${ap1.password}    ${server_name}


#Get Device ID

    ${AP_DEVICE_ID}=            xapi list and get device id     ${ap1.serial}
    skip if   ${AP_DEVICE_ID}==0
    skip if   ${AP_DEVICE_ID}==-1
    set suite variable         ${AP_DEVICE_ID}


#Get Root Location ID

    ${ROOT_LOCATION_ID}=    xapi get root location id
    set suite variable     ${ROOT_LOCATION_ID}


#Create Topoloy - Location

    skip if   ${ROOT_LOCATION_ID}==0
    skip if   ${ROOT_LOCATION_ID}==-1
    skip if   ${ROOT_LOCATION_ID}==''
    skip if   ${ROOT_LOCATION_ID}=='None'
    ${LOCATION_ID}=         xapi create location    ${ROOT_LOCATION_ID}    ${location_name}
    ${RESPONSE}=            xapi get locations tree string
    should contain          ${RESPONSE}             ${location_name}

    set suite variable      ${LOCATION_ID}


#Create Topoloy - Building

    skip if   ${LOCATION_ID}==0
    skip if   ${LOCATION_ID}==-1
    skip if   ${LOCATION_ID}==''
    skip if   ${LOCATION_ID}=='None'
    ${BUILDING_ID}=         xapi create building    ${LOCATION_ID}    ${building_name}     ${building_address}
    ${RESPONSE}=            xapi get locations tree string
    should contain          ${RESPONSE}             ${building_name}
    set suite variable      ${BUILDING_ID}


#Create Topoloy - Floor

    skip if   ${BUILDING_ID}==0
    skip if   ${BUILDING_ID}==-1
    skip if   ${BUILDING_ID}==''
    skip if   ${BUILDING_ID}=='None'
    ${FLOOR_ID}=            xapi create floor    ${BUILDING_ID}    ${floor_name}
    ${RESPONSE}=            xapi get locations tree string
    should contain          ${RESPONSE}             ${floor_name}
    set suite variable      ${FLOOR_ID}


#Check Connected Status of Device(s)

    ${AP_CONNECTED_STATE}=      XAPI Wait Until Device Online              ${ap1.serial}        30      10
    skip if   ${AP_CONNECTED_STATE}=='false'


#Assign Location To AP Device
    skip if   ${FLOOR_ID}==0
    skip if   ${FLOOR_ID}==-1
    skip if   ${FLOOR_ID}==''
    skip if   ${FLOOR_ID}=='None'
    ${RESPONSE}=       xapi assign location to device         ${AP_DEVICE_ID}       ${FLOOR_ID}
    Log    Validating the Successful Assign of Location to Device
    should be equal as integers             ${RESPONSE}         1


#Create Network-Policy

    ${RESP}=  xapi create network policy        '{"name" : "${nw_policy}", "type" : "NETWORK_ACCESS_AND_SWITCHING", "description" : "test network policy for network access and switch"}'
    ${NETWORK_POLICY_ID}=  get json values  ${RESP}  key=id
    set suite variable      ${NETWORK_POLICY_ID}

    ${RESP_LIST}=  xapi list network policies
    ${NETWORK_POLICY_COUNT}=  get json values  ${RESP_LIST}  key=total_count
    set suite variable      ${NETWORK_POLICY_COUNT}


#Assign network policy to device

    skip if   ${NETWORK_POLICY_ID}==0
    skip if   ${NETWORK_POLICY_ID}==-1
    skip if   ${NETWORK_POLICY_ID}==''
    skip if   ${NETWORK_POLICY_ID}=='None'
    sleep       ${device_onboarding_wait}
    ${ASSIGN_NW_POLICY}=                xapi assign network policy to a device      ${AP_DEVICE_ID}     ${NETWORK_POLICY_ID}

    Log    Validating the Successful Assign of Network Policy
    Should Be Equal As Integers          ${ASSIGN_NW_POLICY}      1


#Push configuration and upgrade firmware

    ${AP_CONNECTED_STATE}=      XAPI Wait Until Device Online              ${ap1.serial}        30      10
    skip if     ${AP_CONNECTED_STATE}=='false'

	${PUSH_CONFIG}=               xapi push config      ${AP_DEVICE_ID}
	Log    Validating the Successful Config Push to Device
    Should Be Equal As Integers      ${PUSH_CONFIG}       1


#Get Configuration Deployment Status

    sleep   30s
    ${CONFIG_DEPLOY_STATUS}=                xapi configuration push deployment status    ${AP_DEVICE_ID}
    Log    Retrieving the Config Push Status
    Should Be Equal As Strings              '${CONFIG_DEPLOY_STATUS}'   'True'

#The Reset Device section and Get AP Device Details Post Device Reset Section are commented due to  - https://jira.extremenetworks.com/browse/AIQ-1997

# Reset Device - Run Device Factory Reset API request on AH-AP

    #${AP_CONNECTED_STATE}=      XAPI Wait Until Device Online              ${ap1.serial}        30      10
    #skip if     ${AP_CONNECTED_STATE}=='false'

    #${RESP}=  xapi reset device    ${AP_DEVICE_ID}
    #Log    Validatign the successful device reset
    #should be equal as integers     ${RESP}     1


#Get AP Device Details Post Reset

#    sleep       10s

    #${AP_DEVICE_ID_NEW}=            xapi list and get device id     ${ap1.serial}
    #set suite variable         ${AP_DEVICE_ID_NEW}

    #${AP_DEVICE_ADMIN_STATE}=        xapi list device admin state    ${ap1.serial}
    #Log    Getting the device admin state post device reset
    #Should Be Equal As Strings      '${AP_DEVICE_ADMIN_STATE}'   'NEW'

    #${AP_NW_POLICY_NAME}=            xapi list device network policy name    ${ap1.serial}
    #Log    Getting the Network Policy Name for the the device and validating it to be empty
    #Should Be Equal As Strings      '${AP_NW_POLICY_NAME}'   ''
