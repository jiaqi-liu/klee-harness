from ktest import KTest
from string import Template
import sys

f = open("klee_harness.c.tmpl")
template = Template(f.read())
f.close()

b = KTest.fromfile(sys.argv[1])
numObjects = len(b.objects)

def print_obj_def(object):
    name = object[0].decode('ascii')
    data = map(ord, object[1])
    obj_def = '{ (char*)"%s", %d, {%s} }' % (
        name,
        len(data),
        ", ".join(map(str, data))
    )
    return obj_def

objects_def = map(print_obj_def, b.objects)

src = template.substitute(objects=",\n\t".join(
    objects_def), numObjects=numObjects)

with open("klee_harness.c", "w+") as f:
    print>>f, src
