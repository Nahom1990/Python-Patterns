"""
Now you code.

Build a generic data-processing engine using higher-order functions.

Your engine should process a list of numbers through different behaviors.

Requirements
"""
numbers = [2, 5, 8, 10, 15]

def double(x):
    return x*2

def square(x):
    return x**2

def add_five(x):
    return x+5


def apply_transforamtion(list_of_nums,transformation):
    return [transformation(x) for x in list_of_nums]

new_numbers=apply_transforamtion(numbers,double)
print(new_numbers)
"""
Create:

numbers = [2, 5, 8, 10, 15]

Create at least three transformation functions, for example:

double
square
add_five

Then create a higher-order function:

apply_transformation(numbers, transformation)

It should receive:

a list of numbers
a function describing the transformation

and return the transformed list.

For example conceptually:

numbers
   ↓
apply_transformation()
   ↓
double()
   ↓
new list

Then you should be able to do things like:

apply_transformation(numbers, double)
apply_transformation(numbers, square)
apply_transformation(numbers, add_five)
Important constraints

Do not create:

if transformation == "double":
    ...
elif transformation == "square":
    ...

The transformation itself must be supplied as a function.

"""
transforamtions=[double,square,add_five]
def process_pipeline(numbers,transformations):
    new_numbers=numbers
    for transformation in transformations:
        new_numbers=apply_transforamtion(new_numbers,transformation)

    return new_numbers



        

"""

Then add a second higher-order function:

process_pipeline(numbers, transformations)

where transformations is a list of functions.

For example:

[
    double,
    square,
    add_five
]

The pipeline should execute them sequentially:

[2, 5, 8]
   ↓
double
   ↓
[4, 10, 16]
   ↓
square
   ↓
[16, 100, 256]
   ↓
add_five
   ↓
[21, 105, 261]

Do not mutate the original numbers list.
"""