## Author: Wenqi Cao
# Date: July 7 2022
# For CFD-7548: XIQ pushing out commands that are not configured. ppsk(https://jira.extremenetworks.com/browse/CFD-7548)
# Workflow:
# - Login XIQ
# - Go to "Manage/Planning" to create a Location
# - Go to "Configure/Network Policies" to create a Network Policy
# - In above Network Policy, configure one PPSK SSID with cloud user group and local user group
# - Onboard an simulate AP with above location and Network Policy
# - After simulate AP onboard successfully, check the complete config, make sure there is no any "security additional-auth-method captive-web-portal" CLI

*** Variables ***
######### For Local AIO testbed Start #########
${WEB_DRIVER_LOC}           local
${TENANT_USERNAME}          admin@cust001.com
${TENANT_PASSWORD}          aerohive
${TEST_URL}                 https://10.16.231.72/
${AIO_IP}                   10.16.231.72
${ELEMENT_INFO}             None
${BROWSER}                  chrome
######### For Local AIO testbed End #########
${DEVICE_TYPE}              AP410C
${SIM_AP_COUNT}             1

${CWP_CLI}      security additional-auth-method captive-web-portal
#Variables    TestBeds/${TESTBED}
#Variables    Environments/${TOPO}
#Variables    Environments/${ENV}

*** Settings ***

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
Library     xiq/flows/manage/DeviceConfig.py
Library     xiq/flows/configure/UserGroups.py


Variables    Environments/Config/waits.yaml

Resource    ../Resources/location_config.robot
Resource    ../Resources/wireless_networks_related_config.robot
Force Tags      testbed_none
Suite Setup      Pre Condition

*** Keywords ***
Pre Condition
    [Documentation]   Login XIQ, create 1st location and Network Policy with PPSK SSID with cloud and local user groups, onboard simulate AP and assign Network Policy to it
    [Tags]                      cfd-7548     development    pre-condition
# Login AIO
    ${Login_XIQ}=                  Login User              ${TENANT_USERNAME}      ${TENANT_PASSWORD}
    Should Be Equal As Integers    ${Login_XIQ}             1
# Create First Map info, you can go to /Resources/location_config.robot to change related parameters
    ${FIRST_MAP_CREATION}=      Create First Organization       ${1st_LOCATION_ORG}      ${1st_LOCATION_STREET}       ${1st_LOCATION_CITY_STATE}       ${1st_LOCATION_COUNTRY}      width=${MAP_WIDTH}      height=${MAP_HIGHT}
    Should Be Equal As Integers    ${FIRST_MAP_CREATION}             1

# Create Network Policy
    ${NW_POLICY_CREATION}=  Create Network Policy   ${NW_POLICY_NAME1}   &{WIRELESS_PPSK_WPA2CCMP_1}
    Should Be Equal As Strings   '${NW_POLICY_CREATION}'   '1'
    add_user_group_to_network_policy_ssid       ${NW_POLICY_NAME1}    &{WIRELESS_PPSK_WPA2CCMP_1}    &{PPSK_AUTH_PROFILE_LOCAL_BULK}

# Onboard 1 simulator
    ${ONBOARD_AP_SERIAL}=      Onboard Simulated Device    ${DEVICE_TYPE}      count=${SIM_AP_COUNT}    location=${1st_LOCATION_ORG},${1st_LOCATION_CITY_STATE},${1st_LOCATION_STREET},Floor 1
    Set Suite Variable    ${ONBOARD_AP_SERIAL}
# Assign Network Policy to all devices
    Assign Network Policy To All Devices     ${NW_POLICY_NAME1}

*** Test Cases ***
#######  IP NETWORK  ####################################################################################################
cfd-7548_case: XIQ pushing out commands that are not configured. ppsk
    [Documentation]     Check complete config to make sure there is no "security additional-auth-method captive-web-portal" CLI, when configure local and cloud PPSK group in one PPSK SSID
    [Tags]                      cfd-7548   pnc  development    cfd-7548_case     tcxm-21595
    ${full_config}=       get_device_config_audit_delta_complete        ${ONBOARD_AP_SERIAL}        complete
    Log To Console    Testing!!!!!!!
    Should Not Contain    ${full_config}    ${CWP_CLI}

Test Suite Clean Up
    [Documentation]    Delete all devices, all ssids, Network Policy, location user groups and quit web browser
    [Tags]             cfd-7548         cleanup     development          tcxm-21566
    Delete All devices
    delete_all_ssid_in_policy   ${NW_POLICY_NAME1}
    Delete Network Policy    ${NW_POLICY_NAME1}
    Delete User Groups    ${BULK_CLOUD_USER_GROUP}      ${BULK_LOCAL_USER_GROUP}
    Delete Location Building Floor  ${1st_LOCATION_CITY_STATE}      ${1st_LOCATION_STREET}     Floor 1
    XIQ Quit Browser





