*** Settings ***
Documentation     Suite Core Setup and Teardown
Resource          Tests/Robot/Functional/XIQ/Wireless/Sanity/AllResources.robot
Suite Setup       Base Production Sanity Test Suite Setup
Suite Teardown    Base Production Sanity Test Suite Cleanup