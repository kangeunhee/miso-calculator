import os

# 40개 웹툴 메타데이터
tools_data = [
    # Category 1: Game & Random (1-10)
    {"id": 1, "title": "랜덤 사다리 타기", "desc": "벌칙, 내기, 당첨자 지정을 지원하는 사다리타기", "cat": "game", "icon": "git-merge", "href": "ladder.html"},
    {"id": 2, "title": "원반 룰렛 돌리기", "desc": "메뉴 결정 및 순서 정하기 회전 룰렛", "cat": "game", "icon": "disc", "href": "roulette.html"},
    {"id": 3, "title": "무작위 팀 나누기", "desc": "인원수 및 팀 수 기준 공정한 조 편성기", "cat": "game", "icon": "users", "href": "team-generator.html"},
    {"id": 4, "title": "제비뽑기 / 당첨 추첨", "desc": "명단 입력 후 랜덤 당첨자 무작위 추출", "cat": "game", "icon": "ticket", "href": "raffle.html"},
    {"id": 5, "title": "오늘 점심 메뉴 룰렛", "desc": "한식, 중식, 일식 등 음식 카테고리별 추천", "cat": "game", "icon": "utensils", "href": "lunch-menu.html"},
    {"id": 6, "title": "벌칙 & 미션 생성기", "desc": "술자리 및 모임용 분위기 업 랜덤 미션", "cat": "game", "icon": "dices", "href": "penalty-mission.html"},
    {"id": 7, "title": "로또 번호 추첨기", "desc": "고정수 및 제외수를 설정하는 로또 번호 추출", "cat": "game", "icon": "clover", "href": "lotto-generator.html"},
    {"id": 8, "title": "다중 주사위 굴리기", "desc": "1D6부터 1D100까지 다중 주사위 시뮬레이션", "cat": "game", "icon": "box", "href": "dice-roller.html"},
    {"id": 9, "title": "3D 동전 던지기", "desc": "앞면/뒷면 결정을 위한 동전 던지기", "cat": "game", "icon": "coins", "href": "coin-flip.html"},
    {"id": 10, "title": "초성 퀴즈 단어 생성", "desc": "자음 기준 무작위 초성 단어 제시기", "cat": "game", "icon": "type", "href": "chosung-quiz.html"},

    # Category 2: Test & Measure (11-20)
    {"id": 11, "title": "마우스 CPS 클릭 측정", "desc": "1초, 5초, 10초 마우스 광클 속도 측정기", "cat": "test", "icon": "mouse-pointer-click", "href": "cps-test.html"},
    {"id": 12, "title": "반응 속도 테스트", "desc": "화면 색상 변환 시 순발력 반응 속도 측정", "cat": "test", "icon": "zap", "href": "reaction-time.html"},
    {"id": 13, "title": "타자 속도 연습기", "desc": "한글 및 영문 긍정 문장 타수 측정기", "cat": "test", "icon": "keyboard", "href": "typing-test.html"},
    {"id": 14, "title": "모니터 불량화소 테스트", "desc": "단색, 잔상, 명암비 모니터 정밀 점검", "cat": "test", "icon": "monitor", "href": "monitor-test.html"},
    {"id": 15, "title": "청력 주파수 테스트", "desc": "Hz별 사운드 재생을 통한 가청 주파수 검사", "cat": "test", "icon": "volume-2", "href": "hearing-test.html"},
    {"id": 16, "title": "키보드 동시입력 검사", "desc": "게이밍 키보드 N-Key Rollover 점검", "cat": "test", "icon": "sliders", "href": "keyboard-test.html"},
    {"id": 17, "title": "Tap BPM 측정기", "desc": "음악 비트에 맞춰 클릭하여 BPM 측정", "cat": "test", "icon": "activity", "href": "tap-bpm.html"},
    {"id": 18, "title": "눈싸움 타이머 / 시력", "desc": "눈 안 감기 타이머 및 화면 가늠 테스트", "cat": "test", "icon": "eye", "href": "staring-timer.html"},
    {"id": 19, "title": "에임 정밀도 테스트", "desc": "무작위 표적 정밀 타격 에임 연습 게임", "cat": "test", "icon": "target", "href": "aim-test.html"},
    {"id": 20, "title": "기억력 블록 테스트", "desc": "순서대로 점등되는 블록 기억하기 게임", "cat": "test", "icon": "brain", "href": "memory-game.html"},

    # Category 3: Psychology & Personality (21-30)
    {"id": 21, "title": "MBTI 10문항 빠른 진단", "desc": "핵심 질문으로 빠르게 확인하는 성격 유형", "cat": "psych", "icon": "user-check", "href": "mbti-test.html"},
    {"id": 22, "title": "퍼스널 컬러 간이 진단", "desc": "화면 피부 톤 비교를 통한 웜/쿨톤 검사", "cat": "psych", "icon": "palette", "href": "personal-color.html"},
    {"id": 23, "title": "혈액형/별자리 궁합", "desc": "혈액형, 띠, 별자리 기준 상대와의 궁합", "cat": "psych", "icon": "heart", "href": "compatibility-test.html"},
    {"id": 24, "title": "미래 직업 예측기", "desc": "이름 입력 시 무작위 선호 미래 직업 결과", "cat": "psych", "icon": "briefcase", "href": "future-job.html"},
    {"id": 25, "title": "전생 / 칭호 생성기", "desc": "나의 전생과 특이한 칭호 알아보기", "cat": "psych", "icon": "crown", "href": "past-life.html"},
    {"id": 26, "title": "오늘의 포춘쿠키 운세", "desc": "매일 업데이트되는 포춘쿠키 메시지", "cat": "psych", "icon": "cookie", "href": "fortune-cookie.html"},
    {"id": 27, "title": "연애 상극/환상 짝꿍", "desc": "연애 성향 비교 및 환상의 짝꿍 분석", "cat": "psych", "icon": "flame", "href": "love-match.html"},
    {"id": 28, "title": "스트레스 지수 진단", "desc": "자가 진단을 통한 현재 스트레스 수준 측정", "cat": "psych", "icon": "smile", "href": "stress-test.html"},
    {"id": 29, "title": "닮은 동물상 테스트", "desc": "분위기 키워드로 찾아보는 동물상 결과", "cat": "psych", "icon": "dog", "href": "animal-lookalike.html"},
    {"id": 30, "title": "성향 간이 심리 테스트", "desc": "재미로 보는 심리 특성 간단 테스트", "cat": "psych", "icon": "shield-alert", "href": "psychology-test.html"},

    # Category 4: Utility & Media (31-40)
    {"id": 31, "title": "온라인 스톱워치/시계", "desc": "전체화면 디지털 시계 및 스톱워치", "cat": "utility", "icon": "clock", "href": "stopwatch-clock.html"},
    {"id": 32, "title": "D-Day 위젯 생성기", "desc": "시험, 전역일, 결혼식 D-Day 카운트다운", "cat": "utility", "icon": "calendar", "href": "dday-calculator.html"},
    {"id": 33, "title": "유튜브 썸네일 추출기", "desc": "영상 URL 입력 시 고화질 썸네일 다운로드", "cat": "utility", "icon": "youtube", "href": "youtube-thumbnail.html"},
    {"id": 34, "title": "서명/도장 PNG 생성", "desc": "배경 투명 캔버스 도장 이미지 만들기", "cat": "utility", "icon": "file-signature", "href": "signature-generator.html"},
    {"id": 35, "title": "SNS 특수 폰트 변환기", "desc": "인스타그램 프로필용 예쁜 폰트 생성", "cat": "utility", "icon": "sparkle", "href": "fancy-fonts.html"},
    {"id": 36, "title": "텍스트 음성 변환 (TTS)", "desc": "웹 브라우저 엔진 기반 음성 읽어주기", "cat": "utility", "icon": "volume-x", "href": "text-to-speech.html"},
    {"id": 37, "title": "이미지 컬러 팔레트", "desc": "이미지 업로드 시 대표 색상 추출", "cat": "utility", "icon": "pipette", "href": "color-palette.html"},
    {"id": 38, "title": "텍스트 암호화/복호화", "desc": "비밀 메시지 암호문 변환 및 복원 툴", "cat": "utility", "icon": "lock", "href": "text-encryptor.html"},
    {"id": 39, "title": "웹캠 / 화면 캡처 테스트", "desc": "웹캠 동작 확인 및 화면 캡처 유틸리티", "cat": "utility", "icon": "camera", "href": "webcam-test.html"},
    {"id": 40, "title": "단어 빈도수 분석기", "desc": "텍스트 내 주요 단어 빈도 시각화", "cat": "utility", "icon": "bar-chart-3", "href": "word-frequency.html"}
]

