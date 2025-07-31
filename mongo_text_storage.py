from pymongo import MongoClient, errors
from pymongo.collection import Collection
from pymongo.database import Database
from bson import ObjectId
from datetime import datetime
from typing import Any


# MongoDB class with document insertion and search.
class MongoTextStorage:
    def __init__(self, host: str, port: int, db_name: str, collection_name: str):
        try:    
            self.client = MongoClient(host, port, serverSelectionTimeoutMS=5000)
            self.client.admin.command("ping") # Verifies connection to Mongo
            self.database: Database = self.client[db_name]
            self.collection: Collection = self.database[collection_name]
        except Exception as e:
            self._handle_error("Failure while connecting to MongoDB", e)

    # Add original text with Report to a collection.
    def save_text_with_report(self, input_text: str, report: dict[str, Any]) -> str | None:
        try:
            document = {
                "input_text": input_text,
                "created_at": datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S"),
                "report": report
            }
            result = self.collection.insert_one(document)
            return str(result.inserted_id)
        except Exception as e:
            self._handle_error("Failed to save document", e)
            return None
        
    # Search for documents by phrase
    def find_documents_by_text(self, phrase:str) -> list[dict[str, Any]]:
        try:
            query = {"input_text": {"$regex": phrase, "$options": "i"}}
            return list(self.collection.find(query))
        except errors.OperationFailure as e:
            self._handle_error("Find operation failed", e)
            return []
        except Exception as e:
            self._handle_error("General find error", e)
            return []
    
    # Get latest document
    def get_latest_document(self) -> dict[str, Any] | None:
        try:
            return self.collection.find_one(sort=[("created_at", -1)])
        except Exception as e:
            self._handle_error("Failed to fetch latest document", e)
            return None

    # Delete existing document by id
    def delete_document_by_id(self, id: str) -> bool:
        try:
            result = self.collection.delete_one({"_id": ObjectId(id)})
            return result.deleted_count == 1
        except errors.OperationFailure as e:
            self._handle_error("Delete operation failed", e)
            return False
        except Exception as e:
            self._handle_error("General delete error", e)
            return False

    # Function for error handling.
    def _handle_error(self, message: str, exception: Exception | None = None) -> None:
        if exception:
            print(f"[MongoError] {message}: {exception}")
        else:
            print(f"[MongoError] {message}")
