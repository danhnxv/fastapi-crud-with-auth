from mongoengine import QuerySet, DoesNotExist
from app.domain.job.entity import JobInDB, JobInUpdate
from app.infra.database.models.job import Jobs as JobModel
from typing import Dict, List, Union, Optional, Any
from bson import ObjectId
from app.infra.database.models.user import User


class JobRepository:
    def __init__(self):
        pass

    def create(self, obj_in: JobInDB) -> JobModel:
        """
        Create new client in db
        """
        # create client document instance
        job = JobModel(**obj_in.model_dump())
        # and save it to db
        job.save()
        return job

    def find(self, conditions: Dict[str, Union[str, bool, ObjectId]], skip: int = 0, limit: int = 5) -> (
            List)[Optional[JobModel]]:
        try:
            docs = JobModel._get_collection().find(conditions).skip(skip).limit(limit)

            return [JobModel.from_mongo(doc) for doc in docs] if docs else []
        except Exception:
            return []

    def find_one(self, conditions: Dict[str, Union[str, bool, ObjectId]]) -> Optional[JobModel]:
        try:
            doc = JobModel._get_collection().find_one(conditions)
            return JobModel.from_mongo(doc) if doc else None
        except Exception:
            return None

    def get_by_name(self, name: str) -> Optional[JobInDB]:
        """
        Get client in db from email
        :param name:
        :return:
        """

        qs: QuerySet = JobModel.objects(name=name)
        # retrieve unique result
        # https://mongoengine-odm.readthedocs.io/guide/querying.html#retrieving-unique-results
        try:
            job = qs.get()
        except DoesNotExist:
            return None
        return JobInDB.model_validate(job)

    def get_by_id(self, id: str) -> Optional[JobModel]:
        """
        Get user in db from id
        :return:
        """
        qs: QuerySet = JobModel.objects(id=id)
        # retrieve unique result
        # https://mongoengine-odm.readthedocs.io/guide/querying.html#retrieving-unique-results
        try:
            job: JobModel = qs.get()
            return job
        except DoesNotExist:
            return None

    def update(self, id: ObjectId, data: Union[JobInUpdate, Dict[str, Any]]) -> bool:
        try:
            data = data.model_dump(exclude_none=True) if isinstance(data, JobInUpdate) else data
            JobModel.objects(id=id).update_one(**data, upsert=False)
            return True
        except Exception:
            return False

    def delete(self, object_id: ObjectId) -> bool:
        try:
            JobModel.objects(id=object_id).delete()
            return True
        except Exception:
            return False

    def list(
            self, owner: User, page_index: int = 1, page_size: int = 5
    ) -> List[JobModel]:
        try:
            data = (
                JobModel.objects(owner=owner)
                .order_by("-_id")
                .skip((page_index - 1) * page_size)
                .limit(page_size)
            )
            return data
        except Exception:
            return []

    def count(self, conditions: Dict[str, Union[str, bool, User]] = {}) -> int:
        try:
            return JobModel._get_collection().count_documents(conditions)
        except Exception:
            return 0
