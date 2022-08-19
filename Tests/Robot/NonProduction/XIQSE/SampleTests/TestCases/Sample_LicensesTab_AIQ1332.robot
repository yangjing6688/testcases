#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Heidi S. White
# Description   : Test Suite for sanity testing of basic XIQ-SE Admin> Licenses tab functionality.
#                 This is qTest TC-893 in the XIQ-SE project.

*** Settings ***
Library         xiqse/flows/admin/licenses/XIQSE_AdminLicenses.py

Resource        ../../SampleTests/Resources/AllResources.robot

Force Tags      testbed_0_node

Suite Setup     Log Into XIQSE and Close Panels     ${XIQSE_USER}    ${XIQSE_PASSWORD}    url=${XIQSE_URL}
Suite Teardown  Log Out of XIQSE and Quit Browser


*** Variables ***
${ENV}                  environment.remote.chrome.windows.xiqse1.yaml
${TOPO}                 topo.test.xiqse1.connected.yaml
${TESTBED}              SALEM/Dev/devices-salem-acceptance.yaml

${XIQSE_URL}            ${xiqse.url}
${XIQSE_USER}           ${xiqse.user}
${XIQSE_PASSWORD}       ${xiqse.password}


*** Test Cases ***
Test 1: Retrieve Pilot License Count
    [Documentation]     Retrieves the total Pilot licenses found on the Administration> Licenses tab
    [Tags]              tcxe_893    aiq_1332    development    sample    xiqse    licenses_tab    test1

    Navigate to Licenses and Confirm Success
    ${pilot_count}=  XIQSE Get License Quantity For Feature  XIQ-PIL-S-C
    Log To Console  Pilot count is ${pilot_count}

Test 2: Retrieve Navigator License Count
    [Documentation]     Retrieves the total Navigator licenses found on the Administration> Licenses tab
    [Tags]              tcxe_893    aiq_1332    development    sample    xiqse    licenses_tab    test2

    Navigate to Licenses and Confirm Success
    ${nav_count}=  XIQSE Get License Quantity For Feature  XIQ-NAV-S-C
    Log To Console  Navigator count is ${nav_count}

Test 3: Retrieve NAC License Count
    [Documentation]     Retrieves the total NAC licenses found on the Administration> Licenses tab
    [Tags]              tcxe_893    aiq_1332    development    sample    xiqse    licenses_tab    test3

    Navigate to Licenses and Confirm Success
    ${nac_count}=  XIQSE Get License Quantity For Feature  XIQ-NAC-S
    Log To Console  NAC count is ${nac_count}
