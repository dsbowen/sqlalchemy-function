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
</style># Function relator mixin

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##sqlalchemy_function.**FunctionRelator**



Base for database models with relationships to Function models. It
provides automatic conversion of functions to Function models when
setting attributes.

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

# standard session creation
from sqlalchemy import create_engine, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///:memory:')
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()
Base = declarative_base()

# subclass `FunctionRelator` for models with a relationship to Function models
class Parent(FunctionRelator, Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    functions = relationship('Function', backref='parent')

# subclass `FunctionMixin` to define a Function model
class Function(FunctionMixin, Base):
    __tablename__ = 'function'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parent.id'))

Base.metadata.create_all(engine)
```

We can now set the `functions` attribute to a callable as follows.

```python
def foo(*args, **kwargs):
    print('My args are', args)
    print('My kwargs are', kwargs)
    return 'return value'

parent = Parent()
parent.functions = foo
# equivalent to:
# parent.functions = [foo]
# parent.functions = Function(foo)
# parent.functions = [Function(foo)]
parent.functions
```

Out:

```
[<__main__.Function object at 0x7f4e5a49c160>]
```

