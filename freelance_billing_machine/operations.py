from datetime import date as date_type
from .database import Session
from .models import Client, Project, WorkLog, Invoice
from sqlalchemy import func

def add_client(name: str, email: str, phone: str):
    """Add a new client to the database."""
    session = Session()
    try:
        client = Client(name=name, email=email, phone=phone)
        session.add(client)
        session.commit()
        print(f"Client '{name}' added successfully!")
    except Exception as e:
        session.rollback()
        print(f"Error adding client: {e}")
    finally:
        session.close()


def list_clients():
    """Return all clients."""
    session = Session()
    clients = session.query(Client).all()
    session.close()
    return clients


def add_project(title: str, description: str, rate: float, client_id: int):
    """Add a new project to the database."""
    session = Session()
    try:
        project = Project(
            title=title,
            description=description,
            rate=rate,
            client_id=client_id
        )
        session.add(project)
        session.commit()
        print(f"Project '{title}' added successfully!")
    except Exception as e:
        session.rollback()
        print(f"Error adding project: {e}")
    finally:
        session.close()


def list_projects():
    """List all projects with client names."""
    session = Session()
    projects = (
        session.query(Project, Client.name.label("client_name"))
        .join(Client)
        .all()
    )
    if not projects:
        print("No projects found.")
    else:
        print("\nProjects:")
        for project, client_name in projects:
            print(
                f"ID: {project.id} | Title: {project.title} | "
                f"Client: {client_name} | Rate: {project.rate} | Description: {project.description}"
            )
    session.close()


def log_work(project_id: int, hours: float, date=None):
    """Log hours worked for a project."""
    session = Session()
    try:
        if date is None:
            date = date_type.today()

        worklog = WorkLog(
            project_id=project_id,
            hours=hours,
            date=date
        )
        session.add(worklog)
        session.commit()
        print(f"Logged {hours} hours for project ID {project_id} on {date}.")
    except Exception as e:
        session.rollback()
        print(f"Error logging work: {e}")
    finally:
        session.close()


def list_worklogs():
    """List all work logs."""
    session = Session()
    worklogs = session.query(WorkLog).all()
    if not worklogs:
        print("No worklogs found.")
    else:
        print("\nWorklogs:")
        for w in worklogs:
            print(f"ID: {w.id}, Project ID: {w.project_id}, Date: {w.date}, Hours: {w.hours}")
    session.close()


def generate_invoice(project_id: int):
    """Generate an invoice for a project based on logged hours."""
    session = Session()
    try:
        project = session.query(Project).filter_by(id=project_id).first()
        if not project:
            print("Project not found.")
            return

        total_hours = (
            session.query(func.sum(WorkLog.hours))
            .filter_by(project_id=project_id)
            .scalar()
        )

        if not total_hours:
            print("No work logged for this project.")
            return

        amount = total_hours * project.rate
        invoice = Invoice(
            issue_date=date_type.today(),
            amount=amount,
            status="Unpaid",
            project_id=project_id
        )
        session.add(invoice)
        session.commit()

        print(
            f"✅ Invoice generated for project '{project.title}': "
            f"{total_hours} hours × {project.rate} = {amount}"
        )

    except Exception as e:
        session.rollback()
        print(f"Error generating invoice: {e}")
    finally:
        session.close()
