*** Settings ***
Documentation  This file contains all folders containing the resources and variables to execute the tests.

Resource    ../../../../../Libraries/XIQ/lib_devices.robot
Resource    ../../../../../Libraries/XIQ/lib_login.robot

Variables   Environments/Config/waits.yaml

Variables   TestBeds/${TESTBED}
Variables   Environments/${TOPO}
Variables   Environments/${ENV}