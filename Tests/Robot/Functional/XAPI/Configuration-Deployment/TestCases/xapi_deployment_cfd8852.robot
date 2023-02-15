# Author        : Kun Li
# Date          : 6 Feb 2023
# Description   : xapi sanity - device onboard, assign location, push configure and firmware ...
#               : cfd-8852, xapi update firmware does not work
#               : cfd fix version: 23r1.1

# Topology:
# ---------
#    ScriptHost/AutoIQ
#      |_________________
#      |        |       |
#     Cloud     AP1    AP2
# Pre-config:
# -----------
#
#
#
# Execution Command:
# ------------------
# robot -v ENV:environment.local.chrome.yaml -v TOPO:COATest/topo.test.aio.hz.148.yaml -v TESTBED:HANGZHOU/Dev/xiq_hz_tb2_ap550.yaml xapi_deployment_cfd8852.robot


*** Variables ***
${1st_LOCATION_ORG}          auto test org 1st
${1st_LOCATION_STREET}       auto test building 1st
${1st_LOCATION_CITY_STATE}   auto test location 1st
${1st_LOCATION_COUNTRY}      People's Republic of China (156)
${MAP_WIDTH}                 10
${MAP_HIGHT}                 10

${NON_LASTEST_BUILD}         10.0r10
${XAPI_NW_POLICY_NAME}       Auto_Xapi_nw_01
${XAPI_LOCATION_NAME}        Auto_Xapi_HZ
${XAPI_BUILDING_NAME}        Auto_Xapi_DLX
${XAPI_BUILDING_ADDRESS}     Auto_Xapi_Xueyuan
${XAPI_FLOOR_NAME}           Auto_Xapi_floor2

*** Settings ***

Library     Collections
Library     xiq/flows/extreme_location/ExtremeLocation.py
Library     xiq/flows/manage/Location.py
Library     extauto/common/Utils.py
Library     extauto/common/Screen.py
Library     extauto/common/Cli.py
Library     extauto/common/TestFlow.py
Library     extauto/xiq/flows/common/Login.py
Library     extauto/xiq/flows/common/Navigator.py
Library     extauto/xiq/flows/manage/Location.py
Library     extauto/xiq/flows/manage/Devices.py
Library     extauto/xiq/flows/configure/CommonObjects.py
Library     extauto/xiq/flows/configure/NetworkPolicy.py
Library     extauto/xiq/flows/globalsettings/GlobalSetting.py
Library     ExtremeAutomation/Imports/CommonObjectUtils.py
Library     ExtremeAutomation/Keywords/UserDefinedKeywords/NetworkElements/SetupTeardown/SetupTeardownUdks.py

Resource    Tests/Robot/Libraries/XAPI/XAPI-Device-Keywords.robot
Resource    Tests/Robot/Libraries/XAPI/XAPI-Configuration-Deployment-Keywords.robot
Resource    Tests/Robot/Libraries/XAPI/XAPI-Location-Keywords.robot
Resource    Tests/Robot/Libraries/XAPI/XAPI-Network-Policy-Keywords.robot


Variables   Environments/Config/waits.yaml
Variables   Environments/${TOPO}
Variables   Environments/${ENV}
Variables   TestBeds/${TESTBED}

Force Tags  testbed_2_node

Suite Setup     Test Suite Setup
Suite Teardown  Test Suite Clean Up

*** Keywords ***

Test Suite Setup
    [Documentation]  Suite setup.

    # login/logout the user, just generate the audit logs
    Login User  ${tenant_username}  ${tenant_password}

    # Generate xapi access token
    ${ACCESS_TOKEN}=  generate access token  ${tenant_username}  ${tenant_password}  login
    set suite variable   ${ACCESS_TOKEN}
    Log    Checking the Access Token not equal to -1, ACCESS_TOKEN=${ACCESS_TOKEN}
    skip if   '${ACCESS_TOKEN}' == '-1'

    # Create location building floor
    Create Test Location Building Floor

    # conver all ap or switch to device
    convert to generic device object  device  index=1  set_to_index=1
    convert to generic device object  device  index=2  set_to_index=2

    # Create the connection to the device(s)
    ${DEVICE1_SPAWN}=  Open Spawn  ${device1.ip}  ${device1.port}  ${device1.username}  ${device1.password}  ${device1.cli_type}
    ${DEVICE2_SPAWN}=  Open Spawn  ${device2.ip}  ${device2.port}  ${device2.username}  ${device2.password}  ${device2.cli_type}
    set suite variable  ${DEVICE1_SPAWN}
    set suite variable  ${DEVICE2_SPAWN}

    # Clean up devices
    ${DEVICE1_ID}=  xapi list and get device id  ${device1.serial}
    ${DEVICE2_ID}=  xapi list and get device id  ${device2.serial}
    Clean Up Device  device1  ${DEVICE1_ID}  ${DEVICE1_SPAWN}
    Clean Up Device  device2  ${DEVICE2_ID}  ${DEVICE2_SPAWN}

