# Author        : Kamalesh
# Date          : Sep21,2022
# Description   : Extreme Location GreenField testacses
#
# Topology      :
# AP1----- Cloud-----Ubuntu(MU1)

# Pre-Condtion
# 1. AP1 should be onboarded and it should be in online in XIQ.
# 2. AP1 and Client1 should Present Inside RF Box Environment
# 3. For Running Test3 Need to create Category Creation Manually one time on Customer1 Account with Name "xloc_prod_sanity_en_cat" and assign to site "building_01"

# Execution Command:
# ------------------
#  robot -L INFO -v TEST_URL:https://g2.qa.xcloudiq.com/login -v TESTBED:blr_tb_2 -v DEVICE1:AP460C_RF_BOX_001 -v TOPO:XLOC_topo XLOC_Greenfield_MD-1164.robot

*** Variables ***
${LOCATION}                 auto_location_01, San Jose, building_01, floor_02
${NW_POLICY_NAME}           automation_xloc_gf_policy
${SSID_NAME}                automation_xloc_gf_ssid
${BUILDING_NAME}            building_01
${FLOOR_NAME}               floor_02
${MAP_FILE_NAME}            auto_location_01_1595321828282.tar.gz
${service_name}             greenfield_ibeacon
${uuid}                     475f2a85-c938-46de-b2b1-da36b8114e43
${uuid1}                    952f2a85-c938-46de-b2b1-da36b8114e43


*** Settings ***
Force Tags      testbed_1_node
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

Library     xiq/flows/manage/Client.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/Location.py

Library     xiq/flows/configure/Wips.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/configure/CommonObjects.py
Library     xiq/flows/configure/DeviceTemplate.py

Library     xiq/flows/globalsettings/GlobalSetting.py

Library     xiq/flows/mlinsights/Network360Plan.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml


Resource     Tests/Robot/Functional/XIQ/Wireless/Sanity/Resources/extreme_location_sanity_config.robot
Resource     Tests/Robot/Functional/XIQ/Wireless/Sanity/Resources/extreme_location_sanity_variable.robot

Suite Setup      Pre Condition

*** Keywords ***
Pre Condition
    [Documentation]   AP Should be onboarded  and it is online
    
    ${result}=                       Login User          ${TENANT_USERNAME}     ${TENANT_PASSWORD}   url=${TEST_URL}    map_override=${MAP_FILE_NAME}

    Onboard AP          ${ap1.serial}       ${ap1.make}        ${LOCATION}
    
    ${AP_SPAWN}=        Open Spawn          ${ap1.ip}   ${ap1.port}      ${ap1.username}       ${ap1.password}        ${ap1.cli_type}
    Set Suite Variable  ${AP_SPAWN}

    ${OUTPUT0}=         Send Commands       ${AP_SPAWN}         capwap client server name ${CAPWAP_URL}, capwap client default-server-name ${CAPWAP_URL}, capwap client server backup name ${CAPWAP_URL}, no capwap client enable, capwap client enable, save config
    
    Wait Until Device Online                ${ap1.serial}

    Refresh Devices Page
    
    ${AP1_STATUS}=                  Get AP Status       ap_mac=${ap1.mac}
    Should Be Equal As Strings      '${AP1_STATUS}'     'green'

    ${CREATE_POLICY1}=              Create Network Policy   ${NW_POLICY_NAME}      &{LOCATION_OPEN_NW}
    Should Be Equal As Strings      '${CREATE_POLICY1}'   '1'
    
    ${CREATE_AP_TEMPLATE}=          Add AP Template    ${ap1.model}    ${AP_template_name}    &{AP_TEMPLATE_CONFIG}
    Should Be Equal As Strings      '${CREATE_AP_TEMPLATE}'   '1'

    Enable Nw Presence Analytics    ${NW_POLICY_NAME}

    ${AP1_UPDATE_CONFIG}=           Update Network Policy To AP   ${NW_POLICY_NAME}     ap_serial=${ap1.serial}   update_method=Complete
    Should Be Equal As Strings      '${AP1_UPDATE_CONFIG}'       '1'

    Wait Until Device Online       ${ap1.serial}

    ${SUBSCRIBE_LOCATION}=          Subscribe Extreme Location Essentials
    Should Be Equal As Strings      '${SUBSCRIBE_LOCATION}'   '1'

    Create Asset Category XLOC    ${AS_CATEGORY_NAME}     ${XLOC_SITE_NAME}

    ${OUTPUT1}=         Send Commands       ${AP_SPAWN}         interface ble0 ibeacon enable, interface ble0 ibeacon major 5, interface ble0 ibeacon minor 5, interface ble0 ibeacon uuid 4155726F686976654E5574776F726B72, interface ble0 ibeacon advertisement-interval 120, interface ble0 ibeacon measured-power -65, interface ble0 ibeacon enable, interface ble0 ibeacon-monitor enable

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

