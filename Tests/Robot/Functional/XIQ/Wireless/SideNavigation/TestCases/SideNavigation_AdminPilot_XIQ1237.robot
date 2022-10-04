#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : John Borges
# Description   : Test Suite for testing the side navigation for an Admin user on a Pilot/Copilot account
# Topology      : No topology/device needed


*** Settings ***
Library          xiq/flows/common/Navigator.py
Library          xiq/flows/common/SideNavMenu.py

Resource         ../../SideNavigation/Resources/AllResources.robot

Force Tags       testbed_none

Suite Setup      Log Into XIQ
Suite Teardown   Log Out and Close Session


*** Variables ***
${XIQ_URL}          ${test_url}
${XIQ_USER}         ${tenant_username}
${XIQ_PASSWORD}     ${tenant_password}


*** Test Cases ***
TCXM-15229: Confirm Copilot On Top Menu
    [Documentation]     Confirms the Copilot side nav menu item is on top and has the correct icon
    [Tags]              tcxm_15229   development

    Confirm Main Side Nav Menu Item    ${nav.copilot.tag}   ${nav.copilot.pilot_number}   ${nav.copilot.icon_class}

    # navigate to copilot
    ${nav_result}=      Navigate To Copilot Menu
    Should Be Equal As Integers   ${nav_result}   1
    # check if url is correct
    ${nav_url}=         Is The Expected Url   ${nav.copilot.url}
    Should Be Equal As Integers   ${nav_url}   1

TCXM-18146: Confirm Configure Menu
    [Documentation]     Confirms the Configure side nav menu item is the 2nd memu, has the correct icon and has all expected submenus
    [Tags]              tcxm_18146   development

    Confirm Main Side Nav Menu Item    ${nav.configure.tag}   ${nav.configure.pilot_number}   ${nav.configure.icon_class}

    ${nav_result}=      Navigate To Configure Tab
    Should Be Equal As Integers   ${nav_result}  1

    # check all submenus are available and in order
    Confirm Side Nav Menu Item   ${nav.configure.policies.tag}   ${nav.configure.policies.pilot_number}
    Confirm Side Nav Menu Item   ${nav.configure.guest.tag}   ${nav.configure.guest.pilot_number}

    # check all submenus open the correct pages
    ${nav_result}=      Navigate Configure Network Policies
    Should Be Equal As Integers   ${nav_result}   1
    ${nav_url}=         Is The Expected Url   ${nav.configure.policies.url}
    Should Be Equal As Integers   ${nav_url}   1

    ${nav_result}=      Navigate To Configure Guest Essentials Users
    Should Be Equal As Integers   ${nav_result}   1
    ${nav_url}=         Is The Expected Url   ${nav.configure.guest.url}
    Should Be Equal As Integers   ${nav_url}   1

