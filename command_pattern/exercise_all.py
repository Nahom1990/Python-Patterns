"""You're building a small backend job-processing system.

Your application needs to support different jobs:

SendEmail
GenerateReport
ResizeImage

Each job has different execution logic.

For example:

SendEmail
    → recipient
    → subject
    → body

GenerateReport
    → report type
    → date range

ResizeImage
    → image path
    → width
    → height

Your system has a JobRunner.

The JobRunner should not know how individual jobs work.

It should only know that it has something that can be executed.

The system should allow you to:

1. Create jobs
2. Add jobs to a queue
3. Execute jobs one by one
4. Keep a history of executed jobs
Additional requirement

After execution, you should be able to ask the system:

What jobs have been executed?

and receive the history.

Your tasks

Implement this three ways, just like you've been doing:

Version 1 — Classical OOP

Use:

ABC
Command interface
Concrete Commands
Receiver(s)
Invoker
Version 2 — Pythonic OOP

Use:

Protocol
composition
no unnecessary inheritance
Version 3 — Python functional

Use:

functions
Callable
lists/queues
closures or functools.partial if useful"""