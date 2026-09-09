"""1. The core idea

So far, we used closures mainly for configuration:

def create_validator(minimum_age):
    def validate(age):
        return age >= minimum_age

    return validate

Here, minimum_age is captured configuration.

But closures can do something more interesting:

A closure can remember and update state between function calls.

For example:

def create_counter():
    count = 0

    def increment():
        nonlocal count
        count += 1
        return count

    return increment

Now:

counter = create_counter()

print(counter())  # 1
print(counter())  # 2
print(counter())  # 3

The surprising part is:

create_counter()

has already finished.

Normally you might think count should disappear.

But it doesn't.

The returned function still has access to the captured count.

2. Why nonlocal matters

Consider:

def create_counter():
    count = 0

    def increment():
        count += 1
        return count

    return increment

This doesn't work.

Python sees:

count += 1

inside increment() and treats count as a local variable of increment.

But you're trying to modify the count belonging to the enclosing function.

That's what nonlocal tells Python:

def create_counter():
    count = 0

    def increment():
        nonlocal count
        count += 1
        return count

    return increment

Think:

global
   ↓
create_counter frame
   ↓
count = 0
   ↓
increment closure

nonlocal means:

"Don't create a new local count. Modify the one from my enclosing scope."""









"""4. One closure instance vs another

This is where closures become particularly powerful.

deposit1, withdraw1 = create_account(100)
deposit2, withdraw2 = create_account(500)

These are independent.

deposit1(50)
# 150

deposit2(50)
# 550

They don't share the same balance.

Conceptually:

Account 1 closure
balance = 150
   │
   ├── deposit1
   └── withdraw1


Account 2 closure
balance = 550
   │
   ├── deposit2
   └── withdraw2

Each invocation of the factory creates a new state environment.

This is very similar to creating two objects:

account1 = Account(100)
account2 = Account(500)

But the closure version doesn't require a class.

5. Closures vs classes — now with state

This distinction becomes more interesting now.

Class
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1
        return self.count
Closure
def create_counter():
    count = 0

    def increment():
        nonlocal count
        count += 1
        return count

    return increment

Both can produce:

counter()
# 1

counter()
# 2

counter()
# 3

But they expose state differently.

With the class:

counter.count

is accessible.

With the closure:

counter.count

doesn't exist.

The state is encapsulated inside the closure.

That can actually be desirable.

6. A professional backend example

Imagine a rate limiter.

You want to allow a function to execute only a certain number of times.

We could create:

def create_rate_limiter(max_calls):
    calls = 0

    def allow():
        nonlocal calls

        if calls >= max_calls:
            return False

        calls += 1
        return True

    return allow

Now:

api_limiter = create_rate_limiter(3)

print(api_limiter())  # True
print(api_limiter())  # True
print(api_limiter())  # True
print(api_limiter())  # False

The closure remembers:

calls = 3

without exposing that variable.

This is a realistic use of the pattern, although production rate limiting would usually involve shared infrastructure such as Redis when multiple processes/servers are involved.

7. Another important example — generating IDs

Suppose you need a local ID generator.

def create_id_generator(start=1):
    current = start

    def generate():
        nonlocal current

        value = current
        current += 1

        return value

    return generate

Then:

generate_user_id = create_id_generator(1000)

print(generate_user_id())  # 1000
print(generate_user_id())  # 1001
print(generate_user_id())  # 1002

Again:

Factory
   ↓
create_id_generator(1000)
   ↓
current = 1000
   ↓
generate()

Each call modifies the remembered state.

8. The deeper FP question

This raises an important question:

Is a stateful closure a pure function?

No.

Our counter:

counter()

does not always produce the same result.

The first call gives:

1

The second gives:

2

even though we passed no arguments.

Therefore:

counter()

has hidden state.

That's a side effect/stateful behavior.

So why study this in Functional Programming?

Because FP isn't:

"Everything must be pure."

Professional functional programming is more nuanced.

We try to isolate state rather than allowing state to spread everywhere.

For example:

                  IMPURE / STATEFUL
                        │
                        ▼
              ┌──────────────────┐
              │ Stateful closure  │
              └──────────────────┘
                        │
                        ▼
                 Pure pipeline
                        │
                        ▼
                     Result

This is much easier to reason about than having global mutable variables scattered throughout an application.

9. The dangerous version: global state

Compare:

counter = 0

def increment():
    global counter
    counter += 1
    return counter

with:

def create_counter():
    count = 0

    def increment():
        nonlocal count
        count += 1
        return count

    return increment

The global version has a major problem:

everyone can potentially access the same state.

You could accidentally have:

counter = 0

function_a()
function_b()
function_c()

all interacting with the same global state.

With a closure:

counter_a = create_counter()
counter_b = create_counter()

you get isolated state.

That's a significant architectural advantage.

10. Closure as a tiny state machine

This is another very useful mental model.

Consider:

def create_session():
    state = "anonymous"

    def login():
        nonlocal state
        state = "authenticated"

    def logout():
        nonlocal state
        state = "anonymous"

    def get_state():
        return state

    return login, logout, get_state

Now:

login, logout, get_state = create_session()

print(get_state())
# anonymous

login()

print(get_state())
# authenticated

logout()

print(get_state())
# anonymous

You've essentially created a tiny state machine:

anonymous
    │
    │ login()
    ▼
authenticated
    │
    │ logout()
    ▼
anonymous

The closure owns the state.

11. A very important design principle

Don't immediately think:

"Closures are a replacement for classes."

That's too simplistic.

Instead:

Closure

Good when you have:

ONE main behavior
       +
small amount of private state/configuration

Example:

create_counter()
create_id_generator()
create_validator()
create_formatter()
Class

Better when you have:

multiple related behaviors
+
complex state
+
a meaningful object abstraction
+
inheritance/protocol integration
+
larger public API

For example, a real database session, HTTP client, repository, or complex domain object generally shouldn't be forced into a closure.

12. The key mental model

You've now seen three progressively more powerful uses of closures:

Level 1 — Configuration
create_validator(18)

The closure remembers:

minimum_age = 18
Level 2 — Specialized behavior
adult_validator = create_validator(18)
senior_validator = create_validator(65)

Each closure behaves differently.

Level 3 — Stateful behavior
counter = create_counter()

The closure remembers changing state:

count = 0
   ↓
count = 1
   ↓
count = 2
   ↓
count = 3

That's the important progression."""