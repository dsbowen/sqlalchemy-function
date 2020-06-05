from docstr_md.python import PySoup, compile_md
from docstr_md.src_href import Github

src_href = Github('https://github.com/dsbowen/sqlalchemy-function')

path = 'sqlalchemy_function/function_mixin.py'
soup = PySoup(path=path, parser='sklearn', src_href=src_href)
soup.import_path = 'sqlalchemy_function'
compile_md(soup, compiler='sklearn', outfile='docs_md/function_mixin.md')

path = 'sqlalchemy_function/function_relator.py'
soup = PySoup(path=path, parser='sklearn', src_href=src_href)
soup.import_path = 'sqlalchemy_function'
compile_md(soup, compiler='sklearn', outfile='docs_md/function_relator.md')