Test Suite Clean Up
    [Documentation]  Suite clean.

    Clean Up Device  device1  ${DEVICE1_ID}  ${DEVICE1_SPAWN}
    Clean Up Device  device2  ${DEVICE2_ID}  ${DEVICE2_SPAWN}
    Clean Up Test Location Building Floor
    Clean Up Test Network Policy

    [Teardown]   run keywords    Quit Browser

Clean Up Test Location Building Floor
    [Documentation]  Clean Up Test Location Building Floor

    #Delete Floor
    run keyword unless  '${FLOOR_ID}' == '0'  xapi delete floor   ${FLOOR_ID}
    ${LOCATIONS_TREE_STRING}=  xapi get locations tree string
    should not contain  ${LOCATIONS_TREE_STRING}   ${XAPI_FLOOR_NAME}

    #Delete Building
    run keyword unless  '${BUILDING_ID}' == '0'  xapi delete building   ${BUILDING_ID}
    ${LOCATIONS_TREE_STRING}=  xapi get locations tree string
    should not contain   ${LOCATIONS_TREE_STRING}   ${XAPI_BUILDING_NAME}

    #Delete Location
    run keyword unless   '${LOCATION_ID}' == '0'  xapi delete location   ${LOCATION_ID}
    ${LOCATIONS_TREE_STRING}=  xapi get locations tree string
    should not contain   ${LOCATIONS_TREE_STRING}   ${XAPI_LOCATION_NAME}

Clean Up Test Network Policy
    [Documentation]  Clean Up Test Network Policy

    #Delete Network Policy
    skip if   ${NETWORK_POLICY_ID}==0
    skip if   ${NETWORK_POLICY_ID}==-1
    skip if   ${NETWORK_POLICY_ID}==''
    skip if   ${NETWORK_POLICY_ID}=='None'
    xapi delete network policy  ${NETWORK_POLICY_ID}

    ${NW_POLICY_LIST_RESP}=  xapi list network policies
    ${NEW_POLICY_COUNT}=  get json values  ${NW_POLICY_LIST_RESP}  key=total_count
    ${EXPECT_POLICY_COUNT}=  evaluate   ${NETWORK_POLICY_COUNT} - 1
    should be equal as integers   ${NEW_POLICY_COUNT}    ${EXPECT_POLICY_COUNT}

Create Test Location Building Floor
    [Documentation]  Create Location Building Floor

    # Create first org
    ${FIRST_MAP_CREATION}=  Create First Organization   ${1st_LOCATION_ORG}  ${1st_LOCATION_STREET}  ${1st_LOCATION_CITY_STATE}  ${1st_LOCATION_COUNTRY}  width=${MAP_WIDTH}  height=${MAP_HIGHT}
    Should Be Equal As Integers    ${FIRST_MAP_CREATION}             1

    #Get Root Location ID
    ${ROOT_LOCATION_ID}=  xapi get root location id
    set suite variable  ${ROOT_LOCATION_ID}

    ${LOCATION_ID}=  xapi create location  ${ROOT_LOCATION_ID}  ${XAPI_LOCATION_NAME}
    ${RESPONSE}=  xapi get locations tree string
    should contain   ${RESPONSE}  ${XAPI_LOCATION_NAME}
    set suite variable   ${LOCATION_ID}

    #Create Topoloy - Building
    ${BUILDING_ID}=  xapi create building  ${LOCATION_ID}  ${XAPI_BUILDING_NAME}  ${XAPI_BUILDING_ADDRESS}
    ${RESPONSE}=  xapi get locations tree string
    should contain  ${RESPONSE}  ${XAPI_BUILDING_NAME}
    set suite variable  ${BUILDING_ID}

    #Create Topoloy - Floor
    ${FLOOR_ID}=  xapi create floor  ${BUILDING_ID}  ${XAPI_FLOOR_NAME}
    ${RESPONSE}=  xapi get locations tree string
    should contain   ${RESPONSE}  ${XAPI_FLOOR_NAME}
    set suite variable  ${FLOOR_ID}

