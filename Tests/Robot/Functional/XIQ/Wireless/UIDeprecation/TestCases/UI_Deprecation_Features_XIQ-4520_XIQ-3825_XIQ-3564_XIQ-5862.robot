# Author          : Mohammed Hunise Ceetherakath
# Date            : 09 Apr 2022
# Description     : Automation for XIQ UI Deprecation Features
# User Stroy      : https://jira.extremenetworks.com/browse/XIQ-4520
#                   https://jira.extremenetworks.com/browse/XIQ-3825
#                   https://jira.extremenetworks.com/browse/XIQ-3564
#                   https://jira.extremenetworks.com/browse/XIQ-5862
#Execution Command:  robot -v TOPO:topo.uideprecate.yaml -v ENV:environment.remote.win10.chrome.yaml -v TESTBED:BANGALORE/Dev/testbed-hunise-all.yaml UI_Deprecation_Features_XIQ-4520_XIQ-3825_XIQ-3564_XIQ-5862.robot

*** Variables ***
${AP_SUPPL_CLI_CMDS}                 show capwap client
${SWITCH_MODEL}                      SR2024P
${SWITCH_SUPPL_CLI_CMDS}             show version

*** Settings ***
Force Tags   testbed_1_node

Library      String
Library      Collections
Library      extauto/common/Utils.py
Library      extauto/common/Cli.py
Library      extauto/common/TestFlow.py
Library      extauto/common/tools/remote/WinMuConnect.py
# The keywords in Login.py have been moved to the keywords directory.
# If the moved keyword is not working correctly import the original library and remove the keywords/gui/login/KeywordsLogin.py version.
#Library      extauto/xiq/flows/common/Login.py
Library      keywords/gui/login/KeywordsLogin.py
Library      extauto/xiq/flows/common/Navigator.py
Library      extauto/xiq/flows/configure/DeviceTemplate.py
Library      extauto/xiq/flows/configure/CommonObjects.py
Library      extauto/xiq/flows/configure/NetworkPolicy.py
Library      extauto/xiq/flows/manage/Tools.py
Library      extauto/xiq/flows/manage/Devices.py
Library      ExtremeAutomation/Imports/CommonObjectUtils.py
Library      extauto/xiq/flows/configure/ExpressNetworkPolicies.py

Resource     ../../UIDeprecation/Resources/AllResources.robot

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}

Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml
Variables    Tests/Robot/Functional/XIQ/Wireless/Sanity/Resources/location_sanity_config.py

Library	     Remote 	http://${mu1.ip}:${mu1.port}   WITH NAME   MU1

Suite Setup       Test Suite Setup
Suite Teardown    Run Keyword And Warn On Failure   Test suite Cleanup

*** Keywords ***
Test Suite Setup
    # Create a random string for the variables
    ${random_string}=         Get Random String

    ${AP_POLICY_NAME}=          Catenate    AP_NP_NAME_${random_string}
    ${SWITCH_POLICY_NAME}=      Catenate    SWITCH_NP_NAME_${random_string}
    ${AP_TMPL_NAME}=            Catenate    AP_TMPL_NAME_${random_string}
    ${SW_TMPL_NAME}=            Catenate    SW_TMPL_NAME_${random_string}
    ${AP_SCLI_NAME}=            Catenate    AP_SCLI_NAME_${random_string}
    ${SW_SCLI_NAME}=            Catenate    SW_SCLI_NAME_${random_string}

    Set Global Variable         ${AP_TMPL_NAME}
    Set Global Variable         ${SW_TMPL_NAME}
    Set Global Variable         ${AP_SCLI_NAME}
    Set Global Variable         ${SW_SCLI_NAME}


    Set Global Variable         ${AP_POLICY_NAME}
    Set Global Variable         ${SWITCH_POLICY_NAME}

    # Use this method to convert the ap, wing, netelem to a generic device object
    # ap1       => device1
    # wing1     => device1
    # netelem1  => device1 (EXOS / VOSS)
    convert to generic device object   device  index=1

    ${login_status}=                  Login User               ${tenant_username}     ${tenant_password}
    should be equal as integers       ${login_status}          1

    ${AP_SPAWN}=                      Open Spawn         ${device1.ip}    ${device1.port}    ${device1.username}    ${device1.password}     ${device1.cli_type}
    Should not be equal as Strings    '${AP_SPAWN}'      '-1'

    Set Global Variable               ${AP_SPAWN}

    ${SEARCH_RESULT}=           Search Device               device_serial=${device1.serial}     ignore_failure=True
    IF  ${SEARCH_RESULT} == 1
        ${DISCONNECT_DEVICE_RESULT}=    Disconnect Device From Cloud        ${device1.cli_type}      ${AP_SPAWN}
        Should Be Equal As Integers     ${DISCONNECT_DEVICE_RESULT}         1

        ${DELETE_DEVICE_RESULT}=        Delete Device                       device_serial=${device1.serial}
        Should Be Equal As Integers     ${DELETE_DEVICE_RESULT}             1
    END

    ${delete_ap_nw_policies}=         Delete Network Polices    ${AP_POLICY_NAME}    ${SWITCH_POLICY_NAME}
    should be equal as integers       ${delete_ap_nw_policies}   1

    ${POLICY_RESULT}                  Create Open Auth Express Network Policy     ${POLICY_NAME}      ${SSID_NAME}
    Should Be Equal As Integers       ${POLICY_RESULT}        1

    ${onboard_status}=                Onboard Device Quick     ${device1}
    should be equal as integers       ${onboard_status}        1

    ${connect_cloud}=                 Configure Device To Connect To Cloud   ${device1.cli_type}    ${capwap_url}     ${AP_SPAWN}
    should be equal as integers       ${connect_cloud}                       1

    ${wait_till_online}=              Wait Until Device Online     ${device1.serial}
    should be equal as integers       ${wait_till_online}          1

    ${device_stats}=                  Get Device Status            device_mac=${device1.mac}
    Should Be Equal As Strings        '${device_stats}'           'green'

    ${deploy_status}=                 Deploy Network Policy with Complete Update      ${POLICY_NAME}       ${device1.serial}
    should be equal as integers       ${deploy_status}              1

    ${wait_till_reboots}=             Wait Until Device Reboots    ${device1.serial}
    should be equal as integers       ${wait_till_reboots}         1

    ${device_status}=                 Get Device Status            device_mac=${device1.mac}
    Should Be Equal As Strings        '${device_status}'           'green'

