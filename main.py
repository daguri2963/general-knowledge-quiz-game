"""프로그램 시작과 입력 중단 시의 안전한 종료를 담당합니다."""

from game import QuizGame

def main() -> None:
    """저장된 상태로 게임을 시작하고, 입력이 끊기면 저장 후 종료합니다."""
    # game 객체를 유지해야 Ctrl+C나 EOF가 발생해도 현재 퀴즈와 점수를 저장할 수 있습니다.
    game = QuizGame()
    try:
        game.run()
    except (KeyboardInterrupt, EOFError):
        # 터미널에서 강제 중단하거나 입력 스트림이 끝나도 오류 화면 대신 종료 안내를 냅니다.
        print("\n입력이 중단되어 게임을 종료합니다.")
        game.save()


if __name__ == "__main__":
    # 다른 파일에서 main을 가져올 때는 게임이 자동 실행되지 않도록 합니다.
    main()
