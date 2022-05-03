*** Settings ***
Documentation  This file contains all folders containing the resources and variables to execute the tests.

Resource    ../../../../Libraries/XIQSE/lib_common.robot
Resource    ../../../../Libraries/XIQSE/lib_login.robot
Resource    ../../../../Libraries/XIQSE/lib_server.robot
Resource    ../../../../Libraries/XIQSE/lib_upgrades.robot

Variables   TestBeds/${TESTBED}
Variables   Environments/${TOPO}
Variables   Environments/${ENV}
