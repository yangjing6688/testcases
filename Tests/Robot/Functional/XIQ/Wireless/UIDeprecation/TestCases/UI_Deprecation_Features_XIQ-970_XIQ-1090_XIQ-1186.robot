# Author          : Mohammed Hunise Ceetherakath
# Date            : 14 Feb 2022
# Description     : Automation for XIQ UI Deprecation Features
# User Stroy      : https://jira.extremenetworks.com/browse/XIQ-970
                    https://jira.extremenetworks.com/browse/XIQ-1090
                    https://jira.extremenetworks.com/browse/XIQ-1186
#Execution Command:  robot  -v TOPO:topo.ui.deprecation.yaml -v ENV:environment.remote.win10.chrome.yaml UI_Deprecation_Features_XIQ-970_XIQ-1090_XIQ-1186.robot


*** Settings ***
Force Tags   testbed_3_node

Library      String
Library      Collections
Library      extauto/common/TestFlow.py
Library      extauto.xiq.flows.common.Navigator

Resource    ../../UIDeprecation/Resources/AllResources.robot



*** Keywords ***
Pre Condition


*** Test Cases ***
TC-15154: Verify Navigation to 'Client Monitor and Diagnosis' page
    [Documentation]         Verify that user is able to navigate to 'Client Monitor and Diagnosis' page under ML Insights

    [Tags]       xim_tc_15154         development    

    ${result}=                 Login User             ${xiq.tenant_username}  ${xiq.tenant_password}  url=${xiq.test_url}
    should be equal as strings       '${result}'        '1'

    ${client_monitor_tab}      Navigate To Client Monitor And Diagnosis Tab

    Log                        ${client_monitor_tab}

    [Teardown]
    Logout User
    Quit Browser



TC-15155: Verify Navigation to 'Client 360' page
    [Documentation]         Verify that user is able to navigate to 'Client 360' page under Manage sub-menu

    [Tags]        xim_tc_15155         development

    ${result}=                 Login User             ${xiq.tenant_username}  ${xiq.tenant_password}  url=${xiq.test_url}
    should be equal as strings       '${result}'        '1'

                               Navigate To Manage Tab

    ${client_360_tab}          Navigate To Clients Tab

    Log                        ${client_360_tab}

    [Teardown]
    Logout User
    Quit Browser



TC-15158: Verify Navigation to 'Network 360 Plan' page
    [Documentation]         Verify that user is able to navigate to 'Network 360 Plan' page under Manage sub-menu

    [Tags]       xim_tc_15158            development

    ${result}=                 Login User             ${xiq.tenant_username}  ${xiq.tenant_password}  url=${xiq.test_url}
    should be equal as strings       '${result}'        '1'

    ${network_360_plan}         Navigate To Network360plan

    Log                         ${network_360_plan}

    [Teardown]
    Logout User
    Quit Browser



TC-15188: Verify Navigation to 'Unbind MAC/PPSK binding' page
    [Documentation]         Verify that user is able to navigate to 'Unbind MAC/PPSK binding' page under Configure > Users > User management

    [Tags]        xim_tc_15188           development

    ${result}=              Login User             ${xiq.tenant_username}  ${xiq.tenant_password}  url=${xiq.test_url}
    should be equal as strings       '${result}'        '1'

    ${unbind_devices_tab}      Navigate To Unbind Device Tab

    Log                     ${unbind_devices_tab}

    [Teardown]
    Logout User
    Quit Browser



TC-15146: Verify Navigation to Configure > Users > User management > 'Locked Users' page
    [Documentation]         Verify that user is able to navigate to 'Locked Users' page under Configure > Users > User management

    [Tags]        xim_tc_15146           development

    ${result}=              Login User             ${xiq.tenant_username}  ${xiq.tenant_password}  url=${xiq.test_url}
    should be equal as strings       '${result}'        '1'

    ${locked_user_tab}      Navigate To Locked Users Tab

    Log                     ${locked_user_tab}

    [Teardown]
    Logout User
    Quit Browser