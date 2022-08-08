*** Settings ***
Library     Collections

Force Tags   testbed_1_node

*** Test Cases ***
noop_Step1: noop
    [Documentation]         This is a no operation

    [Tags]                  development

    log to console  noop test