# 공통 HTML 템플릿 함수
def generate_html(tool):
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{tool['title']} - misopick.kr</title>
    <meta name="description" content="{tool['desc']}">
    
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    colors: {{
                        brand: {{
                            50: '#f0f9ff',
                            100: '#e0f2fe',
                            500: '#0284c7',
                            600: '#0284c7',
                            700: '#0369a1',
                        }}
                    }}
                }}
            }}
        }}
    </script>
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
        body {{ font-family: "Pretendard Variable", Pretendard, -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif; }}
    </style>
</head>
<body class="bg-slate-50 text-slate-800 flex flex-col min-h-screen">

    <!-- Header Navigation -->
    <header class="bg-white/80 backdrop-blur-md border-b border-slate-200 sticky top-0 z-40">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <a href="index.html" class="flex items-center space-x-2">
                <div class="w-9 h-9 rounded-xl bg-brand-600 flex items-center justify-center text-white font-black text-lg shadow-sm">M</div>
                <span class="text-xl font-black tracking-tight text-slate-900">misopick<span class="text-brand-600">.kr</span></span>
            </a>
            <a href="index.html" class="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg border border-slate-200 text-sm font-medium text-slate-600 hover:bg-slate-100 transition">
                <i data-lucide="arrow-left" class="w-4 h-4"></i>
                <span>전체 툴 보기</span>
            </a>
        </div>
    </header>

    <!-- Main Content Container -->
    <main class="flex-grow max-w-4xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        <!-- Tool Title Card -->
        <div class="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm mb-6">
            <div class="flex items-center space-x-4 mb-4">
                <div class="w-12 h-12 rounded-2xl bg-brand-50 text-brand-600 flex items-center justify-center">
                    <i data-lucide="{tool['icon']}" class="w-6 h-6"></i>
                </div>
                <div>
                    <span class="text-xs font-bold text-slate-400 block">TOOL #{tool['id']:02d}</span>
                    <h1 class="text-2xl sm:text-3xl font-black text-slate-900">{tool['title']}</h1>
                </div>
            </div>
            <p class="text-slate-600 text-sm sm:text-base leading-relaxed">{tool['desc']}</p>
        </div>

        <!-- Tool Workspace Area -->
        <div class="bg-white rounded-3xl p-6 sm:p-10 border border-slate-200 shadow-sm min-h-[400px] flex flex-col items-center justify-center text-center">
            <!-- TODO: 실제 로직 개발 영역 -->
            <div class="p-4 bg-slate-100 rounded-2xl mb-4">
                <i data-lucide="{tool['icon']}" class="w-12 h-12 text-slate-400 mx-auto"></i>
            </div>
            <h2 class="text-xl font-bold text-slate-800 mb-2">{tool['title']} 기능 준비 중</h2>
            <p class="text-slate-500 text-sm max-w-md">여기에 해당 웹툴의 실행 화면 및 인터랙티브 기능 로직이 들어갑니다.</p>
        </div>

    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-slate-200 py-8 mt-auto">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-slate-500">
            <p>© misopick.kr - 모든 서비스는 무료로 제공됩니다.</p>
            <a href="index.html" class="hover:text-slate-800 transition">메인으로 돌아가기</a>
        </div>
    </footer>

    <script>
        document.addEventListener('DOMContentLoaded', () => {{
            lucide.createIcons();
        }});
    </script>
</body>
</html>
"""

# 스크립트 실행 함수
def create_all_files():
    count = 0
    for tool in tools_data:
        filename = tool["href"]
        content = generate_html(tool)
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
            
        print(f"✅ 생성 완료: {filename} ({tool['title']})")
        count += 1
        
    print(f"\n🎉 총 {count}개의 HTML 파일 생성이 완료되었습니다!")

if __name__ == "__main__":
    create_all_files()