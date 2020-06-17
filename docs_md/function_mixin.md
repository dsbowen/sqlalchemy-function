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
    <i>class</i> sqlalchemy_function.<b>FunctionMixin</b>(<i>func, *args, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/sqlalchemy-function/sqlalchemy_function/function_mixin.py#L8">[source]</a>
</p>

A mixin for 'Function models'. When called, a Function model executes its
function, passing in its arguments and keyword arguments.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>func : <i>callable or None, default=None</i></b>
<p class="attr">
    The function which the Function model will execute when called.
</p>
<b>*args, **kwargs : <i></i></b>
<p class="attr">
    Arguments and keyword arguments which the Function model will pass into its <code>func</code> when called. The <code>FunctionMixin</code> constructor will not override arguments and keyword arguments if they have already been set.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>func : <i>callable sqlalchemy.PickleType</i></b>
<p class="attr">
    Set from the <code>func</code> parameter.
</p>
<b>args : <i>sqlalchemy_mutable.MutableListType</i></b>
<p class="attr">
    Set from the <code>*args</code> parameter.
</p>
<b>kwargs : <i>sqlalchemy_mutable.MutableDictType</i></b>
<p class="attr">
    Set from the <code>**kwargs</code> parameter.
</p></td>
</tr>
    </tbody>
</table>

####Examples

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

####Methods



<p class="func-header">
    <i></i> <b>set</b>(<i>self, func, *args, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/sqlalchemy-function/sqlalchemy_function/function_mixin.py#L93">[source]</a>
</p>

Set the function, arguments, and keyword arguments.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>func : <i>callable or None, default=None</i></b>
<p class="attr">
    The function which the Function model will execute when called.
</p>
<b>*args, **kwargs : <i></i></b>
<p class="attr">
    Arguments and keyword arguments which the Function model will pass into its <code>func</code> when called.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>self : <i>sqlalchemy_function.FunctionMixin</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>__call__</b>(<i>self, *args, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/sqlalchemy-function/sqlalchemy_function/function_mixin.py#L113">[source]</a>
</p>

Call `self.func`, passing in `*self.args, **self.kwargs`.

Additional arguments passed to `self.__call__` are prepended to
`self.args`, and additional keyword arguments update `self.kwargs`
before passing to `self.func`. The function call is essentially:

```python
kwargs_ = self.kwargs.copy()
kwargs_.update(kwargs)
self.__call__(*args, *self.args, **kwargs_)
```

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>*args, **kwargs : <i></i></b>
<p class="attr">
    Additional arguments and keyword arguments passed to <code>self.func</code>.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>output : <i></i></b>
<p class="attr">
    Output of <code>self.func</code>.
</p></td>
</tr>
    </tbody>
</table>

####Notes

If the arguments or keyword arguments contain database models, they
will be 'unshelled' when they are passed into the function. See
<https://dsbowen.github.io/sqlalchemy-mutable/> for more detail.