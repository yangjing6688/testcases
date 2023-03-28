# Author        : Kiran
# Date          : Dec22,2022
# Description   : Extreme Location Brownfield setup cases
#
# NOTE1: This script involves manual effort as well, please refer this wiki - https://wiki.iq.extremenetworks.com/wiki/pages/viewpage.action?pageId=99811442
# NOTE2: This script should be run if the XIQ account is not subscribed to XLOC, also if XIQ account does not have network policy/ssid/template/engagement_category created
# Execution Command:
# ------------------
#  robot -L INFO -v TEST_URL:https://extremecloudiq.com/ -v TESTBED:blr_tb_1 -v DEVICE1:xloc_blr_tb2_ap460c_mu5.yaml -v TOPO:XLOC_Brownfield_topo XLOC_Brownfield_Setup_MD-1676.robot


*** Variables ***
${LOCATION}                 auto_location_01, San Jose, building_01, floor_02
${NW_POLICY_NAME}           xloc_prod_sanity_nw_pol
${SSID_NAME}                xloc_prod_sanity_ssid
${BUILDING_NAME}            building_01
${FLOOR_NAME}               floor_02
${MAP_FILE_NAME}            auto_location_01_1595321828282.tar.gz
${EN_CATEGORY_NAME}         xloc_prod_sanity_en_cat
${EN_CATEGORY_THRESHOLD}    5
${XLOC_SITE_NAME}           building_01

*** Settings ***

Force Tags   testbed_3_node

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

*** Test Cases ***
Test1: Setup Brownfield account in XIQ for XLOC Validations
    [Tags]    tccs_14109            development

    ${result}=                      Login User          ${tenant_username}     ${tenant_password}

    ${IMPORT_MAP}=                  Import Map In Network360Plan  ${MAP_FILE_NAME}
    Should Be Equal As Strings      '${IMPORT_MAP}'              '1'

    ${ONBOARD_RESULT}=              onboard device quick      ${ap1}
    Should be equal as integers     ${ONBOARD_RESULT}       1

    ${AP_SPAWN}=        Open Spawn          ${ap1.console_ip}   ${ap1.console_port}      ${ap1.username}       ${ap1.password}        ${ap1.cli_type}
    Should not be equal as Strings      '${AP_SPAWN}'        '-1'

    ${CONF_STATUS_RESULT}=      Configure Device To Connect To Cloud      ${ap1.cli_type}         ${capwap_url}       ${AP_SPAWN}
    Should Be Equal As Strings                  ${CONF_STATUS_RESULT}       1

    ${WAIT_STATUS_RESULT}=      Wait for Configure Device to Connect to Cloud       ${ap1.cli_type}         ${capwap_url}       ${AP_SPAWN}
    Should Be Equal As Strings                  ${WAIT_STATUS_RESULT}       1

    ${CONNECTED_STATUS}=    Wait Until Device Online                ${ap1.serial}
    Should Be Equal as Integers             ${CONNECTED_STATUS}          1

    ${DEVICE_STATUS}=       Get Device Status       device_serial=${ap1.serial}
    Should contain any  ${DEVICE_STATUS}    green     config audit mismatch

    ${CREATE_POLICY1}=              Create Network Policy   ${NW_POLICY_NAME}      &{LOCATION_OPEN_NW}
    Should Be Equal As Strings      '${CREATE_POLICY1}'   '1'

    ${CREATE_AP_TEMPLATE}=          Add AP Template     ${ap1.model}    ${ap1.template_name}    ${AP_TEMPLATE_CONFIG}
    Should Be Equal As Strings      '${CREATE_AP_TEMPLATE}'   '1'

    ${ENABLE_PRESENCE}=          Enable Nw Presence Analytics    ${NW_POLICY_NAME}
    Should Be Equal As Strings      '${ENABLE_PRESENCE}'    '1'

    ${AP1_UPDATE_CONFIG}=           Update Network Policy To AP   ${NW_POLICY_NAME}     ap_serial=${ap1.serial}   update_method=Complete
    Should Be Equal As Strings      '${AP1_UPDATE_CONFIG}'       '1'

    ${OUTPUT1}=         Send Commands       ${AP_SPAWN}         interface ble0 ibeacon enable, interface ble0 ibeacon major 5, interface ble0 ibeacon minor 5, interface ble0 ibeacon uuid 4155726F686976654E5574776F726B72, interface ble0 ibeacon advertisement-interval 120, interface ble0 ibeacon measured-power -65, interface ble0 ibeacon enable, interface ble0 ibeacon-monitor enable

    ${SUBSCRIBE_LOCATION}=          Subscribe Extreme Location Essentials
    Should Be Equal As Strings      '${SUBSCRIBE_LOCATION}'   '1'

    Close Spawn    ${AP_SPAWN}

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

Test2: Setup Brownfield account in XLOC for XLOC Validations
    [Tags]    tccs_14110            development

    ${result}=                      Login User          ${tenant_username}     ${tenant_password}

    ${Engagement_Cat}=  Create Engagement Category XLOC     ${EN_CATEGORY_NAME}     ${EN_CATEGORY_THRESHOLD}     ${XLOC_SITE_NAME}
    Should Be Equal As Strings      '${Engagement_Cat}'   '1'

    #After this step, manually login to XIQ->XLOC and perform the operations as mentioned in this wiki under brownfield_setup -> https://wiki.iq.extremenetworks.com/wiki/pages/viewpage.action?pageId=99811442

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

Test3: CleanUp of Added AP Device
    [Tags]    tccs_14111            development

    ${result}=                      Login User          ${tenant_username}     ${tenant_password}

    Delete Device                   device_serial=${ap1.serial}

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser
