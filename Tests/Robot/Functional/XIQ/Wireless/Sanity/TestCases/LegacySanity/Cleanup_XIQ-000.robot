# Author        : Rmeswar
#                 modified by pdo
# Date          : July 2020
# Description   : Remove all APs, Network Policies & Common Objects

# Execution Command:
# robot -L DEBUG -i ALL -v TOPO:g7r2 cleanup.robot

*** Variables ***

*** Settings ***
Library      xiq/flows/common/Login.py
Library      common/TestFlow.py
Library      xiq/flows/common/Navigator.py
Library      xiq/flows/manage/Devices.py
Library      xiq/flows/configure/UserGroups.py
Library      xiq/flows/configure/CommonObjects.py
Library      xiq/flows/configure/NetworkPolicy.py
Library      xiq/flows/configure/AutoProvisioning.py
Library      common/Cli.py
Library      common/CommonValidation.py

Variables    Environments/Config/device_commands.yaml
Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}


Suite Setup        run keyword        pre condition
Suite Teardown     run keyword        quit browser

Force Tags   testbed_1_node

*** Keywords ***
pre condition
    [Documentation]   Waits until the devices finish updating

    ${STATUS}=      Login User        ${TENANT_USERNAME}     ${TENANT_PASSWORD}
    Should Be Equal As Integers       ${STATUS}     1        Unable to login

    ${STATUS}     navigate to devices
    Should Be Equal As Integers       ${STATUS}     1        Unable to navigate to devices page

    wait until all devices update done              15

*** Test Cases ***
tccs-7436_step1: Remove all Devices
    [Documentation]    Remove all devices

    [Tags]             production       tccs_7436_step1     tccs_7436

    ${STATUS}    delete all devices
    Should Be Equal As Integers       ${STATUS}     1        Unable to delete all the all devices


tccs-7436_step2: Remove all Auto-Provision-Policies
    [Documentation]    Remove all auto provision Policies
    [Tags]             production      tccs-7436_step2      tccs_7436

    ${STATUS}          Navigate To Network Policies List View Page
    Should Be Equal As Integers       ${STATUS}     1        Unable to navigate to network policies list view page


    ${STATUS}=      Delete All Auto Provision Policies
    Should Be Equal As Integers       ${STATUS}     1        Unable to remove all auto provision policies


tccs-7436_step3: Remove all network policies
    [Documentation]    Remove all network policies
    [Tags]             production       tccs-7436_step3     tccs_7436

    ${STATUS}=         Delete All Network Policies
    Should Be Equal As Integers       ${STATUS}     1        Unable to remove all network policies


tccs-7436_step4: Remove all SSIDs
    [Documentation]    Remove all SSIDs
    [Tags]             production       tccs-7436_step4     tccs_7436

    ${STATUS}=         Delete All SSIDs
    Should Be Equal As Integers       ${STATUS}     1        Unable to remove all SSIDs


tccs-7436_step5: Remove all user groups
    [Documentation]    Remove all user groups
    [Tags]             production       tccs-7436_step5     tccs_7436

    delete all user groups 
