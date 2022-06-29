# Author          : Mohammed Hunise Ceetherakath
# Date            : 09 Apr 2022
# Description     : Automation for XIQ UI Deprecation Features
# User Stroy      : https://jira.extremenetworks.com/browse/XIQ-4520
                    https://jira.extremenetworks.com/browse/XIQ-3825
                    https://jira.extremenetworks.com/browse/XIQ-3564
                    https://jira.extremenetworks.com/browse/XIQ-5862
#Execution Command:  robot -v TOPO:topo.uideprecate.yaml -v ENV:environment.remote.win10.chrome.yaml -v TESTBED:BANGALORE/Dev/testbed-hunise-all.yaml UI_Deprecation_Features_XIQ-4520_XIQ-3825_XIQ-3564_XIQ-5862.robot

*** Settings ***
Force Tags   testbed_3_node

Library      String
Library      Collections
Library      extauto/common/TestFlow.py
Library      extauto/xiq/flows/common/Login.py
Library      extauto/xiq/flows/common/Navigator.py
Library      extauto/xiq/flows/configure/DeviceTemplate.py
Library      extauto/xiq/flows/configure/NetworkPolicy.py
Library      extauto/xiq/flows/manage/Tools.py
Library      extauto/xiq/flows/manage/Devices.py

Resource    ../../UIDeprecation/Resources/AllResources.robot


*** Keywords ***
Pre Condition

*** Test Cases ***

TCXM-17532 : Relocate Supplemental CLI under Switch Template

    [Documentation]         Verify that Supplemental CLI is relocated to Switch Template under advanced settings

    [Tags]       tcxm_17532         development

    ${result}=                 Login User             ${xiq.tenant_username}  ${xiq.tenant_password}  url=${xiq.test_url}
    should be equal as strings       '${result}'                   '1'

    Delete Network Policy             ${var.switch_policy_name}

    ${switch_scli}              Enable Supplemental CLI In Switch Template    ${var.switch_policy_name}    ${var.switch_model}    ${var.switch_template_name}    ${var.switch_suppl_cli_name}   ${var.switch_suppl_cli_cmds}

    should be equal as strings       '${switch_scli}'                   '1'

    Log                               ${switch_scli}

    [Teardown]
    Logout User
    Quit Browser



TCXM-17534 : Relocate Supplemental CLI under AP Template

    [Documentation]         Verify that Supplemental CLI is relocated to AP Template under advanced settings

    [Tags]       tcxm_17534         development

    ${result}=                 Login User             ${xiq.tenant_username}  ${xiq.tenant_password}  url=${xiq.test_url}
    should be equal as strings       '${result}'                   '1'

    Delete Network Policy             ${var.ap_policy_name}

    ${ap_scli}                 Enable Supplemental CLI In AP Template    ${var.ap_policy_name}    ${var.ap_model}    ${var.ap_template_name}    ${var.ap_suppl_cli_name}   ${var.ap_suppl_cli_cmds}

    should be equal as strings       '${ap_scli}'                   '1'

    Log                               ${ap_scli}

    [Teardown]
    Logout User
    Quit Browser



TCXM-17544 : Point client hyperlink to Client 360 page

    [Documentation]         Verify that clicking on clients hyperlink points to ML Insights Client 360 page

    [Tags]       tcxm_17544         development

    ${result}=                 Login User             ${xiq.tenant_username}  ${xiq.tenant_password}  url=${xiq.test_url}
    should be equal as strings       '${result}'                   '1'

    ${client_hyperlink}        Point Client Hyperlink To Client360

    should be equal as strings       '${client_hyperlink}'          '1'

    Log                               ${client_hyperlink}

    [Teardown]
    Logout User
    Quit Browser



TCXM-20275 : Enable PING for Installer user for Aerohive AP

    [Documentation]         Verify that PING is enabled for Installer role for Aerohive AP

    [Tags]       tcxm_20275         development

    ${result}=                 Login User             ${xiq.tenant_username_installer}  ${xiq.tenant_password}  url=${xiq.test_url}
    should be equal as strings       '${result}'                   '1'

    ${select_ap}               Select AP                         ${ap9.serial}
    should be equal as strings       '${select_ap}'                 '1'

    ${ping}                    Installer Role Diagnostics Ping

    should be equal as strings       '${ping}'                      '1'

    Log                               ${ping}

    [Teardown]
    Logout User
    Quit Browser
