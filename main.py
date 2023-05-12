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
# how to generate sequence of mailboxes and therefore locks and concurrency (set as a key)
# leveldb string matching
states = [
  [["running_on", ["A", "thread1"]], ["thread", ["thread1"]], ["assignment", ["A", "t"]]],
  [["send_task_to_thread", ["B", "next_free_thread"]]],
  [["running_on", ["B", 2]], ["paused", ["B", 1]], ["running_on", ["A", 1] ]]
]

def create_mailboxes(states):
  mailboxes = []
  history = ""
  for state in states:
    
    for item in state:
      
      history = "{} {}".format(history, item[0])
      # mailboxes.append(history)
      
      for subitem in item[1]:
        history = "{}_{}".format(history, subitem)
        mailboxes.append(history)
  return mailboxes

mb = create_mailboxes(states)
from pprint import pprint
pprint(mb)