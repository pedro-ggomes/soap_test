from spyne import Application, rpc, ServiceBase, Integer, Unicode, ComplexModel, Iterable
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from faker import Faker
from random import randint
import json

def generate_data():
    persons = []
    for i in range(1,101,1):
        person = {
                  "id":i,
                  "name": Faker().name(),
                  "age": randint(10,99)
                 }
        persons.append(person)
    with open("data.json","w") as fp:
        json.dump(persons,fp)

def get_data():
    with open("data.json","r") as fp:
        persons = json.load(fp,object_hook=lambda d: Person(**d))
    return persons

# Define the complex type for persons
class Person(ComplexModel):
    id = Integer
    name = Unicode
    age = Integer

class PersonService(ServiceBase):
    @rpc(Integer, Integer, _returns=Iterable(Person))
    def get_items(ctx, page, page_size):
        """Returns a paginated list of items."""
        persons = get_data()
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        paginated_items = persons[start_index:end_index]
        
        return paginated_items

app = Application(
    [PersonService],
    tns='persons.soap.example',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

wsgi_app = WsgiApplication(app)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    
    # generate_data()
    # print(get_data())
    
    server = make_server('0.0.0.0', 8000, wsgi_app)
    print("SOAP server running on http://0.0.0.0:8000")
    server.serve_forever()
