from ExtremeAutomation.Utilities.Framework.test_case_inventory import RobotTestData
from robot.api.parsing import get_model
import argparse
import json
import os
import glob

parser = argparse.ArgumentParser(description='Get info for Robot files.')
parser.add_argument('files',
                    type=str,
                    nargs='+',
                    help='a file to process')
args = parser.parse_args()

def main(path):
    model = get_model(path)
    printer = RobotTestData(model)
    printer.visit(model)
    output = printer.print_suite()
    print(f"qTest Tag Count: {len(printer.qTestTags)}\nqTest Tags: {printer.qTestTags}")

    return output

if __name__ == '__main__':
    # main(sys.argv[1])
    output_dict = {}
    for file in args.files:
        if os.path.isdir(file):
            robo_file_match = os.path.join(file, '*.robot')
            robo_files = glob.glob(robo_file_match)
            for robo_file in robo_files:
                print(f"robo file = {robo_file}")
                result = main(robo_file)
                # merge the result dict into the output dict
                output_dict = {**output_dict, **result}
        else:
            result = main(file)
            # merge the result dict into the output dict
            output_dict = {**output_dict, **result}

    # Output CICD info
    #print(json.dumps(output_dict))
    with open(f'{os.getcwd()}/robot_data.json', 'w') as outfile:
        json.dump(output_dict, outfile)