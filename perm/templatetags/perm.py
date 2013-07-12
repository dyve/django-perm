from __future__ import unicode_literals

import re

from django.db.models import Model
from django.template import Library, Node, TemplateSyntaxError, Variable, VariableDoesNotExist
from django.utils.translation import ugettext_lazy

from ..utils import get_model


QUOTED_STRING = re.compile(r'^["\'](?P<noquotes>.+)["\']$')

register = Library()


def handle_var(value, context):
    stringval = QUOTED_STRING.search(value)
    if stringval:
        return stringval.group('noquotes')
    else:
        try:
            return Variable(value).resolve(context)
        except VariableDoesNotExist:
            return value


@register.tag
def ifperm(parser, token):
    # Separate tag name and parameters
    try:
        parts = token.split_contents()
        tag = parts[0]
        perm = parts[1]
        try:
            obj_or_model = parts[2]
        except IndexError:
            obj_or_model = None
    except (ValueError, TypeError):
        raise TemplateSyntaxError(ugettext_lazy("'%(tag)s' tag takes two parameters") % {'tag': tag})

    default_states = ['ifperm', 'else']
    end_tag = 'endifperm'

    # Place to store the states and their values
    states = {}

    # Let's iterate over our context and find our tokens
    while token.contents != end_tag:
        current = token.contents
        states[current.split()[0]] = parser.parse(default_states + [end_tag])
        token = parser.next_token()

    return PermNode(states, perm, obj_or_model)


class PermNode(Node):
    def __init__(self, states, perm, obj_or_model):
        self.states = states
        self.perm = perm
        self.obj_or_model = obj_or_model

    def render(self, context):
        perm = handle_var(self.perm, context)
        model = handle_var(self.obj_or_model, context)

        if not isinstance(model, Model):
            model = get_model(model, raise_exception=True)

        if context['request'].user.has_perm(perm, model):
            index = 'ifperm'
        else:
            index = 'else'

        try:
            return self.states[index].render(context)
        except KeyError:
            return ''