Update Device Firmware
    [Documentation]  Update Device Firmware to Non Latest
    [Arguments]  ${DEVICE}  ${DEVICE_SPAWN}  ${DEVICE_BUILD}

    # Record devices clock, reboot, version info before upgrade
    ${DEV_CLOCK_BEFORE_UPGRADE}=   Send   ${DEVICE_SPAWN}   show clock
    ${DEV_REBOOT_BEFORE_UPGRADE}=  Send   ${DEVICE_SPAWN}   show reboot schedule
    Should Not Contain  ${DEV_REBOOT_BEFORE_UPGRADE}     Next reboot Scheduled
    ${DEV_VERSION_BEFORE_UPGRADE}=  Send  ${DEVICE_SPAWN}   show version detail
    ${DEV_BUILD_VERSION_BEFORE_UPGRADE}=  Get AP Version  ${DEVICE_SPAWN}

    # Upgrade device firmware
    ${DEV_VERSION_UPGRADE}=  Upgrade Device  ${${DEVICE}}  version=${DEVICE_BUILD}
    Should Not be Empty   ${DEV_VERSION_UPGRADE}
    ${UPDATE_DONE_1}=  wait_until_device_update_done   device_serial=${${DEVICE}.serial}
    Should Be Equal As Integers   ${UPDATE_DONE_1}   1
    ${CONN_STATUS_1}=  Wait Until Device Online   ${${DEVICE}.serial}
    Should Be Equal as Integers    ${CONN_STATUS_1}    1

    # Check devices clock, reboot, version info after upgrade
    ${DEV_CLOCK_AFTER_UPGRADE}=   Send   ${DEVICE1_SPAWN}   show clock
    ${DEV_REBOOT_AFTER_UPGRADE}=  Send   ${DEVICE1_SPAWN}   show reboot schedule
    Should Not Contain  ${DEV_REBOOT_AFTER_UPGRADE}     Next reboot Scheduled
    ${DEV_VERSION_AFTER_UPGRADE}=  Send  ${DEVICE_SPAWN}   show version detail
    ${DEV_BUILD_VERSION_AFTER_UPGRADE}=  Get AP Version  ${DEVICE_SPAWN}
    should contain  ${DEV_BUILD_VERSION_AFTER_UPGRADE}  ${DEV_VERSION_UPGRADE}

Clean Up Device
    [Documentation]  Clean Up Device
    [Arguments]  ${DEVICE}  ${DEVICE_ID}  ${DEVICE_SPAWN}

    # Disconnect from Extreme Cloud IQ
    Run Keyword If  '${DEVICE_ID}' != '0'  Delete and Disconnect Device From Cloud  ${DEVICE}  ${DEVICE_ID}  ${DEVICE_SPAWN}

Delete and Disconnect Device From Cloud
    [Documentation]  Delete device from cloud, disconnect device capwap connection
    [Arguments]  ${DEVICE}  ${DEVICE_ID}  ${DEVICE_SPAWN}

    xapi delete device   ${DEVICE_ID}
    disconnect device from cloud     ${${DEVICE}.cli_type}     ${DEVICE_SPAWN}
    ${DEVICE_ID_DLT}=  xapi list and get device id  ${${DEVICE}.serial}
    should be equal as strings  '${DEVICE_ID_DLT}'  '0'

Change Devices to Managed
    [Documentation]  Change Devices to Managed

    ${MANAGE_RESULT}=  xapi change multiple devices to managed   ${DEVICE1_ID}  ${DEVICE2_ID}
    ${DEVICE1_ADMIN_STATE}=  xapi list device admin state  ${device1.serial}
    ${DEVICE2_ADMIN_STATE}=  xapi list device admin state  ${device2.serial}
    should be equal as strings  ${DEVICE1_ADMIN_STATE}  MANAGED
    should be equal as strings  ${DEVICE2_ADMIN_STATE}  MANAGED

    configure device to connect to cloud    ${device1.cli_type}   ${generic_capwap_url}   ${DEVICE1_SPAWN}
    configure device to connect to cloud    ${device2.cli_type}   ${generic_capwap_url}   ${DEVICE2_SPAWN}

    ${ONLINE_STATUS_RESULT_1}=   xapi wait until device online   ${device1.serial}  ${60}  ${5}
    ${ONLINE_STATUS_RESULT_2}=   xapi wait until device online   ${device2.serial}  ${60}  ${5}
    Should Be Equal As Strings    ${ONLINE_STATUS_RESULT_1}   True
    Should Be Equal As Strings    ${ONLINE_STATUS_RESULT_2}   True

