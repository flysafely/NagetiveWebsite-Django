from django import template
register = template.Library()

@register.tag(name="Split_String")
def Do_Split_String(parser,token):
    try:
        tag_name,stringValue,KeyValue=token.split_contents()
        print(tag_name,stringValue,KeyValue)
    except ValueError:
        msg = '%r tag requires a single argument' % token.split_contents()[0]
        raise template.TemplateSyntaxError(msg)
    return stringValue.split(KeyValue[1:-1])[0]
