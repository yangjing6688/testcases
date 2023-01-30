# Author          : Mohammed Hunise Ceetherakath
# Date            : 09 August 2022
# Description     : Automation for XIQ UI Deprecation Features
# User Stroy      : https://jira.extremenetworks.com/browse/XIQ-7647
#Execution Command:  robot  -v TOPO:topo.ui.deprecation.yaml -v ENV:environment.remote.win10.chrome.yaml UI_Deprecation_Features_XIQ-7647.robot

*** Variables ***
${AP_MODEL}                     AP460C
${COUNTRY_CODE}                 France (250)
${COUNTRY_NAME}                 France_(250)


*** Settings ***
Force Tags   testbed_1_node

Library      String
Library      Collections
Library      extauto/common/Utils.py
Library      extauto/common/Cli.py
Library      extauto/common/TestFlow.py
Library      extauto/xiq/flows/common/Login.py
Library      extauto/xiq/flows/common/Navigator.py
Library      extauto/xiq/flows/configure/DeviceTemplate.py
Library      extauto/xiq/flows/configure/NetworkPolicy.py
Library      extauto/xiq/flows/configure/CommonObjects.py
Library      extauto/xiq/flows/manage/Tools.py
Library      extauto/xiq/flows/manage/Devices.py
Library      ExtremeAutomation/Imports/CommonObjectUtils.py

Resource    ../../UIDeprecation/Resources/AllResources.robot

Suite Setup       Pre Condition
Suite Teardown    Test suite Cleanup


*** Keywords ***

Pre Condition
    [Documentation]   Create a Network Policy, AP Template and set Country Code in AP Template

    # Create a random string for the variables
    ${random_string}=         Get Random String

    ${AP_TEMPLATE_NAME}=          Catenate    AP_TEMPLATE_${random_string}
    ${NW_POLICY_NAME}=            Catenate    CC_NP_${random_string}

    Set Global Variable         ${NW_POLICY_NAME}
    Set Global Variable         ${AP_TEMPLATE_NAME}

    # Use this method to convert the ap, wing, netelem to a generic device object
    # ap1       => device1
    # wing1     => device1
    # netelem1  => device1 (EXOS / VOSS)

    convert to generic device object   device  index=1

    ${login_status}=                  Login User                              ${tenant_username}          ${tenant_password}
    should be equal as integers       ${login_status}                1

    ${AP_SPAWN}=                      Open Spawn                               ${device1.ip}          ${device1.port}           ${device1.username}        ${device1.password}     ${device1.cli_type}
    Should not be equal as Strings    '${AP_SPAWN}'                 '-1'
    
    Set Global Variable               ${AP_SPAWN}
    
    ${disconnect_ap}=                 Disconnect Device From Cloud      ${device1.cli_type}      ${AP_SPAWN}
    should be equal as integers       ${disconnect_ap}             1
    
    ${delete_ap}=                     Delete Device                           device_serial=${device1.serial}
    should be equal as integers       ${delete_ap}                   1

    ${np_list_view}=                  Navigate To Network Policies List View Page
    should be equal as integers       ${np_list_view}                1

    ${country_code}=                  Add AP Template With Country Code       ${NW_POLICY_NAME}       ${AP_MODEL}        ${AP_TEMPLATE_NAME}     ${COUNTRY_CODE}
    should be equal as integers       ${country_code}                1


Test suite Cleanup

    [Documentation]    delete device, AP Template, and Network Policy

    ${delete_ap1}=                    Delete Device                           device_serial=${device1.serial}
    should be equal as integers       ${delete_ap1}                   1
    
    ${disconnect_device}=             Disconnect Device From Cloud      ${device1.cli_type}      ${AP_SPAWN}
    should be equal as integers       ${disconnect_device}             1

    ${delete_np}=                     Delete Network Policy                     ${NW_POLICY_NAME}
    should be equal as integers       ${delete_np}                   1

    ${delete_template}=               Delete AP Templates          ${AP_TEMPLATE_NAME}
    Log                               ${delete_template}

    [Teardown]
    Logout User
    Quit Browser


*** Test Cases ***

TCXM-21577: Unhide Country Code - AP templates
    [Documentation]         Verify that user will be able to set Country Code in AP Templates

    [Tags]       tcxm_21577         development

    # Country Code variables in line No.41 and 95 are different because retrived output and assigned output format are different for Country Code value.
    # This test case will work only on the device which has the region World or EU

    ${onboard_status}=                onboard device quick                         ${device1}
    should be equal as integers       ${onboard_status}              1

    ${assign_np}=                     Assign Network Policy To A Device        ${device1.serial}      ${NW_POLICY_NAME}
    should be equal as integers       ${assign_np}                   1

    ${connect_cloud}=                 Configure Device To Connect To Cloud     ${device1.cli_type}        ${capwap_url}     ${AP_SPAWN}
    should be equal as integers       ${connect_cloud}                1

    ${wait_till_online}=              Wait Until Device Online                 ${device1.serial}
    should be equal as integers       ${wait_till_online}             1

    ${wait_till_reboots}=             Wait Until Device Reboots                ${device1.serial}
    should be equal as integers       ${wait_till_reboots}            1

    ${device_status}=                 Get Device Status                       device_mac=${device1.mac}
    Should Be Equal As Strings        '${device_status}'             'green'

    ${refresh}=                       Refresh Devices Page
    should be equal as integers       ${refresh}                     1

    ${country_code_status}=           Get Ap Country                          ${device1.serial}
    should be equal as strings        '${country_code_status}'                '${COUNTRY_NAME}'



