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
Library     xiq/flows/common/Login.py
Library     xiq/flows/common/Navigator.py
Library     xiq/flows/globalsettings/Communications.py
Library     common/Screen.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}

*** Test Cases ***
TC-52306 - Communications pages Validation
    [Documentation]  Check user navigate to communication pages without error
    [Tags]             production       sanity          navigation   TC-52306
    ${LOGIN_XIQ}=       Login User      ${tenant_username}     ${tenant_password}
    ${XIQ_VERSION}=     Get XIQ Version
    Log to Console      ${XIQ_VERSION}
    ${COMM_PAGE}=       Validate Communications Page         ${XIQ_VERSION}
    Save Screen shot
    should be equal as strings       '${COMM_PAGE}'     '1'
    ${NOTIFICATION}=    Validate Notifications Page
    Save Screen shot
    should be equal as strings       '${NOTIFICATION}'      '1'
    ${PREVIEW}=         Validate Preview Page
    Save Screen shot
    should be equal as strings       '${PREVIEW}'   '1'
    ${NEW_IN_XIQ}=      Validate New In Extremecloud Page
    Save Screen shot
    should be equal as strings       '${NEW_IN_XIQ}'   '1'

    [Teardown]         run keywords    logout user
     ...                               quit browser

