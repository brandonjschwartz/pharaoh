from pyramid.scaffolds import PyramidTemplate


class SqlAlchemyPkg(PyramidTemplate):
    _template_dir = 'sqlalchemy'
    summary = 'Sqlalchemy base package.'