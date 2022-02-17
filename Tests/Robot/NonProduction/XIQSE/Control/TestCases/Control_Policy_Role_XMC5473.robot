#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Kevin Yohe
# Description   : Test Suite for sanity testing of basic XIQSE Control Policy Role functionality.
#                 This is qTest TC-881 in the XIQSE project.

*** Settings ***
Library     xiqse/flows/common/XIQSE_CommonNavigator.py
Library     xiqse/flows/control/XIQSE_Control.py
Library     xiqse/flows/control/policy/XIQSE_ControlPolicy.py
Library     xiqse/flows/control/policy/XIQSE_ControlPolicyDomain.py
Library     xiqse/flows/control/policy/XIQSE_ControlPolicyRole.py
Library     xiqse/flows/control/policy/XIQSE_ControlPolicyDomainSave.py
Library     xiqse/flows/control/policy/XIQSE_ControlPolicyDomainCreate.py

Resource    ../../Control/Resources/AllResources.robot

Force Tags      testbed_1_node

Suite Setup      Log In and Set Up Test
Suite Teardown   Tear Down Test and Close Session
Test Teardown    xiqse control policy save domain

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


*** Test Cases ***
Test 1: Test Create And Delete Policy Role:
    [Documentation]    Creates and deletes a policy role in the test domain
    [Tags]             xiqse_tc_881    xmc_5473    development    xiqse    control    policy    test1

    ${result}=  XIQSE Control Policy Create Role    TestRole
    Should Be Equal As Integers                 ${result}     1
    ${result}=  XIQSE Control Policy Delete Role    TestRole
    Should Be Equal As Integers                 ${result}     1

*** Keywords ***
Log In and Set Up Test
    [Documentation]     Logs in and sets up the components for the test

    Log Into XIQSE and Close Panels              ${XIQSE_USERNAME}  ${XIQSE_PASSWORD}  url=${XIQSE_URL}
    Onboard XIQSE To XIQ If In Connected Mode    ${INSTALL_MODE}  ${XIQSE_IP_ADDRESS}  ${XIQ_EMAIL}  ${XIQ_PASSWORD}
    XIQSE Navigate To Control Policy Tab

    # Create Test Domain
    xiqse control policy create domain   Test Domain

Tear Down Test and Close Session
    [Documentation]     Logs in and cleans up all items that were set up for the test

    Log Out of XIQSE and Quit Browser
    Remove XIQSE From XIQ If In Connected Mode    ${INSTALL_MODE}  ${XIQ_EMAIL}  ${XIQ_PASSWORD}  ${XIQ_URL}  ${XIQSE_MAC}
