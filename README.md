# pydocparser
A library for parsing pydoc blocks

## API
### Classes

#### pydocparser.ClassParser([pydocparser.Parser](#pydocparserparser))
Creates a structure representing class object


#### pydocparser.FunctionParser([pydocparser.Parser](#pydocparserparser))
Creates a structure representing a function


#### pydocparser.ModuleParser([pydocparser.Parser](#pydocparserparser))
Handle the parsing of Modules


#### pydocparser.Parser()
Base parser class to handle self metadata and removing empty key values

##### \_\_init\_\_(self, obj, parent=None)

| Name | Type | Description | Default |
|------|------|-------------|---------|
| obj | | A
n
 
o
b
j
e
c
t
 
l
i
k
e
 
m
o
d
u
l
e
,
 
c
l
a
s
s
,
 
f
u
n
c
t
i
o
n
,
 
m
e
t
h
o
d
,
 
w
h
i
c
h
 
c
a
n
 
h
a
v
e
 
a
 
d
o
c
 
b
l
o
c
k
 
e
x
t
r
a
c
t
e
d
 
f
r
o
m
 
i
t | |
| parent | | A
 
s
t
r
i
n
g
 
r
e
p
r
e
s
e
n
t
i
n
g
 
t
h
e
 
p
a
r
e
n
t
 
m
o
d
u
l
e
 
p
a
t
h | |


##### get(self, key)


##### self\_member(self)


##### set(self, key, value)

| Name | Type | Description | Default |
|------|------|-------------|---------|
| key | |  | |
| value | |  | |


##### start(self)





#### pydocparser.docblock.DocParser






### Functions

#### pydocparser.get(key)
Get Configuration option

| Name | Type | Description | Default |
|------|------|-------------|---------|

#### pydocparser.set(key, value)
Set configuration options for the parsing actions

| Name | Type | Description | Default |
|------|------|-------------|---------|


