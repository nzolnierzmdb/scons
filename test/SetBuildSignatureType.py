#!/usr/bin/env python
#
# __COPYRIGHT__
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

__revision__ = "__FILE__ __REVISION__ __DATE__ __DEVELOPER__"

import TestSCons

test = TestSCons.TestSCons()

test.write('SConstruct', """
env = Environment()

def copy1(env, source, target):
    open(str(target[0]), 'wb').write(open(str(source[0]), 'rb').read())

def copy2(env, source, target):
    return copy1(env, source, target)

env['BUILDERS']['Copy1'] = Builder(action=copy1)
env['BUILDERS']['Copy2'] = Builder(action=copy2)

env.Copy2('foo.out', 'foo.in')
env.Copy1('foo.out.out', 'foo.out')

SetBuildSignatureType('content')
""")

test.write('foo.in', 'foo.in')

test.run(arguments='foo.out.out',
         stdout=test.wrap_stdout("""\
copy2("foo.out", "foo.in")
copy1("foo.out.out", "foo.out")
"""))

test.run(arguments='foo.out.out',
         stdout=test.wrap_stdout('scons: "foo.out.out" is up to date.\n'))

test.write('SConstruct', """
env = Environment()

def copy1(env, source, target):
    open(str(target[0]), 'wb').write(open(str(source[0]), 'rb').read())

def copy2(env, source, target):
    # added this line
    return copy1(env, source, target)

env['BUILDERS']['Copy1'] = Builder(action=copy1)
env['BUILDERS']['Copy2'] = Builder(action=copy2)

env.Copy2('foo.out', 'foo.in')
env.Copy1('foo.out.out', 'foo.out')

SetBuildSignatureType('content')
""")

test.run(arguments='foo.out.out',
         stdout=test.wrap_stdout("""\
copy2("foo.out", "foo.in")
scons: "foo.out.out" is up to date.
"""))

test.write('SConstruct', """
env = Environment()

def copy1(env, source, target):
    open(str(target[0]), 'wb').write(open(str(source[0]), 'rb').read())

def copy2(env, source, target):
    # added this line
    return copy1(env, source, target)

env['BUILDERS']['Copy1'] = Builder(action=copy1)
env['BUILDERS']['Copy2'] = Builder(action=copy2)

env.Copy2('foo.out', 'foo.in')
env.Copy1('foo.out.out', 'foo.out')

SetBuildSignatureType('build')
""")

test.run(arguments='foo.out.out',
         stdout=test.wrap_stdout("""\
copy1("foo.out.out", "foo.out")
"""))

test.write('SConstruct', """
env = Environment()

def copy1(env, source, target):
    open(str(target[0]), 'wb').write(open(str(source[0]), 'rb').read())

def copy2(env, source, target):
    return copy1(env, source, target)

env['BUILDERS']['Copy1'] = Builder(action=copy1)
env['BUILDERS']['Copy2'] = Builder(action=copy2)

env.Copy2('foo.out', 'foo.in')
env.Copy1('foo.out.out', 'foo.out')

SetBuildSignatureType('build')
""")

test.run(arguments='foo.out.out',
         stdout=test.wrap_stdout("""\
copy2("foo.out", "foo.in")
copy1("foo.out.out", "foo.out")
"""))


test.pass_test()