*** Test Cases ***
TCXM-42578: XAPI Device - Onboard
    [Documentation]     TCXM-42578: XAPI Onboard Devices;
    [Tags]              development  tcxm_42578

    # On board two Devices
    ${ONBOARD_RESULT}=  xapi onboard multiple extreme devices   ${device1.serial}  ${device2.serial}
    should be equal as integers  ${ONBOARD_RESULT}  1

    configure device to connect to cloud    ${device1.cli_type}   ${generic_capwap_url}   ${DEVICE1_SPAWN}
    configure device to connect to cloud    ${device2.cli_type}   ${generic_capwap_url}   ${DEVICE2_SPAWN}

    ${ONLINE_STATUS_RESULT_1}=   xapi wait until device online   ${device1.serial}  ${60}  ${5}
    ${ONLINE_STATUS_RESULT_2}=   xapi wait until device online   ${device2.serial}  ${60}  ${5}
    Should Be Equal As Strings    ${ONLINE_STATUS_RESULT_1}   True
    Should Be Equal As Strings    ${ONLINE_STATUS_RESULT_2}   True

    ${DEVICE1_ID}=  xapi list and get device id  ${device1.serial}
    ${DEVICE2_ID}=  xapi list and get device id  ${device2.serial}
    set suite variable  ${DEVICE1_ID}
    set suite variable  ${DEVICE2_ID}
    should not be equal as strings  '${DEVICE1_ID}'  '0'
    should not be equal as strings  '${DEVICE1_ID}'  '0'

TCXM-42579: XAPI Device - Change Device Manage State
    [Documentation]     TCXM-42579: XAPI Change Device Manage State;
    [Tags]              development  tcxm_42579

    # Change device to unmanage state
    ${UNMANAGE_RESULT}=  xapi change multiple devices to unmanaged   ${DEVICE1_ID}  ${DEVICE2_ID}
    ${DEVICE1_ADMIN_STATE}=  xapi list device admin state  ${device1.serial}
    ${DEVICE2_ADMIN_STATE}=  xapi list device admin state  ${device2.serial}
    should be equal as strings  ${DEVICE1_ADMIN_STATE}  UNMANAGED
    should be equal as strings  ${DEVICE2_ADMIN_STATE}  UNMANAGED

    # Change device to manage state
    ${MANAGE_RESULT}=  xapi change multiple devices to managed   ${DEVICE1_ID}  ${DEVICE2_ID}
    ${DEVICE1_ADMIN_STATE}=  xapi list device admin state  ${device1.serial}
    ${DEVICE2_ADMIN_STATE}=  xapi list device admin state  ${device2.serial}
    should be equal as strings  ${DEVICE1_ADMIN_STATE}  MANAGED
    should be equal as strings  ${DEVICE2_ADMIN_STATE}  MANAGED

    configure device to connect to cloud    ${device1.cli_type}   ${generic_capwap_url}   ${DEVICE1_SPAWN}
    configure device to connect to cloud    ${device2.cli_type}   ${generic_capwap_url}   ${DEVICE2_SPAWN}

    ${ONLINE_STATUS_RESULT_1}=   xapi wait until device online   ${device1.serial}  ${60}  ${5}
    ${ONLINE_STATUS_RESULT_2}=   xapi wait until device online   ${device2.serial}  ${60}  ${5}
    Should Be Equal As Strings    ${ONLINE_STATUS_RESULT_1}   True
    Should Be Equal As Strings    ${ONLINE_STATUS_RESULT_2}   True

    [Teardown]   run keywords   Change Devices to Managed

