#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : David W. Truesdell
# Description   : Test Suite for testing Connect user licensing when user does not have CoPilot/Pilot/Navigator entitlements
#               : This test assumes the XIQ user has NO entitlements
#               : This verifies a user without CoPilot entitlements can't enable the feature
#               : This is qTest test case tccs-13711 in the CSIT project.


*** Settings ***
Resource         ../../Connect_User/Resources/AllResources.robot

Force Tags       testbed_no_node

Suite Setup      Log Into XIQ and Set Up Test
Suite Teardown   Tear Down Test and Close Session


*** Variables ***
${XIQ_URL}                      ${test_url}
${XIQ_USER}                     ${tenant_username}
${XIQ_PASSWORD}                 ${tenant_password}


*** Test Cases ***
Test 1: Verify CoPilot Entitlement Not Present in License Management
    [Documentation]     Confirms CoPilot entitlement is not present in Licemse Management table
    [Tags]              tccs-13711    connect_release_testing    connect_sanity_testing    aiq-2214    development    xiq    copilot    test1

    Confirm Entitlements Table Does Not Contain Feature         PRD-XIQ-PIL-S-C
    Confirm Entitlements Table Does Not Contain Feature         PRD-XIQ-COPILOT-S-C
    Confirm Entitlements Table Does Not Contain Feature         PRD-XIQ-NAV-S-C

Test 2: Verify User Unable to "Enable CoPilot" Within CoPilot Menu Page and Alert Warning Present
    [Documentation]     Verifies the "Enable CoPilot" feature from CoPilot Menu page in not available to select and alert warning present
    [Tags]              tccs-13711    connect_release_testing    connect_sanity_testing    aiq-2214    development    xiq    copilot    test2

    Depends On          Test 1

    Enable CoPilot Menu Feature and Confirm No CoPilot Entitlements


*** Keywords ***
Log Into XIQ and Set Up Test
    [Documentation]     Logs into XIQ and sets up the elements necessary to complete this test suite

    # Use this method to convert the ap, wing, netelem to a generic device object
    # ap1       => device1
    # wing1     => device1
    # netelem1  => device1 (EXOS / VOSS)
    convert to generic device object            device  index=1

    Log Into XIQ and Confirm Success            ${XIQ_USER}  ${XIQ_PASSWORD}  ${XIQ_URL}

Tear Down Test and Close Session
    [Documentation]     Cleans up test data, logs out of XIQ, and closes the browser

    Log Out of XIQ and Quit Browser

Enable CoPilot Menu Feature and Confirm No CoPilot Entitlements
    [Documentation]     Verifies user is not able to click on "Enable CoPilot" feature in main CoPilot web page since user has no copilot entitlements

    ${result_enable}=               Enable CoPilot Menu Feature   expect_error=True
    Should Be Equal As Strings      ${result_enable}     False

Confirm Entitlements Table Does Not Contain Feature
    [Documentation]     Checks to see if feature is in License Management table
    [Arguments]         ${feature}

    ${result_feature}=   Confirm Entitlements Table Contains Feature             ${feature}
    Should Be Equal As Integers                       ${result_feature}      -1