TCXM-18162: Confirm Manage Menu
    [Documentation]     Confirms the Manage side nav menu item is the 3rd menu, has the correct icon and has all expected submenus
    [Tags]              tcxm_18162   development

    Confirm Main Side Nav Menu Item   ${nav.manage.tag}   ${nav.manage.pilot_number}   ${nav.manage.icon_class}

    ${nav_result}=      Navigate To Manage Tab
    Should Be Equal As Integers   ${nav_result}  1

    # check all submenus are available and in order
    Confirm Side Nav Menu Item   ${nav.manage.summary.tag}   ${nav.manage.summary.pilot_number}
    Confirm Side Nav Menu Item   ${nav.manage.plan.tag}   ${nav.manage.plan.pilot_number}
    Confirm Side Nav Menu Item   ${nav.manage.devices.tag}   ${nav.manage.devices.pilot_number}
    Confirm Side Nav Menu Item   ${nav.manage.users.tag}   ${nav.manage.users.pilot_number}
    Confirm Side Nav Menu Item   ${nav.manage.events.tag}   ${nav.manage.events.pilot_number}
    Confirm Side Nav Menu Item   ${nav.manage.alerts.tag}   ${nav.manage.alerts.pilot_number}
    Confirm Side Nav Menu Item   ${nav.manage.reports.tag}   ${nav.manage.reports.pilot_number}
    Confirm Side Nav Menu Item   ${nav.manage.applications.tag}   ${nav.manage.applications.pilot_number}
    Confirm Side Nav Menu Item   ${nav.manage.security.tag}   ${nav.manage.security.pilot_number}
    Confirm Side Nav Menu Item   ${nav.manage.diagnosis.tag}   ${nav.manage.diagnosis.pilot_number}
    Confirm Side Nav Menu Item   ${nav.manage.vpn.tag}   ${nav.manage.vpn.pilot_number}

    # check all submenus open the correct pages
    ${nav_result}=      Navigate To Manage Summary
    Should Be Equal As Integers   ${nav_result}   1
    ${nav_url}=         Is The Expected Url   ${nav.manage.summary.url}
    Should Be Equal As Integers   ${nav_url}   1

    ${nav_result}=      Navigate To Network360Plan
    Should Be Equal As Integers   ${nav_result}   1
    ${nav_url}=         Is The Expected Url   ${nav.manage.plan.url}
    Should Be Equal As Integers   ${nav_url}   1

    ${nav_result}=      Navigate To Devices
    Should Be Equal As Integers   ${nav_result}   1
    ${nav_url}=         Is The Expected Url   ${nav.manage.devices.url}
    Should Be Equal As Integers   ${nav_url}   1

    ${nav_result}=      Navigate To Manage Users
    Should Be Equal As Integers   ${nav_result}   1
    ${nav_url}=         Is The Expected Url   ${nav.manage.users.url}
    Should Be Equal As Integers   ${nav_url}   1

    ${nav_result}=      Navigate Manage Events
    Should Be Equal As Integers   ${nav_result}   1
    ${nav_url}=         Is The Expected Url   ${nav.manage.events.url}
    Should Be Equal As Integers   ${nav_url}   1

    ${nav_result}=      Navigate Manage Alerts
    Should Be Equal As Integers   ${nav_result}   1
    ${nav_url}=         Is The Expected Url   ${nav.manage.alerts.url}
    Should Be Equal As Integers   ${nav_url}   1

    ${nav_result}=      Navigate To Manage Reports
    Should Be Equal As Integers   ${nav_result}   1
    ${nav_url}=         Is The Expected Url   ${nav.manage.reports.url}
    Should Be Equal As Integers   ${nav_url}   1

    ${nav_result}=      Navigate Manage Application
    Should Be Equal As Integers   ${nav_result}   1
    ${nav_url}=         Is The Expected Url   ${nav.manage.applications.url}
    Should Be Equal As Integers   ${nav_url}   1

    ${nav_result}=      Navigate Manage Security
    Should Be Equal As Integers   ${nav_result}   1
    ${nav_url}=         Is The Expected Url   ${nav.manage.security.url}
    Should Be Equal As Integers   ${nav_url}   1

    ${nav_result}=      Navigate To Client Monitor And Diagnosis Tab
    Should Be Equal As Integers   ${nav_result}   1
    ${nav_url}=         Is The Expected Url   ${nav.manage.diagnosis.url}
    Should Be Equal As Integers   ${nav_url}   1

    ${nav_result}=      Navigate To Vpn Management Tab
    Should Be Equal As Integers   ${nav_result}   1
    ${nav_url}=         Is The Expected Url   ${nav.manage.vpn.url}
    Should Be Equal As Integers   ${nav_url}   1

TCXM-18163: Confirm ML Insights Menu
    [Documentation]     Confirms the ML Insights side nav menu item is the 4th menu, has the correct icon and has all expected submenus
    [Tags]              tcxm_18163   development

    Confirm Main Side Nav Menu Item   ${nav.insights.tag}   ${nav.insights.pilot_number}   ${nav.insights.icon_class}

    ${nav_result}=      Navigate To ML Insight tab
    Should Be Equal As Integers   ${nav_result}  1
    # navigate again to expand menu panel
    ${nav_result}=      Navigate To ML Insight tab
    Should Be Equal As Integers   ${nav_result}  1

    # check all submenus are available and in order
    Confirm Side Nav Menu Item   ${nav.insights.monitor.tag}   ${nav.insights.monitor.pilot_number}
    Confirm Side Nav Menu Item   ${nav.insights.scorecard.tag}   ${nav.insights.scorecard.pilot_number}
    Confirm Side Nav Menu Item   ${nav.insights.clients.tag}   ${nav.insights.clients.pilot_number}
