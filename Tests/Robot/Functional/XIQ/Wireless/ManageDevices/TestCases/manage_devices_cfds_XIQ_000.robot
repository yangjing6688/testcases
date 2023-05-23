# Author        : skp
# Date          : April 2023
# Description   : Manage Devices Testcases
#
# Topology      :
# Host ----- Cloud

*** Variables ***
${CLI_ERROR_CMD}            testerrormessage
${NW_POLICY_NAME}           Openauthssid
${SSID_NAME}                Openauthssid
${SSID_NAME_NEW}            Openauthssid_automation
${NW_POLICY_DUAL_RADIO}     Openauthdualradio
${SSID_DUAL_RADIO}          Openauthdualradio
${SSID_DUAL_RADIO_NW}       Openauthdualradiosecondnw
${DEVICE_MAKE}              Extreme - Aerohive
${LOCATION}                 auto_location_01, San Jose, building_01, floor_01
${LOCATION_DISPLAY}         auto_location_01 >> San Jose >> building_01 >> floor_01
${DEFAULT_POLICY_NAME}      default_network_policy
${INTERFACE_TYPE}           WIFI0
${STATUS}                   OFF
${COLUMN_PICKER_WAN_IP}     WAN IP Address
${COLUMN_PICKER_MGMT_IP}    MGT IP Address
${TOOLTIP_MESSAGE}          Can not get the required device list.
${WIFI0_RADIO_PROFILE}      radio_ng_11ax-2g
${WIFI1_RADIO_PROFILE}      radio_ng_11ax-5g
${AP1_DEVICE_TEMPLATE}      ap1_second_template


*** Settings ***
Library     common/Utils.py
Library     extauto/common/Utils.py
Library     extauto/common/Cli.py
Library     common/Mu.py
Library     Collections
Library     String

# The keywords in Login.py have been moved to the keywords directory.
# If the moved keyword is not working correctly import the original library and remove the keywords/gui/login/KeywordsLogin.py version.
#Library     xiq/flows/common/Login.py
Library     keywords/gui/login/KeywordsLogin.py
Library     xiq/flows/common/DeviceCommon.py
Library     xiq/flows/common/Navigator.py

Library     xiq/flows/configure/DeviceTemplate.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/configure/CommonObjects.py
Library     xiq/flows/configure/ExpressNetworkPolicies.py

Library     xiq/flows/manage/DeviceConfig.py
Library     xiq/flows/manage/DevicesActions.py
Library     xiq/flows/manage/Client.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/DeviceCliAccess.py
Library     xiq/flows/manage/Device360.py
Library     xiq/flows/manage/FilterManageDevices.py
Library     xiq/flows/manage/Location.py

Library     xiq/flows/globalsettings/GlobalSetting.py

Library     xiq/flows/mlinsights/Network360Plan.py
Library     ExtremeAutomation/Imports/CommonObjectUtils.py
Library     extauto/common/TestFlow.py
Library     ExtremeAutomation/Keywords/UserDefinedKeywords/NetworkElements/SetupTeardown/SetupTeardownUdks.py
Library     extauto.xiq.flows.manage.EspAlert

Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml
Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}

Resource    Tests/Robot/Functional/XIQ/Wireless/ManageDevices/Resources/manage_devices_cfds_config_XIQ_000.robot
Suite Setup      Pre Condition
Force Tags       testbed_2_node

*** Keywords ***
Pre Condition
    [Documentation]   This section onboards 2 APs and assigns default policy to those APs
    # Use this method to convert the ap, wing, netelem to a generic device object
    # device1       => device1
    # wing1     => device1
    # netelem1  => device1 (EXOS / VOSS)
    Convert To Generic Device Object    device      index=1     look_for_device_type=ap     set_to_index=1
    Convert To Generic Device Object    device      index=2     look_for_device_type=ap     set_to_index=2

    # Create the connection to the device
    Base Test Suite Setup
    Set Global Variable     ${device1_spawn}            ${device1.name}
    Set Global Variable     ${device2_spawn}            ${device2.name}

    ${result}=          Login User          ${TENANT_USERNAME}     ${TENANT_PASSWORD}

    ${devices}       Create List        ${device1}        ${device2}
    FOR     ${device}   IN    @{devices}
        ${DELETE_DEVICE_STATUS}=        Delete Device       device_serial=${device}[serial]
        should be equal as integers     ${DELETE_DEVICE_STATUS}               1

        ${ONBOARD_STATUS}               Onboard Device Quick    ${device}
        should be equal as integers     ${ONBOARD_STATUS}       1

        ${SEARCH_RESULT}=               Search Device    device_serial=${device}[serial]
        should be equal as integers     ${SEARCH_RESULT}        1
    END

    ${CONF_RESULT1}=         Configure Device To Connect To Cloud            ${device1.cli_type}     ${generic_capwap_url}   ${device1_spawn}
    Should Be Equal As Integers     ${CONF_RESULT1}          1

    ${CONF_RESULT2}=         Configure Device To Connect To Cloud            ${device2.cli_type}     ${generic_capwap_url}   ${device2_spawn}
    Should Be Equal As Integers     ${CONF_RESULT2}          1

    FOR     ${device}   IN    @{devices}
        ${ONLINE_STATUS}=       Wait Until Device Online    ${device}[serial]
        Should Be Equal As Integers     ${ONLINE_STATUS}        1

        ${DEVICE_STATUS}=       Get Device Status           device_mac=${device}[mac]
        Should Contain Any       ${DEVICE_STATUS}           green   config audit mismatch
    END

    ${CREATE_DEFAULT_POLICY}        Create Network Policy If Does Not Exist     ${DEFAULT_POLICY_NAME}     ${CONFIG_PUSH_OPEN_NW_01}
    Should Be Equal As Strings      '${CREATE_DEFAULT_POLICY}'   '1'

    ${UPADATE_AP1}      Update Network Policy To AP     ${DEFAULT_POLICY_NAME}      ap_serial=${device1.serial}
    Should Be Equal As Strings      '${UPADATE_AP1}'       '1'

    ${UPADATE_AP2}      Update Network Policy To AP     ${DEFAULT_POLICY_NAME}      ap_serial=${device2.serial}
    Should Be Equal As Strings      '${UPADATE_AP2}'       '1'

    ${DELETE_POLICIES}      Delete Network Polices          ${NW_POLICY_NAME}   ${NW_POLICY_DUAL_RADIO}
    Should Be Equal As Strings      '${DELETE_POLICIES}'       '1'

    ${DELETE_SSIDS}         Delete SSIDs                    ${SSID_NAME}  ${SSID_NAME_NEW}  ${SSID_DUAL_RADIO}  ${SSID_DUAL_RADIO_NW}
    Should Be Equal As Strings      '${DELETE_SSIDS}'       '1'

    Logout User
    Quit Browser

Test Case Level Cleanup
    ${UPADATE_AP1}      Update Network Policy To AP     ${DEFAULT_POLICY_NAME}     ap_serial=${device1.serial}
    Should Be Equal As Strings      '${UPADATE_AP1}'       '1'

    ${UPADATE_AP2}      Update Network Policy To AP     ${DEFAULT_POLICY_NAME}     ap_serial=${device2.serial}
    Should Be Equal As Strings      '${UPADATE_AP2}'        '1'

    ${DELETE_POLICIES}  Delete Network Polices          ${NW_POLICY_NAME}
    Should Be Equal As Strings      '${DELETE_POLICIES}'       '1'

    ${DELETE_TEMPLATE1}     Delete AP Template Profile      ${device1.template}
    Should Be Equal As Strings      '${DELETE_TEMPLATE1}'       '1'

    ${DELETE_TEMPLATE2}     Delete AP Template Profile      ${AP1_DEVICE_TEMPLATE}
    Should Be Equal As Strings      '${DELETE_TEMPLATE2}'       '1'

    ${DELETE_SSIDS}     Delete SSIDs                    ${SSID_NAME}  ${SSID_NAME_NEW}
    Should Be Equal As Strings      '${DELETE_SSIDS}'       '1'

    Logout User
    Quit Browser

*** Test Cases ***
TCCS-6920: CFD-4618 The CLI access popup page is closed when dismissing the error message returned for a wrongly inputted CLI
    [Documentation]         The CLI access popup page is closed when dismissing the error message returned for a wrongly inputted CLI
    [Tags]                  p2   regression   manage-device   tccs_6920
    ${LOGIN_XIQ} =                  Login User          ${TENANT_USERNAME}      ${TENANT_PASSWORD}
    ${keyword_run_status}      ${CHECK_ERROR_MSG}=      Run keyword And Ignore Error    Send CMD On Device Advanced CLI  device_serial=${device1.serial}   cmd=${CLI_ERROR_CMD}
    Should Contain      ${CHECK_ERROR_MSG}      Failed to get cli command output error tooltip

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

