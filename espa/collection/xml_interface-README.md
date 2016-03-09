## XMLInterface
Implements an interface for parcing, writing, and validating XML files utilizing the lxml python module.

### Usage

```
>>> from lxml import objectify as objectify
>>> from espa import XMLInterface
>>> xml_xsd = str(<THE XSD AS A STRING>)
>>> xml_filename = 'animals.xml'
>>> xml = XMLInterface(xml_xsd=xml_xsd, xml_filename=xml_filename)
>>> xml.parse()
>>> e_maker = objectify.ElementMaker(annotate=False, namespace=None, nsmap=None)
>>> animal = e_maker.animal()
>>> animal.set('name', 'Hyla cinerea')
>>> animal.description = e_maker.element('American tree frog')
>>> animal.color = e_maker.element('green')
>>> xml.append(animal)
>>> xml.validate()
>>> xml.write(xml_filename='animals.xml')
```
