# Author        : Peter Sadej
# Date          : March 1st 2023
# Description   : No Operation Test
## Topology      : N/A
# Notes:
#  - This test is used to test the test framework and/or AutoIQ
#  - It does not perform any real operations

*** Variables ***

*** Settings ***
Library     common/TestFlow.py

*** Test Cases ***
Test 1: This test must pass
    ${string1}  Set Variable  'Hello'
    ${string2}  Set Variable  'Hello'
    Should be equal as strings  ${string1}  ${string2}