TCCS-6854: CFD 4636 Changing Device host name should not result in Device overirde icon
    [Documentation]         Changing Device host name should not result in Device overirde icon
    [Tags]                  p3   regression   manage-device   tccs_6854
    ${LOGIN_XIQ} =                  Login User          ${TENANT_USERNAME}      ${TENANT_PASSWORD}

    ${CHANGE_HOST_NAME}=            Change Device Host Name    ${device1.name}_new    device_mac=${device1.mac}
    Should Be Equal As Strings      '${CHANGE_HOST_NAME}'      '1'

    ${CREATE_POLICY1}=              Create Network Policy If Does Not Exist   ${NW_POLICY_NAME}      ${OPEN_NW_01}
    Should Be Equal As Strings      '${CREATE_POLICY1}'   '1'

    ${CREATE_AP_TEMPLATE}=          add ap template from common object     ${device1.model}    ${device1.template}      ${AP_TEMPLATE_CONFIG}
    Should Be Equal As Strings      '${CREATE_AP_TEMPLATE}'   '1'

    ${UPDATE_AP_TEMPLATE}           add ap template to network policy       ${device1.template}     ${NW_POLICY_NAME}
    Should Be Equal As Integers      ${UPDATE_AP_TEMPLATE}       1

    ${AP1_UPDATE_CONFIG}=           Update Network Policy To AP   ${NW_POLICY_NAME}     ap_serial=${device1.serial}
    Should Be Equal As Strings      '${AP1_UPDATE_CONFIG}'       '1'
    sleep                           ${CONFIG_PUSH_WAIT}

    ${CHECK_HOST_NAME}=             Get Hostname Name From Device 360    device_mac=${device1.mac}
    Should Be Equal As Strings      '${CHECK_HOST_NAME}'      '${device1.name}_new'

    [Teardown]  run keywords  Change Device Host Name  ${device1.name}   device_mac=${device1.mac}
    ...     AND               Test Case Level Cleanup

TCCS-6973: CFD-4561 Verify to update a large number of APs at the same time.
    [Documentation]         Verify to update a large number of APs at the same time.
    [Tags]                  p2   regression   manage-device   tccs_6973
    ${LOGIN_XIQ} =                 Login User          ${TENANT_USERNAME}      ${TENANT_PASSWORD}

    ${CREATE_POLICY1}=             Create Network Policy If Does Not Exist   ${NW_POLICY_NAME}      ${OPEN_NW_01}
    Should Be Equal As Strings    '${CREATE_POLICY1}'   '1'

    ${AP1_UPDATE_CONFIG}=          Update Network Policy To Multiple AP   policy_name=${NW_POLICY_NAME}   ap_serial=${device1.serial},${device2.serial}
    Should Be Equal As Strings    '${AP1_UPDATE_CONFIG}'       '1'

    ${CHANGE_SSID_NAME}=           Edit Network Policy SSID   ${NW_POLICY_NAME}   ${SSID_NAME}  ${SSID_NAME_NEW}
    Should Be Equal As Strings    '${CHANGE_SSID_NAME}'       '1'

    ${CONFIG_UPDATE_SSID_CHANGE}=  Update Network Policy To Multiple AP   policy_name=${NW_POLICY_NAME}   ap_serial=${device1.serial},${device2.serial}
    Should Be Equal As Strings    '${CONFIG_UPDATE_SSID_CHANGE}'       '1'

    [Teardown]   run keywords    Test Case Level Cleanup

TCCS-6822: CFD-4520 Device 360 page is not displayed when selecting one device and clicking the Edit button
    [Documentation]         Device 360 page is not displayed when selecting one device and clicking the Edit button
    [Tags]                  p2   regression   manage-device   tccs_6822
    ${LOGIN_XIQ} =                 Login User          ${TENANT_USERNAME}      ${TENANT_PASSWORD}

    ${SYS_INFO_360_PAGE}=          Get Device System Information  device_mac=${device1.mac}

    ${HOST_NAME}=                  Get From Dictionary     ${SYS_INFO_360_PAGE}    host_name
    Should Be Equal As Strings    '${HOST_NAME}'     '${device1.name}'
    ${DEVICE_MODEL}=               Get From Dictionary     ${SYS_INFO_360_PAGE}    device_model
    Should Be Equal As Strings    '${DEVICE_MODEL}'     '${ap1.model}'
    ${DEVICE_SERIAL}=              Get From Dictionary     ${SYS_INFO_360_PAGE}    serial_number
    Should Be Equal As Strings    '${DEVICE_SERIAL}'     '${ap1.serial}'
    ${DEVICE_MAC}=                 Get From Dictionary     ${SYS_INFO_360_PAGE}    mgt0_mac
    Should Be Equal As Strings    '${DEVICE_MAC}'     '${device1.mac}'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

