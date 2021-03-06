SQLAlchemy-Function defines a [SQLALchemy Mixin](https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/mixins.html) for creating Function models.

A Function model has a parent (optional), a function, arguments, and keyword arguments. When called, the Function model executes its function, passing in its parent (if applicable), its arguments, and its keyword arguments.

## Installation

```
$ pip install sqlalchemy-function
```

## Quickstart

In the setup, we create a SQLAlchemy session, define a Parent model 
subclassing `FunctionRelator`, and a Function model subclassing 
`FunctionMixin`.

```python
from sqlalchemy_function import FunctionMixin, FunctionRelator

from sqlalchemy import create_engine, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

# standard session creation
engine = create_engine('sqlite:///:memory:')
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()
Base = declarative_base()

# define a Function model parent
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

We can now register, store, and call functions as follows.

```python
@Function.register
def foo(parent, *args, **kwargs):
    print('My parent is', parent)
    print('My args are', args)
    print('My kwargs are', kwargs)
    return 'return value'

parent = Parent()
Function.foo(parent, 'hello world', goodbye='moon')
parent.functions[0]()
```

Out:

```
My parent is <__main__.Parent object at 0x7f8b4d200518>
My args are ('hello world',)
My kwargs are {'goodbye': 'moon'}
'return value'
```

## Citation

```
@software{bowen2020sqlalchemy-function,
  author = {Dillon Bowen},
  title = {SQLAlchemy-Function},
  url = {https://dsbowen.github.io/sqlalchemy-function/},
  date = {2020-06-05},
}
```

## License

Users must cite this package in any publications which use it.

It is licensed with the MIT [License](https://github.com/dsbowen/sqlalchemy-function/blob/master/LICENSE).