TCXM-42581: XAPI Device - Assign Location to Devices
    [Documentation]     TCXM-42581: XAPI Assign Location to Devices;
    [Tags]              development  tcxm_42581

    # Assign Location to Devices
    ${RESP_ASSIGN_DEV1_LOCATION}=  xapi assign location to device   ${DEVICE1_ID}   ${FLOOR_ID}
    ${RESP_ASSIGN_DEV2_LOCATION}=  xapi assign location to device   ${DEVICE2_ID}   ${FLOOR_ID}
    should be equal as integers    ${RESP_ASSIGN_DEV1_LOCATION}    1
    should be equal as integers    ${RESP_ASSIGN_DEV2_LOCATION}    1

TCXM-42580: XAPI Device - Assign Network Policy to Devices
    [Documentation]     TCXM-42580: XAPI Assign Network Policy to Devices;
    [Tags]              development  tcxm_42580

    #Create Network-Policy
    ${RESP}=  xapi create network policy  '{"name" : "${xapi_nw_policy_name}", "type" : "NETWORK_ACCESS_AND_SWITCHING", "description" : "Xapi auto test network policy for network access and switch"}'
    ${NETWORK_POLICY_ID}=  get json values  ${RESP}  key=id
    set suite variable      ${NETWORK_POLICY_ID}

    ${RESP_LIST}=  xapi list network policies
    ${NETWORK_POLICY_COUNT}=  get json values  ${RESP_LIST}  key=total_count
    set suite variable      ${NETWORK_POLICY_COUNT}

    #Assign network policy to device
    ${ASSIGN_NW_POLICY}=  xapi assign network policy to two devices  ${DEVICE1_ID}  ${DEVICE2_ID}  ${NETWORK_POLICY_ID}
    Should Be Equal As Integers  ${ASSIGN_NW_POLICY}  1

    ${DEV1_NW_POLICY_ID}=  xapi get device network policy id  ${DEVICE1_ID}
    ${DEV2_NW_POLICY_ID}=  xapi get device network policy id  ${DEVICE2_ID}
    should be equal as strings  '${DEV1_NW_POLICY_ID}'  '${NETWORK_POLICY_ID}'
    should be equal as strings  '${DEV2_NW_POLICY_ID}'  '${NETWORK_POLICY_ID}'

    ${DEV1_NW_POLICY_NAME}=  xapi get device network policy name  ${DEVICE1_ID}
    ${DEV2_NW_POLICY_NAME}=  xapi get device network policy name  ${DEVICE2_ID}
    should be equal as strings  '${DEV1_NW_POLICY_NAME}'  '${XAPI_NW_POLICY_NAME}'
    should be equal as strings  '${DEV2_NW_POLICY_NAME}'  '${XAPI_NW_POLICY_NAME}'

TCXM-42575: XAPI Deployment - Update Complete Configuration to Device
    [Documentation]      XAPI Deployment - Update Complete Configuration to Device
    [Tags]			     development  tcxm_42575

    # Prepare the environment, upgrade the device to non latest build
    ${DEV1_LATEST_BUILD}=  get device latest version  ${device1}
    #${DEV1_LATEST_BUILD}=  upgrade device  ${device1}  action=close
    set suite variable  ${DEV1_LATEST_BUILD}
    ${DEV1_BUILD_VERSION_BEFORE_UPGRADE}=  Get AP Version  ${DEVICE1_SPAWN}
    run keyword if  '${DEV1_BUILD_VERSION_BEFORE_UPGRADE}' == '${DEV1_LATEST_BUILD}'  Update Device Firmware  device1  ${DEVICE1_SPAWN}  ${NON_LASTEST_BUILD}

    ${DEV1_BUILD_VERSION_BEFORE_PUSH}=  Get AP Version  ${DEVICE1_SPAWN}
    # Update complete configuration via XAPI
	${DEV1_PUSH_CONFIG}=  xapi push complete config   ${DEVICE1_ID}
    Should Be Equal As Integers   ${DEV1_PUSH_CONFIG}   1
    sleep   10s
    ${UPDATE_DONE_1}=  wait_until_device_update_done   device_serial=${device1.serial}
    Should Be Equal As Integers   ${UPDATE_DONE_1}   1
    ${CONFIG_DEPLOY_STATUS}=  xapi configuration push deployment status  ${DEVICE1_ID}
    Should Be Equal As Strings   '${CONFIG_DEPLOY_STATUS}'   'True'
    ${ONLINE_STATUS_RESULT_1}=   xapi wait until device online   ${device1.serial}  ${60}  ${5}
    Should Be Equal As Strings    ${ONLINE_STATUS_RESULT_1}   True

    # Validate the firmware was not upgraded
    ${DEV1_BUILD_VERSION_AFTER_PUSH}=  Get AP Version  ${DEVICE1_SPAWN}
    Should Be Equal As Strings  ${DEV1_BUILD_VERSION_BEFORE_PUSH}   ${DEV1_BUILD_VERSION_AFTER_PUSH}

