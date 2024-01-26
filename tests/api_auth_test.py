# TODO: NEED HUGE REFACTORING!!! THIS TESTS ARE BAD!!!
import asyncio
import re
from secrets import token_urlsafe
from random import choices
from string import (
    ascii_letters,
    ascii_lowercase,
    ascii_uppercase,
    digits,
)
from datetime import (
    datetime as dt,
    UTC,
)

import jwt
import pytest
import pytest_asyncio

from virtual_school_backend.config import Config


class TestAuthEndpoints:
    LOGIN_URL = ''
    LOGOUT_URL = ''
    REGISTRATION_URL = ''
    REFRESH_URL = ''

    @pytest.fixture
    def valid_reg_data(self):
        data = {
           'email': 'andrey@yandex.ru',
           'password': '1234qwertyQW',
           'name': 'Андрей',
           'secondname': 'Шахов',
           'patronymic': 'Владимирович',
           'birthdate': '2000-11-22',
           'phone': '8999992233',
           'class': 1,
        }
        return data

    @pytest.fixture
    def valid_login_data(self, valid_reg_data):
        return {'email': valid_reg_data['email'], 'password': valid_reg_data['password']}
    
    @pytest.fixture
    def fake_refresh_payload(self):
        payload = {
            'iss': Config.BACKEND_NAME,
            'sub': 'user',
            'jti': 'qwerty',
            'iat': (timestamp := dt.now(tz=UTC).timestamp()),
            'exp': timestamp + 60,
        }
        return payload


class TestLogoutEndpoint(TestAuthEndpoints):
    URL = '/auth/logout'

    @pytest.fixture
    def valid_reg_data(self):
        data = {
           'email': 'andrey5@yandex.ru',
           'password': '1234qwertyQW',
           'name': 'ААААдрей',
           'secondname': 'Шахов',
           'patronymic': 'Владимирович',
           'birthdate': '2000-11-22',
           'phone': '6739992233',
           'class': 1,
        }
        return data

    @pytest.mark.asyncio
    async def registration_for_logout_endpoint_test(self, backend_client, valid_reg_data):
        cli = await backend_client
        resp = await cli.post('/auth/registration', json=valid_reg_data)
        assert (resp.status, await resp.text()) == (200, '')
    
    @pytest.mark.asyncio
    async def logout_test(self, backend_client, valid_login_data):
        cli = await backend_client
        resp = await cli.post('/auth/login', json=valid_login_data)
        cookies = {
            '__Secure-refresh-token':  resp.cookies['__Secure-refresh-token'].value
        }
        resp = await cli.get(self.URL, cookies=cookies)

        assert resp.status == 200

        refresh_cookie = resp.cookies['__Secure-refresh-token']

        assert refresh_cookie.value == ''
        assert refresh_cookie['max-age'] == '0'
        assert refresh_cookie['path'] == '/auth/'
        assert refresh_cookie['httponly'] == True
        assert refresh_cookie['samesite'] == 'None'
        assert refresh_cookie['secure'] == True

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'payload, expectation',
        [
            ({}, (401, '{"errors": ["token not in database"]}')),
            ({'exp': dt.now(tz=UTC).timestamp()}, (403, '{"errors": ["the refresh token has expired"]}')),
            ({'exp': 'invalid'}, (401, '{"errors": ["invalid refresh token"]}')),
            ({'iss': 'bad issuer'}, (401, '{"errors": ["invalid iss claim in refresh token"]}')),
            ({'iat': dt.now(tz=UTC).timestamp() + 600}, (403, '{"errors": ["iat claim in the future in refresh token"]}')),
            ({'iat': 'invalid'}, (401, '{"errors": ["invalid iat claim in refresh token"]}')),
        ],
        ids=('token not in db', 'expired', 'bad exp', 'bad issuer', 'future iat', 'invalid iat'),
    )
    async def bad_refresh_payload_logout_test(self, backend_client, fake_refresh_payload,
                                              payload, expectation):
        fake_refresh_payload.update(payload)
        cookies = {
            '__Secure-refresh-token': jwt.encode(
                fake_refresh_payload, Config.TOKEN_KEY,
                algorithm=Config.TOKEN_ALG,
            ),
        }
        cli = await backend_client
        resp = await cli.get(self.URL, cookies=cookies)
        assert (resp.status, await resp.text()) == expectation
    
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'part_num, expectation',
        [
            (0, (401, '{"errors": ["invalid refresh token"]}')),
            (1, (401, '{"errors": ["invalid refresh token signature"]}')),
            (2, (401, '{"errors": ["invalid refresh token signature"]}')),
        ],
        ids=('bad first part', 'bad second part', 'bad third part'),
    )
    async def invalid_sign_refresh_logout_test(self, backend_client, fake_refresh_payload,
                                               part_num, expectation):
        token = jwt.encode(
            fake_refresh_payload, Config.TOKEN_KEY,
            algorithm=Config.TOKEN_ALG,
        )
        cookies = {
            '__Secure-refresh-token': '.'.join(
                (part if num != part_num else 'invalid') for num, part in enumerate(token.split('.')))
        }
        cli = await backend_client
        resp = await cli.get(self.URL, cookies=cookies)
        assert (resp.status, await resp.text()) == expectation
    
    @pytest.mark.asyncio
    @pytest.mark.repeat(20)
    async def random_refresh_data_logout_test(self, backend_client):
        expectation = (401, '{"errors": ["invalid refresh token"]}')
        cli = await backend_client
        cookies = {'__Secure-refresh-token': token_urlsafe(32)}
        resp = await cli.get(self.URL, cookies=cookies)
        assert (resp.status, await resp.text()) == expectation
    
    @pytest.mark.asyncio
    async def without_token_logout_test(self, backend_client):
        cli = await backend_client
        resp = await cli.get(self.URL)
        assert (resp.status, await resp.text()) == (401, '{"errors": ["the refresh token is missing in request"]}')


