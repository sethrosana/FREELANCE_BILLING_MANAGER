import unittest
from datetime import date
from freelance_billing_machine.models import Client, Project, Invoice, WorkLog

class TestModels(unittest.TestCase):
    def test_client_creation(self):
        client = Client(name="Test Client", email="test@example.com", phone="12345")
        self.assertEqual(client.name, "Test Client")

    def test_project_relationship(self):
        project = Project(title="Website", description="Web dev", rate=50.0)
        self.assertEqual(project.title, "Website")

    def test_worklog_creation(self):
        worklog = WorkLog(project_id=1, date=date(2025, 10, 19), hours=4)
        self.assertEqual(worklog.hours, 4)

if __name__ == '__main__':
    unittest.main()

