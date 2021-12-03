#----------------------------------------------------------------------
# Copyright (C) 2021... 2021 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# This file contains keywords specific to the basic Analytics functionality.
#

*** Settings ***
Library     xiqse/flows/common/XIQSE_CommonNavigator.py
Library     xiqse/flows/analytics/XIQSE_Analytics.py
Library     xiqse/flows/analytics/configuration/XIQSE_AnalyticsConfiguration.py
Library     xiqse/flows/analytics/configuration/XIQSE_AnalyticsConfigurationAddEngine.py
Library     xiqse/flows/analytics/configuration/XIQSE_AnalyticsConfigurationDeleteEngine.py
Library     xiqse/flows/analytics/configuration/XIQSE_AnalyticsConfigurationEnforceEngine.py
Library     xiqse/flows/analytics/configuration/XIQSE_AnalyticsConfigurationEnforceAllEngines.py
Library     xiqse/flows/analytics/configuration/XIQSE_AnalyticsConfigurationRestartCollector.py
Library     xiqse/flows/analytics/flows/XIQSE_AnalyticsApplicationFlows.py


*** Keywords ***
Navigate to Analytics Configuration Panel
    [Documentation]     Navigates to the Analytics> Configuration view in XIQ-SE and confirms the action was successful
    [Arguments]

    ${nav_result}=   XIQSE Navigate to Analytics Configuration Tab
    Should Be Equal As Integers                         ${nav_result}     1

Navigate and Add Analytics Engine
    [Documentation]     Navigates to the Analytics> Configuration view in XIQ-SE and confirms an analytics engine can be added to Analytics Configuration panel
        [Arguments]     ${ip}  ${name}  ${profile}

    Navigate to Analytics Configuration Panel
    XIQSE Close Add Application Analytics Engine Dialog
    Add Analytics Engine and Confirm Success                 ${ip}  ${name}  ${profile}

Add Analytics Engine and Confirm Success
    [Documentation]     Adds Analytics Engine in the Analytics> Configuration view in XIQ-SE and confirms the action was successful
    [Arguments]         ${ip}  ${name}  ${profile}

    ${add_result}=  XIQSE Add Analytics Engine              ${ip}  ${name}  ${profile}
    Should Be Equal As Integers                             ${add_result}     1

    ${confirm_results}=  XIQSE Wait Until Engine Added      ${ip}
    Should Be Equal As Integers                             ${confirm_results}     1

Navigate and Enforce Analytics Engine
    [Documentation]     Navigates to the Analytics> Configuration view in XIQ-SE and enforces an Analytics Engine
    [Arguments]         ${ip}

    Navigate to Analytics Configuration Panel
    Enforce Analytics Engine and Confirm Success            ${ip}

Enforce Analytics Engine and Confirm Success
    [Documentation]     Enforces an Analytics Engine in the Analytics> Configuration view in XIQ-SE
    [Arguments]         ${ip}

    ${confirm_results}=  XIQSE Enforce Selected Engine     ${ip}
    Should Be Equal As Integers                             ${confirm_results}     1

Navigate and Enforce All Analytics Engines
    [Documentation]     Navigates to the Analytics> Configuration view in XIQ-SE and enforces all Analytics Engines
    [Arguments]

    Navigate to Analytics Configuration Panel
    Enforce All Analytics Engines and Confirm Success

Enforce All Analytics Engines and Confirm Success
    [Documentation]     Enforces all  Analytics Engines in the Analytics> Configuration view in XIQ-SE
    [Arguments]

    ${confirm_results}=  XIQSE Enforce All Engines
    Should Be Equal As Integers                             ${confirm_results}     1

Navigate and Poll Analytics Engine
    [Documentation]     Navigates to the Analytics> Configuration view in XIQ-SE and polls the Analytics Engine
    [Arguments]         ${ip}

    Navigate to Analytics Configuration Panel
    Poll Analytics Engine and Confirm Success               ${ip}

Poll Analytics Engine and Confirm Success
    [Documentation]     Polls the Analytics Engine in the Analytics> Configuration view in XIQ-SE
    [Arguments]         ${ip}

    ${confirm_results}=  XIQSE Poll Selected Engine     ${ip}
    Should Be Equal As Integers                         ${confirm_results}     1

Navigate and Restart Collector
    [Documentation]     Navigates to the Analytics> Configuration view in XIQ-SE and Restarts Collector on Analytics Engine
    [Arguments]         ${ip}

    Navigate to Analytics Configuration Panel
    Restart Collector and Confirm Success        ${ip}

Restart Collector and Confirm Success
    [Documentation]     Restarts Collector on Analytics Engine in the Analytics> Configuration view in XIQ-SE
    [Arguments]         ${ip}

    ${confirm_results}=  XIQSE Restart Collector Selected Engine     ${ip}
    Should Be Equal As Integers                                      ${confirm_results}     1

Navigate and Delete Analytics Engine
    [Documentation]     Navigates to the Analytics> Configuration view in XIQ-SE and confirms an analytics engine
    [Arguments]         ${ip}

    Navigate to Analytics Configuration Panel
    Delete Analytics Engine and Confirm Success             ${ip}

Delete Analytics Engine and Confirm Success
    [Documentation]     Confirms an analytics engine can be deleted in Analytics Configuration panel
    [Arguments]         ${ip}

    ${del_result}=  XIQSE Delete Selected Engine            ${ip}
    Should Be Equal As Integers                             ${del_result}       1

    ${confirm_result}=  XIQSE Wait Until Engine Deleted     ${ip}
    Should Be Equal As Integers                             ${confirm_result}   1

Navigate to Analytics Application Flows tab and Confirm Success
    [Documentation]     Navigates to the Analytics> Application Flows in XIQ-SE and confirms the action was successful

    ${nav_result}=   XIQSE Navigate to Analytics Application Flows tab
    Should Be Equal As Integers         ${nav_result}     1

Set Application Flows Search String and Confirm Success
    [Documentation]     Sets the search string on the Applications flows tab
    [Arguments]         ${value}

    ${result}=    XIQSE Application Flows Perform Search  ${value}
    Should Be Equal As Integers    ${result}      1

Clear Application Flows Search String and Confirm Success
    [Documentation]     Clears the search string on the Applications flows tab

    ${result}=  XIQSE Applications Flows Clear Search
    Should Be Equal As Integers  ${result}      1

Confirm Application Flows Row Contains Text
    [Documentation]     Confirms the specified text exists within a row of the Applications Flow tab
    [Arguments]         ${value}

    ${result}=  XIQSE Application Flows Find With Text      ${value}
    Should Be Equal As Integers  ${result}      1
