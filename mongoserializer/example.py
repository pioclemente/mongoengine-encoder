# -*- coding: utf-8 -*-

#MongoEngineSerializer().dumps(MongoObject)
import mongoengine
from mongoengine import *
from pprint import pprint as pp
import serializer

class User(Document):
    email = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)

class Comment(EmbeddedDocument):
    content = StringField()
    name = StringField(max_length=120)

class Post(Document):
    title = StringField(max_length=120, required=True)
    author = ReferenceField(User)
    tags = ListField(StringField(max_length=30))
    comments = ListField(EmbeddedDocumentField(Comment))


def create_docs():
    john = User(email='jdoe@example.com', first_name='John', last_name='Doe')
    john.save()

    comment = Comment(content="comment content",name="comment name")
    #comment.save()

    comment1 = Comment(content="comment content2",name="comment name2")
    #comment1.save()

    comment2 = Comment(content="comment content3",name="comment name3")
    #comment2.save()

    post = Post(title='MongoEngine Documentation', author=john)
    post.tags = ['mongoengine']
    post.comments = [comment,comment1,comment2]
    post.save()


def serialize_example1():
    res = []
    inject = []
    exclude = []
    func_generic_extra_info = []
    func_extra_info = []
    for x in Post.objects():
        res.append(serializer.MongoEngineSerializer(inject,exclude,func_generic_extra_info,func_extra_info).dumps(x,indent=2))
    print "OUT"
    print res
def serialize_example2():
    inject = []
    exclude = []
    func_generic_extra_info = []
    func_extra_info = []
    x = Post.objects.all()
    res = serializer.MongoEngineSerializer(inject,exclude,func_generic_extra_info,func_extra_info).dumps(x,indent=2)
    print "OUT"
    print res

def serialize_example3():
    print "TEST INJECT"
    inject = []
    inject.append({'mapping_type':'default'})
    inject.append({'static_velue':'inject_static_value_for_each_item'})
    exclude = []
    func_generic_extra_info = []
    func_extra_info = []
    x = Post.objects.all()
    res = serializer.MongoEngineSerializer(inject,exclude,func_generic_extra_info,func_extra_info).dumps(x,indent=2)
    #print "OUT"
    print res

def serialize_example4():
    print "TEST EXCLUDE"
    inject = []
    exclude = ["_types","_cls","key"]
    func_generic_extra_info = []
    func_extra_info = []
    x = Post.objects.all()
    res = serializer.MongoEngineSerializer(inject,exclude,func_generic_extra_info,func_extra_info).dumps(x,indent=2)
    #print "OUT"
    print res

def my_add_generic_extra_info(data):
    data['test_pio'] = 'test_pio'

def my_add_user_extra_info(data):
    data['author']['slug'] = u"http://site.com/%s"%(data['_id'])

def my_add_tot_comments(data):
    data['tot_comments'] = len(data['comments'])

def serialize_example4():
    print "TEST func_generic_extra_info"
    inject = []
    exclude = ["_types","_cls","key"]
    func_generic_extra_info = [my_add_generic_extra_info]
    func_extra_info = [my_add_user_extra_info,my_add_tot_comments]
    x = Post.objects.all()
    res = serializer.MongoEngineSerializer(inject,exclude,func_generic_extra_info,func_extra_info).dumps(x,indent=2)
    #print "OUT"
    print res


def main():
    mongo_db_name = "test_serializer"
    mongoengine.connect(mongo_db_name)
    print "CREATE DOC"
    create_docs()
    print "serialize_example1"
    serialize_example1()

    print "serialize_example2"
    serialize_example2()

    print "serialize_example3"
    serialize_example3()

    print "serialize_example4"
    serialize_example4()





if __name__=="__main__":
    main()
