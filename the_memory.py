from base_has_logs import BaseHasLogs
import redis
import json

class TheMemory(object):
    @property
    def namespace(self):
        return f"percyns:{self._session_id}"
    
    @property
    def hist_key(self):
        return f"{self.namespace}:history"
    
    @property
    def sys_prompt_key(self):
        return f"{self.namespace}:system_prompt"
    
    @property
    def num_messages(self):
        return self._redis.llen(self.hist_key)

    def __init__(self, session_id='test', redis_host="pi-b1.local"):
        super().__init__()
        self._redis = redis.RedisCluster(host=redis_host)
        self._session_id = session_id
    
    def _update_system_prompt(self, content: str):
        msg = json.dumps({"role": "system", "content": content})
        self._redis.set(self.sys_prompt_key, msg)
    
    def add_message(self, role:str, content: str):
        msg = json.dumps({"role": role, "content": content})
        self._redis.rpush(self.hist_key, msg)

    # TODO: USE TOKEN CUTOFF
    def get_messages(self, max_messages=10000):
        sys_prompt = self._redis.get(self.sys_prompt_key)

        if self.num_messages <= max_messages:
            regular_messages = self._redis.lrange(self.hist_key, 0, -1)
        else:
            regular_messages = self._redis.lrange(self.hist_key, -max_messages, -1)
        
        desired_messages = [sys_prompt] + regular_messages
        message_dicts = []

        for curr_bytes in desired_messages:
            msg = json.loads(curr_bytes.decode('utf-8'))
            message_dicts.append(msg)
        
        return message_dicts