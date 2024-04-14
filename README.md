# tidyworkflow

TidyWorkFlow is the package for validating self-documenting code. It promotes a coding structure that is heavily inspired by functional programming and Python's usage of decorators. With minor modifications to an existing set of functions, any workflow can become a tidyworkflow, providing out-of-the-box support for logging, validation, and consistent function definitions.

## Example

Basic usage involves wrapping a series of documented, modular function. All arguments - if any - are passed to the decorated function and accessed in their respective functions. Each step is logged to the console, and the output is returned if it satisfies the validations.

```{python}
@tidyworkflow(
    message="Normalizes a string using the following steps:",
    validators=[lambda x: isinstance(x, str), lambda x: x == '@x@mpl@ str@ng']
)
def normalize_string_format(string, **kwargs):
    def remove_whitespace(string, **kwargs):
        '''Select/filter raw data to get working version of dataset'''
        return string.strip()

    def replace_vowels(string, **kwargs):
        '''Replace vowels with specific character (default '@')'''
        import re
        replacement = kwargs.get('replacement', '@')
        return re.sub('[aeiou]', repl=replacement, string=string, flags=re.IGNORECASE)

    def convert_to_case(string, **kwargs):
        '''Convert case using string method (default "lower")'''
        case_func = kwargs.get('case', 'lower')
        return getattr(str, case_func)(string)

    return locals()

>>> clean_string = normalize_string_format(string='EXamPle String')
INFO     | __main__:wrapper:43 - #> (normalize_string_format) Normalizes a string using the following steps:
INFO     | __main__:wrapper:60 - #>	(01) Remove whitespace characters from string
INFO     | __main__:wrapper:60 - #>	(02) Replace vowels with specific character (default: '@')
INFO     | __main__:wrapper:60 - #>	(03) Convert case using string method (default: 'lower')
>>> clean_string
"@x@mpl@ str@ng"
```

Users can control the execution of the workflow. As of development, support for ignoring nested functions is possible with the `@tidyignore` decorator.

```{python}
@tidyworkflow(
    message="Normalizes a string using the following steps:",
    validators=[lambda x: isinstance(x, str), lambda x: x == '@x@mpl@ str@ng']
)
def normalize_string_format(string, **kwargs):
    
    @tidyignore
    def remove_whitespace(string, **kwargs):
        """Remove whitespace characters from string"""
        return string.strip()

    def replace_vowels(string, **kwargs):
        """Replace vowels with specific character (default: '@')"""
        import re
        replacement = kwargs.get('replacement', '@')
        return re.sub('[aeiou]', repl=replacement, string=string, flags=re.IGNORECASE)

    def convert_to_case(string, **kwargs):
        """Convert case using string method (default: 'lower')"""
        # call tdf.utils.map_input_fields?
        case_func = kwargs.get('case', 'lower')
        return getattr(str, case_func)(string)

    return locals()

>>> clean_string = normalize_string_format(string='EXamPle String')
INFO     | __main__:wrapper:43 - #> (normalize_string_format) Normalizes a string using the following steps:
WARNING  | __main__:wrapper:60 - #>	(01) Skipping remove_whitespace
INFO     | __main__:wrapper:60 - #>	(02) Replace vowels with specific character (default: '@')
INFO     | __main__:wrapper:60 - #>	(03) Convert case using string method (default: 'lower')
>>> clean_string
"@x@mpl@ str@ng"
```
