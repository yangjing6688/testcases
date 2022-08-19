#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Heidi S. White
# Description   : Test Suite for sanity testing of the License Agreement amd Welcome/Onboard pages.
#                 This is qTest TC-104 in the XIQ-SE project.

*** Settings ***
Resource        ../../SampleTests/Resources/AllResources.robot

Force Tags      testbed_0_node


*** Variables ***
${ENV}                  environment.remote.chrome.windows.xiqse1.yaml
${TOPO}                 topo.test.xiqse1.connected.yaml
${TESTBED}              SALEM/Dev/devices-salem-acceptance.yaml

${XIQSE_URL}            ${xiqse.url}
${XIQSE_USER}           ${xiqse.user}
${XIQSE_PASSWORD}       ${xiqse.password}
${XIQSE_IP}             ${xiqse.ip}

${XIQ_USER}             ${xiq.tenant_username}
${XIQ_PASSWORD}         ${xiq.tenant_password}


*** Test Cases ***
Test 1: Confirm License Agreement Page is Displayed Correctly
    [Documentation]     Confirms the license agreement page is displayed correctly
    [Tags]              tcxe_104    aiq_1332    development    sample    xiqse    license_agreement    test1

    [Setup]     Log Into XIQSE and confirm Success  ${XIQSE_USER}  ${XIQSE_PASSWORD}  url=${XIQSE_URL}

    # Confirm license page is displayed
    ${disp_result}=  XIQSE Confirm License Agreement Page Displayed
    Should Be Equal As Integers    ${disp_result}     1

    # Confirm default values
    ${desel_result}=  XIQSE Confirm Accept License Agreement Checkbox Deselected
    Should Be Equal As Integers    ${desel_result}     1

    ${next_result}=  XIQSE Confirm License Agreement Next Button Disabled
    Should Be Equal As Integers    ${next_result}     1

    # Confirm button states
    ${accept_result}=  XIQSE Accept License Agreement
    Should Be Equal As Integers    ${accept_result}     1

    ${sel_result}=  XIQSE Confirm Accept License Agreement Checkbox Selected
    Should Be Equal As Integers    ${sel_result}     1

    ${next_result}=  XIQSE Confirm License Agreement Next Button Enabled
    Should Be Equal As Integers    ${next_result}     1

    ${decline_result}=  XIQSE Decline License Agreement
    Should Be Equal As Integers    ${decline_result}     1

    ${desel_result}=  XIQSE Confirm Accept License Agreement Checkbox Deselected
    Should Be Equal As Integers    ${desel_result}     1

    ${next_result}=  XIQSE Confirm License Agreement Next Button Disabled
    Should Be Equal As Integers    ${next_result}     1

    [Teardown]    XIQSE Quit Browser

Test 2: Confirm License Agreement Can Be Accepted
    [Documentation]     Confirms the license agreement can be accepted
    [Tags]              tcxe_104    aiq_1332    development    sample    xiqse    license_agreement     test2

    [Setup]     Log Into XIQSE and Confirm Success  ${XIQSE_USER}  ${XIQSE_PASSWORD}  url=${XIQSE_URL}

    # Accept the License Agreement if it is displayed
    ${license_displayed}=  XIQSE Confirm License Agreement Page Displayed
    Run Keyword If  '${license_displayed}' == '1'    Accept License Agreement
    ...  ELSE  Log To Console  License Agreement Page Not Displayed

    [Teardown]    XIQSE Quit Browser

Test 3: Confirm XIQ-SE Can Be Onboarded via License Agreement Workflow
    [Documentation]     Confirms XIQ-SE can be onboarded without error
    [Tags]              tcxe_104    aiq_1332    development    sample    xiqse    license_agreement     test3

    [Setup]    Log Into XIQSE and Confirm Success       ${XIQSE_USER}  ${XIQSE_PASSWORD}  url=${XIQSE_URL}

    Handle License Agreement If Displayed               ${XIQ_USER}  ${XIQ_PASSWORD}
    Close Panels on Login If Displayed
    Navigate and Confirm XIQSE Onboarded Successfully   ${XIQSE_IP}

    [Teardown]    XIQSE Quit Browser
