import config
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Boolean, Column, DateTime, Integer, Numeric, String, Text

from sqlalchemy.orm import backref, sessionmaker, scoped_session, relationship


engine = create_engine(config.DB_URI, echo=False)
session = scoped_session(sessionmaker(bind=engine,
									  autocommit = False,
									  autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

class CarbonConsumption(Base):
	"""This table contains all information for carbon consumption"""

	__tablename__ = "carbon_consumption"
	id = Column(Integer, primary_key=True)
	carbon = Column(Integer, nullable=True)

	def to_dict(self):
		"""Adds all of the CarbonConsumption columns to a dictionary, so the data
		can be easily formatted in the app.py"""

		output_dict = {}

		output_dict["id"] = int(self.id)
		output_dict["carbon"] = float(self.carbon)

		return output_dict


class Threshold(Base):
	"""This table contains all information for carbon consumption"""

	__tablename__ = "thresholds"
	id = Column(Integer, primary_key=True)
	value = Column(Integer, nullable=True)
	name = Column(String, nullable=True)

	def to_dict(self):
		"""Adds all of the CarbonConsumption columns to a dictionary, so the data
		can be easily formatted in the app.py"""

		output_dict = {}

		output_dict["id"] = int(self.id)
		output_dict["value"] = int(self.value)
		output_dict["name"] = self.name

		return output_dict

def create_tables():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
	create_tables()