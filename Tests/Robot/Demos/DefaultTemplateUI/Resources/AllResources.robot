*** Settings ***
Documentation  This file contains all folders containing the resources and variables to execute the tests.
Resource    ExtremeAutomation/Resources/Libraries/DefaultLibraries.robot
Resource    SuiteUdks.robot
Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
