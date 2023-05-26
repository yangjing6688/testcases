# Author        : Shreen
# Date          : Mar 2023
# Description   : Cloud Config Group

# Topology      :
# Client -----> AP --->XIQ Instance
# Pre-Condtion
# 1. AP should be onboarded and it is online

# Execution Command :
# robot -L INFO -v TESTBED:blr_tb_1 -v DEVICE1:AP460C -v DEVICE2:AP630 -v ap3:AP410C -v TOPO:topo-1   cloud_config_group.robot
# robot -v TESTBED:xiq_blr_tb3_ap410c_mu1.yaml -v ENV:environment.local.chrome.yaml -v TOPO:topo.test.g2r1.xim.blrtb2.automation.yaml ap_cloud_config_group_sanity-000.robot
# Select the "TESTBED" ,"TOPO" and "DEVICE" variable based on Test bed
*** Variables ***
# Arguments passed from the command line

${EMPTY}
${CCG_DESC1}                        CCG Group for AutoCCG1234567890123456789012345
${CCG_DESC2}                        CCG Group for   CCG_MANAGE
${CCG_DUPLICATE_DESC}               CCG Group for CCG_DUPLICATE
${RULE1_DESC}                       Classification Rule for CLASSIFICATION_CCG
${MATCH_FLAG}                       YES
${LOCATION}                         auto_location_01, Santa Clara, building_02, floor_04

*** Settings ***
Library     common/Utils.py
Library     extauto/common/Cli.py
Library     extauto/common/TestFlow.py
Library     common/LoadBrowser.py
# The keywords in Login.py have been moved to the keywords directory.
# If the moved keyword is not working correctly import the original library and remove the keywords/gui/login/KeywordsLogin.py version.
#Library     xiq/flows/common/Login.py
Library     keywords/gui/login/KeywordsLogin.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/Device360.py
Library     xiq/flows/manage/DeviceCliAccess.py
Library     xiq/flows/configure/UserGroups.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/configure/CommonObjects.py
Library     xiq/flows/configure/CloudConfigGroup.py
Library     xiq/flows/configure/ClassificationRule.py
Library     xiq/flows/manage/Location.py
Library     xiq/flows/globalsettings/GlobalSetting.py
Library     extauto/common/Utils.py
Library     ExtremeAutomation/Imports/CommonObjectUtils.py
Library     ExtremeAutomation/Keywords/UserDefinedKeywords/NetworkElements/SetupTeardown/SetupTeardownUdks.py

Variables   Tests/Robot/Functional/XIQ/Wireless/Sanity/Resources/ap_cloud_config_group_config.py


Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/device_commands.yaml
Variables    Environments/Config/waits.yaml

Force Tags   testbed_3_node
Suite Setup      Pre Condition
Suite Teardown    Run Keyword And Warn On Failure  Test Suite Cleanup

