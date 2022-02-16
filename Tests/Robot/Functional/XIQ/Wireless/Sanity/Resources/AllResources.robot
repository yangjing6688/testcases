*** Settings ***
Documentation  This file contains all folders containing the resources and variables to execute the tests.

Library     extauto/common/ConfigFileHelper.py

Variables   TestBeds/${TESTBED}
Variables   Environments/${TOPO}
Variables   Environments/${ENV}

*** Keywords ***
#----------------------------------------------------------------------------------------------------------
#   Absolute Start and End Setup/Teardown Keywords
#----------------------------------------------------------------------------------------------------------
Base Production Sanity Test Suite Setup
    log to console   Initial Production Sanity Setup
    REFRESH CONFIG

Base Production Sanity Test Suite Cleanup
    log to console   Final Production Sanity Cleanup
