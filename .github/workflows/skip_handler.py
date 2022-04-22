from argparse import ArgumentParser
from json import load
from os import environ

parser = ArgumentParser()
parser.add_argument("--actor", help="GitHub Username of the current user", type=str)
parser.add_argument("--title", help="Title of the pull request", type=str)
parser.add_argument("--check", help="CI check that we are currently running from. Needs to match keys authorized_users.json", type=str)

args = parser.parse_args()

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

pr_title = args.title.lower()

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

    # and map keywords to actual keys in authorized_users
    if args.check in checks_to_skip:
        if args.actor in auth_users['admins'] + auth_users.get(CHECK_MAPPING.get(args.check), []):
            print(f"[*] Request to skip {args.check} accepted. Skipping...")
            print(environ['GITHUB_ENV'])
            environ['GITHUB_ENV'] = environ.get('GITHUB_ENV', '') + "\nSKIP_CHECK=true"
            print(environ['GITHUB_ENV'])
        else:
            print(f"[*] Request to skip denied. {args.actor} is not authorized")
    else:
        print("[*] No request to skip the current check. Note: you may see this error if you mispelled the check keyword")
else:
    print("[*] No request to skip checks found.")