*** Keywords ***
Pre Condition
    [Documentation]     Cleanup before running the suite
    [Tags]      production  cleanup

    ${device}=      Create Dictionary
    ...     name=simulated_dut08
    ...     model=AP120
    ...     simulated_count=1
    ...     onboard_device_type=Simulated
    ...     location=auto_location_01, Santa Clara, building_02, floor_04

    Log To Console      DOING CLEANUP BEFORE RUNNING THE SUITE!

    # Use this method to convert the ap, wing, netelem to a generic device object
    # ap1      => device1
    # wing1    => device1
    # netelem1 => device1 (EXOS/VOSS)
    Convert To Generic Device Object    device      index=1     look_for_device_type=ap     set_to_index=1

    # Create the connection to the device
    Base Test Suite Setup
    Set Global Variable     ${MAIN_DEVICE_SPAWN}            ${device1.name}

    ${LOGIN_RESULT}=            Login User                  ${tenant_username}      ${tenant_password}      check_warning_msg=True
    Should Be Equal As Integers     ${LOGIN_RESULT}         1

    ${SEARCH_RESULT}=           Search Device               device_serial=${device1.serial}     ignore_failure=True
    IF  ${SEARCH_RESULT} == 1
        ${DISCONNECT_DEVICE_RESULT}=    Disconnect Device From Cloud        ${device1.cli_type}      ${MAIN_DEVICE_SPAWN}
        Should Be Equal As Integers     ${DISCONNECT_DEVICE_RESULT}         1

        ${DELETE_DEVICE_RESULT}=        Delete Device                       device_serial=${device1.serial}
        Should Be Equal As Integers     ${DELETE_DEVICE_RESULT}             1
    END

    ${CONF_RESULT}=         Configure Device To Connect To Cloud            ${device1.cli_type}     ${generic_capwap_url}   ${MAIN_DEVICE_SPAWN}
    Should Be Equal As Integers     ${CONF_RESULT}          1

    ${ONBOARD_RESULT}=      Onboard Device Quick        ${device1}
    Should Be Equal As Strings      ${ONBOARD_RESULT}       1

    ${WAIT_CONF_RESULT}=    Wait For Configure Device To Connect To Cloud   ${device1.cli_type}     ${generic_capwap_url}   ${MAIN_DEVICE_SPAWN}
    Should Be Equal As Integers     ${WAIT_CONF_RESULT}     1

    ${ONLINE_STATUS}=       Wait Until Device Online    ${device1.serial}
    Should Be Equal As Integers     ${ONLINE_STATUS}        1

    ${MANAGED_STATUS}=      Wait Until Device Managed   ${device1.serial}
    Should Be Equal As Integers     ${MANAGED_STATUS}       1

    ${DEVICE_STATUS_RESULT}=       Get Device Status           device_mac=${device1.mac}
    Should contain any                  ${DEVICE_STATUS_RESULT}    green     config audit mismatch

    #Upgrade the device to latest/supported version to avoid config push issues.
    ${LATEST_VERSION}=      Upgrade Device      ${device1}
    Should Not be Empty     ${LATEST_VERSION}

    Sleep                   ${ap_reboot_wait}

    ${REBOOT_STATUS}=    Wait Until Device Reboots               ${device1.serial}
    Should Be Equal as Integers             ${REBOOT_STATUS}          1

    ${CONNECTED_STATUS}=    Wait Until Device Online                ${device1.serial}       retry_count=15
    Should Be Equal as Integers             ${CONNECTED_STATUS}          1

    set suite variable    ${device}

    ${ONBOARD_RESULT_SIM}=                  onboard device quick    ${device}
    Should Be Equal As Strings              ${ONBOARD_RESULT_SIM}       1

    ${DELETE_POLICIES_RESULT}=      Delete Network Policy          ${NETWORK}
    Should Be Equal As Integers     ${DELETE_POLICIES_RESULT}           1

    ${DELETE_SSID_RESULT}=          Delete SSIDs                    ${CONFIG_PUSH_SSID}
    Should Be Equal As Integers     ${DELETE_SSID_RESULT}               1

    ${RULE_DELETE_RESULT}=          Delete single classification rule     ${RULE1_NAME}
    Should Be Equal As Integers     ${RULE_DELETE_RESULT}               1

    ${CCG_DELETE_RESULT}=           Delete cloud config groups      ${CCG_NAME1}    ${CCG_DUPLICATE}    ${CCG_NAME2}
    Should Be Equal As Integers     ${CCG_DELETE_RESULT}               1