TCCS-6937: CFD-4383 Bulk editing of transmission power of wifi1 should not affect wifi0
    [Documentation]         CFD-4383: Bulk editing of transmission power of wifi1 should not affect wifi0
    [Tags]                  p2   regression   manage-device   tccs_6937
    ${LOGIN_XIQ} =                   Login User          ${TENANT_USERNAME}      ${TENANT_PASSWORD}

    ${CHANGE_WIFI_STATUS}=           Change Multiple Devices Wireless Interface Radio Status  device_serials=${device1.serial},${device2.serial}   interface_name=WIFI0  status=OFF
    Should Be Equal As Strings      '${CHANGE_WIFI_STATUS}'      '1'

    ${CHANGE_POWER_WIFI1}=           Change Transmission Power To Multiple Devices   device_serials=${device1.serial},${device2.serial}  interface_name=WIFI1   transmission_mode=Manual  power_value=15 dBm
    Should Be Equal As Strings      '${CHANGE_POWER_WIFI1}'      '1'

    ${UPDATE_CONFIG}=                Update Override Configuration To Multiple Devices   device_serials=${device1.serial},${device2.serial}      update_method=Delta
    Should Be Equal As Strings      '${UPDATE_CONFIG}'      '1'

    sleep  ${CONFIG_PUSH_WAIT}

    Refresh Devices Page

    ${AP1_CHECK_POWER_WIFI1}=        Get AP WIFI1 Power  ap_serial=${device1.serial}
    Run Keyword And Continue On Failure     Should Be Equal As Strings      '${AP1_CHECK_POWER_WIFI1}'      '15'

    ${AP2_CHECK_POWER_WIFI1}=        Get AP WIFI1 Power  ap_serial=${device2.serial}
    Run Keyword And Continue On Failure     Should Be Equal As Strings      '${AP2_CHECK_POWER_WIFI1}'      '15'

    ${AP1_CHECK_POWER_WIFI0}=        Get AP WIFI0 Power  ap_serial=${device1.serial}
    Run Keyword And Continue On Failure     Should Be Equal As Strings      '${AP1_CHECK_POWER_WIFI0}'      'Down'

    ${AP2_CHECK_POWER_WIFI0}=        Get AP WIFI0 Power  ap_serial=${device2.serial}
    Run Keyword And Continue On Failure     Should Be Equal As Strings      '${AP2_CHECK_POWER_WIFI0}'      'Down'

    ${AP1_CHECK_WIFI0_STATUS}=        Check WiFi Radio Status      WIFI0     device_mac=${device1.mac}
    Run Keyword And Continue On Failure     Should Be Equal As Strings      '${AP1_CHECK_WIFI0_STATUS}'      'OFF'

    ${AP2_CHECK_WIFI0_STATUS}=        Check WiFi Radio Status      WIFI0     device_mac=${device2.mac}
    Run Keyword And Continue On Failure     Should Be Equal As Strings      '${AP2_CHECK_WIFI0_STATUS}'      'OFF'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

