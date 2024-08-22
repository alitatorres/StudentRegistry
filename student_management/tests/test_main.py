import pytest
from datetime import datetime
from main import create_student, get_student_by_cpf, get_students

# Configuração para testar com um banco de dados temporário
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Student

# Criar uma conexão com um banco de dados SQLite em memória para testes
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criar as tabelas no banco de dados temporário
Base.metadata.create_all(engine)

# Fixture para fornecer uma sessão de banco de dados para cada teste
@pytest.fixture(scope="function")
def db_session():
    session = SessionLocal()
    yield session
    session.close()

# Testar a criação de um novo aluno
def test_create_student(db_session):
    student_data = {
        "name": "Alice",
        "birth_date": datetime.strptime("2000-01-01", "%Y-%m-%d"),
        "cpf": "12345678900",
        "email": "alice@example.com",
        "phone": "555-1234",
        "income_before": 1000,
        "income_after": 2000,
        "course_start_date": datetime.strptime("2024-01-01", "%Y-%m-%d"),
        "course_end_date": datetime.strptime("2024-12-31", "%Y-%m-%d")
    }
    create_student(db_session, **student_data)
    student = get_student_by_cpf(db_session, "12345678900")
    assert student is not None
    assert student.name == "Alice"

# Testar a criação de um aluno com CPF duplicado
def test_create_student_duplicate_cpf(db_session):
    student_data = {
        "name": "Bob",
        "birth_date": datetime.strptime("1995-05-15", "%Y-%m-%d"),
        "cpf": "98765432100",
        "email": "bob@example.com",
        "phone": "555-5678",
        "income_before": 1500,
        "income_after": 2500,
        "course_start_date": datetime.strptime("2024-02-01", "%Y-%m-%d"),
        "course_end_date": datetime.strptime("2024-11-30", "%Y-%m-%d")
    }
    create_student(db_session, **student_data)
    with pytest.raises(Exception):
        create_student(db_session, **student_data)  # Tentativa de criar o mesmo aluno novamente

# Testar a criação de um aluno com curso duplicado
def test_create_student_duplicate_course(db_session):
    student_data1 = {
        "name": "Charlie",
        "birth_date": datetime.strptime("1990-07-22", "%Y-%m-%d"),
        "cpf": "55566677700",
        "email": "charlie@example.com",
        "phone": "555-8765",
        "income_before": 1200,
        "income_after": 2200,
        "course_start_date": datetime.strptime("2024-03-01", "%Y-%m-%d"),
        "course_end_date": datetime.strptime("2024-08-31", "%Y-%m-%d")
    }
    student_data2 = {
        "name": "Dana",
        "birth_date": datetime.strptime("1985-12-10", "%Y-%m-%d"),
        "cpf": "66655544400",
        "email": "dana@example.com",
        "phone": "555-4321",
        "income_before": 1100,
        "income_after": 2100,
        "course_start_date": datetime.strptime("2024-03-01", "%Y-%m-%d"),
        "course_end_date": datetime.strptime("2024-08-31", "%Y-%m-%d")
    }
    create_student(db_session, **student_data1)
    create_student(db_session, **student_data2)
    students = get_students(db_session)
    assert len(students) == 2