Test Suite Cleanup
    [Documentation]     Cleanup after running the suite
    [Tags]      production  cleanup

    Log To Console      DOING CLEANUP AFTER RUNNING THE SUITE!

    ${SEARCH_RESULT}=   Search Device               device_serial=${device1.serial}     ignore_failure=True
    IF  ${SEARCH_RESULT} == 1
        ${DISCONNECT_DEVICE_RESULT}=    Disconnect Device From Cloud        ${device1.cli_type}     ${MAIN_DEVICE_SPAWN}
        Should Be Equal As Integers     ${DISCONNECT_DEVICE_RESULT}         1

        ${DELETE_DEVICE_RESULT}=        Delete Device                       device_serial=${device1.serial}
        Should Be Equal As Integers     ${DELETE_DEVICE_RESULT}             1
    END

    ${DELETE_DEVICE_STATUS}=        Run Keyword If  'serial' in ${device}    Delete Device  device_serial=${device.serial}
    should be equal as integers     ${DELETE_DEVICE_STATUS}               1

    ${DELETE_POLICIES_RESULT}=      Delete Network Policy          ${NETWORK}
    Should Be Equal As Integers     ${DELETE_POLICIES_RESULT}           1

    ${DELETE_SSID_RESULT}=          Delete SSIDs                    ${CONFIG_PUSH_SSID}
    Should Be Equal As Integers     ${DELETE_SSID_RESULT}               1

    ${RULE_DELETE_RESULT}=          Delete single classification rule     ${RULE1_NAME}
    Should Be Equal As Integers     ${RULE_DELETE_RESULT}               1

    ${CCG_DELETE_RESULT}=           Delete cloud config groups      ${CCG_NAME1}    ${CCG_DUPLICATE}    ${CCG_NAME2}
    Should Be Equal As Integers     ${CCG_DELETE_RESULT}               1

    ${LOGOUT_RESULT}=               Logout User
    Should Be Equal As Integers     ${LOGOUT_RESULT}                1

    ${QUIT_BROWSER_RESULT}=         Quit Browser
    Should Be Equal As Integers     ${QUIT_BROWSER_RESULT}          1

*** Test Cases ***
TCCS-14511: Cloud Config group Sanity Testcase
    [Documentation]    CCG CommonObject Add Edit Delete
    [Tags]             production   tccs_14511

    ${CREATE_NW_POLICY_STATUS}=     Create Network Policy           ${NETWORK}                  ${CONFIG_PUSH_OPEN_NW_02}
    should be equal as integers     ${CREATE_NW_POLICY_STATUS}               1

    # ADD CCG Group with No APs
    ${EMPTY_CCG_STATUS}             add cloud config group      ${EMPTY}        ${CCG_DESC1}        ${device1.serial}
    should be equal as strings     '${EMPTY_CCG_STATUS}'     '-2'

    # ADD CCG Group with AP1
    ${ADD_CCG_STATUS}               add cloud config group      ${CCG_NAME1}        ${CCG_DESC1}        ${device1.serial}
    Should Be Equal As Integers     ${ADD_CCG_STATUS}            1

    # ADD CCG Group with Simulated AP
    ${ASSIGN_CCG_POLICY}            assign cloud config group       ${CCG_NAME1}        Delta       None       ${device.serial}
    should be equal as strings     '${ASSIGN_CCG_POLICY}'     '1'

    #EDIT CCG Group - REMOVE AP from CCG
    ${EDIT_CCG_REMOVE_DEVICE}       edit cloud config group         ${CCG_NAME1}        remove      ap_serials=${device1.serial}
    should be equal as strings     '${EDIT_CCG_REMOVE_DEVICE}'     '1'

    #ADD AP in existing CCG group from Manage devices Page
    ${ADD_CCG_FROM_MANAGE}          add cloud config group from manage     ${CCG_NAME2}        ${CCG_DESC2}        ${device1.serial}
    should be equal as strings     '${ADD_CCG_FROM_MANAGE}'     '1'

    #Add Sim AP to CCG Group 2
    ${ADD_CCG_DUP_STATUS}           add cloud config group      ${CCG_DUPLICATE}        ${CCG_DUPLICATE_DESC}        ${device.serial}
    should be equal as strings     '${ADD_CCG_DUP_STATUS}'     '1'

    # Add Classification rule
    ${CLASS_RULE_STATUS}            add classification rule with ccg        ${RULE1_NAME}       ${RULE1_DESC}        ${MATCH_FLAG}        ${CCG_NAME2}
    should be equal as strings     '${CLASS_RULE_STATUS}'     '1'

    # Assign classification rule to SSID
    ${RULE_SSID_STATUS}             add classification rule to ssid          ${NETWORK}          ${CONFIG_PUSH_SSID}        ${RULE1_NAME}
    should be equal as strings     '${RULE_SSID_STATUS}'     '1'