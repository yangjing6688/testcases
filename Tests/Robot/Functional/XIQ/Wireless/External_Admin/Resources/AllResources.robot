*** Settings ***
Library     Collections
Library     String
Library     extauto/xiq/flows/common/Login.py
Library     extauto/xiq/flows/manage/Devices.py

Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml
