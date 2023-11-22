from place.exceptions import *
import place
import requests
import json
import sys
if sys.version_info >= (3,0):
    from urllib.parse import urljoin
else:
    from urlparse import urljoin
import os
import pprint
import copy


def _conv_object(obj, client=None, inverse=False):
    obj = copy.copy( obj )
    if isinstance(obj, list):
        _iter = enumerate(obj)
    else:
        _iter = obj.items()
    for key, val in _iter:
        if inverse:
            if isinstance(val, APIResource):
                val = obj[key] = val._obj
        elif isinstance(val, dict)\
                and 'object' in val:
            for resource in APIResource.__subclasses__():
                if val['object'] != resource.object_type:
                    continue
                val = obj[key] = resource(client=client, **val)
                break
        if isinstance(val, (list, dict)):
            obj[key] = _conv_object(val, client=client, inverse=inverse)
    return obj


class APIResource(object):
    resource = None
    object_type = None
    default_params = None
    _object_index = {}

    def __new__(cls, client=None, **obj):
        if 'id' in obj:
            key = '{}_{}'.format(cls.object_type, obj['id'])
            if key in cls._object_index:
                cls._object_index[key]._set_obj(obj)
                return cls._object_index[key]
        return super(APIResource, cls).__new__(cls)

    def __init__(self, client=None, **obj):
        self._client = client or place.default_client
        self._set_obj(obj)

    def __repr__(self):
        return '{} (id={})'.format(
            super(APIResource, self).__repr__(), self.id)

    def _set_obj(self, obj):
        self._obj = obj
        self._obj = _conv_object(self._obj, client=self._client)
        if 'id' in obj:
            key = '{}_{}'.format(obj['object'], obj['id'])
            self._object_index[key] = self

    def __getattr__(self, attr):
        if attr in self._obj:
            return self._obj[attr]

    def json(self):
        return json.dumps(_conv_object(self._obj, inverse=True), indent=4, sort_keys=True)

    @classmethod
    def _request(cls, method, path=None, id=None,
                 client=None, *args, **kwargs):
        path = path or cls.resource
        client = client or place.default_client
        if id:
            path = os.path.join(path, id)
        url = urljoin(client.api_url, path.strip('/'))

        kwargs['headers'] = kwargs.get('headers', {})
        if 'X-API-Version' not in kwargs['headers']:
            kwargs['headers']['X-API-Version'] = 'v2.5'

        kwargs['auth'] = (client.api_key, '')
        if cls.default_params:
            if 'params' not in kwargs: kwargs['params'] = {}
            for k, v in cls.default_params.items():
                if k not in kwargs['params']: kwargs['params'][k] = v

        response = getattr(requests, method)(url, *args, **kwargs)
        status_code = response.status_code

        try:
            obj = response.json()
        except ValueError:
            if status_code == 500:
                raise InternalError()
            raise InvalidResponse()

        if not isinstance(obj, dict):
            raise InvalidResponse()

        object_type = obj.get('object')
        if not object_type:
            raise InvalidResponse('Response missing "object" attribute')

        if status_code != 200:
            if object_type != 'error':
                raise InvalidResponse('Expected error object')
            for exc in APIException.__subclasses__():
                if exc.status_code != status_code:
                    continue
                if exc.error_type and exc.error_type != obj.get('error_type'):
                    continue
                raise exc(obj.get('error_description'), obj)
            raise APIException(obj.get('error_description'), obj)

        if object_type == 'list':
            return [cls(client=client, **o) for o in obj['values']]
        return cls(client=client, **obj)

    def update(self, **updates):
        self._request('put', id=self.id, json=updates)

    def delete(self):
        self._request('delete', id=self.id)

    @classmethod
    def get(cls, id, update=None, **params):
        if not id:
            raise ValueError('id cannot be empty')
        if update:
            return cls._request('put', id=id, json=update, params=params)
        return cls._request('get', id=id, params=params)

    @classmethod
    def select(cls, update_all=None, delete_all=False, **filter_by):
        if update_all:
            return cls._request('put', params=filter_by, json=update_all)
        if delete_all:
            return cls._request('delete', params=filter_by)
        return cls._request('get', params=filter_by)

    @classmethod
    def create(cls, obj=None, **values):
        if isinstance( obj, list ):
            obj = {"object": "list", "values": obj}
        else:
            obj = dict(obj or {}, **values)
        obj = _conv_object(obj, inverse=True)
        return cls._request('post', json=obj)

    @classmethod
    def update_all(cls, objects, **params):
        updates = [dict(id=o.id, **upd) for o, upd in objects]
        return cls._request('put',
                            json={"object": "list", "values": updates}, params=params)
    @classmethod
    def delete_all(cls, objects):
        deletes = '|'.join(map(str, [o.id for o in objects]))
        return cls._request('delete', params={'id': deletes})
