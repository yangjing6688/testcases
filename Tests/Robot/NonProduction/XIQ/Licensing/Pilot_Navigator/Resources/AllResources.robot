*** Settings ***
Documentation  This file contains all folders containing the resources and variables to execute the tests.

Resource    ../../../../../Libraries/XIQ/lib_devices.robot
Resource    ../../../../../Libraries/XIQ/lib_digital_twin.robot
Resource    ../../../../../Libraries/XIQ/lib_global_settings.robot
Resource    ../../../../../Libraries/XIQ/lib_login.robot
Resource    ../../../../../Libraries/XIQ/lib_voss.robot
Resource    ../../../../../Libraries/XIQ/lib_license.robot

Library     OperatingSystem
Library     common/Utils.py
Library     DependencyLibrary
Library     xiq/flows/manage/FilterManageDevices.py
Library     ExtremeAutomation/Imports/CommonObjectUtils.py

Variables   Environments/Config/waits.yaml

Variables   TestBeds/${TESTBED}
Variables   Environments/${TOPO}
Variables   Environments/${ENV}
