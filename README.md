# relational state machines

This is the beginnings of a parser to parse a state formulation described in [ideas4, 558. State machine formulation](https://github.com/samsquire/ideas4#558-state-machine-formulation).

The state machine formulation looks like this:

```
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
```