# Assignment 10
**1.Use Faker library to get 10000 random profiles. Using namedtuple,
calculate the largest blood type, mean-current_location, oldest_person_age and average age 
(add proper doc-strings). - 250**

```python
get_age = lambda x: int((date.today() - x).days/365)
get_age.__doc__ = 'Return Age from Date'
get_age.__annotations__ = {1:1}
faker = Faker()
nt_keys_str = 'name blood_type age curr_loc'
profile = namedtuple('Profile', nt_keys_str)

def return_n_t_profile() -> namedtuple:
    """Returns a new fake profile from Faker lib every time 

    Returns:
        namedtuple: contanting name blood_type age curr_loc in order.
    """
    profile = namedtuple('Profile', nt_keys_str)
    p1 = faker.profile()
    nt_1 = profile(p1['name'], p1['blood_group'], get_age(p1['birthdate']), p1['current_location'])
    return nt_1

def return_profiles_n_t(num_profiles:int)->namedtuple:
    "Returns a namedtuple of nametuples of profiles"

    nt_parent_keys_str = ' '.join(f'p{i}' for i in range(num_profiles))
    nt_parent = namedtuple('Parent_Tuple', nt_parent_keys_str)
    n_profies = tuple(return_n_t_profile() for _ in range(num_profiles))
    return nt_parent(*n_profies)


def get_nt_mc_blood_type(nt_profiles:namedtuple)->str:
    """Returns most common blood type location for namedtuple of nametuples of profiles

    Args:
        nt_parofiles (namedtuple):namedtuple of nametuples of profiles

    Returns:
        str: blood type
    """

    counter = Counter()
    for p in nt_profiles:
        counter[p[1]] += 1
    return counter.most_common(1)[0][0]

def get_nt_mean_loc(nt_profiles:namedtuple)->tuple:
    """Returns mean location for namedtuple of nametuples of profiles

    Args:
        nt_parofiles (namedtuple):namedtuple of nametuples of profiles

    Returns:
        tuple: mean location (lat, long)
    """
    mean_loc = (0,0)
    num = len(nt_profiles._fields)
    for p in nt_profiles:
        mean_loc = mean_loc[0]+p[3][0],  mean_loc[1]+p[3][1]
    return mean_loc[0]/num, mean_loc[1]/num

def get_nt_oldest_age(nt_profiles:namedtuple)->int:
    """Returns oldest age in namedtuple of nametuples of profiles

    Args:
        nt_profiles (namedtuple): namedtuple of nametuples of profiles

    Returns:
        int: largest age
    """
    age = 0
    for p in nt_profiles:
        if p[-2]>age:
            age = p[-2]
    return age       

def get_nt_avg_age(nt_profiles:namedtuple) -> float:
    """Returns avg age in namedtuple of nametuples of profiles

    Args:
        nt_profiles (namedtuple): namedtuple of nametuples of profiles

    Returns:
        float: average age
    """ 
    age = sum(p[-2] for p in nt_profiles)
    return age/len(nt_profiles._fields)

```
**2. Do the same thing above using a dictionary. Prove that namedtuple is faster. - 250**
   
```python 
def return_dict_profile() -> dict:
    """Returns a new fake profile from Faker lib every time 

    Returns:
        dict: contanting keys name blood_type age curr_loc in order.
    """
    p = faker.profile()
    p = {
        'name':p['name'],
        'age':get_age(p['birthdate']),
        'blood_type':p['blood_group'],
        'cur_loc':p['current_location']
        }

    return p

def return_n_dict_profiles(num_profiles:int):
    "Calls return_dict_profile num_profiles times "
    profiles = {i:return_dict_profile() for i in range(num_profiles)}
    return profiles



def get_dict_mc_blood_type(dict_profiles:dict)->str:
    """Returns most common blood type location for dict of dict of profiles

    Args:
        dict_profiles (dict):dict of dict of profiles

    Returns:
        str: blood type
    """

    counter = Counter()
    for key, profile in dict_profiles.items():
        counter[profile.get('blood_type', '')] += 1
    return counter.most_common(1)[0][0]

def get_dict_mean_loc(dict_profiles:dict)->tuple:
    """Returns mean location for dict of dict of profiles

    Args:
        dict_profiles (dict):dict of dict of profiles

    Returns:
        tuple: mean location (lat, long)
    """
    mean_loc = (0,0)
    num = len(dict_profiles)
    for key, p in dict_profiles.items():
        cur_loc = p.get('cur_loc', (0, 0))
        mean_loc = mean_loc[0]+cur_loc[0],  mean_loc[1]+cur_loc[1]
    return mean_loc[0]/num, mean_loc[1]/num

def get_dict_oldest_age(dict_profiles:dict)->int:
    """Returns oldest age in dict of dict of profiles

    Args:
        dict_profiles (dict):dict of dict of profiles

    Returns:
        int: largest age
    """
    age = 0
    for key, p in dict_profiles.items():
        p_age = p.get('age', 0)
        if p_age >age:
            age = p_age
    return age     

def get_dict_avg_age(dict_profiles:dict) -> float:
    """Returns avg age in dict of dict of profiles

    Args:
        dict_profiles (dict):dict of dict of profiles

    Returns:
        float: average age
    """ 
    age = sum(p.get('age', 0) for key, p in dict_profiles.items())
    return age/len(dict_profiles)
```
**3. Create a fake data (you can use Faker for company names) for imaginary stock exchange for top 100 companies (name, symbol, open, high, close). Assign a random weight to all the companies. Calculate and show what value stock market started at, what was the highest value during the day and where did it end. Make sure your open, high, close are not totally random. You can only use namedtuple. - 500**

