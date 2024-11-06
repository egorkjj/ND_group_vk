from sqlalchemy import create_engine, Column, Integer, Text, Boolean, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from environs import Env

env = Env()
env.read_env(".env")
user_db = env.str("DB_USER")
passw = env.str("DB_PASSWORD")
host = env.str("DB_HOST")
name = env.str("DB_NAME")


DATABASE_URL = f"postgresql+psycopg2://{user_db}:{passw}{host}/{name}"

# Создание объекта Engine
engine = create_engine(DATABASE_URL)

# Создание базового класса для моделей
Base = declarative_base()



class Applications_Avito(Base):
    __tablename__ = "appl_avito"
    id = Column(BigInteger, autoincrement=True, primary_key=True)
    avito_id = Column(BigInteger, nullable=True, unique = True)
    telegram_id = Column(BigInteger, nullable=True, unique=True)
    quest1 = Column(Text, nullable=True)
    quest2 = Column(Text, nullable=True)
    quest3 = Column(Text, nullable=True)
    quest4 = Column(Text, nullable=True)
    quest5 = Column(Text, nullable=True)
    quest6 = Column(Text, nullable=True)
    quest7 = Column(Text, nullable=True)
    task_path = Column(Text, nullable=True)
    accepted = Column(Boolean, nullable=True)


class States_VK(Base):
    __tablename__ = "states_vk"
    id = Column(BigInteger, autoincrement=True, primary_key=True)
    vk_id = Column(BigInteger, nullable=True, unique = True)
    state = Column(Text, nullable=True)


def get_state(vk_id) -> str:
    Session = sessionmaker()
    session = Session(bind = engine)
    curr = session.query(States_VK).filter(States_VK.vk_id == vk_id).first()
    session.close()
    return "quest0" if curr is None else curr.state


def set_state(vk_id, state) -> None:
    Session = sessionmaker()
    session = Session(bind = engine)
    curr = session.query(States_VK).filter(States_VK.vk_id == vk_id).first()
    if curr is None:
        new = States_VK(vk_id = vk_id, state = state)
        session.add(new)
    else:
        curr.state = state
    session.commit()
    session.close()


def upload_database(vk_id, data, state) -> None:
    if state == "quest0":
        return
    
    else:
        Session = sessionmaker()
        session = Session(bind = engine)
        if state == "quest1":
            new = Applications_Avito(avito_id = vk_id, quest1 = data)
            session.add(new)
        else:
            curr = session.query(Applications_Avito).filter(Applications_Avito.avito_id == vk_id).first()
            if state == "quest2":
                curr.quest2 = data
            elif state == "quest3":
                curr.quest3 = data
            elif state == "quest4":
                curr.quest4 = data
            elif state == "quest5":
                curr.quest5 = data
            elif state == "quest6":
                curr.quest6 = data
            elif state == "quest7":
                curr.quest7 = data
                
        session.commit()
        session.close()

