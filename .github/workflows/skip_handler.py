from argparse import ArgumentParser
from json import load
from os import environ

AUTHORIZED_USERS_FILE = ".github/workflows/authorized_users.json"
CHECK_MAPPING = {
    "testbed": "testbed_check",
    "file": "filename_and_location_check",
    "dir": "directory_check",
    "name": "testcase_name_check",
    "tags": "tags_check",
    "reserved tags": "reserved_tags",
    "func": "functionality_check",
}

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--actor", help="GitHub Username of the current user", type=str, required=True)
    parser.add_argument("--title", help="Title of the pull request", type=str, required=True)
    parser.add_argument("--check",
                        help="CI check that we are currently running from. Needs to match keys authorized_users.json",
                        type=str, required=True)
    parser.add_argument("--extended_auth",
                        help="Allow another set of authorized users to use this skip. Ex. allow tags_check users to skip reserved_tags aswell",
                        default="", type=str)
    parser.add_argument("--envvar",
                        help="Use a non-standard environment variable for sub-check skips",
                        default="SKIP_CHECK", type=str)

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    pr_title = args.title.lower().strip()
    skip_check = "false" # Note: this is how false is represented in bash

    # Basic check to see if we're trying to skip anything at all
    if pr_title.startswith("[skip checks:"):
        # Pair down title from something like this: "[Skip Checks: Dir,  Blah,   Tags] Hey everybody! I made a code change!"
        # to a list of checks we want to skip like this: [ "Dir", "Blah", "Tags" ]
        checks_to_skip = pr_title.split("]", 1)[0].split(":")[1].split(",")

        # Strip spaces and force everything to lowercase
        checks_to_skip = [ x.strip().lower() for x in checks_to_skip ]
        print(f"Requested skips: {checks_to_skip}")

        try:
            with open(AUTHORIZED_USERS_FILE, "r") as f:
                auth_users = load(f)
        except Exception as e:
            raise Exception("The CI script encountered a problem loading authorized_users.json. Please alert the AutoIQ team!") from e

        # map keywords to actual keys in authorized_users
        long_check_name = CHECK_MAPPING.get(args.check)
        long_extended_check_name = CHECK_MAPPING.get(args.extended_auth)

        if args.check in checks_to_skip:
            authorized_users = auth_users['admins'] + auth_users.get(long_check_name, []) + auth_users.get(long_extended_check_name, [])
            print(authorized_users)
            if args.actor in authorized_users:
                print(f"[*] Request to skip {long_check_name} accepted. Skipping...")
                skip_check = "true" # Note: this is how true is represented in bash

            else:
                print(f"[*] Request to skip denied. {args.actor} is not authorized")

        else:
            print(f"[*] No request to skip the {long_check_name}. Note: you may see this error if you mispelled the check keyword")

    else:
        print("[*] No request to skip checks found.")

    # GITHUB_ENV is a file that holds the environment variables for workflows.
    # Append a control environment variable that signals to the workflow when to skip a CI check.
    #
    try:
        with open(environ["GITHUB_ENV"], "a") as f:
            f.write(f"\n{args.envvar}={skip_check}")
    except Exception as e:
        raise Exception("The CI script encountered a problem loading Github environment. Please alert the AutoIQ team!") from e
