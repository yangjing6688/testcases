# Digital Twin Unit Testing

Digital Twin Unit Tests are designed for low-level and early testing of DT features that may not be easily testable in a normal QA environment and with normal QA tests.  For instance, when adding a new feature, new Unit Tests can be added by the developer and used to verify new functionality before the code is ever submitted and QA writes tests.  As such, there may be some overlap with normal QA testing, but there is likely (and should be) an abundance of low-level testing that QA may not perform.

DT tests are unique in that there is a small number of fixed tests, but there is a large, varying number of environments in which to run the tests.  A number of fixtures and DT-specific command-line options used to determine which environments to run the tests.  Use the "--help" options to see the option help:

```
# From the "Tests/Pytest/NonProduction/DigitalTwin" directory:
pytest --help TestCases
```

---

## Options Summary
#### Comma-separated list of configurations to test.  Each definition represents a set of DT Config YAML files to use to create a DT environment to run the tests specified through the normal pytest options (eg. "-k").  Note this only affects the "test_10_generic" tests.
```
--configs=CONFIGS

 CONFIGS:
   all         - Run all the different test configurations
   standard    - Run the standard, pre-created YAML configs (default)
   <yaml_file> - Specify a single yaml file from the dtyaml directory
   <sys_type>  - Specify a single sys_type
   sys_sample  - Create a simple YAML file for one of each system type
   sys_5320    - Create a simple YAML file for each sys_5320 system type
   sys_5420    - Create a simple YAML fileach sys_5420 system type
   sys_5520    - Create a simple YAML fileach sys_5520 system type
   sys_5720    - Create a simple YAML fileach sys_5720 system type
   sys_7520    - Create a simple YAML fileach sys_7520 system type
   sys_7720    - Create a simple YAML fileach sys_7720 system type
   vim_5520    - Create a simple YAML fileach vim_5520 VIM type
   vim_5720    - Create a simple YAML file for each vim_5720 VIM type
```

#### Downloadable DTEC GNS3 Docker container.  The docker environment for the user running pytest must be configued to pull the docker image specified (eg. if it's from Extreme's artifactory, "insecure-registries" must be setup)
```
  --docker-image=DOCKER_IMAGE
```

#### Define the HTTP server IP address to access DT YAML files.  By default, the code will try to determine the correct local IP address reachable through the docker container; however, a specific IP address can be specified using this option.
```
 --http-ip=HTTP_IP
```

#### Define the HTTP server port to access DT YAML files.  By default, port 8181 is used; however a different port can be specified using this option.
```
  --http-port=HTTP_PORT
```

#### Limit the number of DT instances per test.  After determining which environments should be used (using the "--configs" option), a maximum number of instances, chosen at random, can be configured with this option.  This is mostly useful for testing.  A value of 0 can be used to exit after selection and not run any tests.   Note this only affects the "test_10_generic" tests.
```
  --max-instances=MAX_INSTANCES
```

#### Don't use DT Mgmt Interface.  By default, all test environments are setup to use the DT Mgmt interface/network; however, for complete feature coverage, environments need to be setup both with and without DT Mgmt.
```
  --no-dt-mgmt
```

#### Full path of NOS QCOW2 image file (mandatory).  All DTs will be setup using this image.
```
  --nos-image=NOS_IMAGE
```

#### Include or exclude configurations that use stacking.  Since stacking can take twice as long to setup as a single node, it may be useful to test stacking separately or to test stacking only.  This is mostly useful when testing or creating new tests.  Note this only affects the "test_10_generic" tests.
 ```
 --stacking=STACKING

  STACKING
    include     - Include stacking configurations (default)
    exclude     - Exclude any stacking configurations
    only        - Only include stacking tconfigurations
```
----
## Test Categories
### Generic ("test_10_generic")
These tests are designed to run against the environments as specified by the options mentioned above (--configs, --max-instances, ...).  Some of these tests use hard-coded DT Config YAML files from the repo (Resources/dtyaml/cfg_xxx.yaml) and auto-generated DT Config files.
### Negative ("test_20_negative")
These tests are specifically designed to test a mis-configuration or invalid setting.  The environment(s) for each test is hard-coded in the repo (Resources/dtyaml/neg_xxx.yaml) and specified as a fixture parametrization where the test is defined.

----
## Example test run commands
##### Tests should be run from the "Tests/Pytest/NonProduction/DigitalTwin" directory

<br>

Run only the generic tests on the standard (hard-coded) environments, excluding any stacking environments
```
pytest --tc-file=Resources/gns3.yaml \
       --nos-image=~/xos/vm-32.1.0.336.x86_64.qcow2 \
       --stacking=exclude \
       TestCases/test_10_generic_XIQ_793.py
```
Run all tests on the 5520 auto-generated environments, including with and without VIMs, using a specific docker image
```
pytest --tc-file=Resources/gns3.yaml \
       --nos-image=~/xos/vm-32.1.0.336.x86_64.qcow2 \
       --docker-image=engartifacts1.extremenetworks.com:8099/dtec/dtec:22.4.19.A \
       --configs=sys_5520,vim_5520 \
       TestCases
```
Run all tests on a full suite of all possible environments
```
pytest --tc-file=Resources/gns3.yaml \
       --nos-image=~/xos/vm-32.1.0.336.x86_64.qcow2 \
       --configs=all \
       TestCases
pytest --tc-file=Resources/gns3.yaml \
       --nos-image=~/xos/vm-32.1.0.336.x86_64.qcow2 \
       --configs=all \
       --no-dt-mgmt \
       TestCases
```