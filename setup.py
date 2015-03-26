from setuptools import setup

setup(
    name='knowquiz',
    version='0.2',
    description='a quiz of knownsec inc.',
    license='BSD',
    author='Coyote',
    author_email='chencoyote@gmail.com',
    packages=['knowquiz'],
    zip_safe=False,
    platforms='any',
    scripts=['spider.py']
)
