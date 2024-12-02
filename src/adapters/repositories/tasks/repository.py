from loguru import logger
from sqlalchemy import delete, func, select
from sqlalchemy.exc import NoResultFound

from src.adapters.data_types.requests.tasks_request import (
    NewTaskRequest,
    PatchTaskStatusRequest,
    UpdateTaskRequest,
)
from src.adapters.data_types.typed_dicts.tasks_typed_dict import (
    PaginatedTasksTypedDict,
)
from src.domain.exceptions.repository.exception import (
    TaskAlreadyInStatusError,
    TaskNotFoundError,
)
from src.domain.models.tasks.model import TaskModel
from src.externals.infrastructures.postgres.infrastructure import (
    PostgresInfrastructure,
)


class TaskRepository:
    postgres_infrastructure = PostgresInfrastructure()

    @classmethod
    async def insert_one_task(
        cls,
        task_request: NewTaskRequest,
    ) -> TaskModel:
        async with cls.postgres_infrastructure.get_session() as session:
            new_task_model = TaskModel(**task_request.model_dump())
            session.add(new_task_model)
            await session.commit()
            await session.refresh(new_task_model)

            return new_task_model

    @classmethod
    async def get_tasks_paginated(
        cls,
        limit: int,
        offset: int,
    ) -> PaginatedTasksTypedDict:
        async with cls.postgres_infrastructure.get_session() as session:
            statement = select(TaskModel)
            count_query = select(func.count(TaskModel.id))

            query = statement.limit(limit).offset(offset)

            db_result = await session.execute(query)
            tasks_model = db_result.unique().scalars().all()

            total_tasks = await session.execute(count_query)
            total_count = total_tasks.scalar()

            return PaginatedTasksTypedDict(
                tasks=tasks_model,
                total=total_count,
                limit=limit,
                offset=offset,
            )

    async def get_one_task_by_id(self, task_id: int) -> TaskModel:
        async with self.postgres_infrastructure.get_session() as session:
            try:
                statement = select(TaskModel).where(TaskModel.id == task_id)
                db_result = await session.execute(statement)
                task = db_result.unique().scalar_one()

                return task

            except NoResultFound as ex:
                logger.info(ex)
                raise TaskNotFoundError(task_id)

    async def update_task(
        self, task_id: int, task_request: UpdateTaskRequest
    ) -> TaskModel:
        async with self.postgres_infrastructure.get_session() as session:
            try:
                statement = select(TaskModel).where(TaskModel.id == task_id)
                db_result = await session.execute(statement)
                task = db_result.scalar_one()

                task_data = task_request.model_dump(exclude_none=True)
                for key, value in task_data.items():
                    setattr(task, key, value)

                await session.commit()
                await session.refresh(task)

                return task

            except NoResultFound as ex:
                logger.info(ex)
                raise TaskNotFoundError(task_id)

    async def update_task_status(
        self, request: PatchTaskStatusRequest
    ) -> TaskModel:
        async with self.postgres_infrastructure.get_session() as session:
            try:
                task_id = request.task_id
                new_status = request.status
                statement = select(TaskModel).where(TaskModel.id == task_id)
                db_result = await session.execute(statement)
                task = db_result.scalar_one()

                if task.status == new_status:
                    raise TaskAlreadyInStatusError(
                        status=new_status, task_id=task_id
                    )

                task.status = new_status
                await session.commit()

                return task

            except NoResultFound as ex:
                logger.info(ex)
                raise TaskNotFoundError(task_id)

    async def delete_one_task_by_id(self, task_id: int) -> None:
        async with self.postgres_infrastructure.get_session() as session:
            statement = (
                delete(TaskModel)
                .where(TaskModel.id == task_id)
                .returning(TaskModel.id)
            )

            db_result = await session.execute(statement)
            deleted_id = db_result.scalar()

            if not deleted_id:
                raise TaskNotFoundError(task_id=task_id)

            await session.commit()
