from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///students.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    income_before = Column(Integer, nullable=False)
    income_after = Column(Integer, nullable=False)
    course_start_date = Column(Date, nullable=False)
    course_end_date = Column(Date, nullable=False)

# Criação da tabela
Base.metadata.create_all(engine)

# Configuração da sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)