*** Test Cases ***

TCEL-3046: Create ibeacon with long name upto 32 characters	

    [Documentation]         Create ibeacon with long name upto 32 characters

    [Tags]                  development    tcel_3046
    
    ${result}=                      Login User          ${TENANT_USERNAME}     ${TENANT_PASSWORD}   url=${TEST_URL}        
    
    ${CREATE_BECON}=           Create XLOC Third Party Ibeacon   ${IBEACON_NAME_32}    ${uuid}   ${XLOC_SITE_NAME}   ${AS_CATEGORY_NAME}   ${IBEACON_MAC_ADDRESS}    major_version=0    minor_version=0

    Should Be Equal As Strings      '${CREATE_BECON}'       '1'

    [Teardown]   run keywords       switch_to_extreme_location_window
    ...                             close_extreme_location_window
    ...                             Go back To XLOC

TCEL-3047: Create ibeacon with uuid and leave blank for major and minor
    
    [Documentation]         Create ibeacon with uuid and leave blank for major and minor

    [Tags]                  development    tcel_3047

    ${CREATE_BECON}=           Create XLOC Third Party Ibeacon   ${IBEACON_NAME_32}    ${uuid}   ${XLOC_SITE_NAME}   ${AS_CATEGORY_NAME}   ${IBEACON_MAC_ADDRESS1}

    Should Be Equal As Strings      '${CREATE_BECON}'       '-1'

    [Teardown]   run keywords       switch_to_extreme_location_window
    ...                             close_extreme_location_window
    ...                             Go back To XLOC

TCEL-3048: Create ibeacon with uuid, major and leave blank for minor	

    [Documentation]         Create ibeacon with uuid, major and leave blank for minor

    [Tags]                  development    tcel_3048

    ${CREATE_BECON}=           Create XLOC Third Party Ibeacon   ${IBEACON_NAME_32}    ${uuid}   ${XLOC_SITE_NAME}   ${AS_CATEGORY_NAME}   ${IBEACON_MAC_ADDRESS1}    major_version=1
    
    Should Be Equal As Strings      '${CREATE_BECON}'       '-1'

    [Teardown]   run keywords       switch_to_extreme_location_window
    ...                             close_extreme_location_window
    ...                             Go back To XLOC

TCEL-3049: Create ibeacon with uuid, minor and leave blank for major	

    [Documentation]         Create ibeacon with uuid, minor and leave blank for major

    [Tags]                  development    tcel_3049

    ${CREATE_BECON}=           Create XLOC Third Party Ibeacon   ${IBEACON_NAME_32}    ${uuid}   ${XLOC_SITE_NAME}   ${AS_CATEGORY_NAME}   ${IBEACON_MAC_ADDRESS1}    minor_version=0
    
    Should Be Equal As Strings      '${CREATE_BECON}'       '-1'

    [Teardown]   run keywords       switch_to_extreme_location_window
    ...                             close_extreme_location_window
    ...                             Go back To XLOC

TCEL-3050: Create ibeacon with uuid, major and minor number	

    [Documentation]         Create ibeacon with uuid, major and minor number

    [Tags]                  development    tcel_3050

    ${CREATE_BECON}=           Create XLOC Third Party Ibeacon   ${IBEACON_NAME_1}    ${uuid}   ${XLOC_SITE_NAME}   ${AS_CATEGORY_NAME}   ${IBEACON_MAC_ADDRESS1}    major_version=1    minor_version=1

    [Teardown]   run keywords       switch_to_extreme_location_window
    ...                             close_extreme_location_window
    ...                             Go back To XLOC

