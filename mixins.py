from attr import attrs


@attrs(auto_attribs=False)
class OrderMixin:
    order: int = int()


@attrs(auto_attribs=False)
class IdentityMixin:
    id: int = int()


@attrs(auto_attribs=False)
class ParentMixin:
    parent: int = int()

