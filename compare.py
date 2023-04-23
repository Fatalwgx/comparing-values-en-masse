import csv
import random
from postgres import get_db, init_tables
from sqlalchemy.orm import Session
from sqlalchemy import text, select
import models


class Data:
    def __init__(self, row_number: int = 300000):
        self.ROWS = row_number

    def timer(func):
        import time

        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            print(f"{func.__name__} took {end_time - start_time} seconds to run")
            return result

        return wrapper


    def populate_datasets(self, db: Session):
        for _ in range(self.ROWS):
            dataset1 = models.OldData(digits=random.randint(0, 9))
            db.add(dataset1)

            dataset2 = models.NewData(digits=random.randint(0, 9))
            db.add(dataset2)

        db.commit()

    def drop_tables(self, db: Session, *tables: str):
        for table in tables:
            db.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY"))
        db.commit()

    @timer
    def match_datasets_plain_comparison(self, db: Session):
        query = select(models.OldData, models.NewData).join(
            models.NewData, models.OldData.id == models.NewData.id
        )
        for row in db.execute(query):
            if row.OldData.id != row.NewData.id:
                raise ValueError("Ids don't match")

            if row.OldData.digits == row.NewData.digits:
                values = models.Result(
                    id=row.OldData.id,
                    Value1=row.OldData.digits,
                    Value2=row.NewData.digits,
                )
                db.add(values)
        db.commit()

    @timer
    def match_datasets_yieldings(self, db: Session):
        query = select(models.OldData, models.NewData).join(
            models.NewData, models.OldData.id == models.NewData.id
        )
        for row in db.execute(query).yield_per(10):
            if row.OldData.id != row.NewData.id:
                raise ValueError("Ids don't match")

            if row.OldData.digits == row.NewData.digits:
                values = models.Result(
                    id=row.OldData.id,
                    Value1=row.OldData.digits,
                    Value2=row.NewData.digits,
                )
                db.add(values)
        db.commit()

    @timer
    def match_datasets_partitioning(self, db: Session):
        query = (
            select(models.OldData, models.NewData)
            .join(models.NewData, models.OldData.id == models.NewData.id)
            .execution_options(yield_per=1000)
        )
        for partition in db.execute(query).partitions():
            for row in partition:
                if row.OldData.id != row.NewData.id:
                    raise ValueError("Ids don't match")

                if row.OldData.digits == row.NewData.digits:
                    values = models.Result(
                        id=row.OldData.id,
                        Value1=row.OldData.digits,
                        Value2=row.NewData.digits,
                    )
                    db.add(values)
        db.commit()


def main():
    init_tables()
    db = next(get_db())
    data = Data()
    data.drop_tables(
        db,
        models.OldData.__tablename__,
        models.NewData.__tablename__,
        models.Result.__tablename__,
    )
    data.populate_datasets(db)
    data.match_datasets_plain_comparison(db)
    data.drop_tables(db, models.Result.__tablename__)
    data.match_datasets_yieldings(db)
    data.drop_tables(db, models.Result.__tablename__)
    data.match_datasets_partitioning(db)


if __name__ == "__main__":
    main()
