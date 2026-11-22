"""프로젝트 루트의 state.json을 읽고 씁니다."""

import json
import shutil
from datetime import datetime
from pathlib import Path

from default_quizzes import make_default_quizzes
from quiz import Quiz


STATE_PATH = Path(__file__).resolve().parent / "state.json"
STATE_WRITE_BLOCKED = False


def load_state() -> tuple[list[Quiz], dict | None]:
    global STATE_WRITE_BLOCKED
    STATE_WRITE_BLOCKED = False
    try:
        if not STATE_PATH.exists():
            return make_default_quizzes(), None
        with STATE_PATH.open("r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, dict) or not isinstance(data["quizzes"], list):
            raise ValueError("잘못된 데이터 형식")
        quizzes = [Quiz.from_dict(item) for item in data["quizzes"]]
        best = data["best_score"]
        if best is not None:
            if not isinstance(best, dict):
                raise ValueError("잘못된 점수 형식")
            score, correct, total = (best[key] for key in ("score", "correct", "total"))
            if any(type(value) is not int for value in (score, correct, total)):
                raise ValueError("잘못된 점수 형식")
            if not (0 <= score <= 100 and 0 <= correct <= total and total > 0):
                raise ValueError("잘못된 점수 범위")
        print(f"저장된 데이터를 불러왔습니다. (퀴즈 {len(quizzes)}개)")
        return quizzes, best
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        print(f"저장 파일을 읽을 수 없어 기본 퀴즈로 시작합니다: {error}")
        if STATE_PATH.exists():
            backup = STATE_PATH.with_name(
                f"state.corrupt-{datetime.now().strftime('%Y%m%d-%H%M%S-%f')}.json"
            )
            try:
                shutil.copy2(STATE_PATH, backup)
                print(f"원본 파일을 백업했습니다: {backup.name}")
            except OSError as backup_error:
                STATE_WRITE_BLOCKED = True
                print(f"원본 백업에 실패해 저장을 중지합니다: {backup_error}")
        return make_default_quizzes(), None


def save_state(quizzes: list[Quiz], best_score: dict | None) -> bool:
    if STATE_WRITE_BLOCKED:
        print("원본 파일 백업에 실패해 저장할 수 없습니다.")
        return False
    data = {"quizzes": [quiz.to_dict() for quiz in quizzes], "best_score": best_score}
    temporary = STATE_PATH.with_name("state.json.tmp")
    try:
        with temporary.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
            file.write("\n")
        temporary.replace(STATE_PATH)
        return True
    except (OSError, UnicodeError) as error:
        print(f"저장하지 못했습니다: {error}")
        try:
            temporary.unlink(missing_ok=True)
        except OSError:
            pass
        return False
