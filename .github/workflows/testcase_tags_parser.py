# Built-ins
from argparse import ArgumentParser
from sys import exit
from json import load as jsonload
from re import sub

# 3rd party
from requests import exceptions as req_excepts, get as http_get, post as http_post

##########################
# Helper functions
##########################
def parse_args():
    parser = ArgumentParser()
    # General Args
    parser.add_argument("file", help="File that contains the results of the tag/marker checks", type=str)
    parser.add_argument("--mode", help="Script operating mode.", choices=['validate_tags', 'update_qtest', 'update_testcase_data'])
    parser.add_argument("--framework", help="The type of test cases we are parsing.", choices=['pytest', 'robot'] )
    parser.add_argument("--auth_token", help="AutoIQ auth token for calling endpoints", required=True, type=str)
    parser.add_argument('--warn', help="Don't return a bad return code. Only print problems.", action='store_true')

    # Only applicable to update_testcase_data
    parser.add_argument('--testcase_author', help="Author of the testcases", type=str)

    # Only applicable to validate_tags mode
    parser.add_argument('--skip_reserved_tags', help="Don't fail testcases for containing reserved tags/markers", choices=['true', 'false'])
    return parser.parse_args()

def readFile(file):
    try:
        with open(file, "r") as f:
            return jsonload(f)
    except Exception as e:
        raise Exception(f'The CI script encountered a problem opening {f}.') from e

def qtestTagCleanup(tag):
    """
    Hypens and underscores are valid in testcases, but only hypen is valid in qtest
    _step[x] or -step[x] suffixes will potentially be valid in testcases in the future
    This function replaces underscores with hypens if needed and removes 'step' suffix for passing to qtest
    """
    tag = sub('_', '-', tag)
    tag = sub(r'-step[0-9]+', '', tag, count=1)
    return tag

##########################
# Mode Functions
##########################
def validate_tags():
    rc=0
    for file, file_info in results.items():
        print(f'{LINE_BREAK}\nResults for file: {file}')

        for testcase, testcase_info in file_info.items():
            print(f'Results for testcase: {testcase}')
            testcase_passed = True

            if not testcase_info['all_tags_lower_case']:
                print(f"{PRINT_PREFIX} One or more {TAG_OR_MARKER}s contain uppercase characters")
                testcase_passed = False

            if testcase_info['contains_reserved_tag'] and not SKIP_RESERVED_TAGS:
                print(f"{PRINT_PREFIX} One or more reserved {TAG_OR_MARKER}s were found. Reserved {TAG_OR_MARKER}s: [production, regression, nightly, sanity, p1, p2, p3, p4, p5]")
                testcase_passed = False

            if not testcase_info['contains_development'] and not SKIP_RESERVED_TAGS:
                print(f"{PRINT_PREFIX} 'development' marker not found")
                testcase_passed = False

            if not testcase_info['contains_testbed_tag']:
                print(f"{PRINT_PREFIX} Testbed type {TAG_OR_MARKER} not found")
                testcase_passed = False

            if testcase_info['valid_qtest_tag']:
                qtest_tags = list(map(qtestTagCleanup, testcase_info['qtest_tags']))

                # Validate each qtest tag with qtest
                for tag in qtest_tags:
                    url = f"{AUTOIQ_BASE_URL}/qtest-client/testcases/testcaseid/{tag}"

                    try:
                        r = http_get(url, headers=HEADERS)
                    except req_excepts.RequestException as e:
                        raise Exception(f'Encountered a problem calling url: {url}') from e

                    try:
                        json_response = r.json()
                        if json_response['result']['status'] != 'pass':
                            print(f"{PRINT_PREFIX} qTest {TAG_OR_MARKER} [{tag}] does not exist in qTest")
                            testcase_passed = False
                    except Exception as e:
                        # endpoint returned non-json response or didn't contain status key in dict
                        # Since this is unhandled it exits with a 1 code
                        raise Exception(f'Bad response from endpoint: {r.text}') from e

                print(qtest_tags)
            else:
                print(f"{PRINT_PREFIX} qTest {TAG_OR_MARKER} not found. It is either malformed or non-existant.")
                rc=1
                testcase_passed = False

            if testcase_passed:
                print(f"[*] PASS: {file} passed!")
            else:
                rc=1

            print() # Add blank line between testcases
        print() # Add blank line between files
    return rc

