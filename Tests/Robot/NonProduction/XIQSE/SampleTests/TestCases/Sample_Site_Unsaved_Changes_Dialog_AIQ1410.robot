# ----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
# ----------------------------------------------------------------------
#
# Author        : Dan McCarthy
# Description   : AIQ-1410: Test Suite for sanity testing of the XIQ-SE Site 'Unsaved Changes' dialog

*** Settings ***
Library         xiqse/flows/network/devices/site/ztp_device_defaults/XIQSE_NetworkDevicesSiteZtpDeviceDefaults.py

Resource        ../../SampleTests/Resources/AllResources.robot

Force Tags      testbed_0_node

Suite Setup     Log Into XIQSE and Close Panels    ${XIQSE_USER}  ${XIQSE_PASSWORD}  url=${XIQSE_URL}
Suite Teardown  Log Out of XIQSE and Quit Browser


*** Variables ***
${ENV}              environment.remote.chrome.windows.xiqse1.yaml
${TOPO}             topo.test.xiqse1.connected.yaml
${TESTBED}          SALEM/Dev/devices-salem-acceptance.yaml

${XIQSE_URL}        ${xiqse.url}
${XIQSE_USER}       ${xiqse.user}
${XIQSE_PASSWORD}   ${xiqse.password}


*** Test Cases ***
Test 1: Site Unsaved Changes Click Yes
    [Documentation]     Confirms the Yes button can be selected in the 'Site - Unsaved Changes' dialog panel.
    [Tags]              tcxe_941    aiq-1410    development     xiqse     site      test1

    Navigate to Site and Select ZTP+ Device Defaults            World

    ${actions_result}=  XIQSE Site Ztp Set Domain Name          test01.site.org
    Should Be Equal As Integers         ${actions_result}       1

    ${actions_result}=  XIQSE Site Ztp Set Dns Server           10.54.37.63
    Should Be Equal As Integers         ${actions_result}       1

    ${actions_result}=  XIQSE Devices Select Devices Tab
    Should Be Equal As Integers         ${actions_result}       1

    ${actions_result}=  XIQSE Site Unsaved Changes Dialog       Yes
    Should Be Equal As Integers         ${actions_result}       1

    ${actions_result}=  XIQSE Devices Select Devices Tab
    Should Be Equal As Integers         ${actions_result}       1

Test 2: Site Unsaved Changes Click No
    [Documentation]     Confirms the No button can be selected in the 'Site - Unsaved Changes' dialog panel.
    [Tags]              tcxe_941    aiq-1410    development     xiqse     site      test2

    Navigate to Site and Select ZTP+ Device Defaults            World

    ${actions_result}=  XIQSE Site Ztp Set Domain Name          test02.site.org
    Should Be Equal As Integers         ${actions_result}       1

    ${actions_result}=  XIQSE Site Ztp Set Dns Server           10.57.252.11
    Should Be Equal As Integers         ${actions_result}       1

    ${actions_result}=  XIQSE Devices Select Devices Tab
    Should Be Equal As Integers         ${actions_result}       1

    ${actions_result}=  XIQSE Site Unsaved Changes Dialog       No
    Should Be Equal As Integers         ${actions_result}       1

    ${actions_result}=  XIQSE Devices Select Devices Tab
    Should Be Equal As Integers         ${actions_result}       1

Test 3: Site Unsaved Changes Click Cancel
    [Documentation]     Confirms the Cancel button can be selected in the 'Site - Unsaved Changes' dialog panel.
    [Tags]              tcxe_941    aiq-1410    development     xiqse     site      test3

    Navigate to Site and Select ZTP+ Device Defaults            World

    ${actions_result}=  XIQSE Site Ztp Set Domain Name          test03.site.org
    Should Be Equal As Integers         ${actions_result}       1

    ${actions_result}=  XIQSE Site Ztp Set Dns Server           10.57.252.12
    Should Be Equal As Integers         ${actions_result}       1

    ${actions_result}=  XIQSE Devices Select Devices Tab
    Should Be Equal As Integers         ${actions_result}       1

    ${actions_result}=  XIQSE Site Unsaved Changes Dialog       Cancel
    Should Be Equal As Integers         ${actions_result}       1

    ${save_result}=  XIQSE Site Click Save
    Should Be Equal As Integers         ${save_result}          1

    ${actions_result}=  XIQSE Devices Select Devices Tab
    Should Be Equal As Integers         ${actions_result}       1

*** Keywords ***
Navigate to Site and Select ZTP+ Device Defaults
    [Documentation]     Navigate to the Site and select the ZTP+ Device Defaults tab
    [Arguments]         ${site}

    ${nav_result}=  XIQSE Navigate to Network Devices Tab
    Should Be Equal As Integers         ${nav_result}           1

    ${sel_tree}=  XIQSE Devices Select Site Tree Node           ${site}
    Should Be Equal As Integers         ${sel_tree}             1

    ${site_result}=  XIQSE Devices Select Site Tab              ${site}
    Should Be Equal As Integers         ${site_result}          1

    ${actions_result}=  XIQSE Site Select ZTP Device Defaults Tab
    Should Be Equal As Integers         ${actions_result}       1
