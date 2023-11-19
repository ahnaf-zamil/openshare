from ariadne import ObjectType
from graphql import GraphQLSchema
from typing import List, Type


class ResolverGroup(ObjectType):
    """Custom class to nest multiple resolver object types into a single entity"""

    def __init__(self, *args) -> None:
        self._resolvers: List[ObjectType] = [i() for i in args]

    def field(self, field_name: str, obj_type: Type[ObjectType]):
        """Decorator for assigning resolvers to respective object types"""
        obj = [i for i in self._resolvers if isinstance(i, obj_type)][0]

        def wrapper(func):
            obj.set_field(field_name, func)

        return wrapper

    def bind_to_schema(self, schema: GraphQLSchema) -> None:
        """Overrides method of parent class to bind every resolver in the group to its respective schema"""
        for i in self._resolvers:
            i.bind_to_schema(schema)
