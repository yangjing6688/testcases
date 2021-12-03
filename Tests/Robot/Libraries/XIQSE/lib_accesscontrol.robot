#----------------------------------------------------------------------
# Copyright (C) 2021... 2021 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# This file contains keywords specific to the Access Control functionality.
#

*** Settings ***
Library     Collections
Library     OperatingSystem
Library     common/Cli.py
Library     xiqse/flows/control/XIQSE_Control.py
Library     xiqse/flows/control/access_control/XIQSE_AccessControlAddRemove.py
Library     xiqse/flows/control/access_control/XIQSE_AccessControlPanel.py
Library     xiqse/flows/control/access_control/XIQSE_AccessControlTree.py
Library     xiqse/flows/control/dashboard/XIQSE_ControlDashboard.py
Library     xiqse/flows/common/XIQSE_CommonNavigator.py
Library     xiqse/flows/admin/licenses/XIQSE_AdminLicenses.py
Library     xiqse/flows/admin/licenses/XIQSE_AdminLicensesAddLicense.py

*** Variables ***
${SSH_PORT}             22

*** Keywords ***
Update Access Control License File and Restart
    [Documentation]     Updates tag-license file in Access Control and restarts NAC service
    [Arguments]         ${ip}  ${user}  ${password}  ${tag_license}

    ${sshSession}=  Open Paramiko SSH Spawn     ${ip}  ${user}  ${password}  ${SSH_PORT}
    ${output}=  Send Paramiko CMD               ${sshSession}  echo '${tag_license}' > /etc/tag-license
    ${output}=  Send Paramiko CMD               ${sshSession}  tagctl restart

Remove Access Control License File and Restart
    [Documentation]     Updates tag-license file in Access Control and restarts NAC service
    [Arguments]         ${ip}  ${user}  ${password}

    ${sshSession}=  Open Paramiko SSH Spawn     ${ip}  ${user}  ${password}  ${SSH_PORT}
    ${output}=  Send Paramiko CMD               ${sshSession}  rm /etc/tag-license
    ${output}=  Send Paramiko CMD               ${sshSession}  tagctl restart

Get NAC Status In Panel
    [Arguments]    ${expected_value}  ${nacip}
    ${returned_val}=  XIQSE Get NAC Status
    RUN KEYWORD UNLESS  '${expected_value}' in '${returned_val}'  RUN KEYWORDS
    ...  XIQSE Control Select Engines Tree Node  All Engines
    ...  AND  sleep  2 seconds
    ...  AND  XIQSE Control Select Engines Tree Node  ${nacip}/${nacip}

    Should Contain      ${returned_val}     ${expected_value}

Get License Count In Control Dashboard
    [Arguments]    ${label}  ${expected_value}
    sleep  1 seconds
    ${returned_val}=  XIQSE Get License Overview In Control Dashboard  ${label}
    # Update could be delayed. Need to refresh the data if happens.
    RUN KEYWORD UNLESS  ${returned_val} == ${expected_value}  RUN KEYWORDS
    ...  XIQSE Control Select Access Control Tab
    ...  AND  sleep  2 seconds
    ...  AND  XIQSE Control Select Dashboard Tab

    Should Be Equal As Integers     ${returned_val}     ${expected_value}
