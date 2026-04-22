"""Manage Students - add and remove students from classrooms."""

import streamlit as st
import pandas as pd
from auth import require_role
import models

require_role("teacher")
user = st.session_state.user

st.title("👥 Manage Students")

classrooms = models.get_teacher_classrooms(user["id"])
if not classrooms:
    st.warning("No classrooms assigned to you.")
    st.stop()

# ── Add New Student ────────────────────────────────────────────────────
st.subheader("Add New Student")

with st.form("add_student", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        display_name = st.text_input("Student Name", placeholder="e.g., Sam Parker")
        username = st.text_input("Username", placeholder="e.g., sparker")
    with col2:
        password = st.text_input("Password", value="student",
                                 help="Default password is 'student'. Students can't change it yet.")
        classroom_options = {c["name"]: c["id"] for c in classrooms}
        selected_classroom = st.selectbox("Classroom", options=list(classroom_options.keys()))

    if st.form_submit_button("Add Student", use_container_width=True):
        if not display_name.strip():
            st.warning("Please enter the student's name.")
        elif not username.strip():
            st.warning("Please enter a username.")
        elif len(username.strip()) < 3:
            st.warning("Username must be at least 3 characters.")
        elif not password.strip():
            st.warning("Please enter a password.")
        else:
            success, msg = models.add_student(
                username.strip().lower(),
                password,
                display_name.strip(),
                classroom_options[selected_classroom],
            )
            if success:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)

st.markdown("---")

# ── Current Students ───────────────────────────────────────────────────
st.subheader("Current Students")

classroom_names = {c["name"]: c["id"] for c in classrooms}
view_classroom = st.selectbox("View Classroom", options=list(classroom_names.keys()),
                              key="view_classroom")

students = models.get_students_by_classroom(classroom_names[view_classroom])

if students:
    df = pd.DataFrame([{
        "Name": s["display_name"],
        "Username": s["username"],
        "Balance": f"${s['balance']}",
    } for s in students])
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("Remove a Student")
    st.caption("This will permanently delete the student and all their transaction history.")

    remove_options = {s["display_name"]: s["id"] for s in students}
    selected_remove = st.selectbox("Select student to remove", options=list(remove_options.keys()))

    if st.button("Remove Student", type="secondary"):
        st.session_state["confirm_remove"] = remove_options[selected_remove]

    if "confirm_remove" in st.session_state:
        student_name = next(
            name for name, sid in remove_options.items()
            if sid == st.session_state["confirm_remove"]
        )
        st.warning(f"Are you sure you want to remove **{student_name}**? This cannot be undone.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Yes, Remove", type="primary"):
                success, msg = models.remove_student(st.session_state["confirm_remove"])
                if success:
                    st.success(msg)
                    st.session_state.pop("confirm_remove", None)
                    st.rerun()
                else:
                    st.error(msg)
        with col2:
            if st.button("Cancel"):
                st.session_state.pop("confirm_remove", None)
                st.rerun()
else:
    st.info("No students in this classroom yet. Add one above!")
