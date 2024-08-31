import unittest
from unittest.mock import patch, MagicMock
from client import process_packet

class TestClient(unittest.TestCase):

    @patch('client.socket.socket')
    def test_process_packet(self, mock_socket):
        mock_socket_instance = MagicMock()
        mock_socket.return_value = mock_socket_instance

        # Mock the recv method to simulate receiving data
        mock_socket_instance.recv.side_effect = [
            b'file1.txt' + b' ' * (32 - len('file1.txt')) + b'00000010004',  # Header
            b'data'  # Data
        ]

        files_dict = {}
        result = process_packet(mock_socket_instance, files_dict)

        self.assertTrue(result)
        self.assertIn('file1.txt', files_dict)
        self.assertIn(1, files_dict['file1.txt'])
        self.assertEqual(files_dict['file1.txt'][1], 'data')

if __name__ == '__main__':
    unittest.main()