import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, firestore
import json

# Streamlit 페이지 기본 설정
st.set_page_config(page_title="간단 일정관리 앱", page_icon="📅", layout="centered")

# 1. Firebase Admin SDK 초기화
@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        # 파일에서 키를 읽거나 Streamlit Secrets에서 가져오는 방식
        try:
            # 로컬 파일 기준 (배포 시 st.secrets 사용 권장)
            cred = credentials.Certificate("firebase_key.json")
            firebase_admin.initialize_app(cred)
        except Exception:
            # st.secrets에 등록된 JSON 형태 정보를 읽어옴 (배포용)
            key_dict = json.loads(st.secrets["textkey"])
            cred = credentials.Certificate(key_dict)
            firebase_admin.initialize_app(cred)

init_firebase()
db = firestore.client()

# 2. 세션 상태 초기화 (로그인 유지를 위함)
if "user" not in st.session_state:
    st.session_state["user"] = None

# --- 인증 관련 함수 ---
def login_user(email, password):
    try:
        user = auth.get_user_by_email(email)
        # Firebase Admin SDK는 비밀번호 직접 검증 기능을 제공하지 않으므로,
        # 실무에서는 Firebase REST API를 사용하거나 간이 인증 처리를 합니다.
        # 본 예시에서는 존재 유무 확인 후 로그인 상태를 저장합니다.
        st.session_state["user"] = {"uid": user.uid, "email": user.email}
        st.success(f"{user.email}님 환영합니다!")
        st.rerun()
    except Exception as e:
        st.error("로그인 실패: 이메일이나 비밀번호를 확인하세요.")

def signup_user(email, password):
    try:
        user = auth.create_user(email=email, password=password)
        st.success("회원가입이 완료되었습니다! 로그인 해주세요.")
    except Exception as e:
        st.error(f"회원가입 실패: {e}")

def logout():
    st.session_state["user"] = None
    st.rerun()


# --- UI 및 비즈니스 로직 ---
st.title("📅 간단 일정 관리 앱")

# A. 비로그인 상태 (회원가입 / 로그인 화면)
if st.session_state["user"] is None:
    tab1, tab2 = st.tabs(["로그인", "회원가입"])

    with tab1:
        st.subheader("로그인")
        login_email = st.text_input("이메일", key="login_email")
        login_password = st.text_input("비밀번호", type="password", key="login_pw")
        if st.button("로그인"):
            if login_email and login_password:
                login_user(login_email, login_password)
            else:
                st.warning("이메일과 비밀번호를 모두 입력해주세요.")

    with tab2:
        st.subheader("회원가입")
        signup_email = st.text_input("이메일", key="signup_email")
        signup_password = st.text_input("비밀번호 (6자리 이상)", type="password", key="signup_pw")
        if st.button("회원가입"):
            if signup_email and signup_password:
                signup_user(signup_email, signup_password)
            else:
                st.warning("이메일과 비밀번호를 모두 입력해주세요.")

# B. 로그인 상태 (일정 관리 화면)
else:
    user = st.session_state["user"]
    user_uid = user["uid"]

    # 상단 사용자 정보 및 로그아웃
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(f"👤 **{user['email']}** 님 로그인 중")
    with col2:
        if st.button("로그아웃"):
            logout()

    st.divider()

    # 1. 새 일정 추가 Form
    st.subheader("➕ 새 일정 추가")
    with st.form("todo_form", clear_on_submit=True):
        todo_text = st.text_input("할 일을 입력하세요")
        todo_date = st.date_input("날짜")
        submitted = st.form_submit_button("추가하기")

        if submitted:
            if todo_text:
                # Firestore의 todos 컬렉션에 사용자 ID와 함께 저장
                db.collection("todos").add({
                    "uid": user_uid,
                    "text": todo_text,
                    "date": str(todo_date),
                    "done": False
                })
                st.success("일정이 추가되었습니다.")
                st.rerun()
            else:
                st.warning("내용을 입력해주세요.")

    st.divider()

    # 2. 내 일정 목록 보기 및 상태 변경/삭제
    st.subheader("📋 내 일정 목록")
    
    # 로그인한 사용자의 일정만 조회
    todos_ref = db.collection("todos").where("uid", "==", user_uid).stream()
    todos = [{"id": doc.id, **doc.to_dict()} for doc in todos_ref]

    if not todos:
        st.info("등록된 일정이 없습니다. 새 일정을 추가해보세요!")
    else:
        for todo in todos:
            col_check, col_content, col_del = st.columns([0.8, 3, 0.8])
            
            # 완료 여부 체크박스
            with col_check:
                is_done = st.checkbox("", value=todo["done"], key=f"check_{todo['id']}")
                if is_done != todo["done"]:
                    db.collection("todos").doc(todo["id"]).update({"done": is_done})
                    st.rerun()

            # 일정 내용 표시 (완료 시 취소선)
            with col_content:
                if todo["done"]:
                    st.markdown(f"~~{todo['text']} ({todo['date']})~~")
                else:
                    st.markdown(f"**{todo['text']}** ({todo['date']})")

            # 삭제 버튼
            with col_del:
                if st.button("삭제", key=f"del_{todo['id']}"):
                    db.collection("todos").doc(todo["id"]).delete()
                    st.success("삭제되었습니다.")
                    st.rerun()