TCXM-42576: XAPI Deployment - Update Delta Configuration to Device
    [Documentation]      XAPI Deployment - Update Delta Configuration to Device
    [Tags]			     development  tcxm_42576

    # Change device hostname
    ${RESP}=  xapi change device hostname  ${DEVICE1_ID}    ${device1.name}
    Should Be Equal As Integers  ${RESP}  1
    ${DEV1_CUR_HOSTNAME}=  xapi get device hostname  ${DEVICE1_ID}
    should not be empty  ${DEV1_CUR_HOSTNAME}
    ${DEV1_UPDATE_HOSTNAME}=  set variable  ${device1.name}_xapi_auto
    ${RESP}=  xapi change device hostname  ${DEVICE1_ID}    ${DEV1_UPDATE_HOSTNAME}
    Should Be Equal As Integers  ${RESP}  1

    # Update delta configuration via XAPI
    ${DEV1_BUILD_VERSION_BEFORE_PUSH}=  Get AP Version  ${DEVICE1_SPAWN}
	${DEV1_PUSH_CONFIG}=  xapi push delta config   ${DEVICE1_ID}
    Should Be Equal As Integers   ${DEV1_PUSH_CONFIG}   1
    ${UPDATE_DONE_1}=  wait_until_device_update_done   device_serial=${device1.serial}
    Should Be Equal As Integers   ${UPDATE_DONE_1}   1
    ${CONFIG_DEPLOY_STATUS}=  xapi configuration push deployment status  ${DEVICE1_ID}
    Should Be Equal As Strings   '${CONFIG_DEPLOY_STATUS}'   'True'

    # Check the device new hostname
    ${DEV1_NEW_HOSTNAME}=  xapi get device hostname  ${DEVICE1_ID}
    should not be empty  ${DEV1_NEW_HOSTNAME}
    should be equal as strings  ${DEV1_NEW_HOSTNAME}  ${DEV1_UPDATE_HOSTNAME}

    # Validate the firmware was not upgraded
    ${DEV1_BUILD_VERSION_AFTER_PUSH}=  Get AP Version  ${DEVICE1_SPAWN}
    Should Be Equal As Strings  ${DEV1_BUILD_VERSION_BEFORE_PUSH}   ${DEV1_BUILD_VERSION_AFTER_PUSH}

    # Change hostname back to the original one
    ${RESP}=  xapi change device hostname  ${DEVICE1_ID}    ${DEV1_CUR_HOSTNAME}
    Should Be Equal As Integers  ${RESP}  1

TCXM-42577: XAPI Deployment - Update Complete Configuration and Firmware to Device
    [Documentation]      XAPI Deployment - Update Complete Configuration and Firmware to Device
    [Tags]			     development  tcxm_42577

    # Update firmware via XAPI
	${DEV1_PUSH_CONFIG}=  xapi push complete config and firmware  ${DEVICE1_ID}
    Should Be Equal As Integers   ${DEV1_PUSH_CONFIG}   1
    sleep   10s
    ${UPDATE_DONE_1}=  wait_until_device_update_done   device_serial=${device1.serial}
    Should Be Equal As Integers   ${UPDATE_DONE_1}   1
    ${CONFIG_DEPLOY_STATUS}=  xapi configuration push deployment status  ${DEVICE1_ID}
    Should Be Equal As Strings   '${CONFIG_DEPLOY_STATUS}'   'True'
    ${ONLINE_STATUS_RESULT_1}=   xapi wait until device online   ${device1.serial}  ${60}  ${5}
    Should Be Equal As Strings    ${ONLINE_STATUS_RESULT_1}   True

    # Validate the firmware was upgraded to the latest one
    ${DEV1_BUILD_VERSION_AFTER_PUSH}=  Get AP Version  ${DEVICE1_SPAWN}
    Should Be Equal As Strings  ${DEV1_LATEST_BUILD}   ${DEV1_BUILD_VERSION_AFTER_PUSH}

