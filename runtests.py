#!/usr/bin/env python
import optparse
import sys

from django.conf import settings


if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=(
            'reports',
        ),
        SITE_ID=1,
        SECRET_KEY='this-is-just-for-tests-so-not-that-secret',
    )


from django.test.utils import get_runner


def runtests():
    parser = optparse.OptionParser()
    _, tests = parser.parse_args()
    tests = tests or ['reports']

    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True, failfast=False)
    sys.exit(test_runner.run_tests(tests))


if __name__ == '__main__':
    runtests()