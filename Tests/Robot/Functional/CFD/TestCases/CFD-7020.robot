## Author: Wenqi Cao
# Date: Jun 27th 2022
# For CFD-7020: SSID assignment rule with "Does Not Contain" a CCG removes SSID from all devices in policy (https://jira.extremenetworks.com/browse/CFD-7020)
# Workflow:
# - Login XIQ
# - Go to "Manage/Planning" to create a Location
# - Onboard 4 APs: AP1, AP2, AP3 and AP4
# - Go to "Configure/Common Objects/Policy/Cloud Config Group" to create Cloud Config Group with AP1 and AP2
# - Go to "Configure/Network Policies" to create a Network Policy
# - In above Network Policy, configure one SSID and enable classification rules
# - Create a classification rules with don't contain the configured CCG as above
# - Assign Network Policy to the 4 APs
# - Go to AP device level page one by one
# - Check the SSID:
# -- SSID shouldn't be there for AP1 and AP2
# -- SSID shouldn BE there for AP3 and AP4


*** Variables ***
######### For Local AIO testbed Start #########
${WEB_DRIVER_LOC}           local
${TENANT_USERNAME}          admin@cust001.com
${TENANT_PASSWORD}          aerohive
${TEST_URL}                 https://10.16.231.72/
${AIO_IP}                   10.16.231.72
${BROWSER}                  chrome
######### For Local AIO testbed End #########


*** Settings ***

# The keywords in Login.py have been moved to the keywords directory.
# If the moved keyword is not working correctly import the original library and remove the keywords/gui/login/KeywordsLogin.py version.
#Library     xiq/flows/common/Login.py
Library     keywords/gui/login/KeywordsLogin.py
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

#Variables    TestBeds/${TESTBED}
#Variables    Environments/${TOPO}
#Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml

Resource    ../Resources/location_config.robot
Resource    ../Resources/wireless_networks_related_config.robot
Force Tags      testbed_none
Suite Setup      Pre Condition
Suite Teardown   Suite Clean Up

*** Keywords ***
Pre Condition
    [Documentation]   Login XIQ and Create Maps and classification rules first
    [Tags]                      cfd-7020     development    pre-condition

    ${device}=      Create Dictionary
    ...     name=simulated_dut01
    ...     model=AP410C
    ...     simulated_count=4
    ...     onboard_device_type=Simulated
    ...     location=auto_location_01, Santa Clara, building_02, floor_04

    set suite variable    ${device}

# Login AIO
    ${Login_XIQ}=                  Login User              ${TENANT_USERNAME}      ${TENANT_PASSWORD}
    Should Be Equal As Integers    ${Login_XIQ}             1
# Create First Map info, you can go to /Resources/location_config.robot to change related parameters
    ${FIRST_MAP_CREATION}=      Create First Organization       ${1st_LOCATION_ORG}      ${1st_LOCATION_STREET}       ${1st_LOCATION_CITY_STATE}       ${1st_LOCATION_COUNTRY}      width=${MAP_WIDTH}      height=${MAP_HIGHT}
    Should Be Equal As Integers    ${FIRST_MAP_CREATION}             1

# Create Network Policy
    ${NW_POLICY_CREATION}=  Create Network Policy   ${NW_POLICY_NAME1}   ${WIRELESS_PESRONAL_WPA2CCMP_1}
    Should Be Equal As Strings   '${NW_POLICY_CREATION}'   '1'
    Add Wireless Nw To Network Policy    ${NW_POLICY_NAME1}    &{WIRELESS_PESRONAL_WPA2CCMP_2}

# Onboard 2 simulator APs
    ${ONBOARD_RESULT}=      onboard device quick    ${device}
    Should Be Equal As Strings          ${ONBOARD_RESULT}       1


    ${ONBOARD_AP_SERIALS}=     set variable    ${${device.name}.serial}
    Set Suite Variable         ${ONBOARD_AP_SERIALS}

