from datetime import datetime, date
import typing
import random
from decimal import Decimal
from faker import Faker
from collections import namedtuple, Counter
namedtuple.__doc__ = "Doc"
namedtuple.__annotations__ = {1: 1}
'''
1.Use Faker library to get 10000 random profiles. Using namedtuple,
calculate the largest blood type, mean-current_location, oldest_person_age and average age 
(add proper doc-strings). - 250
2.Do the same thing above using a dictionary. Prove that namedtuple is faster. - 250
3.Create a fake data (you can use Faker for company names) for imaginary stock exchange for top 100 companies (name, symbol, open, high, close). Assign a random weight to all the companies. Calculate and show what value stock market started at, what was the highest value during the day and where did it end. Make sure your open, high, close are not totally random. You can only use namedtuple. - 500
Add the notebook as well to your github where logs can be visible. 
'''


def get_age(x: date) -> int:
    """Get current age from date

    Args:
        x (date): datetime.date object

    Returns:
        int: current age
    """
    return int((date.today() - x).days/365)


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
    nt_1 = profile(p1['name'], p1['blood_group'], get_age(
        p1['birthdate']), p1['current_location'])
    return nt_1


def return_profiles_n_t(num_profiles: int) -> namedtuple:
    "Returns a namedtuple of nametuples of profiles"
    if not isinstance(num_profiles, int):
        raise ValueError("Number of Profiles needs to be an integer")

    nt_parent_keys_str = ' '.join(f'p{i}' for i in range(num_profiles))
    nt_parent = namedtuple('Parent_Tuple', nt_parent_keys_str)
    n_profies = tuple(return_n_t_profile() for _ in range(num_profiles))
    return nt_parent(*n_profies)


def get_nt_mc_blood_type(nt_profiles: namedtuple) -> str:
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


def get_nt_mean_loc(nt_profiles: namedtuple) -> tuple:
    """Returns mean location for namedtuple of nametuples of profiles

    Args:
        nt_parofiles (namedtuple):namedtuple of nametuples of profiles

    Returns:
        tuple: mean location (lat, long)
    """
    mean_loc = (0, 0)
    num = len(nt_profiles._fields)
    for p in nt_profiles:
        mean_loc = mean_loc[0]+p[3][0],  mean_loc[1]+p[3][1]
    return mean_loc[0]/num, mean_loc[1]/num


def get_nt_oldest_age(nt_profiles: namedtuple) -> int:
    """Returns oldest age in namedtuple of nametuples of profiles

    Args:
        nt_profiles (namedtuple): namedtuple of nametuples of profiles

    Returns:
        int: largest age
    """
    age = 0
    for p in nt_profiles:
        if p[-2] > age:
            age = p[-2]
    return age


def get_nt_avg_age(nt_profiles: namedtuple) -> float:
    """Returns avg age in namedtuple of nametuples of profiles

    Args:
        nt_profiles (namedtuple): namedtuple of nametuples of profiles

    Returns:
        float: average age
    """
    age = sum(p[-2] for p in nt_profiles)
    return age/len(nt_profiles._fields)


def return_dict_profile() -> dict:
    """Returns a new fake profile from Faker lib every time 

    Returns:
        dict: contanting keys name blood_type age curr_loc in order.
    """
    p = faker.profile()
    p = {
        'name': p['name'],
        'age': get_age(p['birthdate']),
        'blood_type': p['blood_group'],
        'cur_loc': p['current_location']
    }

    return p


def return_n_dict_profiles(num_profiles: int):
    "Calls return_dict_profile num_profiles times "
    if not isinstance(num_profiles, int):
        raise ValueError("Number of Profiles needs to be an integer")
    profiles = {i: return_dict_profile() for i in range(num_profiles)}
    return profiles


def get_dict_mc_blood_type(dict_profiles: dict) -> str:
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


def get_dict_mean_loc(dict_profiles: dict) -> tuple:
    """Returns mean location for dict of dict of profiles

    Args:
        dict_profiles (dict):dict of dict of profiles

    Returns:
        tuple: mean location (lat, long)
    """
    mean_loc = (0, 0)
    num = len(dict_profiles)
    for key, p in dict_profiles.items():
        cur_loc = p.get('cur_loc', (0, 0))
        mean_loc = mean_loc[0]+cur_loc[0],  mean_loc[1]+cur_loc[1]
    return mean_loc[0]/num, mean_loc[1]/num


def get_dict_oldest_age(dict_profiles: dict) -> int:
    """Returns oldest age in dict of dict of profiles

    Args:
        dict_profiles (dict):dict of dict of profiles

    Returns:
        int: largest age
    """
    age = 0
    for key, p in dict_profiles.items():
        p_age = p.get('age', 0)
        if p_age > age:
            age = p_age
    return age


def get_dict_avg_age(dict_profiles: dict) -> float:
    """Returns avg age in dict of dict of profiles

    Args:
        dict_profiles (dict):dict of dict of profiles

    Returns:
        float: average age
    """
    age = sum(p.get('age', 0) for key, p in dict_profiles.items())
    return age/len(dict_profiles)


company_profile = namedtuple('Company', ['name', 'symbol', 'open', 'low', 'high', 'close'])


def return_symbol(x: str) -> str:
    "Returns A symbol from a name of a company"
    return x[:3].upper() if len(
        x.split()) < 2 else ''.join(a[0].upper() for a in x.split())


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
