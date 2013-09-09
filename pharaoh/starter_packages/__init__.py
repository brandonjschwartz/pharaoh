from pyramid.scaffolds import PyramidTemplate


class SqlAlchemyPkg(PyramidTemplate):
    template_dir = 'sqlalchemy'
    summary = 'Sqlalchemy base package.'