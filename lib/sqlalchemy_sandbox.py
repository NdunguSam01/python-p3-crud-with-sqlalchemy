#!/usr/bin/env python3

from datetime import datetime

from sqlalchemy import (create_engine, desc, func,
    CheckConstraint, PrimaryKeyConstraint, UniqueConstraint,
    Index, Column, DateTime, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    __table_args__ = (
        PrimaryKeyConstraint(
            'id',
            name='id_pk'),
        UniqueConstraint(
            'email',
            name='unique_email'),
        CheckConstraint(
            'grade BETWEEN 1 AND 12',
            name='grade_between_1_and_12')
    )

    Index('index_name', 'name')

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    email = Column(String(55))
    grade = Column(Integer())
    birthday = Column(DateTime())
    enrolled_date = Column(DateTime(), default=datetime.now())

    def __repr__(self):
        return f"Student {self.id}: " \
            + f"{self.name}, " \
            + f"Grade {self.grade}"

if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    Session= sessionmaker(bind=engine)
    session=Session()
    
    albert_einstein = Student(
        name="Albert Einstein",
        email="albert.einstein@zurich.edu",
        grade=6,
        birthday=datetime(
            year=1879,
            month=3,
            day=14
        ),
    )

    alan_turing = Student(
        name="Alan Turing",
        email="alan.turing@sherborne.edu",
        grade=11,
        birthday=datetime(
            year=1912,
            month=6,
            day=23
        ),
    )

    session.bulk_save_objects([albert_einstein, alan_turing])
    session.commit()

    print(f"New student ID is {albert_einstein.id}.")
    print(f"New student ID is {alan_turing.id}.")

    students = session.query(Student)
    print([student for student in students])

    #Selecting Only Certain Columns
    names = [name for name in session.query(Student.name)]
    print(names)

    #Ordering
    students_by_name = [student for student in session.query(Student.name).order_by(Student.name)]
    print(students_by_name)

    #Ordering by descending order
    students_by_grade_desc = [student for student in session.query(Student.name, Student.grade).order_by(desc(Student.grade))]
    print(students_by_grade_desc)

    #Limiting the result set to the first x records
    oldest_student = [student for student in session.query(Student.name, Student.birthday).order_by(desc(Student.grade)).limit(1)]
    print(oldest_student)

    #The first() method is a quick and easy way to execute a limit(1) statement and does not require a list interpretation
    oldest_student = session.query(Student.name, Student.birthday).order_by(desc(Student.grade)).first()
    print(oldest_student)

    #Importing func from sqlalchemy gives us access to common SQL operations through functions like sum() and count(). As these operations act upon columns, we carry them out through wrapping a Column object passed to the query() method
    student_count = session.query(func.count(Student.id)).first()
    print(student_count)

    #Retrieving specific records requires use of the filter() method
    query = session.query(Student).filter(Student.name.like('%Alan%'),
        Student.grade == 11)
    for record in query:
        print(record.name)

    #Updating Data
    for student in session.query(Student):
        student.grade += 1
    session.commit()
    print([(student.name,student.grade) for student in session.query(Student)])

    #Deleting Data  
    query = session.query(
        Student).filter(
            Student.name == "Albert Einstein")        

    # retrieve first matching record as object
    albert_einstein = query.first()

    # delete record
    session.delete(albert_einstein)
    session.commit()

    # try to retrieve deleted record
    albert_einstein = query.first()
    print(albert_einstein)