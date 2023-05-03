# Author          : Mohammed Hunise Ceetherakath
# Date            : 29 June 2022
# Description     : Automation for XIQ UI Deprecation Features
# User Stroy      : https://jira.extremenetworks.com/browse/XIQ-7646

#Execution Command: robot -v TOPO:topo.uideprecate.yaml -v ENV:environment.remote.win10.chrome.yaml -v TESTBED:BANGALORE/Dev/testbed-hunise-all.yaml UI_Deprecation_Features_XIQ-7646.robot

*** Settings ***
Library      String
Library      Collections
Library      extauto/common/TestFlow.py
Library      extauto/xiq/flows/common/Login.py
Library      extauto/xiq/flows/common/Navigator.py

Variables   Environments/Config/waits.yaml
Variables   Environments/${TOPO}
Variables   Environments/${ENV}

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

TCXM-21457 : Verify that VPN Management is restored under Manage Page

	[Documentation]         Verify that user is able to navigate to 'VPN Management' page under Manage

    [Tags]       tcxm_21457         development

    ${vpn_management_tab}        Navigate To VPN Management Tab

    should be equal as strings       '${vpn_management_tab}'          '1'

    Log                               ${vpn_management_tab}

TCXM-21555 : Verify that VPN Services is restored under Common Objects > Network Page

	[Documentation]         Verify that user is able to navigate to 'VPN Services' page under Common Object > Network Page

    [Tags]       tcxm_21555         development

    Navigate Configure Common Objects

    ${common_nw_tab}            Navigate To Common Object Network Tab
    should be equal as strings       '${common_nw_tab}'          '1'

    ${vpn_services}        Navigate To VPN Services Tab
    should be equal as strings       '${vpn_services}'          '1'

    Log                               ${vpn_services}