import binascii
import os
from textwrap import dedent

from pyramid.compat import native_

from pharaoh.package import Package


class PharaohPackage(Package):
    """
     A class that can be used as a base class for Pyramid scaffolding
     templates.
    """
    def pre(self, command, output_dir, vars):
        """ Overrides :meth:`pyramid.scaffolds.template.Template.pre`, adding
        several variables to the default variables list (including
        ``random_string``, and ``package_logger``).  It also prevents common
        misnamings (such as naming a package "site" or naming a package
        logger "root".
        """
        if vars['package'] == 'site':
            raise ValueError('Sorry, you may not name your package "site". '
                             'The package name "site" has a special meaning in '
                             'Python.  Please name it anything except "site".')
        vars['random_string'] = native_(binascii.hexlify(os.urandom(20)))
        package_logger = vars['package']
        if package_logger == 'root':
            # Rename the app logger in the rare case a project is named 'root'
            package_logger = 'app'
        vars['package_logger'] = package_logger
        return Package.pre(self, command, output_dir, vars)

    def post(self, command, output_dir, vars): # pragma: no cover
        separator = "=" * 79
        msg = dedent(
            """
            %(separator)s
            Installation successful.
            %(separator)s
        """ % {'separator': separator})

        self.out(msg)
        return Package.post(self, command, output_dir, vars)

    def out(self, msg): # pragma: no cover (replaceable testing hook)
        print(msg)


class SqlAlchemyPkg(PharaohPackage):
    _package_dir = 'sqlalchemy'
    summary = 'Sqlalchemy base package.'