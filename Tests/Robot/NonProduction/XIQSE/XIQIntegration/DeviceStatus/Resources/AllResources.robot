*** Settings ***
Documentation  This file contains all folders containing the resources and variables to execute the tests.

Resource    ../../../../../Libraries/XIQSE/lib_banner.robot
Resource    ../../../../../Libraries/XIQSE/lib_common.robot
Resource    ../../../../../Libraries/XIQSE/lib_devices.robot
Resource    ../../../../../Libraries/XIQSE/lib_diagnostics.robot
Resource    ../../../../../Libraries/XIQSE/lib_login.robot
Resource    ../../../../../Libraries/XIQSE/lib_options.robot
Resource    ../../../../../Libraries/XIQSE/lib_profiles.robot
Resource    ../../../../../Libraries/XIQSE/lib_server.robot
Resource    ../../../../../Libraries/XIQSE/lib_snmp_creds.robot
Resource    ../../../../../Libraries/XIQSE/lib_xiq.robot

Variables   TestBeds/${TESTBED}
Variables   Environments/${TOPO}
Variables   Environments/${ENV}
