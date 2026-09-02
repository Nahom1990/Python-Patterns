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

from typing import Any 
class SendEmail:
    def __init__(self,recipient,subject,body) -> None:
        self.recipient=recipient
        self.subject=subject
        self.body=body
    def send(self):
        print(f"sent email to {self.recipient}")

class GenerateRport:
    def __init__(self,report_type,start_date,end_date) -> None:
        self.report_type=report_type
        self.start_date=start_date
        self.end_date=end_date
    def generate(self):
        print(f"generated report from {self.start_date}-{self.end_date}")

class ResizeImage:
    def __init__(self,image_path,width,height) -> None:
        self.image_path=image_path
        self.width=width
        self.height=height

    def resize(self):
        print(f"resized the image at {self.image_path}")

from abc import ABC,abstractmethod
class Command(ABC):
    @abstractmethod
    def execute(self): pass

class SendEmailCommand(Command):
    def __init__(self,email:SendEmail) -> None:
        self.email=email

    def execute(self):
        self.email.send()
class GenerateReportCommand(Command):
    def __init__(self,report:GenerateRport) -> None:
        self.report=report

    def execute(self):
        self.report.generate()
class ResizeImageCommand(Command):
    def __init__(self,image:ResizeImage) -> None:
        self.image=image

    def execute(self):
        self.image.resize()


class JobRunner:
    def __init__(self) -> None:
        self.queue:list[Any]=[]
        self.history:list[Any]=[]

    def queue_job(self,job):
        self.queue.append(job)

    def execute_job(self):
        while self.queue:
                job=self.queue.pop(0)
                self.history.append(job)
                yield job.execute()

runner=JobRunner()
job_email=SendEmail(recipient="nahom",subject="hi hi",body="how are you")
job_report=GenerateRport("Yearly","may-5-2025","may-5-2026")
command_email=SendEmailCommand(job_email)
command_report=GenerateReportCommand(job_report)
runner.queue_job(command_email)
runner.queue_job(command_report)

task=runner.execute_job()

next(task)
next(task)
#####version 2 
class SendEmail2:
    def __init__(self,recipient,subject,body) -> None:
        self.recipient=recipient
        self.subject=subject
        self.body=body
    def send(self):
        print(f"sent email to {self.recipient}")

class GenerateRport2:
    def __init__(self,report_type,start_date,end_date) -> None:
        self.report_type=report_type
        self.start_date=start_date
        self.end_date=end_date
    def generate(self):
        print(f"generated report from {self.start_date}-{self.end_date}")

class ResizeImage2:
    def __init__(self,image_path,width,height) -> None:
        self.image_path=image_path
        self.width=width
        self.height=height

    def resize(self):
        print(f"resized the image at {self.image_path}")

from typing import Protocol
class Command2(Protocol):

    def execute(self): ...

class SendEmailCommand2:
    def __init__(self,email:SendEmail2) -> None:
        self.email=email

    def execute(self):
        self.email.send()
class GenerateReportCommand2:
    def __init__(self,report:GenerateRport2) -> None:
        self.report=report

    def execute(self):
        self.report.generate()
class ResizeImageCommand2:
    def __init__(self,image:ResizeImage2) -> None:
        self.image=image

    def execute(self):
        self.image.resize()


class JobRunner2:
    def __init__(self) -> None:
        self.queue:list[Any]=[]
        self.history:list[Any]=[]

    def queue_job(self,job:Command2):
        self.queue.append(job)

    def execute_job(self):
        while self.queue:
                job=self.queue.pop(0)
                self.history.append(job)
                yield job.execute()

runner2=JobRunner2()
job_email2=SendEmail2(recipient="nahom",subject="hi hi",body="how are you")
job_report2=GenerateRport2("Yearly","may-5-2025","may-5-2026")
command_email2=SendEmailCommand2(job_email2)
command_report2=GenerateReportCommand2(job_report2)
runner2.queue_job(command_email2)
runner2.queue_job(command_report2)

task2=runner2.execute_job()

next(task2)
next(task2)

####version 3

def send_email(recipient,subject,body):
    print(f"sending email to {recipient}")

def generate_report(report_type,start_date,end_date):
    print(f"generate report from {start_date}-{end_date}")

def resize_image(path,width,height):
    print(f"resizing image at {path}")

queue:list[Any]=[]
history=[]

def jobrunner():
    while queue:
        job=queue.pop(0)
        history.append(job)
        yield job()

job_email3:Any=lambda:send_email("nahom","hi hi","how are you")
job_report3:Any=lambda:generate_report("yearly","may-5-2026","may-5-2027")

queue.append(job_email3)
queue.append(job_report3)

task=jobrunner()

next(task)
next(task)