TCCS-6869: CFD-4693 XIQ - Unable to set transmission power on wifi1 with multiple APs selected
    [Documentation]         CFD-4693 XIQ - Unable to set transmission power on wifi1 with multiple APs selected
    [Tags]                  p2   regression   manage-device   tccs_6869
    ${LOGIN_XIQ} =                   Login User          ${TENANT_USERNAME}      ${TENANT_PASSWORD}

    ${CHANGE_POWER_WIFI0}=           Change Transmission Power To Multiple Devices   device_serials=${device1.serial},${device2.serial}  interface_name=WIFI0   transmission_mode=Manual  power_value=15 dBm
    Should Be Equal As Strings      '${CHANGE_POWER_WIFI0}'      '1'

    ${CHANGE_POWER_WIFI1}=           Change Transmission Power To Multiple Devices   device_serials=${device1.serial},${device2.serial}  interface_name=WIFI1   transmission_mode=Manual  power_value=15 dBm
    Should Be Equal As Strings      '${CHANGE_POWER_WIFI1}'      '1'

    ${UPDATE_CONFIG}=                Update Override Configuration To Multiple Devices   device_serials=${device1.serial},${device2.serial}      update_method=Delta
    Should Be Equal As Strings      '${UPDATE_CONFIG}'      '1'

    sleep  ${CONFIG_PUSH_WAIT}

    Refresh Devices Page

    ${AP1_CHECK_POWER_WIFI0}=        Get AP WIFI0 Power  ap_serial=${device1.serial}
    Run Keyword And Continue On Failure     Should Be Equal As Strings      '${AP1_CHECK_POWER_WIFI0}'      '15'

    ${AP2_CHECK_POWER_WIFI0}=        Get AP WIFI0 Power  ap_serial=${device2.serial}
    Run Keyword And Continue On Failure     Should Be Equal As Strings      '${AP2_CHECK_POWER_WIFI0}'      '15'

    ${AP1_CHECK_POWER_WIFI1}=        Get AP WIFI1 Power  ap_serial=${device1.serial}
    Run Keyword And Continue On Failure     Should Be Equal As Strings      '${AP1_CHECK_POWER_WIFI1}'      '15'

    ${AP2_CHECK_POWER_WIFI1}=        Get AP WIFI1 Power  ap_serial=${device2.serial}
    Run Keyword And Continue On Failure     Should Be Equal As Strings      '${AP2_CHECK_POWER_WIFI1}'      '15'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

TCCS-7391: CFD-4423 Searched devices information do not pop up if you click on the part of the search string
    [Documentation]         CFD-4423 : Searched devices information do not pop up if you click on the part of the search string
    [Tags]                  p2   regression   manage-device   tccs_7391
    ${LOGIN_XIQ} =                 Login User          ${TENANT_USERNAME}      ${TENANT_PASSWORD}

    @{AP_NAME_PARTS}     Split String     ${device1.name}       -

    ${AP_NAME_PART_STRING1}=     Set Variable       ${AP_NAME_PARTS[0]}
    ${AP_NAME_PART_STRING2}=     Set Variable       ${AP_NAME_PARTS[1]}
    ${AP_NAME_PART_STRING3}=     Set Variable       ${AP_NAME_PARTS[2]}

    ${SEARCH_DEVICE1}=             Check Devices By Search Field   ${AP_NAME_PART_STRING1}   device_name=${device1.name}
    ${HOST_NAME}=                  Get From Dictionary     ${SEARCH_DEVICE1}    host_name
    Should Be Equal As Strings    '${HOST_NAME}'     '${device1.name}'

    ${DEVICE_MODEL}=               Get From Dictionary     ${SEARCH_DEVICE1}    device_model
    Should Be Equal As Strings    '${DEVICE_MODEL}'     '${device1.model}'

    ${DEVICE_SERIAL}=              Get From Dictionary     ${SEARCH_DEVICE1}    serial_number
    Should Be Equal As Strings    '${DEVICE_SERIAL}'     '${device1.serial}'

    ${DEVICE_MAC}=                 Get From Dictionary     ${SEARCH_DEVICE1}    mgt0_mac
    Should Be Equal As Strings    '${DEVICE_MAC}'     '${device1.mac}'

    ${SEARCH_DEVICE2}=             Check Devices By Search Field   ${AP_NAME_PART_STRING2}   device_name=${device1.name}
    ${HOST_NAME}=                  Get From Dictionary     ${SEARCH_DEVICE2}    host_name
    Should Be Equal As Strings    '${HOST_NAME}'     '${device1.name}'

    ${DEVICE_MODEL}=               Get From Dictionary     ${SEARCH_DEVICE2}    device_model
    Should Be Equal As Strings    '${DEVICE_MODEL}'     '${device1.model}'

    ${DEVICE_SERIAL}=              Get From Dictionary     ${SEARCH_DEVICE2}    serial_number
    Should Be Equal As Strings    '${DEVICE_SERIAL}'     '${device1.serial}'

    ${DEVICE_MAC}=                 Get From Dictionary     ${SEARCH_DEVICE2}    mgt0_mac
    Should Be Equal As Strings    '${DEVICE_MAC}'     '${device1.mac}'

    ${SEARCH_DEVICE3}=             Check Devices By Search Field   ${AP_NAME_PART_STRING3}   device_name=${device1.name}
    ${HOST_NAME}=                  Get From Dictionary     ${SEARCH_DEVICE3}    host_name
    Should Be Equal As Strings    '${HOST_NAME}'     '${device1.name}'

    ${DEVICE_MODEL}=               Get From Dictionary     ${SEARCH_DEVICE3}    device_model
    Should Be Equal As Strings    '${DEVICE_MODEL}'     '${device1.model}'

    ${DEVICE_SERIAL}=              Get From Dictionary     ${SEARCH_DEVICE3}    serial_number
    Should Be Equal As Strings    '${DEVICE_SERIAL}'     '${device1.serial}'

    ${DEVICE_MAC}=                 Get From Dictionary     ${SEARCH_DEVICE3}    mgt0_mac
    Should Be Equal As Strings    '${DEVICE_MAC}'     '${device1.mac}'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

