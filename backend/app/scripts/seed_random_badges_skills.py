# Script to assign random badges and random skills to all users for demo/hackathon
# Run: python backend/app/scripts/seed_random_badges_skills.py

import random
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User
from app.models.skill import Skill, UserSkill, SkillLevel
from app.models.badge import Badge

BADGE_TYPES = ["mentor", "learned", "rated_5star"]

# Example skills to assign randomly if not enough in DB
EXAMPLE_SKILLS = [
    "Python", "React", "FastAPI", "UI/UX", "SQL", "Docker", "Kubernetes", "Node.js", "Figma", "Tailwind"
]


def main():
    db: Session = SessionLocal()
    users = db.query(User).all()
    skills = db.query(Skill).all()
    if not skills:
        # Create example skills if DB is empty
        for name in EXAMPLE_SKILLS:
            s = Skill(name=name, category="General")
            db.add(s)
        db.commit()
        skills = db.query(Skill).all()

    for user in users:
        # Assign random skills_offered and skills_wanted (as lists)
        offered = random.sample(skills, k=min(3, len(skills)))
        wanted = random.sample(skills, k=min(2, len(skills)))
        user.skills_offered = [s.name for s in offered]
        user.skills_wanted = [s.name for s in wanted]
        db.add(user)
        # Add UserSkill entries for offered
        for s in offered:
            if not db.query(UserSkill).filter_by(user_id=user.id, skill_id=s.id, type="offered").first():
                db.add(UserSkill(user_id=user.id, skill_id=s.id, type="offered", level=SkillLevel.beginner))
        for s in wanted:
            if not db.query(UserSkill).filter_by(user_id=user.id, skill_id=s.id, type="wanted").first():
                db.add(UserSkill(user_id=user.id, skill_id=s.id, type="wanted", level=SkillLevel.beginner))
        # Assign random badges
        for _ in range(random.randint(1, 3)):
            badge_type = random.choice(BADGE_TYPES)
            skill = random.choice(skills)
            db.add(Badge(user_id=user.id, skill_id=skill.id, badge_type=badge_type))
    db.commit()
    print(f"Seeded random badges and skills for {len(users)} users.")

if __name__ == "__main__":
    main()
