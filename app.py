import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import base64
import core_engine as ce
import db_engine as db
import slide_maker as sm

# --- PAGE CONFIG & INIT ---
st.set_page_config(page_title="Nexus | EdTech Platform", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")
db.init_db()


def get_avatar(username):
    user_prof = db.get_profile(username)
    if user_prof and user_prof.get("profile_pic"):
        return base64.b64decode(user_prof["profile_pic"])
    return "👤"


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "active_chat" not in st.session_state:
    st.session_state.active_chat = None

if "sidebar_hidden" not in st.session_state:
    st.session_state.sidebar_hidden = False

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #0f172a; color: #f8fafc; font-family: 'Inter', sans-serif; }
    .stTextArea textarea { background-color: #1e293b; color: #f1f5f9; border: 1px solid #334155; border-radius: 12px; }
    .stButton>button { background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); color: white; border: none; border-radius: 8px; font-weight: 600; transition: all 0.3s ease; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.4); }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; background-color: transparent; }
    .stTabs [data-baseweb="tab"] { height: 50px; background-color: transparent; color: #cbd5e1; font-size: 1.1rem; font-weight: 500; }
    .stTabs [aria-selected="true"] { color: #818cf8 !important; border-bottom-color: #818cf8 !important; }

    /* Custom metric styling for leaderboard */
    div[data-testid="stMetricValue"] { font-size: 1.5rem; color: #818cf8; }
</style>
""", unsafe_allow_html=True)

# --- LOGIN / SIGNUP SCREEN ---
if not st.session_state.logged_in:
    st.markdown(
        "<br><br><h1 style='text-align: center; font-size: 4rem; background: -webkit-linear-gradient(45deg, #818cf8, #c084fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Nexus Learning</h1>",
        unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center; color: #94a3b8; font-size: 1.2rem;'>Bridging the gap between messy notes and collaborative mastery.</p><br>",
        unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            auth_mode = st.radio("Welcome:", ["Login", "Sign Up"], horizontal=True)
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.button("Enter Platform", use_container_width=True):
                if auth_mode == "Sign Up":
                    if db.create_user(username, password):
                        st.success("Account created! Please switch to Login.")
                    else:
                        st.error("Username already exists.")
                else:
                    if db.login_user(username, password):
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.rerun()
                    else:
                        st.error("Invalid credentials.")

# --- MAIN APPLICATION DASHBOARD ---
else:
    # --- SIDEBAR TOGGLE ---
    cols = st.columns([0.1, 0.8, 0.1])
    with cols[1]:
        if st.session_state.sidebar_hidden:
            if st.button("▶ Open Sidebar", use_container_width=True):
                st.session_state.sidebar_hidden = False
                st.rerun()
        else:
            if st.button("◀ Close Sidebar", use_container_width=True):
                st.session_state.sidebar_hidden = True
                st.rerun()

    # --- SIDEBAR (PROFILE & EXTRAS) ---
    if not st.session_state.sidebar_hidden:
        with st.sidebar:
            current_profile = db.get_profile(st.session_state.username)

            prof_col1, prof_col2 = st.columns([1, 2])
        with prof_col1:
            if current_profile.get("profile_pic"):
                st.image(base64.b64decode(current_profile["profile_pic"]), use_container_width=True)
            else:
                st.markdown("### 👤")
        with prof_col2:
            st.markdown(f"**{st.session_state.username}**")
            st.caption(f"⭐ {current_profile.get('score', 0)} XP")

        with st.expander("📸 Change Profile Photo"):
            pic_upload = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
            if pic_upload and st.button("Save Photo", use_container_width=True):
                b64_img = base64.b64encode(pic_upload.getvalue()).decode('utf-8')
                db.update_profile_pic(st.session_state.username, b64_img)
                st.success("Photo updated!")
                st.rerun()

        st.markdown("---")

        # --- FEATURE 1: LEADERBOARD ---
        st.markdown("🏆 **Contribution Count**")
        leaders = db.get_leaderboard()
        for idx, leader in enumerate(leaders):
            medal = "🥇" if idx == 0 else "🥈" if idx == 1 else "🥉" if idx == 2 else "🎓"
            st.markdown(f"{medal} **{leader['username']}** - {leader['score']} XP")

        st.markdown("---")

        # --- FEATURE 2: POMODORO TIMER (JS Injection) ---
        st.markdown("⏱️ **Focus Room**")
        pomodoro_html = """
        <div style="text-align: center; color: #f8fafc; font-family: sans-serif; background: #1e293b; padding: 15px; border-radius: 12px; border: 1px solid #334155;">
            <h2 id="time" style="margin: 0; font-size: 2rem; color: #818cf8;">25:00</h2>
            <div style="margin-top: 10px;">
                <button onclick="startTimer(25)" style="background: #4f46e5; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;">Work</button>
                <button onclick="startTimer(5)" style="background: #0ea5e9; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;">Rest</button>
            </div>
            <script>
                let timerInterval;
                function startTimer(minutes) {
                    clearInterval(timerInterval);
                    let time = minutes * 60;
                    const display = document.getElementById('time');
                    timerInterval = setInterval(function () {
                        let min = parseInt(time / 60, 10);
                        let sec = parseInt(time % 60, 10);
                        min = min < 10 ? "0" + min : min;
                        sec = sec < 10 ? "0" + sec : sec;
                        display.textContent = min + ":" + sec;
                        if (--time < 0) {
                            clearInterval(timerInterval);
                            display.textContent = "Time's up!";
                        }
                    }, 1000);
                }
            </script>
        </div>
        """
        components.html(pomodoro_html, height=130)

        st.markdown("---")
        st.markdown("**⚙️ My Learning Profile**")
        available_subjects = db.get_subjects()

        my_strengths = st.multiselect("I am strong in:", available_subjects,
                                      default=current_profile.get("strengths", []))
        my_weaknesses = st.multiselect("I need help with:", available_subjects,
                                       default=current_profile.get("weaknesses", []))

        if st.button("Update Skills", use_container_width=True):
            db.update_profile(st.session_state.username, my_strengths, my_weaknesses)
            st.success("Skills saved!")

        with st.expander("➕ Add Missing Subject"):
            new_sub_sidebar = st.text_input("New Subject Name:")
            if st.button("Add to Platform", use_container_width=True):
                if new_sub_sidebar:
                    db.add_subject(new_sub_sidebar)
                    st.success(f"Added {new_sub_sidebar}!")
                    st.rerun()

        st.markdown("---")
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.active_chat = None
            st.rerun()

    st.markdown("<h2 style='color: #818cf8;'>Nexus Dashboard</h2>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["📚 Solo Study Engine", "🔒 Private Peer Hubs", "🎯 Peer Matchmaking"])

    # === TAB 1: SOLO STUDY ENGINE ===
    with tab1:
        st.markdown("### Your Personal AI Tutor")
        st.write("Turn unstructured notes into actionable study materials.")

        input_method = st.radio("1. Choose Input Format:", ["📸 Image (PNG/JPG)", "📝 Paste Text", "📄 Document (.docx)"],
                                horizontal=True)
        raw_text_data = ""

        if input_method == "📸 Image (PNG/JPG)":
            uploaded_file = st.file_uploader("Upload Notes", type=['png', 'jpg', 'jpeg'])
            if uploaded_file:
                if st.button("Transcribe Image"):
                    with st.spinner("AI is reading your handwriting..."):
                        st.session_state['temp_notes'] = ce.process_image_notes(Image.open(uploaded_file))
                        st.rerun()

            if st.session_state.get('temp_notes'):
                st.success("Handwriting transcribed successfully!")
                st.session_state['temp_notes'] = st.text_area("Review & Edit Transcribed Text:",
                                                              value=st.session_state['temp_notes'], height=200)

        elif input_method == "📄 Document (.docx)":
            uploaded_file = st.file_uploader("Upload Word Doc", type=['docx'])
            if uploaded_file:
                if st.button("Extract Document"):
                    st.session_state['temp_notes'] = ce.extract_text_from_docx(uploaded_file)
                    st.rerun()

            if st.session_state.get('temp_notes'):
                st.success("Document loaded!")
                st.session_state['temp_notes'] = st.text_area("Review & Edit Document Text:",
                                                              value=st.session_state['temp_notes'], height=200)

        else:
            st.session_state['temp_notes'] = st.text_area("Paste Notes:", value=st.session_state.get('temp_notes', ''),
                                                          height=200)

        st.markdown("---")
        output_format = st.radio("2. Choose Export Format:",
                                 ["Study Guide (Text/PDF)", "PPT Presentation", "Important Q&A"], horizontal=True)

        if st.button("Generate Material", type="primary"):
            notes_to_process = st.session_state.get('temp_notes', '')
            if len(notes_to_process) > 10:
                with st.spinner(f"Generating your {output_format}..."):
                    result = ce.format_for_export(notes_to_process, output_format)

                    if output_format == "Study Guide (Text/PDF)":
                        with st.container(border=True):
                            st.markdown(result)
                        try:
                            pdf_bytes = ce.generate_pdf(result)
                            st.download_button(label="📥 Download Guide (.pdf)", data=pdf_bytes,
                                               file_name="Nexus_Study_Guide.pdf", mime="application/pdf")
                        except Exception as e:
                            st.error("Failed to generate PDF. You can still copy the text above!")

                    elif output_format == "PPT Presentation":
                        ppt_file = sm.create_presentation(result)
                        st.success("Presentation ready!")
                        st.download_button("📥 Download Deck (.pptx)", ppt_file, file_name="Nexus_Deck.pptx")

                    elif output_format == "Important Q&A":
                        st.success("Q&A Ready! Click the bars to reveal the answers.")
                        for idx, card in enumerate(result):
                            with st.expander(f"❓ **Q:** {card['question']}"):
                                st.info(f"**Answer:** {card['answer']}")
            else:
                st.warning("Please provide notes first.")

    # === TAB 2: PRIVATE PEER HUBS ===
    with tab2:
        st.markdown("### 🔒 Secure Study Groups")
        st.write("Join or create a private hub to collaborate exclusively with your peers.")

        user_hubs = db.get_user_hubs(st.session_state.username)

        col1, col2 = st.columns([1, 1])
        with col1:
            with st.expander("➕ Create a New Hub"):
                new_hub_name = st.text_input("Hub Name (e.g., 'Section B CS')")
                if st.button("Create Hub"):
                    if new_hub_name:
                        code = db.create_hub(new_hub_name, st.session_state.username)
                        st.success(f"Hub created! Your access code is: **{code}**")
                        st.rerun()
                    else:
                        st.warning("Enter a name.")
        with col2:
            with st.expander("🔑 Join Existing Hub"):
                join_code = st.text_input("Enter 6-Character Access Code:")
                if st.button("Join Hub"):
                    success, msg = db.join_hub(join_code, st.session_state.username)
                    if success:
                        st.success(f"Successfully joined {msg}!")
                        st.rerun()
                    else:
                        st.error(msg)

        st.markdown("---")

        if not user_hubs:
            st.info("👋 You aren't in any hubs yet. Create one or ask a classmate for their access code!")
        else:
            hub_options = {f"{name} (Code: {code})": code for code, name in user_hubs.items()}
            selected_hub_display = st.selectbox("📂 Active Workspace:", list(hub_options.keys()))
            active_hub_code = hub_options[selected_hub_display]

            st.markdown(f"#### 🚀 Workspace: {selected_hub_display.split(' (')[0]}")

            hub_tab1, hub_tab2 = st.tabs(["📝 Shared Notes & Guides", "💬 Group Chat"])

            with hub_tab1:
                available_subjects = db.get_subjects()

                subj_col1, subj_col2 = st.columns([3, 1])
                with subj_col1:
                    selected_subject = st.selectbox("📚 Subject:", available_subjects, key="hub_subj")
                with subj_col2:
                    with st.expander("➕ New Subject"):
                        new_sub_hub = st.text_input("Subject Name:", key="new_sub_hub")
                        if st.button("Add", key="btn_new_sub_hub"):
                            if new_sub_hub:
                                db.add_subject(new_sub_hub)
                                st.rerun()

                existing_topics = db.get_all_topics(active_hub_code, selected_subject)

                tc1, tc2 = st.columns(2)
                with tc1:
                    topic_mode = st.radio("Topic Action:", ["Use Existing Topic", "Create New Topic"], horizontal=True,
                                          key="hub_radio")
                with tc2:
                    if topic_mode == "Use Existing Topic":
                        if existing_topics:
                            selected_topic = st.selectbox("Choose Existing Topic:", existing_topics, key="hub_top")
                        else:
                            st.info("No topics exist yet.")
                            selected_topic = None
                    else:
                        selected_topic = st.text_input("Enter New Topic Name:")

                contribution_type = st.radio("Contribute via:", ["📝 Paste Text", "📸 Upload Image Note"],
                                             horizontal=True)
                community_notes = ""
                img_base64 = None

                if contribution_type == "📝 Paste Text":
                    community_notes = st.text_area(
                        f"Paste your notes for '{selected_topic if selected_topic else 'this topic'}':", height=100,
                        key="hub_notes")
                else:
                    uploaded_file = st.file_uploader("Upload a photo of your notes", type=['png', 'jpg', 'jpeg'],
                                                     key="hub_img")
                    if uploaded_file:
                        st.image(uploaded_file, caption="Image Preview", width=400)
                        img_base64 = base64.b64encode(uploaded_file.getvalue()).decode('utf-8')
                        st.info("🧠 When you click contribute, the AI will transcribe this image in the background.")

                if st.button("⬆️ Contribute to Hub"):
                    if selected_subject and selected_topic:
                        if contribution_type == "📝 Paste Text" and community_notes:
                            db.add_community_note(active_hub_code, selected_subject, selected_topic, community_notes,
                                                  st.session_state.username)
                            st.success("Note added privately! (+10 XP)")
                            st.rerun()
                        elif contribution_type == "📸 Upload Image Note" and uploaded_file:
                            with st.spinner("Uploading and transcribing your image..."):
                                image = Image.open(uploaded_file)
                                transcription = ce.process_image_notes(image)
                                db.add_community_note(active_hub_code, selected_subject, selected_topic, transcription,
                                                      st.session_state.username, image_base64=img_base64)
                                st.success("Image uploaded and transcribed successfully! (+10 XP)")
                                st.rerun()
                        else:
                            st.warning("Please provide notes or upload an image.")
                    else:
                        st.warning("Ensure all fields are filled.")

                st.markdown("---")
                if selected_subject and selected_topic:
                    all_notes = db.get_topic_notes(active_hub_code, selected_subject, selected_topic)
                    if not all_notes:
                        st.info("No notes here yet.")
                    else:
                        st.markdown(f"#### 📖 Hub Notes ({len(all_notes)} Contributions)")
                        notes_container = st.container(height=400)
                        with notes_container:
                            for note in all_notes:
                                with st.container(border=True):
                                    note_col, del_col = st.columns([10, 1])
                                    with note_col:
                                        display_time = note['timestamp'][:16]
                                        st.markdown(
                                            f"**👤 {note['author']}** <span style='color:gray; font-size:0.8em;'>{display_time}</span>",
                                            unsafe_allow_html=True)
                                        if note.get("image_data"):
                                            img_bytes = base64.b64decode(note["image_data"])
                                            st.image(img_bytes, use_container_width=True)
                                            with st.expander("View AI Transcription"):
                                                st.write(note['content'])
                                        else:
                                            st.write(note['content'])
                                    with del_col:
                                        if note['author'] == st.session_state.username:
                                            if st.button("🗑️", key=f"del_{note['timestamp']}"):
                                                db.delete_community_note(active_hub_code, selected_subject,
                                                                         selected_topic, note['timestamp'],
                                                                         st.session_state.username)
                                                st.rerun()

                        st.markdown("---")

                        # --- FEATURE 3: LAST MINUTE REVISION SLIDES ---
                        st.markdown(f"#### 🧠 Synthesize '{selected_topic}'")
                        if st.button("Generate Master Guide & Revision Slides", type="primary"):
                            with st.spinner(
                                    f"Synthesizing {len(all_notes)} private contributions and building slide deck..."):
                                raw_strings = [entry['content'] for entry in all_notes]

                                # 1. Generate the Text Guide
                                master_guide = ce.process_collab_notes(raw_strings)

                                # 2. Generate the PowerPoint Slides invisibly!
                                slide_data = ce.format_for_export(master_guide, "PPT Presentation")
                                ppt_file = sm.create_presentation(slide_data)

                                st.success("Synthesized successfully! Grab your slides below.")

                                # Display the download button
                                st.download_button(
                                    label="📥 Download Last-Minute Revision Slides (.pptx)",
                                    data=ppt_file,
                                    file_name=f"{selected_topic.replace(' ', '_')}_Revision.pptx",
                                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                                )

                                # Display the text below it
                                with st.container(border=True):
                                    st.markdown(master_guide)

            with hub_tab2:
                st.markdown(f"### 💬 {selected_hub_display.split(' (')[0]} Chat")
                chat_container = st.container(height=400)
                messages = db.get_hub_chat(active_hub_code)

                with chat_container:
                    if not messages:
                        st.caption("Say hello to your study group!")
                    for msg in messages:
                        is_me = msg["sender"] == st.session_state.username
                        user_avatar = get_avatar(msg["sender"])

                        with st.chat_message("user" if is_me else "assistant", avatar=user_avatar):
                            msg_col, del_col = st.columns([10, 1])
                            with msg_col:
                                display_time = msg['timestamp'][:16]
                                st.markdown(
                                    f"**{msg['sender']}** <span style='color:gray; font-size:0.8em;'>{display_time}</span>",
                                    unsafe_allow_html=True)
                                st.write(msg['message'])
                            with del_col:
                                if is_me:
                                    if st.button("🗑️", key=f"del_hub_chat_{msg['timestamp']}"):
                                        db.delete_hub_chat_message(active_hub_code, msg['timestamp'],
                                                                   st.session_state.username)
                                        st.rerun()

                new_hub_msg = st.chat_input("Message the group...", key="hub_chat_input")
                if new_hub_msg:
                    db.add_hub_chat_message(active_hub_code, st.session_state.username, new_hub_msg)
                    st.rerun()

    # === TAB 3: PEER MATCHMAKING ===
    with tab3:
        st.markdown("### Smart Study Partners")
        st.write("Find classmates who excel in the topics you find difficult, and collaborate in real-time.")

        my_profile = db.get_profile(st.session_state.username)
        if not my_profile.get("weaknesses"):
            st.info("👈 Please set your learning profile in the sidebar to get matched with peers!")
        else:
            matches = db.find_matches(st.session_state.username)
            if not matches:
                st.warning("No perfect matches found yet. Check back when more students join!")
            else:
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.markdown("**🤝 Your Matches**")
                    for match in matches:
                        with st.container(border=True):
                            match_avatar = get_avatar(match['username'])
                            if match_avatar != "👤":
                                st.image(match_avatar, width=50)

                            st.markdown(f"#### 👤 {match['username']}")
                            st.caption(f"**Can teach you:** {', '.join(match['can_teach'])}")
                            st.caption(f"**They need help with:** {', '.join(match['their_needs'])}")
                            if st.button(f"Chat with {match['username']}", key=f"chat_{match['username']}",
                                         use_container_width=True):
                                st.session_state.active_chat = match['username']
                                st.rerun()
                with col2:
                    if st.session_state.active_chat:
                        chat_partner = st.session_state.active_chat
                        st.markdown(f"**💬 Study Room with {chat_partner}**")

                        history = db.get_chat_history(st.session_state.username, chat_partner)
                        chat_container = st.container(height=350)
                        with chat_container:
                            if not history:
                                st.caption("Say hello and start collaborating!")
                            for msg in history:
                                is_me = msg["sender"] == st.session_state.username
                                dm_avatar = get_avatar(msg["sender"])

                                with st.chat_message("user" if is_me else "assistant", avatar=dm_avatar):
                                    display_time = msg['timestamp'][:16]
                                    st.markdown(
                                        f"**{msg['sender']}** <span style='color:gray; font-size:0.8em;'>{display_time}</span>",
                                        unsafe_allow_html=True)
                                    st.write(msg['message'])

                        new_message = st.chat_input(f"Message {chat_partner}...", key="dm_input")
                        if new_message:
                            db.send_message(st.session_state.username, chat_partner, new_message)
                            st.rerun()
                    else:
                        with st.container(border=True):
                            st.info("Select a match on the left to open the collaboration room.")