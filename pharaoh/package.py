import re
import sys
import os

from pyramid.compat import (
    native_,
    bytes_,
)

from pyramid.scaffolds import copydir

fsenc = sys.getfilesystemencoding()


class Package(object):
    """ Inherit from this base class and override methods to use the Pharaoh packaging system."""
    copydir = copydir # for testing
    _package_dir = None

    def __init__(self, name):
        self.name = name

    def render_package(self, content, vars, filename=None):
        """ Return a bytestring representing a templated file based on the
        input (content) and the variable names defined (vars).  ``filename``
        is used for exception reporting."""
        # this method must not be named "template_renderer" fbo of extension
        # scaffolds that need to work under pyramid 1.2 and 1.3, and which
        # need to do "template_renderer =
        # staticmethod(paste_script_template_renderer)"
        content = native_(content, fsenc)
        try:
            return bytes_(
                substitute_escaped_double_braces(
                    substitute_double_braces(content, TypeMapper(vars))), fsenc)
        except Exception as e:
            _add_except(e, ' in file %s' % filename)
            raise

    def module_dir(self):
        mod = sys.modules[self.__class__.__module__]
        return os.path.dirname(mod.__file__)

    def package_dir(self):
        """ Return the template directory of the scaffold.  By default, it
        returns the value of ``os.path.join(self.module_dir(),
        self._template_dir)`` (``self.module_dir()`` returns the module in
        which your subclass has been defined).  If ``self._template_dir`` is
        a tuple this method just returns the value instead of trying to
        construct a path.  If _template_dir is a tuple, it should be a
        2-element tuple: ``(package_name, package_relative_path)``."""
        assert self._package_dir is not None, (
            "Package %r didn't set _package_dir" % self)
        if isinstance(self._package_dir, tuple):
            return self._package_dir
        else:
            return os.path.join(self.module_dir(), self._package_dir)

    def run(self, command, output_dir, vars):
        self.pre(command, output_dir, vars)
        self.write_files(command, output_dir, vars)
        self.post(command, output_dir, vars)

    def pre(self, command, output_dir, vars): # pragma: no cover
        """
        Called before package is applied.
        """
        pass

    def post(self, command, output_dir, vars): # pragma: no cover
        """
        Called after package is applied.
        """
        pass

    def write_files(self, command, output_dir, vars):
        package_dir = self.package_dir()
        if not self.exists(output_dir):
            self.out("Creating directory %s" % output_dir)
            if not command.options.simulate:
                # Don't let copydir create this top-level directory,
                # since copydir will svn add it sometimes:
                self.makedirs(output_dir)
        self.copydir.copy_dir(
            package_dir,
            output_dir,
            vars,
            verbosity=command.verbosity,
            simulate=command.options.simulate,
            interactive=command.options.interactive,
            overwrite=command.options.overwrite,
            indent=1,
            template_renderer=self.render_package,
            )

    def makedirs(self, dir): # pragma: no cover
        return os.makedirs(dir)

    def exists(self, path): # pragma: no cover
        return os.path.exists(path)

    def out(self, msg): # pragma: no cover
        print(msg)


class TypeMapper(dict):

    def __getitem__(self, item):
        options = item.split('|')
        for op in options[:-1]:
            try:
                value = eval_with_catch(op, dict(self.items()))
                break
            except (NameError, KeyError):
                pass
        else:
            value = eval(options[-1], dict(self.items()))
        if value is None:
            return ''
        else:
            return str(value)


def eval_with_catch(expr, vars):
    try:
        return eval(expr, vars)
    except Exception as e:
        _add_except(e, 'in expression %r' % expr)
        raise

double_brace_pattern = re.compile(r'{{(?P<braced>.*?)}}')


def substitute_double_braces(content, values):
    def double_bracerepl(match):
        value = match.group('braced').strip()
        return values[value]
    return double_brace_pattern.sub(double_bracerepl, content)

escaped_double_brace_pattern = re.compile(r'\\{\\{(?P<escape_braced>[^\\]*?)\\}\\}')


def substitute_escaped_double_braces(content):
    def escaped_double_bracerepl(match):
        value = match.group('escape_braced').strip()
        return "{{%(value)s}}" % locals()
    return escaped_double_brace_pattern.sub(escaped_double_bracerepl, content)


def _add_except(exc, info): # pragma: no cover
    if not hasattr(exc, 'args') or exc.args is None:
        return
    args = list(exc.args)
    if args:
        args[0] += ' ' + info
    else:
        args = [info]
    exc.args = tuple(args)
    return