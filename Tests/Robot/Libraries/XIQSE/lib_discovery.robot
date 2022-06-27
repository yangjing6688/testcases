#----------------------------------------------------------------------
# Copyright (C) 2021... 2021 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# This file contains keywords specific to the Discovery functionality.
#

*** Settings ***
Library     xiqse/flows/network/XIQSE_Network.py
Library     xiqse/flows/network/devices/site/XIQSE_NetworkDevicesSite.py
Library     xiqse/flows/network/devices/site/discover/XIQSE_NetworkDevicesSiteDiscover.py
Library     xiqse/flows/network/discovered/XIQSE_NetworkDiscovered.py


*** Keywords ***
Navigate to Discovered and Confirm Success
    [Documentation]     Navigates to the Network> Discovered view in XIQ-SE and confirms the action was successful

    ${nav_result}=  XIQSE Navigate to Network Tab
    Should Be Equal As Integers    ${nav_result}    1

    ${disc_result}=  XIQSE Network Select Discovered Tab
    Should Be Equal As Integers    ${disc_result}    1

Perform IP Range Discovery and Ignore License Limit Error
    [Documentation]  Performs an IP Range discovery in XIQ-SE and ignores the license limit error, if displayed
    [Arguments]      ${ip_start}  ${ip_end}  ${profile}  ${auto_add}=false  ${trap}=false  ${syslog}=false  ${archive}=false

    ${disc_result}=  XIQSE Site Perform IP Range Discovery  ${ip_start}  ${ip_end}  ${profile}  auto_add=${auto_add}
    ...  trap=${trap}  syslog=${syslog}  archive=${archive}
    Should Be Equal As Integers  ${disc_result}  1

    ${discovery_complete}=  XIQSE Site Wait Until Discovery Complete
    Should Be Equal As Integers  ${discovery_complete}  1

Perform IP Range Discovery and Confirm Success
    [Documentation]  Performs an IP Range discovery in XIQ-SE and confirms the action was successful
    [Arguments]      ${ip_start}  ${ip_end}  ${profile}  ${auto_add}=false  ${trap}=false  ${syslog}=false  ${archive}=false

    ${disc_result}=  XIQSE Site Perform IP Range Discovery  ${ip_start}  ${ip_end}  ${profile}  auto_add=${auto_add}
    ...  trap=${trap}  syslog=${syslog}  archive=${archive}
    Should Be Equal As Integers  ${disc_result}  1

    ${discovery_complete}=  XIQSE Site Wait Until Discovery Complete
    Should Be Equal As Integers  ${discovery_complete}  1

    # Make sure we didn't get a license limit banner
    Confirm License Limit Warning Message Not Displayed

Perform Subnet Discovery and Confirm Success
    [Documentation]  Performs a subnet discovery in XIQ-SE and confirms the action was successful
    [Arguments]      ${subnet_mask}  ${profile}  ${auto_add}=false  ${trap}=false  ${syslog}=false  ${archive}=false

    ${disc_result}=  XIQSE Site Perform Subnet Discovery  ${subnet_mask}  ${profile}  auto_add=${auto_add}
    ...  trap=${trap}  syslog=${syslog}  archive=${archive}
    Should Be Equal As Integers  ${disc_result}  1

    ${discovery_complete}=  XIQSE Site Wait Until Discovery Complete
    Should Be Equal As Integers  ${discovery_complete}  1

    # Make sure we didn't get a license limit banner
    Confirm License Limit Warning Message Not Displayed

Perform Seed Discovery and Confirm Success
    [Documentation]  Performs a Seed discovery in XIQ-SE and confirms the action was successful
    [Arguments]      ${seed_address}  ${profile}  ${auto_add}=false  ${trap}=false  ${syslog}=false  ${archive}=false

    ${disc_result}=  XIQSE Site Perform Seed Discovery  ${seed_address}  ${profile}  auto_add=${auto_add}
    ...  trap=${trap}  syslog=${syslog}  archive=${archive}
    Should Be Equal As Integers  ${disc_result}  1

    ${discovery_complete}=  XIQSE Site Wait Until Discovery Complete
    Should Be Equal As Integers  ${discovery_complete}  1

