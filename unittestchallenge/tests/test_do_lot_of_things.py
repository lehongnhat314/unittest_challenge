from unittest.mock import patch
from datetime import datetime, date
from django.conf import settings
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.test import TestCase
from unittestchallenge.sample_function import do_lots_of_things


def mock_validate_is_int(a):
	if not isinstance(a, int):
		raise ValidationError('a is invalid')

def mock_validate_is_string(b):
	if not isinstance(b, str):
		raise ValidationError('b is invalid')

def mock_validate_is_datetime(c):
	if not isinstance(c, datetime):
		raise ValidationError('c is invalid')

def mock_validate_is_next_year(c):
	if c.year != datetime.now().year + 1:
		raise ValidationError('c is not next year')

class DoLotsOfThingsTestCase(TestCase):
	@patch('unittestchallenge.sample_function.validate_is_int', side_effect=mock_validate_is_int)
	@patch('unittestchallenge.sample_function.validate_is_string', side_effect=mock_validate_is_string)
	@patch('unittestchallenge.sample_function.validate_is_datetime', side_effect=mock_validate_is_datetime)
	@patch('unittestchallenge.sample_function.validate_is_next_year', side_effect=mock_validate_is_next_year)
	@patch.object(settings, 'MULTIPLY_A', 5)
	@patch.object(settings, 'ALWAYS_CHECK_C', False)
	def test_do_lots_of_things(self, mocked_f1, mocked_f2, mocked_f3, mocked_f4):
		# Test case: return a * 3
		a = 2
		b = 'bar'
		c = datetime(date.today().year + 1, 1, 1)
		result = do_lots_of_things(a, b, c)
		self.assertEqual(result, a*3)

		# Test case: return a * django.conf.settings.MULTIPLY_A
		a = 2
		b = 'foobar'
		c = datetime(date.today().year + 1, 1, 1)
		result = do_lots_of_things(a, b, c)
		self.assertEqual(result, a * settings.MULTIPLY_A)


		# Test case: fail validate int
		a = '2'
		b = 'foo'
		c = datetime(2023, 1, 1)
		with self.assertRaisesMessage(ValidationError, 'a is invalid'):
			do_lots_of_things(a, b, c)

		# Test case: fail validate str
		a = 2
		b = 5
		c = datetime(2023, 1, 1)
		with self.assertRaisesMessage(ValidationError, 'b is invalid'):
			do_lots_of_things(a, b, c)

		# Test case: fail validate datetime
		a = 2
		b = 'foo'
		c = 'bar'
		with self.assertRaisesMessage(ValidationError, 'c is invalid'):
			do_lots_of_things(a, b, c)

		# Test case: fail next year check
		a = 2
		b = 'bar'
		c = datetime(2023, 1, 1)
		with self.assertRaisesMessage(ValidationError, 'c is not next year'):
			do_lots_of_things(a, b, c)

		# Test case: skipping next year check
		a = 3
		b = 'foo'
		c = datetime(2023, 1, 1)
		result = do_lots_of_things(a, b, c)
		self.assertEqual(result, a * settings.MULTIPLY_A)