@pytest.mark.asyncio(scope="class")
class TestRefreshEndpoint(TestAuthEndpoints):
    """
    Copy past from TestLogoutEndpoint, but for future it can be ok.
    You can use double parameterization for some tests from TestLogoutEndpoint to avoid this.
    """
    URL = '/auth/refresh'

    @pytest.fixture
    def valid_reg_data(self):
        data = {
           'email': 'andrey6@yandex.ru',
           'password': '1234qwertyQW',
           'name': 'АААААдрей',
           'secondname': 'Шахов',
           'patronymic': 'Владимирович',
           'birthdate': '2000-11-22',
           'phone': '6739982233',
           'class': 1,
        }
        return data

    @pytest.mark.asyncio
    async def registration_for_refresh_endpoint_test(self, backend_client, valid_reg_data):
        cli = await backend_client
        resp = await cli.post('/auth/registration', json=valid_reg_data)
        assert (resp.status, await resp.text()) == (200, '')
    
    @pytest.mark.asyncio
    async def refresh_test(self, backend_client, valid_login_data):
        cli = await backend_client
        resp = await cli.post('/auth/login', json=valid_login_data)
        cookies = {
            '__Secure-refresh-token':  resp.cookies['__Secure-refresh-token'].value
        }
        time_delta = 1
        await asyncio.sleep(time_delta)  # need for changing max-age in new refresh token
        resp = await cli.get(self.URL, cookies=cookies)

        assert resp.status == 200

        refresh_cookie = resp.cookies['__Secure-refresh-token']
        refresh_payload = jwt.decode(
            refresh_cookie.value, Config.TOKEN_KEY,
            algorithms=Config.TOKEN_ALG,
            issuer=Config.BACKEND_NAME,
            options={
                'require': Config.REFRESH_TOKEN_CLAIMS,
            },
        )

        assert int(refresh_cookie['max-age']) == Config.REFRESH_TOKEN_EXP - time_delta
        assert refresh_cookie['path'] == '/auth/'
        assert refresh_cookie['httponly'] == True
        assert refresh_cookie['samesite'] == 'None'
        assert refresh_cookie['secure'] == True
        
        assert refresh_payload['sub'] == 'user'
        assert refresh_payload['iss'] == Config.BACKEND_NAME
        assert abs(int(refresh_cookie['max-age']) -
            (refresh_payload['exp'] - refresh_payload['iat']) <= 1)


    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'payload, expectation',
        [
            ({}, (401, '{"errors": ["token not in database"]}')),
            ({'exp': dt.now(tz=UTC).timestamp()}, (403, '{"errors": ["the refresh token has expired"]}')),
            ({'exp': 'invalid'}, (401, '{"errors": ["invalid refresh token"]}')),
            ({'iss': 'bad issuer'}, (401, '{"errors": ["invalid iss claim in refresh token"]}')),
            ({'iat': dt.now(tz=UTC).timestamp() + 600}, (403, '{"errors": ["iat claim in the future in refresh token"]}')),
            ({'iat': 'invalid'}, (401, '{"errors": ["invalid iat claim in refresh token"]}')),
        ],
        ids=('token not in db', 'expired', 'bad exp', 'bad issuer', 'future iat', 'invalid iat'),
    )
    async def bad_refresh_payload_refresh_test(self, backend_client, fake_refresh_payload,
                                              payload, expectation):
        fake_refresh_payload.update(payload)
        cookies = {
            '__Secure-refresh-token': jwt.encode(
                fake_refresh_payload, Config.TOKEN_KEY,
                algorithm=Config.TOKEN_ALG,
            ),
        }
        cli = await backend_client
        resp = await cli.get(self.URL, cookies=cookies)
        assert (resp.status, await resp.text()) == expectation
    
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'part_num, expectation',
        [
            (0, (401, '{"errors": ["invalid refresh token"]}')),
            (1, (401, '{"errors": ["invalid refresh token signature"]}')),
            (2, (401, '{"errors": ["invalid refresh token signature"]}')),
        ],
        ids=('bad first part', 'bad second part', 'bad third part'),
    )
    async def invalid_sign_refresh_refresh_test(self, backend_client, fake_refresh_payload,
                                               part_num, expectation):
        token = jwt.encode(
            fake_refresh_payload, Config.TOKEN_KEY,
            algorithm=Config.TOKEN_ALG,
        )
        cookies = {
            '__Secure-refresh-token': '.'.join(
                (part if num != part_num else 'invalid') for num, part in enumerate(token.split('.')))
        }
        cli = await backend_client
        resp = await cli.get(self.URL, cookies=cookies)
        assert (resp.status, await resp.text()) == expectation
    
    @pytest.mark.asyncio
    @pytest.mark.repeat(20)
    async def random_refresh_data_refresh_test(self, backend_client):
        expectation = (401, '{"errors": ["invalid refresh token"]}')
        cli = await backend_client
        cookies = {'__Secure-refresh-token': token_urlsafe(32)}
        resp = await cli.get(self.URL, cookies=cookies)
        assert (resp.status, await resp.text()) == expectation
    
    @pytest.mark.asyncio
    async def without_token_refresh_test(self, backend_client):
        cli = await backend_client
        resp = await cli.get(self.URL)
        assert (resp.status, await resp.text()) == (401, '{"errors": ["the refresh token is missing in request"]}')


