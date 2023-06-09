#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : John Borges
# Modified By   : Ramkumar Vellasamy
# Description   : Test Suite for testing the helpdesk user access to features on devices page
# Topology      : One simulated device will be onboarded
#               : A helpdesk user will have to be pre-configured before running these tests


*** Settings ***
Library          xiq/flows/common/DeviceCommon.py
Library          xiq/flows/globalsettings/AccountManagement.py
Library          common/GmailHandler.py

Resource         ../../ManageDevices/Resources/AllResources.robot

Force Tags       testbed_1_node

Suite Setup      Log Into XIQ and Set Up Test
Suite Teardown   Tear Down Test and Close Session


*** Variables ***
${XIQ_URL}           ${test_url}
${XIQ_USER}          ${tenant_username}
${XIQ_PASSWORD}      ${tenant_password}
${SIM_SERIAL}
${SIM_LOCATION}      auto_location_01, Santa Clara, building_02, floor_04


*** Test Cases ***
TCXM-19759: Confirm That Left Side Action Icons Are Not Available
    [Documentation]     Confirms that the left side grid action icons (add, download, edit, delete) are not visible
    [Tags]              tcxm_19759   development

    Navigate to Devices and Confirm Success

    ${btn_visible}=     validate add button hidden
    Should Be Equal As Integers   ${btn_visible}   1
    ${btn_visible}=     validate download button hidden
    Should Be Equal As Integers   ${btn_visible}   1
    ${btn_visible}=    validate bulk edit button hidden
    Should Be Equal As Integers   ${btn_visible}   1
    ${btn_visible}=    validate delete button hidden
    Should Be Equal As Integers   ${btn_visible}   1

TCXM-19758: Confirm The Update Device Button Is Not Available
    [Documentation]     Confirms that the right side Update Device button is not visible
    [Tags]              tcxm_19758   development

    ${btn_visible}=    validate update device button hidden
    Should Be Equal As Integers   ${btn_visible}   1

TCXM-19835: Confirm The Actions Button Is Not Available
    [Documentation]     Confirms that the right side Actions button is not visible
    [Tags]              tcxm_19835   development

    ${btn_visible}=     validate actions button hidden
    Should Be Equal As Integers   ${btn_visible}   1

TCXM-19834: Confirm The Utilities Button Is Available
    [Documentation]     Confirms that the right side Utilities button is visible
    [Tags]              tcxm_19834   development

    ${btn_visible}=     validate utilities button visible
    Should Be Equal As Integers   ${btn_visible}   1

TCXM-19760: Confirm No Access To Device360
    [Documentation]     Confirms no access to the Device360 popup
    [Tags]              tcxm_19760   development

    ${is_link}=         Verify Hostname Link Not Available   ${device.serial}
    Should Be Equal As Integers   ${is_link}   1
    ${is_link}=         Verify Mac Link Not Available   ${device.serial}
    Should Be Equal As Integers   ${is_link}   1

TCXM-19838: Confirm No Access To Device360 With Clients
    [Documentation]     Confirms no access to the Device360 popup through clients
    [Tags]              tcxm_19838   development

    ${is_link}=         Verify Client Link Not Available   ${device.serial}
    Should Be Equal As Integers   ${is_link}   1

TCXM-19836: Confirm No Access To Policy Change
    [Documentation]     Confirms no access to the policy change popup
    [Tags]              tcxm_19836   development

    ${is_link}=         Verify Policy Link Not Available   ${device.serial}
    Should Be Equal As Integers   ${is_link}   1

TCXM-19837: Confirm No Access To Location Change
    [Documentation]     Confirms no access to the location change popup
    [Tags]              tcxm_19837   development

    ${is_link}=         Verify Location Link Not Available   ${device.serial}
    Should Be Equal As Integers   ${is_link}   1


*** Keywords ***

Create HelpDesk Role Account
    [Documentation]     Create HelpDesk Role Account
    [Arguments]         ${HELPDESK_ROLE}
    Login User  ${TENANT_USERNAME}    ${TENANT_PASSWORD}
    Create Role Based Account        ${HELPDESK_ROLE}
    logout user
    sleep   4s
    ${URL}=                 get_url_to_set_password_for_new_user     ${HELPDESK_EMAIL}     ${HELPDESK_APP_PASSWORD}
    ${DRIVER}=              load web page       url=${URL}
    ${result2}=             set_password      ${help_password}
    Quit Browser

Log Into XIQ and Set Up Test
    [Documentation]     Logs into XIQ

    ${device}=      Create Dictionary
    ...     name=simulated_dut04
    ...     model=AP460C
    ...     simulated_count=1
    ...     onboard_device_type=Simulated
    ...     location=auto_location_01, Santa Clara, building_02, floor_04

    set suite variable    ${device}
    Log Into XIQ and Confirm Success   ${XIQ_USER}   ${XIQ_PASSWORD}   ${XIQ_URL}

    ${ONBOARD_RESULT}=      onboard device quick    ${device}
    Should Be Equal As Strings          ${ONBOARD_RESULT}       1

    Delete Management Account   ${XIQ_HD_USER}
    Log Out of XIQ and Quit Browser
    Create HelpDesk Role Account        ${HELPDESK_ROLE}
    Log Into XIQ and Confirm Success   ${XIQ_HD_USER}   ${XIQ_HD_PASSWORD}   ${XIQ_URL}

Tear Down Test and Close Session
    [Documentation]     Cleans up test data, logs out of XIQ, and closes the browser

    Log Out of XIQ and Quit Browser
    Log Into XIQ and Confirm Success   ${XIQ_USER}   ${XIQ_PASSWORD}   ${XIQ_URL}
    Delete Device and Confirm Success   ${device.serial}
    Confirm Device Serial Not Present   ${device.serial}
    Log Out of XIQ and Quit Browser