TCCS-6915: CFD-4532 Manage Tab erroneously loading all devices
    [Documentation]         CFD-4532 : Manage Tab erroneously loading all devices
    [Tags]                  p2   regression   manage-device   tccs_6915
    ${LOGIN_XIQ} =                    Login User          ${TENANT_USERNAME}      ${TENANT_PASSWORD}

    ${SORT_DEVICES} =                 Sort Device Grid With MGMT IP Address    ascending
    Should Not Be Equal As Strings   '${SORT_DEVICES}'     'None'

    Sleep       3s

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

TCCS-6861: CFD-4635 Enabling dual 5 GHz causes the issue that the SSID configured on wifi0 only in the network policy stops being broadcasted
    [Documentation]         Enabling dual 5 GHz causes the issue that the SSID configured on wifi0 only in the network policy stops being broadcasted
    [Tags]                  p2   regression   manage-device   tccs_6861
    ${LOGIN_XIQ} =                   Login User          ${TENANT_USERNAME}      ${TENANT_PASSWORD}

    ${NW_STATUS}=                    Create Network Policy If Does Not Exist   ${NW_POLICY_DUAL_RADIO}   ${OPEN_NW_DUAL_RADIO_01}
    Should Be Equal As Strings       '${NW_STATUS}'   '1'

    ${ADD_WR_NW}=                    Add Wireless Nw To Network Policy    ${NW_POLICY_DUAL_RADIO}    &{OPEN_NW_DUAL_RADIO_02}
    Should Be Equal As Strings      '${ADD_WR_NW}'   '1'

    ${AP1_UPDATE_CONFIG}=            Update Network Policy To AP   ${NW_POLICY_DUAL_RADIO}     ap_serial=${device1.serial}
    Should Be Equal As Strings       '${AP1_UPDATE_CONFIG}'       '1'

    ${CHANGE_STATUS}=          Change Single Device Wireless Interface Radio Status     device_serial=${device1.serial}  interface_name=${INTERFACE_TYPE}  status=${STATUS}
    Update Device Delta Configuration       ${device1.serial}
    ${VALUE1}=          Get AP Wifi0 Power              ap_serial=${device1.serial}
    Should Be Equal As Strings      ${VALUE1}       Down
    ${VALUE2}=          Get AP Wifi1 Power              ap_serial=${device1.serial}
    Should Not Be Equal As Strings      ${VALUE2}       Down

    [Teardown]   run keywords           Update Network Policy To AP     ${DEFAULT_POLICY_NAME}     ap_serial=${device1.serial}
    ...          AND                    Delete Network Polices          ${NW_POLICY_DUAL_RADIO}
    ...          AND                    Delete SSIDs                    ${SSID_NAME}  ${SSID_NAME_NEW}  ${SSID_DUAL_RADIO}  ${SSID_DUAL_RADIO_NW}
    ...          AND                    Logout User
    ...          AND                    Quit Browser

TCCS-7587: APC-40763 Select all Functionality of multiple devices in Manage-Devices Page
    [Documentation]         APC-40763 : Select all Functionality of multiple devices in Manage-Devices Page
    [Tags]                  p2   regression   manage-device   tccs_7587
    ${LOGIN_XIQ} =                   Login User          ${TENANT_USERNAME}      ${TENANT_PASSWORD}

    ${SELECT_ALL_CHECKBOX_STATUS}=   Check Select All Devices Checkbox Status   device_serials=${device1.serial},${device2.serial}
    Should Be Equal As Strings       '${SELECT_ALL_CHECKBOX_STATUS}'       '1'

    ${DEVICE_360_AP1}=               get device system information   device_mac=${device1.mac}
    ${HOST_NAME1}=                   Get From Dictionary     ${DEVICE_360_AP1}    host_name
    Should Be Equal As Strings      '${HOST_NAME1}'     '${device1.name}'

    ${DEVICE_360_AP2}=               get device system information   device_mac=${device2.mac}
    ${HOST_NAME2}=                   Get From Dictionary     ${DEVICE_360_AP2}    host_name
    Should Be Equal As Strings      '${HOST_NAME2}'     '${device2.name}'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