@pytest.mark.asyncio(scope="class")
class TestRegistrationEndpoint(TestAuthEndpoints):
    URL = '/auth/registration'

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'data, expectation',
        [
            ({}, (200, '')),
            ({}, (400, '{"errors": ["email already exists"]}')),
            ({'email': 'andrey.ru'}, (400, '{"errors": ["email validation error"]}')),
            ({'email': 'andrey@.ru'}, (400, '{"errors": ["email validation error"]}')),
            ({'email': 'andrey@ru'}, (400, '{"errors": ["email validation error"]}')),
            ({'email': '..andrey@ro.ru'}, (400, '{"errors": ["email validation error"]}')),
            ({'name': 'andrey'}, (400, '{"errors": ["name validation error"]}')),
            ({'secondname': 'shahov'}, (400, '{"errors": ["secondname validation error"]}')),
            ({'patronymic': 'vladimirovich'}, (400, '{"errors": ["patronymic validation error"]}')),
            ({'password': 'qwertyQW'}, (400, '{"errors": ["password validation error"]}')),
            ({'password': '1234qwertyQ  Q'}, (400, '{"errors": ["password validation error"]}')),
            ({'password': '1234qwerty'}, (400, '{"errors": ["password validation error"]}')),
            ({'password': '1234DKFDLKFH'}, (400, '{"errors": ["password validation error"]}')),
            ({'password': '123'}, (400, '{"errors": ["password validation error", "password validation error"]}')),
            ({'birthdate': '100-11-22'}, (400, '{"errors": ["birthdate validation error"]}')),
            ({'birthdate': '2000-14-14'}, (400, '{"errors": ["birthdate validation error"]}')),
            ({'phone': 'qqqww'}, (400, '{"errors": ["phone validation error"]}')),
            ({'phone': '+7'}, (400, '{"errors": ["phone validation error"]}')),
            ({'phone': '8'}, (400, '{"errors": ["phone validation error"]}')),
            ({'class': 0}, (400, '{"errors": ["class validation error"]}')),
            ({'class': '1'}, (400, '{"errors": ["class validation error"]}')),
            ({'email': 'andrey2@yandex.ru'}, (400, '{"errors": ["phone number already exists"]}')),
            ({'email': 'andrey2@yandex.ru', 'phone': '+7877833443'}, (400, '{"errors": ["user already exists"]}')),
            ({'email': 'andrey2@yandex.ru', 'phone': '+7877833443', 'name': 'Эндрю'}, (200, '')),
            ({'email': 'andrey2@yandex.ru', 'phone': '+7877833443', 'name': 'Эндрю'}, (400, '{"errors": ["email already exists"]}')),
        ],
        ids=(
            'success registration', 'email repeat', 'bad email1', 'bad email2', 'bad email3',
            'bad email4', 'bad name chars', 'bad secondname chars',
            'bad patronymic chars', 'password without numbers', 'password with whitespaces',
            'password without capital', 'password without lowercase', 'short password only numbers',
            'bad birthdate', 'bad month birthdate', 'bad phone chars', 'bad phone 2 symbols',
            'bad phone 1 number', 'bad class num', 'bad class type', 'repeat phone', 'repeat full name',
            'success registration', 'email repeat',
        ),
    )
    async def registration_test(self, backend_client, valid_reg_data, data, expectation):
        valid_reg_data.update(data)
        cli = await backend_client
        resp = await cli.post(self.URL, json=valid_reg_data)
        assert (resp.status, await resp.text()) == expectation
    
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'data, expectation',
        [
            ({'class': '1', 'phone': '2'},
            (400, {'class validation error', 'phone validation error'})),
    
            ({'class': '1', 'phone': '2', 'name': 'andrey'},
            (400, {'class validation error', 'phone validation error', 'name validation error'})),
    
            ({'name': 'andrey', 'secondname': 'shahov', 'patronymic': 'vladimirovich'},
            (400, {"name validation error", "secondname validation error", "patronymic validation error"})),
    
            ({'email': 'bad@!@email.ru', 'password': '12Qq', 'birthdate': '2000-0-0'},
            (400, {'email validation error', 'password validation error', 'birthdate validation error'})),
    
            ({
                'email': 'bad@!@email.ru', 'password': '12Qq', 'birthdate': '2000-0-0',
                'name': 'andrey', 'secondname': 'shahov', 'patronymic': 'vladimirovich',
            },
            (400, {
                'email validation error', 'password validation error',
                'birthdate validation error', 'name validation error',
                'secondname validation error', 'patronymic validation error',
            })),
            ({
                'email': 'bad@!@email.ru', 'password': '12Qq', 'birthdate': '2000-0-0',
                'phone': '+7', 'secondname': 'shahov', 'class': '1',
            },
            (400, {
                'email validation error', 'password validation error',
                'birthdate validation error', 'phone validation error',
                'secondname validation error', 'class validation error',
            })),
            ({
                'email': 'bad@!@email.ru', 'password': '12Qq', 'birthdate': '2000-0-0',
                'name': 'andrey', 'secondname': 'shahov', 'patronymic': 'vladimirovich',
                'phone': '+7', 'class': '1',
            },
            (400, {
                'email validation error', 'password validation error',
                'birthdate validation error', 'phone validation error',
                'secondname validation error', 'class validation error',
                'name validation error', 'patronymic validation error',
            })),
        ],
        ids=(
            'class, phone', 'class, phone, name', 'name, secondname, patronymic',
            'email, password, birthdate', 'without class, phone', 'without name, patronymic',
            'all fields',
        )
    )
    async def multiple_errors_registration_test(self, backend_client, valid_reg_data, 
                                                data, expectation):
        valid_reg_data.update(data)
        cli = await backend_client
        resp = await cli.post(self.URL, json=valid_reg_data)
        assert resp.status == expectation[0]
        matched_errors = set(
            error.strip()[1:-1] for error in re.match(
                r'\{"errors": \[((?:(?:".+?")[, ]*){2,})\]\}',
                await resp.text()
            ).group(1).split(',')
        )
        assert matched_errors == expectation[1] 
        
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'key, expectation',
        [
            ('email', (400, '{"errors": ["\'email\' is a required property"]}')),
            ('phone', (400, '{"errors": ["\'phone\' is a required property"]}')),
            ('password', (400, '{"errors": ["\'password\' is a required property"]}')),
            ('birthdate', (400, '{"errors": ["\'birthdate\' is a required property"]}')),
            ('class', (400, '{"errors": ["\'class\' is a required property"]}')),
            ('name', (400, '{"errors": ["\'name\' is a required property"]}')),
            ('secondname', (400, '{"errors": ["\'secondname\' is a required property"]}')),
            ('patronymic', (400, '{"errors": ["\'patronymic\' is a required property"]}')),
        ]
    )
    async def missing_errors_registration_test(self, backend_client, valid_reg_data,
                                               key, expectation):
        valid_reg_data.pop(key)
        cli = await backend_client
        resp = await cli.post(self.URL, json=valid_reg_data)
        assert (resp.status, await resp.text()) == expectation


