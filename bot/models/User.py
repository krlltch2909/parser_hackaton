from pydantic import BaseModel, Field
from database import user_preferences_collection
from aiogram.dispatcher import FSMContext
from models.Event import Event


class User(BaseModel):
    id: int = Field(alias="_id")
    events_types: list[int]
    tags: list[int]
    mailing_status: bool
    mailing_type: str
    
    def agreed_to_mailing(self) -> bool:
        return self.mailing_status is not None and self.mailing_status
    
    def agreed_to_accept_event(self, event: Event) -> bool:
        need_to_send = False
        if self.mailing_type == "all":
            need_to_send = True
        else:
            event_code = event.type_of_event.type_code
            tags_codes = map(lambda x: x.type_code, event.tags)
            matched_by_tag = any(item in self.tags for item in tags_codes)
            matched_by_event_code = event_code in self.events_types
            
            if len(self.events_types) != 0 and len(self.tags) != 0:
                if matched_by_tag and matched_by_event_code:
                    need_to_send = True
            elif len(self.events_types) != 0 and matched_by_event_code:
                need_to_send = True
            elif len(self.tags) != 0 and matched_by_tag:
                need_to_send = True 
        return need_to_send       

    def tick_tag(self, tag_code: int) -> None:
        if tag_code in self.tags:
            self.tags.remove(tag_code)
        else:
            self.tags.append(tag_code)
        
    def tick_event_type(self, type_code: int) -> None:
        if type_code in self.events_types:
            self.events_types.remove(type_code)
        else:
            self.events_types.append(type_code)
    
    async def save_to_state(self, state: FSMContext) -> None:
        await state.update_data(user_data=self)
        
    async def save_to_db(self) -> None:
        await user_preferences_collection.update_one(
            {"_id": self.id},
            {"$set": self.dict(by_alias=True)})
        
    async def delete(self) -> None:
        await user_preferences_collection.delete_one({"_id": self.id})
    
    @classmethod
    async def init_user(cls, user_id: int):
        user_data = await user_preferences_collection.find_one({"_id": user_id})
        if user_data is None:
            await cls.__instantiate_user(user_id)
            user_preferences = await user_preferences_collection.find_one({"_id": user_id})
            return User.parse_obj(user_preferences)
        else:
            return User.parse_obj(user_data)

    @staticmethod
    async def __instantiate_user(user_id: int) -> None:
        await user_preferences_collection.insert_one({
            "_id": user_id,
            "events_types": [],
            "tags": [],
            "mailing_status": False,
            "mailing_type": "all"
        })
