# Author        : Heidi S. White
# Description   : Test Suite for sanity testing of the XIQ-SE to XIQ onboarding functionality:
#                   - onboards XIQ Site Engine via the License Agreement workflow (TC-9525)
#                   - onboards XIQ Site Engine via the Auto Onboard button in Administration> Diagnostics (TC-9528)
#                 This is qTest test cases TC-9525 and TC-9528 in the CSIT project.

*** Settings ***
Resource        ../../Onboarding/Resources/AllResources.robot

Force Tags      testbed_0_node


*** Variables ***
# Defaults
${ENV}                  environment.remote.chrome.windows.xiqse1.yaml
${TOPO}                 topo.test.xiqse1.connected.yaml
${TESTBED}              SALEM/Dev/devices-salem-acceptance.yaml

${XIQSE_URL}            ${xiqse.url}
${XIQSE_USER}           ${xiqse.user}
${XIQSE_PASSWORD}       ${xiqse.password}
${XIQSE_SERIAL}         ${xiqse.serial}
${XIQSE_IP}             ${xiqse.ip}
${XIQSE_MAC}            ${xiqse.mac}
${XIQSE_VERSION}        ${xiqse.version}

${XIQ_URL}              ${xiq.test_url}
${XIQ_USER}             ${xiq.tenant_username}
${XIQ_PASSWORD}         ${xiq.tenant_password}

@{COLUMNS}              Serial #  Managed By  MAC Address  Make  Model  MGT IP Address  OS  OS Version
${LICENSE_SUFFIX}       /xiqLicenseSetup.jsp?setupMode=xiq


*** Test Cases ***
TC-9525: Confirm XIQ-SE Can Be Onboarded via License Agreement Workflow
    [Documentation]     Confirms the XIQ Site Engine can be onboarded using the license agreement workflow
    [Tags]              nightly2    release_testing    staging_testing    csit_tc_9525    xmc_3196    development    xiqse    xiq_integration    onboarding    license

    [Setup]  Log In and Set Up Test for License Agreement Workflow

    Log To Console  This Test Only Works for XIQSE 21.4.x

    [Teardown]  Tear Down Test and Close Session

TC-9528: Confirm Site Engine Onboarded via Auto Onboard Workflow
    [Documentation]     Confirms the XIQ Site Engine can be onboarded successfully using the Auto Onboard button
    [Tags]              nightly2    release_testing    staging_testing    csit_tc_9528    xmc_3196    development    xiqse    xiq_integration    onboarding     auto

    [Setup]  Log In and Set Up Test for Button Workflow

    Remove Existing Site Engine from XIQ
    Auto Onboard XIQ Site Engine
    Confirm XIQ Site Engine Onboarded to XIQ
    Confirm Diagnostics Page Shows XIQSE Onboarded Successfully

    [Teardown]  Tear Down Test and Close Session


*** Keywords ***
Log In and Set Up Test for License Agreement Workflow
    [Documentation]     Logs in and sets up the components for the test using the License Agreement workflow

    Run Keyword If  '21.4' in '${XIQSE_VERSION}'  Perform 21.4.x License Agreement Workflow
    ...  ELSE  Perform License Agreement Workflow

Log In and Set Up Test for Button Workflow
    [Documentation]     Logs in and sets up the components for the test using the Auto Onboard Button workflow

    XIQSE Log In and Set Window Index
    Set Up XIQSE Components

    XIQ Log In and Set Window Index
    Set Up XIQ Components

Tear Down Test and Close Session
    [Documentation]     Cleans up XIQ and XIQSE test components and closes the browser

    Clean Up XIQ Components
    Clean Up XIQSE Components
    Quit Browser and Confirm Success

XIQSE Log In and Set Window Index
    [Documentation]     Logs into XIQSE and sets the window index

    Log Into XIQSE and Confirm Success              ${XIQSE_USER}  ${XIQSE_PASSWORD}  url=${XIQSE_URL}
    Handle License Agreement If Displayed           ${XIQ_USER}  ${XIQ_PASSWORD}

    # Close any banner messages (Connection Lost with XIQ, License Expiration, etc.) and the Help panel, if displayed
    Close Panels on Login If Displayed

    # Store the window index so we can switch between XIQSE and XIQ
    ${xiqse_win}=  XIQSE Get Window Index
    Log To Console  Setting XIQSE Window Index to ${xiqse_win}
    Set Suite Variable  ${XIQSE_WINDOW_INDEX}  ${xiqse_win}

