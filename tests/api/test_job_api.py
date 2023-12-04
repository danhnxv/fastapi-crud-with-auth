import unittest
from unittest.mock import patch
from mongoengine import connect, disconnect
from fastapi.testclient import TestClient
from app.main import app
import mongomock
from app.infra.database.models.user import User as UserModel
from app.infra.database.models.job import Jobs as JobModel
from app.infra.security.security_service import (
    TokenData,
    get_password_hash,
)


class TestClientApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        disconnect()
        connect(
            "mongoenginetest",
            host="mongodb://localhost:1234",
            mongo_client_class=mongomock.MongoClient,
            uuidRepresentation="standard"
        )
        cls.client = TestClient(app)
        cls.user = UserModel(
            username="danhnv",
            role="admin",
            hashed_password=get_password_hash(password="danhnv@bhsoft"),
        ).save()

    @classmethod
    def tearDownClass(cls):
        disconnect()

    def test_create_job(self):
        with patch("app.infra.security.security_service.verify_token") as mock_token:
            mock_token.return_value = TokenData(username=self.user.username)
            UserModel.objects(owner=self.user.id)
            r = self.client.post(
                "/jobs",
                json={
                    "name": "Learning FastAPI",
                    "description": "In testing",
                },
                headers={
                    "Authorization": "Bearer {}".format("xxx"),
                },
            )
            assert r.status_code == 200
            job = JobModel.objects(id=r.json().get("id")).get()
            assert job.owner.username == "danhnv"

    def test_create_job_w_existed_name(self):
        job = JobModel(
            **{
                "name": "Testing existed name",
                "description": "test existed name",
            },
            owner=self.user,
        ).save()
        with patch("app.infra.security.security_service.verify_token") as mock_token:
            mock_token.return_value = TokenData(username=self.user.username)
            r = self.client.post(
                "/jobs",
                json={
                    "name": job.name,
                    "description": "fastapi",
                },
                headers={
                    "Authorization": "Bearer {}".format("xxx"),
                },
            )
            assert r.status_code == 500
            resp = r.json()
            assert resp.get("detail") == "Job already existed"

    def test_get_job(self):
        cus = JobModel(
            **{
                "name": "Learning Docker",
                "description": "Docker"
            },
            owner=self.user,
        ).save()
        with patch("app.infra.security.security_service.verify_token") as mock_token:
            mock_token.return_value = TokenData(username=self.user.username)
            r = self.client.get(
                f"/jobs/{str(cus.id)}",
                headers={
                    "Authorization": "Bearer {}".format("xxx"),
                },
            )
            assert r.status_code == 200
            resp = r.json()
            assert resp.get("name") == cus.name

    def test_update_job(self):
        cus = JobModel(
            **{
                "name": "Learning NextJS",
                "description": "NextJS"
            },
            owner=self.user,
        ).save()
        with patch("app.infra.security.security_service.verify_token") as mock_token:
            mock_token.return_value = TokenData(username=self.user.username)
            r = self.client.put(
                f"/jobs/{str(cus.id)}",
                json={"name": "Learning ReactJS"},
                headers={
                    "Authorization": "Bearer {}".format("xxx"),
                },
            )
            assert r.status_code == 200
            resp = r.json()
            assert resp.get("name") == "Learning ReactJS"

    def test_get_list_jobs(self):
        with patch("app.infra.security.security_service.verify_token") as mock_token:
            mock_token.return_value = TokenData(username=self.user.username)
            r = self.client.get(
                "/jobs",
                headers={
                    "Authorization": "Bearer {}".format("xxx"),
                },
            )
            assert r.status_code == 200
            resp = r.json()
            assert len(resp) > 0

    def test_get_completed_job(self):
        cus = JobModel(
            **{
                "name": "Active Job",
                "description": "Job",
                "is_completed": True
            },
            owner=self.user,
        ).save()
        with patch("app.infra.security.security_service.verify_token") as mock_token:
            mock_token.return_value = TokenData(username=self.user.username)
            r = self.client.get(
                f"/jobs/completed-jobs",
                headers={
                    "Authorization": "Bearer {}".format("xxx"),
                },
            )
            assert r.status_code == 200
            resp = r.json()
            assert resp[0]['name'] == cus.name

    def test_delete_job(self):
        cus = JobModel(
            **{
                "name": "Learning JavaScript",
                "description": "JavaScript"
            },
            owner=self.user,
        ).save()
        with patch("app.infra.security.security_service.verify_token") as mock_token:
            mock_token.return_value = TokenData(username=self.user.username)
            r = self.client.delete(
                f"/jobs/{str(cus.id)}",
                headers={
                    "Authorization": "Bearer {}".format("xxx"),
                },
            )
            assert r.status_code == 200
            resp = r.json()
            assert resp.get("success") == True
