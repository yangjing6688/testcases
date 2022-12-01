# Author          : Mohammed Hunise Ceetherakath
# Date            : 30 Mar 2022
# Description     : Automation for XIQ UI Deprecation Features
# User Stroy      : https://jira.extremenetworks.com/browse/XIQ-1523
                    https://jira.extremenetworks.com/browse/XIQ-4143
#Execution Command:  robot -v TOPO:topo.ui.deprecation.yaml -v ENV:environment.remote.win10.chrome.yaml UI_Deprecation_Features_XIQ-1523_XIQ-4143.robot

*** Variables ***
${APPLICATION_NAME}            test-app
${APPLICATION_NAME_MODIFIED}   test-app-modified
${WAIT}                        5


*** Settings ***
Force Tags   testbed_1_node
Suite Setup  Test Suite Setup

Library      String
Library      Collections
Library      extauto/common/Utils.py
Library      extauto/common/TestFlow.py
Library      extauto/xiq/flows/common/Login.py
Library      extauto/xiq/flows/common/Navigator.py
Library      extauto/xiq/flows/manage/Applications.py

Resource    ../../UIDeprecation/Resources/AllResources.robot



*** Keywords ***
Test Suite Setup
# Create a random string for application group name
    ${random_string}=         Get Random String
    ${GROUP_NAME}=            Catenate    GROUP_NAME_${random_string}

    Set Global Variable       ${GROUP_NAME}


*** Test Cases ***

TCXM-18052 : Verify Navigation to 'Client Monitor and Diagnosis' page

	[Documentation]         Verify that user is able to navigate to 'Client Monitor and Diagnosis' page under Manage

    [Tags]       tcxm_18052         development

    ${result}=                 Login User             ${tenant_username}    ${tenant_password}
    should be equal as strings       '${result}'                    '1'

    ${client_monitor_tab}      Navigate To Client Monitor And Diagnosis Tab

    should be equal as strings       '${client_monitor_tab}'        '1'

    Log                               ${client_monitor_tab}

    [Teardown]
    Logout User
    Quit Browser



TCXM-17452 : Verify Navigation to 'Applications' page

	[Documentation]         Verify that user is able to navigate to 'Applications' page under Manage

    [Tags]       tcxm_17452         development

    ${result}=                 Login User             ${tenant_username}  ${tenant_password}

    should be equal as strings       '${result}'                   '1'

    ${applications_tab}        Navigate To Applications Tab

    should be equal as strings       '${applications_tab}'         '1'

    Log                               ${applications_tab}

    [Teardown]
    Logout User
    Quit Browser



TCXM-17491 : Create Custom Application

	[Documentation]         Verify that user is able to create custom applications

    [Tags]       tcxm_17491         development

    ${result}=                Login User             ${tenant_username}    ${tenant_password}

    should be equal as strings       '${result}'                   '1'

    ${app_tab}=               Navigate To Applications Tab

    should be equal as strings       '${app_tab}'                  '1'

    sleep                             ${WAIT}

    ${add_custom}             Add Custom Applications     ${APPLICATION_NAME}     ${GROUP_NAME}

    should be equal as strings       '${add_custom}'                '1'

    Log                               ${add_custom}

    [Teardown]
    Logout User
    Quit Browser



TCXM-17493 : Edit Custom Application

   [Documentation]         Verify that user is able to edit custom applications

    [Tags]       tcxm_17493         development

    ${result}=                 Login User             ${tenant_username}     ${tenant_password}

    should be equal as strings       '${result}'                   '1'

    ${app_tab}=                Navigate To Applications Tab

    should be equal as strings       '${app_tab}'                  '1'

    sleep                             ${WAIT}

    ${edit_custom}             Edit Custom Applications     ${APPLICATION_NAME}     ${APPLICATION_NAME_MODIFIED}

    should be equal as strings       '${edit_custom}'                '1'

    Log                               ${edit_custom}

    [Teardown]
    Logout User
    Quit Browser



TCXM-17494 : Delete Custom Application

    [Documentation]         Verify that user is able to delete custom applications

    [Tags]       tcxm_17493         development

    ${result}=                 Login User             ${tenant_username}    ${tenant_password}

    should be equal as strings       '${result}'                   '1'

    ${app_tab}=               Navigate To Applications Tab

    should be equal as strings       '${app_tab}'                  '1'

    sleep                             ${WAIT}

    ${delete_custom}             Delete Custom Applications     ${APPLICATION_NAME_MODIFIED}

    should be equal as strings       '${delete_custom}'                '1'


    Log                               ${delete_custom}

    [Teardown]
    Logout User
    Quit Browser
