# seed_data.py
# Script to populate the database with lots of users, skills, and user skills for testing
# Run: python backend/app/seed_data.py

from app.database import SessionLocal
from app.models.user import User
from app.models.skill import Skill, UserSkill, SkillLevel
from sqlalchemy.exc import IntegrityError
from passlib.hash import bcrypt
import random

# Sample data
NAMES = [
    "Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Heidi", "Ivan", "Judy",
    "Karl", "Liam", "Mallory", "Niaj", "Olivia", "Peggy", "Quentin", "Rupert", "Sybil", "Trent",
    "Uma", "Victor", "Wendy", "Xavier", "Yvonne", "Zara"
]
LOCATIONS = [
    "New York", "London", "Berlin", "Paris", "Tokyo", "Delhi", "Mumbai", "San Francisco", "Sydney", "Toronto"
]
CATEGORIES = [
    "Programming", "Design", "Marketing", "Writing", "Music", "Art", "Business", "Language", "Cooking", "Fitness"
]
SKILLS = [
    ("Python", "Programming"), ("JavaScript", "Programming"), ("UI Design", "Design"), ("SEO", "Marketing"),
    ("Copywriting", "Writing"), ("Guitar", "Music"), ("Painting", "Art"), ("Entrepreneurship", "Business"),
    ("Spanish", "Language"), ("Baking", "Cooking"), ("Yoga", "Fitness"), ("React", "Programming"),
    ("Photoshop", "Design"), ("Piano", "Music"), ("Public Speaking", "Business"), ("French", "Language")
]
AVAILABILITY = ["weekends", "weekdays", "evenings"]

PASSWORD = "test123"  # Easy password for all users

random.seed(42)

def hash_pw(pw):
    return bcrypt.hash(pw)

def main():
    db = SessionLocal()
    # Add skills
    for name, category in SKILLS:
        skill = Skill(name=name, category=category)
        db.merge(skill)
    db.commit()
    skills = db.query(Skill).all()
    # Add users
    for i in range(50):
        name = random.choice(NAMES) + str(i)
        email = f"user{i}@test.com"
        location = random.choice(LOCATIONS)
        availability = random.choice(AVAILABILITY)
        user = User(
            name=name,
            email=email,
            password_hash=hash_pw(PASSWORD),
            location=location,
            availability=availability,
            is_public=True,
            photo_url="https://placehold.co/64x64"
        )
        try:
            db.add(user)
            db.commit()
        except IntegrityError:
            db.rollback()
    users = db.query(User).all()
    # Assign random skills to users
    for user in users:
        offered = random.sample(skills, k=2)
        wanted = random.sample(skills, k=2)
        for skill in offered:
            us = UserSkill(user_id=user.id, skill_id=skill.id, type="offered", level=random.choice(list(SkillLevel)))
            db.merge(us)
        for skill in wanted:
            us = UserSkill(user_id=user.id, skill_id=skill.id, type="wanted", level=random.choice(list(SkillLevel)))
            db.merge(us)
    db.commit()
    print("Seeded 50 users, skills, and user skills. All passwords: test123")
    db.close()

if __name__ == "__main__":
    main()
