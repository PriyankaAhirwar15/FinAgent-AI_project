from langgraph.checkpoint.memory import MemorySaver
import os
def get_checkpointer():
    return MemorySaver()
