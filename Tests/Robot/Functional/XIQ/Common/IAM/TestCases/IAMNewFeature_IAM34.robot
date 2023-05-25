# Author        : Lacy Wu
# Date          : April 12th 2023
# Description   : test IAM
#
# Topology      :
# Host ----- Cloud
*** Variables ***

*** Settings ***
Documentation  robot -v ENV:environment.local.chrome.yaml -v TOPO:topo.test.g2.portal.yaml  IAMNewFeature_IAM34.robot

Library     common/Utils.py
Library     extauto/common/TestFlow.py
Library     iam/flows/LoginXIQ.py
Library     iam/flows/ConfigureIDP.py
Library     keywords/gui/login/KeywordsLogin.py
Library     common/Cli.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/Device360.py
Library     xiq/flows/common/Navigator.py
Library     String
Library     Collections
Resource    ../Resources/idp_releated_config.robot



Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Force Tags      testbed_none
#Suite Setup      Pre Condition
Suite Teardown   Suite Clean Up

*** Test Cases ***
TCXM-43763: Verify user should be able to Import Metadata by URL
    [Documentation]         Verify user should be able to Import Metadata by URL
    [Tags]                  tcxm_43763  development
    #Login AIO
    ${Login_XIQ}=                  Login User              ${tenant_username}      ${tenant_password}
    Should Be Equal As Integers    ${Login_XIQ}             1
    add idp               ${domain}        ${description}        ${email}        ${group}       ${meta_data_url}


TCXM-43788: Verify user's employees should be able to login XIQ by SSO successfully after logout
    [Documentation]         Verify user’s employees should be able to login XIQ by SSO successfully after logout
    [Tags]                  tcxm_43788  development
    #Login XIQ by sso process
    ${CHECK_RESULT}=        login xiq by sso        ${sso_username}       ${sso_password}       ${org_name}
    Should Be Equal As Integers    ${CHECK_RESULT}        1


*** Keywords ***
Pre Condition
    [Documentation]   Login XIQ and Create Maps and classification rules first
    [Tags]                      tcxm_26873     development    pre-condition

 #Login Portal
    ${Login_Portal}=                  Login User              ${portal_username}      ${portal_password}
    Should Be Equal As Integers    ${Login_Portal}             1

Suite Clean Up
    [Documentation]    logout and quit web browser
    [Tags]             development          tcxm_26873
    Gui Switch To Window      0
    Gui Logout User
    Quit Browser