# Create ccg profile
    ${CCG_NAME}=     Get From List      ${ONBOARD_AP_SERIALS}        0
    Set Suite Variable     ${CCG_NAME}
    ${CCG_DESCRIPTION}=     Get From List      ${ONBOARD_AP_SERIALS}        0
    @{AP_SERIAL_IN_CCG}=     Get Slice From List      ${ONBOARD_AP_SERIALS}        0   2
    Set Suite Variable     @{AP_SERIAL_IN_CCG}
    Add Cloud Config Group      ${CCG_NAME}        ${CCG_DESCRIPTION}        @{AP_SERIAL_IN_CCG}
# Add classification rule with ccg
    ${RULE_NAME}=     Get From List      ${ONBOARD_AP_SERIALS}        0
    Set Suite Variable     ${RULE_NAME}
    ${RULE_DESCRIPTION}=     Get From List      ${ONBOARD_AP_SERIALS}        0
    ${CLOUD_CONFIG_GROUP_POLCIY}=     Get From List      ${ONBOARD_AP_SERIALS}        0
    Add Classification Rule With CCG    ${RULE_NAME}    ${RULE_DESCRIPTION}    not    ${CLOUD_CONFIG_GROUP_POLCIY}
# Enable SSID classification and assign rule
    ${Classification_Rule}=      Get From List      ${ONBOARD_AP_SERIALS}        0
    Add Classification Rule to SSID     ${NW_POLICY_NAME1}        ${WIRELESS_PESRONAL_WPA2CCMP_1}[ssid_name]        ${Classification_Rule}

# Assign Network Policy to all devices
    Assign Network Policy To All Devices     ${NW_POLICY_NAME1}

Suite Clean Up
    [Documentation]    Delete all devices, all ssids, Network Policy, classification rule, ccg, location and quit web browser
    [Tags]             cfd-7020         cleanup     development          tcxm-21566
    Delete All devices
    delete_all_ssid_in_policy   ${NW_POLICY_NAME1}
    Delete Network Policy    ${NW_POLICY_NAME1}
    Delete Single Classification rule      ${RULE_NAME}
    Delete Cloud Config Group      ${CCG_NAME}
    Delete Location Building Floor  ${1st_LOCATION_CITY_STATE}      ${1st_LOCATION_STREET}     Floor 1
    XIQ Quit Browser

*** Test Cases ***
######  IP NETWORK  ####################################################################################################
CFD-7020_case: AP in CCG profile with "(Does Not Contain)" should NOT have SSID, or AP should have the SSID
    [Documentation]     AP in CCG profile with "(Does Not Contain)" should NOT have SSID, or AP should have the SSID
    [Tags]                      cfd-7020   pnc  development    cfd-7020_case     tcxm-21566
    ${AP_Serials}=        Get Device Serial Numbers     ${DEVICE_TYPE}
    FOR     ${ap_sn}       IN      @{AP_Serials}
        ${hostname}=   get_hostname     ${ap_sn}
        ${ssid_lists}=       Get Ap Wifi0and1 Configured Ssids     ${hostname}
        ${match_count}=      Get Match Count    ${AP_SERIAL_IN_CCG}        ${ap_sn}
        IF  ${match_count} > 0
            Log To Console                      "The SSID: ${WIRELESS_PESRONAL_WPA2CCMP_1}[ssid_name]"
            Log To Console                      "WiFi0 SSID list: ${ssid_lists}[wifi0]"
            List Should Not Contain Value       ${ssid_lists}[wifi0]        ${WIRELESS_PESRONAL_WPA2CCMP_1}[ssid_name]
            List Should Not Contain Value       ${ssid_lists}[wifi1]        ${WIRELESS_PESRONAL_WPA2CCMP_1}[ssid_name]
        ELSE
            Log To Console                      "The SSID: ${WIRELESS_PESRONAL_WPA2CCMP_1}[ssid_name]"
            Log To Console                      "WiFi0 SSID list: ${ssid_lists}[wifi0]"
            List Should Contain Value       ${ssid_lists}[wifi0]        ${WIRELESS_PESRONAL_WPA2CCMP_1}[ssid_name]
            List Should Contain Value       ${ssid_lists}[wifi1]        ${WIRELESS_PESRONAL_WPA2CCMP_1}[ssid_name]
        END
    END





