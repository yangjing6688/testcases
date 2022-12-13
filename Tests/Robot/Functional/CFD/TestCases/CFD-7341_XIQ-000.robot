## Author        : Wenqi Cao
# Date          : May 22th 2022
# For CFD-7341: IP Objects only save the active page (https://jira.extremenetworks.com/browse/CFD-7341)
# Workflow:
# - Login XIQ
# - Go to "Manage/Planning" to create Location
# - Go to "Configure/Common Objects/Policy/Classification Rules" to create classification rules based on location
# - Go to "Configure/Common Objects/Basic/IP Objects/Hostnames" to create IP objects with 17 items
# - Then edit the IP Objects profile, and go to 2nd page to add another one item, then save the profile, the total items are 18
# - Check the number of the items(18) in the IP Object is same as defined itmes(18) in ip_and_subnet_resource.robot file
# - Clean all the configuration and quit web browser


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

${RANGE_START}  1
${RANGE_END}    21

*** Settings ***

Library     xiq/flows/common/Login.py
Library     xiq/flows/manage/Device360.py
Library     xiq/flows/common/Navigator.py
Library     String
Library     Collections
Library     xiq/flows/configure/CommonObjects.py
Library     xiq/flows/extreme_location/ExtremeLocation.py
Library     xiq/flows/manage/Location.py
Library     xiq/flows/configure/ClassificationRule.py


#Variables    TestBeds/${TESTBED}
#Variables    Environments/${TOPO}
#Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml

Resource    ../Resources/location_config.robot
Resource    ../Resources/ip_and_subnet_resource.robot
Force Tags      testbed_none
Suite Setup      Pre Condition
Suite Teardown   Suite Clean Up

*** Keywords ***
Pre Condition
    [Documentation]   Login XIQ and Create Maps and classification rules first
    [Tags]                      cfd-7341     development    pre-condition
### Login AIO
    ${Login_XIQ}=                  Login User              ${TENANT_USERNAME}      ${TENANT_PASSWORD}
    Should Be Equal As Integers    ${Login_XIQ}             1

### Create First Map info, you can go to /Resources/location_config.robot to change related parameters
    ${FIRST_MAP_CREATION}=  Create First Organization       ${1st_LOCATION_ORG}      ${1st_LOCATION_STREET}       ${1st_LOCATION_CITY_STATE}       ${1st_LOCATION_COUNTRY}      width=${MAP_WIDTH}      height=${MAP_HIGHT}
    Should Be Equal As Integers    ${FIRST_MAP_CREATION}             1

####### Create More Maps, and classification rules based on location with FOR loop logic
####### You can go to /Resources/location_config.robot to change related parameters
    FOR     ${index}    IN RANGE    ${RANGE_START}       ${RANGE_END}
        Create Location Building Floor      ${LOCATION_${index}}   ${BUILDING_${index}}    ${FLOOR_${index}}  width=${MAP_WIDTH}   height=${MAP_HIGHT}
        Add Classification Rule with Location       cls_rule_location_${index}      cls_rule_location_${index}      ${LOC_TEST_${index}}
    END

Suite Clean Up
    [Documentation]    delete IP Object profile, classification rules, and MAPs
    [Tags]             cfd-7341         cleanup     development          tcxm-21454
    @{PROFILES}    Create List      ${IP_OBJECT_NAME}       ${IP_NETWORKS_OBJECT_NAME}      ${HOSTNAME_OBJECT_NAME}         ${WILDCARD_HOSTNAME_OBJECT_NAME}        ${WILDCARD_NETWORK_OBJECT_NAME}         ${IP_RANGE_OBJECT_NAME}

    FOR     ${PROFILE}  IN  @{PROFILES}
        IP Object Hostname Delete Object Profile        ${PROFILE}
    END

    FOR     ${index}    IN RANGE    ${RANGE_START}       ${RANGE_END}
        Delete Classification rules   cls_rule_location_${index}
        Delete Location Building Floor      ${LOCATION_${index}}   ${BUILDING_${index}}    ${FLOOR_${index}}
    END
    Delete Location Building Floor  ${1st_LOCATION_CITY_STATE}      ${1st_LOCATION_STREET}     Floor 1
    XIQ Quit Browser

