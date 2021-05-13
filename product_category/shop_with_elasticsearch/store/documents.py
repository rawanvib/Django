from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import Cuisine

# cuisines=Index('cuisines')

@registry.register_document
class CuisineDocument(Document):
    class Index:
        name='cuisines'
        settings={
            'number_of_shards':1,
            'number_of_replicas':0
        }

    class Django:
        model=Cuisine

        fields=[
            'id','title','description','price','image'
        ]



# Relational DB → Databases → Tables → Rows → Columns
#
# Elasticsearch → Indexes → Types → Documents → Fields
#The only difference is that in relational databases each
# database can have many tables. But in Elasticsearch each index can only have one type.