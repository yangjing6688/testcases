# When written
# 05/25/21 - Added Test Cases 1,2,3 and 4,5,6,7
#
# When modified
# 06/28/21 - Added Test case 8 & 9 By Rachana
#
# What are preconditions
# Ex: Need to have A3 installed and AP onboarded & configured & windows 10 client
#
# What Instance required ?
# Production/Test Env/AIO - Test Env
#
# Topology diagram
# A3
#
# How to run - syntax
# robot -v TEST_URL:https://10.234.188.223:1443 -v TENANT_USERNAME:demo@demo.com -v TENANT_PASSWORD:Extr_123 /
# -v BROWSER:chrome -v TOPO:a3details -i test9  a3_sanity.robot
#
# Common failures
# None
#
# Any specific command combinations
# No


*** Variables ***
${TEST_URL}
${TENANT_USERNAME}
${TENANT_PASSWORD}
${WRONG_PASSWORD}       test123
${TITLE}                ExtremeCloud
${search_string}
${WEB_DRIVER_LOC}       remote


*** Settings ***
Library     extauto/common/Utils.py
Library     extauto/common/Cli.py
Library     extauto/a3/flows/common/Login.py
Library     extauto/xiq/flows/manage/Client.py
Library     extauto/a3/flows/common/Navigator.py
Library     extauto/a3/flows/a3/A3WebElementsflow.py
Library     extauto/a3/flows/a3/RolesWebElementsFlow.py
Library     extauto/a3/flows/a3/RealmsWebElementsFlow.py
Library     extauto/a3/flows/a3/ActiveDirectoryWebElementsFlow.py
Library     extauto/a3/flows/a3/AuthSourcesWebElementsFlow.py
Library     extauto/xiq/elements/MuCPWebElements.py
Library     extauto/common/tools/remote/WinMuConnect.py
Library     extauto/xiq/flows/common/MuCaptivePortal.py
Library     extauto/common/Mu.py

Resource    Tests/Robot/NonProduction/a3/Resources/envirnoment.robot
Resource    Tests/Robot/NonProduction/a3/Resources/a3details.robot


#Library	 Remote 	http://${MU1_IP}:${MU1_REMOTE_PORT}   WITH NAME   MU1


*** Test Cases ***
Test1: Verify Login and Logout
    [Documentation]     Check the login and logout functionality
    [Tags]      test1      login
    ${result1}=      Login a3 User      ${TENANT_USERNAME}     ${TENANT_PASSWORD}
    Should Be Equal As Strings      '${result1}'     '1'
    logout a3 user
    Quit Browser

Test2: A3 configuration
    [Documentation]     Setting up A3 configuration
    [Tags]      test2      configuration
    ${result1}=      Login a3 User      ${TENANT_USERNAME}     ${TENANT_PASSWORD}
    Should Be Equal As Strings      '${result1}'     '1'
    navigate to configuration tab
    switch policies access control
    create roles
    create active directory domains
    join domain
    create realm
    create auth source
    add device
    create new conn profile
    logout a3 user
    Quit Browser

Test3: Cloud Integration - A3 linking & unlinking to XIQ account
    [Documentation]     A3 linking & unlinking to XIQ account
    [Tags]      test3      cloud
    ${result1}=      Login a3 User      ${TENANT_USERNAME}     ${TENANT_PASSWORD}
    Should Be Equal As Strings      '${result1}'     '1'
    navigate to configuration tab
    switch system configuration
    select cloud integration
    logout a3 user
    Quit Browser

Test4: System Backup - creation and validation
    [Documentation]     To create system backup & validate backup is created successfully
    [Tags]      test4      backup
    ${result1}=      Login a3 User      ${TENANT_USERNAME}     ${TENANT_PASSWORD}
    Should Be Equal As Strings      '${result1}'     '1'
    navigate to configuration tab
    switch system configuration
    backup file
    validate backup created  bkup2
    logout a3 user
    Quit Browser

Test5: Tools - Download Tech Data
    [Documentation]     To Download the tech data in Normal & Lite mode
    [Tags]      test5      techdata
    ${result1}=      Login a3 User      ${TENANT_USERNAME}     ${TENANT_PASSWORD}
    Should Be Equal As Strings      '${result1}'     '1'
    navigate to tools tab
    select tech data
    logout a3 user
    Quit Browser

Test6: Tools - Logs
    [Documentation]     To load the logs page and view the selected log
    [Tags]      test6      logs
    ${result1}=      Login a3 User      ${TENANT_USERNAME}     ${TENANT_PASSWORD}
    Should Be Equal As Strings      '${result1}'     '1'
    navigate to tools tab
    select logs  a3-ama.log
    logout a3 user
    Quit Browser

Test7: Tools - SSH enable
    [Documentation]     To load the logs page and view the selected log
    [Tags]      test7      ssh
    ${result1}=      Login a3 User      ${TENANT_USERNAME}     ${TENANT_PASSWORD}
    Should Be Equal As Strings      '${result1}'     '1'
    navigate to tools tab
    select ssh
    ssh page entries
    logout a3 user
    Quit Browser

Test8: Authentication - 802.1X Authentication with A3
    [Documentation]     To authenticate windows client with 802.1X auth
    [Tags]      test8     802.1xauth

    MU1.Connect Enterprise Network     ${SSID_EMP}
    ${result1}=      Login a3 User      ${TENANT_USERNAME}     ${TENANT_PASSWORD}
    Should Be Equal As Strings      '${result1}'     '1'
    navigate to auditing tab
    select radius audit logs  54:8d:5a:69:3c:55  Accept  a3225\a3test1
    navigate to a3 clients tab
    select clients search  54:8d:5a:69:3c:55  on  a3225\a3test1
    logout a3 user
    Quit Browser

Test9: Authentication - Guest Authentication with A3
    [Documentation]     To authenticate windows client with Guest user
    [Tags]      test9      guestuser
    #${FLAG}=   MU1.Connectivity Check
    #Should Be Equal As Strings   '${FLAG}'   '1'

    MU1.Connect Open Network     ${SSID_GUEST}
    #${CURRENT_DATE_TIME}=         Get Current Date Time
    #Log to Console      Sleep for ${CLIENT_CONNECT_WAIT}
    #sleep                         ${CLIENT_CONNECT_WAIT}
    #${CLIENT_STATUS}=             Get Client Status   client_mac=${MU1_WIFI_MAC}
    #Should Be Equal As Strings    '${CLIENT_STATUS}'      '1'
    ${result1}=      Login a3 User      ${TENANT_USERNAME}     ${TENANT_PASSWORD}
    Should Be Equal As Strings      '${result1}'     '1'
    navigate to auditing tab
    select radius audit logs  54:8d:5a:69:3c:55  Accept  548d5a693c55
    navigate to a3 clients tab
    select clients search  54:8d:5a:69:3c:55  on  default
    logout a3 user
    Quit Browser

Test10: Tools - Connection Profile Test
    [Documentation]     To return current profile in use
    [Tags]      test10      profiletest
    ${result1}=      Login a3 User      ${TENANT_USERNAME}     ${TENANT_PASSWORD}
    Should Be Equal As Strings      '${result1}'     '1'
    navigate to tools tab
    connection profile test  54:8d:5a:69:3c:55
    logout a3 user
    Quit Browser




