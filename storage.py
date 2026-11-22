"""프로젝트 루트의 state.json을 읽고 씁니다."""

import json
import shutil
from datetime import datetime
from pathlib import Path

from default_quizzes import make_default_quizzes
from quiz import Quiz


# 실행 위치가 달라도 프로젝트 루트의 동일한 state.json을 사용합니다.
STATE_PATH = Path(__file__).resolve().parent / "state.json"
# 손상 파일의 백업에 실패하면 원본을 덮어쓰지 않도록 이번 실행의 저장을 막습니다.
STATE_WRITE_BLOCKED = False


def load_state() -> tuple[list[Quiz], dict | None]:
    """JSON을 검증해 문제와 점수를 돌려주고, 손상 시 원본을 백업합니다."""
    global STATE_WRITE_BLOCKED
    # 다시 불러올 때 이전 시도의 저장 차단 상태를 그대로 사용하지 않습니다.
    STATE_WRITE_BLOCKED = False
    try:
        if not STATE_PATH.exists():
            # 첫 실행에는 파일이 없으므로 기본 문제와 아직 없는 최고 기록을 사용합니다.
            return make_default_quizzes(), None
        with STATE_PATH.open("r", encoding="utf-8") as file:
            # data는 JSON의 quizzes와 best_score를 담는 최상위 사전입니다.
            data = json.load(file)
        if not isinstance(data, dict) or not isinstance(data["quizzes"], list):
            raise ValueError("잘못된 데이터 형식")
        # Quiz 생성자를 거치면 저장 파일에 들어 있는 선택지·정답 형식도 검증됩니다.
        quizzes = [Quiz.from_dict(item) for item in data["quizzes"]]
        # best는 아직 플레이하지 않았을 때 null(None)일 수 있습니다.
        best = data["best_score"]
        if best is not None:
            if not isinstance(best, dict):
                raise ValueError("잘못된 점수 형식")
            # 세 숫자를 따로 확인해 손상된 점수 기록이 화면에 나타나지 않게 합니다.
            score, correct, total = (best[key] for key in ("score", "correct", "total"))
            if any(type(value) is not int for value in (score, correct, total)):
                raise ValueError("잘못된 점수 형식")
            if not (0 <= score <= 100 and 0 <= correct <= total and total > 0):
                raise ValueError("잘못된 점수 범위")
        print(f"저장된 데이터를 불러왔습니다. (퀴즈 {len(quizzes)}개)")
        return quizzes, best
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        # 읽기·인코딩·스키마 오류를 안내하되 게임 자체는 기본 문제로 시작합니다.
        print(f"저장 파일을 읽을 수 없어 기본 퀴즈로 시작합니다: {error}")
        if STATE_PATH.exists():
            # backup 이름에 시각과 마이크로초를 넣어 이전 백업과 겹치지 않게 합니다.
            backup = STATE_PATH.with_name(
                f"state.corrupt-{datetime.now().strftime('%Y%m%d-%H%M%S-%f')}.json"
            )
            try:
                shutil.copy2(STATE_PATH, backup)
                print(f"원본 파일을 백업했습니다: {backup.name}")
            except OSError as backup_error:
                # 백업을 못 만들었다면 다음 저장이 손상된 원본을 덮지 못하도록 합니다.
                STATE_WRITE_BLOCKED = True
                print(f"원본 백업에 실패해 저장을 중지합니다: {backup_error}")
        return make_default_quizzes(), None


def save_state(quizzes: list[Quiz], best_score: dict | None) -> bool:
    """문제와 최고 기록을 UTF-8 JSON으로 쓰고 성공 여부를 돌려줍니다."""
    if STATE_WRITE_BLOCKED:
        print("원본 파일 백업에 실패해 저장할 수 없습니다.")
        return False
    # data는 Quiz 객체를 JSON으로 저장할 수 있는 사전 형태로 바꾼 결과입니다.
    data = {"quizzes": [quiz.to_dict() for quiz in quizzes], "best_score": best_score}
    # temporary에 먼저 완성본을 써야 저장 중 오류가 나도 기존 state.json이 남습니다.
    temporary = STATE_PATH.with_name("state.json.tmp")
    try:
        with temporary.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
            file.write("\n")
        # 같은 폴더의 임시 파일을 원본과 교체해 부분적으로 쓰인 파일을 피합니다.
        temporary.replace(STATE_PATH)
        return True
    except (OSError, UnicodeError) as error:
        print(f"저장하지 못했습니다: {error}")
        try:
            # 실패한 임시 파일은 다음 저장을 방해하지 않도록 정리합니다.
            temporary.unlink(missing_ok=True)
        except OSError:
            pass
        return False