*** Test Cases ***
######  IP NETWORK  ####################################################################################################
CFD-7341_Network_Step1: Create IP Object Hostname profile
    [Documentation]             Go to Configure/Common Objects//Basic/IP Objects and Host Name to create an profile with Network type, with 17 network items, and then save it
    [Tags]                      cfd-7341     development    cfd-7341_network_step_1     tcxm-21454
    Add IP Object Hostname With IP Network      ${IP_NETWORKS_OBJECT_NAME}    ${NETWORK_OBJECT_TYPE}      ${IP_NETWORK_GLOBAL}       ${NETMASK}      @{IP_NETWORKS_MORE}

CFD-7341_Network_Step2: Add new network items
    [Documentation]             Edit above IP Object profile, and go to the 2nd page, add the 18th network item, and save it
    [Tags]                      cfd-7341     development    cfd-7341_network_step_2     tcxm-21454
    ${new_items_add_result}=        IP Object Hostname Update Object Profile        ${IP_NETWORKS_OBJECT_NAME}   ${NETMASK}    None     @{IP_NETWORKS_MORE_1}
    Should Be Equal As Integers     ${new_items_add_result}     1

CFD-7341_Network_Step3: Check the count of network items in the profile
    [Documentation]             Edit the IP Object profile again, to check if there are 18 network items in the profile are same as parameter file
    [Tags]                      cfd-7341     development    cfd-7341_network_step_3     tcxm-21454
    @{Configured_Items_for_Object_Profile}      create list     ${IP_NETWORK_GLOBAL}    @{IP_NETWORKS_MORE}     @{IP_NETWORKS_MORE_1}
    ${Get_Items_Of_Object_Profile}=        IP Object Hostname List All Objects in Profile      ${IP_NETWORKS_OBJECT_NAME}
    Lists Should Be Equal       ${Configured_Items_for_Object_Profile}      ${Get_Items_Of_Object_Profile}

#######  IP ADDRESS  ####################################################################################################
#CFD-7341_IP_Step1: Create IP Object Hostname profile
#    [Documentation]             Go to Configure/Common Objects//Basic/IP Objects and Host Name to create an profile with Network type, with 17 network items, and then save it
#    [Tags]                      cfd-7341     development    cfd-7341_ip_step_1     tcxm-21454
#    Add IP Object Hostname With IP or Hostname  ${IP_OBJECT_NAME}       ${IP_OBJECT_TYPE}       ${IP_ADDRESS_GLOBAL}        @{IP_ADDRESSES_MORE}
#
#CFD-7341_IP_Step2: Add new ip items
#    [Documentation]             Edit above IP Object profile, and go to the 2nd page, add the 18th ip item, and save it
#    [Tags]                      cfd-7341     development    cfd-7341_ip_step_2     tcxm-21454
#    IP Object Hostname Update Object Profile     ${IP_OBJECT_NAME}      None      None      @{IP_ADDRESSES_MORE_1}
#
#CFD-7341_IP_Step3: Check the count of ip items in the profile
#    [Documentation]             Edit the IP Object profile again, to check if there are 18 ip items in the profile are same as parameter file
#    [Tags]                      cfd-7341    development     cfd-7341_ip_step_3     tcxm-21454
#    @{Configured_Items_for_Object_Profile}      create list     ${IP_ADDRESS_GLOBAL}    @{IP_ADDRESSES_MORE}     @{IP_ADDRESSES_MORE_1}
#    ${Get_Items_Of_Object_Profile}=        IP Object Hostname List All Objects in Profile      ${IP_OBJECT_NAME}
#    Lists Should Be Equal       ${Configured_Items_for_Object_Profile}      ${Get_Items_Of_Object_Profile}

