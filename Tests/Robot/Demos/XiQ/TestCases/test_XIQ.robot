
# Author        : John Subler
# Date          : Dec 17th 2021
# Description   : Example Test Case
#
# Topology      :
# Host ----- Cloud

*** Variables ***

*** Settings ***
Library     common/Cli.py
# The keywords in Login.py have been moved to the keywords directory.
# If the moved keyword is not working correctly import the original library and remove the keywords/gui/login/KeywordsLogin.py version.
#Library     xiq/flows/common/Login.py
Library     keywords/gui/login/KeywordsLogin.py
Library     xiq/flows/manage/Devices.py

Variables    Environments/${TOPO}
Variables    Environments/${ENV}



*** Test Cases ***
test_XIQ: Basic Login Test Case
    [Documentation]         Login
    ...                     robot -v ENV:environment.local.chrome.yaml -v TOPO:topo.test.g2r1.yaml  test_XIQ.robot
    [Tags]                  demos
    ${result}=              Login User          ${tenant_username}      ${tenant_password}

    [Teardown]   run keywords        Logout User
    ...          AND                 quit browser





