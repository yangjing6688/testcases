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
${VIQ_USER}           viq_admin_user1
${VIQ_USER_EMAIL}     viq_admin_email+1@extremenetworks.com
${VIQ_USER_EMAIl_1}   viq_admin_email+2@extremenetworks.com
${CUSTOMER_NAME_1}    customer_1
${CUSTOMER_First_NAME_1}     Customer_1
${CUSTOMER_Last_NAME_1}      Qa
${CUSTOMER_EMAIL_1}          customer_1@extremenetworks.com
${CUSTOMER_PASSWORD_1}       Aerohive123

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
    ${CHECK_RESULT}=        create user        MSP        ${MSP_USER}        ${MSP_USER_EMAIL}
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

TCXM-31052: Verify User should be able to add a VIQ-Admin account with MSP-Admin account
    [Documentation]         User should be able to add a VIQ-Admin account with MSP-Admin account
    [Tags]                  tcxm_31052  development
    depends on             TCXM-31051
    #logout and login with MSP account
    Logout User
    ${Login_Portal}=                  Login User              ${msp_username}      ${msp_password}
    Should Be Equal As Integers    ${Login_Portal}             1
    #create a VIQ-Admin with MSP-Admin
    ${CHECK_RESULT}=        create user        VIQ          ${VIQ_USER}        ${VIQ_USER_EMAIL}
    Should Be Equal As Integers    ${CHECK_RESULT}        1
 #    [Teardown]   Delete User    ${VIQ_USER}

 TCXM-31054: Verify User should be able to edit a VIQ-Admin account with MSP-Admin account
    [Documentation]         User should be able to add a VIQ-Admin account with MSP-Admin account
    [Tags]                  tcxm_31054  development
    depends on             TCXM-31052
    #edit a VIQ-Admin with MSP-Admin
    ${CHECK_RESULT}=        edit user        ${VIQ_USER}        ${VIQ_USER_EMAIL}        ${VIQ_USER_EMAIL_1}
    Should Be Equal As Integers    ${CHECK_RESULT}        1

    [Teardown]   Delete User    ${VIQ_USER}

 TCXM-31055: Verify User should be able to Create account(customer) with VIQ-Admin account
    [Documentation]         User should be able to add an account(customer) with VIQ-Admin account
    [Tags]                  tcxm_31055  development
    #edit a VIQ-Admin with MSP-Admin
    depends on          TCXM-31054
    Logout User
    Quit Browser
    ${Login_Portal}=                  Login User              ${viq_username}      ${viq_password}
    Should Be Equal As Integers    ${Login_Portal}          1
    ${Check_Result}=            Create Xiq Account         ${CUSTOMER_NAME_1}        ${CUSTOMER_First_NAME_1}      ${CUSTOMER_Last_NAME_1}      ${CUSTOMER_EMAIL_1}     ${CUSTOMER_PASSWORD_1}


    [Teardown]   Delete Customer     ${CUSTOMER_NAME_1}

 TCXM-31056: Verify User should be able to Create account(customer) with MSP-Admin account
    [Documentation]         User should be able to add a VIQ-Admin account with MSP-Admin account
    [Tags]                  tcxm_31056  development
    #edit a VIQ-Admin with MSP-Admin
    depends on          TCXM-31056
    Logout User
    Quit Browser
    ${Login_Portal}=                  Login User              ${msp_username}      ${msp_password}
    Should Be Equal As Integers    ${Login_Portal}          1
    ${Check_Result}=            Create Xiq Account         ${CUSTOMER_NAME_1}        ${CUSTOMER_First_NAME_1}      ${CUSTOMER_Last_NAME_1}      ${CUSTOMER_EMAIL_1}     ${CUSTOMER_PASSWORD_1}


    [Teardown]   Delete Customer     ${CUSTOMER_NAME_1}

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
    Logout User
    Quit Browser

