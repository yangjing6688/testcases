*** Settings ***
Documentation  This file contains all folders containing the resources and variables to execute the tests.

Resource    ../../../../../Libraries/XIQ/lib_devices.robot
Resource    ../../../../../Libraries/XIQ/lib_login.robot
Resource    ../../../../../Libraries/XIQ/lib_voss.robot
Resource    ../../../../../Libraries/XIQ/lib_telegraf.robot
Resource    ../../../../../Libraries/XIQSE/lib_xiq.robot

Variables   TestBeds/${TESTBED}
Variables   Environments/${TOPO}
Variables   Environments/${ENV}

Variables   ./Webhook.yaml
Variables   ./AlertPolicy.yaml