```python 
def return_n_companies(num_companies: int) -> list:
    """Returns list of namedtuples of n company profile

    Args:
        num_companies (int): number of profiles

    Raises:
        ValueError: number of profiles isn't an integer

    Returns:
        list: list of namedtuples
    """

    if not isinstance(num_companies, int):
        raise ValueError("Number of Company Profiles needs to be an integer")

    precision = 10
    weights_range = (.3, .9)
    stock_value_range = (1, 10000)
    max_high = round(random.uniform(1, 1.5), precision)
    min_low = round(random.uniform(.5, 1), precision)
    weights = [round(random.uniform(*weights_range), precision)
            for _ in range(num_companies)]
    norm_weights = [round(w / sum(weights), precision) for w in weights]

    profiles = []
    for i in range(num_companies):
        company_name = faker.company()
        company_sym = return_symbol(company_name)
        company_open = round(
            (random.randint(*stock_value_range) * norm_weights[i]), precision)
        company_high = round(random.uniform(
            company_open, company_open * max_high), precision)
        company_low = min(company_open, round(random.uniform(
            company_open * min_low, company_high), precision))
        company_close = round(random.uniform(
            company_low, company_high), precision)
        company = company_profile(
            company_name, company_sym, company_open, company_low, company_high, company_close)
        profiles.append(company)

    return profiles
```

## **Test Cases (Pytest)**
>The names of the tests are so that `'test_'` prefix is added to the function it tests, suffied by the what the test does.

### `test_readme_exists`
   Checks if there is a README.md file in the same folder.

### `test_readme_contents`
   Checks if the README.md file has alteast 500 words.

### `test_readme_proper_description`
   Checks if the required functions are present in the README.md file.

### `test_readme_file_for_formatting`
   Checks if there are adequete headings present in the README.md file.

### `test_indentations`
   Checks if proper indentations are present throughout the python file.
   using the rule of 4 spaces equals 1 Tab.

### `test_function_name_had_cap_letter`
   Checks if any one the functions have capital letters used in their names, which breaks the PEP8 conventions.
   
### ***Annotation and Docstring tests***
tests if any of the functions in function list don't have annotations or docstrings
1. `get_age`
2. `return_n_t_profile`
3. `return_profiles_n_t`
4. `get_nt_mc_blood_type`
5. `get_nt_mean_loc`
6. `get_nt_oldest_age`
7. `get_nt_avg_age`
8. `return_dict_profile`
9. `return_n_dict_profiles`
10. `get_dict_mc_blood_type`
11. `get_dict_mean_loc`
12. `get_dict_oldest_age`
13. `get_dict_avg_age`



### `test_get_nt_mc_blood_type`
   Check named tuple implementation of most common blood type

### `test_get_dict_mc_blood_type`
   Check named tuple implementation of most common blood type

### `test_get_nt_mean_loc`
   Check namedtuple implementation of mean location

### `test_get_dict_mean_loc`
   Check dict implementation of mean location

### `test_get_dict_oldest_age`
   Check dict implementation of max age

### `test_get_nt_oldest_age`
   Check namedtuple implementation of max age

### `test_get_nt_avg_age`
   Check namedtuple implementation of avg. age

### `test_get_dict_avg_age`
   Check dict implementation of avg. age

### `test_company_profile`
   Check Basic things like low <= open <= close <= high

### `test_return_0_company_profile`
   Checks if 0 input returns an empty list

### `test_return_0_nt_profile`
   Checks if zero input zero output namedtuple profiles

### `test_return_0_dict_profile`
   Checks if zero input zero output dict profiles