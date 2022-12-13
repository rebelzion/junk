from typing import Dict
import pytest

class Solution:

    def compute_char_count(self, s: str) -> Dict[str, int]:
        """
        Computes character count for string `s`
        """
        d = {}
        for c in s:
            if c not in d:
                d[c] = 0
            d[c] += 1
        return d

    def contains(self, s_cnt: Dict[str, int], t_cnt: Dict[str, int]) -> bool:
        """
        Checks wether `s_cnt` contains `t_cnt`.
        """
        for c, cnt in t_cnt.items():
            if c not in s_cnt or s_cnt[c] < cnt:
                return False
        return True


    def minWindow(self, s: str, t: str) -> str:
        """
        Finds the minimum window length such that `s` contains all the characters
        that `t` contains.
        The solution runs in O(N) time and space O(N+M) where N = #s and M = #t
        Returns:
            str: It returns the substring of s with that window size or
        empty string('') if no minimum window respecting the conditions has been
        found.
        """

        t_cnt = self.compute_char_count(t)

        l,r = 0,0
        is_complete = False
        s_cnt = {}

        min_window_len = 2**32
        min_left_index = -1
        while l <= r and r < len(s):
            c = s[r]
            if c not in s_cnt:
                s_cnt[c] = 0
            s_cnt[c] += 1

            if not is_complete:
                if self.contains(s_cnt, t_cnt):
                    is_complete = True
                    if r-l+1 < min_window_len:
                        min_window_len = r-l+1
                        min_left_index = l
            if is_complete:
                # if the current window (l,r) in s contains all the characters
                # we try to shrink it from the left as long as we don't remove
                # characters that need to be contained in `t`.
                while True:
                    cc = s[l]
                    if cc not in t_cnt or s_cnt[cc]-1 >= t_cnt[cc]:
                        s_cnt[cc] -= 1
                        l += 1
                    else:
                        break
                if r-l+1 < min_window_len:
                    min_window_len = r-l+1
                    min_left_index = l

            r += 1

        return "" if min_left_index == -1 else s[min_left_index:min_left_index+min_window_len]


@pytest.mark.parametrize("inp,expected", [
    (("ADOBECODEBANC", "ABC"), "BANC"),
    (("a","a"), "a"),
    (("a", "aa"), ""),
    (("ab", "a"), "a")]
)
def test_minWindow(inp, expected):
    sol = Solution()
    assert sol.minWindow(*inp) == expected



