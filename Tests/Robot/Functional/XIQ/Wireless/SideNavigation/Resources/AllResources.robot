*** Settings ***
Documentation  This file contains all folders containing the resources and variables to execute the tests.

Resource    ../../../../../Libraries/XIQ/lib_login.robot
Resource    ../../../../../Libraries/XIQ/lib_rbac_config.robot

Variables   Environments/Config/waits.yaml
Variables   nav_items.yaml

Variables   Environments/${TOPO}
Variables   Environments/${ENV}
