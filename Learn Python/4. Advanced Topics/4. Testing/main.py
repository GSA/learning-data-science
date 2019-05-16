from divide import divide
from get_resource import get_resource_by_date

def get_ints_from_resource(uri, date = None):
    response_text = get_resource_by_date(uri, date)
    x, y = (response_text[-2:])

    return x, y

def main(uri, date = None):
    x, y = get_ints_from_resource(uri, date = None)
    z = divide(x, y)

    return z

if __name__ == '__main__':
    #this won't actually work! Just for demo purposes
    z = main('http://test.com')