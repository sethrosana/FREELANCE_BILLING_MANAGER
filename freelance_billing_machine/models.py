from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String)
    phone = Column(String)

    projects = relationship('Project', back_populates='client')

    def __repr__(self):
        return f"<Client(name='{self.name}', email='{self.email}')>"


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    rate = Column(Float)
    client_id = Column(Integer, ForeignKey('clients.id'))

    client = relationship('Client', back_populates='projects')
    invoices = relationship('Invoice', back_populates='project')
    worklogs = relationship('WorkLog', back_populates='project')

    def __repr__(self):
        return f"<Project(title='{self.title}', rate={self.rate})>"


class Invoice(Base):
    __tablename__ = 'invoices'

    id = Column(Integer, primary_key=True)
    issue_date = Column(Date)
    amount = Column(Float)
    status = Column(String)
    project_id = Column(Integer, ForeignKey('projects.id'))

    project = relationship('Project', back_populates='invoices')

    def __repr__(self):
        return f"<Invoice(amount={self.amount}, status='{self.status}')>"


class WorkLog(Base):
    __tablename__ = 'worklogs'

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    date = Column(Date, nullable=False)
    hours = Column(Float, nullable=False)

    project = relationship('Project', back_populates='worklogs')

    def __repr__(self):
        return f"<Worklog(project_id={self.project_id}, date={self.date}, hours={self.hours})>"