@pytest.mark.asyncio(scope="class")
class TestLoginEndpoint(TestAuthEndpoints):
    URL = '/auth/login'

    @pytest.fixture
    def valid_reg_data(self):
        data = {
           'email': 'andrey3@yandex.ru',
           'password': '1234qwertyQW',
           'name': 'ААндрей',
           'secondname': 'Шахов',
           'patronymic': 'Владимирович',
           'birthdate': '2000-11-22',
           'phone': '6999992233',
           'class': 1,
        }
        return data
    
    @pytest.mark.asyncio
    async def registration_for_login_endpoint_test(self, backend_client, valid_reg_data):
        cli = await backend_client
        resp = await cli.post('/auth/registration', json=valid_reg_data)
        assert (resp.status, await resp.text()) == (200, '')

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'data, expectation',
        [
            ({'email': 'bad@!@email.ru'}, (400, '{"errors": ["email validation error"]}')),
            ({'email': 'unknown@email.ru'}, (400, '{"errors": ["email not in database"]}')),
            ({'password': '1234'}, (400, '{"errors": ["password validation error"]}')),
        ],
        ids=('invalid email', 'unknown email', 'wrong password'),
    )
    async def fail_login_test(self, data, expectation, backend_client, valid_login_data):
        valid_login_data.update(data)
        cli = await backend_client
        resp = await cli.post(self.URL, json=valid_login_data)
        assert (resp.status, await resp.text()) == expectation
    
    @pytest.mark.asyncio
    @pytest.mark.repeat(5)
    async def login_test(self, backend_client, valid_login_data):
        cli = await backend_client
        resp = await cli.post(self.URL, json=valid_login_data)
        json_response = await resp.json()

        # TODO: move all asserts into function
        assert resp.status == 200
        assert json_response['token_type'] == 'Bearer'
        assert json_response['role'] == 'user'
        assert json_response['expires_in'] == Config.ACCESS_TOKEN_EXP
        assert abs(json_response['expires'] -
            (Config.REFRESH_TOKEN_EXP + dt.now(UTC).timestamp())) <= 1

        access_token = json_response['access_token']
        access_payload = jwt.decode(
            access_token, Config.TOKEN_KEY,
            algorithms=Config.TOKEN_ALG,
            issuer=Config.BACKEND_NAME,
            options={
                'require': Config.ACCESS_TOKEN_CLAIMS,
            },
        )

        assert json_response['role'] == access_payload['sub']
        assert abs(json_response['expires_in'] -
            (access_payload['exp'] - access_payload['iat'])) <= 1

        refresh_cookie = resp.cookies['__Secure-refresh-token']
        refresh_payload = jwt.decode(
            refresh_cookie.value, Config.TOKEN_KEY,
            algorithms=Config.TOKEN_ALG,
            issuer=Config.BACKEND_NAME,
            options={
                'require': Config.REFRESH_TOKEN_CLAIMS,
            },
        )

        assert refresh_cookie['path'] == '/auth/'
        assert refresh_cookie['secure'] == True
        assert refresh_cookie['httponly'] == True
        assert refresh_cookie['samesite'] == 'None'
        assert int(refresh_cookie['max-age']) == Config.REFRESH_TOKEN_EXP
        assert abs(int(refresh_cookie['max-age']) -
            (refresh_payload['exp'] - refresh_payload['iat']) <= 1)


@pytest.mark.asyncio(scope='class')
class TestBehaviour(TestAuthEndpoints):

    @pytest.fixture
    def valid_reg_data(self):
        data = {
           'email': 'andrey4@yandex.ru',
           'password': '1234qwertyQW',
           'name': 'АААндрей',
           'secondname': 'Шахов',
           'patronymic': 'Владимирович',
           'birthdate': '2000-11-22',
           'phone': '6799992233',
           'class': 1,
        }
        return data

    @pytest.mark.asyncio
    async def registration_for_behaviours_test(self, backend_client, valid_reg_data):
        cli = await backend_client
        resp = await cli.post('/auth/registration', json=valid_reg_data)
        assert (resp.status, await resp.text()) == (200, '')
        assert 0
