# Author          : Mohammed Hunise Ceetherakath
# Date            : 14 Feb 2022
# Description     : Automation for XIQ UI Deprecation Features
# User Stroy      : https://jira.extremenetworks.com/browse/XIQ-970
#                    https://jira.extremenetworks.com/browse/XIQ-1090
#                    https://jira.extremenetworks.com/browse/XIQ-1186
#Execution Command:  robot  -v TOPO:topo.ui.deprecation.yaml -v ENV:environment.remote.win10.chrome.yaml UI_Deprecation_Features_XIQ-970_XIQ-1090_XIQ-1186.robot


*** Settings ***
Force Tags   testbed_1_node

Library      String
Library      Collections
Library      extauto/common/TestFlow.py
Library      extauto.xiq.flows.common.Navigator
Library      extauto/xiq/flows/common/Login.py

Resource    ../../UIDeprecation/Resources/AllResources.robot

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}



*** Keywords ***
Pre Condition


*** Test Cases ***
TC-15158: Verify Navigation to 'Network 360 Plan' page
    [Documentation]         Verify that user is able to navigate to 'Network 360 Plan' page under Manage sub-menu

    [Tags]       tcxm_15158            development

    ${result}=                 Login User             ${tenant_username}     ${tenant_password}
    should be equal as strings       '${result}'        '1'

    ${network_360_plan}         Navigate To Network360plan

    Log                         ${network_360_plan}

    [Teardown]
    Logout User
    Quit Browser



TC-15188: Verify Navigation to 'Unbind MAC/PPSK binding' page
    [Documentation]         Verify that user is able to navigate to 'Unbind MAC/PPSK binding' page under Configure > Users > User management

    [Tags]        tcxm_15188           development

    ${result}=              Login User             ${tenant_username}      ${tenant_password}
    should be equal as strings       '${result}'        '1'

    ${unbind_devices_tab}      Navigate To Unbind Device Tab

    Log                     ${unbind_devices_tab}

    [Teardown]
    Logout User
    Quit Browser



TC-15146: Verify Navigation to Configure > Users > User management > 'Locked Users' page
    [Documentation]         Verify that user is able to navigate to 'Locked Users' page under Configure > Users > User management

    [Tags]        tcxm_15146           development

    ${result}=              Login User             ${tenant_username}      ${tenant_password}
    should be equal as strings       '${result}'        '1'

    ${locked_user_tab}      Navigate To Locked Users Tab

    Log                     ${locked_user_tab}

    [Teardown]
    Logout User
    Quit Browser
