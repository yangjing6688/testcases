#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : John Borges
# Description   : Test Suite for testing the side navigation for a Helpdesk user on a Pilot/Copilot account
# Topology      : No topology/devices needed
#               : A helpdesk user (helpdesk@cust001.com) will have to be pre-configured before running these tests
#               : Role based accounts listed on ../../../../../Libraries/XIQ/lib_rbac_config.robot


*** Settings ***
Library          xiq/flows/common/Navigator.py
Library          xiq/flows/common/SideNavMenu.py

Resource         ../../SideNavigation/Resources/AllResources.robot

Force Tags       testbed_none

Suite Setup      Log Into XIQ
Suite Teardown   Log Out and Close Session


*** Variables ***
${XIQ_URL}          ${xiq.test_url}


*** Test Cases ***
TCXM-19756: Confirm Manage Menu Is The Only One
    [Documentation]     Confirms the Manage side nav menu item is the only menu, has the correct icon and has all expected submenus
    [Tags]              tcxm_19756   development

    Confirm Main Side Nav Menu Item   ${nav.manage.tag}   ${nav.manage.helpdesk_number}   ${nav.manage.icon_class}

    # check all other menus are not available
    Confirm Main Side Nav Menu Item Is Not There   ${nav.copilot.tag}
    Confirm Main Side Nav Menu Item Is Not There   ${nav.configure.tag}
    Confirm Main Side Nav Menu Item Is Not There   ${nav.insights.tag}
    Confirm Main Side Nav Menu Item Is Not There   ${nav.essentials.tag}
    Confirm Main Side Nav Menu Item Is Not There   ${nav.a3.tag}

    ${nav_result}=      Navigate To Manage Tab
    Should Be Equal As Integers   ${nav_result}  1

    # check all submenus are available and in order
    Confirm Side Nav Menu Item   ${nav.manage.devices.tag}   ${nav.manage.devices.helpdesk_number}
    Confirm Side Nav Menu Item   ${nav.manage.alerts.tag}   ${nav.manage.alerts.helpdesk_number}
    Confirm Side Nav Menu Item   ${nav.manage.diagnosis.tag}   ${nav.manage.diagnosis.helpdesk_number}

    # check all other submenus are not available
    Confirm Side Nav Menu Item Is Not There   ${nav.manage.summary.tag}
    Confirm Side Nav Menu Item Is Not There   ${nav.manage.plan.tag}
    Confirm Side Nav Menu Item Is Not There   ${nav.manage.users.tag}
    Confirm Side Nav Menu Item Is Not There   ${nav.manage.events.tag}
    Confirm Side Nav Menu Item Is Not There   ${nav.manage.reports.tag}
    Confirm Side Nav Menu Item Is Not There   ${nav.manage.applications.tag}
    Confirm Side Nav Menu Item Is Not There   ${nav.manage.security.tag}
    Confirm Side Nav Menu Item Is Not There   ${nav.manage.vpn.tag}

    ${nav_result}=      Navigate To Devices
    Should Be Equal As Integers   ${nav_result}   1
    ${nav_url}=         Is The Expected Url   ${nav.manage.devices.url}
    Should Be Equal As Integers   ${nav_url}   1

    ${nav_result}=      Navigate Manage Alerts
    Should Be Equal As Integers   ${nav_result}   1
    ${nav_url}=         Is The Expected Url   ${nav.manage.alerts.url}
    Should Be Equal As Integers   ${nav_url}   1

    ${nav_result}=      Navigate To Client Monitor And Diagnosis Tab
    Should Be Equal As Integers   ${nav_result}   1
    ${nav_url}=         Is The Expected Url   ${nav.manage.diagnosis.url}
    Should Be Equal As Integers   ${nav_url}   1


*** Keywords ***
Log Into XIQ
    [Documentation]     Logs into XIQ

    Log Into XIQ and Confirm Success  ${XIQ_HD_USER}   ${XIQ_HD_PASSWORD}   ${XIQ_URL}

Log Out and Close Session
    [Documentation]     Logs out of XIQ and closes the browser

    Log Out of XIQ and Quit Browser

Confirm Main Side Nav Menu Item
    [Documentation]     Confirm main menu item is visible, enabled, in the expected location and has the correct icon
    [Arguments]         ${tag}   ${order}   ${icon_class}

    # check tab is visible
    ${nav_visible}=     Is Nav Menu Item Visible   ${tag}
    Should Be Equal As Integers   ${nav_visible}   1
    # check tab is in the expected order number
    ${nav_order}=       Get Order Number Of Main Nav Tab   ${tag}
    Should Be Equal As Integers   ${nav_order}   ${order}
    # check tab has the correct icon
    ${nav_icon}=        Has Main Nav Tab The Expected Image   ${tag}  ${icon_class}
    Should Be Equal As Integers   ${nav_icon}   1

Confirm Main Side Nav Menu Item Is Not There
    [Documentation]     Confirm main menu item is not visible
    [Arguments]         ${tag}

    ${nav_visible}=     Is Nav Menu Item Visible   ${tag}
    Should Be Equal As Integers   ${nav_visible}   -1

Confirm Side Nav Menu Item
    [Documentation]     Confirm side menu item is visible, enabled and in the expected location
    [Arguments]         ${tag}   ${order}

    # check that menu item is visible
    ${nav_visible}=     Is Nav Menu Item Visible   ${tag}
    Should Be Equal As Integers   ${nav_visible}   1
    # check that menu item is in the expected order number
    ${nav_order}=       Get Order Number Of Side Nav Menu Item   ${tag}
    Should Be Equal As Integers   ${nav_order}   ${order}
    # check tab is enabled
    ${nav_enabled}      Is Nav Menu Item Enabled   ${tag}
    Should Be Equal As Integers   ${nav_enabled}   1

Confirm Side Nav Menu Item Is Not There
    [Documentation]     Confirm side menu item is not visible
    [Arguments]         ${tag}

    ${nav_visible}=     Is Nav Menu Item Visible   ${tag}
    Should Be Equal As Integers   ${nav_visible}   -1
