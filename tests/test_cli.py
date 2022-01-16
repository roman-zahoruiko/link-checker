import unittest
import subprocess
import os
from pathlib import Path


class TestLinkCheckerCli(unittest.TestCase):
    path = Path(__file__).resolve().parent.parent

    def test_run_cli(self):
        exit_status = os.system(f'python {self.path}/link-checker-cli.py -h')
        self.assertEqual(exit_status, 0)

    def test_cases_cli(self):
        cases = [
            ('google.com', [(False, 'the website redirects to http://www.google.com/ location'),
                            (False, 'the website rejects robots'),
                            (True, 'the website is not parked')]),
            ('//konstankino.com', [(True, 'the website redirects to https'),
                                   (True, 'the website accepts robots'),
                                   (True, 'the website is not parked')]),
            ('http://conversationgrabber.com', [(True, 'the website valid as is'),
                                                (False, 'the website rejects robots'),
                                                (False, 'the website is parked')]),
        ]
        for url, correct_response in cases:
            cli_response = subprocess.check_output(
                f'python {self.path}/link-checker-cli.py -url {url}', universal_newlines=True, shell=True
            )
            self.assertEqual(cli_response.replace('\n', ''), str(correct_response).replace('\n', ''))

    def test_cases_cli_with_log(self):
        url = 'brokendomain342342341frgr.com'
        log_data = '...log: No data retrieved because <urlopen error [Errno -2] Name or service not known'
        cli_response = subprocess.check_output(
            f'python {self.path}/link-checker-cli.py -url {url} -log', universal_newlines=True, shell=True
        )
        self.assertIn(log_data, str(cli_response.replace('\n', '')))