TCCS-7370: CFD-4725 Verify that 'Clear Audit Mismatch' action will clear configuration audit alert icon
    [Documentation]         CFD-4725 - Verify that 'Clear Audit Mismatch' action will clear configuration audit alert icon
    [Tags]                  p2   regression   manage-device   tccs_7370
    ${LOGIN_XIQ} =                 Login User          ${TENANT_USERNAME}      ${TENANT_PASSWORD}

    ${CHANGE_HOST_NAME}=           Change Device Host Name    ${device1.name}    device_mac=${device1.mac}
    Should Be Equal As Strings     '${CHANGE_HOST_NAME}'      '1'

    ${AUDIT_STATUS}=               Get Device Configuration Audit Status   ${device1.serial}
    Should Be Equal As Strings    '${AUDIT_STATUS}'   'audit mismatch'

    ${CLEAR_AUDIT_MISMATCH}=       Clear Audit Mismatch On Device   ${device1.serial}
    Should Be Equal As Strings    '${CLEAR_AUDIT_MISMATCH}'   '1'

    sleep  10

    ${AUDIT_STATUS}=               Get Device Configuration Audit Status   ${device1.serial}
    Should Be Equal As Strings    '${AUDIT_STATUS}'   'audit match'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

TCCS-7397: CFD-4845 XIQ - Can not get the required device list error on Manage tab
    [Documentation]         CFD-4845, XIQ - "Can not get the required device list." error on Manage tab
    [Tags]                  p2   regression   manage-device  onboard  tccs_7397
    ${LOGIN_XIQ} =                  Login User          ${TENANT_USERNAME}      ${TENANT_PASSWORD}

    ${COLUMN_PICKER}=                Column Picker Select   ${COLUMN_PICKER_WAN_IP}
    Should Be Equal As Strings      '${COLUMN_PICKER}'       '1'

    ${keyword_run_status}      ${ERROR_MSG_PRESENCE}=           Run keyword And Ignore Error   Check Tooltip Message Presence  ${TOOLTIP_MESSAGE}
    Should Contain      ${ERROR_MSG_PRESENCE}       Tooltip message not seen

    ${COLUMN_PICKER2}=               Column Picker Unselect   ${COLUMN_PICKER_WAN_IP}
    Should Be Equal As Strings      '${COLUMN_PICKER2}'       '1'

    [Teardown]   run keywords       Logout User
    ...          AND                Quit Browser

TCCS-7332: CFD-5728 Manage - Devices Adding and removing columns from column picker
    [Documentation]         CFD-5728 Manage - Devices Adding and removing columns from column picker
    [Tags]                  p2   regression   manage-device   tccs_7332
    ${LOGIN_XIQ} =                    Login User          ${TENANT_USERNAME}      ${TENANT_PASSWORD}

    ${LOCATION_RESULT}=               Assign Location With Device Actions         ${device1.serial}       ${LOCATION}
    Should Be Equal As Integers       ${LOCATION_RESULT}      1       Unable to Assign Location to Device

    ${GET_AP_LOCATION}=               Get AP Assigned Location  ap_serial=${device1.serial}
    Should Contain                    ${GET_AP_LOCATION}       ${LOCATION_DISPLAY}

    ${WIFI0_RADIO_PROFILE1}=           get ap wifi0 radio profile  ap_serial=${device1.serial}
    Should Be Equal As Strings        ${WIFI0_RADIO_PROFILE1}       ${WIFI0_RADIO_PROFILE1}

    ${WIFI1_RADIO_PROFILE1}=           get ap wifi1 radio profile  ap_serial=${device1.serial}
    Should Be Equal As Strings        ${WIFI1_RADIO_PROFILE1}       ${WIFI1_RADIO_PROFILE1}

    ${AP_PUBLIC_IP}=                  get ap public ip address  ap_serial=${device1.serial}

    ${COLUMN_PICKER}=                 Column Picker UnSelect   WiFi0 Radio Profile   WiFi1 Radio Profile   Location   Public IP Address
    Should Be Equal As Strings       '${COLUMN_PICKER}'       '1'

    ${GET_AP_LOCATION1}=              Get Device Details    ${device1.serial}   LOCATION
    Should Not Contain                ${GET_AP_LOCATION1}       ${LOCATION_DISPLAY}

    ${WIFI0_RADIO_PROFILE2}=          Get Device Details    ${device1.serial}   WIFI0 RADIO PROFILE
    Should Not Be Equal As Strings    ${WIFI0_RADIO_PROFILE2}    ${WIFI0_RADIO_PROFILE1}

    ${WIFI1_RADIO_PROFILE2}=           Get Device Details    ${device1.serial}   WIFI1 RADIO PROFILE
    Should Not Be Equal As Strings     ${WIFI1_RADIO_PROFILE2}    ${WIFI1_RADIO_PROFILE1}

    ${AP_PUBLIC_IP1}=                  Get Device Details    ${device1.serial}   PUBLIC IP ADDRESS
    Should Not Be Equal As Strings        ${AP_PUBLIC_IP1}       ${AP_PUBLIC_IP}

    [Teardown]   run keywords       Column Picker Select   WiFi0 Radio Profile   WiFi1 Radio Profile   Location     Public IP Address
    ...          AND                Logout User
    ...          AND                Quit Browser