#    Handle this later when we add the needed automation tags to check industry
#    Confirm Side Nav Menu Item   ${nav.insights.retail.tag}   ${nav.insights.retail.pilot_number}

    # check all submenus open the correct pages
    ${nav_url}=         Is The Expected Url   ${nav.insights.monitor.url}
    Should Be Equal As Integers   ${nav_url}   1

    ${nav_result}=      Navigate To Network Scorecard
    Should Be Equal As Integers   ${nav_result}   1
    ${nav_url}=         Is The Expected Url   ${nav.insights.scorecard.url}
    Should Be Equal As Integers   ${nav_url}   1

    ${nav_result}=      Navigate To Client360
    Should Be Equal As Integers   ${nav_result}   1
    ${nav_url}=         Is The Expected Url   ${nav.insights.clients.url}
    Should Be Equal As Integers   ${nav_url}   1

#    Handle this later when we add the needed automation tags to check industry
#    ${nav_result}=      Navigate To Retail Dashboard
#    Should Be Equal As Integers   ${nav_result}   1
#    ${nav_url}=         Is The Expected Url   ${nav.insights.retail.url}
#    Should Be Equal As Integers   ${nav_url}   1

TCXM-15230: Confirm Essentials Menu
    [Documentation]     Confirms the Essentials side nav menu item is the 5th, has the correct icon and has all expected submenus
    [Tags]              tcxm_15230   development

    Confirm Main Side Nav Menu Item    ${nav.essentials.tag}   ${nav.essentials.pilot_number}   ${nav.essentials.icon_class}

    ${nav_result}=      Navigate To Essentials Menu
    Should Be Equal As Integers   ${nav_result}   1

    # check all submenus are available and in order
    Confirm Side Nav Menu Item   ${nav.essentials.iot.tag}   ${nav.essentials.iot.pilot_number}
    Confirm Side Nav Menu Item   ${nav.essentials.airdefense.tag}   ${nav.essentials.airdefense.pilot_number}
    Confirm Side Nav Menu Item   ${nav.essentials.guest.tag}   ${nav.essentials.guest.pilot_number}
    Confirm Side Nav Menu Item   ${nav.essentials.location.tag}   ${nav.essentials.location.pilot_number}

    # check all submenus open the correct pages
    ${nav_result}=      Navigate To Extreme IOT Menu
    Should Be Equal As Integers   ${nav_result}   1
    ${nav_url}=         Is The Expected Url   ${nav.essentials.iot.url}
    Run Keyword If      ${nav_url} != 1   Confirm IOT Submenu

    ${nav_result}=      Navigate To Extreme AirDefence
    Should Be Equal As Integers   ${nav_result}   1
    ${nav_url}=         Is The Expected Url   ${nav.essentials.airdefense.url}
    Should Be Equal As Integers   ${nav_url}   1

    ${nav_result}=      Navigate To Extreme Guest Menu
    Should Be Equal As Integers   ${nav_result}   1
    ${nav_url}=         Is The Expected Url   ${nav.essentials.guest.url}
    Should Be Equal As Integers   ${nav_url}   1

    ${nav_result}=      Navigate To Extreme Location Menu
    Should Be Equal As Integers   ${nav_result}   1
    ${nav_url}=         Is The Expected Url   ${nav.essentials.location.url}
    Should Be Equal As Integers   ${nav_url}   1

