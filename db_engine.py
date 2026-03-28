import json
import os
import random
import string
from datetime import datetime

DB_FILE = 'nexus_db.json'


def init_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w') as f:
            json.dump({
                "users": {}, "hubs": {}, "community_notes": {},
                "profiles": {}, "chats": {}, "hub_chats": {},
                "subjects": ["C Programming", "Data Structures", "Algorithms", "Machine Learning", "Quantum Mechanics",
                             "Linear Algebra", "Web Development"]
            }, f)
    else:
        with open(DB_FILE, 'r+') as f:
            db = json.load(f)
            updated = False
            for key in ["users", "hubs", "community_notes", "profiles", "chats", "hub_chats"]:
                if key not in db:
                    db[key] = {}
                    updated = True

            if "subjects" not in db:
                db["subjects"] = ["C Programming", "Data Structures", "Algorithms", "Machine Learning",
                                  "Quantum Mechanics", "Linear Algebra", "Web Development"]
                updated = True

            # Upgrade existing profiles to have a score
            for user, prof in db.get("profiles", {}).items():
                if "score" not in prof:
                    prof["score"] = 0
                    updated = True

            if updated:
                f.seek(0)
                json.dump(db, f, indent=4)
                f.truncate()


def get_subjects():
    init_db()
    with open(DB_FILE, 'r') as f:
        db = json.load(f)
        return db.get("subjects", [])


def add_subject(new_subject):
    init_db()
    new_subject = new_subject.strip()
    with open(DB_FILE, 'r+') as f:
        db = json.load(f)
        existing_lower = [s.lower() for s in db.get("subjects", [])]
        if new_subject and new_subject.lower() not in existing_lower:
            db["subjects"].append(new_subject)
            f.seek(0)
            json.dump(db, f, indent=4)
            f.truncate()
            return True
        return False


def create_user(username, password):
    init_db()
    with open(DB_FILE, 'r+') as f:
        db = json.load(f)
        if username in db["users"]:
            return False
        db["users"][username] = password
        # Initialize score to 0
        db["profiles"][username] = {"strengths": [], "weaknesses": [], "profile_pic": None, "score": 0}
        f.seek(0)
        json.dump(db, f, indent=4)
        return True


def login_user(username, password):
    init_db()
    with open(DB_FILE, 'r') as f:
        db = json.load(f)
        return db["users"].get(username) == password


def update_profile(username, strengths, weaknesses):
    init_db()
    with open(DB_FILE, 'r+') as f:
        db = json.load(f)
        if username not in db["profiles"]:
            db["profiles"][username] = {"profile_pic": None, "score": 0}
        db["profiles"][username]["strengths"] = strengths
        db["profiles"][username]["weaknesses"] = weaknesses
        f.seek(0)
        json.dump(db, f, indent=4)
        f.truncate()


def update_profile_pic(username, image_base64):
    init_db()
    with open(DB_FILE, 'r+') as f:
        db = json.load(f)
        if username not in db["profiles"]:
            db["profiles"][username] = {"strengths": [], "weaknesses": [], "score": 0}
        db["profiles"][username]["profile_pic"] = image_base64
        f.seek(0)
        json.dump(db, f, indent=4)
        f.truncate()


def get_profile(username):
    init_db()
    with open(DB_FILE, 'r') as f:
        db = json.load(f)
        return db["profiles"].get(username, {"strengths": [], "weaknesses": [], "profile_pic": None, "score": 0})


def get_leaderboard():
    """Returns top 5 users based on contribution score."""
    init_db()
    with open(DB_FILE, 'r') as f:
        db = json.load(f)
        users = [{"username": k, "score": v.get("score", 0)} for k, v in db.get("profiles", {}).items()]
        # Sort by score descending
        return sorted(users, key=lambda x: x["score"], reverse=True)[:5]


def find_matches(current_user):
    init_db()
    with open(DB_FILE, 'r') as f:
        db = json.load(f)

    my_profile = db["profiles"].get(current_user, {"strengths": [], "weaknesses": []})
    my_weaknesses = set(my_profile.get("weaknesses", []))

    matches = []
    for user, profile in db["profiles"].items():
        if user == current_user:
            continue

        their_strengths = set(profile.get("strengths", []))
        skills_they_can_teach_me = my_weaknesses.intersection(their_strengths)

        if skills_they_can_teach_me:
            matches.append({
                "username": user,
                "can_teach": list(skills_they_can_teach_me),
                "their_needs": profile.get("weaknesses", [])
            })
    return matches


def get_chat_history(user1, user2):
    init_db()
    room_id = tuple(sorted([user1, user2]))
    room_key = f"{room_id[0]}_{room_id[1]}"
    with open(DB_FILE, 'r') as f:
        db = json.load(f)
        return db["chats"].get(room_key, [])


