program = """
running_on(A, 1)
thread(1)
assignment(A, 1)
thread_free(next_free_thread) = fork(A, B)
                                | send_task_to_thread(B, next_free_thread)
                                |   running_on(B, 2)
                                    paused(B, 1)
                                    running_on(A, 1)
                               | { yield(B, returnvalue) | paused(B, 2) }
                                 { await(A, B, returnvalue) | paused(A, 1) }
                               | send_returnvalue(B, A, returnvalue)   
"""

class State:
  def __init__(self, state):
    self.state = state
    self.children = []
    self.parents = []
    self.indent = 0
  def add_parent(self, state):
    self.parents.append(state)
  def add_state(self, state):
    state.add_parent(self)
    self.children.append(state)
    state.indent = self.indent + 1
  def __repr__(self):
    data = (self.indent * "  ") + str(self.state) + "\n"
    for child in self.children:
      data += str(child)
    return data
      
# how to generate sequence of mailboxes and therefore locks and concurrency (set as a key)
# leveldb string matching
states = [
  [["running_on", ["A", "thread1"]], ["thread", ["thread1"]], ["assignment", ["A", "t"]]],
  [["send_task_to_thread", ["B", "next_free_thread"]]],
  [["running_on", ["B", "2"]], ["paused", ["B", "1"]], ["running_on", ["A", 1] ]]
]

def create_mailboxes(states):
  mailboxes = []
  history = ""
  depth = 0
  parent = State("root")
  for state in states:
    stateline = State("stateline{}".format(depth))
    depth = depth + 1
                                          
    parent.add_state(stateline)
    for item in state:
      child = State(item[0])
      stateline.add_state(child)
      history = "{} {}".format(history, item[0])
      # mailboxes.append(history)
      
      for subitem in item[1]:
        subchild = State(subitem)
        child.add_state(subchild)
        history = "{}_{}".format(history, subitem)
        mailboxes.append(history)
  return mailboxes, parent

mb, state = create_mailboxes(states)
from pprint import pprint
pprint(mb)
pprint(state)

# use ^ hat symbol to refer to parent