*** Settings ***
Documentation  This file contains all folders containing the resources and variables to execute the tests.

Resource    ../../../../Libraries/XIQSE/lib_analytics.robot
Resource    ../../../../Libraries/XIQSE/lib_archives.robot
Resource    ../../../../Libraries/XIQSE/lib_banner.robot
Resource    ../../../../Libraries/XIQSE/lib_cli_creds.robot
Resource    ../../../../Libraries/XIQSE/lib_common.robot
Resource    ../../../../Libraries/XIQSE/lib_devices.robot
Resource    ../../../../Libraries/XIQSE/lib_diagnostics.robot
Resource    ../../../../Libraries/XIQSE/lib_discovery.robot
Resource    ../../../../Libraries/XIQSE/lib_events.robot
Resource    ../../../../Libraries/XIQSE/lib_firmware.robot
Resource    ../../../../Libraries/XIQSE/lib_license.robot
Resource    ../../../../Libraries/XIQSE/lib_login.robot
Resource    ../../../../Libraries/XIQSE/lib_operations.robot
Resource    ../../../../Libraries/XIQSE/lib_options.robot
Resource    ../../../../Libraries/XIQSE/lib_profiles.robot
Resource    ../../../../Libraries/XIQSE/lib_sites.robot
Resource    ../../../../Libraries/XIQSE/lib_syslog.robot
Resource    ../../../../Libraries/XIQSE/lib_traps.robot
Resource    ../../../../Libraries/XIQSE/lib_xiq.robot

Variables   TestBeds/${TESTBED}
Variables   Environments/${TOPO}
Variables   Environments/${ENV}
