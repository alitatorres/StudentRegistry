from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Student, Base  # Certifique-se de que Student e Base estão definidos em models.py

DATABASE_URL = "sqlite:///students.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_student(session, name, birth_date, cpf, email, phone, income_before, income_after, course_start_date, course_end_date):
    # Verificar se o CPF já está cadastrado
    existing_student = session.query(Student).filter(Student.cpf == cpf).first()
    if existing_student:
        raise ValueError("O CPF já está cadastrado.")

    # Criar novo aluno
    new_student = Student(
        name=name,
        birth_date=birth_date,
        cpf=cpf,
        email=email,
        phone=phone,
        income_before=income_before,
        income_after=income_after,
        course_start_date=course_start_date,
        course_end_date=course_end_date
    )
    session.add(new_student)
    session.commit()
    print("Aluno cadastrado com sucesso!")

def list_students(session):
    students = session.query(Student).all()
    for student in students:
        print(f"Nome: {student.name}, CPF: {student.cpf}, Curso: {student.course_start_date} - {student.course_end_date}")

def main():
    # Criar o banco de dados e a tabela
    Base.metadata.create_all(engine)

    # Criar uma nova sessão
    session = SessionLocal()

    try:
        while True:
            print("\nGerenciamento de Alunos")
            print("1. Adicionar aluno")
            print("2. Listar alunos")
            print("3. Sair")

            choice = input("Escolha uma opção: ")

            if choice == "1":
                name = input("Nome: ")
                birth_date = input("Data de nascimento (YYYY-MM-DD): ")
                cpf = input("CPF: ")
                email = input("Email: ")
                phone = input("Número de telefone: ")
                income_before = int(input("Renda antes do curso: "))
                income_after = int(input("Renda após o curso: "))
                course_start_date = input("Data de início do curso (YYYY-MM-DD): ")
                course_end_date = input("Data de fim do curso (YYYY-MM-DD): ")

                try:
                    create_student(
                        session,
                        name,
                        birth_date,
                        cpf,
                        email,
                        phone,
                        income_before,
                        income_after,
                        course_start_date,
                        course_end_date
                    )
                except ValueError as e:
                    print(f"Erro: {e}")

            elif choice == "2":
                list_students(session)

            elif choice == "3":
                break

            else:
                print("Opção inválida. Tente novamente.")

    finally:
        session.close()

if __name__ == "__main__":
    main()