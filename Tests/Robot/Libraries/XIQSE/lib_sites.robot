#----------------------------------------------------------------------
# Copyright (C) 2021... 2021 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# This file contains keywords specific to the Sites functionality.
#

*** Settings ***
Library     xiqse/flows/network/devices/tree_panel/XIQSE_NetworkDevicesTreePanel.py
Library     xiqse/flows/network/devices/site/XIQSE_NetworkDevicesSite.py


*** Keywords ***
Navigate to Site Context and Confirm Success
    [Documentation]     Navigates to Network> Devices, selects the Sites tree context, and selects the site in the tree
    [Arguments]         ${site}

    # Navigate to the Devices view
    Navigate to Devices and Confirm Success

    # Select the Sites device tree context
    ${context_result}=  XIQSE Devices Select Device Tree Context  Sites
    Should Be Equal As Integers     ${context_result}     1

    # Select the specified site in the tree
    Select Site and Confirm Success  ${site}

Navigate to Site Tree Node and Confirm Success
    [Documentation]     Navigates to Network> Devices and selects the specified site in the tree
    [Arguments]         ${site}

    # Navigate to the Devices view
    Navigate to Devices and Confirm Success

    # Select the specified site in the tree
    Select Site and Confirm Success  ${site}

Navigate to Site Tab and Confirm Success
    [Documentation]     Navigates to the specified site tab in XIQ-SE and confirms the action was successful
    [Arguments]         ${site}

    # Navigate to the site context
    Navigate to Site Tree Node and Confirm Success  ${site}

    # Select the site tab
    ${sel_tab}=  XIQSE Devices Select Site Tab      ${site}
    Should Be Equal As Integers     ${sel_tab}      1

Navigate to Site Devices and Confirm Success
    [Documentation]     Navigates to the Devices tab for the specified site in XIQ-SE and confirms the action was successful
    [Arguments]         ${site}

    # Navigate to the site context
    Navigate to Site Tree Node and Confirm Success  ${site}

    # Select the Devices tab
    ${sel_tab}=  XIQSE Devices Select Devices Tab
    Should Be Equal As Integers     ${sel_tab}      1

Navigate and Create Site
    [Documentation]     Navigates to the World site on the Devices tab and creates the specified site, confirming it was added
    [Arguments]         ${site}

    Navigate to Site Tree Node and Confirm Success  World
    Create Site and Confirm Success                 ${site}

Navigate and Delete Site
    [Documentation]     Navigates to the World site on the Devices tab and deletes the specified site, confirming it was removed
    [Arguments]         ${site}

    Navigate to Site Tree Node and Confirm Success  World
    Delete Site and Confirm Success                 ${site}

Create Site and Confirm Success
    [Documentation]     Creates the specified site
    [Arguments]         ${site}

    ${result}=  XIQSE Devices Create Site  ${site}
    Should Be Equal As Integers  ${result}  1

Delete Site and Confirm Success
    [Documentation]     Deletes the specified site
    [Arguments]         ${site}

    ${result}=  XIQSE Devices Delete Site  ${site}
    Should Be Equal As Integers  ${result}  1

Select Site and Confirm Success
    [Documentation]     Selects the specified site
    [Arguments]         ${site}

    # Select the specified site in the tree
    ${sel_tree}=  XIQSE Devices Select Site Tree Node  ${site}
    Should Be Equal As Integers     ${sel_tree}     1

Save Site Changes and Confirm Success
    [Documentation]  Clicks Save on the Site tab to save the changes

    ${save_result}=  XIQSE Site Click Save
    Should Be Equal As Integers      ${save_result}    1

Disable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver
    [Documentation]     In the Sites Actions tab, uncheck the boxes for Add to Archive, Add Trap Receiver & Add Syslog Receiver
    [Arguments]         ${site}

    Navigate to Site Tab and Confirm Success    ${site}

    ${actions_result}=  XIQSE Site Select Actions Tab
    Should Be Equal As Integers         ${actions_result}        1

    ${actions_result}=  XIQSE Actions Set Add Trap Receiver      false
    Should Be Equal As Integers         ${actions_result}        1

    ${actions_result}=  XIQSE Actions Set Add Syslog Receiver    false
    Should Be Equal As Integers         ${actions_result}        1

    ${actions_result}=  XIQSE Actions Set Add To Archive         false
    Should Be Equal As Integers         ${actions_result}        1

    Save Site Changes and Confirm Success

Enable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver
    [Documentation]     In the Sites Actions tab, check the boxes for Add to Archive, Add Trap Receiver & Add Syslog Receiver
    [Arguments]         ${site}

    Navigate to Site Tab and Confirm Success    ${site}

    ${actions_result}=  XIQSE Site Select Actions Tab
    Should Be Equal As Integers         ${actions_result}     1

    ${actions_result}=  XIQSE Actions Set Add Trap Receiver   true
    Should Be Equal As Integers         ${actions_result}     1

    ${actions_result}=  XIQSE Actions Set Add Syslog Receiver  true
    Should Be Equal As Integers         ${actions_result}     1

    ${actions_result}=  XIQSE Actions Set Add To Archive       true
    Should Be Equal As Integers         ${actions_result}     1

    Save Site Changes and Confirm Success