XIQ Log In and Set Window Index
    [Documentation]     Logs into XIQ and sets the window index

    Log Into XIQ and Confirm Success    ${XIQ_USER}  ${XIQ_PASSWORD}  url=${XIQ_URL}

    ${xiq_win}=  Get Window Index
    Log To Console  Setting XIQ Window Index to ${xiq_win}
    Set Suite Variable  ${XIQ_WINDOW_INDEX}  ${xiq_win}

Set Up XIQSE Components
    [Documentation]     Sets up the XIQSE components for the test

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    # Confirm the serial number is correct and set the common options needed for automation
    Confirm Serial Number and Set Common Options     ${XIQSE_SERIAL}

Set Up XIQ Components
    [Documentation]     Sets up the XIQ components for the test

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Navigate to XIQ Devices and Confirm Success
    Column Picker Select  @{COLUMNS}

Perform 21.4.x License Agreement Workflow
    [Documentation]     Performs the License Agreement workflow in place for 21.4.x versions of XIQSE

    ${result}=  XIQSE Load Page    url=${XIQSE_URL}${LICENSE_SUFFIX}
    Should Be Equal As Integers    ${result}     1

    ${xiqse_win}=  XIQSE Get Window Index
    Log To Console  Setting XIQ-SE Window Index to ${xiqse_win}
    Set Suite Variable  ${XIQSE_WINDOW_INDEX}  ${xiqse_win}

    XIQ Log In and Set Window Index
    Set Up XIQ Components

    Remove Existing Site Engine from XIQ

    Switch To Window  ${XIQSE_WINDOW_INDEX}
    Handle License Agreement If Displayed    ${XIQ_USER}  ${XIQ_PASSWORD}
    XIQSE Login User  ${XIQSE_USER}  ${XIQSE_PASSWORD}
    Close Panels on Login If Displayed

    Confirm Diagnostics Page Shows XIQSE Onboarded Successfully
    Confirm XIQ Site Engine Onboarded to XIQ

Perform License Agreement Workflow
    [Documentation]     Performs the License Agreement workflow in place for current (post 21.4.x) versions of XIQSE

    Log To Console  Need to Log Into XIQSE and then load the license URL to do this test flow

    XIQSE Log In and Set Window Index

    XIQ Log In and Set Window Index
    Set Up XIQ Components

    Remove Existing Site Engine from XIQ

    Switch To Window  ${XIQSE_WINDOW_INDEX}

Remove Existing Site Engine from XIQ
    [Documentation]     Removes the XIQ Site Engine from XIQ if it exists

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Navigate and Remove Device by MAC From XIQ  ${XIQSE_MAC}

Auto Onboard XIQ Site Engine
    [Documentation]     Onboards the specified XIQ Site Engine, deleting it first if it already exists

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Enter XIQ Credentials to Auto Onboard XIQSE  ${XIQ_USER}  ${XIQ_PASSWORD}

Confirm XIQ Site Engine Onboarded to XIQ
    [Documentation]     Confirms the XIQ Site Engine has been onboarded to XIQ successfully

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Confirm Device Serial Present   ${XIQSE_SERIAL}
    Confirm Device Serial Online    ${XIQSE_SERIAL}

Confirm Diagnostics Page Shows XIQSE Onboarded Successfully
    [Documentation]     Confirms the Administration> Diagnostics page shows XIQSE has a SUCCESS onboard status

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Run Keyword If  '21.4' in '${XIQSE_VERSION}'  Log To Console  21.4.x Shows Unkmown Onboard Status: XMC-4898
    ...  ELSE  Navigate and Confirm XIQSE Onboarded Successfully   ${XIQSE_IP}

Clean Up XIQ Components
    [Documentation]     Cleans up components used in XIQ during the test and logs out

    Switch To Window                        ${XIQ_WINDOW_INDEX}

    # Make sure XIQSE has been removed
    Remove Existing Site Engine from XIQ

    # Log out of XIQ and close the window
    Log Out of XIQ and Confirm Success
    Close Window                            ${XIQ_WINDOW_INDEX}

Clean Up XIQSE Components
    [Documentation]     Cleans up components used in XIQ-SE during the test and logs out

    Switch To Window                        ${XIQSE_WINDOW_INDEX}
    Log Out of XIQSE and Confirm Success
