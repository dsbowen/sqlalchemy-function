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
</style># Function mixin

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##sqlalchemy_function.**FunctionMixin**

<p class="func-header">
    <i>class</i> sqlalchemy_function.<b>FunctionMixin</b>(<i>parent=None, func=None, args=[], kwargs={}</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/sqlalchemy-function/sqlalchemy_function/function_mixin.py#L8">[source]</a>
</p>

A mixin for 'Function models'. When called, a Function model executes its
function, passing in its parent (if applicable) and its args and kwargs.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>parent : <i>usually a database model or None, default=None</i></b>
<p class="attr">
    The Function model's parent is usually a database model which subclasses a <code>sqlalchemy.ext.declarative.declarative_base()</code>.
</p>
<b>func : <i>callable or None, default=None</i></b>
<p class="attr">
    The function which the Function model will execute when called.
</p>
<b>args : <i>iterable, default=[]</i></b>
<p class="attr">
    Arguments which the Function model will pass into its <code>func</code> when called.
</p>
<b>kwargs : <i>dict, default={}</i></b>
<p class="attr">
    Keyword arguments which the Function model will pass into its <code>func</code> when called.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>parent : <i>usually a database model of None</i></b>
<p class="attr">
    Set from the <code>parent</code> parameter.
</p>
<b>func : <i>callable sqlalchemy.PickleType</i></b>
<p class="attr">
    Set from the <code>func</code> parameter.
</p>
<b>args : <i>sqlalchemy_mutable.MutableListType</i></b>
<p class="attr">
    Set from the <code>args</code> parameter.
</p>
<b>kwargs : <i>sqlalchemy_mutable.MutableDictType</i></b>
<p class="attr">
    Set from the <code>kwargs</code> parameter.
</p></td>
</tr>
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

We can now store and later call functions as follows.

```python
def foo(parent, *args, **kwargs):
    print('My parent is', parent)
    print('My args are', args)
    print('My kwargs are', kwargs)
    return 'return value'

parent = Parent()
function = Function(
    parent, func=foo, args=['hello world'], kwargs={'goodbye': 'moon'}
)
parent.functions[0]()
```

Out:

```
My parent is <__main__.Parent object at 0x7f2bb5c12518>
My args are ('hello world',)
My kwargs are {'goodbye': 'moon'}
'return value'
```

####Methods



<p class="func-header">
    <i></i> <b>register</b>(<i>cls, func</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/sqlalchemy-function/sqlalchemy_function/function_mixin.py#L118">[source]</a>
</p>

Class method which registers a function with the Function model. This simplifies the syntax for creating Function models and associating them with their parents.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>func : <i>callable</i></b>
<p class="attr">
    The registered function.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>func : <i>callable</i></b>
<p class="attr">
    Original <code>func</code> parameter.
</p></td>
</tr>
    </tbody>
</table>

####Examples

Follow the setup above.

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
My parent is <__main__.Parent object at 0x7f2bc4269588>
My args are ('hello world',)
My kwargs are {'goodbye': 'moon'}
'return value'
```



<p class="func-header">
    <i></i> <b>__call__</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/sqlalchemy-function/sqlalchemy_function/function_mixin.py#L164">[source]</a>
</p>

Call `self.func`, passing in `self.parent` (if applicable) and
`*self.args, **self.kwargs`.

**Note.** If the arguments or keyword arguments contain database models,
they will be 'unshelled' when they are passed into the function. See
<https://dsbowen.github.io/sqlalchemy-mutable> for more detail.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>output : <i></i></b>
<p class="attr">
    Output of <code>self.func</code>.
</p></td>
</tr>
    </tbody>
</table>

