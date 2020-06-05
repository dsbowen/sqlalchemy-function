<script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript"></script>

<link rel="stylesheet" href="https://assets.readthedocs.org/static/css/readthedocs-doc-embed.css" type="text/css" />

<style>
    a.src-href {
        float: right;
    }
    p.attr {
        margin-top: 0.5em;
        margin-left: 1em;
    }
    p.func-header {
        background-color: gainsboro;
        border-radius: 0.1em;
        padding: 0.5em;
        padding-left: 1em;
    }
    table.field-table {
        border-radius: 0.1em
    }
</style>##sqlalchemy_function.**FunctionRelator**



Base for database models with relationships to Function models. It provides
automatic conversion of functions to Function models when setting attributes.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>

####Examples

In the setup, we create a SQLAlchemy session, define a Parent model
subclassing `FunctionRelator`, and a Function model subclassing
`FunctionMixin`.

```python
from sqlalchemy_function import FunctionMixin, FunctionRelator

from sqlalchemy import create_engine, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.orderinglist import ordering_list

# standard session creation
engine = create_engine('sqlite:///:memory:')
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()
Base = declarative_base()

# define a Parent model with the FunctionRelator
class Parent(FunctionRelator, Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)

    # Fuction models must reference their parent with a `parent` attribute
    functions = relationship('Function', backref='parent')

# define a Function model with the FunctionMixin
class Function(FunctionMixin, Base):
    __tablename__ = 'function'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parent.id'))

Base.metadata.create_all(engine)
```

We can now set the `functions` attribute to a callable as follows.

```python
def foo(parent, *args, **kwargs):
    print('My parent is', parent)
    print('My args are', args)
    print('My kwargs are', kwargs)
    return 'return value'

parent.functions = foo
# equivalent to:
# parent.functions = [foo]
# parent.functions = Function(func=foo)
print(parent.functions)
```

Out:

```
[<__main__.Function object at 0x7f4e5a49c160>]
```

