#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Heidi S. White
# Description   : Test Suite for sanity testing of basic XIQ-SE archives functionality.
#                 This is qTest TC-136 in the XIQ-SE project.

*** Settings ***
Resource        ../../SampleTests/Resources/AllResources.robot

Force Tags      testbed_3_node

Suite Setup     Log In and Set Up Test
Suite Teardown  Tear Down Test and Close Session


*** Variables ***
${ENV}                  environment.remote.chrome.windows.xiqse1.yaml
${TOPO}                 topo.test.xiqse1.connected.yaml
${TESTBED}              SALEM/Dev/devices-salem-acceptance.yaml

${XIQSE_URL}            ${xiqse.url}
${XIQSE_USER}           ${xiqse.user}
${XIQSE_PASSWORD}       ${xiqse.password}

${DUT1_IP}              ${netelem1.ip}
${DUT1_PROFILE}         ${netelem1.profile}

${DUT2_IP}              ${netelem2.ip}
${DUT2_PROFILE}         ${netelem2.profile}

${DUT3_IP}              ${netelem3.ip}
${DUT3_PROFILE}         ${netelem3.profile}

${SINGLE_ARCHIVE}       AUTO_SINGLE_ARCHIVE
${MULTI_ARCHIVE}        AUTO_MULTI_ARCHIVE


*** Test Cases ***
Test 1: Create Archive with Single Device and No Frequency Specified
    [Documentation]     Confirms an archive can be created with a single device and the default frquency
    [Tags]              tcxe_136    aiq_1332    development    sample    xiqse    archives    test1

    Navigate and Create Archive    ${SINGLE_ARCHIVE}    ${DUT1_IP}

Test 2: Create Archive with Multiple Devices and a Frequency Specified
    [Documentation]     Confirms an archive can be created with multiple devices and a specified frequency
    [Tags]              tcxe_136    aiq_1332    development    sample    xiqse    archives    test2

    Navigate and Create Archive    ${MULTI_ARCHIVE}  ${DUT1_IP},${DUT2_IP},${DUT3_IP}  frequency=Daily

Test 3: Stamp New Version for Archive
    [Documentation]     Confirms the Stamp New Version action can be performed on an archive
    [Tags]              tcxe_136    aiq_1332    development    sample    xiqse    archives    test3

    Navigate to Archives and Confirm Success
    Stamp New Version and Confirm Success       ${SINGLE_ARCHIVE}
    Stamp New Version and Confirm Success       ${MULTI_ARCHIVE}

Test 4: Delete Archive
    [Documentation]     Confirms an archive can be deleted (depends on tests 1 and 2 to successfully create the archives)
    [Tags]              tcxe_136    aiq_1332    development    sample    xiqse    archives    test4

    Navigate to Archives and Confirm Success
    Delete Archive and Confirm Success          ${SINGLE_ARCHIVE}
    Delete Archive and Confirm Success          ${MULTI_ARCHIVE}


*** Keywords ***
Log In and Set Up Test
    [Documentation]     Logs in and sets up the components for the test

    # Log into XIQSE and close the banner messages and help panel
    Log Into XIQSE and Close Panels     ${XIQSE_USER}    ${XIQSE_PASSWORD}    url=${XIQSE_URL}

    # Create the devices to use in the test
    Navigate to Devices and Confirm Success
    Create Device and Confirm Success           ${DUT1_IP}  ${DUT1_PROFILE}
    Create Device and Confirm Success           ${DUT2_IP}  ${DUT2_PROFILE}
    Create Device and Confirm Success           ${DUT3_IP}  ${DUT3_PROFILE}

    # Set the option to display devices in trees with their IP Address
    Set Option Device Tree Name Format and Confirm Success   IP Address

Tear Down Test and Close Session
    [Documentation]     Cleans up XIQ and XIQSE test components and closes the browser

    # Delete the test devices
    Navigate to Devices and Confirm Success
    Delete Device and Confirm Success           ${DUT1_IP}
    Delete Device and Confirm Success           ${DUT2_IP}
    Delete Device and Confirm Success           ${DUT3_IP}

    # Log out of XIQSE and close the browser
    Log Out of XIQSE and Quit Browser