Test suite Cleanup

    ${delete_device}=                 Delete Device            device_serial=${device1.serial}
    should be equal as integers       ${delete_device}         1
    
    ${disconnect_device}=             Disconnect Device From Cloud      ${device1.cli_type}      ${AP_SPAWN}
    should be equal as integers       ${disconnect_device}              1

    ${delete_sw_np}=                  Delete Network Polices         ${SWITCH_POLICY_NAME}    ${AP_POLICY_NAME}    ${POLICY_NAME}
    should be equal as integers       ${delete_sw_np}          1

    ${delete_ap_templ}=               Delete AP Template Profile     ${AP_TMPL_NAME}
    Log                               ${delete_ap_templ}

    ${delete_sw_templ}=               Delete Switch Template          ${SW_TMPL_NAME}
    Log                               ${delete_sw_templ}

    ${delete_ssids}=                  Delete ssids                    ${SSID_NAME}
    should be equal as integers       ${delete_ssids}          1

    [Teardown]  run keywords       logout user
    ...                            Quit Browser

*** Test Cases ***

TCXM-17532 : Relocate Supplemental CLI under Switch Template

	[Documentation]         Verify that Supplemental CLI is relocated to Switch Template under advanced settings

    [Tags]       tcxm_17532         development

    ${delete_np}=                 Delete Network Policy             ${SWITCH_POLICY_NAME}
    should be equal as strings       '${delete_np}'                   '1'

    ${switch_scli}              Enable Supplemental CLI In Switch Template    ${SWITCH_POLICY_NAME}    ${SWITCH_MODEL}     ${SW_TMPL_NAME}    ${SW_SCLI_NAME}    ${SWITCH_SUPPL_CLI_CMDS}
    should be equal as strings       '${switch_scli}'                   '1'

    Log                               ${switch_scli}

TCXM-17534 : Relocate Supplemental CLI under AP Template

	[Documentation]         Verify that Supplemental CLI is relocated to AP Template under advanced settings
    [Tags]       tcxm_17534         development

    ${delete_np}=                 Delete Network Policy             ${AP_POLICY_NAME}
    should be equal as strings       '${delete_np}'                   '1'

    ${ap_scli}                 Enable Supplemental CLI In AP Template    ${AP_POLICY_NAME}    ${device1.model}     ${AP_TMPL_NAME}    ${AP_SCLI_NAME}   ${AP_SUPPL_CLI_CMDS}
    should be equal as strings       '${ap_scli}'                   '1'

    Log                               ${ap_scli}

TCXM-20275 : Enable PING for Installer user for Aerohive AP

	[Documentation]         Verify that PING is enabled for Installer role for Aerohive AP

    [Tags]       tcxm_20275         development

    ${select_ap}               select device                         device_serial=${device1.serial}
    should be equal as strings       '${select_ap}'                 '1'

    ${ping}                    Installer Role Diagnostics Ping
    should be equal as strings       '${ping}'                      '1'

    Log                               ${ping}

TCXM-17544 : Point client hyperlink to Client 360 page
	[Documentation]         Verify that clicking on clients hyperlink points to ML Insights Client 360 page
    [Tags]       tcxm_17544         development

    ${CONNECT_STATUS}=              MU1.Connect Open Network        ${SSID_NAME}
    should be equal as strings      '${CONNECT_STATUS}'    '1'
    sleep   ${client_connect_wait}

    Refresh Devices Page

    ${client_hyperlink}              Point Client Hyperlink To Client360
    should be equal as strings       '${client_hyperlink}'          '1'
    Log                               ${client_hyperlink}

    MU1.Disconnect WiFi
    sleep  ${client_disconnect_wait}