TCXM-18164: Confirm A3 Menu
    [Documentation]     Confirms the A3 side nav menu item is the 6th menu, has the correct icon and has all the expected submenus
    [Tags]              tcxm_18164   development

    Confirm Main Side Nav Menu Item   ${nav.a3.tag}   ${nav.a3.pilot_number}   ${nav.a3.icon_class}

    ${nav_result}=      Navigate To A3 Menu
    Should Be Equal As Integers   ${nav_result}  1

    # check all submenus are available and in order
    Confirm Side Nav Menu Item   ${nav.a3.inventory.tag}   ${nav.a3.inventory.pilot_number}
    Confirm Side Nav Menu Item   ${nav.a3.reporting.tag}   ${nav.a3.reporting.pilot_number}

    # check all submenus open the correct pages
    ${nav_result}=      Navigate A3 Inventory
    Should Be Equal As Integers   ${nav_result}   1
    ${nav_url}=         Is The Expected Url   ${nav.a3.inventory.url}
    Should Be Equal As Integers   ${nav_url}   1

    ${nav_result}=      Navigate A3 Reporting
    Should Be Equal As Integers   ${nav_result}   1
    ${nav_url}=         Is The Expected Url   ${nav.a3.reporting.url}
    Should Be Equal As Integers   ${nav_url}   1


*** Keywords ***
Log Into XIQ
    [Documentation]     Logs into XIQ

    Log Into XIQ and Confirm Success  ${XIQ_USER}  ${XIQ_PASSWORD}  ${XIQ_URL}

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

Confirm Side Nav Sub Menu Item
    [Documentation]     Confirm side sub menu item is visible, enabled and in the expected location
    [Arguments]         ${tag}   ${order}

    # check that sub menu item is visible
    ${nav_visible}=     Is Nav Menu Item Visible   ${tag}
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_order}=       Get Order Number Of Side Nav Sub Menu Item   ${tag}
    Should Be Equal As Integers   ${nav_order}   ${order}
    # check tab is enabled
    ${nav_enabled}      Is Nav Menu Item Enabled   ${tag}
    Should Be Equal As Integers   ${nav_enabled}   1

Confirm IOT Submenu
    [Documentation]     Confirm IOT side menu items are visible, enabled and in the expected location

    Confirm Side Nav Sub Menu Item   ${nav.essentials.iot.dashboard.tag}   ${nav.essentials.iot.dashboard.pilot_number}
    Confirm Side Nav Sub Menu Item   ${nav.essentials.iot.devices.tag}    ${nav.essentials.iot.devices.pilot_number}
    Confirm Side Nav Sub Menu Item   ${nav.essentials.iot.clients.tag}   ${nav.essentials.iot.clients.pilot_number}
    Confirm Side Nav Sub Menu Item   ${nav.essentials.iot.userprofile.tag}   ${nav.essentials.iot.userprofile.pilot_number}
    Confirm Side Nav Sub Menu Item   ${nav.essentials.iot.groups.tag}   ${nav.essentials.iot.groups.pilot_number}

    # check all submenus open the correct pages
    ${nav_result}=      Navigate To Extreme IOT Dashboard Page
    Should Be Equal As Integers   ${nav_result}   1
    ${nav_url}=         Is The Expected Url   ${nav.essentials.iot.dashboard.url}
    Should Be Equal As Integers   ${nav_url}   1
    ${nav_result}=      Navigate To Extreme IOT Devices Page
    Should Be Equal As Integers   ${nav_result}   1
    ${nav_url}=         Is The Expected Url   ${nav.essentials.iot.devices.url}
    Should Be Equal As Integers   ${nav_url}   1
    ${nav_result}=      Navigate To Extreme IOT Clients Page
    Should Be Equal As Integers   ${nav_result}   1
    ${nav_url}=         Is The Expected Url   ${nav.essentials.iot.clients.url}
    Should Be Equal As Integers   ${nav_url}   1
    ${nav_result}=      Navigate To Extreme IOT User Profiles Page
    Should Be Equal As Integers   ${nav_result}   1
    ${nav_url}=         Is The Expected Url   ${nav.essentials.iot.userprofile.url}
    Should Be Equal As Integers   ${nav_url}   1
    ${nav_result}=      Navigate To Extreme IOT Policy Groups Page
    Should Be Equal As Integers   ${nav_result}   1
    ${nav_url}=         Is The Expected Url   ${nav.essentials.iot.groups.url}
    Should Be Equal As Integers   ${nav_url}   1