def update_qtest():
    rc=0
    for file, file_info in results.items():
        print(f'{LINE_BREAK}\nProcessing tags from file: {file}')
        for testcase, testcase_info in file_info.items():
            print(f'Processing testcase: {testcase}')
            # This check is still needed here incase someone skips CI
            if testcase_info['valid_qtest_tag']:
                qtest_tags = list(map(qtestTagCleanup, testcase_info['qtest_tags']))

                # Set automated status of each tag in qTest
                for tag in qtest_tags:
                    url = f"{AUTOIQ_BASE_URL}/qtest-client/testcases/automated"

                    payload = {
                        "tcid": tag,
                        "repo": "https://github.com/extremenetworks/extreme_automation_tests",
                        "path": file,
                        "branch": ["main"]
                    }
                    try:
                        r = http_post(url, headers=HEADERS, json=payload)
                    except req_excepts.RequestException as e:
                        raise Exception(f'Encountered a problem calling url: {url}') from e

                    try:
                        json_response = r.json()
                        if json_response['result'].get('status') == 'pass':
                            print(f"{SUCCESS_PREFIX} Test Case [{tag}] marked automated in qTest ")
                        elif json_response['result'].get('status') == 'already automated':
                            print(f"{SUCCESS_PREFIX} Test Case [{tag}] is already marked automated in qTest")
                        elif json_response['result'].get('status') == 'fail':
                            print(f"{PRINT_PREFIX} Test Case [{tag}] does not exist in qTest")
                        else:
                            print(f"{PRINT_PREFIX} {json_response}")
                            rc=1
                    except Exception as e:
                        # endpoint returned non-json response or didn't contain status key in dict
                        # Since this is unhandled it exits with a 1 code
                        raise Exception(f'Bad response from endpoint: {r.text}') from e

                print() # Add blank line between testcases
        print() # Add blank line between files

    return rc

def update_testcase_data():
    rc=0
    for file, file_info in results.items():
        print(f'{LINE_BREAK}\nProcessing testcases from file: {file}')
        for testcase, testcase_info in file_info.items():
            print(f'Processing testcase: {testcase}')

            # Attempt to add testcase to AutoIQ testcase DB
            url = f"{AUTOIQ_BASE_URL}/stats/testCaseMetadata/testCases"

            payload={
                "filePath": file,
                "testCaseName": testcase,
                "qTestId":  testcase_info.get('valid_qtest_tag', ''),
                "author": args.testcase_author,
                "authorsManager": "", # TODO: To be implemented in the future
                "pod": "" # TODO: To be implemented in the future
            }

            try:
                r = http_post(url, headers=HEADERS, json=payload)
            except req_excepts.RequestException as e:
                raise Exception(f'Encountered a problem calling url: {url}') from e

            try:
                json_response = r.json()
                if json_response['result'].get('status') == 'success':
                    print(f"{SUCCESS_PREFIX} Test Case [{testcase}] added to the AutoIQ Database")
                elif 'Duplicate' in json_response['errors'][0]:
                    print(f"{SUCCESS_PREFIX} Test Case [{testcase}] is already in the AutoIQ Database")
                else:
                    print(f"{PRINT_PREFIX} {json_response}")
                    rc=1
            except Exception as e:
                # endpoint returned non-json response or didn't contain status key in dict
                # Since this is unhandled it exits with a 1 code
                raise Exception(f'Bad response from endpoint: {r.text}') from e

            print() # Add blank line between testcases
        print() # Add blank line between files

    return rc


##########################
# Main
##########################
if __name__ == '__main__':
    args = parse_args()

    results = readFile(args.file)
    # print(results)

    if args.framework == 'pytest':
        TAG_OR_MARKER = 'marker'
    else:
        TAG_OR_MARKER = 'tag'
    WARN_PREFIX     = "[*] WARNING:"
    FAIL_PREFIX     = "[*] FAIL:"
    SUCCESS_PREFIX  = "[*] SUCCESS:"
    LINE_BREAK      = "=" * 80
    AUTOIQ_BASE_URL = 'https://autoiq.extremenetworks.com'
    # AUTOIQ_BASE_URL = 'https://autoiq-test.extremenetworks.com' # for testing

    PRINT_PREFIX = WARN_PREFIX if args.warn else FAIL_PREFIX

    HEADERS = {
        'Content-Type': 'application/json',
        'authorization': f'PAT {args.auth_token}'
    }

    if args.mode == 'validate_tags':
        SKIP_RESERVED_TAGS = True if args.skip_reserved_tags == 'true' else False

        rc = validate_tags()

    elif args.mode == 'update_qtest':
        rc = update_qtest()

    elif args.mode == 'update_testcase_data':
        if not args.testcase_author:
            raise ValueError("Error: Testcase Author required when using update_testcase_data mode")
        rc = update_testcase_data()



    if args.warn:
        rc=0
    exit(rc)
