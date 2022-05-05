#----------------------------------------------------------------------
# Copyright (C) 2021... 2021 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# This file contains keywords specific to the basic License Agreement functionality.
#

*** Settings ***
Library     xiqse/flows/admin/XIQSE_Administration.py
Library     xiqse/flows/common/XIQSE_CommonNavigator.py
Library     xiqse/flows/license/XIQSE_LicenseAgreement.py
Library     xiqse/flows/license/XIQSE_LicenseDeployment.py
Library     xiqse/flows/license/XIQSE_LicenseOnboard.py


*** Keywords ***
Navigate to Licenses and Confirm Success
    [Documentation]     Navigates to the Administration> Licenses view in XIQ-SE and confirms the action was successful

    ${nav_result}=  XIQSE Navigate to Administration Tab
    Should Be Equal As Integers    ${nav_result}    1

    ${lic_result}=  XIQSE Admin Select Licenses Tab
    Should Be Equal As Integers    ${lic_result}    1

Handle License Agreement If Displayed
    [Documentation]     Handles accepting the license agreement and entering XIQ credentials if it is displayed
    [Arguments]         ${xiq_email}  ${xiq_pwd}

    # If the License Agreement page is displayed, enter the required information
    ${license_displayed}=  XIQSE Confirm License Agreement Page Displayed
    Run Keyword If  '${license_displayed}' == '1'    Handle License Agreement and Onboard to XIQ  ${xiq_email}  ${xiq_pwd}
    ...  ELSE  Log To Console  License Agreement Page Not Displayed

Handle License Agreement and Onboard to XIQ
    [Documentation]     Handles accepting the license agreement and entering XIQ credentials if it is displayed
    [Arguments]         ${xiq_email}  ${xiq_pwd}

    Accept License Agreement
    Enter XIQ Credentials on Onboard Page    ${xiq_email}  ${xiq_pwd}

    # Make sure the XIQSE version is set
    Get XIQSE Version

    Run Keyword If  '21.4' not in '${XIQSE_OS_VERSION}'  Confirm User Is Logged Into XIQSE

Accept License Agreement
    [Documentation]     Accepts the license agreement and proceeds to the onboard page

    ${disp_result}=  XIQSE Confirm License Agreement Page Displayed
    Should Be Equal As Integers    ${disp_result}     1

    ${accept_result}=  XIQSE Accept License Agreement and Click Next
    Should Be Equal As Integers    ${accept_result}     1

    # If the Deployment page is displayed, click Next on it (Onboard radio is selected by default)
    ${deploy_page_displayed}=  XIQSE Is License Deployment Page Displayed
    Run Keyword If  '${deploy_page_displayed}' == '1'    XIQSE License Deployment Click Next

    ${page_result}=  XIQSE Confirm Onboard Page Displayed
    Should Be Equal As Integers    ${page_result}     1

Enter XIQ Credentials on Onboard Page
    [Documentation]     Enters XIQ credentials on Onboard page
    [Arguments]         ${xiq_email}  ${xiq_pwd}

    ${onboard_result}=  XIQSE Onboard to XIQ    ${xiq_email}    ${xiq_pwd}
    Should Be Equal As Integers    ${onboard_result}     1
