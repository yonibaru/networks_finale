import unittest
from server import inject_file_data

class TestServer(unittest.TestCase):
    def test_inject_file_data(self):
        filepath = "/path/to/file.txt"
        data = "Lorem ipsum dolor sit amet"
        id = "1234567"
        packet_size = "0123"

        expected_result = "/path/to/file.txt               12345670123Lorem ipsum dolor sit amet"
        result = inject_file_data(filepath, data, id, packet_size)

        self.assertEqual(result, expected_result)

if __name__ == "__main__":
    unittest.main()