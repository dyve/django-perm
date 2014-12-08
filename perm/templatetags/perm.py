from __future__ import unicode_literals

import re

from django.db.models import Model
from django.template import Library, Node, TemplateSyntaxError, Variable, VariableDoesNotExist

from ..utils import get_model_for_perm


QUOTED_STRING = re.compile(r'^["\'](?P<noquotes>.+)["\']$')

register = Library()


def handle_var(value, context):
    if not value:
        return None
    stringval = QUOTED_STRING.search(value)
    if stringval:
        return stringval.group('noquotes')
    else:
        try:
            return Variable(value).resolve(context)
        except VariableDoesNotExist:
            return value


def handle_perm(parser, token):
    parts = token.split_contents()
    tag = parts[0]
    num_parts = len(parts)
    if num_parts > 1 and parts[num_parts - 2] == 'as':
        context_var = parts.pop()
        parts.pop()  # 'as'
        num_parts -= 2
    else:
        context_var = None
    if num_parts > 3:
        raise TemplateSyntaxError("Too many arguments for '{tag}' tag ({num})".format(tag=tag, num=num_parts))
    try:
        perm = parts[1]
    except IndexError:
        raise TemplateSyntaxError("Tag '{tag}' takes at least one parameter".format(tag=tag))
    try:
        obj_or_model = parts[2]
    except IndexError:
        obj_or_model = None
    return tag, perm, obj_or_model, context_var


def get_permission(tag, perm, obj_or_model, context):
    perm = handle_var(perm, context)
    model = handle_var(obj_or_model, context)
    if model and not isinstance(model, Model):
        model = get_model_for_perm(model, raise_exception=True)
    try:
        request = context['request']
    except IndexError:
        raise TemplateSyntaxError("Tag '%(tag)' requires request context".format(tag=tag))
    try:
        user = request.user
    except AttributeError:
        raise TemplateSyntaxError("Tag '%(tag)' requires attribute 'user' in request context".format(tag=tag))
    if model:
        return user.has_perm(perm, model)
    return user.has_perm(perm)


@register.tag
def perm(parser, token):
    tag, perm, obj_or_model, context_var = handle_perm(parser, token)
    return PermNode(perm, obj_or_model, context_var)


@register.tag
def ifperm(parser, token):
    tag, perm, obj_or_model, context_var = handle_perm(parser, token)
    # States
    default_states = ['ifperm', 'else']
    end_tag = 'endifperm'
    # Place to store the states and their values
    states = {}
    # Iterate over our context and find tokens
    while token.contents != end_tag:
        current = token.contents
        states[current.split()[0]] = parser.parse(default_states + [end_tag])
        token = parser.next_token()
    # Return node
    return IfPermNode(states, perm, obj_or_model)


class PermNode(Node):
    def __init__(self, perm, obj_or_model, context_var):
        self.perm = perm
        self.obj_or_model = obj_or_model
        self.context_var = context_var

    def render(self, context):
        result = get_permission('perm', self.perm, self.obj_or_model, context)
        if self.context_var:
            context[self.context_var] = result
            return ''
        return result


class IfPermNode(Node):
    def __init__(self, states, perm, obj_or_model):
        self.states = states
        self.perm = perm
        self.obj_or_model = obj_or_model

    def render(self, context):
        result = get_permission('perm', self.perm, self.obj_or_model, context)
        if result:
            index = 'ifperm'
        else:
            index = 'else'
        try:
            return self.states[index].render(context)
        except KeyError:
            return ''
