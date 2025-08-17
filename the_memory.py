from base_has_logs import BaseHasLogs
import redis
import json

class TheMemory(object):
    @property
    def num_messages(self):
        return self._redis.llen(self._session_id)
    
    @property
    def is_first_message(self):
        return self.num_messages == 0

    def __init__(self, session_id='test', redis_host="pi-b1.local"):
        super().__init__()
        self._redis = redis.Redis(host=redis_host)
        self._session_id = session_id
    
    def _update_system_prompt(self, content: str):
        msg = json.dumps({"role": "system", "content": content})
        self._redis.lset(self._session_id, 0, msg)
    
    def add_message(self, role:str, content: str):
        msg = json.dumps({"role": role, "content": content})
        self._redis.rpush(self._session_id, msg)

    # TODO: USE TOKEN CUTOFF
    def get_messages(self, max_messages=10000):
        if self.num_messages <= max_messages:
            desired_messages = self._redis.lrange(self._session_id, 0, -1)
        else:
            sys_prompt = self._redis.lrange(self._session_id, 0, 0)
            tail_messages = self._redis.lrange(self._session_id, 1, -max_messages)
            desired_messages = sys_prompt + tail_messages

        message_dicts = []

        for curr_bytes in desired_messages:
            msg = json.loads(curr_bytes.decode('utf-8'))
            message_dicts.append(msg)
        
        return message_dicts