def send_message(sender, receiver, message):
    init_db()
    room_id = tuple(sorted([sender, receiver]))
    room_key = f"{room_id[0]}_{room_id[1]}"
    with open(DB_FILE, 'r+') as f:
        db = json.load(f)
        if room_key not in db["chats"]:
            db["chats"][room_key] = []
        db["chats"][room_key].append({"sender": sender, "message": message, "timestamp": str(datetime.now())})
        f.seek(0)
        json.dump(db, f, indent=4)
        f.truncate()


def create_hub(hub_name, creator):
    init_db()
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    with open(DB_FILE, 'r+') as f:
        db = json.load(f)
        while code in db["hubs"]:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

        db["hubs"][code] = {"name": hub_name, "creator": creator, "members": [creator]}
        db["community_notes"][code] = {}
        db["hub_chats"][code] = []

        f.seek(0)
        json.dump(db, f, indent=4)
        f.truncate()
    return code


def join_hub(hub_code, username):
    init_db()
    hub_code = hub_code.strip().upper()
    with open(DB_FILE, 'r+') as f:
        db = json.load(f)
        if hub_code in db["hubs"]:
            if username not in db["hubs"][hub_code]["members"]:
                db["hubs"][hub_code]["members"].append(username)
                f.seek(0)
                json.dump(db, f, indent=4)
                f.truncate()
            return True, db["hubs"][hub_code]["name"]
        return False, "Invalid Code"


def get_user_hubs(username):
    init_db()
    with open(DB_FILE, 'r') as f:
        db = json.load(f)
        user_hubs = {}
        for code, hub_data in db["hubs"].items():
            if username in hub_data["members"]:
                user_hubs[code] = hub_data["name"]
        return user_hubs


def get_hub_chat(hub_code):
    init_db()
    with open(DB_FILE, 'r') as f:
        db = json.load(f)
        return db.get("hub_chats", {}).get(hub_code, [])


def add_hub_chat_message(hub_code, sender, message):
    init_db()
    with open(DB_FILE, 'r+') as f:
        db = json.load(f)
        if "hub_chats" not in db:
            db["hub_chats"] = {}
        if hub_code not in db["hub_chats"]:
            db["hub_chats"][hub_code] = []

        db["hub_chats"][hub_code].append({
            "sender": sender,
            "message": message,
            "timestamp": str(datetime.now())
        })

        if len(db["hub_chats"][hub_code]) > 100:
            db["hub_chats"][hub_code] = db["hub_chats"][hub_code][-100:]

        f.seek(0)
        json.dump(db, f, indent=4)
        f.truncate()


def delete_hub_chat_message(hub_code, timestamp, sender):
    init_db()
    with open(DB_FILE, 'r+') as f:
        db = json.load(f)
        if "hub_chats" in db and hub_code in db["hub_chats"]:
            db["hub_chats"][hub_code] = [
                msg for msg in db["hub_chats"][hub_code]
                if not (msg["sender"] == sender and msg["timestamp"] == timestamp)
            ]
            f.seek(0)
            json.dump(db, f, indent=4)
            f.truncate()
            return True
        return False


def add_community_note(hub_code, subject, topic, content, author, image_base64=None):
    init_db()
    with open(DB_FILE, 'r+') as f:
        db = json.load(f)
        if subject not in db["community_notes"][hub_code]:
            db["community_notes"][hub_code][subject] = {}
        if topic not in db["community_notes"][hub_code][subject]:
            db["community_notes"][hub_code][subject][topic] = []

        db["community_notes"][hub_code][subject][topic].append({
            "author": author,
            "content": content,
            "image_data": image_base64,
            "timestamp": str(datetime.now())
        })

        # INCREMENT THE AUTHOR'S SCORE
        if author in db["profiles"]:
            db["profiles"][author]["score"] = db["profiles"][author].get("score", 0) + 10

        f.seek(0)
        json.dump(db, f, indent=4)
        f.truncate()


def get_all_topics(hub_code, subject):
    init_db()
    with open(DB_FILE, 'r') as f:
        db = json.load(f)
        if subject in db["community_notes"].get(hub_code, {}):
            return list(db["community_notes"][hub_code][subject].keys())
        return []


def get_topic_notes(hub_code, subject, topic):
    init_db()
    with open(DB_FILE, 'r') as f:
        db = json.load(f)
        try:
            return db["community_notes"][hub_code][subject][topic]
        except KeyError:
            return []


def delete_community_note(hub_code, subject, topic, timestamp, author):
    init_db()
    with open(DB_FILE, 'r+') as f:
        db = json.load(f)
        try:
            notes = db["community_notes"][hub_code][subject][topic]
            db["community_notes"][hub_code][subject][topic] = [
                n for n in notes if not (n["author"] == author and n["timestamp"] == timestamp)
            ]

            # DECREMENT SCORE IF DELETED
            if author in db["profiles"]:
                db["profiles"][author]["score"] = max(0, db["profiles"][author].get("score", 0) - 10)

            f.seek(0)
            json.dump(db, f, indent=4)
            f.truncate()
            return True
        except KeyError:
            return False