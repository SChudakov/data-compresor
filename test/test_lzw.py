import unittest

from src import lzw


class TestLZW(unittest.TestCase):

    # ---------------- test compress --------------

    def test_compress_data_special_case(self):
        data = 'ABABABA'
        expected_compressed_data = '0110011101000'
        # lzw_code = '01 10 011 101 000'
        # code_bytes = '01100111 01000'

        compressed_data = lzw._compress_data(data, self.generate_special_case_dictionary())

        self.assertEqual(expected_compressed_data, compressed_data)

    # ---------------- test _compress_data --------------

    def test_compress_data_wiki(self):
        data = 'TOBEORNOTTOBEORTOBEORNOT'
        expected_compressed_data = '101000111100010001010111110010001110001111010100' \
                                '011011011101011111100100011110100000100010000000'

        compressed_data = lzw._compress_data(data, self.generate_wiki_dictionary())

        self.assertEqual(expected_compressed_data, compressed_data)

    # ---------------- test decompress --------------

    def test_decompress_wiki(self):
        bits = '101000111100010001010111110010001110001111010100011011011101011111100100011110100000100010000000'
        expected_decompressed_data = 'TOBEORNOTTOBEORTOBEORNOT'

        wiki_dictionary = self.generate_wiki_dictionary()
        wiki_reversed_dictionary = self.generate_wiki_reversed_dictionary()

        decompressed_data = lzw._decompress_data(bits, wiki_dictionary, wiki_reversed_dictionary)

        self.assertEqual(expected_decompressed_data, decompressed_data)

    # ---------------- test _decompress_data --------------

    def test_decompress_special_case(self):
        bits = '0110011101000000'
        expected_decompressed_data = 'ABABABA'

        special_case_dictionary = self.generate_special_case_dictionary()
        special_case_reversed_dictionary = self.generate_special_case_reversed_dictionary()
        decompressed_data = lzw._decompress_data(bits, special_case_dictionary, special_case_reversed_dictionary)

        self.assertEqual(expected_decompressed_data, decompressed_data)

    @staticmethod
    def generate_special_case_dictionary():
        result = dict()
        result[lzw.end_of_file] = '0'
        result['A'] = '01'
        result['B'] = '10'
        return result

    @staticmethod
    def generate_special_case_reversed_dictionary():
        result = dict()
        result['0'] = lzw.end_of_file
        result['1'] = 'A'
        result['10'] = 'B'
        return result

    @staticmethod
    def generate_wiki_dictionary():
        result = dict()
        result[lzw.end_of_file] = '0'
        for i in range(1, 27):
            result[chr(i + 64)] = bin(i)[2:]
        return result

    @staticmethod
    def generate_wiki_reversed_dictionary():
        result = dict()
        result['0'] = lzw.end_of_file
        for i in range(1, 27):
            result[bin(i)[2:]] = chr(i + 64)
        return result

    @staticmethod
    def generate_wap_alphabet():
        chars_spans = [
            (0, 1),  # end of file
            (10, 11),  # strange new line
            (32, 128),  # simple characters
            (160, 161),  # strange space
            (171, 172),  # russian quotes
            (176, 177),  # degree symbol
            (187, 188),  # russian quotes
            (192, 256),  # other latin characters
            (1040, 1106),  # russian characters
            (8211, 8213),  # dash and long dash
            (8220, 8221),  # usual quotes
            (8222, 8223),  # usual quotes
            (8230, 8231),  # 3 points
            (8470, 8471)  # №
        ]

        result = dict()
        p = 0
        for i, j in chars_spans:
            for k in range(i, j):
                result[chr(k)] = bin(p)[2:]
                p += 1
        return result
