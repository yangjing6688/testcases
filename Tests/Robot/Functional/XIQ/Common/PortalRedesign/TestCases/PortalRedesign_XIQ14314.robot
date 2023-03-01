# Author        : Lacy Wu
# Date          : Feb 14th 2023
# Description   : test Portal account management
#
# Topology      :
# Host ----- Cloud
*** Variables ***
${MSP_USER}           msp_admin_user1
${MSP_USER_EMAIL}     msp_admin_email+2@extremenetworks.com
${MSP_USER_EMAIL_1}     msp_admin_email+3@extremenetworks.com
*** Settings ***
Documentation  robot -v ENV:environment.local.chrome.yaml -v TOPO:topo.test.g2.portal.yaml  PortalRedesign_XIQ14314.robot

Library     common/Utils.py
Library     extauto/common/TestFlow.py
Library     portal/flows/LoginPortal.py
Library     portal/flows/ManageUsers.py
Library     common/Cli.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/Device360.py
Library     xiq/flows/common/Navigator.py
Library     String
Library     Collections



Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Force Tags      testbed_none
Suite Setup      Pre Condition
Suite Teardown   Suite Clean Up

*** Test Cases ***
TCXM-31051: Verify User should be able to create a MSP-Admin account with System-Admin account
    [Documentation]         User should be able to create a MSP-Admin account with System-Admin account
    [Tags]                  tcxm_31051  development
    #create a MSP-Admin with System-Admin
    ${CHECK_RESULT}=        create MSP user        ${MSP_USER}        ${MSP_USER_EMAIL}
    Should Be Equal As Integers    ${CHECK_RESULT}        1

#     [Teardown]   Delete User    ${MSP_USER}

TCXM-31053: Verify User should be able to edit a MSP-Admin account with System-Admin account
    [Documentation]         User should be able to edit a MSP-Admin account with System-Admin account
    [Tags]                  tcxm_31053  development
    depends on             TCXM-31051
    #edit a MSP-Admin with System-Admin
    ${CHECK_RESULT}=        edit user        ${MSP_USER}          ${MSP_USER_EMAIL}        ${MSP_USER_EMAIL_1}
    Should Be Equal As Integers    ${CHECK_RESULT}        1

     [Teardown]   Delete User    ${MSP_USER}

*** Keywords ***
Pre Condition
    [Documentation]   Login XIQ and Create Maps and classification rules first
    [Tags]                      tcxm_26873     development    pre-condition

 #Login AIO
    ${Login_Portal}=                  Login User              ${portal_username}      ${portal_password}
    Should Be Equal As Integers    ${Login_Portal}             1

Suite Clean Up
    [Documentation]    logout and quit web browser
    [Tags]             development          tcxm_26873
    Logout User
    Quit Browser

