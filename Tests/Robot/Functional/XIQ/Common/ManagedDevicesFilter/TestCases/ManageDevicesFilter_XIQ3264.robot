# Author        : Lacy Wu
# Date          : Nov 28th 2022
# Description   : Managed Devices Filter
#
# Topology      :
# Host ----- Cloud
*** Variables ***
${device_type1}           AP230
${device_type2}           AP410C
#${BUILDING_1}             building_01
#${BUILDING_2}             building_02
#${FLOOR_1}                floor_01
#${FLOOR_2}                floor_03
*** Settings ***
Documentation  robot -v ENV:environment.local.chrome.yaml -v TOPO:topo.test.cp8r1.yaml  ESPAlert_XIQ6344.robot

Library     xiq/flows/common/Login.py
Library     common/Cli.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/Device360.py
Library     xiq/flows/common/Navigator.py
Library     String
Library     Collections
Library     xiq/flows/configure/CommonObjects.py
Library     xiq/flows/extreme_location/ExtremeLocation.py
Library     xiq/flows/manage/Location.py
Library     xiq/flows/configure/ClassificationRule.py
Library     xiq/flows/configure/CloudConfigGroup.py
Library     xiq/flows/globalsettings/GlobalSetting.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/mlinsights/MLInsights.py
Library     xiq/flows/manage/FilterManageDevices.py
Library     xiq/flows/manage/TestFilterDevicesBy.py


Resource    ../Resources/location_config.robot
Resource    ../Resources/wireless_networks_related_config.robot

Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Force Tags      testbed_none
Suite Setup      Pre Condition
Suite Teardown   Suite Clean Up

*** Test Cases ***
TCXM-26873: Filtering devices based on network policy
    [Documentation]         Filtering devices based on network policy
    [Tags]                  tcxm_26873  development
    #filter device by network policy
    ${CHECK_RESULT}=        check filter device by network policy is correct
    Should Be Equal As Integers    ${CHECK_RESULT}        1

*** Keywords ***
Pre Condition
    [Documentation]   Login XIQ and Create Maps and classification rules first
    [Tags]                      tcxm_26873     development    pre-condition

    ${device1}=      Create Dictionary
    ...     name=simulated_dut01
    ...     model=${device_type1}
    ...     simulated_count=1
    ...     onboard_device_type=Simulated
    ...     location=${LOCATION_1}, San Jose, ${BUILDING_1}, ${FLOOR_1}

    ${device2}=      Create Dictionary
    ...     name=simulated_dut02
    ...     model=${device_type2}
    ...     simulated_count=1
    ...     onboard_device_type=Simulated
    ...     location=${LOCATION_2}, Santa Clara, ${BUILDING_2}, ${FLOOR_2}

    set suite variable    ${device1}
    set suite variable    ${device2}

 #Login AIO
    ${Login_XIQ}=                  Login User              ${tenant_username}      ${tenant_password}
    Should Be Equal As Integers    ${Login_XIQ}             1
# Create First Map info, you can go to /Resources/location_config.robot to change related parameters
    ${FIRST_MAP_CREATION}=      Create First Organization       ${1st_LOCATION_ORG}      ${1st_LOCATION_STREET}       ${1st_LOCATION_CITY_STATE}       ${1st_LOCATION_COUNTRY}      width=${MAP_WIDTH}      height=${MAP_HIGHT}
    Should Be Equal As Integers    ${FIRST_MAP_CREATION}        1
#### Create location building floor
    ${Create_LBF_1}=        create location building floor    ${LOCATION_1}    ${BUILDING_1}    ${FLOOR_1}
    Log         Create Location Building Floor 1 result: ${Create_LBF_1}
    Should Be Equal As Integers    ${Create_LBF_1}             1

    ${Create_LBF_2}=        create location building floor    ${LOCATION_2}    ${BUILDING_2}    ${FLOOR_2}
    Log         Create Location Building Floor 2 result: ${Create_LBF_2}
    Should Be Equal As Integers    ${Create_LBF_2}             1

# Create Two Network Policys
    ${NW_POLICY_CREATION}=  Create Network Policy   ${NW_POLICY_NAME1}   ${WIRELESS_PESRONAL_WPA2CCMP_1}
    Should Be Equal As Strings   '${NW_POLICY_CREATION}'   '1'
    ${NW_POLICY_CREATION}=  Create Network Policy   ${NW_POLICY_NAME2}   ${WIRELESS_PESRONAL_WPA2CCMP_2}
    Should Be Equal As Strings   '${NW_POLICY_CREATION}'   '1'

# Onboard 2 simulator APs
    ${ONBOARD_RESULT}=      onboard device quick    ${device1}
    Should Be Equal As Strings          ${ONBOARD_RESULT}       1
    ${ONBOARD_RESULT}=      onboard device quick    ${device2}
    Should Be Equal As Strings          ${ONBOARD_RESULT}       1

    ${ONBOARD_AP1_SERIALS}=     set variable    ${${device1.name}.serial}
    Set Suite Variable         ${ONBOARD_AP1_SERIALS}
    ${ONBOARD_AP2_SERIALS}=     set variable    ${${device2.name}.serial}
    Set Suite Variable         ${ONBOARD_AP2_SERIALS}
# Assign Network Policy1 to device1
    assign network policy to a device    ${${device1.name}.serial}  ${NW_POLICY_NAME1}
# Assign Network Policy2 to device2
    assign network policy to a device    ${${device2.name}.serial}  ${NW_POLICY_NAME2}
Suite Clean Up
    [Documentation]    Delete all devices, all ssids, Network Policy, classification rule, ccg, location and quit web browser
    [Tags]             development          tcxm_26873
    Delete All devices
    delete_all_ssid_in_policy   ${NW_POLICY_NAME1}
    Delete Network Policy    ${NW_POLICY_NAME1}
    delete_all_ssid_in_policy   ${NW_POLICY_NAME2}
    Delete Network Policy    ${NW_POLICY_NAME2}
    Delete Location Building Floor  ${LOCATION_1}      ${BUILDING_1}     ${FLOOR_1}
    Delete Location Building Floor  ${LOCATION_2}      ${BUILDING_2}     ${FLOOR_2}
    Logout User
    XIQ Quit Browser

