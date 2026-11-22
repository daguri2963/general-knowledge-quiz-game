"""실제 프로그램을 실행해 저장과 오류 처리를 확인합니다."""

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCES = ("main.py", "game.py", "quiz.py", "default_quizzes.py", "storage.py")


class GameTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        for name in SOURCES:
            shutil.copy2(ROOT / name, self.folder / name)

    def run_game(self, answers: str) -> str:
        result = subprocess.run(
            [sys.executable, "main.py"],
            cwd=self.folder,
            input=answers,
            text=True,
            encoding="utf-8",
            capture_output=True,
            timeout=10,
            check=True,
        )
        return result.stdout

    def test_add_quiz_survives_restart(self) -> None:
        output = self.run_game("2\n새 상식 문제?\n하나\n둘\n셋\n넷\n 2 \n5\n")
        self.assertIn("퀴즈가 추가되고 저장되었습니다.", output)
        self.assertIn("새 상식 문제?", self.run_game("3\n5\n"))
        data = json.loads((self.folder / "state.json").read_text(encoding="utf-8"))
        self.assertEqual(len(data["quizzes"]), 8)

    def test_score_survives_restart(self) -> None:
        output = self.run_game("1\n2\n3\n2\n3\n4\n2\n1\n5\n")
        self.assertIn("7문제 중 7문제 정답! (100점)", output)
        self.assertIn("최고 점수: 100점", self.run_game("4\n5\n"))

    def test_invalid_input_and_corrupt_file(self) -> None:
        (self.folder / "state.json").write_text("{broken", encoding="utf-8")
        output = self.run_game("\nabc\n9\n 3 \n5\n")
        self.assertIn("기본 퀴즈로 시작합니다", output)
        self.assertEqual(output.count("1~5 사이의 숫자를 입력하세요."), 3)
        self.assertIn("등록된 퀴즈 목록 (총 7개)", output)

    def test_eof_saves_and_exits(self) -> None:
        output = self.run_game("")
        self.assertIn("입력이 중단되어 게임을 종료합니다.", output)
        self.assertTrue((self.folder / "state.json").exists())


if __name__ == "__main__":
    unittest.main()
