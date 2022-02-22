#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
# Author        : Kiet Tran
# Description   : Test Suite for sanity testing of basic Policy Manager on XIQ-SE.  XMC-4477.
#                 This is qTest TC-880 in the XIQSE project.
# NOTE:         : To run this test, execute "robot Control_Policy_Sanity_XMC5473.robot"

*** Settings ***
Library     Collections
Library     xiqse/flows/control/policy/XIQSE_ControlPolicy.py
Library     xiqse/flows/control/policy/XIQSE_ControlPolicyDomainOpenManageMenu.py
Library     xiqse/flows/control/policy/XIQSE_ControlPolicyDomainCreate.py
Library     xiqse/flows/control/policy/XIQSE_ControlPolicyDomainDelete.py
Library     xiqse/flows/control/policy/XIQSE_ControlPolicyDomainAssignDevice.py
Library     xiqse/flows/control/policy/XIQSE_ControlPolicyDomainSave.py
Library     xiqse/flows/control/policy/XIQSE_ControlPolicyDomainEnforce.py
Library     xiqse/flows/control/policy/XIQSE_ControlPolicyDomainVerify.py
Library     xiqse/flows/control/policy/XIQSE_ControlPolicyDomainEnforcePreview.py
Library     xiqse/flows/control/policy/XIQSE_ControlPolicyRole.py
Library     xiqse/flows/control/policy/XIQSE_ControlPolicyServiceCreate.py
Library     xiqse/flows/control/policy/XIQSE_ControlPolicyServiceDelete.py
Library     xiqse/flows/control/policy/XIQSE_ControlPolicyRuleCreate.py
Library     xiqse/flows/control/policy/XIQSE_ControlPolicyRuleDelete.py

Resource    ../../Control/Resources/AllResources.robot

Force Tags      testbed_1_node

Suite Setup      Log In and Set Up Test
Suite Teardown   Tear Down Test and Close Session

*** Variables ***
${XIQSE_URL}                ${xiqse.url}
${XIQSE_USERNAME}           ${xiqse.user}
${XIQSE_PASSWORD}           ${xiqse.password}
${XIQSE_IP_ADDRESS}         ${xiqse.ip}
${XIQSE_MAC}                ${xiqse.mac}
${INSTALL_MODE}             ${upgrades.install_mode}

${XIQ_URL}                  ${xiq.test_url}
${XIQ_EMAIL}                ${xiq.tenant_username}
${XIQ_PASSWORD}             ${xiq.tenant_password}

${DUT_IP}                   ${netelem1.ip}
${DUT_PROFILE}              ${netelem1.profile}

${DOMAIN_NAME}              Pol-extauto-Domain
${ROLE_NAME}                auto-role-1
${SERVICE_NAME}             auto-service-1
${RULE_NAME}                auto-rule-1
${WORLD_SITE}               World


*** Test Cases ***
Test 1: Create Domain
    [Documentation]     Create a new policy domain
    [Tags]              xiqse_tc_880    xmc_5473    development    xiqse    acceptance    control    policy    create_domain    test1
    
    Navigate to Control Policy Tab and Dismiss Cached Window

    ${create_domain_result}=  XIQSE Control Policy Create Domain        ${DOMAIN_NAME}
    Should Be Equal As Integers     ${create_domain_result}     1

Test 2: Assign Device to Domain
    [Documentation]     Assign a device to the current policy domain
    [Tags]              xiqse_tc_880    xmc_5473    development    xiqse    acceptance    control    policy    assign_device_to_domain    test2
    
    XIQSE Control Policy Select Assign Devices to Domain Menu

    ${assign_dev_result}=  XIQSE Control Policy Assign Device to Domain    ${DUT_IP}
    Should Be Equal As Integers     ${assign_dev_result}     1

Test 3: Create Role In The Domain
    [Documentation]     Create a role in the current policy domain
    [Tags]              xiqse_tc_880    xmc_5473    development    xiqse    acceptance    control    policy    create_role    test3
    
    ${create_role_result}=  XIQSE Control Policy Create Role   ${ROLE_NAME}
    Should Be Equal As Integers     ${create_role_result}     1

Test 4: Create Service In The Domain
    [Documentation]     Create a "Local" service in the current policy domain
    [Tags]              xiqse_tc_880    xmc_5473    development    xiqse    acceptance    control    policy    create_service    test4
    
    ${create_service_result}=  XIQSE Control Policy Create Service    ${SERVICE_NAME}   local
    Should Be Equal As Integers     ${create_service_result}     1

