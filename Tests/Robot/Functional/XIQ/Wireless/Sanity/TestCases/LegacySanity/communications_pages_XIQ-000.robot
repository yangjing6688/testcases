# Author        : Gayathri
# Date          : January 5th 2021
# Description   : Test suite validates sucsessful navigation to all Communication pages under user profile.
#                 For QA test env we need to add needed files and check for communication pages.
#                 If the issue is seen in staging or production, cloud ops have missed to add, hence need to raise a bug.
#                 aws s3 cp . s3://cloud-communication-qa/communications/21.1.20.6/ --recursive
#                 aws s3 cp . s3://cloud-communication-qa/communications/global/ --recursive
# Topology      :
# Host ----- Cloud


*** Variables ***

*** Settings ***
Library     common/Utils.py
# The keywords in Login.py have been moved to the keywords directory.
# If the moved keyword is not working correctly import the original library and remove the keywords/gui/login/KeywordsLogin.py version.
#Library     xiq/flows/common/Login.py
Library     keywords/gui/login/KeywordsLogin.py
Library     xiq/flows/common/Navigator.py
Library     xiq/flows/globalsettings/Communications.py
Library     common/Screen.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}

Force Tags   testbed_none

*** Test Cases ***
TCCS-7294: Communications pages Validation
    [Documentation]  Check user navigate to communication pages without error

    [Tags]             production       tccs_7294
    ${LOGIN_XIQ}=       Login User      ${tenant_username}     ${tenant_password}

    ${COMM_PAGE}=       Validate Communications Page
    Save Screen shot
    should be equal as strings       '${COMM_PAGE}'     '1'

    [Teardown]         run keywords    logout user
     ...                               quit browser

