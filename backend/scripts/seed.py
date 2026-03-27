from sqlalchemy import select

from app.core.security import hash_password
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models.scientific import Axis, News
from app.models.user import MemberProfile, User, UserRole


def run() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        admin_email = "admin@lias.local"
        admin = db.scalar(select(User).where(User.email == admin_email))
        if not admin:
            admin = User(
                email=admin_email,
                password_hash=hash_password("Admin@12345"),
                role=UserRole.ADMIN,
                is_active=True,
            )
            db.add(admin)
            db.flush()
            db.add(
                MemberProfile(
                    user_id=admin.id,
                    first_name="Admin",
                    last_name="LIAS",
                    professional_email=admin_email,
                    grade="Responsable",
                )
            )

        for axis_title in ["IA et Data", "Systemes Distribues", "Ingenierie Logicielle"]:
            exists = db.scalar(select(Axis).where(Axis.title == axis_title))
            if not exists:
                db.add(Axis(title=axis_title, description=f"Axe {axis_title}"))

        welcome = db.scalar(select(News).where(News.title == "Lancement de la plateforme LIAS"))
        if not welcome:
            db.add(
                News(
                    title="Lancement de la plateforme LIAS",
                    content="La plateforme institutionnelle et scientifique du laboratoire LIAS est disponible.",
                    is_published=True,
                )
            )

        db.commit()
        print("Seed completed. Admin: admin@lias.local / Admin@12345")
    finally:
        db.close()


if __name__ == "__main__":
    run()
