*** Settings ***
Documentation  This file contains all folders containing the resources and variables to execute the tests.

Resource    Tests/Robot/Libraries/XIQSE/lib_banner.robot
Resource    Tests/Robot/Libraries/XIQSE/lib_login.robot
Resource    Tests/Robot/Libraries/XIQSE/lib_sites.robot
Resource    Tests/Robot/Libraries/XIQSE/lib_devices.robot

Variables   TestBeds/${TESTBED}
Variables   Environments/${TOPO}
Variables   Environments/${ENV}
