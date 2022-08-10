# Author          : Mohammed Hunise Ceetherakath
# Date            : 09 August 2022
# Description     : Automation for XIQ UI Deprecation Features
# User Stroy      : https://jira.extremenetworks.com/browse/XIQ-7647
#Execution Command:  robot  -v TOPO:topo.ui.deprecation.yaml -v ENV:environment.remote.win10.chrome.yaml UI_Deprecation_Features_XIQ-7647.robot


*** Settings ***
Force Tags   testbed_3_node

Library      String
Library      Collections
Library      extauto/common/Cli.py
Library      extauto/common/TestFlow.py
Library      extauto/xiq/flows/common/Login.py
Library      extauto/xiq/flows/common/Navigator.py
Library      extauto/xiq/flows/configure/DeviceTemplate.py
Library      extauto/xiq/flows/configure/NetworkPolicy.py
Library      extauto/xiq/flows/configure/CommonObjects.py
Library      extauto/xiq/flows/manage/Tools.py
Library      extauto/xiq/flows/manage/Devices.py

Resource    ../../UIDeprecation/Resources/AllResources.robot

Suite Setup       Pre Condition
Suite Teardown    Test suite Cleanup


*** Keywords ***

Pre Condition

    [Documentation]   Create a Network Policy, AP Template and set Country Code in AP Template

    ${login_status}=                  Login User                              ${xiq.tenant_username}          ${xiq.tenant_password}     url=${xiq.test_url}
    should be equal as integers       ${login_status}                1

    ${np_list_view}=                  Navigate To Network Policies List View Page
    should be equal as integers       ${np_list_view}                1

    ${country_code}=                  Add AP Template With Country Code       ${xiq.nw_policy_name}            ${xiq.ap_model}             ${xiq.ap_template_name}         ${xiq.country_code}
    should be equal as integers       ${country_code}                1


Test suite Cleanup

    [Documentation]    delete device, AP Template, and Network Policy

    ${delete_ap}=                     Delete Device                           device_serial=${ap1.serial}
    should be equal as integers       ${delete_ap}                   1

    ${remove_ap_template}=            Remove AP Template From Network Policy    ${xiq.ap_template_name}   ${xiq.nw_policy_name}
    ${delete_np}=                     Delete Network Policy                   ${xiq.nw_policy_name}
    should be equal as integers       ${delete_np}                   1

    ${delete_template}                Delete AP Templates                     ${xiq.ap_template_name}
    Log       ${delete_template}


    [Teardown]
    Logout User
    Quit Browser


*** Test Cases ***

TCXM-21577: Unhide Country Code - AP templates
    [Documentation]         Verify that user will be able to set Country Code in AP Templates

    [Tags]       tcxm_21577         development

    # Country Code variables in line No.41 and 95 are different because retrived output and assigned output format are different for Country Code value.

    ${onboard_status}=                Onboard Device                          ${ap1.serial}                    ${ap1.make}                 location=${xiq.location}
    should be equal as integers       ${onboard_status}              1

    ${assign_np}=                     Assign Network Policy To All Devices    ${xiq.nw_policy_name}
    should be equal as integers       ${assign_np}                   1

    ${connect_cloud}=                 Configure Device To Connect To Cloud     ${ap1.cli_type}   ${ap1.ip}       ${ap1.port}     ${ap1.username}      ${ap1.password}       ${xiq.capwap_url}
    should be equal as integers       ${connect_cloud}                1

    ${wait_till_online}=              Wait Until Device Online                 ${ap1.serial}
    should be equal as integers       ${wait_till_online}             1

    ${wait_till_reboots}=             Wait Until Device Reboots                ${ap1.serial}
    should be equal as integers       ${wait_till_reboots}            1

    ${device_status}=                 Get Device Status                       device_mac=${ap1.mac}
    Should Be Equal As Strings        '${device_status}'             'green'

    ${refresh}=                       Refresh Devices Page
    should be equal as integers       ${refresh}                     1

    ${country_code_status}=           Get Ap Country                          ${ap1.serial}
    should be equal as strings        '${country_code_status}'                '${xiq.country_name}'



