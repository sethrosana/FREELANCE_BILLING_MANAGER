import click
from tabulate import tabulate
from datetime import datetime
from .database import init_db
from .operations import (
    add_client,
    list_clients,
    add_project,
    list_projects,
    log_work,
    list_worklogs,
    generate_invoice
)

@click.group()
def cli():
    """Freelance Billing Manager CLI"""
    pass


@cli.command()
def setup():
    """Initialize the database"""
    init_db()
    click.echo("✅ Database initialized successfully!")

@cli.command()
@click.option('--name', prompt='Client name', help='Name of the client')
@click.option('--email', prompt='Client email', help='Email of the client')
@click.option('--phone', prompt='Client phone', help='Phone number of the client')
def new_client(name, email, phone):
    """Add a new client"""
    add_client(name, email, phone)


@cli.command()
def clients():
    """List all clients"""
    clients = list_clients()
    if not clients:
        click.echo("No clients found.")
        return

    table = [(c.id, c.name, c.email, c.phone) for c in clients]
    click.echo(tabulate(table, headers=["ID", "Name", "Email", "Phone"], tablefmt="psql"))


@cli.command()
@click.option('--title', prompt='Project title', help='Title of the project')
@click.option('--description', prompt='Description', help='Description of the project')
@click.option('--rate', prompt='Rate per hour', type=float)
@click.option('--client_id', prompt='Client ID', type=int)
def new_project(title, description, rate, client_id):
    """Add a new project"""
    add_project(title, description, rate, client_id)


@cli.command()
def list_projects_cmd():
    """List all projects"""
    list_projects()


@cli.command()
@click.option('--project_id', prompt='Project ID', type=int)
@click.option('--hours', prompt='Hours worked', type=float)
@click.option('--date', prompt='Date (YYYY-MM-DD)', required=False)
def worklog(project_id, hours, date):
    """Log work hours for a project"""
    work_date = datetime.strptime(date, "%Y-%m-%d").date() if date else None
    log_work(project_id, hours, work_date)


@cli.command()
def list_worklogs_cmd():
    """List all work logs"""
    list_worklogs()



@cli.command()
@click.option('--project_id', prompt='Project ID', type=int)
def generate_invoice_cmd(project_id):
    """Generate an invoice for a project"""
    generate_invoice(project_id)


if __name__ == '__main__':
    cli()
