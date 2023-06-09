*** Settings ***
Documentation  This file contains all folders containing the resources and variables to execute the tests.

Library     Collections
Library     common/TestFlow.py
Library     xiq/flows/common/DeviceCommon.py

Resource    ../../../../Libraries/XIQ/lib_devices.robot
Resource    ../../../../Libraries/XIQ/lib_device360.robot
Resource    ../../../../Libraries/XIQ/lib_digital_twin.robot
Resource    ../../../../Libraries/XIQ/lib_global_settings.robot
Resource    ../../../../Libraries/XIQ/lib_login.robot
Resource    ../../../../Libraries/XIQ/lib_policy.robot
Resource    ../../../../Libraries/XIQ/lib_voss.robot

Variables   Environments/Config/waits.yaml

Variables   Environments/${TOPO}
Variables   Environments/${ENV}
