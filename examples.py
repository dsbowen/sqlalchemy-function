"""SQLAlchemy-Function examples"""

"""Setup for Example 1: Basic use"""
# 1. import FunctionMixin and FunctionBase
from sqlalchemy_function import FunctionMixin, FunctionBase

# 2. Standard session creation
from sqlalchemy import create_engine, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.orderinglist import ordering_list

engine = create_engine('sqlite:///:memory:')
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()
Base = declarative_base()

# 3. Create a Function model with the FunctionMixin
class Function(FunctionMixin, Base):
    __tablename__ = 'function'
    id = Column(Integer, primary_key=True)

# 4. Create the database
Base.metadata.create_all(engine)

"""Example 1"""
def foo(*args, **kwargs):
    print('My arguments are:', args)
    print('My keyword arguments are:', kwargs)
    return 'hello world'

print('\nExample 1: Basic use')
f = Function(func=foo, args=['hello moon'], kwargs={'hello': 'star'})
session.add(f)
session.commit()
print(f())

"""Additional Setup for Examples 2-4: Function parents"""
class Child(FunctionMixin, Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parent.id'))

# 4. Define a Parent model with the FunctionBase mixin
class Parent(FunctionBase, Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)

    # 5. Fuction models must reference their parent with a 'parent' attribute
    functions = relationship(
        'Child',
        backref='parent',
        order_by='Child.index',
        collection_class=ordering_list('index')
    )

    # 6. Call _set_function_relationships before setting function attributes
    def __init__(self):
        self._set_function_relationships()

Base.metadata.create_all(engine)

print('\nExample 2: Function models with parents (basic use)')
def foo(parent, *args, **kwargs):
    print('My parent is:', parent)
    print('My arguments are:', args)
    print('My keyword arguments are:', kwargs)
    return 'hello world'

p = Parent()
session.add(p)
session.commit()
f = Function(
    parent=p, func=foo, args=['hello moon'], kwargs={'hello': 'star'}
)
print(f())

print('\nExample 3: Automatic conversion of functions to Function models')
p.functions.clear()
p.functions = foo
print(p.functions)
print(p.functions[0]())

print('\nExample 4: Automatic conversion of a list of functions to a list of Function mdoels')
def bar(parent):
    return 'goodbye world'

p.functions.clear()
p.functions = [foo, bar]
print(p.functions)
[print(f()) for f in p.functions]