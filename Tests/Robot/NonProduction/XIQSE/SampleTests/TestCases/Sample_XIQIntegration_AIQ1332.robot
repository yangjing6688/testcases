#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Heidi S. White
# Description   : Test Suite for sanity testing of basic XIQ Integration functionality.
#                 Logs into both XIQSE and XIQ, onboards XIQSE to XIQ, removes XIQSE from XIQ,
#                 and logs out of XIQ and XIQSE.
#                 This is qTest TC-899 in the XIQ-SE project.

*** Settings ***
Resource        ../../SampleTests/Resources/AllResources.robot

Force Tags      testbed_0_node

Suite Setup     Log In and Set Up Test
Suite Teardown  Tear Down Test and Close Session


*** Variables ***
${ENV}                  environment.remote.chrome.windows.xiqse1.yaml
${TOPO}                 topo.test.xiqse1.connected.yaml
${TESTBED}              SALEM/Dev/devices-salem-acceptance.yaml

${XIQSE_URL}            ${xiqse.url}
${XIQSE_USER}           ${xiqse.user}
${XIQSE_PASSWORD}       ${xiqse.password}
${XIQSE_SERIAL}         ${xiqse.serial}
${XIQSE_IP}             ${xiqse.ip}
${XIQSE_MAC}            ${xiqse.mac}
${XIQSE_NAME}           ${xiqse.name}

${XIQ_URL}              ${xiq.test_url}
${XIQ_USER}             ${xiq.tenant_username}
${XIQ_PASSWORD}         ${xiq.tenant_password}


*** Test Cases ***
Test 1: Onboard XIQSE to XIQ
    [Documentation]     Onboards XIQSE to XIQ and confirms the onboard was successful
    [Tags]              tcxe_899    aiq_1332    development    sample    xiqse    xiq_integration    test1

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Navigate to XIQ Device Message Details and Confirm Success
    Onboard XIQSE if Not Onboarded          ${XIQSE_IP}  ${XIQ_USER}  ${XIQ_PASSWORD}
    Confirm XIQSE Onboarded Successfully    ${XIQSE_IP}

Test 2: Confirm XIQSE Present in XIQ Devices Table
    [Documentation]     Performs a search in the XIQ Devices table for XIQSE and confirms XIQSE is present
    [Tags]              tcxe_899    aiq_1332    development    sample    xiqse    xiq_integration    test2

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Navigate Filter and Confirm Device MAC Present  ${XIQSE_MAC}

    Search XIQ Devices Table and Confirm Success  ${XIQSE_SERIAL}
    Confirm Device Serial Present  ${XIQSE_SERIAL}
    Confirm Device Name Present  ${XIQSE_NAME}
    Clear Search on XIQ Devices Table and Confirm Success

Test 3: Remove XIQSE from XIQ
    [Documentation]     Removes XIQSE from XIQ
    [Tags]              tcxe_899    aiq_1332    development    sample    xiqse    xiq_integration    test3

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Navigate and Remove Device by MAC From XIQ   ${XIQSE_MAC}

Test 4: Confirm XIQSE Not Present in XIQ Devices Table
    [Documentation]     Confirms XIQSE is not present in XIQ Devices table
    [Tags]              tcxe_899    aiq_1332    development    sample    xiqse    xiq_integration    test4

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Confirm Device MAC Address Not Present  ${XIQSE_MAC}
    Confirm Device Serial Not Present  ${XIQSE_SERIAL}
    Confirm Device Name Not Present  ${XIQSE_NAME}


*** Keywords ***
Log In and Set Up Test
    [Documentation]     Sets up the components for the test

    XIQSE Log In and Set Window Index
    Set Up XIQSE Components

    XIQ Log In and Set Window Index

Tear Down Test and Close Session
    [Documentation]     Cleans up XIQ and XIQ-SE test components

    Clean Up XIQ Components
    Clean Up XIQSE Components
    XIQSE Quit Browser

XIQSE Log In and Set Window Index
    [Documentation]     Logs into XIQ-SE and confirms the login was successful

    Log Into XIQSE and Confirm Success    ${XIQSE_USER}    ${XIQSE_PASSWORD}    url=${XIQSE_URL}

    # Close any banner messages (Connection Lost with XIQ, License Expiration, etc.) and the Help panel, if displayed
    Close Panels on Login If Displayed

    # Store the window index so we can switch between XIQSE and XIQ
    ${xiqse_win}=  XIQSE Get Window Index
    Log To Console  Setting XIQSE Window Index to ${xiqse_win}
    Set Suite Variable  ${XIQSE_WINDOW_INDEX}  ${xiqse_win}

XIQ Log In and Set Window Index
    [Documentation]     Logs into XIQ and confirms the login was successful

    Log Into XIQ and Confirm Success    ${XIQ_USER}  ${XIQ_PASSWORD}  ${XIQ_URL}

    ${xiq_win}=  Get Window Index
    Log To Console  Setting XIQ Window Index to ${xiq_win}
    Set Suite Variable  ${XIQ_WINDOW_INDEX}  ${xiq_win}

Set Up XIQSE Components
    [Documentation]     Sets up the XIQ-SE components for the test

    # Confirm the XIQ-SE serial number
    Confirm XIQSE Serial Number  ${XIQSE_SERIAL}

Clean Up XIQ Components
    [Documentation]     Cleans up components used in XIQ during the test and logs out

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Navigate and Remove Device by MAC From XIQ   ${XIQSE_MAC}

    Log Out of XIQ and Confirm Success

Clean Up XIQSE Components
    [Documentation]     Cleans up components used in XIQ-SE during the test and logs out

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    # Log out
    Log Out of XIQSE and Confirm Success
