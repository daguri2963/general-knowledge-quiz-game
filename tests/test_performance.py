"""1,000문제 규모에서 목록과 풀이 흐름의 시간·메모리를 확인합니다."""

import contextlib
import io
import time
import tracemalloc
import unittest
from unittest.mock import patch

from game import QuizGame
from quiz import Quiz


class PerformanceTests(unittest.TestCase):
    def test_thousand_quizzes(self) -> None:
        tracemalloc.start()
        started = time.perf_counter()
        try:
            with contextlib.redirect_stdout(io.StringIO()) as output:
                game = QuizGame()
                game.quizzes = [
                    Quiz(f"상식 문제 {number}?", ["하나", "둘", "셋", "넷"], 1)
                    for number in range(1, 1001)
                ]
                game.best_score = {"score": 100, "correct": 1000, "total": 1000}
                game.list_quizzes()
                with patch("builtins.input", return_value="1"):
                    game.play()
            elapsed = time.perf_counter() - started
            _, peak = tracemalloc.get_traced_memory()
        finally:
            tracemalloc.stop()
        self.assertIn("등록된 퀴즈 목록 (총 1000개)", output.getvalue())
        self.assertIn("1000문제 중 1000문제 정답! (100점)", output.getvalue())
        print(f"1000 quizzes: {elapsed:.2f}s, peak {peak / 1024 / 1024:.2f} MiB")
        self.assertLess(elapsed, 10)
        self.assertLess(peak, 30 * 1024 * 1024)


if __name__ == "__main__":
    unittest.main()
