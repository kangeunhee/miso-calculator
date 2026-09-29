import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, firestore
import json
from datetime import datetime, date

# -----------------------------------------------------------------------------
# 1. Page Configuration & Custom CSS
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Pro Task Manager",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 깔끔한 대시보드 및 UI 스타일링을 위한 Custom CSS
st.markdown("""
<style>
    .stProgress > div > div > div > div { background-color: #4CAF50; }
    .task-card {
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin-bottom: 0.8rem;
        background-color: #f9f9f9;
    }
    .priority-high { color: #ff4d4f; font-weight: bold; }
    .priority-medium { color: #faad14; font-weight: bold; }
    .priority-low { color: #52c41a; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. Firebase Initialization
# -----------------------------------------------------------------------------
@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        try:
            # 로컬 테스트 환경
            cred = credentials.Certificate("firebase_key.json")
            firebase_admin.initialize_app(cred)
        except Exception:
            # Streamlit Cloud 배포 환경 (Secrets)
            key_dict = json.loads(st.secrets["textkey"])
            cred = credentials.Certificate(key_dict)
            firebase_admin.initialize_app(cred)

init_firebase()
db = firestore.client()

# -----------------------------------------------------------------------------
# 3. Session State Management
# -----------------------------------------------------------------------------
if "user" not in st.session_state:
    st.session_state["user"] = None

# -----------------------------------------------------------------------------
# 4. Authentication Logic
# -----------------------------------------------------------------------------
def login_user(email, password):
    try:
        user = auth.get_user_by_email(email)
        st.session_state["user"] = {"uid": user.uid, "email": user.email}
        st.toast("성공적으로 로그인되었습니다!", icon="✅")
        st.rerun()
    except Exception as e:
        st.error("로그인 실패: 이메일 또는 비밀번호를 확인하세요.")

def signup_user(email, password):
    try:
        if len(password) < 6:
            st.warning("비밀번호는 최소 6자리 이상이어야 합니다.")
            return
        user = auth.create_user(email=email, password=password)
        st.success("회원가입이 완료되었습니다. 로그인 탭으로 이동하여 로그인해주세요.")
    except Exception as e:
        st.error(f"회원가입 실패: {e}")

def logout():
    st.session_state["user"] = None
    st.rerun()

# -----------------------------------------------------------------------------
# 5. Main Application Logic
# -----------------------------------------------------------------------------

# A. 비로그인 상태 (인증 화면)
if st.session_state["user"] is None:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("📅 Pro Task Manager")
        st.subheader("개인 일정 관리 시스템")
        
        tab_login, tab_signup = st.tabs(["🔒 로그인", "📝 회원가입"])
        
        with tab_login:
            with st.form("login_form"):
                email = st.text_input("이메일 주소")
                password = st.text_input("비밀번호", type="password")
                submit = st.form_submit_button("로그인", use_container_width=True)
                if submit:
                    if email and password:
                        login_user(email, password)
                    else:
                        st.warning("이메일과 비밀번호를 모두 입력하세요.")

        with tab_signup:
            with st.form("signup_form"):
                new_email = st.text_input("이메일 주소")
                new_password = st.text_input("비밀번호 (6자리 이상)", type="password")
                submit = st.form_submit_button("회원가입", use_container_width=True)
                if submit:
                    if new_email and new_password:
                        signup_user(new_email, new_password)
                    else:
                        st.warning("이메일과 비밀번호를 모두 입력하세요.")

# B. 로그인 상태 (일정 관리 메인 화면)
else:
    user = st.session_state["user"]
    user_uid = user["uid"]

    # --- 사이드바 (사용자 정보 및 필터 설정) ---
    with st.sidebar:
        st.title("👤 프로필")
        st.write(f"**이메일**: {user['email']}")
        if st.button("로그아웃", use_container_width=True):
            logout()
        
        st.divider()
        st.header("🔍 검색 및 필터")
        search_query = st.text_input("일정 검색", placeholder="제목 검색...")
        
        filter_category = st.selectbox(
            "카테고리 필터",
            ["전체", "업무", "개인", "공부", "기타"]
        )
        
        filter_priority = st.selectbox(
            "우선순위 필터",
            ["전체", "높음", "중간", "낮음"]
        )

        filter_status = st.radio(
            "상태 필터",
            ["전체", "진행 중", "완료됨"]
        )

    # --- 메인 본문 ---
    st.title("📅 개인 일정 관리 대시보드")

    # 1. Firestore에서 사용자의 데이터 로드
    todos_ref = db.collection("todos").where("uid", "==", user_uid).stream()
    all_todos = [{"id": doc.id, **doc.to_dict()} for doc in todos_ref]

    # 2. 통계 대시보드 계산
    total_count = len(all_todos)
    done_count = sum(1 for t in all_todos if t.get("done", False))
    pending_count = total_count - done_count
    completion_rate = (done_count / total_count) if total_count > 0 else 0.0

    st.subheader("📊 통계 요약")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("전체 일정", f"{total_count}개")
    m2.metric("진행 중인 일정", f"{pending_count}개")
    m3.metric("완료된 일정", f"{done_count}개")
    m4.metric("달성률", f"{int(completion_rate * 100)}%")
    st.progress(completion_rate)

    st.divider()

    # 3. 새 일정 추가 Form
    with st.expander("➕ 새 일정 등록하기", expanded=False):
        with st.form("new_todo_form", clear_on_submit=True):
            col_title, col_cat, col_prio = st.columns([3, 1, 1])
            with col_title:
                title = st.text_input("일정 제목 *")
            with col_cat:
                category = st.selectbox("카테고리", ["업무", "개인", "공부", "기타"])
            with col_prio:
                priority = st.selectbox("우선순위", ["높음", "중간", "낮음"], index=1)
            
            col_date, col_memo = st.columns([1, 2])
            with col_date:
                due_date = st.date_input("마감일", min_value=date.today())
            with col_memo:
                memo = st.text_input("상세 메모 (선택사항)")

            submit_todo = st.form_submit_button("일정 저장", use_container_width=True)

            if submit_todo:
                if title.strip():
                    db.collection("todos").add({
                        "uid": user_uid,
                        "title": title.strip(),
                        "category": category,
                        "priority": priority,
                        "due_date": str(due_date),
                        "memo": memo.strip(),
                        "done": False,
                        "created_at": datetime.now().isoformat()
                    })
                    st.toast("새 일정이 추가되었습니다!", icon="🎉")
                    st.rerun()
                else:
                    st.warning("일정 제목을 입력해주세요.")

    # 4. 데이터 필터링 로직
    filtered_todos = all_todos

    if search_query:
        filtered_todos = [t for t in filtered_todos if search_query.lower() in t.get("title", "").lower()]
    
    if filter_category != "전체":
        filtered_todos = [t for t in filtered_todos if t.get("category") == filter_category]

    if filter_priority != "전체":
        filtered_todos = [t for t in filtered_todos if t.get("priority") == filter_priority]

    if filter_status == "진행 중":
        filtered_todos = [t for t in filtered_todos if not t.get("done", False)]
    elif filter_status == "완료됨":
        filtered_todos = [t for t in filtered_todos if t.get("done", False)]

    # 마감일 순으로 정렬
    filtered_todos = sorted(filtered_todos, key=lambda x: x.get("due_date", "9999-12-31"))

    # 5. 일정 목록 표시
    st.subheader(f"📋 일정 목록 ({len(filtered_todos)}개)")

    if not filtered_todos:
        st.info("조건에 일치하는 일정이 없습니다.")
    else:
        for todo in filtered_todos:
            todo_id = todo["id"]
            is_done = todo.get("done", False)
            prio = todo.get("priority", "중간")
            prio_class = f"priority-{prio.replace('높음', 'high').replace('중간', 'medium').replace('낮음', 'low')}"

            # 오늘 마감이거나 지연된 미완료 일정 경고
            due_str = todo.get("due_date", "")
            is_overdue = False
            if due_str and not is_done:
                due_dt = datetime.strptime(due_str, "%Y-%m-%d").date()
                if due_dt <= date.today():
                    is_overdue = True

            with st.container():
                c_check, c_body, c_actions = st.columns([0.5, 4, 1.5])

                # 체크박스 (상태 변경)
                with c_check:
                    checked = st.checkbox("", value=is_done, key=f"chk_{todo_id}")
                    if checked != is_done:
                        db.collection("todos").doc(todo_id).update({"done": checked})
                        st.rerun()

                # 본문
                with c_body:
                    title_display = f"~~{todo['title']}~~" if is_done else f"**{todo['title']}**"
                    overdue_badge = " ⚠️ **[마감 임박/지연]**" if is_overdue else ""
                    
                    st.markdown(f"{title_display} {overdue_badge}")
                    st.caption(f"📁 {todo.get('category', '기타')} | 🎯 우선순위: <span class='{prio_class}'>{prio}</span> | 📅 마감일: {due_str} | 📝 {todo.get('memo', '')}", unsafe_allow_html=True)

                # 수정/삭제 액션
                with c_actions:
                    btn_col1, btn_col2 = st.columns(2)
                    
                    with btn_col1:
                        if st.button("🗑️", key=f"del_{todo_id}", help="삭제"):
                            db.collection("todos").doc(todo_id).delete()
                            st.toast("일정이 삭제되었습니다.")
                            st.rerun()

                    with btn_col2:
                        # 수정 기능은 expander로 서브 폼 제공
                        with st.popover("✏️"):
                            with st.form(key=f"edit_form_{todo_id}"):
                                new_t = st.text_input("제목", value=todo["title"])
                                new_cat = st.selectbox("카테고리", ["업무", "개인", "공부", "기타"], index=["업무", "개인", "공부", "기타"].index(todo.get("category", "기타")))
                                new_prio = st.selectbox("우선순위", ["높음", "중간", "낮음"], index=["높음", "중간", "낮음"].index(todo.get("priority", "중간")))
                                new_memo = st.text_input("메모", value=todo.get("memo", ""))
                                
                                update_btn = st.form_submit_button("수정 완료")
                                if update_btn:
                                    db.collection("todos").doc(todo_id).update({
                                        "title": new_t,
                                        "category": new_cat,
                                        "priority": new_prio,
                                        "memo": new_memo
                                    })
                                    st.toast("수정되었습니다.")
                                    st.rerun()
                st.divider()
