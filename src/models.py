from mongoengine import *
from mongoengine.document import Document

class Deputy(Document):
    id = IntField(primary_key=True)
    name = StringField(required=True)
    photo_url = StringField()
    initial_legislature_id = IntField(required=True)
    final_legislature_id = IntField()
    initial_legislature_year = IntField(required=True)
    final_legislature_year = IntField()
    last_activity_date = DateTimeField()
    full_name = StringField()
    sex = StringField()
    email = StringField()
    birth_date = DateTimeField()
    death_date = DateTimeField()
    federative_unity = StringField()
    party = StringField()
    instagram_username = StringField()
    twitter_username = StringField()
    facebook_username = StringField()
    twitter_id = StringField()
    website = StringField()
    office_number = StringField()
    office_name = StringField()
    office_premise = StringField()
    office_floor = StringField()
    office_phone = StringField()
    office_email = StringField()

    def to_json(self):
        return{
            'id':self.id,
            'name':self.name,
            'photo_url':self.photo_url,
            'initial_legislature_id':self.initial_legislature_id,
            'final_legislature_id':self.final_legislature_id,
            'initial_legislature_year':self.initial_legislature_year,
            'final_legislature_year':self.final_legislature_year,
            'last_activity_date':self.last_activity_date,
            'full_name':self.full_name,
            'sex':self.sex,
            'email':self.email,
            'birth_date':self.birth_date,
            'death_date':self.death_date,
            'federative_unity':self.federative_unity,
            'party':self.party,
            'instagram_username':self.instagram_username,
            'twitter_username':self.twitter_username,
            'facebook_username':self.facebook_username,
            'twitter_id':self.twitter_id,
            'website':self.website,
            'office_number':self.office_number,
            'office_name':self.office_name,
            'office_premise':self.office_premise,
            'office_floor':self.office_floor,
            'office_phone':self.office_phone,
            'office_email':self.office_email
        }

class DeputyEquity(Document):
    id = IntField(primary_key=True)
    deputy_name = StringField(required=True)
    deputy_id = StringField(required=True)
    value = IntField(required=True)
    description = StringField()
    death_date = DateTimeField()

    def to_json(self):
        return {
            'id':self.id,
            'deputy_name':self.deputy_name,
            'deputy_id':self.deputy_id,
            'value':self.value,
            'description':self.description,
            'death_date':self.death_date
        }
    
# class News(Document):
#     id = IntField(primary_key=True)
#     deputy_id = IntField()
#     link = StringField()
#     photo = StringField()
#     title = StringField()
#     abstract = StringField()
#     deputy_name = StringField()
#     update_date = DateTimeField()
#     source = StringField()

#     def to_json(self, context):
#         return {
#             'id':context.id,
#             'deputy_id':context.deputy_id,
#             'link': context.link,
#             'photo':context.photo,
#             'title':context.title,
#             'abstract':context.abstract,
#             'deputy_name':context.deputy_name,
#             'update_date':context.update_date,
#             'source':context.source
#         }


# class Tweet(Document):
#     tweet_id = IntField(primary_key=True)
#     deputy_id = IntField()
#     name = StringField()
#     twitter_username = StringField()
#     date = DateTimeField()

