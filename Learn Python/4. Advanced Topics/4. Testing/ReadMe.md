# Introduction to Testing in Python
This lesson introduces **testing** in Python using the built-in `unittest` library as well as the third-party `requests-mock` library, which helps you write tests for code that makes requests. 

We'll attempt to answer these questions:

1. What is testing and test-driven development?
2. How do I write tests in Python?
3. How can I run/automate a suite of tests?

# 1. What is testing and test-driven development?

## Testing your code
Testing is using code to prove to yourself that code you're writing does what you've intended. There are three main types of tests: unit, integration, and end-to-end.

### Unit Tests
Unit tests focus on testing small units (typically a function). As the name "unit" implies, they should execute in isolation and independent of other units (i.e. functions) in your codebase. This is typically achieved by "mocking" the dependencies (we'll see this later). Because of this, unit tests are lightweight and should execute quickly.

### Integration Tests
Integration tests ensure that code which works well in isolation (as proven by a unit test), also plays well with the rest of your code and/or third-party services (e.g. an API or other external service). Integration tests typically focus on a small number of modules and test their interactions.

### End-to-End Tests
End-to-end testing tests whether the flow of an entire application works as intended from start to finish. A drawback of end-to-end testing is that it typically takes longer and, when things go wrong, it can be difficult to introspect the source of the error(s).

## Finding the Right Balance
According to [Google's testing blog](https://testing.googleblog.com/2015/04/just-say-no-to-more-end-to-end-tests.html), you can strike the right balance between all three test types by thinking of your tests in terms of this pyramid:

![testing pyramind](https://2.bp.blogspot.com/-YTzv_O4TnkA/VTgexlumP1I/AAAAAAAAAJ8/57-rnwyvP6g/s1600/image02.png)

The bulk of your tests are unit tests at the bottom of the pyramid. As you move up the pyramid, your tests gets larger, but at the same time the number of tests (the width of your pyramid) gets smaller.

## Test-Driven Development
Test-driven development (TDD) is a software development practice where requirements are turned into very specific test cases that fail until the developer writes code to make them pass. This is opposed to software development that allows software to be added that is not proven to meet requirements. **Sometimes TDD isn't feasible, but it's a good goal to strive for as it encourages simple designs and inspires confidence.**

# 2. How do I write tests in Python?

## Organizing your tests
Now we'll get to code. Our directory tree should look like this:

├── ReadMe.md<br>
├── divide.py<br>
├── get_resource.py<br>
├── main.py<br>
├── requirements.txt<br>
├── tests<br>
│   ├── test_divide.py<br>
│   ├── test_get_resource.py<br>
│   └── test_main.py<br>

We've got some top-level python modules (`divide.py` and `get_resource.py`) that are utilized by `main.py` to do something trivial. Then, in a `tests/` directory, we have test files for each of those .py files. This is a common way to organize your tests as it makes it easy to see the relationship between tests and what's being tested. It'll also come in handy when we want to automate the test running later.

To get a feel for the program, let's open `divide.py` and see what it does:

```python
def divide(x, y):
    z = x / y

    return z
```

There's only one function. It takes two parameters, `x` and `y`. Since this function is called divide, we should presumably pass numeric arguments. Other types should raise exceptions. Finally, `y` should never be equal to zero. When exceptions are raised, let's assume that we just want this function to return `0`.

## Writing Tests
Let's open `tests/test_divide.py` to see how we can write some **unit** tests using the [unittest](https://docs.python.org/3.6/library/unittest.html) library. We'll use `unittest` since it has been built into the Python standard library since version 2.1. It's likely the most common testing framework in use.

Here are the important object-oriented concepts that unittest supports:

#### test fixture
>A test fixture represents the preparation needed to perform one or more tests, and any associate cleanup actions. This may involve, for example, creating temporary or proxy databases, directories, or starting a server process.

#### test case
>A test case is the individual unit of testing. It checks for a specific response to a particular set of inputs. unittest provides a base class, `TestCase`, which may be used to create new test cases.

#### test suite
>A test suite is a collection of test cases, test suites, or both. It is used to aggregate tests that should be executed together.

#### test runner
>A test runner is a component which orchestrates the execution of tests and provides the outcome to the user. The runner may use a graphical interface, a textual interface, or return a special value to indicate the results of executing the tests.

### Test Fixtures
In `test_divide.py`, you'll see two methods in the `DivideCase` class: `setUp` and `tearDown`. We'll use these methods to create **test fixtures**. 

Test fixtures are the resources and initial conditions that a unit test needs to operate correctly and independently from other tests. These methods will run before and after a test. The intent is to provide developers hooks to set up preconditions needed for the test, and cleanup after the test. The main benefit of these fixtures is that they set up structures or variables the same way for all tests. This is to make sure that tests can run individually as well as a set and in any order.

>There's an additional helper method called `log_point` that'll help show how the `setUp` occurs before every test and that the `tearDown` occurs after each test.

### Test Case
In `test_divide.py`, we import `unittest` and then subclass `unittest.TestCase` as `DivideCase`:

```python
import unittest
...

class DivideCase(unittest.TestCase):
    ...
```

This is our **test case** and we do this because `unittest` has some important requirements for writing and executing tests. `unittest` requires that:

1. You put your tests into classes as methods
2. You use a series of special assertion methods in the unittest.TestCase class instead of the built-in assert statement. These special assertion methods are inherited from `unittest.TestCase`.

### Running a Test Case
To run a test, `cd` into the tests directory and then run the following:

```
python3 -m unittest test_divide.DivideCase.test_divide_int_args
```

This will run just one of the tests within the test case. Your output should look something like this:
```
(env) MCOH2J-X08CJHD3:tests charlessmcallister$ python3 -m unittest test_divide.DivideCase.test_divide_int_args
in test_divide_int_args - setUp()
in test_divide_int_args - test_divide_int_args()
in test_divide_int_args - tearDown()
.
----------------------------------------------------------------------
Ran 1 test in 0.014s

OK
```

As you can see, the `setUp` and `tearDown` methods were called before and after the test, respectively. You can also see that the test passed (`OK`) and how long the test took.

Now, looking at the rest of the test cases, we should see that `test_divide_by_zero` and `test_divide_str_args` will fail. Let's see that by running all of the tests together with:

```
python3 -m unittest test_divide.py
```

Sure enough, those two tests failed. Let's go re-write the `divide` function until it passes. This is TDD in action.

## Mocking in your Tests
Writing the unit tests for `divide.py` was easy because the divide function didn't integrate with any other functions or external resources like an API. In `get_resource.py`, there's a couple of functions that *do* integrate with externalites. In order to write proper unit tests, we'll need to isolate these and control for them. This process is often referred to as `mocking`. 

Fortunately, the `unittest` library has a `mock` library that does just this. And for `requests`, there's the `requests-mock` library.

Open `get_resource.py`. You'll see these three functions:

```python
def get_resource(uri):
    r = requests.get(uri)
    response_text = r.text

    return response_text

def get_now():
    now = datetime.now().strftime("%Y-%d-%m")
    return now

def get_resource_by_date(uri, date = None):
    if not date:
        date = get_now()
    uri += f"?date={date}"
    r = requests.get(uri)
    response_text = r.text

    return response_text
```
The first, `get_resource()`, uses `requests` to make a GET request to a uri and then return the text of the response.

The second, `get_now()`, is a wrapper for `datetime.now()` that returns an abbreviated date string instead of a datetime object.

The third, `get_resource_by_date()`, combines the two previous functions by tacking a date query string onto our request uri.

In `tests/test_get_resource.py` we'll only test the last two functions, but we'll do so by creating our fixtures somewhat differently. Instead of using `setUp` and `tearDown`, we'll use `tearDownClass` and `setUpClass` to create fixtures just once before all of the tests are run and then to destroy them just once after all of the tests are done. 

### Mocking Requests with a Third-Party Library
Let's look at the first test case, `test_get_resource`:

```python
@requests_mock.Mocker()
def test_get_resource(self, mock_request):
    mock_request.register_uri('GET', 
                                GetResourceCase.uri, 
                                text = GetResourceCase.response_text)
    result = get_resource(GetResourceCase.uri)
    expected = GetResourceCase.response_text
    self.assertEqual(result, expected)
```
Here we're using the `requests_mock` library to mock a GET request to http://test.com. We're doing this because we don't actually want to make a request across the internet to this website whose response we cannot control. Without controlling for this dependency, we'd be unable to write a unit test for this function. **If, however, we didn't mock this request, then we'd have an integration test.**

>The `requests_mock` documentation fully walks though what's going on above, but in essence we're just tricking the requests library by defining ourselves what the response of a GET request to http://test.com will be. 

We can run this test with:

```
python3 -m unittest test_get_resource.GetResourceCase.test_get_resource
```

We'll see that the test passed and can rest assured that this function, which might be more complicated in real life, returns the text of an expected response properly.

The next test (`test_get_resource_exc`) is a mix of an integration and unit test since it tests what our function returns in the case that the GET request fails. Let's run that test to see what happens:

```
python3 -m unittest test_get_resource.GetResourceCase.test_get_resource_exc
```

You should have seen an exception's traceback followed by `FAILED (errors=1)`. That means our test failed. Let's rewrite `get_resource.get_resource()` to make this test pass.

### Mocking with Unittest's `patch`
Above, we mocked a GET request. We can also mock python code. This is achieved with the `patch` functionality of `unittest`. The `test_get_resource_by_date_complete_qs()` test case shows us how we can do this:

```python
@patch('get_resource.get_now')
@requests_mock.Mocker()
def test_get_resource_by_date_complete_qs(self, mocked_now, mock_request):
    '''
    Test response with complete query param by patching a func that calls datetime.now()
    '''
    now = '2019-05-16'
    mocked_now.return_value = now
    uri = f'{GetResourceCase.uri}?date={now}'
    mock_request.register_uri('GET', 
                                uri, 
                                text = GetResourceCase.response_text,
                                complete_qs = True) #match only the complete query string; no partial/wildcard matches
    result = get_resource_by_date(GetResourceCase.uri)
    expected = GetResourceCase.response_text
    self.assertTrue(result, expected)
```

Here, we're writing a unittest for `get_resource_by_date()`. Since this functionn calls `get_now()`, which in turns calls `datetime.now()`, we need to control for these return values in order to be sure that `get_resource_by_date()` does just what we'd expect. To do so, we patch `get_resource.get_now` and specify its return value ourself in `mocked_now.return_value = now`.

>We've passed `get_resource.get_now` into the patch decorator because you're supposed to **mock an item where it is used, not where it came from**. That's because each module keeps its own imports in Python.

Once we've patched that dependency, we've guaranteed the behavior of `get_now()` and can write a test very similar to `test_get_resource`.

Let's run the test to see that it passes:
```
python -m unittest test_get_resource.GetResourceCase.test_get_resource_by_date_complete_qs
```

Sure enough it passes.

# 3. How can I run/automate a suite of tests?

## Test Discovery
Unittest provides you with a **test runner**, which is what ocherstates all of your test cases into a **test suite** that can be run at once. There's a variety of ways to run your tests, but **test discovery** is one of the easiest and most flexible. Test discovery will let you specify where your tests are located and then run them. To test discover our tests, make sure you're in `/learning-data-science/Learn Python/4. Advanced Topics/4. Testing` and then run the following:

```bash
python -m unittest discover tests -p 'test*.py'
```

Above, we're invoking unittest's test discovery with `discover` and then passing in `tests` as an argument that specifies where, relative to the current working directory, our tests are located. The `-p` flag lets us specify a filename pattern for our tests files. The pattern is `test*.py` by default, but we're including it here anyway.

## Continuous Integration
Continuous Integration (CI) is a practice that encourages developers to integrate their code into a master branch of a shared repository early and often. Instead of building out features in isolation and integrating them at the end of a development cycle, code is integrated with the shared repository by each developer multiple times throughout the day.

There are a lot of CI services, and most provide free services for open source projects.

# Postscript
If you'd like, open `tests/test_main.py` and write out the two unit tests.