#######  HOSTNAME  ######################################################################################################
#CFD-7341_Hostname_Step1: Create IP Object Hostname profile
#    [Documentation]             Go to Configure/Common Objects//Basic/IP Objects and Host Name to create an profile with Host Name type, with 17 network items, and then save it
#    [Tags]                      cfd-7341     development    cfd-7341_hostname_step_1     tcxm-21454
#    Add IP Object Hostname With IP or Hostname  ${HOSTNAME_OBJECT_NAME}       ${HOSTNAME_OBJECT_TYPE}       ${HOSTNAME_GLOBAL}        @{HOSTNAME_MORE}
#
#CFD-7341_Hostname_Step2: Add new hostname items
#    [Documentation]             Edit above IP Object profile, and go to the 2nd page, add the 18th hostname item, and save it
#    [Tags]                      cfd-7341     development    cfd-7341_hostname_step_2     tcxm-21454
#    IP Object Hostname Update Object Profile     ${HOSTNAME_OBJECT_NAME}      None     None     @{HOSTNAME_MORE_1}
#
#CFD-7341_Hostname_Step3: Check the count of hostname items in the profile
#    [Documentation]             Edit the IP Object profile again, to check if there are 18 hostname items in the profile are same as parameter file
#    [Tags]                      cfd-7341     development    cfd-7341_hostname_step_3     tcxm-21454
#    @{Configured_Items_for_Object_Profile}      create list     ${HOSTNAME_GLOBAL}    @{HOSTNAME_MORE}     @{HOSTNAME_MORE_1}
#    ${Get_Items_Of_Object_Profile}=       IP Object Hostname List All Objects in Profile        ${HOSTNAME_OBJECT_NAME}
#    Lists Should Be Equal       ${Configured_Items_for_Object_Profile}      ${Get_Items_Of_Object_Profile}

#######  IP RANGE  ######################################################################################################
#CFD-7341_IP_Range_Step1: Create IP Object Hostname profile
#    [Documentation]             Go to Configure/Common Objects//Basic/IP Objects and Host Name to create an profile with IP Range type, with 17 network items, and then save it
#    [Tags]                      cfd-7341     development    cfd-7341_ip_range_step_1     tcxm-21454
#    Add IP Object Hostname With IP Range        ${IP_RANGE_OBJECT_NAME}       ${IP_RANGE_START_GLOBAL}      ${IP_RANGE_GAP}       @{IP_RANGE_START_CLASSIFIED}
#
#CFD-7341_IP_Range_Step2: Add new IP Range items
#    [Documentation]             Edit above IP Object profile, and go to the 2nd page, add the 18th ip range item, and save it
#    [Tags]                      cfd-7341     development    cfd-7341_ip_range_step_2     tcxm-21454
#    IP Object Hostname Update Object Profile     ${IP_RANGE_OBJECT_NAME}      None     ${IP_RANGE_GAP}     @{IP_RANGE_START_CLASSIFIED_1}
#
#CFD-7341_IP_Range_Step3: Check the count of IP Range items in the profile
#    [Documentation]             Edit the IP Object profile again, to check if there are 18 ip range items in the profile are same as parameter file
#    [Tags]                      cfd-7341     development    cfd-7341_ip_range_step_3     tcxm-21454
#    @{Configured_Items_for_Object_Profile}      create list     ${IP_RANGE_START_GLOBAL}    @{IP_RANGE_START_CLASSIFIED}     @{IP_RANGE_START_CLASSIFIED_1}
#    ${Get_Items_Of_Object_Profile}=        IP Object Hostname List All Objects in Profile      ${IP_RANGE_OBJECT_NAME}
#    Lists Should Be Equal       ${Configured_Items_for_Object_Profile}      ${Get_Items_Of_Object_Profile}