Test 5: Create Rule In The Domain
    [Documentation]     Create a "Local" rule in the current policy domain
    [Tags]              xiqse_tc_880    xmc_5473    development    xiqse    acceptance    control    policy    create_rule    test5
    
    ${create_rule_result}=  XIQSE Control Policy Create Rule    ${RULE_NAME}  ${SERVICE_NAME}  local
    Should Be Equal As Integers     ${create_rule_result}     1

Test 6: Delete Rule In The Domain
    [Documentation]     Delete a "Local" rule in the current policy domain
    [Tags]              xiqse_tc_880    xmc_5473    development    xiqse    acceptance    control    policy    delete_rule    test6
    
    ${del_rule_result}=  XIQSE Control Policy Delete Rule    ${RULE_NAME}  ${SERVICE_NAME}  local
    Should Be Equal As Integers     ${del_rule_result}     1

Test 7: Delete Service In The Domain
    [Documentation]     Delete a "Local" service in the current policy domain
    [Tags]              xiqse_tc_880    xmc_5473    development    xiqse    acceptance    control    policy    delete_service    test7
    
    ${del_serv_result}=  XIQSE Control Policy Delete Service    ${SERVICE_NAME}   local
    Should Be Equal As Integers     ${del_serv_result}     1

Test 8: Delete Role In The Domain
    [Documentation]     Delete a role in the current policy domain
    [Tags]              xiqse_tc_880    xmc_5473    development    xiqse    acceptance    control    policy    delete_role    test8
    
    ${del_serv_result}=  XIQSE Control Policy Delete Role    ${ROLE_NAME}
    Should Be Equal As Integers     ${del_serv_result}     1

Test 9: Save Domain
    [Documentation]     Save the current policy domain
    [Tags]              xiqse_tc_880    xmc_5473    development    xiqse    acceptance    control    policy    save_domain    test9
    
    ${save_domain_result}=  XIQSE Control Policy Save Domain
    Should Be Equal As Integers     ${save_domain_result}     1

Test 10: Enforce Domain
    [Documentation]     Enforce the current policy domain
    [Tags]              xiqse_tc_880    xmc_5473    development    xiqse    acceptance    control    policy    enforce_domain    test10
    
    ${enforce_domain_result}=  XIQSE Control Policy Enforce Domain
    Should Be Equal As Integers     ${enforce_domain_result}     1

Test 11: Verify Domain
    [Documentation]     Verify the current policy domain
    [Tags]              xiqse_tc_880    xmc_5473    development    xiqse    acceptance    control    policy    verify_domain    test11
        
    # MUST save policy domain before perform Verify. If not, the "cache" dialog will interrupt the test
    XIQSE Control Policy Select Verify Domain Menu

    ${verify_domain_result}=  XIQSE Control Policy Verify Domain
    Should Be Equal As Integers     ${verify_domain_result}     1

Test 12: Delete Domain
    [Documentation]     Delete the current policy domain
    [Tags]              xiqse_tc_880    xmc_5473    development    xiqse    acceptance    control    policy    delete_domain    test12
    
    ${delete_result}=   XIQSE Control Policy Delete Domain      ${DOMAIN_NAME}
    Should Be Equal As Integers                                 ${delete_result}     1


*** Keywords ***
Log In and Set Up Test
    [Documentation]     Logs in and sets up the components for the test

    Log Into XIQSE and Close Panels              ${XIQSE_USERNAME}    ${XIQSE_PASSWORD}    url=${XIQSE_URL}
    Disable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver    ${WORLD_SITE}
    Onboard XIQSE To XIQ If In Connected Mode    ${INSTALL_MODE}  ${XIQSE_IP_ADDRESS}  ${XIQ_EMAIL}  ${XIQ_PASSWORD}
    Navigate and Create Device                   ${DUT_IP}  ${DUT_PROFILE}

Tear Down Test and Close Session
    [Documentation]     Logs in and cleans up all items that were set up for the test
    
    Navigate to Devices and Confirm Success
    Delete Device and Confirm Success              ${DUT_IP}
    Enable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver    ${WORLD_SITE}
    Log Out of XIQSE and Quit Browser
    Remove XIQSE From XIQ If In Connected Mode     ${INSTALL_MODE}  ${XIQ_EMAIL}  ${XIQ_PASSWORD}  ${XIQ_URL}  ${XIQSE_MAC}

Navigate to Control Policy Tab and Dismiss Cached Window
    [Documentation]     Navigate to Control Policy tab and dismiss "Cached" window, if present

    ${nav_policy}=  XIQSE Navigate to Control Policy Tab
    Should Be Equal As Integers         ${nav_policy}     1

    XIQSE Control Policy Dismiss Cached Window
