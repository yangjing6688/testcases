# Author        : skp
# Date          : April ,2023
# Description   : Manage Devices Testcases
#
# Topology      :
# Host ----- Cloud

*** Variables ***
${DEVICE_MAKE}              Extreme - Aerohive
${DEFAULT_POLICY_NAME}      default_network_policy
${COLUMN_PICKER_MGMT_IP}    MGT IP Address

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
Force Tags   testbed_1_node

*** Keywords ***
Pre Condition
    [Documentation]   AP Should be onboarded  and it is online
    # Use this method to convert the ap, wing, netelem to a generic device object
    # device1       => device1
    # wing1     => device1
    # netelem1  => device1 (EXOS / VOSS)
    Convert To Generic Device Object    device      index=1     look_for_device_type=ap     set_to_index=1

    # Create the connection to the device
    Base Test Suite Setup
    Set Global Variable     ${device1_spawn}            ${device1.name}

    ${result}=          Login User          ${TENANT_USERNAME}     ${TENANT_PASSWORD}
    
    ${CREATE_DEFAULT_POLICY}        Create Network Policy If Does Not Exist     ${DEFAULT_POLICY_NAME}     ${CONFIG_PUSH_OPEN_NW_01}
    Should Be Equal As Strings      '${CREATE_DEFAULT_POLICY}'   '1'

    Logout User
    Quit Browser

Test Case Level Cleanup
    Logout User
    Quit Browser

*** Test Cases ***
TCCS-15510: Onboard Device through csv file with serial number
    [Documentation]         Onboard Device through csv file with serial number
    [Tags]                  p2   regression   manage-device  onboard  csv   tccs_15510
    ${LOGIN_XIQ} =                  Login User          ${TENANT_USERNAME}      ${TENANT_PASSWORD}

    Delete Device                   device_serial=${device1.serial}
    ${RESOURCE_PATH}                Get Suite Resource Path         ${SUITE SOURCE}
    ${CSV_FILE}=                    Set Variable               ${RESOURCE_PATH}/AP1.csv
    ${device_json_str}=             Catenate                {"onboard_device_type":"${device1.onboard_device_type}", "serial":"${device1.serial}", "device_make":"${device1.make}", "location":"${device1.location}", "csv_location":"${CSV_FILE}"}
    ${device_json}=                 get json from string    ${device_json_str}

    ${ONBOARD_AP}=                  Onboard Device Quick     ${device_json}
    Should Be Equal As Strings      ${ONBOARD_AP}       1

    ${CONF_RESULT}=                Configure Device To Connect To Cloud            ${device1.cli_type}     ${generic_capwap_url}   ${device1_spawn}
    Should Be Equal As Integers     ${CONF_RESULT}          1

    ${ONLINE_STATUS}=                Wait Until Device Online        ${device1.serial}
    Should Be Equal As Integers      ${ONLINE_STATUS}       1
    Refresh Devices Page

    ${AP1_UPDATE_CONFIG}=           Update Network Policy To AP   default_network_policy     ap_serial=${device1.serial}
    Should Be Equal As Strings      '${AP1_UPDATE_CONFIG}'       '1'
    sleep                           ${CONFIG_PUSH_WAIT}

    ${AP1_STATUS}=                   get device status       device_mac=${device1.mac}
    Should Be Equal As Strings       '${AP1_STATUS}'     'green'

    [Teardown]   run keywords       Test Case Level Cleanup

TCCS-6862: CFD-4525 Setting static IP during import from .csv not working
    [Documentation]         CFD-4525 : Setting static IP during import from .csv not working
    [Tags]                  p2   regression   manage-device  onboard  csv     tccs_6862
    ${LOGIN_XIQ} =                  Login User          ${TENANT_USERNAME}      ${TENANT_PASSWORD}

    Delete Device                   device_serial=${device1.serial}
    ${RESOURCE_PATH}                Get Suite Resource Path         ${SUITE SOURCE}
    ${CSV_FILE}=                    Set Variable               ${RESOURCE_PATH}/CFD-4525.csv
    ${device_json_str}=             Catenate                {"onboard_device_type":"${device1.onboard_device_type}", "serial":"${device1.serial}", "device_make":"${device1.make}", "location":"${device1.location}", "csv_location":"${CSV_FILE}"}
    ${device_json}=                 get json from string    ${device_json_str}

    ${ONBOARD_AP}=                  Onboard Device Quick     ${device_json}
    Should Be Equal As Strings      ${ONBOARD_AP}       1

    ${CONF_RESULT}=                Configure Device To Connect To Cloud            ${device1.cli_type}     ${generic_capwap_url}   ${device1_spawn}
    Should Be Equal As Integers     ${CONF_RESULT}          1

    ${ONLINE_STATUS}=                Wait Until Device Online        ${device1.serial}
    Should Be Equal As Integers      ${ONLINE_STATUS}       1
    Refresh Devices Page

    ${AP1_UPDATE_CONFIG}=           Update Network Policy To AP   default_network_policy     ap_serial=${device1.serial}
    Should Be Equal As Strings      '${AP1_UPDATE_CONFIG}'       '1'
    #Log to Console      Sleep for   ${CONFIG_PUSH_WAIT}
    sleep                           ${CONFIG_PUSH_WAIT}

    ${AP1_STATUS}=                   get device status       device_mac=${device1.mac}
    Should Be Equal As Strings       '${AP1_STATUS}'     'green'

    ${COLUMN_PICKER}=                Column Picker Select   ${COLUMN_PICKER_MGMT_IP}
    Should Be Equal As Strings      '${COLUMN_PICKER}'       '1'

    ${AP_MGMT_IP}=                   Get Device Management IP Address     device_mac=${device1.mac}
    Should Be Equal As Strings      '${AP_MGMT_IP}'     '${device1.ip}'

    [Teardown]   run keywords       Test Case Level Cleanup