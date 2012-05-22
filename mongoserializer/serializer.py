# -*- coding: utf-8 -*-
from pymongo.dbref import DBRef
from pymongo.objectid import ObjectId
import datetime
from pprint import pprint as pp
from mongoengine.queryset import QuerySet
import json
class MongoEncoder(object):
    def __init__(self,obj,inject=[],exclude=[],func_generic_extra_info=[],func_extra_info=[]):
        self.main_obj = obj
        self.exclude = exclude
        self.inject = inject
        self.final_fields = []
        self.func_extra_info=func_extra_info
        self.func_generic_extra_info = func_generic_extra_info;
        obj_to_mongo = obj.to_mongo()
        self.fields=obj_to_mongo.keys()

        for f in self.fields:
            val = self.h_value(f,obj,obj_to_mongo[f])
            if val is not None:
                self._sett_attr(f,val)
        for i  in self.inject:
            if isinstance(i,dict):
                k=i.keys()[0]
                if not hasattr(self,k):
                    self._sett_attr(k,i.values()[0])
    def _sett_attr(self,k,v):
        setattr(self,k,v)
        self.final_fields.append(k)


    def print_all(self):
        for f in self.final_fields:
            print "F [%s] Val [%s]"%(f,getattr(self,f))
    def to_dict(self):
        d={}
        for f in self.final_fields:
            v = getattr(self,f,None)
            if v is not None:
                d[f]=v
        for f in self.func_generic_extra_info:
            f(d)
        for f in self.func_extra_info:
            f(d)

        return d
    def h_value(self,f,obj,obj_to_mongo):
        if f in self.exclude:
            return None
        if isinstance(obj_to_mongo, dict):
            #return obj_to_mongo.strftime('%Y-%m-%dT%H:%M:%S')
            tmp_ret = {}
            for k in obj_to_mongo:
                new_obj = obj_to_mongo[k]
                try:
                    new_obj_to_mongo = new_obj.to_mongo()
                except :
                    new_obj_to_mongo = new_obj
                val = self.h_value(k,new_obj,new_obj_to_mongo)
                if val is not None:
                    tmp_ret.update({k:val})
            return tmp_ret


        elif isinstance(obj_to_mongo, unicode):
            return u"%s"%obj_to_mongo
        elif isinstance(obj_to_mongo, datetime.datetime):
            return obj_to_mongo.strftime('%Y-%m-%dT%H:%M:%S')
        elif isinstance(obj_to_mongo, datetime.date):
            return obj_to_mongo.strftime('%Y-%m-%d')
        elif isinstance(obj_to_mongo, ObjectId):
            return u"%s"%str(obj_to_mongo)
        elif isinstance(obj_to_mongo, list):
            tmp_list_ret = []
            for position,tmp in enumerate(obj_to_mongo):
                #pp(new_obj)
                if isinstance(tmp, dict):
                    #print "KKKKKKKKK",tmp
                    tmp_list_ret.append(self.h_value(f,tmp,tmp))
                elif isinstance(tmp, DBRef):
                    #tmp_ret.append('cioa')
                    #print "ECCO L -- f [%s] position [%s]"%(f,position)
                    #new_obj = obj.l_posts[position]
                    new_obj = getattr(obj,f)[position]
                    new_obj_to_mongo = new_obj.to_mongo()
                    tmp_ret = {}
                    for fn in new_obj_to_mongo.keys():
                        val = self.h_value(fn,new_obj,new_obj_to_mongo[fn])
                        if val is not None:
                            tmp_ret.update({fn:val})
                    if len(tmp_ret):
                        tmp_list_ret.append(tmp_ret)
                elif isinstance(tmp,unicode) or isinstance(tmp,str):
                    tmp_list_ret.append(self.h_value(f,tmp,tmp))
            return tmp_list_ret
        elif isinstance(obj_to_mongo, DBRef):
            new_obj_to_mongo = getattr(obj,f).to_mongo()
            new_obj = getattr(obj,f)
            tmp_ret = {}
            for fn in new_obj_to_mongo.keys():
                #pp(new_obj_to_mongo)
                val = self.h_value(fn,new_obj,new_obj_to_mongo[fn])
                if val is not None:
                    tmp_ret.update({fn:val})
            return tmp_ret
            #return self.h_value(f,obj,getattr(obj,f).to_mongo())
        else:
            return obj_to_mongo


class MongoEngineSerializer(object):
    def __init__(self,inject=[],exclude=[],func_generic_extra_info=[],func_extra_info=[]):
        self.inject=inject
        self.exclude=exclude
        self.func_generic_extra_info=func_generic_extra_info
        self.func_extra_info=func_extra_info
    def dumps(self,obj,indent=0):
        ret = []
        if isinstance(obj,QuerySet):
            for o in obj:
                ret.append(MongoEncoder(obj=o,inject=self.inject,exclude=self.exclude,func_generic_extra_info=self.func_generic_extra_info,func_extra_info=self.func_extra_info).to_dict())

        else:
            ret = MongoEncoder(obj=obj,inject=self.inject,exclude=self.exclude,func_generic_extra_info=self.func_generic_extra_info,func_extra_info=self.func_extra_info).to_dict()
        return json.dumps(ret,indent=indent)