TCCS-7450: CFD-4664 The radio profiles displayed on Manage Device view is incorrect
    [Documentation]         CFD-4664-The radio profiles displayed on Manage Device view is incorrect when the
    ...                     manually assigned device template is different from the one configured in the network policy
    [Tags]                  p2   regression   manage-device    tccs_7450
    ${LOGIN_XIQ} =                   Login User          ${TENANT_USERNAME}      ${TENANT_PASSWORD}

    ${CREATE_POLICY}=                Create Network Policy If Does Not Exist   ${NW_POLICY_NAME}      ${OPEN_NW_01}
    Should Be Equal As Strings      '${CREATE_POLICY}'   '1'

    ${CREATE_AP_TEMPLATE}=          add ap template from common object     ${device1.model}    ${device1.template}      ${AP_TEMPLATE_CONFIG}
    Should Be Equal As Strings      '${CREATE_AP_TEMPLATE}'   '1'

    ${UPDATE_AP_TEMPLATE}           add ap template to network policy       ${device1.template}     ${NW_POLICY_NAME}
    Should Be Equal As Integers      ${UPDATE_AP_TEMPLATE}       1

    ${AP1_UPDATE_CONFIG}=            Update Network Policy To AP   ${NW_POLICY_NAME}     ap_serial=${device1.serial}   update_method=Complete
    Should Be Equal As Strings      '${AP1_UPDATE_CONFIG}'       '1'

    #Log to Console      Sleep for ${CONFIG_PUSH_WAIT}
    sleep                         ${CONFIG_PUSH_WAIT}

    ${DELETE_AP_TEMPLATE}           Remove AP Template From Network Policy      ${device1.template}     ${NW_POLICY_NAME}
    Should Be Equal As Integers     ${DELETE_AP_TEMPLATE}       1

    ${CREATE_AP_TEMPLATE1}=          add ap template from common object     ${device1.model}    ${AP1_DEVICE_TEMPLATE}      ${AP_TEMPLATE_CONFIG}
    Should Be Equal As Strings      '${CREATE_AP_TEMPLATE}'   '1'

    ${UPDATE_AP_TEMPLATE1}           add ap template to network policy       ${AP1_DEVICE_TEMPLATE}     ${NW_POLICY_NAME}
    Should Be Equal As Integers      ${UPDATE_AP_TEMPLATE1}       1

    ${CHANGE_TEMPLATE}=              Override Config Device Template   ${AP1_DEVICE_TEMPLATE}   device_mac=${device1.mac}
    Should Be Equal As Strings      '${CHANGE_TEMPLATE}'   '1'

    ${UPDATE_CONFIG}=                Update Device Delta Configuration   ${device1.serial}   update_method=Complete
    Should Be Equal As Strings      '${UPDATE_CONFIG}'   '1'

    sleep                         ${CONFIG_PUSH_WAIT}
    wait until device online         ${device1.serial}

    ${CHECK_TEMPLATE_NAME}=          Check Device Configured Template   device_mac=${device1.mac}
    Should Be Equal As Strings       '${CHECK_TEMPLATE_NAME}'   '${AP1_DEVICE_TEMPLATE}'

    [Teardown]   run keywords   Test Case Level Cleanup