# Author          : Mohammed Hunise Ceetherakath
# Date            : 14 Feb 2022
# Description     : Automation for XIQ UI Deprecation Features
# User Story      : https://jira.extremenetworks.com/browse/XIQ-970
#                    https://jira.extremenetworks.com/browse/XIQ-1090
#                    https://jira.extremenetworks.com/browse/XIQ-1186
#Execution Command:  robot  -v TOPO:topo.ui.deprecation.yaml -v ENV:environment.remote.win10.chrome.yaml UI_Deprecation_Features_XIQ-970_XIQ-1090_XIQ-1186.robot


*** Settings ***
Library      extauto/xiq/flows/common/Navigator.py
Library      extauto/xiq/flows/common/Login.py

Variables   Environments/${TOPO}
Variables    Environments/${ENV}

Force Tags   testbed_none
Suite Setup  Test Suite Setup
Suite Teardown    Run Keyword And Warn On Failure  Test suite Cleanup

*** Keywords ***
Test Suite Setup
    ${result}=                 Login User             ${tenant_username}    ${tenant_password}
    should be equal as strings       '${result}'                    '1'

Test suite Cleanup
    Logout User
    Quit Browser


*** Test Cases ***
TC-15158: Verify Navigation to 'Network 360 Plan' page
    [Documentation]         Verify that user is able to navigate to 'Network 360 Plan' page under Manage sub-menu

    [Tags]       tcxm-15158            development

    ${network_360_plan}=         Navigate To Network360plan
    should be equal as strings       '${network_360_plan}'        '1'

    Log                         ${network_360_plan}

TC-15188: Verify Navigation to 'Unbind MAC/PPSK binding' page
    [Documentation]         Verify that user is able to navigate to 'Unbind MAC/PPSK binding' page under Configure > Users > User management
    [Tags]        tcxm-15188           development

    ${unbind_devices_tab}      Navigate To Unbind Device Tab
    should be equal as strings       '${unbind_devices_tab}'        '1'
    Log                     ${unbind_devices_tab}

TC-15146: Verify Navigation to Configure > Users > User management > 'Locked Users' page
    [Documentation]         Verify that user is able to navigate to 'Locked Users' page under Configure > Users > User management
    [Tags]        tcxm-15146           development

    ${locked_user_tab}      Navigate To Locked Users Tab
    should be equal as strings       '${locked_user_tab}'        '1'

    Log                     ${locked_user_tab}