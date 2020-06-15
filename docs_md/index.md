# SQLAlchemy-Function

SQLAlchemy-Function defines a [SQLALchemy Mixin](https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/mixins.html) for creating Function models.

A Function model has a function, arguments, and keyword arguments. When called, the Function model executes its function, passing in its arguments and keyword arguments.

## Installation

```
$ pip install sqlalchemy-function
```

## Quickstart

In the setup, we create a SQLAlchemy session and a Function model  
subclassing `FunctionMixin`.

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

# subclass `FunctionMixin` to define a Function model
class Function(FunctionMixin, Base):
    __tablename__ = 'function'
    id = Column(Integer, primary_key=True)

Base.metadata.create_all(engine)
```

We can now store and later call functions as follows.

```python
def foo(*args, **kwargs):
    print('My args are', args)
    print('My kwargs are', kwargs)
    return 'return value'

func = Function(foo, 'hello world', goodbye='moon')
func()
```

Out:

```
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
  date = {2020-06-15},
}
```

## License

Users must cite this package in any publications which use it.

It is licensed with the MIT [License](https://github.com/dsbowen/sqlalchemy-function/blob/master/LICENSE).