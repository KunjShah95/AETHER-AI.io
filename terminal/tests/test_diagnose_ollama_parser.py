import unittest
from terminal.diagnose_ollama import parse_ollama_list_output


class TestParseOllamaListOutput(unittest.TestCase):
    def test_sample_noisy_output(self):
        sample = '''\
NAME                                        SIZE    PARAMS  FAMILY        QUANT     MODIFIED     
--------------------------------------------------------------------------------------------     
unknown                                 12.85 GB         ?  ?             ?         2025-10-16   
19:09:53.346960+05:30
unknown                                    366 B         ?  ?             ?         2025-10-16   
14:28:25.874936+05:30
20:27:45.920519+05:30
unknown                                  7.59 GB         ?  ?             ?         2025-10-15   
20:21:02.524803+05:30
unknown                                  4.87 GB         ?  ?             ?         2025-10-15   
20:15:44.235613+05:30
unknown                                    384 B         ?  ?             ?         2025-10-15   
19:56:31.827662+05:30
unknown                                    384 B         ?  ?             ?         2025-10-15   
19:48:02.064570+05:30
'''

        parsed = parse_ollama_list_output(sample)
        # Expect rows for each 'unknown' line (6 rows in sample)
        self.assertGreaterEqual(len(parsed), 6)
        for row in parsed:
            self.assertIn('NAME', row)
            self.assertIn('SIZE', row)

    def test_header_not_found(self):
        parsed = parse_ollama_list_output('no header here\njust text')
        self.assertEqual(parsed, [])


if __name__ == '__main__':
    unittest.main()
