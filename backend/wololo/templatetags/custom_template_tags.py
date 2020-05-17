from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def keyvalue(dict, key):    
    return dict[key]

@register.filter
@stringfilter
def humanizeCamelCase(givenString):
    upperCaseLetterIndex = None
    print(givenString)
    i = 0
    for letter in givenString:
        if(letter.isupper()):
            upperCaseLetterIndex = i
            break
        i+=1
    if upperCaseLetterIndex is not None:
        return givenString[0:upperCaseLetterIndex].capitalize() + ' ' + givenString[upperCaseLetterIndex:len(givenString)].capitalize()
    else:
        return givenString.capitalize()