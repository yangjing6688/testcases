import os
import sys
import argparse


class ReportReformatter:

    def __init__(self, input_report_file, reformat_report_file=None, rename=False):
        self.input_report_file = input_report_file
        self.reformat_report_file = reformat_report_file
        self.rename_report_file = rename

    def set_input_report_file(self, filename):
        """
        - set_input_report_file - option to set input report filename
        :param filename: value to set the input report filename to
        - Useage:
        - ``report_reformat_Object.set_input_report_file(filename)``
        """
        self.input_report_file = filename

    def set_reformat_report_file(self, filename):
        """
        -set_reformat_report_file - option to set reformat report filename
        :param filename: value to set the input report filename to
        - Useage:
        - ``report_reformat_Object.set_reformat_report_file(filename)``
        """
        self.reformat_report_file = filename

    def set_rename_report_file(self, value):
        """
        -set_rename_report_file - option to set renaming input and reformat filenames
        :param value: value used to indicate if renaming is enabled or disabled
        - Useage:
        - ``report_reformat_Object.set_rename_report_file(True)``
        """
        self.rename_report_file = value

    def _get_input_report_file(self):
        return self.input_report_file

    def _get_reformat_report_file(self):
        return self.reformat_report_file

    def _get_rename_report_file(self):
        return self.rename_report_file

    def _load_reformat_file(self):
        file_data = []
        file_point: None

        with open(self.input_report_file, "r") as file_point:
            file_data = file_point.readlines()

        if not self.reformat_report_file:
            self.reformat_report_file = self._get_default_reformat_file()

        with open(self.reformat_report_file, "w") as file_point:
            for write_data in file_data:
                html_str = str(write_data)
                if html_str.startswith('*HTML*'):
                    html_str = self._replace_html_values(html_str)
                file_point.write(html_str)

        if self._get_rename_report_file():
            os.rename(self._get_input_report_file(), self._get_report_original_file_name())
            os.rename(self._get_reformat_report_file(), self._get_input_report_file())

    def _replace_html_values(self, html_str):
        html_str = html_str.replace('*HTML*', '')
        html_str = html_str.replace('&lt;', '<')
        html_str = html_str.replace('&quot;', '"')
        html_str = html_str.replace('&gt;', '>')
        return html_str

    def _get_default_reformat_file(self):
        _fle = str(self.input_report_file[:-5])
        _fle = _fle + "_reformat_print.html"
        return _fle

    def _get_report_original_file_name(self):
        _fle = str(self.input_report_file[:-5])
        _fle = _fle + "_original.html"
        return _fle

    def _start_conversion(self):
        print('Starting conversion of test results...')

    def _complete_conversion(self):
        print('Conversion of test results complete...')

    def convert_test_results(self):
        """
        - convert_test_results method used to modify results file so that an image can be embedded and displayed
        - in the file
        - Useage:
        - report_reformatter_Object.convert_test_results()
        """
        self._start_conversion()
        self._load_reformat_file()
        self._complete_conversion()


# Defining main function
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("report", help="Name/path of the source report")
    parser.add_argument("--reformat", help="Name/path of the converted report")
    parser.add_argument("--rename", help="Save source report as new file and rewrite formatted data to source",
                        action="store_true")
    arguments = parser.parse_args()
    report_file = arguments.report
    reformat_file = arguments.reformat
    rename_file = arguments.rename

    report_reformat_formatter = ReportReformatter("", "")
    report_reformat_formatter.set_input_report_file(report_file)
    if reformat_file:
        report_reformat_formatter.set_reformat_report_file(reformat_file)
    if rename_file:
        report_reformat_formatter.set_rename_report_file(True)
    report_reformat_formatter.convert_test_results()

# __name__
if __name__ == "__main__":
    main()