Clean Up IP Range Discovery Settings and Confirm Success
    [Documentation]     Cleans up the Site IP Range Discovery settings
    [Arguments]         ${ip_start}  ${ip_end}  ${profile}

    XIQSE Site Select Discover Tab
    ${profile_result}=  XIQSE Discover Set Accept Profile               ${profile}  false
    ${range_result}=    XIQSE Discover Addresses Delete Address Range   ${ip_start}  ${ip_end}
    ${save_result}=     XIQSE Site Save Changes

    Should Be Equal As Integers  ${profile_result}  1
    Should Be Equal As Integers  ${range_result}    1
    Should Be Equal As Integers  ${save_result}     1

Clean Up Subnet Discovery Settings and Confirm Success
    [Documentation]     Cleans up the Site Subnet Discovery settings
    [Arguments]         ${subnet}  ${profile}

    XIQSE Site Select Discover Tab
    ${profile_result}=  XIQSE Discover Set Accept Profile       ${profile}  false
    ${subnet_result}=   XIQSE Discover Addresses Delete Subnet  ${subnet}
    ${save_result}=     XIQSE Site Save Changes

    Should Be Equal As Integers  ${profile_result}  1
    Should Be Equal As Integers  ${subnet_result}   1
    Should Be Equal As Integers  ${save_result}     1

Clean Up Seed Discovery Settings and Confirm Success
    [Documentation]     Cleans up the Site Seed Discovery settings
    [Arguments]         ${seed_address}  ${profile}

    XIQSE Site Select Discover Tab
    ${profile_result}=  XIQSE Discover Set Accept Profile               ${profile}  false
    ${seed_result}=     XIQSE Discover Addresses Delete Seed Address    ${seed_address}
    ${save_result}=     XIQSE Site Save Changes

    Should Be Equal As Integers  ${profile_result}  1
    Should Be Equal As Integers  ${seed_result}    1
    Should Be Equal As Integers  ${save_result}     1

Clear IP From Discovered and Confirm Success
    [Documentation]     Clears the device with the specified IP from the Discovered tab and confirms the action was successful
    [Arguments]         ${ip}

    ${clear_result}=  XIQSE Discovered Clear Row By IP  ${ip}
    Should Be Equal As Integers                         ${clear_result}     1

    # Confirm the device was removed
    Confirm IP Address Not Present in Discovered Table  ${ip}

Clear All From Discovered and Confirm Success
    [Documentation]     Clears all the devices from the Discovered tab and confirms the action was successful

    ${clear_result}=  XIQSE Discovered Clear All Devices
    Should Be Equal As Integers      ${clear_result}     1

    # Confirm all devices were removed
    Confirm Discovered Table Empty

Confirm IP Address Present in Discovered Table
    [Documentation]     Confirms the specified IP address is present in the Discovered table
    [Arguments]         ${ip}

    Navigate to Discovered and Confirm Success
    XIQSE Discovered Refresh Table

    ${result}=  XIQSE Wait Until Discovered Device Added  ${ip}
    Should Be Equal As Integers                           ${result}     1

Confirm IP Address Not Present in Discovered Table
    [Documentation]     Confirms the specified IP address is present in the Discovered table
    [Arguments]         ${ip}

    Navigate to Discovered and Confirm Success
    XIQSE Discovered Refresh Table

    ${result}=  XIQSE Wait Until Discovered Device Removed  ${ip}
    Should Be Equal As Integers                             ${result}     1

Confirm Discovered Row Count
    [Documentation]     Confirms the Discovered tab contains the expected number of rows
    [Arguments]         ${count}

    Navigate to Discovered and Confirm Success
    XIQSE Discovered Refresh Table

    ${wait_result}=  XIQSE Wait Until Discovered Table Contains Row Count  ${count}
    Should Be Equal As Integers      ${wait_result}     1

    ${result}=  XIQSE Discovered Confirm Table Row Count  ${count}
    Should Be Equal As Integers      ${result}     1

Confirm Discovered Table Empty
    [Documentation]     Confirms the Discovered tab is empty

    Navigate to Discovered and Confirm Success
    XIQSE Discovered Refresh Table

    ${wait_result}=  XIQSE Wait Until Discovered Table Empty
    Should Be Equal As Integers      ${wait_result}     1

    ${empty_result}=  XIQSE Discovered Confirm Table Empty
    Should Be Equal As Integers      ${empty_result}     1
