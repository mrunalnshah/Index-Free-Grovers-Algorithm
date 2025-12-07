import plotly.graph_objects as go

class KMP:
    def __init__(self):
        pass

    
    @staticmethod
    def get_lps_array(pattern: str) :
        """
        Computes the Longest Proper Prefix which is also a Suffix (LPS) array for the pattern.

        :param pattern: input pattern to be search in the DNA Sequence
        """

        n = len(pattern)
        lps = [0] * n

        length = 0
        i = 1 # lps[0] is always 0

        while i < n:
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps
        
    # KMP Search Method
    @staticmethod
    def search(pattern: str, text: str):
        """
        Searches for all occurrences of pattern P in text T using the KMP algorithm.
        
        :param pattern: input pattern to be search in the DNA Sequence (string)
        :param text: DNA Sequence as a string
        """

        n = len(text)
        m = len(pattern)

        lps = KMP.get_lps_array(pattern)

        i = 0
        j = 0

        match = []
        while i < n:
            if pattern[j] == text[i]:
                i += 1
                j += 1
            
            if j == m:
                match.append(i - j)
                j = lps[j - 1]
            elif i < n and pattern[j] != text[i]:
                if j != 0:
                    j = lps[j - 1]
                else:
                    i += 1
        return match