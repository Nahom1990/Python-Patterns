"""
You're going to build your own reusable functional pipeline.

We have user input:

name = "   nahom mekuria   "

Create these functions:

1. remove_extra_spaces(text)

Should remove unnecessary spaces from the beginning/end and between words.

Example:

"   nahom    mekuria   "

becomes:

"nahom mekuria"
2. capitalize_words(text)

Should produce:

"Nahom Mekuria"
3. add_prefix(text)

Should produce:

"User: Nahom Mekuria"


4. Build pipe(*functions)

It should return a reusable function.

Example:

process_name = pipe(
    remove_extra_spaces,
    capitalize_words,
    add_prefix
)

Then:

process_name("   nahom    mekuria   ")

should produce:

User: Nahom Mekuria
🔥 Bonus Challenge

Create:

compose(*functions)

Then demonstrate that:

compose(
    add_prefix,
    capitalize_words,
    remove_extra_spaces
)

produces the same result.

Think carefully about why the function order is reversed."""

name= "   nahom mekuria   "

def remove_extra_spaces(text):
    return " ".join(text.split())

def capitalize_words(text):
    return text.title()

def add_prefix(text):
    return f"user: {text}"


def pipe(*functions):
    def piped(text):
        for func in functions:
            text=func(text)
        return text
    return piped

functions=[remove_extra_spaces,capitalize_words,add_prefix]
pipeline=pipe(*functions)
final_text=pipeline(name)
print(final_text)

def compose(*functions):
    def composed(text):
        for func in reversed(functions):
            text=func(text)
        return text
    return composed

c=compose(*reversed(functions))
final_text2=c(name)
print(final_text2)
