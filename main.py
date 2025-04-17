from fastapi import FastAPI, HTTPException, Path, Depends
from pydantic import BaseModel, constr
from typing import List
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# Настройка базы данных SQLite
DATABASE_URL = "sqlite:///./tasks.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


# Модель БД
class TaskDB(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(String, nullable=False)


Base.metadata.create_all(bind=engine)


# Pydantic модели для валидации
class TaskBase(BaseModel):
    title: constr(min_length=1)
    description: constr(min_length=1)
    status: constr(min_length=1)


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass


class Task(TaskBase):
    id: int

    class Config:
        orm_mode = True


# Инициализация FastAPI
app = FastAPI(title="Task Management API")


# Зависимость для сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CRUD операции

@app.get("/tasks", response_model=List[Task])
def read_tasks(db: Session = Depends(get_db)):
    tasks = db.query(TaskDB).all()
    return tasks


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = TaskDB(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(
        task_id: int = Path(..., gt=0),
        task_update: TaskUpdate = ...,
        db: Session = Depends(get_db)
):
    task_db = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not task_db:
        raise HTTPException(status_code=404, detail="Task not found")

    for field, value in task_update.dict().items():
        setattr(task_db, field, value)

    db.commit()
    db.refresh(task_db)

    return task_db


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    task_db = db.query(TaskDB).filter(TaskDB.id == task_id).first()

    if not task_db:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task_db)
    db.commit()

    return None
