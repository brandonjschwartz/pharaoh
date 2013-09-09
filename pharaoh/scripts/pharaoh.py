import optparse
import os
import pkg_resources
import re
import sys

_bad_chars_re = re.compile('[^a-zA-Z0-9_]')


def main(argv=sys.argv, quiet=False):
    command = PkgCreateCommand(argv, quiet)
    return command.run()


class PkgCreateCommand(object):
    verbosity = 1 # required
    description = "Render a new starter package"
    usage = "usage: %prog [options] output_directory"
    parser = optparse.OptionParser(usage, description=description)
    parser.add_option('-s', '--starter_package',
                      dest='package_name',
                      action='append',
                      help=("Add a package to the create process "
                            "(multiple -s args accepted)"))
    parser.add_option('-l', '--list',
                      dest='list',
                      action='store_true',
                      help="List all available starter packages")
    parser.add_option('--simulate',
                      dest='simulate',
                      action='store_true',
                      help='Simulate but do no work')

    def __init__(self, argv, quiet=False):
        self.quiet = quiet
        self.options, self.args = self.parser.parse_args(argv[1:])
        self.packages = self.all_packages()

    def run(self):
        if self.options.list:
            return self.show_packages()
        if not self.options.package_name:
            self.out('You must provide at least one scaffold name')
            return 2
        if not self.args:
            self.out('You must provide a project name')
            return 2
        available = [x.name for x in self.packages]
        diff = set(self.options.package_name).difference(available)
        if diff:
            self.out('Unavailable scaffolds: %s' % list(diff))
            return 2
        return self.render_packages()

    def render_packages(self):
        options = self.options
        args = self.args
        project_name = os.path.basename(args[0])
        output_dir = os.path.abspath(os.path.normpath(args[0]))
        pkg_name = _bad_chars_re.sub('', project_name.lower())
        safe_name = pkg_resources.safe_name(project_name)
        egg_name = pkg_resources.to_filename(safe_name)
        vars = {
            'project': project_name,
            'package': pkg_name,
            'egg': egg_name,
            }
        for package_name in options.package_name:
            for package in self.packages:
                if package.name == package_name:
                    package.run(self, output_dir, vars)
        return 0

    def show_packages(self):
        packages = sorted(self.packages, key=lambda x: x.name)
        if packages:
            max_name = max([len(t.name) for t in packages])
            self.out('Available scaffolds:')
            for package in packages:
                self.out('  %s:%s  %s' % (
                    package.name,
                    ' '*(max_name-len(package.name)), package.summary))
        else:
            self.out('No scaffolds available')
        return 0

    def all_packages(self):
        packages = []
        eps = list(pkg_resources.iter_entry_points('pyramid.scaffold'))
        for entry in eps:
            try:
                package_class = entry.load()
                package = package_class(entry.name)
                packages.append(package)
            except Exception as e: # pragma: no cover
                self.out('Warning: could not load entry point %s (%s: %s)' % (
                    entry.name, e.__class__.__name__, e))
        return packages

    def out(self, msg):  # pragma: no cover
        if not self.quiet:
            print(msg)