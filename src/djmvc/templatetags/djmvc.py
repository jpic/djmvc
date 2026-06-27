import re

from django import template
from django.template.base import token_kwargs, Variable
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()

SAFE_ATTR_NAME = re.compile(r'^[a-zA-Z][\w-]*$')


@register.filter
def html_attributes(attrs):
    if not attrs:
        return ''
    parts = []
    for key, value in attrs.items():
        if not SAFE_ATTR_NAME.match(key):
            continue
        if value is True:
            parts.append(key)
        elif value is False:
            parts.append(f'{key}="false"')
        else:
            parts.append(f'{key}="{escape(value)}"')
    return mark_safe(' '.join(parts))


@register.filter
def unpoly_attributes(view, context=''):
    fn = getattr(view, 'unpoly_attributes', None)
    if fn is None:
        return {}
    return fn(context)


@register.tag(name='eval')
def do_eval(parser, token):
    bits = token.split_contents()

    if len(bits) < 4:
        raise template.TemplateSyntaxError(
            "%r tag requires at least 3 arguments: the callable, "
            "optional arguments, and 'as variable_name'" % bits[0]
        )

    tag_name = bits[0]

    try:
        as_index = bits.index('as')
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires 'as variable_name' at the end" % tag_name
        )

    if as_index < 2:
        raise template.TemplateSyntaxError(
            "%r tag requires a callable before 'as'" % tag_name
        )

    if as_index >= len(bits) - 1:
        raise template.TemplateSyntaxError(
            "%r tag requires a variable name after 'as'" % tag_name
        )

    callable_expr = bits[1]
    arg_bits = bits[2:as_index]
    var_name = bits[as_index + 1]

    args = []
    kwargs = {}

    for bit in arg_bits:
        if '=' in bit and not (bit.startswith('"') or bit.startswith("'")):
            kwarg_dict = token_kwargs([bit], parser)
            kwargs.update(kwarg_dict)
        else:
            args.append(parser.compile_filter(bit))

    callable_var = Variable(callable_expr)

    return EvalNode(callable_var, args, kwargs, var_name)


class EvalNode(template.Node):
    def __init__(self, callable_var, args, kwargs, var_name):
        self.callable_var = callable_var
        self.args = args
        self.kwargs = kwargs
        self.var_name = var_name

    def render(self, context):
        callable_obj = self._resolve_variable_path(self.callable_var, context)

        resolved_args = [arg.resolve(context) for arg in self.args]

        resolved_kwargs = {
            key: val.resolve(context)
            for key, val in self.kwargs.items()
        }

        try:
            result = callable_obj(*resolved_args, **resolved_kwargs)
        except Exception:
            if context.template.engine.debug:
                raise
            result = None

        context[self.var_name] = result

        return ''

    def _resolve_variable_path(self, variable, context):
        current = context

        parts = variable.var.split('.')

        for i, part in enumerate(parts):
            try:
                current = current[part]
            except (TypeError, KeyError, AttributeError):
                try:
                    current = getattr(current, part)
                except AttributeError:
                    try:
                        current = current[int(part)]
                    except (ValueError, KeyError, TypeError, IndexError):
                        return ''

            if callable(current) and i < len(parts) - 1:
                try:
                    current = current()
                except TypeError:
                    pass

        return current