TCEL-3052: Check editing of ibeacon

    [Documentation]         Check editing of ibeacon

    [Tags]                  development    tcel_3052

    Edit Ibeacon in XLOC    ${IBEACON_MAC_ADDRESS1}    ${uuid1}    major_version=2    minor_version=2

    [Teardown]   run keywords       switch_to_extreme_location_window
    ...                             close_extreme_location_window
    ...                             Go back To XLOC


TCEL-3053: Check deleting of ibeacon	
    
    [Documentation]         Check deleting of ibeacon

    [Tags]                  development    tcel_3053

    ${DELETE_IBEACON}=                      Delete ibeacon in xloc    ${IBEACON_MAC_ADDRESS1}

    Should Be Equal As Strings      '${DELETE_IBEACON}'       '1' 
    
    [Teardown]   run keywords       switch_to_extreme_location_window
    ...                             close_extreme_location_window
    ...                             Go back To XLOC


TCEL-3054: Create ibeacon with mac, uuid, major and minor and check status as "online"	
    
    [Documentation]         Create ibeacon with mac, uuid, major and minor and check status as "online"

    [Tags]                  development    tcel_3054

    ${CREATE_BECON}=           Create XLOC Third Party Ibeacon   ${IBEACON_NAME_WORK}    ${UUID_WORK}   ${XLOC_SITE_NAME}   ${AS_CATEGORY_NAME}   ${BEACON_MAC_ADDRESS_WORK}    major_version=1    minor_version=1

    ${DEVICE_STATUS}=           Get ibeacon Status       ${BEACON_MAC_ADDRESS_WORK}
    Should Be Equal As Strings      '${DEVICE_STATUS}'       '1'

    [Teardown]   run keywords       switch_to_extreme_location_window
    ...                             close_extreme_location_window
    ...                             Go back To XLOC


TCEL-3055: Create ibeacon with incorrect mac, uuid, major and minor and check status as "offline"	
	
    [Documentation]         Create ibeacon with incorrect mac, uuid, major and minor and check status as "offline"
    
    [Tags]                  development    tcel_3055
    
    ${CREATE_BECON}=           Create XLOC Third Party Ibeacon   ${IBEACON_NAME_32}    ${uuid}   ${XLOC_SITE_NAME}   ${AS_CATEGORY_NAME}   ${IBEACON_MAC_ADDRESS3}    major_version=1    minor_version=1

    ${DEVICE_STATUS}=           Get ibeacon Status       ${IBEACON_MAC_ADDRESS3}
    Should Be Equal As Strings      '${DEVICE_STATUS}'       '-1'

    [Teardown]   run keywords       switch_to_extreme_location_window
    ...                             close_extreme_location_window
    ...                             Go back To XLOC

TCEL-3056: Check downloading ibeacon page in CSV format	

    [Documentation]         Create ibeacon with incorrect mac, uuid, major and minor and check status as "offline"

    [Tags]                  development    tcel_3046
    
    ${DOWNLOAD_REPORT}=           Download Ibeacon Report
    Should Be Equal As Strings      '${DOWNLOAD_REPORT}'       '1'

    [Teardown]   run keywords       switch_to_extreme_location_window
    ...                             close_extreme_location_window
    ...                             Go back To XLOC

TCEL-3057: Reset VIQ
    
    [Documentation]         Reset Customer Account Data

    [Tags]                  development    tccs_13022

    #Step1: Perform BackUp VIQ
    ${BACKUP_VIQ_DATA}=             Backup VIQ Data
    Should Be Equal As Strings      '${BACKUP_VIQ_DATA}'              '1'

    ${LOGOUT_XIQ}=                   Logout User

    ${QUIT_BROWSER}=                   Quit Browser

    BuiltIn.Sleep  30 seconds

    #Step2: Perform Reset VIQ
    ${LOGIN_XIQ}=                   Login User          ${TENANT_USERNAME}      ${TENANT_PASSWORD}      url=${TEST_URL}
    Should Be Equal As Strings      '${LOGIN_XIQ}'     '1'

    ${RESET_VIQ_DATA}=               Reset VIQ Data

    Should Be Equal As Strings      '${RESET_VIQ_DATA}'              '1'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser
